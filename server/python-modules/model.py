import os
import uuid
import torch
import nibabel as nib
import numpy as np
import cc3d
import vtk
import SimpleITK as sitk
from vtk.util import numpy_support
from monai.networks.nets import SwinUNETR
from monai.inferers import sliding_window_inference
from monai.transforms import MapTransform
from scipy import ndimage

class NormalizeArray(MapTransform):
    def __init__(self, keys):
        super().__init__(keys)

    def __call__(self, data):
        for key in self.keys:
            arr = data[key]
            min_val = arr.min()
            max_val = arr.max()
            data[key] = (arr - min_val) / (max_val - min_val)
        return data

def resize_volume(img, spacing):
    depth_factor, width_factor, height_factor = spacing
    return ndimage.zoom(img, (depth_factor, width_factor, height_factor), order=1)

def predict_and_save_nifti(image_path, output_folder, model_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    os.makedirs(output_folder, exist_ok=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Load model
    model = SwinUNETR(
        img_size=(96, 96, 96),
        in_channels=1,
        out_channels=2,
        feature_size=48,
        use_checkpoint=True
    ).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    # Read image using SimpleITK
    sitk_image = sitk.ReadImage(image_path)
    spacing = sitk_image.GetSpacing()
    img_volume = sitk.GetArrayFromImage(sitk_image).astype(np.float32)

    # Apply normalization
    img_volume = NormalizeArray(keys=["image"])({"image": img_volume})["image"]

    # Reshape to (Z, Y, X) and transpose to (Y, X, Z)
    img_volume_xyz = np.transpose(img_volume, (1, 2, 0))

    # Resize using spacing
    resized_img = resize_volume(img_volume_xyz, spacing)

    # Transpose back to (Z, Y, X)
    final_volume = np.transpose(resized_img, (2, 0, 1))

    # Prepare input tensor
    val_inputs = torch.tensor(final_volume).unsqueeze(0).unsqueeze(0).to(device)

    # Inference
    with torch.no_grad():
        val_outputs = sliding_window_inference(val_inputs, (96, 96, 96), 1, model, overlap=0.8)

    if val_outputs is None or not isinstance(val_outputs, torch.Tensor):
        print("Error: sliding_window_inference returned None or unexpected value.")
        return None, None

    predicted_volume = torch.argmax(val_outputs, dim=1).cpu().numpy().astype(np.uint8)[0]

    random_base_name = str(uuid.uuid4())[:8]
    predicted_nii = f"{random_base_name}_predicted_mask.nii.gz"
    nib.save(nib.Nifti1Image(predicted_volume, affine=np.eye(4)), os.path.join(output_folder, predicted_nii))

    print(f"Predicted mask saved: {predicted_nii}")

    # Connected components
    labels_out = cc3d.connected_components(predicted_volume, connectivity=26)

    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(labels_out.shape[::-1])
    vtk_image.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1)
    vtk_array = numpy_support.numpy_to_vtk(labels_out.ravel(), deep=True)
    vtk_image.GetPointData().SetScalars(vtk_array)

    discrete_marching_cubes = vtk.vtkDiscreteMarchingCubes()
    discrete_marching_cubes.SetInputData(vtk_image)
    discrete_marching_cubes.GenerateValues(np.max(labels_out), 1, np.max(labels_out))

    smooth_filter = vtk.vtkSmoothPolyDataFilter()
    smooth_filter.SetInputConnection(discrete_marching_cubes.GetOutputPort())
    smooth_filter.SetNumberOfIterations(500)

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(np.max(labels_out) + 1)
    lut.Build()
    for i in range(1, np.max(labels_out) + 1):
        r, g, b = np.random.rand(3)
        lut.SetTableValue(i, r, g, b)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(smooth_filter.GetOutputPort())
    mapper.SetLookupTable(lut)
    mapper.SetScalarRange(0, np.max(labels_out))

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    vtp_name = f"{random_base_name}_connected_components.vtp"
    vtp_output_path = os.path.join(output_folder, vtp_name)
    vtp_writer = vtk.vtkXMLPolyDataWriter()
    vtp_writer.SetFileName(vtp_output_path)
    vtp_writer.SetInputConnection(smooth_filter.GetOutputPort())
    vtp_writer.Write()

    print(f"Connected components saved: {vtp_name}")

    return vtp_name, predicted_nii
