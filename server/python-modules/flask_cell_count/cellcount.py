import os
import uuid
import logging
import threading
import csv
from math import sqrt
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import numpy as np
from flask import Flask, request, send_from_directory, render_template, Response
from skimage.feature import blob_log

import matplotlib
matplotlib.use("Agg")  # headless/server-safe
import matplotlib.pyplot as plt
import io
import base64
from skimage import io as skio, exposure
import psycopg2
import json

# ---------------------------
# Config
# ---------------------------
BASE_ROOT = "/home/msohaib/3D_organixInsight/server/python-modules/imagesbulk"
BASE_ROOT_second ="/home/msohaib/3D_organixInsight/server/uploads"
DEFAULTS = {
    "min_sigma": 4.0,
    "max_sigma": 7.0,
    "threshold": 0.05,
    "dilation_radius": 10,  # used for perinuclear donut; not drawn on main overlay
    # Contrast controls (data-driven Top/Low)
    "top_n": 5,   # high clip = median of top N brightest pixels (0 disables)
    "low_n": 5,   # low clip  = median of bottom N darkest pixels (0 disables)
    # Protein measurement defaults (off by default)
    "protein_measurements": False,
    "protein_region": "nucli",  # "nucli" or "prinucli"
}

# -----------------------------
# Load DB config from JSON file
# -----------------------------
CFG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db_config.json"))
if not os.path.exists(CFG_PATH):
    raise FileNotFoundError(
        f"Config file '{CFG_PATH}' not found. Create it with keys: "
        "{database, user, host, password, port}"
    )

with open(CFG_PATH, "r", encoding="utf-8") as f:
    DB_CFG = json.load(f)

DATA_ROOT = BASE_ROOT  # legacy alias

# ---------------------------
# DB helpers
# ---------------------------
def db_query(query: str, params: Optional[tuple] = None) -> List[tuple]:
    conn = psycopg2.connect(**DB_CFG)
    try:
        with conn, conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    finally:
        conn.close()


def db_execute(query: str, params: Optional[tuple] = None) -> None:
    conn = psycopg2.connect(**DB_CFG)
    try:
        with conn, conn.cursor() as cur:
            cur.execute(query, params or ())
        conn.commit()
    finally:
        conn.close()


def db_execute_many(query: str, rows: List[tuple]) -> None:
    if not rows:
        return
    conn = psycopg2.connect(**DB_CFG)
    try:
        with conn, conn.cursor() as cur:
            cur.executemany(query, rows)
        conn.commit()
    finally:
        conn.close()

def ensure_protein_upsert_index() -> None:
    """
    Ensure a unique key exists on (random_id, experiment_id, file_name, cell_id)
    so we can upsert protein features into model_2d_prots.
    """
    try:
        db_execute("DROP INDEX IF EXISTS model_2d_prots_unique_rid_file_cell")
        db_execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS model_2d_prots_unique_rid_exp_file_cell "
            "ON model_2d_prots (random_id, experiment_id, file_name, cell_id)"
        )
    except Exception as e:
        print(f"[INIT] Could not create protein unique index (ok if it already exists): {e}")


# def ensure_upsert_index() -> None:
#     """
#     Ensure a unique key exists for ON CONFLICT to target.
#     We'll use (random_id, file_name) as the natural key.
#     """
#     try:
#         db_execute(
#             "CREATE UNIQUE INDEX IF NOT EXISTS model_2ds_unique_random_file "
#             "ON model_2ds (random_id, file_name)"
#         )
#     except Exception as e:
#         # Not fatal if you already have another unique constraint; upserts may still work.
#         print(f"[INIT] Could not create unique index (safe to ignore if it already exists): {e}")
def ensure_upsert_index() -> None:
    """
    Ensure a unique key exists for ON CONFLICT to target.
    We'll use (random_id, experiment_id, file_name) as the natural key.
    """
    try:
        # Drop the old index so it stops forcing uniqueness on (random_id, file_name)
        db_execute("DROP INDEX IF EXISTS model_2ds_unique_random_file")

        db_execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS model_2ds_unique_rid_file_exp "
            "ON model_2ds (random_id, experiment_id, file_name)"
        )
    except Exception as e:
        print(f"[INIT] Could not create unique index (safe to ignore if it already exists): {e}")

# ---------------------------
# Metadata helpers
# ---------------------------
def normalize_rid(raw: str) -> str:
    """
    Normalize ONLY for DB insert (and for searching metadata):
    'randomIdOUdSMgSN' -> 'OUdSMgSN'; otherwise return as-is.
    """
    s = (raw or "").strip()
    if s.lower().startswith("randomid"):
        s = s[len("randomid"):]
    return s

def _array_to_data_url(arr: np.ndarray, *, cmap: str = "gray", title: Optional[str] = None) -> str:
    fig, ax = plt.subplots()
    ax.imshow(arr, cmap=cmap)
    if title:
        ax.set_title(title)
    ax.axis("off")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('ascii')}"

def load_metadata_map_for_rid(rid: str) -> Dict[str, List[Tuple[Optional[str], Optional[str], str]]]:
    """
    Build mapping trying BOTH the raw rid and normalized rid:
        basename(file_addr) -> [
            (study_id, experiment_id, random_id-from-DB),
            ...
        ]
    So the same TIFF can belong to many experiments.
    """
    rid_raw = (rid or "").strip()
    rid_norm = normalize_rid(rid_raw)

    meta_map: Dict[str, List[Tuple[Optional[str], Optional[str], str]]] = {}

    if rid_norm != rid_raw:
        q = """
            SELECT study_id, experiment_id, random_id, file_addr
            FROM files
            WHERE random_id IN (%s, %s)
        """
        rows = db_query(q, (rid_raw, rid_norm))
    else:
        q = """
            SELECT study_id, experiment_id, random_id, file_addr
            FROM files
            WHERE random_id = %s
        """
        rows = db_query(q, (rid_raw,))

    for study_id, experiment_id, random_id_db, file_addr in rows:
        base = Path(str(file_addr)).name
        meta_map.setdefault(base, []).append((study_id, experiment_id, random_id_db))

    logging.info(
        f"[META MAP] rid_raw='{rid_raw}' rid_norm='{rid_norm}' -> "
        f"{len(meta_map)} unique files, {len(rows)} file rows"
    )
    return meta_map
# def load_metadata_map_for_rid(rid: str) -> Dict[str, Tuple[Optional[str], Optional[str], str]]:
#     """
#     Build mapping trying BOTH the raw rid and normalized rid:
#         basename(file_addr) -> (study_id, experiment_id, random_id-from-DB)
#     This fixes 'no metadata in DB' when the DB stores 'OUdSMgSN' but the UI uses 'randomIdOUdSMgSN'.
#     """
#     rid_raw = (rid or "").strip()
#     rid_norm = normalize_rid(rid_raw)

#     meta_map: Dict[str, Tuple[Optional[str], Optional[str], str]] = {}
#     if rid_norm != rid_raw:
#         q = """
#             SELECT study_id, experiment_id, random_id, file_addr
#             FROM files
#             WHERE random_id IN (%s, %s)
#         """
#         rows = db_query(q, (rid_raw, rid_norm))
#     else:
#         q = """
#             SELECT study_id, experiment_id, random_id, file_addr
#             FROM files
#             WHERE random_id = %s
#         """
#         rows = db_query(q, (rid_raw,))

#     for study_id, experiment_id, random_id_db, file_addr in rows:
#         base = Path(str(file_addr)).name
#         prev = meta_map.get(base)
#         # prefer normalized form if duplicates for same basename appear
#         if (not prev) or (normalize_rid(random_id_db) == random_id_db):
#             meta_map[base] = (study_id, experiment_id, random_id_db)

#     logging.info(f"[META MAP] rid_raw='{rid_raw}' rid_norm='{rid_norm}' -> {len(meta_map)} items")
#     return meta_map

# ---------------------------
# File & path helpers
# ---------------------------
def list_all_files(root_dir, extensions=None):
    all_files = []
    for r, d, f in os.walk(root_dir):
        for file in f:
            if extensions is None or file.lower().endswith(tuple(extensions)):
                all_files.append(os.path.join(r, file))
    return all_files


def _is_safe_token(s: str) -> bool:
    return bool(s) and all(ch.isalnum() or ch in "-_" for ch in s)


# def _subdir_from_filename(fname: str) -> str:
#     stem = Path(fname).name
#     base = Path(stem).stem
#     prefix = base.split("_", 1)[0] if "_" in base else base
#     return prefix
def _subdir_from_filename(fname: str) -> str:
    fname = Path(fname).name

    # remove double extensions like .ome.tif / .ome.tiff
    lower = fname.lower()
    if lower.endswith(".ome.tif"):
        base = fname[:-8]
    elif lower.endswith(".ome.tiff"):
        base = fname[:-9]
    else:
        base = Path(fname).stem

    prefix = base.split("_", 1)[0] if "_" in base else base
    return prefix

def resolve_by_rule(random_id: str, filename: str) -> str:
    """
    Resolve an image path using exactly two allowed layouts:

      1) imagesbulk/<rid>/<prefix>/<file>
      2) uploads/<file>

    <prefix> is derived from filename before first "_" OR full stem if no "_".
    """
    rid = (random_id or "").strip()
    if not rid:
        raise ValueError("Missing 'rid'. Provide ?rid=<random_id>.")
    if not _is_safe_token(rid):
        raise ValueError("Invalid 'rid'. Allowed: A-Z a-z 0-9 - _")

    if os.path.isabs(filename):
        raise ValueError("Filename must be a basename, not absolute.")

    fname = Path(filename).name
    subdir = _subdir_from_filename(fname)

    if not _is_safe_token(subdir):
        raise ValueError(f"Invalid prefix from filename: {subdir}")

    # 1) imagesbulk/<rid>/<prefix>/<file>
    p1 = os.path.abspath(os.path.join(BASE_ROOT, rid, subdir, fname))

    # 2) uploads/<file>
    p2 = os.path.abspath(os.path.join(BASE_ROOT_second, fname))

    for p in (p1, p2):
        if os.path.exists(p):
            return p

    raise FileNotFoundError(
        "File not found in allowed base paths:\n"
        f"- {p1}\n"
        f"- {p2}"
    )




# ---------------------------
# Image pipeline
# ---------------------------
def load_grayscale(path: str) -> np.ndarray:
    img = skio.imread(path)
    arr = np.asarray(img)

    if arr.ndim == 2:
        return arr

    arr = np.squeeze(arr)
    if arr.ndim == 2:
        return arr

    if arr.ndim == 3:
        if arr.shape[-1] <= 4:  # (Y,X,C)
            return arr[..., 0]
        if arr.shape[0] <= 4:   # (C,Y,X)
            return arr[0, ...]
        return arr[0, ...]      # (Z/T,Y,X)

    if arr.ndim == 4:
        if arr.shape[-1] <= 4:  # (Z/T,Y,X,C)
            return arr[0, ..., 0]
        if arr.shape[1] <= 4:   # (Z/T,C,Y,X)
            return arr[0, 0, ...]
        return arr.reshape((-1,) + arr.shape[-2:])[0]

    return arr.reshape((-1,) + arr.shape[-2:])[0]


def load_dapi_and_marker(path: str) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Load DAPI (channel 0) and marker (channel 1) from a multi-dimensional TIFF/CZI.
    Falls back to single-channel if only one is present.
    Supports: (Y,X), (Z,Y,X), (C,Y,X), (Y,X,C), (Z,C,Y,X), (Z,Y,X,C) etc.
    """
    arr = np.asarray(skio.imread(path))
    arr = np.squeeze(arr)

    # If single 2D plane
    if arr.ndim == 2:
        return arr, None

    # (Y, X, C)
    if arr.ndim == 3 and arr.shape[-1] <= 8:
        dapi = arr[..., 0]
        marker = arr[..., 1] if arr.shape[-1] >= 2 else None
        return dapi, marker

    # (C, Y, X)
    if arr.ndim == 3 and arr.shape[0] <= 8:
        dapi = arr[0, ...]
        marker = arr[1, ...] if arr.shape[0] >= 2 else None
        return dapi, marker

    # (Z, Y, X) -> take first Z
    if arr.ndim == 3:
        return arr[0, ...], None

    # (Z, Y, X, C)
    if arr.ndim == 4 and arr.shape[-1] <= 8:
        dapi = arr[0, ..., 0]
        marker = arr[0, ..., 1] if arr.shape[-1] >= 2 else None
        return dapi, marker

    # (Z, C, Y, X)
    if arr.ndim == 4 and arr.shape[1] <= 8:
        dapi = arr[0, 0, ...]
        marker = arr[0, 1, ...] if arr.shape[1] >= 2 else None
        return dapi, marker

    # Fallback: flatten leading dims, take first plane
    flat = arr.reshape((-1,) + arr.shape[-2:])
    return flat[0], None


def _clip_from_top_low(image: np.ndarray, top_n: int, low_n: int) -> Tuple[Optional[float], Optional[float]]:
    """
    Returns (low_clip, high_clip):
      low_clip  = median of darkest low_n pixels (if low_n>0)
      high_clip = median of brightest top_n pixels (if top_n>0)
    """
    arr = np.asarray(image).astype(np.float64, copy=False).ravel()
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return (None, None)

    # Clip extremes to reduce outlier dominance
    lo_cap = np.percentile(arr, 0.05)     # bottom 0.05% cutoff
    hi_cap = np.percentile(arr, 99.95)    # top 0.05% cutoff
    arr = np.clip(arr, lo_cap, hi_cap)

    # Low side
    if low_n > 0:
        ln = int(min(low_n, arr.size))
        low_part = np.partition(arr, ln - 1)[:ln]
        low_clip = float(np.median(low_part))
    else:
        low_clip = None

    # High side
    if top_n > 0:
        tn = int(min(top_n, arr.size))
        high_part = np.partition(arr, arr.size - tn)[-tn:]
        high_clip = float(np.median(high_part))
    else:
        high_clip = None

    return (low_clip, high_clip)


def preprocess_image_toplow(image: np.ndarray, *, top_n: int, low_n: int) -> np.ndarray:
    if image is None:
        return None
    low_clip, high_clip = _clip_from_top_low(image, top_n=top_n, low_n=low_n)

    # If neither side is set, just return original
    if low_clip is None and high_clip is None:
        return image

    # Build in_range
    if low_clip is None:
        in_range = (np.min(image), high_clip)
    elif high_clip is None:
        in_range = (low_clip, np.max(image))
    else:
        in_range = (low_clip, high_clip)

    # Safety: if inverted, skip stretch
    if in_range[1] <= in_range[0]:
        return image

    return exposure.rescale_intensity(image, in_range=in_range)


def detect_blobs(image: np.ndarray, min_sigma: float, max_sigma: float, threshold: float) -> np.ndarray:
    blobs = blob_log(
        image,
        min_sigma=min_sigma,
        max_sigma=max_sigma,
        threshold=threshold,
        overlap=0.25,
        log_scale=True,
    )
    if blobs.size:
        blobs[:, 2] = blobs[:, 2] * sqrt(2)
    return blobs


def analyze_one_image_overlay(
    image_path: str,
    min_sigma: float,
    max_sigma: float,
    threshold: float,
    dilation_radius: int,
    top_n: int,
    low_n: int,
    protein_measurements: bool,
    protein_region: str,
) -> Tuple[int, str, str, Optional[str]]:
    """
    Returns:
      count,
      right_data_url (processed + yellow blobs),
      left_data_url  (processed no overlay),
      marker_data_url (marker + red circles) if protein_measurements is True and ch1 exists else None
    """
    # Channels
    dapi_raw, marker_raw = load_dapi_and_marker(image_path)
    # Process (contrast)
    dapi = preprocess_image_toplow(dapi_raw, top_n=top_n, low_n=low_n)
    marker = preprocess_image_toplow(marker_raw, top_n=top_n, low_n=low_n) if marker_raw is not None else None

    # Detect on processed DAPI
    blobs = detect_blobs(dapi, min_sigma=min_sigma, max_sigma=max_sigma, threshold=threshold)

    # LEFT: processed (no overlay)
    left_data_url = _array_to_data_url(dapi, cmap="gray", title="Processed (no overlay)")

    # RIGHT: processed + yellow blobs
    fig1, ax1 = plt.subplots()
    ax1.imshow(dapi, cmap="gray")
    for (y, x, r) in blobs:
        ax1.add_patch(plt.Circle((x, y), r, color="yellow", linewidth=0.9, fill=False))
    ax1.set_title(f"Processed + Blobs ({len(blobs)} cells)")
    ax1.axis("off")
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png", dpi=150, bbox_inches="tight", pad_inches=0)
    plt.close(fig1)
    buf1.seek(0)
    right_data_url = f"data:image/png;base64,{base64.b64encode(buf1.read()).decode('ascii')}"

    # THIRD: marker + red circles (only if checkbox is on AND marker exists)
    marker_data_url = None
    if protein_measurements and (marker is not None):
        fig2, ax2 = plt.subplots()
        ax2.imshow(marker, cmap="gray")
        title = "Marker (ch1) + Nuclear Circles" if protein_region == "nucli" else f"Marker (ch1) + Perinuclear (r + {dilation_radius}px)"
        ax2.set_title(title)
        for (y, x, r) in blobs:
            y = float(y); x = float(x); r = float(r)
            # always draw inner nuclear circle
            ax2.add_patch(plt.Circle((x, y), r, color="red", linewidth=0.9, fill=False))
            # draw outer perinuclear ring only in prinucli
            if protein_region == "prinucli":
                ax2.add_patch(plt.Circle((x, y), r + float(dilation_radius), color="red", linewidth=0.9, fill=False))
        ax2.axis("off")
        buf2 = io.BytesIO()
        fig2.savefig(buf2, format="png", dpi=150, bbox_inches="tight", pad_inches=0)
        plt.close(fig2)
        buf2.seek(0)
        marker_data_url = f"data:image/png;base64,{base64.b64encode(buf2.read()).decode('ascii')}"

    return int(len(blobs)), right_data_url, left_data_url, marker_data_url


def count_only(image_path: str, *, min_sigma: float, max_sigma: float, threshold: float, top_n: int, low_n: int) -> int:
    img = load_grayscale(image_path)
    img_p = preprocess_image_toplow(img, top_n=top_n, low_n=low_n)
    blobs = detect_blobs(img_p, min_sigma=min_sigma, max_sigma=max_sigma, threshold=threshold)
    return int(len(blobs))


def _measure_cells_for_file(
    img_path: str,
    *,
    min_sigma: float,
    max_sigma: float,
    threshold: float,
    top_n: int,
    low_n: int,
    protein_region: str,     # "nucli" or "prinucli"
    dilation_radius: int
) -> List[Dict]:
    """
    Per-image, per-cell mean measurements (RAW signal).

    Detection:
      - Find blobs on *processed* DAPI for robustness.

    Quantification (means):
      - Use RAW DAPI and RAW marker arrays (float32).
      - Compute both nuclear and perinuclear marker means, but:
        * If protein_region == "nucli":   save nuclear mean in mean_nucli
        * If protein_region == "prinucli": save perinuclear mean in mean_nucli
      - mean_peri_nucli is always set to NaN (so DB stores NULL).
      - mean_dapi is the nuclear mean of RAW DAPI.

    Returns
    -------
    List[Dict]
      Each dict:
        {
          "file_name": <basename>,
          "cell_id":   <1-based>,
          "mean_dapi": <float or NaN>,
          "mean_nucli": <active-region marker mean>,
          "mean_peri_nucli": NaN
        }
    """
    # ---------- Load channels ----------
    dapi_raw, marker_raw = load_dapi_and_marker(img_path)

    # Processed images only for detection/visualization (not for quant)
    dapi_vis = preprocess_image_toplow(dapi_raw,   top_n=top_n, low_n=low_n)
    # marker_vis is not needed for quant; skip to save memory

    # Quantification arrays = RAW float32
    dapi_q   = dapi_raw.astype(np.float32, copy=False)
    marker_q = marker_raw.astype(np.float32, copy=False) if marker_raw is not None else None

    # ---------- Detect blobs on processed DAPI ----------
    blobs = detect_blobs(dapi_vis, min_sigma=min_sigma, max_sigma=max_sigma, threshold=threshold)

    rows: List[Dict] = []
    H, W = dapi_q.shape
    fname = Path(img_path).name

    # Global coordinate grids (for fast mask math)
    rr_full, cc_full = np.ogrid[:H, :W]

    # Precompute a mask of ALL nuclei (to exclude ANY nucleus from perinuclear rings)
    nuclei_all = np.zeros((H, W), dtype=bool)
    for (y0, x0, r0) in blobs:
        y0 = int(round(float(y0))); x0 = int(round(float(x0))); r0 = int(round(float(r0)))
        if r0 <= 0:
            continue
        nuclei_all |= ((rr_full - y0)**2 + (cc_full - x0)**2) <= (r0**2)

    # Normalize region flag
    region = str(protein_region).strip().lower()
    if region not in ("nucli", "prinucli"):
        region = "nucli"

    # ---------- Per-cell loop ----------
    for i, (y, x, r) in enumerate(blobs):
        y = int(round(float(y))); x = int(round(float(x))); r = int(round(float(r)))
        if r <= 0:
            continue

        # Nuclear mask for this cell
        nuc_mask = ((rr_full - y)**2 + (cc_full - x)**2) <= (r**2)

        # RAW DAPI mean inside nucleus
        dapi_vals = dapi_q[nuc_mask]
        mean_dapi = float(np.mean(dapi_vals)) if dapi_vals.size else np.nan

        # Compute both nuclear and perinuclear marker means (if marker exists)
        nuclear_marker_mean = np.nan
        perinuclear_marker_mean = np.nan

        if marker_q is not None:
            # Nuclear marker mean
            mvals_n = marker_q[nuc_mask]
            nuclear_marker_mean = float(np.mean(mvals_n)) if mvals_n.size else np.nan

            # Perinuclear donut: between r and r+dilation_radius, excluding ALL nuclei
            R_out = max(r + int(dilation_radius), r + 1)
            outer = ((rr_full - y)**2 + (cc_full - x)**2) <= (R_out**2)
            donut = outer & (~nuc_mask) & (~nuclei_all)
            mvals_p = marker_q[donut]
            perinuclear_marker_mean = float(np.mean(mvals_p)) if mvals_p.size else np.nan

        # ---- IMPORTANT SAVING RULE ----
        # Save the ACTIVE region mean into 'mean_nucli'
        # and set 'mean_peri_nucli' to NaN to store NULL in DB.
        # if region == "prinucli":
        #     saved_mean = perinuclear_marker_mean
        # else:
        #     saved_mean = nuclear_marker_mean
        # ---- IMPORTANT SAVING RULE ----
# Fallback: if marker missing → use DAPI mean
        if region == "prinucli":
            saved_mean = perinuclear_marker_mean if not np.isnan(perinuclear_marker_mean) else mean_dapi
        else:
            saved_mean = nuclear_marker_mean if not np.isnan(nuclear_marker_mean) else mean_dapi

        rows.append({
            "file_name": fname,
            "cell_id": i + 1,          # 1-based id (keeps your convention)
            "mean_dapi": mean_dapi,
            "mean_nucli": saved_mean,  # <- chosen region is always written here
            "mean_peri_nucli": np.nan  # <- always NaN (NULL in DB)
        })

    return rows


def run_bulk_counts(
    *, files: List[str], rid: str, min_sigma: float, max_sigma: float, threshold: float,
    dilation_radius: int, top_n: int, low_n: int
) -> List[Dict]:
    results: List[Dict] = []
    for name in files:
        try:
            if os.path.isabs(name):
                raise ValueError("Absolute paths are not allowed in BULK_FILENAMES under the new rule.")
            fp = resolve_by_rule(rid, name)
            if not os.path.exists(fp):
                raise FileNotFoundError(fp)
            cnt = count_only(
                fp,
                min_sigma=min_sigma,
                max_sigma=max_sigma,
                threshold=threshold,
                top_n=top_n,
                low_n=low_n,
            )
            item = {"file": fp, "count": cnt}
        except Exception as ex:
            logging.error(f"[BULK] {name}: {ex}")
            item = {"file": name, "count": None, "error": str(ex)}
        results.append(item)
    return results

# ---------------------------
# Flask app
# ---------------------------
app = Flask(__name__, template_folder="templates", static_folder="static")
RESULT_DIR = os.path.join(app.static_folder, "results")
os.makedirs(RESULT_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("cellcount")

# Shared state
BULK_FILENAMES: List[str] = []  # basenames
LAST_PARAMS = DEFAULTS.copy()
LAST_CONTEXT = {"rid": ""}      # store RAW rid (as user passed)
JOBS: Dict[str, Dict] = {}      # job_id -> {'csv_path': str|None}

# ---------------------------
# Self-healing helpers for bulk
# ---------------------------
def refresh_filenames_from_db(rid: str) -> List[str]:
    meta_map = load_metadata_map_for_rid(rid)
    return sorted(list(meta_map.keys()))


def scan_filesystem_for_rid(rid: str) -> List[str]:
    found = []
    rid_root = os.path.join(BASE_ROOT, rid)
    if not os.path.isdir(rid_root):
        return found
    for r, d, f in os.walk(rid_root):
        for file in f:
            low = file.lower()
            if low.endswith(".tif") or low.endswith(".tiff"):
                found.append(Path(file).name)
    return sorted(list(set(found)))

# ---------------------------
# Background worker (counts CSV + optional measurements CSV + DB upsert)
# ---------------------------
def _bulk_worker(job_id: str, *, rid: str, params: Dict, files: List[str]) -> None:
    """
    Background worker:
      - COUNTS CSV:     bulk_<job_id>.csv
      - MEASUREMENTS CSV (optional): measurements_<job_id>.csv
      - DB upserts:
          model_2ds       on (random_id, file_name)
          model_2d_prots  on (random_id, file_name, cell_id)
    """
    try:
        meta_map = load_metadata_map_for_rid(rid)  # basename -> (study_id, experiment_id, random_id-from-DB)
        print(f"[JOB {job_id}] Started bulk run with {len(files)} files (rid={rid}).")

        # ====== COUNTS ======
        results = run_bulk_counts(
            files=files,
            rid=rid,
            min_sigma=float(params["min_sigma"]),
            max_sigma=float(params["max_sigma"]),
            threshold=float(params["threshold"]),
            dilation_radius=int(params["dilation_radius"]),
            top_n=int(params["top_n"]),
            low_n=int(params["low_n"]),
        )

        # counts_csv = os.path.join(RESULT_DIR, f"bulk_{job_id}.csv")
        # ok = err = processed = 0
        # sum_counts = 0
        # rows_for_db: List[tuple] = []  # (study_id, experiment_id, random_id_norm, file_name, cell_count)

        # with open(counts_csv, "w", newline="") as f:
        #     writer = csv.writer(f)
        #     writer.writerow(["study_id", "experiment_id", "random_id", "file_name", "cell_count", "error"])

        #     for row in results:
        #         processed += 1
        #         fname = Path(str(row.get("file", ""))).name  # basename only
        #         meta = meta_map.get(fname)

        #         if row.get("error"):
        #             err += 1
        #             cell_count = None
        #             error_msg = row["error"]
        #             print(f"[JOB {job_id}] {fname} -> ERROR: {error_msg}")
        #         else:
        #             cell_count = int(row.get("count", 0))
        #             ok += 1
        #             sum_counts += cell_count
        #             error_msg = ""
        #             print(f"[JOB {job_id}] {fname} -> {cell_count} cells")

        #         if meta is None:
        #             # No metadata in DB; still write CSV with rid for traceability
        #             writer.writerow([None, None, rid, fname, cell_count, "no metadata in DB (files table) for rid"])
        #             continue

        #         study_id, experiment_id, db_random_id = meta  # keep DB's random_id AS-IS in CSV
        #         writer.writerow([study_id, experiment_id, db_random_id, fname, cell_count, error_msg])

        #         # DB upsert uses normalized random_id for the key
        #         rows_for_db.append((study_id, experiment_id, normalize_rid(db_random_id), fname, cell_count))
        counts_csv = os.path.join(RESULT_DIR, f"bulk_{job_id}.csv")
        ok = err = processed = 0
        sum_counts = 0
        rows_for_db: List[tuple] = []  # (study_id, experiment_id, random_id_norm, file_name, cell_count)

        with open(counts_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["study_id", "experiment_id", "random_id", "file_name", "cell_count", "error"])

            for row in results:
                processed += 1
                fname = Path(str(row.get("file", ""))).name  # basename only
                meta_list = meta_map.get(fname)  # <-- now a list of (study_id, experiment_id, random_id_db)

                if row.get("error"):
                    err += 1
                    cell_count = None
                    error_msg = row["error"]
                    print(f"[JOB {job_id}] {fname} -> ERROR: {error_msg}")

                    # keep old behaviour for 'no metadata' case
                    writer.writerow([None, None, rid, fname, cell_count, error_msg])
                    continue

                cell_count = int(row.get("count", 0))
                ok += 1
                sum_counts += cell_count
                error_msg = ""
                print(f"[JOB {job_id}] {fname} -> {cell_count} cells")

                # If no metadata, write one generic row (same as before)
                if not meta_list:
                    writer.writerow([None, None, rid, fname, cell_count, "no metadata in DB (files table) for rid"])
                    continue

                # For EACH experiment that uses this file, write a row
                for (study_id, experiment_id, db_random_id) in meta_list:
                    writer.writerow([study_id, experiment_id, db_random_id, fname, cell_count, error_msg])
                    rows_for_db.append(
                        (study_id, experiment_id, normalize_rid(db_random_id), fname, cell_count))

        # Upsert COUNTS into model_2ds
        # upsert_counts_q = """
        #     INSERT INTO model_2ds (study_id, experiment_id, random_id, file_name, cell_count)
        #     VALUES (%s, %s, %s, %s, %s)
        #     ON CONFLICT (random_id, file_name)
        #     DO UPDATE SET
        #         study_id = EXCLUDED.study_id,
        #         experiment_id = EXCLUDED.experiment_id,
        #         cell_count = EXCLUDED.cell_count
        # """
        # db_execute_many(upsert_counts_q, rows_for_db)

        upsert_counts_q = """
            INSERT INTO model_2ds (study_id, experiment_id, random_id, file_name, cell_count)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (random_id, experiment_id, file_name)
            DO UPDATE SET
                study_id   = EXCLUDED.study_id,
                cell_count = EXCLUDED.cell_count
        """

        # ✅ actually insert/update in DB
        db_execute_many(upsert_counts_q, rows_for_db)

        print(f"[JOB {job_id}] COUNT DONE. Processed={processed}, OK={ok}, ERRORS={err}, SUM_COUNTS={sum_counts}")
        print(f"[JOB {job_id}] Counts CSV: {counts_csv}")
        print(f"[JOB {job_id}] Upserted {len(rows_for_db)} rows into model_2ds")


        # Base job metadata
        job_meta: Dict[str, Optional[str]] = {"csv_path": counts_csv}

        # ====== MEASUREMENTS (optional) ======
        if bool(params.get("protein_measurements", False)):
            protein_region = str(params.get("protein_region", "nucli")).lower()
            if protein_region not in ("nucli", "prinucli"):
                protein_region = "nucli"

            dilation_radius = int(params.get("dilation_radius", 10))
            min_sigma = float(params["min_sigma"])
            max_sigma = float(params["max_sigma"])
            threshold = float(params["threshold"])
            top_n = int(params["top_n"])
            low_n = int(params["low_n"])

            measurements_csv = os.path.join(RESULT_DIR, f"measurements_{job_id}.csv")
            rows_for_prot_db: List[tuple] = []  # (study_id, experiment_id, random_id_norm, file_name, cell_id, mean_dapi, mean_nucli, mean_peri_nucli)

            with open(measurements_csv, "w", newline="") as f:
                writer = csv.writer(f)
                # EXACT schema requested
                header = ["study_id", "experiment_id", "random_id", "file_name", "cell_id",
                          "mean_dapi", "mean_nucli", "mean_peri_nucli"]
                writer.writerow(header)

                for name in files:
                    try:
                        if os.path.isabs(name):
                            raise ValueError("Absolute paths not allowed in bulk file list.")
                        fp = resolve_by_rule(rid, name)
                        if not os.path.exists(fp):
                            raise FileNotFoundError(fp)

                        # fname = Path(name).name
                        # meta = meta_map.get(fname)
                        # # defaults if metadata missing
                        # study_id, experiment_id, db_random_id = (None, None, rid)
                        # if meta is not None:
                        #     study_id, experiment_id, db_random_id = meta

                        # # compute mean-only rows
                        # meas_rows = _measure_cells_for_file(
                        #     fp,
                        #     min_sigma=min_sigma,
                        #     max_sigma=max_sigma,
                        #     threshold=threshold,
                        #     top_n=top_n,
                        #     low_n=low_n,
                        #     protein_region=protein_region,
                        #     dilation_radius=dilation_radius
                        # )

                        # for r in meas_rows:
                        #     writer.writerow([
                        #         study_id, experiment_id, db_random_id,
                        #         r["file_name"], r["cell_id"],
                        #         r["mean_dapi"], r["mean_nucli"], r["mean_peri_nucli"]
                        #     ])
                        #     rows_for_prot_db.append((
                        #         study_id,
                        #         experiment_id,
                        #         normalize_rid(db_random_id),
                        #         r["file_name"],
                        #         int(r["cell_id"]),
                        #         r["mean_dapi"],
                        #         r["mean_nucli"],
                        #         r["mean_peri_nucli"],
                        #     ))
                        fname = Path(name).name
                        meta_list = meta_map.get(fname)

                        # defaults if metadata missing
                        if not meta_list:
                            meta_list = [(None, None, rid)]

                        meas_rows = _measure_cells_for_file(
                            fp,
                            min_sigma=min_sigma,
                            max_sigma=max_sigma,
                            threshold=threshold,
                            top_n=top_n,
                            low_n=low_n,
                            protein_region=protein_region,
                            dilation_radius=dilation_radius
                        )

                        for (study_id, experiment_id, db_random_id) in meta_list:
                            for r in meas_rows:
                                writer.writerow([
                                    study_id, experiment_id, db_random_id,
                                    r["file_name"], r["cell_id"],
                                    r["mean_dapi"], r["mean_nucli"], r["mean_peri_nucli"]
                                ])
                                rows_for_prot_db.append((
                                    study_id,
                                    experiment_id,
                                    normalize_rid(db_random_id),
                                    r["file_name"],
                                    int(r["cell_id"]),
                                    r["mean_dapi"],
                                    r["mean_nucli"],
                                    r["mean_peri_nucli"],
                                ))

                        print(f"[JOB {job_id}] measurements -> {fname}: {len(meas_rows)} nuclei")

                    except Exception as ex:
                        print(f"[JOB {job_id}] measurements ERROR for {name}: {ex}")

            # Upsert MEASUREMENTS into model_2d_prots
            # upsert_prot_q = """
            #     INSERT INTO model_2d_prots
            #         (study_id, experiment_id, random_id, file_name, cell_id,
            #          mean_dapi, mean_nucli, mean_peri_nucli)
            #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            #     ON CONFLICT (random_id, file_name, cell_id)
            #     DO UPDATE SET
            #         study_id = EXCLUDED.study_id,
            #         experiment_id = EXCLUDED.experiment_id,
            #         mean_dapi = EXCLUDED.mean_dapi,
            #         mean_nucli = EXCLUDED.mean_nucli,
            #         mean_peri_nucli = EXCLUDED.mean_peri_nucli
            # """
            upsert_prot_q = """
                INSERT INTO model_2d_prots
                    (study_id, experiment_id, random_id, file_name, cell_id,
                    mean_dapi, mean_nucli, mean_peri_nucli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (random_id, experiment_id, file_name, cell_id)
                DO UPDATE SET
                    study_id        = EXCLUDED.study_id,
                    experiment_id   = EXCLUDED.experiment_id,
                    mean_dapi       = EXCLUDED.mean_dapi,
                    mean_nucli      = EXCLUDED.mean_nucli,
                    mean_peri_nucli = EXCLUDED.mean_peri_nucli
            """

            db_execute_many(upsert_prot_q, rows_for_prot_db)

            print(f"[JOB {job_id}] Measurements CSV: {measurements_csv}")
            print(f"[JOB {job_id}] Upserted {len(rows_for_prot_db)} rows into model_2d_prots")
            job_meta["measurements_csv"] = measurements_csv

        # record job outputs
        JOBS[job_id] = job_meta
        print(f"[JOB {job_id}] DONE.")

    except Exception as ex:
        print(f"[JOB {job_id}] FATAL ERROR: {ex}")
        JOBS[job_id] = {"csv_path": None}

# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def home():
    return render_template(
        "index.html",
        defaults=DEFAULTS,
        last_rid=(LAST_CONTEXT.get("rid") or ""),
        last_filename="",
        last_params=LAST_PARAMS,
    )


@app.route("/count", methods=["GET", "POST"])
def count_route():
    if request.method == "GET":
        rid = (request.args.get("rid") or LAST_CONTEXT.get("rid") or "").strip()
        filename = (request.args.get("filename") or "").strip()

        return render_template(
            "index.html",
            defaults=DEFAULTS,
            last_rid=rid,
            last_filename=filename,
            last_params=LAST_PARAMS,
            last_image=None,
            overlay_data_url=None,
            base_image_data_url=None,
            marker_image_data_url=None,
            bulk_ready=False,
            echo_msg="Ready. Click “Visualize Overlay” to run." if (rid or filename) else None
        )

    # POST → run analysis
    source   = request.form
    filename = (source.get("filename") or "").strip()
    rid      = (source.get("rid") or "").strip()

    if not filename:
        return render_template(
            "index.html",
            error="Please provide a filename (e.g., B1_P1.tif).",
            defaults=DEFAULTS,
            last_rid=rid,
            last_filename=filename,
            last_params=LAST_PARAMS,
        ), 400

    if not rid:
        return render_template(
            "index.html",
            error="Please provide rid (e.g., randomIdOUdSMgSN).",
            defaults=DEFAULTS,
            last_rid=rid,
            last_filename=filename,
            last_params=LAST_PARAMS,
        ), 400

    # ---- Resolve image path using new rule
    try:
        image_path = resolve_by_rule(rid, filename)
    except Exception as e:
        return render_template(
            "index.html",
            error=str(e),
            defaults=DEFAULTS,
            last_rid=rid,
            last_filename=filename,
            last_params=LAST_PARAMS,
        ), 400

    # ---- parse params
    try:
        min_sigma       = float(source.get("min_sigma", DEFAULTS["min_sigma"]))
        max_sigma       = float(source.get("max_sigma", DEFAULTS["max_sigma"]))
        threshold       = float(source.get("threshold", DEFAULTS["threshold"]))
        dilation_radius = int(source.get("dilation_radius", DEFAULTS["dilation_radius"]))
        top_n           = max(0, int(source.get("top_n", DEFAULTS["top_n"])))
        low_n           = max(0, int(source.get("low_n", DEFAULTS["low_n"])))
    except ValueError as e:
        return render_template(
            "index.html",
            error=f"Invalid parameter: {e}",
            defaults=DEFAULTS,
            last_rid=rid,
            last_filename=filename,
            last_params=LAST_PARAMS,
        ), 400

    # ---- Protein settings
    protein_measurements = (source.get("protein_measurements") or "").lower() in ("on", "true", "1", "yes")
    protein_region       = (source.get("protein_region") or DEFAULTS["protein_region"]).lower().strip()
    if protein_region not in ("nucli", "prinucli"):
        protein_region = "nucli"

    # ---- Persist
    LAST_PARAMS.update({
        "min_sigma": min_sigma,
        "max_sigma": max_sigma,
        "threshold": threshold,
        "dilation_radius": dilation_radius,
        "top_n": top_n,
        "low_n": low_n,
        "protein_measurements": protein_measurements,
        "protein_region": protein_region,
    })
    LAST_CONTEXT["rid"] = rid

    # ---- Run analysis
    count, overlay_data_url, base_image_data_url, marker_image_data_url = analyze_one_image_overlay(
        image_path, min_sigma, max_sigma, threshold, dilation_radius, top_n, low_n,
        protein_measurements, protein_region
    )

    # ---- Bulk list refresh
    meta_map = load_metadata_map_for_rid(rid)
    global BULK_FILENAMES
    BULK_FILENAMES = sorted(list(meta_map.keys()))

    return render_template(
        "index.html",
        defaults=DEFAULTS,
        overlay_data_url=overlay_data_url,
        base_image_data_url=base_image_data_url,
        marker_image_data_url=marker_image_data_url,
        last_params=LAST_PARAMS,
        last_count=count,
        last_image=Path(image_path).name,
        last_filename=Path(image_path).name,
        last_rid=rid,
        bulk_ready=True
    )


@app.post("/bulk_run")
def bulk_run():
    """
    Start background bulk job.

    File selection priority:
      1) JSON body: {"files": ["B1_P1.tif", ...]} (basenames only)
      2) Cached BULK_FILENAMES (set by /count after DB refresh)
      3) DB for the current RAW rid (tries raw+normalized)
      4) Filesystem scan under BASE_ROOT/<RAW rid>
    """
    rid = (LAST_CONTEXT.get("rid") or "").strip()  # RAW rid as set by /count
    if not rid:
        return Response("Error: rid is not set. Visit /count first.\n", status=400, mimetype="text/plain")

    # Optional incoming files
    incoming_files: List[str] = []
    try:
        if request.is_json:
            payload = request.get_json(silent=True) or {}
            if isinstance(payload.get("files"), list):
                incoming_files = [Path(str(x)).name for x in payload["files"]]
    except Exception:
        pass

    global BULK_FILENAMES
    files_to_run = incoming_files if incoming_files else BULK_FILENAMES

    if not files_to_run:
        files_to_run = refresh_filenames_from_db(rid)  # tries raw + normalized under the hood
        BULK_FILENAMES = files_to_run

    if not files_to_run:
        files_to_run = scan_filesystem_for_rid(rid)
        BULK_FILENAMES = files_to_run

    if not files_to_run:
        msg = (
            "Error: No files found for current rid.\n"
            f"- rid: {rid}\n"
            f"- Looked in DB (files table) and {BASE_ROOT}/{rid}\n"
            "You can also POST JSON: {\"files\": [\"B1_P1.tif\", ...]}\n"
        )
        return Response(msg, status=400, mimetype="text/plain")

    job_id = uuid.uuid4().hex[:8]
    t = threading.Thread(
        target=_bulk_worker,
        kwargs={"job_id": job_id, "rid": rid, "params": LAST_PARAMS.copy(), "files": files_to_run},
        daemon=True,
    )
    t.start()

    msg = (
        f"Bulk started (job_id={job_id}) for rid={rid} with {len(files_to_run)} files.\n"
        "Results will be available after Processing.\n"
        f"Counts CSV → static/results/bulk_{job_id}.csv\n"
        f"Measurements CSV (if enabled) → static/results/measurements_{job_id}.csv\n"
        "Use /bulk_download/<job_id> or /bulk_download_measurements/<job_id>\n"
    )
    return Response(msg, status=202, mimetype="text/plain")


@app.get("/bulk_download/<job_id>")
def bulk_download(job_id):
    job = JOBS.get(job_id)
    if not job or not job.get("csv_path"):
        return Response("Not ready or unknown job_id\n", status=404, mimetype="text/plain")
    csv_path = job["csv_path"]
    rel_name = os.path.basename(csv_path)
    return send_from_directory(RESULT_DIR, rel_name, as_attachment=True)


@app.get("/bulk_download_measurements/<job_id>")
def bulk_download_measurements(job_id):
    job = JOBS.get(job_id)
    path = job.get("measurements_csv") if job else None
    if not path or not os.path.exists(path):
        return Response("Not ready or unknown job_id\n", status=404, mimetype="text/plain")
    rel = os.path.basename(path)
    return send_from_directory(RESULT_DIR, rel, as_attachment=True)


@app.get("/results/<path:filename>")
def results_file(filename):
    # Serves files from static/results (counts/meas CSVs if you want to expose direct links)
    return send_from_directory(RESULT_DIR, filename, as_attachment=False)

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    # Make sure upsert key exists
    ensure_upsert_index()
    ensure_protein_upsert_index()   # NEW: protein features table

    # Optional: visibility at startup
    scan = list_all_files(DATA_ROOT, extensions=[".tif", ".tiff"])
    root_used = DATA_ROOT

    if not scan:
        # Fallback: look under BASE_ROOT_second if nothing in DATA_ROOT/BASE_ROOT
        scan = list_all_files(BASE_ROOT_second, extensions=[".tif", ".tiff"])
        root_used = BASE_ROOT_second

    print(f"Found {len(scan)} files by scan under {root_used}")
    print(scan[:5])

    app.run(host="0.0.0.0", port=6883)
