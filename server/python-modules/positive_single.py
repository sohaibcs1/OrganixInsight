import os
import io
import json
import base64
import traceback
import warnings

import numpy as np
import pandas as pd
import psycopg2
import nibabel as nib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scipy.ndimage import binary_dilation
from skimage.measure import regionprops
from skimage.transform import resize

try:
    import dask
except Exception:
    dask = None


warnings.filterwarnings("ignore", message=".*Reshaping is producing a large chunk.*")
warnings.filterwarnings("ignore", message=".*To avoid creating the large chunks.*")


CFG_PATH = "db_config.json"

if not os.path.exists(CFG_PATH):
    raise FileNotFoundError(f"Config file '{CFG_PATH}' not found.")

with open(CFG_PATH, "r", encoding="utf-8") as f:
    DB_CFG = json.load(f)


UPLOAD_BASE_DIR = "/home/msohaib/3D_organixInsight/server/uploads"
MASK_BASE_DIR = "/home/msohaib/3D_organixInsight/server/python-modules/model_prediction"


def fig_to_base64(fig):
    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=250,
        bbox_inches="tight",
        pad_inches=0.05
    )

    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    plt.close(fig)

    return img_base64


def split_marker_text(value):
    if value is None:
        return []

    value = str(value).strip()

    if value.lower() in ["", "null", "none", "undefined", "[null]"]:
        return []

    return [
        x.strip()
        for x in value.split(",")
        if x.strip()
    ]


def normalize_name(value):
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .upper()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


def get_experiment_channel_mapping(conn, experiment_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT "primary", secondary
            FROM experiments
            WHERE uuid = %s
            LIMIT 1
            """,
            (str(experiment_id),)
        )

        row = cur.fetchone()

    if not row:
        return {}

    primary, secondary = row

    primaries = split_marker_text(primary)
    secondaries = split_marker_text(secondary)

    mapping = {}

    for marker, fluor in zip(primaries, secondaries):
        fluor_key = normalize_name(fluor)

        if not fluor_key:
            continue

        mapping[fluor_key] = {
            "marker": marker,
            "marker_type": "Primary",
            "secondary": fluor,
            "source": "primary_secondary"
        }

    return mapping


def get_czi_channels(czi_path):
    try:
        from aicsimageio import AICSImage
        from aicsimageio.readers import CziReader

        if not os.path.exists(czi_path):
            return []

        if dask is not None:
            with dask.config.set({"array.slicing.split_large_chunks": False}):
                img = AICSImage(czi_path, reader=CziReader)
        else:
            img = AICSImage(czi_path, reader=CziReader)

        try:
            channel_names = list(img.channel_names)
        except Exception:
            channel_names = []

        if channel_names:
            return [
                {
                    "channel_index": int(i),
                    "channel_name": str(ch) if ch else f"Channel {i}"
                }
                for i, ch in enumerate(channel_names)
            ]

        try:
            c_size = int(img.dims.C)
        except Exception:
            c_size = 1

        return [
            {
                "channel_index": int(i),
                "channel_name": f"Channel {i}"
            }
            for i in range(c_size)
        ]

    except Exception:
        traceback.print_exc()
        return []


def find_single_file_for_overlay(experiment_id, file_name):
    conn = psycopg2.connect(**DB_CFG)

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    uuid,
                    experiment_id,
                    study_id,
                    model_prediction_mask
                FROM model_files
                WHERE experiment_id = %s
                AND study_id = %s
                AND model_prediction_mask IS NOT NULL
                LIMIT 1
                """,
                (
                    str(experiment_id),
                    str(file_name)
                )
            )

            row = cur.fetchone()

            if row:
                return {
                    "uuid": row[0],
                    "experiment_id": row[1],
                    "study_id": row[2],
                    "model_prediction_mask": row[3]
                }

            clean_name = str(file_name).replace(".czi", "").strip()

            cur.execute(
                """
                SELECT
                    uuid,
                    experiment_id,
                    study_id,
                    model_prediction_mask
                FROM model_files
                WHERE experiment_id = %s
                AND study_id ILIKE %s
                AND model_prediction_mask IS NOT NULL
                LIMIT 1
                """,
                (
                    str(experiment_id),
                    f"%{clean_name}%"
                )
            )

            row = cur.fetchone()

            if row:
                return {
                    "uuid": row[0],
                    "experiment_id": row[1],
                    "study_id": row[2],
                    "model_prediction_mask": row[3]
                }

        raise ValueError(
            f"No model_prediction_mask found for experiment_id={experiment_id}, file_name={file_name}"
        )

    finally:
        conn.close()


def get_matched_marker_channel(experiment_id, raw_czi_path):
    conn = psycopg2.connect(**DB_CFG)

    try:
        experiment_mapping = get_experiment_channel_mapping(
            conn,
            experiment_id
        )
    finally:
        conn.close()

    all_channels = get_czi_channels(raw_czi_path)

    print("[INFO] Experiment mapping:", experiment_mapping)
    print("[INFO] Available CZI channels:", all_channels)

    for ch in all_channels:
        ch_name = str(ch["channel_name"]).strip()
        ch_key = normalize_name(ch_name)

        if ch_key in experiment_mapping:
            marker_info = experiment_mapping[ch_key]

            print(
                f"[INFO] Matched overlay channel: "
                f"{ch['channel_index']} {ch_name} -> {marker_info['marker']}"
            )

            return {
                "channel_index": int(ch["channel_index"]),
                "channel_name": ch_name,
                "marker": marker_info["marker"],
                "marker_type": marker_info["marker_type"],
                "secondary": marker_info["secondary"],
                "mapping_source": marker_info["source"],
                "available_czi_channels": all_channels,
                "experiment_mapping": experiment_mapping
            }

    raise ValueError(
        f"No matching CZI channel found for experiment_id={experiment_id}. "
        f"DB secondary={list(experiment_mapping.keys())}, "
        f"CZI channels={[c['channel_name'] for c in all_channels]}"
    )


def load_czi_middle_slice(czi_path, z_mid, channel_index):
    from aicsimageio import AICSImage
    from aicsimageio.readers import CziReader

    if dask is not None:
        with dask.config.set({"array.slicing.split_large_chunks": False}):
            img = AICSImage(czi_path, reader=CziReader)
            raw = img.get_image_data(
                "ZYX",
                C=int(channel_index),
                T=0
            )
    else:
        img = AICSImage(czi_path, reader=CziReader)
        raw = img.get_image_data(
            "ZYX",
            C=int(channel_index),
            T=0
        )

    raw = np.squeeze(raw)

    if raw.ndim != 3:
        raw = raw.reshape(raw.shape[-3:])

    z_raw = min(int(z_mid), raw.shape[0] - 1)

    raw_slice = raw[z_raw, :, :].astype(np.float32)

    p1, p99 = np.percentile(raw_slice, [1, 99])

    if p99 > p1:
        raw_slice = (raw_slice - p1) / (p99 - p1)
        raw_slice = np.clip(raw_slice, 0, 1)
    else:
        raw_slice = raw_slice * 0

    return raw_slice


def build_display_mask(label_slice, dilation_radius=0):
    label_slice = np.asarray(label_slice).astype(np.int32)
    dilation_radius = int(dilation_radius)

    nucleus_mask = label_slice > 0
    ring_mask = np.zeros_like(nucleus_mask, dtype=bool)

    if dilation_radius > 0:
        expanded_mask = np.zeros(label_slice.shape, dtype=bool)

        for region in regionprops(label_slice):
            nucleus = label_slice == region.label
            dilated = binary_dilation(nucleus, iterations=dilation_radius)
            expanded_mask |= dilated

        ring_mask = np.logical_and(expanded_mask, np.logical_not(nucleus_mask))

    return {
        "nucleus_mask": nucleus_mask,
        "ring_mask": ring_mask,
        "title": (
            "Original Mask Overlay"
            if dilation_radius <= 0
            else f"Original Mask + Ring Overlay (radius={dilation_radius})"
        ),
        "mode": "original_mask" if dilation_radius <= 0 else "mask_plus_ring"
    }


def draw_mask_image(mask_info, display_title, dilation_radius):
    nucleus_mask = mask_info["nucleus_mask"]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(np.zeros_like(nucleus_mask), cmap="gray")

    # LEFT image: always original mask only
    ax.contour(
        nucleus_mask.astype(np.uint8),
        levels=[0.5],
        colors="white",
        linewidths=2.8
    )

    ax.set_title("Original Mask Region", fontsize=16, fontweight="bold")
    ax.axis("off")

    return fig_to_base64(fig)


def draw_overlay_image(raw_slice, mask_info, display_title, dilation_radius):
    nucleus_mask = mask_info["nucleus_mask"]
    ring_mask = mask_info["ring_mask"]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(raw_slice, cmap="gray")

    # Original mask boundary
    ax.contour(
        nucleus_mask.astype(np.uint8),
        levels=[0.5],
        colors="red",
        linewidths=2.8
    )

    # Extra ring only when dilation > 0
    if int(dilation_radius) > 0:
        ax.contour(
            ring_mask.astype(np.uint8),
            levels=[0.5],
            colors="red",
            linewidths=3.8
        )

    ax.set_title(display_title, fontsize=16, fontweight="bold")
    ax.axis("off")

    return fig_to_base64(fig)

def generate_single_mask_overlay_base64(
    experiment_id,
    file_name,
    dilation_radius=0
):
    dilation_radius = int(dilation_radius)

    item = find_single_file_for_overlay(
        experiment_id=experiment_id,
        file_name=file_name
    )

    raw_file_name = item["study_id"]
    mask_file_name = item["model_prediction_mask"]

    raw_czi_path = os.path.join(
        UPLOAD_BASE_DIR,
        raw_file_name
    )

    mask_path = os.path.join(
        MASK_BASE_DIR,
        mask_file_name
    )

    if not os.path.exists(raw_czi_path):
        raise FileNotFoundError(raw_czi_path)

    if not os.path.exists(mask_path):
        raise FileNotFoundError(mask_path)

    matched_channel = get_matched_marker_channel(
        experiment_id=experiment_id,
        raw_czi_path=raw_czi_path
    )

    channel_index = int(matched_channel["channel_index"])
    channel_name = str(matched_channel["channel_name"])
    marker = str(matched_channel["marker"])

    mask = np.asarray(nib.load(mask_path).dataobj)
    mask = np.squeeze(mask)

    if mask.ndim != 3:
        raise ValueError(f"Mask must be 3D. Got shape={mask.shape}")

    z_mid = mask.shape[0] // 2
    label_slice = mask[z_mid, :, :]

    mask_info = build_display_mask(
        label_slice=label_slice,
        dilation_radius=dilation_radius
    )

    title = mask_info["title"]
    mode = mask_info["mode"]
    display_mask = mask_info["nucleus_mask"]

    raw_slice = load_czi_middle_slice(
        czi_path=raw_czi_path,
        z_mid=z_mid,
        channel_index=channel_index
    )

    if raw_slice.shape != display_mask.shape:
        raw_slice = resize(
            raw_slice,
            display_mask.shape,
            preserve_range=True,
            anti_aliasing=True
        ).astype(np.float32)

    display_title = f"{title} - {marker} ({channel_name})"

    mask_base64 = draw_mask_image(
        mask_info=mask_info,
        display_title=display_title,
        dilation_radius=dilation_radius
    )

    overlay_base64 = draw_overlay_image(
        raw_slice=raw_slice,
        mask_info=mask_info,
        display_title=display_title,
        dilation_radius=dilation_radius
    )

    return {
        "status": "success",
        "experiment_id": str(experiment_id),
        "uuid": item["uuid"],
        "file_name": raw_file_name,
        "mask_file_name": mask_file_name,
        "dilation_radius": dilation_radius,
        "z_mid": int(z_mid),
        "mode": mode,

        "channel_index": channel_index,
        "channel_name": channel_name,
        "marker": marker,
        "secondary": matched_channel["secondary"],
        "mapping_source": matched_channel["mapping_source"],

        "mask_image_base64": mask_base64,
        "overlay_image_base64": overlay_base64,

        "available_czi_channels": matched_channel["available_czi_channels"],
        "experiment_mapping": matched_channel["experiment_mapping"]
    }


def check_input(payload):
    try:
        experiment_id = payload.get("experiment_id")
        file_name = payload.get("file_name")
        dilation_radius = payload.get("dilation_radius", 0)

        if experiment_id is None:
            raise ValueError("experiment_id is required.")

        if not file_name:
            raise ValueError("file_name is required.")

        return generate_single_mask_overlay_base64(
            experiment_id=experiment_id,
            file_name=file_name,
            dilation_radius=dilation_radius
        )

    except Exception as e:
        traceback.print_exc()

        return {
            "status": "failed",
            "error_message": str(e)
        }
