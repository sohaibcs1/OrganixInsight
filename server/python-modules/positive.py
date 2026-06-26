import os
import json
import traceback
import warnings
import tempfile

import numpy as np
import pandas as pd
import psycopg2
import nibabel as nib

from scipy.ndimage import binary_dilation
from skimage.measure import regionprops

from positive_cells_3d.positive3d import run_intensity_positive_negative


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


def clean_for_json(obj):
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_for_json(v) for v in obj]
    if isinstance(obj, tuple):
        return [clean_for_json(v) for v in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)
    if isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    try:
        if pd.isna(obj):
            return None
    except Exception:
        pass
    return obj


def split_marker_text(value):
    if value is None:
        return []

    value = str(value).strip()

    if value.lower() in ["", "null", "none", "undefined", "[null]"]:
        return []

    return [x.strip() for x in value.split(",") if x.strip()]


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


def normalize_channel_name(value):
    name = normalize_name(value)

    aliases = {
        "ALEXAFLUOR488": "AF488",
        "ALEXA488": "AF488",
        "FITC": "AF488",
        "GFP": "AF488",
        "488": "AF488",

        "ALEXAFLUOR594": "AF594",
        "ALEXA594": "AF594",
        "TRITC": "AF594",
        "594": "AF594",

        "ALEXAFLUOR647": "AF647",
        "ALEXA647": "AF647",
        "CY5": "AF647",
        "647": "AF647",

        "HOECHST": "DAPI",
        "HOECHST33342": "DAPI",
        "NUCLEAR": "DAPI",
    }

    return aliases.get(name, name)


def parse_positive_payload(payload):
    if isinstance(payload, dict):
        experiment_ids = (
            payload.get("experiment_ids")
            or payload.get("experiment_id")
            or payload.get("name")
            or ""
        )
        dilation_radius = int(payload.get("dilation_radius", 0) or 0)
        return experiment_ids, dilation_radius

    return payload, 0


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
        fluor_key = normalize_channel_name(fluor)
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

        if not str(czi_path).lower().endswith(".czi"):
            raise ValueError(f"Only .czi files supported in this positive.py: {czi_path}")

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
                    "channel_name": str(ch) if ch else f"Channel {i}",
                    "normalized_name": normalize_channel_name(ch)
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
                "channel_name": f"Channel {i}",
                "normalized_name": f"CHANNEL{i}"
            }
            for i in range(c_size)
        ]

    except Exception:
        traceback.print_exc()
        return []


def get_channels_to_run(all_channels, experiment_mapping, channel_index="all"):
    if channel_index != "all":
        selected = int(channel_index)

        selected_channels = [
            ch for ch in all_channels
            if int(ch["channel_index"]) == selected
        ]

        if not selected_channels:
            selected_channels = [{
                "channel_index": selected,
                "channel_name": f"Channel {selected}",
                "marker": f"Channel {selected}",
                "marker_type": "Manual",
                "mapping_source": "manual"
            }]

        for ch in selected_channels:
            ch.setdefault("marker", ch["channel_name"])
            ch.setdefault("marker_type", "Manual")
            ch.setdefault("mapping_source", "manual")
            ch.setdefault("secondary", ch["channel_name"])

        return selected_channels

    channels_to_run = []

    for ch in all_channels:
        ch_name = str(ch["channel_name"]).strip()
        ch_key = normalize_channel_name(ch_name)

        if ch_key in experiment_mapping:
            marker_info = experiment_mapping[ch_key]

            ch["marker"] = marker_info["marker"]
            ch["marker_type"] = marker_info["marker_type"]
            ch["mapping_source"] = marker_info["source"]
            ch["secondary"] = marker_info["secondary"]

            channels_to_run.append(ch)

    return channels_to_run


def make_ring_only_label_mask(nuclei_mask_nifti, dilation_radius):
    dilation_radius = int(dilation_radius)

    if dilation_radius < 0:
        raise ValueError("dilation_radius must be >= 0")

    if dilation_radius == 0:
        return nuclei_mask_nifti, None

    nii = nib.load(nuclei_mask_nifti)
    mask = np.asarray(nii.dataobj).astype(np.int32)

    ring_only = np.zeros(mask.shape, dtype=np.int32)
    original_mask = mask > 0

    for region in regionprops(mask):
        label = int(region.label)
        nucleus = mask == label

        dilated = binary_dilation(
            nucleus,
            iterations=dilation_radius
        )

        ring = np.logical_and(
            dilated,
            np.logical_not(original_mask)
        )

        add_area = np.logical_and(ring, ring_only == 0)
        ring_only[add_area] = label

    tmp = tempfile.NamedTemporaryFile(
        suffix="_positive_ring_only_mask.nii.gz",
        delete=False
    )
    tmp.close()

    nib.save(
        nib.Nifti1Image(ring_only, nii.affine, nii.header),
        tmp.name
    )

    return tmp.name, tmp.name


def parse_positive_result(result_json):
    if isinstance(result_json, pd.DataFrame):
        return result_json.iloc[0].to_dict()

    if isinstance(result_json, dict):
        return result_json

    if isinstance(result_json, str):
        return json.loads(result_json)

    return dict(result_json)


def get_positive_files_by_experiment_ids(name):
    if isinstance(name, list):
        experiment_ids = [str(x).strip() for x in name if str(x).strip()]
    else:
        experiment_ids = [x.strip() for x in str(name).split(",") if x.strip()]

    if not experiment_ids:
        return []

    conn = psycopg2.connect(**DB_CFG)

    try:
        with conn.cursor() as cur:
            placeholders = ",".join(["%s"] * len(experiment_ids))

            query = f"""
                SELECT
                    uuid,
                    experiment_id,
                    study_id,
                    model_prediction_mask
                FROM model_files
                WHERE experiment_id IN ({placeholders})
                AND study_id IS NOT NULL
                AND model_prediction_mask IS NOT NULL
                ORDER BY experiment_id, uuid
            """

            cur.execute(query, experiment_ids)
            rows = cur.fetchall()

        return [
            {
                "uuid": row[0],
                "experiment_id": row[1],
                "study_id": row[2],
                "model_prediction_mask": row[3],
            }
            for row in rows
        ]

    finally:
        conn.close()


def run_positive_for_experiments(
    name,
    channel_index="all",
    positive_threshold=None,
    marker_column="mean_intensity",
    save_final=False
):
    name, dilation_radius = parse_positive_payload(name)
    dilation_radius = int(dilation_radius)

    if dilation_radius < 0:
        raise ValueError("dilation_radius must be >= 0")

    measurement_mask_mode = (
        "original_nucleus_mask"
        if dilation_radius == 0
        else "dilated_ring_only"
    )

    files = get_positive_files_by_experiment_ids(name)
    results = []

    if len(files) == 0:
        return {
            "status": "failed",
            "processed": 0,
            "dilation_radius": dilation_radius,
            "measurement_mask_mode": measurement_mask_mode,
            "error": "No model_files found for the provided experiment IDs.",
            "results": []
        }

    conn = psycopg2.connect(**DB_CFG)

    try:
        with conn.cursor() as cur:
            for item in files:
                file_uuid = item["uuid"]
                experiment_id = item["experiment_id"]
                raw_file_name = item["study_id"]
                mask_file_name = item["model_prediction_mask"]

                raw_czi_path = os.path.join(UPLOAD_BASE_DIR, raw_file_name)
                nuclei_mask_nifti = os.path.join(MASK_BASE_DIR, mask_file_name)

                temp_mask_path = None

                try:
                    if not os.path.exists(raw_czi_path):
                        raise FileNotFoundError(raw_czi_path)

                    if not str(raw_czi_path).lower().endswith(".czi"):
                        raise ValueError(f"Only .czi files supported: {raw_czi_path}")

                    if not os.path.exists(nuclei_mask_nifti):
                        raise FileNotFoundError(nuclei_mask_nifti)

                    all_channels = get_czi_channels(raw_czi_path)

                    if len(all_channels) == 0:
                        raise ValueError(f"No CZI channels found for {raw_czi_path}")

                    experiment_mapping = get_experiment_channel_mapping(
                        conn,
                        experiment_id
                    )

                    print("[INFO] Experiment mapping:", experiment_mapping)
                    print("[INFO] Available CZI channels:", all_channels)

                    if len(experiment_mapping) == 0 and channel_index == "all":
                        raise ValueError(
                            f"No experiment primary/secondary mapping found for experiment={experiment_id}"
                        )

                    channels_to_run = get_channels_to_run(
                        all_channels=all_channels,
                        experiment_mapping=experiment_mapping,
                        channel_index=channel_index
                    )

                    if len(channels_to_run) == 0:
                        raise ValueError(
                            f"No matching positive channels found for experiment={experiment_id}. "
                            f"Available channels={all_channels}. "
                            f"Experiment mapping={experiment_mapping}"
                        )

                    measurement_mask_path, temp_mask_path = make_ring_only_label_mask(
                        nuclei_mask_nifti,
                        dilation_radius
                    )

                    channel_results = []

                    for ch in channels_to_run:
                        ch_index = int(ch["channel_index"])
                        ch_name = str(ch["channel_name"])
                        marker = str(ch.get("marker", ch_name))
                        marker_type = str(ch.get("marker_type", "Unknown"))
                        mapping_source = str(ch.get("mapping_source", "unknown"))
                        secondary = ch.get("secondary", ch_name)

                        try:
                            result_json = run_intensity_positive_negative(
                                nuclei_mask_nifti=measurement_mask_path,
                                raw_czi_path=raw_czi_path,
                                channel_index=ch_index,
                                positive_threshold=positive_threshold,
                                marker_column=marker_column,
                                save_final=save_final
                            )

                            result_dict = parse_positive_result(result_json)

                            result_dict["channel_index"] = ch_index
                            result_dict["channel_name"] = ch_name
                            result_dict["marker"] = marker
                            result_dict["marker_type"] = marker_type
                            result_dict["secondary"] = secondary
                            result_dict["display_name"] = f"{marker} ({ch_name})"
                            result_dict["mapping_source"] = mapping_source
                            result_dict["dilation_radius"] = dilation_radius
                            result_dict["measurement_mask_mode"] = measurement_mask_mode
                            result_dict["status"] = result_dict.get("status", "success")

                            channel_results.append(clean_for_json(result_dict))

                        except Exception as channel_error:
                            traceback.print_exc()

                            channel_results.append({
                                "status": "failed",
                                "channel_index": ch_index,
                                "channel_name": ch_name,
                                "marker": marker,
                                "marker_type": marker_type,
                                "secondary": secondary,
                                "display_name": f"{marker} ({ch_name})",
                                "mapping_source": mapping_source,
                                "dilation_radius": dilation_radius,
                                "measurement_mask_mode": measurement_mask_mode,
                                "error_message": str(channel_error)
                            })

                    failed_channels = [
                        ch for ch in channel_results
                        if ch.get("status") == "failed"
                    ]

                    file_status = (
                        "failed"
                        if len(failed_channels) == len(channel_results)
                        else "success"
                    )

                    final_json = {
                        "status": file_status,
                        "file_name": os.path.basename(raw_czi_path),
                        "mask_file_name": os.path.basename(nuclei_mask_nifti),
                        "experiment_id": experiment_id,
                        "uuid": file_uuid,
                        "total_channels": len(channel_results),
                        "failed_channels": len(failed_channels),
                        "channels": channel_results,
                        "experiment_markers": experiment_mapping,
                        "available_czi_channels": all_channels,
                        "dilation_radius": dilation_radius,
                        "measurement_mask_mode": measurement_mask_mode,
                        "file_info": {
                            "file_name": os.path.basename(raw_czi_path),
                            "raw_czi_path": raw_czi_path,
                            "mask_file_name": os.path.basename(nuclei_mask_nifti),
                            "mask_path": nuclei_mask_nifti,
                        }
                    }

                    final_json = clean_for_json(final_json)

                    cur.execute(
                        """
                        UPDATE model_files
                        SET positive = %s
                        WHERE uuid = %s
                        """,
                        (
                            json.dumps(final_json, separators=(",", ":")),
                            file_uuid
                        )
                    )

                    results.append({
                        "uuid": file_uuid,
                        "experiment_id": experiment_id,
                        "file_name": os.path.basename(raw_czi_path),
                        "mask_file_name": os.path.basename(nuclei_mask_nifti),
                        "total_channels": len(channel_results),
                        "failed_channels": len(failed_channels),
                        "dilation_radius": dilation_radius,
                        "measurement_mask_mode": measurement_mask_mode,
                        "status": file_status
                    })

                except Exception as e:
                    traceback.print_exc()

                    error_json = {
                        "status": "failed",
                        "file_name": os.path.basename(raw_czi_path),
                        "mask_file_name": os.path.basename(nuclei_mask_nifti),
                        "dilation_radius": dilation_radius,
                        "measurement_mask_mode": measurement_mask_mode,
                        "error_message": str(e)
                    }

                    cur.execute(
                        """
                        UPDATE model_files
                        SET positive = %s
                        WHERE uuid = %s
                        """,
                        (
                            json.dumps(error_json, separators=(",", ":")),
                            file_uuid
                        )
                    )

                    results.append({
                        "uuid": file_uuid,
                        "experiment_id": experiment_id,
                        "dilation_radius": dilation_radius,
                        "measurement_mask_mode": measurement_mask_mode,
                        "status": "failed",
                        "error": str(e)
                    })

                finally:
                    if temp_mask_path and os.path.exists(temp_mask_path):
                        try:
                            os.remove(temp_mask_path)
                        except Exception:
                            pass

            conn.commit()

        failed_files = [r for r in results if r.get("status") == "failed"]

        return {
            "status": "success" if len(failed_files) == 0 else "partial_failed",
            "processed": len(results),
            "failed": len(failed_files),
            "dilation_radius": dilation_radius,
            "measurement_mask_mode": measurement_mask_mode,
            "results": results
        }

    except Exception as e:
        conn.rollback()
        traceback.print_exc()

        return {
            "status": "failed",
            "dilation_radius": dilation_radius,
            "measurement_mask_mode": measurement_mask_mode,
            "error": str(e)
        }

    finally:
        conn.close()
