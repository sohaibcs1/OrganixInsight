from flask import Flask, render_template, jsonify, send_file, Response
import os
import vtk
import numpy as np
import hashlib

app = Flask(__name__)

# Directory where original and processed VTP files are stored
current_dir = os.path.dirname(os.path.abspath(__file__))
VTP_FILES_DIR = os.path.abspath(os.path.join(current_dir, "..", "model_prediction"))
PROCESSED_FILES_DIR = os.path.join(current_dir, "hash_vtps")


# Ensure processed directory exists
os.makedirs(PROCESSED_FILES_DIR, exist_ok=True)

def get_processed_filename(input_vtp_path):
    # Generate a unique filename for the processed file using a hash
    file_hash = hashlib.md5(open(input_vtp_path, 'rb').read()).hexdigest()
    return os.path.join(PROCESSED_FILES_DIR, f"{file_hash}_processed.vtp")

def process_and_save_vtp(input_vtp_path):
    # Read the input VTP file
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(input_vtp_path)
    reader.Update()
    polydata = reader.GetOutput()

    # Apply vtkConnectivityFilter to label connected components
    connectivity_filter = vtk.vtkConnectivityFilter()
    connectivity_filter.SetInputData(polydata)
    connectivity_filter.SetExtractionModeToAllRegions()  # Extract all connected components
    connectivity_filter.ColorRegionsOn()  # Color each component with a unique scalar value
    connectivity_filter.Update()

    connected_polydata = connectivity_filter.GetOutput()

    # Ensure that 'RegionId' scalar data is selected
    scalars = connected_polydata.GetPointData().GetArray('RegionId')
    connected_polydata.GetPointData().SetScalars(scalars)

    # Apply decimation to reduce polygons
    decimate = vtk.vtkDecimatePro()
    decimate.SetInputData(connected_polydata)
    decimate.SetTargetReduction(0.2)  # Reduce 50% of triangles
    decimate.PreserveTopologyOn()
    decimate.Update()

    # Apply smoothing
    smooth_filter = vtk.vtkSmoothPolyDataFilter()
    smooth_filter.SetInputConnection(decimate.GetOutputPort())
    smooth_filter.SetNumberOfIterations(10)  # Light smoothing
    smooth_filter.SetRelaxationFactor(0.1)
    smooth_filter.Update()

    smoothed_polydata = smooth_filter.GetOutput()

    # Assign dynamic colors using a lookup table based on RegionId
    max_region_id = int(np.max(scalars.GetRange()))
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(max_region_id + 1)
    lut.Build()

    for i in range(1, max_region_id + 1):
        color = np.random.rand(3)  # Random RGB color
        lut.SetTableValue(i, color[0], color[1], color[2])

    # Write the processed polydata to a file on disk
    processed_vtp_path = get_processed_filename(input_vtp_path)
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(processed_vtp_path)
    writer.SetInputData(smoothed_polydata)
    writer.SetDataModeToBinary()  # Binary mode to reduce size
    writer.SetCompressorTypeToZLib()  # Compression for smaller file size
    writer.Write()

    print(f"Processed VTP saved at: {processed_vtp_path}")
    return processed_vtp_path

@app.route('/get_vtp/<filename>')
def serve_processed_vtp(filename):
    input_vtp_path = os.path.join(VTP_FILES_DIR, filename)
    if not os.path.isfile(input_vtp_path):
        return jsonify({"error": f"File {filename} not found"}), 404

    # Check if the processed file already exists
    processed_vtp_path = get_processed_filename(input_vtp_path)
    if not os.path.exists(processed_vtp_path):
        print("Processing and saving the VTP file for the first time...")
        processed_vtp_path = process_and_save_vtp(input_vtp_path)

    # Serve the processed VTP file directly
    return send_file(processed_vtp_path, mimetype='application/xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_vtp_files')
def list_vtp_files():
    # List all .vtp files in the directory
    files = [f for f in os.listdir(VTP_FILES_DIR) if f.endswith('.vtp')]
    return jsonify(files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5012)
