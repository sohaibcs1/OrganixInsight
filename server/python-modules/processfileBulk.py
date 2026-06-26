import os
import json
import re
import numpy as np
import pandas as pd
import tifffile
from pathlib import Path
from pylibCZIrw import czi as pyczi
import imageio.v3 as iio   # pip install -U imageio
import psycopg2

# ------------------------------------------------------------
# Color map (with common synonyms)
# ------------------------------------------------------------
color_map = {
    'dapi': (0, 0, 255),
    'hoechst': (0, 0, 255),

    'egfp': (0, 255, 0),
    'gfp': (0, 255, 0),
    'fitc': (0, 255, 0),
    'af488': (0, 255, 0),

    'cy3': (255, 255, 0),      # yellow

    'cy5': (255, 0, 0),
    'af647': (255, 0, 0),
    'rfp': (255, 0, 100),
    'mcher': (255, 0, 100),
    'mcherry': (255, 0, 100),

    'turfp': (255, 103, 0),    # reddish-orange

    'bright': (255, 255, 255), # white
}

# ---------- helpers ----------
def sget(d, path, default=None):
    """Safe deep-get for nested dicts/lists. path is a tuple of keys/indices."""
    cur = d
    try:
        for p in path:
            if isinstance(p, int):
                cur = cur[p]
            else:
                cur = cur.get(p) if isinstance(cur, dict) else getattr(cur, p)
        return cur
    except Exception:
        return default

def get_channel_names_from_metadata(md, fallback_n=1):
    """Try to extract channel names (e.g., DAPI, FITC)."""
    names = []

    # 1) DisplaySetting (common)
    chans = sget(md, ("ImageDocument", "Metadata", "DisplaySetting", "Channels", "Channel"))
    if isinstance(chans, list):
        for ch in chans:
            nm = ch.get("@Name") or ch.get("Name")
            if nm:
                names.append(str(nm))
    elif isinstance(chans, dict):
        nm = chans.get("@Name") or chans.get("Name")
        if nm:
            names = [str(nm)]

    # 2) Alternate path
    if not names:
        chans2 = sget(md, ("ImageDocument", "Metadata", "Information", "Image", "Dimensions", "Channels", "Channel"))
        if isinstance(chans2, list):
            for ch in chans2:
                nm = ch.get("@Name") or ch.get("ShortName") or ch.get("Name")
                if nm:
                    names.append(str(nm))
        elif isinstance(chans2, dict):
            nm = chans2.get("@Name") or chans2.get("ShortName") or chans2.get("Name")
            if nm:
                names = [str(nm)]

    if not names:
        names = [f"C{i}" for i in range(fallback_n)]
    return names

def build_tile_index_from_regions(md):
    """
    Flatten Zeiss RegionsSetup into rows:
      [Well, SceneIndex, TileIndex, TileName]
    """
    tile_regions = sget(
        md,
        ("ImageDocument", "Metadata", "Experiment", "ExperimentBlocks",
         "AcquisitionBlock", "SubDimensionSetups", "RegionsSetup",
         "SampleHolder", "SingleTileRegionArrays", "SingleTileRegionArray"),
        []
    )
    if isinstance(tile_regions, dict):
        tile_regions = [tile_regions]

    rows = []
    for scene_id, region in enumerate(tile_regions):
        well = region.get("@Name", f"Scene_{scene_id}")
        tile_list = sget(region, ("SingleTileRegions", "SingleTileRegion"), [])
        if isinstance(tile_list, dict):
            tile_list = [tile_list]
        if not tile_list:
            rows.append([well, scene_id, 0, "P1"])
            continue
        for tile_id, tile in enumerate(tile_list):
            tile_name = tile.get("@Name", f"P{tile_id + 1}")
            rows.append([well, scene_id, tile_id, tile_name])
    return rows

def _sanitize(name: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(name))
    return safe.strip("_") or "unnamed"

def save_tiff(path, array_cyx, channel_names_only):
    """Save (C,Y,X) array as TIFF with only channel names in ImageDescription."""
    tifffile.imwrite(
        path,
        array_cyx,
        photometric="minisblack",
        metadata={"axes": "CYX"},
        description=json.dumps({"channels": channel_names_only}),
        bigtiff=True
    )

def _best_key_match(name: str, cmap_keys_lower):
    n = (name or "").lower()
    hits = [k for k in cmap_keys_lower if k in n]
    return max(hits, key=len) if hits else None  # prefer the most specific key

# ------------------------------------------------------------
# Normalization utilities
# ------------------------------------------------------------
def robust_percentile_scale(img: np.ndarray, p_low=2.0, p_high=99.8) -> np.ndarray:
    """Per-slice robust percentile scaling to [0,1]."""
    x = img.astype(np.float32, copy=False)
    lo, hi = np.percentile(x, [float(p_low), float(p_high)])
    if not np.isfinite(lo): lo = float(np.min(x))
    if not np.isfinite(hi): hi = float(np.max(x))
    if hi <= lo:
        return np.zeros_like(x, dtype=np.float32)
    y = (x - lo) / (hi - lo)
    return np.clip(y, 0.0, 1.0)

def minmax_scale(img: np.ndarray) -> np.ndarray:
    """Per-slice dynamic min-max scaling to [0,1]."""
    x = img.astype(np.float32, copy=False)
    mn = float(np.min(x))
    mx = float(np.max(x))
    if mx <= mn:
        return np.zeros_like(x, dtype=np.float32)
    y = (x - mn) / (mx - mn)
    return np.clip(y, 0.0, 1.0)

def _robust_norm_with_anchors(
    img: np.ndarray,
    *,
    p_low=2.0,
    p_high=99.8,
    bg_sub_percentile=None,
    lo: float | None = None,
    hi: float | None = None,
) -> np.ndarray:
    """
    Normalize an image to [0,1] using either fixed anchors (lo, hi) or robust percentiles.
    """
    x = img.astype(np.float32, copy=False)

    if bg_sub_percentile is not None:
        bg = np.percentile(x, float(bg_sub_percentile))
        x = x - float(bg)
        x[x < 0] = 0

    if lo is not None and hi is not None:
        if hi <= lo:
            return np.zeros_like(x, dtype=np.float32)
        y = (x - float(lo)) / (float(hi) - float(lo))
        return np.clip(y, 0.0, 1.0)

    return robust_percentile_scale(x, p_low=p_low, p_high=p_high)

def compute_global_channel_anchors(czidoc, df_tiles, export_channels,
                                   p_low=2.0, p_high=99.8, bg_sub_percentile=None):
    """
    Returns dict: {channel_index: (lo_anchor, hi_anchor)}, where each anchor is
    the median across tiles of that channel's p_low / p_high percentiles.
    """
    from collections import defaultdict
    lows = defaultdict(list)
    highs = defaultdict(list)

    for _, row in df_tiles.iterrows():
        scene_idx = int(row["GlobalScene"])
        for c in export_channels:
            try:
                img = np.squeeze(czidoc.read(scene=scene_idx, plane={"C": int(c)})).astype(np.float32)
                x = img
                if bg_sub_percentile is not None:
                    bg = np.percentile(x, float(bg_sub_percentile))
                    x = x - float(bg)
                    x[x < 0] = 0
                lows[c].append(np.percentile(x, float(p_low)))
                highs[c].append(np.percentile(x, float(p_high)))
            except Exception:
                continue

    anchors = {}
    for c in export_channels:
        if lows[c] and highs[c]:
            anchors[c] = (float(np.median(lows[c])), float(np.median(highs[c])))
    return anchors

# ------------------------------------------------------------
# Main RGB composer (scaled only — binary optional if you want later)
# ------------------------------------------------------------
# def save_color_jpg(
#     path,
#     array_cyx: np.ndarray,
#     channel_names: list[str],
#     color_map: dict,
#     *,
#     norm_mode: str = "dynamic",               # "dynamic" | "percentile" | "global"
#     p_low: float = 2.0,
#     p_high: float = 99.8,
#     bg_sub_percentile: float | None = None,
#     per_channel_anchors: dict[int, tuple[float, float]] | None = None,
#     anti_saturation: bool = True,
# ):
#     """
#     Create a color composite JPEG from (C,Y,X) using a chosen normalization mode.
#     """
#     if array_cyx.ndim != 3:
#         raise ValueError("save_color_jpg expects a (C,Y,X) array")
#     C, H, W = array_cyx.shape

#     cmap_keys_lower = [k.lower() for k in color_map.keys()]
#     rgb = np.zeros((H, W, 3), dtype=np.float32)

#     for c in range(C):
#         nm = str(channel_names[c]) if c < len(channel_names) else f"c{c}"
#         key = _best_key_match(nm, cmap_keys_lower)
#         rgb255 = color_map[key] if key is not None else (200, 200, 200)  # safe gray fallback
#         w = np.array(rgb255, dtype=np.float32) / 255.0

#         if norm_mode == "dynamic":
#             ch = minmax_scale(array_cyx[c])
#         elif norm_mode == "percentile":
#             ch = robust_percentile_scale(array_cyx[c], p_low=p_low, p_high=p_high)
#         elif norm_mode == "global":
#             lo_hi = per_channel_anchors.get(c) if per_channel_anchors else None
#             ch = _robust_norm_with_anchors(
#                 array_cyx[c],
#                 p_low=p_low, p_high=p_high,
#                 bg_sub_percentile=bg_sub_percentile,
#                 lo=lo_hi[0] if lo_hi else None,
#                 hi=lo_hi[1] if lo_hi else None,
#             )
#             noise_floor = 0.05  # keep or tune
#             if noise_floor > 0.0:
#                 # move floor to 0, compress range above floor back to [0,1]
#                 denom = max(1.0 - noise_floor, 1e-6)
#                 ch = np.clip((ch - noise_floor) / denom, 0.0, 1.0)
#             else:
#                 ch = np.clip(ch, 0.0, 1.0)
#         else:
#             raise ValueError(f"Unknown norm_mode: {norm_mode}")
#         rgb[..., 0] += ch * w[0]
#         rgb[..., 1] += ch * w[1]
#         rgb[..., 2] += ch * w[2]

#     # Hue-preserving anti-saturation (avoids divide-by-zero warnings)
#     if anti_saturation:
#         maxpix = np.max(rgb, axis=-1, keepdims=True)  # shape (H,W,1)
#         scale = np.ones_like(maxpix, dtype=np.float32)
#         mask = maxpix > 1.0
#         scale[mask] = 1.0 / maxpix[mask]
#         rgb = rgb * scale

#     rgb = np.clip(rgb, 0.0, 1.0)
#     iio.imwrite(path, (rgb * 255.0).astype(np.uint8), quality=90)
def save_color_jpg(
    path,
    array_cyx: np.ndarray,
    channel_names: list[str],
    color_map: dict,
    *,
    norm_mode: str = "global",               # "dynamic" | "percentile" | "global"
    p_low: float = 2.0,
    p_high: float = 99.8,
    bg_sub_percentile: float | None = None,
    per_channel_anchors: dict[int, tuple[float, float]] | None = None,
    anti_saturation: bool = True,
    gamma: float = 0.9,      # brighten midtones (<1 brightens)
    gain: float = 1.1,        # global contrast multiplier
    sat_boost: float = 1.15,  # saturation scaling
):
    """
    Create a color composite JPEG from (C,Y,X) using a chosen normalization mode,
    with optional gamma, gain, and saturation boosts to make colors more visible.
    """
    if array_cyx.ndim != 3:
        raise ValueError("save_color_jpg expects a (C,Y,X) array")
    C, H, W = array_cyx.shape

    cmap_keys_lower = [k.lower() for k in color_map.keys()]
    rgb = np.zeros((H, W, 3), dtype=np.float32)

    for c in range(C):
        nm = str(channel_names[c]) if c < len(channel_names) else f"c{c}"
        key = _best_key_match(nm, cmap_keys_lower)
        rgb255 = color_map[key] if key is not None else (200, 200, 200)  # safe gray fallback
        w = np.array(rgb255, dtype=np.float32) / 255.0

        # --- Normalization modes ---
        if norm_mode == "dynamic":
            ch = minmax_scale(array_cyx[c])
        elif norm_mode == "percentile":
            ch = robust_percentile_scale(array_cyx[c], p_low=p_low, p_high=p_high)
        elif norm_mode == "global":
            lo_hi = per_channel_anchors.get(c) if per_channel_anchors else None
            ch = _robust_norm_with_anchors(
                array_cyx[c],
                p_low=p_low, p_high=p_high,
                bg_sub_percentile=bg_sub_percentile,
                lo=lo_hi[0] if lo_hi else None,
                hi=lo_hi[1] if lo_hi else None,
            )
            noise_floor = 0.05  # tune if needed
            if noise_floor > 0.0:
                denom = max(1.0 - noise_floor, 1e-6)
                ch = np.clip((ch - noise_floor) / denom, 0.0, 1.0)
            else:
                ch = np.clip(ch, 0.0, 1.0)
        else:
            raise ValueError(f"Unknown norm_mode: {norm_mode}")

        rgb[..., 0] += ch * w[0]
        rgb[..., 1] += ch * w[1]
        rgb[..., 2] += ch * w[2]

    # --- Anti-saturation to preserve hue ---
    if anti_saturation:
        maxpix = np.max(rgb, axis=-1, keepdims=True)
        scale = np.ones_like(maxpix, dtype=np.float32)
        mask = maxpix > 1.0
        scale[mask] = 1.0 / maxpix[mask]
        rgb = rgb * scale

    # --- Post-processing boosts ---
    rgb = np.clip(rgb, 0.0, 1.0)

    # 1) Gamma correction
    if gamma != 1.0:
        rgb = np.power(rgb, gamma)

    # 2) Global gain
    if gain != 1.0:
        rgb = np.clip(rgb * gain, 0.0, 1.0)

    # 3) Optional saturation boost
    rgb_u8 = (rgb * 255.0).astype(np.uint8)
    if sat_boost != 1.0:
        import cv2
        hsv = cv2.cvtColor(rgb_u8, cv2.COLOR_RGB2HSV).astype(np.float32)
        hsv[..., 1] = np.clip(hsv[..., 1] * sat_boost, 0, 255)
        rgb_u8 = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    # --- Save ---
    iio.imwrite(path, rgb_u8, quality=90)

def save_jpg(path, array_cyx):
    """Make a grayscale JPEG preview (mean of channels)."""
    if array_cyx.ndim == 3:   # C,Y,X
        img2d = array_cyx.mean(axis=0)
    else:
        img2d = array_cyx

    img2d = img2d.astype(np.float32)
    img2d = (img2d - img2d.min()) / (img2d.ptp() + 1e-6) * 255.0
    img2d = img2d.astype(np.uint8)
    iio.imwrite(path, img2d, quality=90)

# ------------------------------------------------------------
# Tile extraction
# ------------------------------------------------------------
def extract_tiles(
    input_path,
    output_root,
    *,
    norm_mode: str = "global",     # "dynamic" | "percentile" | "global"
    p_low: float = 2.0,
    p_high: float = 99.8,
    bg_sub_percentile: float | None = None,
    anti_saturation: bool = True,
):
    """
    Extract tiles from a .czi into output_root/<Well>/<TileName>.tif + .jpg

    Returns:
      dict: { "A1": ["P1", "P2", ...], "A2": ["P1", ...], ... }
            (one base name per tile; tif & jpg share the base)
    """
    saved, failed = 0, 0
    results = {}  # well -> [base names]
    gmin, gmax = float("inf"), float("-inf")

    input_path = str(input_path)
    if not input_path.lower().endswith(".czi"):
        raise ValueError(f"Input must be a .czi file: {input_path}")

    os.makedirs(output_root, exist_ok=True)
    print(f"[INFO] Reading metadata: {input_path}")
    with pyczi.open_czi(input_path) as czidoc:
        metadata = czidoc.metadata

    rows = build_tile_index_from_regions(metadata)
    if not rows:
        print("[WARN] No RegionsSetup tiles found; nothing to export.")
        return {}

    df_tiles = pd.DataFrame(rows, columns=["Well", "SceneIndex", "TileIndex", "TileName"])
    df_tiles = df_tiles.reset_index().rename(columns={"index": "GlobalScene"})

    chan_names_all = get_channel_names_from_metadata(metadata, fallback_n=1)
    export_channels = list(range(len(chan_names_all)))
    print(f"[INFO] Exporting {len(export_channels)} channels: {chan_names_all}")

    # Compute global per-channel anchors if requested
    per_channel_anchors = None
    if norm_mode == "global":
        with pyczi.open_czi(input_path) as czidoc:
            per_channel_anchors = compute_global_channel_anchors(
                czidoc, df_tiles, export_channels,
                p_low=p_low, p_high=p_high, bg_sub_percentile=bg_sub_percentile
            )
        print("[INFO] Global per-channel anchors:", per_channel_anchors)

    with pyczi.open_czi(input_path) as czidoc:
        for _, row in df_tiles.iterrows():
            well = _sanitize(row["Well"])
            tile_name = _sanitize(row["TileName"])  # base name shared by tif/jpg
            scene_idx = int(row["GlobalScene"])

            well_dir = os.path.join(output_root, well)
            os.makedirs(well_dir, exist_ok=True)
            base_name = f"{well}_{tile_name}"

            tif_path = os.path.join(well_dir, base_name + ".tif")
            jpg_path = os.path.join(well_dir, base_name + ".jpg")

            try:
                channel_imgs, used_names = [], []
                for c in export_channels:
                    try:
                        img = np.squeeze(czidoc.read(scene=scene_idx, plane={"C": int(c)}))
                        vmin = float(np.min(img)); vmax = float(np.max(img))
                        if vmin < gmin: gmin = vmin
                        if vmax > gmax: gmax = vmax
                        channel_imgs.append(img)
                        used_names.append(chan_names_all[c] if c < len(chan_names_all) else f"C{c}")
                    except Exception as ce:
                        print(f"[WARN] Scene {scene_idx} C={c} failed: {ce}")
                        continue

                if not channel_imgs:
                    raise RuntimeError("No channels readable")

                combined = np.stack(channel_imgs, axis=0)

                # Save raw multi-channel TIFF
                save_tiff(tif_path, combined, used_names)

                # Save color JPG (scaled using chosen normalization)
                save_color_jpg(
                    jpg_path, combined, used_names, color_map,
                    norm_mode=norm_mode,
                    p_low=p_low, p_high=p_high,
                    bg_sub_percentile=bg_sub_percentile,
                    per_channel_anchors=per_channel_anchors,
                    anti_saturation=anti_saturation,
                )

                results.setdefault(well, [])
                if tile_name not in results[well]:
                    results[well].append(tile_name)

                saved += 1
                print(f"[OK] {tif_path}, {jpg_path}")

            except Exception as e:
                failed += 1
                print(f"[ERR] {well}/{tile_name}: {e}")

    print(f"\n[DONE] Saved {saved}, Failed {failed}")
    print(f"[INFO] Outputs are under: {output_root}/<Well>/")
    print(f"[GLOBAL] min={gmin}, max={gmax}")
    for k in results:
        results[k].sort()
    return results

# ------------------------------------------------------------
# DB helpers (same logic, with safe closes)
# ------------------------------------------------------------
def execute_query(query, params=None):
    try:
        conn = psycopg2.connect(
            database="datacollection",
            user="new_user",
            host="134.197.75.35",
            password="1234",
            port=5432
        )
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"❌ Database error: {e}")
        return []
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

def execute_insert(query, params=None):
    DB_CONFIG = {
        "database": "datacollection",
        "user": "new_user",
        "host": "134.197.75.35",
        "password": "1234",
        "port": 5432
    }
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Database INSERT error: {e}")
        return False
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

def arrayofFiles(random_id):
    query = "SELECT file_addr FROM file_bulks WHERE experiment_id = %s"
    allfilesarry = execute_query(query, (random_id,))
    return [file[0] for file in allfilesarry]

def getwells(random_id):
    query = "SELECT uuid,study_id,ex_type,phase_info,counterstain,well_number FROM experiments WHERE random_id = %s"
    allfilesarry = execute_query(query, (random_id,))
    return allfilesarry

def normalize_well(s: str) -> str:
    """
    Normalize well IDs like 'A01', 'a1', ' A1_Site1 ' -> 'A1'
    Rules:
      - uppercase
      - strip non-alphanumerics
      - keep only the *leading* [A-Z]+ followed by digits
      - collapse leading zeros in the numeric part
    """
    s = re.sub(r'[^A-Za-z0-9]', '', str(s).upper())
    m = re.match(r'^([A-Z]+)0*([0-9]+)', s)  # only the leading well token
    if m:
        return f"{m.group(1)}{int(m.group(2))}"
    return s

def save_files_metadata(random_id: str, results: dict):
    """
    Insert file rows into `files` table using execute_insert().
    - random_id: the batch id you used to fetch experiments
    - results:   dict from extract_tiles -> {'A1': ['P1','P2',...], 'A2': [...], ...}
    """
    wells = getwells(random_id)
    insert_sql = """
        INSERT INTO files (study_id, experiment_id, ex_type, phase_info, counterstain, file_addr, random_id, file_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Map from normalized well -> original result keys
    norm_to_result_keys = {}
    for k in results.keys():
        nk = normalize_well(k)
        norm_to_result_keys.setdefault(nk, set()).add(k)

    total = 0

    # NOTE: getwells() returns: uuid, study_id, ex_type, phase_info, counterstain, well_number
    for (experiment_id, study_id, ex_type, phase_info, counterstain, well_number) in wells:
        wells_split = [w.strip() for w in str(well_number).split(",") if w.strip()]
        if not wells_split:
            print(f"[WARN] Experiment {experiment_id}: empty well_number; skipping")
            continue

        for raw_well in wells_split:
            want = normalize_well(raw_well)

            matched_result_wells = norm_to_result_keys.get(want, set())
            if not matched_result_wells:
                print(f"[WARN] No extracted tiles matched DB well '{raw_well}' (norm='{want}')")
                continue

            for matched_well in sorted(matched_result_wells):
                tile_bases = results.get(matched_well, [])
                if not tile_bases:
                    print(f"[WARN] Matched well '{matched_well}' has no tiles; skipping")
                    continue

                for tile_base in tile_bases:
                    # Files saved as <Well>_<TileName>.tif; tile_base == TileName (e.g., 'P1')
                    file_addr = f"{matched_well}_{tile_base}.tif"
                    params = (
                        str(study_id),
                        int(experiment_id),
                        str(ex_type),
                        str(phase_info),
                        str(counterstain),
                        file_addr,
                        str(random_id),
                        str(matched_well),  # If this column is truly "file_type", set to 'tif'
                    )
                    ok = execute_insert(insert_sql, params)
                    if ok:
                        total += 1
                        print(f"[OK][INS] exp={experiment_id} db_well='{raw_well}' -> matched_well='{matched_well}' -> {file_addr}")
                    else:
                        print(f"[ERR][INS] exp={experiment_id} db_well='{raw_well}' -> matched_well='{matched_well}' -> {file_addr}")

    print(f"[DONE] Inserted {total} file rows for random_id={random_id}")

def merge_results(dst: dict, src: dict):
    """Merge {well: [bases]} without duplicates."""
    for well, bases in src.items():
        if well not in dst:
            dst[well] = list(bases)
        else:
            # extend without dupes, preserve order
            seen = set(dst[well])
            for b in bases:
                if b not in seen:
                    dst[well].append(b)
                    seen.add(b)

# # ------------------------------------------------------------
# # Example main (adjust/remove for your runtime)
# # ------------------------------------------------------------
# if __name__ == "__main__":
#     # Example usage:
#     randomid = "OUdSMgSN"
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     uploads_dir = os.path.abspath(os.path.join(current_dir, '..', 'uploads'))
#     split_dir = os.path.join("imagesbulk", "randomId" + randomid)

#     namelist = arrayofFiles(randomid)  # e.g., ["file1.czi", "file2.czi"]
#     input_root = uploads_dir

#     aggregated_results = {}
#     for fname in list(namelist):
#         fpath = os.path.join(input_root, fname)
#         print(f"[INFO] Processing {fpath}")
#         try:
#             # Choose one:
#             # norm_mode = "dynamic"      # per-slice min-max (fast previews)
#             # norm_mode = "percentile"   # per-slice robust (less noise)
#             norm_mode = "global"         # global per-channel anchors (comparable)

#             results = extract_tiles(
#                 fpath, split_dir,
#                 norm_mode=norm_mode,
#                 p_low=2, p_high=99.8,
#                 bg_sub_percentile=None,        # e.g., 0.5 or 1.0 if uneven background
#                 anti_saturation=True,
#             )
#             merge_results(aggregated_results, results)
#         except Exception as e:
#             print(f"[ERR] Failed {fname}: {e}")

#     save_files_metadata(randomid, aggregated_results)
