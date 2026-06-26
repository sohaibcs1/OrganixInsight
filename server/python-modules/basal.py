import os
import json
from datetime import datetime
from typing import List, Tuple
import numpy as np
import pandas as pd
import psycopg2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import traceback
from basal_analysis import run_mask_basal_morphology_json

# DB config
# -----------------------------
CFG_PATH = "db_config.json"
if not os.path.exists(CFG_PATH):
    raise FileNotFoundError(
        f"Config file '{CFG_PATH}' not found. Create it with keys: "
        "{database, user, host, password, port}"
    )
with open(CFG_PATH, "r", encoding="utf-8") as f:
    DB_CFG = json.load(f)
MASK_BASE_DIR = "/home/msohaib/3D_organixInsight/server/python-modules/model_prediction"


def get_mask_files_by_uuid(name):
    print("[DEBUG] raw name received:", name, type(name))

    if isinstance(name, dict):
        name = name.get("name") or name.get("data") or name.get("ids") or ""

    if isinstance(name, list):
        experiment_ids = []
        for x in name:
            if isinstance(x, dict):
                val = x.get("experiment_id") or x.get("uuid") or x.get("value")
                if val:
                    experiment_ids.append(str(val).strip())
            else:
                experiment_ids.append(str(x).strip())
    else:
        experiment_ids = [
            x.strip()
            for x in str(name).replace("[", "").replace("]", "").replace('"', "").replace("'", "").split(",")
            if x.strip()
        ]

    experiment_ids = list(dict.fromkeys(experiment_ids))

    print("[DEBUG] parsed experiment_ids:", experiment_ids)

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
                    model_prediction_mask
                FROM model_files
                WHERE TRIM(experiment_id::text) IN ({placeholders})
                AND model_prediction_mask IS NOT NULL
                ORDER BY experiment_id, uuid
            """

            cur.execute(query, experiment_ids)
            rows = cur.fetchall()

        print("[DEBUG] rows found:", len(rows))
        print("[DEBUG] experiment_ids in rows:", sorted(set(str(r[1]) for r in rows)))

        return [
            {
                "uuid": row[0],
                "experiment_id": row[1],
                "model_prediction_mask": row[2]
            }
            for row in rows
        ]

    finally:
        conn.close()

def run_basal_for_experiments(name):
    """
    Runs basal analysis on all masks belonging
    to supplied experiment ids and saves JSON
    into model_files.basal
    """

    files = get_mask_files_by_uuid(name)
    print("[DEBUG] total files to process:", len(files))
    print("[DEBUG] experiments to process:", sorted(set(str(f["experiment_id"]) for f in files)))

    results = []

    if len(files) == 0:
        return {
            "status": "success",
            "processed": 0,
            "results": []
        }

    conn = psycopg2.connect(**DB_CFG)

    try:
        with conn.cursor() as cur:

            for item in files:

                file_uuid = item["uuid"]
                experiment_id = item["experiment_id"]
                mask_file_name = item["model_prediction_mask"]

                mask_path = os.path.join(
                    MASK_BASE_DIR,
                    mask_file_name
                )

                print(
                    f"[INFO] Processing "
                    f"experiment={experiment_id} "
                    f"uuid={file_uuid}"
                )

                try:

                    if not os.path.exists(mask_path):
                        raise FileNotFoundError(mask_path)

                    basal_json = run_mask_basal_morphology_json(
                        nuclei_mask_nifti=mask_path
                    )

                    cur.execute(
                        """
                        UPDATE model_files
                        SET basal = %s
                        WHERE uuid = %s
                        """,
                        (
                            basal_json,
                            file_uuid
                        )
                    )

                    results.append({
                        "uuid": file_uuid,
                        "experiment_id": experiment_id,
                        "file_name": mask_file_name,
                        "status": "success"
                    })

                except Exception as e:

                    traceback.print_exc()

                    error_json = json.dumps(
                        {
                            "file_name": mask_file_name,
                            "status": "failed",
                            "error_message": str(e)
                        },
                        separators=(",", ":")
                    )

                    cur.execute(
                        """
                        UPDATE model_files
                        SET basal = %s
                        WHERE uuid = %s
                        """,
                        (
                            error_json,
                            file_uuid
                        )
                    )

                    results.append({
                        "uuid": file_uuid,
                        "experiment_id": experiment_id,
                        "file_name": mask_file_name,
                        "status": "failed",
                        "error": str(e)
                    })

            conn.commit()

        return {
            "status": "success",
            "processed": len(results),
            "results": results
        }

    except Exception as e:

        conn.rollback()
        traceback.print_exc()

        return {
            "status": "failed",
            "error": str(e)
        }

    finally:
        conn.close()
