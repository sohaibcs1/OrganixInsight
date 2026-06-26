import os
import json
import traceback
import numpy as np
import nibabel as nib
import pandas as pd

from skimage import measure
from scipy.spatial import Voronoi, ConvexHull, QhullError
from scipy.spatial.distance import pdist


def load_nii_3d(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    img = nib.load(path)
    arr = np.asarray(img.dataobj)
    arr = np.squeeze(arr)

    if arr.ndim != 3:
        raise ValueError(f"Expected 3D NIfTI volume, got {arr.shape}")

    return arr


def get_labels(mask):
    m = np.asarray(mask)

    if int(m.max()) > 1:
        return m.astype(np.int32)

    return measure.label(m > 0).astype(np.int32)


def compute_cell_geometry_df(labels):
    props = measure.regionprops(labels)
    rows = []

    for p in props:
        cz, cy, cx = p.centroid

        rows.append({
            "cell_id": int(p.label),
            "z": float(cz),
            "y": float(cy),
            "x": float(cx),
            "nucleus_size": int(p.area),
        })

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No cells found in mask.")

    return df.sort_values("cell_id").reset_index(drop=True)


def classify_basal_voronoi(df):
    pts = df[["z", "y", "x"]].to_numpy(np.float64)
    df = df.copy()

    if pts.shape[0] < 5 or np.linalg.matrix_rank(pts - pts.mean(axis=0)) < 3:
        df["cell_type"] = "Unknown"
        return df

    try:
        pts_j = pts + 1e-8 * np.random.randn(*pts.shape)
        vor = Voronoi(pts_j)

        basal_flags = []

        for i in range(len(pts_j)):
            region_idx = vor.point_region[i]
            region = vor.regions[region_idx]

            is_basal = (
                region is None
                or len(region) == 0
                or -1 in region
            )

            basal_flags.append(is_basal)

        df["cell_type"] = np.where(
            basal_flags,
            "Basal",
            "Non-basal"
        )

    except Exception:
        df["cell_type"] = "Unknown"

    return df


def make_subset_labels(labels, cell_ids):
    subset = np.zeros_like(labels, dtype=np.int32)

    if len(cell_ids) == 0:
        return subset

    mask = np.isin(labels, list(cell_ids))
    subset[mask] = labels[mask]

    return subset


def safe_group_stats(df, prefix):
    if df.empty:
        return {
            f"{prefix}_cells": 0,
            f"{prefix}_mean_nucleus_size": None,
            f"{prefix}_median_nucleus_size": None,
            f"{prefix}_total_nucleus_volume": None,
            f"{prefix}_mean_z": None,
            f"{prefix}_mean_y": None,
            f"{prefix}_mean_x": None,
        }

    return {
        f"{prefix}_cells": int(len(df)),
        f"{prefix}_mean_nucleus_size": float(df["nucleus_size"].mean()),
        f"{prefix}_median_nucleus_size": float(df["nucleus_size"].median()),
        f"{prefix}_total_nucleus_volume": float(df["nucleus_size"].sum()),
        f"{prefix}_mean_z": float(df["z"].mean()),
        f"{prefix}_mean_y": float(df["y"].mean()),
        f"{prefix}_mean_x": float(df["x"].mean()),
    }


def compute_morphometric_properties(labels, prefix):
    props = measure.regionprops(labels)

    cell_pixels_list = []
    total_nuclei_volume = 0
    sum_cov_matrix = np.zeros((3, 3))
    num_cells = 0

    result = {
        f"{prefix}_morph_cells": 0,
        f"{prefix}_Nuclear_Elongation": None,
        f"{prefix}_Nuclear_Flatness": None,
        f"{prefix}_Nuclear_Volume": None,
        f"{prefix}_Colony_Elongation": None,
        f"{prefix}_Colony_Flatness": None,
        f"{prefix}_Colony_Diameter": None,
        f"{prefix}_Colony_Radius": None,
        f"{prefix}_Max_Neighbourhood_Distance": None,
        f"{prefix}_Mean_Neighbourhood_Distance": None,
        f"{prefix}_Volume_of_Colony_Convex_Hull": None,
        f"{prefix}_Lumen_Volume": None,
    }

    for prop in props:
        coords = np.array(prop.coords)

        if len(coords) >= 4:
            cell_pixels_list.append(coords)
            total_nuclei_volume += len(coords)

            try:
                cov_matrix = np.cov(coords, rowvar=False)
                if cov_matrix.shape == (3, 3):
                    sum_cov_matrix += cov_matrix
            except Exception:
                pass

            num_cells += 1

    result[f"{prefix}_morph_cells"] = int(num_cells)

    if num_cells == 0 or len(cell_pixels_list) == 0:
        return result

    result[f"{prefix}_Nuclear_Volume"] = float(
        total_nuclei_volume / num_cells
    )

    try:
        eigenvalues, _ = np.linalg.eigh(sum_cov_matrix)
        eigenvalues.sort()
        moments = np.sqrt(np.maximum(eigenvalues, 1e-8))

        result[f"{prefix}_Nuclear_Elongation"] = float(
            moments[2] / moments[0]
        )
        result[f"{prefix}_Nuclear_Flatness"] = float(
            moments[2] / moments[1]
        )
    except Exception:
        pass

    all_pixels = np.vstack(cell_pixels_list)

    try:
        colony_cov = np.cov(all_pixels, rowvar=False)
        colony_eigenvalues, _ = np.linalg.eigh(colony_cov)
        colony_eigenvalues.sort()
        colony_moments = np.sqrt(np.maximum(colony_eigenvalues, 1e-8))

        result[f"{prefix}_Colony_Elongation"] = float(
            colony_moments[2] / colony_moments[0]
        )
        result[f"{prefix}_Colony_Flatness"] = float(
            colony_moments[2] / colony_moments[1]
        )
    except Exception:
        pass

    try:
        rank = np.linalg.matrix_rank(
            all_pixels - all_pixels.mean(axis=0)
        )

        if len(all_pixels) >= 4 and rank >= 3:
            hull = ConvexHull(all_pixels)
            hull_volume = float(hull.volume)

            hull_points = all_pixels[hull.vertices]
            distances = pdist(hull_points)

            if len(distances) > 0:
                diameter = float(np.max(distances))

                result[f"{prefix}_Colony_Diameter"] = diameter
                result[f"{prefix}_Colony_Radius"] = diameter / 2
                result[f"{prefix}_Mean_Neighbourhood_Distance"] = float(
                    np.mean(distances)
                )
                result[f"{prefix}_Max_Neighbourhood_Distance"] = float(
                    np.max(distances)
                )

            result[f"{prefix}_Volume_of_Colony_Convex_Hull"] = hull_volume
            result[f"{prefix}_Lumen_Volume"] = max(
                hull_volume - float(total_nuclei_volume),
                0.0
            )

    except QhullError:
        pass
    except Exception:
        pass

    return result


def clean_for_json(obj):
    clean = {}

    for k, v in obj.items():
        if isinstance(v, (np.integer,)):
            clean[k] = int(v)
        elif isinstance(v, (np.floating,)):
            if np.isnan(v) or np.isinf(v):
                clean[k] = None
            else:
                clean[k] = float(v)
        elif isinstance(v, float):
            if np.isnan(v) or np.isinf(v):
                clean[k] = None
            else:
                clean[k] = v
        else:
            clean[k] = v

    return clean


def run_mask_basal_morphology_json(nuclei_mask_nifti):
    try:
        mask = load_nii_3d(nuclei_mask_nifti)
        labels = get_labels(mask)

        if int(labels.max()) < 1:
            raise ValueError("No labeled cells found.")

        cell_df = compute_cell_geometry_df(labels)
        cell_df = classify_basal_voronoi(cell_df)

        basal_df = cell_df[cell_df["cell_type"] == "Basal"]
        non_basal_df = cell_df[cell_df["cell_type"] == "Non-basal"]
        unknown_df = cell_df[cell_df["cell_type"] == "Unknown"]

        basal_labels = make_subset_labels(
            labels,
            basal_df["cell_id"].tolist()
        )

        non_basal_labels = make_subset_labels(
            labels,
            non_basal_df["cell_id"].tolist()
        )

        total_cells = len(cell_df)

        print(
            "Cells:",
            "all =", len(cell_df),
            "basal =", len(basal_df),
            "non_basal =", len(non_basal_df),
            "unknown =", len(unknown_df)
        )

        combined_properties = {
            "file_name": os.path.basename(nuclei_mask_nifti),
            "status": "success",

            "all_cells": int(total_cells),
            "basal_cells": int(len(basal_df)),
            "non_basal_cells": int(len(non_basal_df)),
            "unknown_cells": int(len(unknown_df)),

            "basal_percent": float(
                100.0 * len(basal_df) / total_cells
            ) if total_cells else 0.0,

            "non_basal_percent": float(
                100.0 * len(non_basal_df) / total_cells
            ) if total_cells else 0.0,

            "unknown_percent": float(
                100.0 * len(unknown_df) / total_cells
            ) if total_cells else 0.0,
        }

        combined_properties.update(
            safe_group_stats(cell_df, "all")
        )

        combined_properties.update(
            safe_group_stats(basal_df, "basal")
        )

        combined_properties.update(
            safe_group_stats(non_basal_df, "non_basal")
        )

        combined_properties.update(
            compute_morphometric_properties(labels, "all")
        )

        combined_properties.update(
            compute_morphometric_properties(basal_labels, "basal")
        )

        combined_properties.update(
            compute_morphometric_properties(non_basal_labels, "non_basal")
        )

        combined_properties = clean_for_json(combined_properties)

        return json.dumps(
            combined_properties,
            separators=(",", ":")
        )

    except Exception as e:
        traceback.print_exc()

        error_json = {
            "file_name": os.path.basename(nuclei_mask_nifti),
            "status": "failed",
            "error_message": str(e),
        }

        return json.dumps(
            error_json,
            separators=(",", ":")
        )
# # ============================================================
# # RUN
# # ============================================================
# if __name__ == "__main__":

#     result_json = run_mask_basal_morphology_json(
#         nuclei_mask_nifti="/home/msohaib/z_check/db93c87c_predicted_mask.nii.gz"
#     )

#     print(result_json)
