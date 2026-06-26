
# #pip install python-socketio
# # pip install requests
# # from processfile import initialize_jvm,process_any_file

import socketio
import app
import subprocess
import random
import time
import psutil
from analysis import properties_from_nifti
from heatmap import generate_and_plot
from cellcount import fetch_model2ds_with_meta,plot_per_experiment_improved
from processfileBulk import extract_tiles,arrayofFiles,save_files_metadata
from cc import save_consensus_panel_from_db
from basal import run_basal_for_experiments
from basal_heatmap import generate_basal_nonbasal_heatmap
from positive import run_positive_for_experiments
from positive_analysis import generate_positive_barplot
from positive_single import check_input
import json
import os
import subprocess
import random
import socket
import atexit
import requests
from PIL import Image
import threading
from queue import Queue
import traceback
import sys

# Qeue for single upload
process_queue = Queue()
_worker_started = False
_worker_lock = threading.Lock()

# # Global variables to store server details
# Global variables to store server details
paraview_processes = {}  # Dictionary to store process references and ports
sio = socketio.Client()

print("running.")
@sio.event
def connect():
    print('connection established')

@sio.event
def respond():
    sio.emit("reponse", {"success": True})

@sio.event
def getNumbers():
    # initialize_jvm()
    sio.emit("numbers","aaasssss")

@sio.event
def getHeatmap(name):
    # Extract data array

    # Initialize arrays for mask_file_analysis and label
    mask_file_analysis_array = []
    label_array = []

    # Iterate over the data array to extract mask_file_analysis and label
    for item in name:
        mask_file_analysis_array.append(item["mask_file_analysis"])
        label_array.append(item["label"])
    imgbase64=generate_and_plot(mask_file_analysis_array,label_array)
    sio.emit("heatmap",imgbase64)

@sio.event
def getHeatmap_basal(name):
    basal_analysis_array = []
    label_array = []

    for item in name:
        if not item.get("basal"):
            continue

        basal_analysis_array.append(item["basal"])
        label_array.append(item.get("label", ""))

    if len(basal_analysis_array) == 0:
        sio.emit("heatmap_basal", "")
        return

    imgbase64 = generate_basal_nonbasal_heatmap(
        basal_analysis_array,
        label_array
    )

    sio.emit("heatmap_basal", imgbase64)

@sio.event
def getPositiveBarplot(name):
    positive_array = []
    label_array = []

    for item in name:
        if not item.get("positive"):
            continue

        positive_array.append(item["positive"])
        label_array.append(item.get("label", ""))

    if len(positive_array) == 0:
        sio.emit("positive_barplot", "")
        return

    imgbase64 = generate_positive_barplot(
        positive_array,
        label_array
    )

    sio.emit("positive_barplot", imgbase64)

@sio.event
def getbasal(name):
    # Extract data array
    result = run_basal_for_experiments(name)
    sio.emit("basal",result)

# @sio.event
# def getpositive(name):
#     # Extract data array
#     result = run_positive_for_experiments(name)
#     sio.emit("positive",result)

@sio.event
def getpositive(payload):
    result = run_positive_for_experiments(payload)
    sio.emit("positive", result)


@sio.event
def getpositive_input(name):
    result = check_input(name)
    sio.emit("positive_input", result)


@sio.event
def getCellcount(data):
    try:
        # Flatten payload: accept {data: [...] } or just [...]
        rows = data.get("data", data) if isinstance(data, dict) else data

        # Basic validation
        if not isinstance(rows, list):
            raise ValueError("Expected a list of rows under key 'data'.")
        if not rows:
            raise ValueError("Empty 'data' list.")

        # Each row should be [experiment_id, condition, treatment_group]
        for i, r in enumerate(rows):
            if not (isinstance(r, (list, tuple)) and len(r) >= 3):
                raise ValueError(f"Row {i} invalid: expected [id, condition, group], got {r}")

        # Use the incoming rows (not a hardcoded meta_data)
        df_db, df_meta, df_merged = fetch_model2ds_with_meta(rows)
        img_b64, normalized =plot_per_experiment_improved(df_merged)  # saves JPG in current path

        # Send a compact ack
        payload = {
            "status": "ok",
            "received": len(rows),
            "image_base64": img_b64,
            "message": "Plot generated."
        }
        sio.emit("cellcount", payload)
        return payload  # ack
    except Exception as e:
        err = {"status": "error", "message": str(e)}
        sio.emit("cellcount", err)
        return err

@sio.event
def getCc(data):
    try:
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object.")

        rid = str(data.get("random_id") or data.get("id") or "").strip()
        if not rid:
            raise ValueError("Missing 'random_id' (or 'id').")

        out = save_consensus_panel_from_db(
            rid=rid,
            results_dir="static/results",
            table="model_2d_prots",
            reps=3,
            sample_size=2000,
            iterations=100,
            k_clusters=2
        )

        payload = {
            "status": "ok",
            "filename": out,
            "message": "Plot generated."
        }
        sio.emit("cccluster", payload)
        return payload
    except Exception as e:
        err = {"status": "error", "message": str(e)}
        sio.emit("cccluster", err)
        return err

@sio.event
def getAnalysis(name):
    # nifti_file = '/home/msohaib/3D_organixInsight/server/python-modules/model_prediction/67ea4dbf_predicted_mask.nii.gz'
    nifti_file = os.path.join('/home/msohaib/3D_organixInsight/server/python-modules/model_prediction', name)
    graph_properties_json = properties_from_nifti(nifti_file)
    graph_properties_json_string = json.dumps(graph_properties_json)
    sio.emit("numbers", {"numbers": graph_properties_json_string})



@sio.event
def getParaviewUrl(name):
    # Generate a new port for the new request
    PORT = "5012"
    sio.emit("url", {"url": PORT, "file_name": name})

def _process_worker():
    print("[WORKER] started, waiting for jobs...")
    while True:
        job = process_queue.get()  # blocks until something is queued
        try:
            print(f"[WORKER] got job. queue_left={process_queue.qsize()}")

            # run your script
            subprocess.run([sys.executable, "processfile.py"], check=True)

            # ✅ keep your emit EXACTLY (frontend unchanged)
            sio.emit("response", "processed")
            print("[WORKER] done -> emitted response=processed")

        except Exception as e:
            print("[WORKER] ERROR:", e)
            traceback.print_exc()
            # optional: notify error channel
            # sio.emit("response_error", str(e))

        finally:
            process_queue.task_done()


# @sio.event
# def processFiles():
#     try:
#         subprocess.run(['python', 'processfile.py'], check=True)
#         sio.emit("response", "processed")
#         print("done")
#     except subprocess.CalledProcessError as e:
#         print(f"Error running 'processfile.py': {e}")
@sio.event
def processFiles(data=None):
    global _worker_started

    process_queue.put(True)
    print(f"[QUEUE] added job. queue_size={process_queue.qsize()}")

    # start worker ONCE
    with _worker_lock:
        if not _worker_started:
            _worker_started = True
            # ✅ for socketio.Client, this is safer than raw threading.Thread
            sio.start_background_task(_process_worker)

@sio.event
def processFilesbulk(files):
    # ---- inputs & paths ----
    randomid = files["randomid"]
    print(f"[INFO] randomid={randomid}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    uploads_dir = os.path.abspath(os.path.join(current_dir, "..", "uploads"))
    split_dir = os.path.join("imagesbulk", f"randomId{randomid}")

    # ensure output root exists
    os.makedirs(split_dir, exist_ok=True)

    # build a *snapshot* of the incoming file list (names only)
    try:
        namelist = arrayofFiles(randomid)  # e.g., ["file1.czi", "file2.czi"]
        if not isinstance(namelist, (list, tuple)):
            raise TypeError(f"arrayofFiles({randomid}) must return list/tuple, got {type(namelist)}")
        namelist = [str(x) for x in namelist]
    except Exception as e:
        msg = f"[ERR] arrayofFiles({randomid}) failed: {e}"
        print(msg)
        sio.emit("response_error", {"randomid": randomid, "error": msg})
        return

    # where the inputs live (keep as uploads_dir unless you know they landed in split_dir)
    input_root = uploads_dir

    # ---- aggregate results across files ----
    aggregated_results = {}

    for fname in list(namelist):  # snapshot to avoid mutations during iteration
        fpath = os.path.join(input_root, fname)
        print(f"[INFO] Processing: {fpath}")

        if not os.path.isfile(fpath):
            print(f"[WARN] Skipping missing file: {fpath}")
            continue

        try:
            # extract_tiles should return: { "A1": ["P1", ...], "A2": [...], ... }
            # results = extract_tiles(fpath, split_dir)
            norm_mode = "global"
            results = extract_tiles( fpath, split_dir, norm_mode=norm_mode, p_low=2, p_high=99.8, bg_sub_percentile=None,anti_saturation=True, )
            if results is None:
                print(f"[WARN] extract_tiles returned None for {fname}; treating as empty.")
                results = {}
            if not isinstance(results, dict):
                raise TypeError(f"extract_tiles({fname}) must return dict, got {type(results)}")

            # safe merge (use your merge_results if present; else do a fallback)
            try:
                merge_results(aggregated_results, results)  # your helper
            except NameError:
                # fallback merge if merge_results isn't defined in this scope
                for well, tiles in results.items():
                    if not isinstance(tiles, (list, tuple)):
                        print(f"[WARN] Tiles for well '{well}' not list/tuple; skipping.")
                        continue
                    aggregated_results.setdefault(well, [])
                    aggregated_results[well].extend([str(t) for t in tiles])

        except Exception as e:
            print(f"[ERR] Failed processing {fname}: {e}")

    # ---- write DB rows for ALL tiles ----
    try:
        save_files_metadata(randomid, aggregated_results)
        print(f"[OK] DB write completed for randomid={randomid}")
    except Exception as e:
        msg = f"[ERR] save_files_metadata failed for randomid={randomid}: {e}"
        print(msg)
        sio.emit("response_error", {"randomid": randomid, "error": msg})
        return

    # ---- run the follow-up script (no threading) ----
    try:
        # prefer absolute path + current interpreter for reliability
        import sys
        script_path = os.path.join(current_dir, "processfilerun_bulk.py")
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")

        completed = subprocess.run(
            [sys.executable, script_path],
            cwd=current_dir,
            check=True,
            capture_output=True,
            text=True
        )
        if completed.stdout:
            print(f"[processfilerun_bulk.py][STDOUT]\n{completed.stdout.strip()}")
        if completed.stderr:
            print(f"[processfilerun_bulk.py][STDERR]\n{completed.stderr.strip()}")

        # only emit success after everything finished cleanly
        sio.emit("response", randomid)
        print("[OK] done")

    except subprocess.CalledProcessError as e:
        print(f"[ERR] processfilerun_bulk.py failed (rc={e.returncode}): {e}\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}")
        sio.emit("response_error", {
            "randomid": randomid,
            "error": f"processfilerun_bulk.py failed (rc={e.returncode})"
        })
    except Exception as e:
        print(f"[ERR] Error running processfilerun_bulk.py: {e}")
        sio.emit("response_error", {"randomid": randomid, "error": str(e)})

# @sio.event
# def processFilesbulk(files):
#     randomid = files["randomid"]
#     print(randomid, "iddddddddddddddd")
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     uploads_dir = os.path.abspath(os.path.join(current_dir, '..', 'uploads'))
#     split_dir = os.path.join("imagesbulk", "randomId" + randomid)

#     # Get the list of filenames to process (make sure this returns just names, not paths)
#     namelist = arrayofFiles(randomid)  # e.g., ["file1.czi", "file2.czi"]

#     # If your files are actually under split_dir, use split_dir; if they're under uploads_dir, keep uploads_dir.
#     input_root = uploads_dir  # or: uploads_dir

#     # Aggregate results from all files here
#     aggregated_results = {}

#     # Iterate over a SNAPSHOT of the list (no self-appending!)
#     for fname in list(namelist):
#         fpath = os.path.join(input_root, fname)
#         print(f"[INFO] Processing {fpath}")
#         try:
#             # extract_tiles should return { "A1": ["P1",...], "A2": [...], ... }
#             results = extract_tiles(fpath, split_dir)   # output_root = split_dir (per your design)
#             merge_results(aggregated_results, results)
#         except Exception as e:
#             print(f"[ERR] Failed {fname}: {e}")

#     # Now write DB rows for ALL tiles from all files
#     save_files_metadata(randomid, aggregated_results)
#     try:
#         subprocess.run(['python', 'processfilerun_bulk.py'], check=True)
#         sio.emit("response", randomid)
#         print("done")
#     except subprocess.CalledProcessError as e:
#         print(f"Error running 'processfile.py': {e}")



try:
    sio.connect('http://localhost:6080')
    sio.wait()
except:
    sio.connect('http://localhost:6080')
    sio.wait()




# server.py

# from flask import Flask, send_from_directory,request
# import socketio
# import os
# from processfile import combine_process

# # #pip install python-socketio
# # # pip install requests

# app = Flask(__name__)
# # sio = socketio.Server()
# sio = socketio.Server(cors_allowed_origins='*')

# @app.route('/images/<exp_dir>/<filename>')
# def serve_image(exp_dir, filename):
#     return send_from_directory(os.path.join('images', exp_dir), filename)

# @sio.event
# def connect(sid, environ):
#     print('Client connected', sid)

# @sio.event
# def respond(sid, data):
#     sio.emit("response", {"success": True})

# @sio.event
# def getNumbers(sid):
#     # initialize_jvm()
#     sio.emit("numbers", "server",room=sid)

# @sio.event
# def processFiles():
#     # initialize_jvm()
#     combine_process()
#     sio.emit("response", "files are Processed and saved in DB")

# if __name__ == '__main__':
#     app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
#     app.run(debug=True,host='0.0.0.0', port=6080)  # Set the port to 6080

