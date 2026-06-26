import os
import uuid
import torch
import nibabel as nib
import numpy as np
import cc3d
import vtk
import SimpleITK as sitk

from vtk.util import numpy_support
from scipy import ndimage
from cellpose import models


def robust_normalize(img):
    img = img.astype(np.float32)

    p1 = np.percentile(img, 1)
    p99 = np.percentile(img, 99.5)

    print("Auto normalization range p1/p99.5:", p1, p99)

    img = np.clip(img, p1, p99)
    img = (img - p1) / (p99 - p1 + 1e-8)

    return img


def resize_volume(img_zyx, spacing_xyz, desired_spacing=(1.0, 1.0, 1.0)):
    sx, sy, sz = spacing_xyz

    zoom_factors = (
        sz / desired_spacing[2],
        sy / desired_spacing[1],
        sx / desired_spacing[0],
    )

    print("Resize factors Z,Y,X:", zoom_factors)

    return ndimage.zoom(img_zyx, zoom_factors, order=1)


def auto_cellpose_params(img_zyx):
    bright_ratio = np.mean(img_zyx > 0.2)
    print("Auto bright ratio:", bright_ratio)

    if bright_ratio > 0.25:
        diameter = 12
        flow_threshold = 0.8
        cellprob_threshold = 0.3
        min_size = 30
    elif bright_ratio > 0.10:
        diameter = 15
        flow_threshold = 0.6
        cellprob_threshold = 0.1
        min_size = 30
    else:
        diameter = 20
        flow_threshold = 0.4
        cellprob_threshold = 0.0
        min_size = 50

    return diameter, flow_threshold, cellprob_threshold, min_size


def remove_small_labels(labels, min_size=50):
    labels = labels.astype(np.uint16)
    clean = np.zeros_like(labels, dtype=np.uint16)

    new_label = 1
    for label_id in range(1, int(labels.max()) + 1):
        comp = labels == label_id

        if comp.sum() >= min_size:
            clean[comp] = new_label
            new_label += 1

    return clean


def save_vtp_from_labels(labels_zyx, output_folder, base_name):
    labels_vtk = np.transpose(labels_zyx, (2, 1, 0))
    labels_vtk = np.ascontiguousarray(labels_vtk.astype(np.uint16))

    print("VTK labels shape X,Y,Z:", labels_vtk.shape)
    print("VTK max label:", labels_vtk.max())

    if labels_vtk.max() == 0:
        print("No connected components found. VTP not saved.")
        return None

    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(labels_vtk.shape)
    vtk_image.AllocateScalars(vtk.VTK_UNSIGNED_SHORT, 1)

    vtk_array = numpy_support.numpy_to_vtk(
        labels_vtk.ravel(order="F"),
        deep=True,
        array_type=vtk.VTK_UNSIGNED_SHORT
    )

    vtk_array.SetName("Cell_ID")
    vtk_image.GetPointData().SetScalars(vtk_array)

    discrete_marching_cubes = vtk.vtkDiscreteMarchingCubes()
    discrete_marching_cubes.SetInputData(vtk_image)
    discrete_marching_cubes.GenerateValues(
        int(labels_vtk.max()),
        1,
        int(labels_vtk.max())
    )
    discrete_marching_cubes.Update()

    smooth_filter = vtk.vtkSmoothPolyDataFilter()
    smooth_filter.SetInputConnection(discrete_marching_cubes.GetOutputPort())
    smooth_filter.SetNumberOfIterations(500)
    smooth_filter.FeatureEdgeSmoothingOff()
    smooth_filter.BoundarySmoothingOn()
    smooth_filter.Update()

    vtp_name = f"{base_name}_connected_components.vtp"
    vtp_output_path = os.path.join(output_folder, vtp_name)

    vtp_writer = vtk.vtkXMLPolyDataWriter()
    vtp_writer.SetFileName(vtp_output_path)
    vtp_writer.SetInputConnection(smooth_filter.GetOutputPort())
    vtp_writer.Write()

    print(f"Connected components saved: {vtp_name}")

    return vtp_name


def predict_and_save_nifti(image_path, output_folder, model_path=None):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    os.makedirs(output_folder, exist_ok=True)

    # Read image using SimpleITK
    sitk_image = sitk.ReadImage(image_path)
    spacing_xyz = sitk_image.GetSpacing()
    img_zyx = sitk.GetArrayFromImage(sitk_image).astype(np.float32)

    print("Original shape Z,Y,X:", img_zyx.shape)
    print("Original spacing X,Y,Z:", spacing_xyz)
    print("Original min/max:", img_zyx.min(), img_zyx.max())

    # Resize only if spacing is not near 1.0
    if all(abs(s - 1.0) < 0.05 for s in spacing_xyz):
        print("Skipping resize; spacing already near 1.0")
    else:
        img_zyx = resize_volume(
            img_zyx,
            spacing_xyz=spacing_xyz,
            desired_spacing=(1.0, 1.0, 1.0)
        )

    print("Final image shape Z,Y,X:", img_zyx.shape)

    # Normalize
    img_zyx = robust_normalize(img_zyx)
    print("Normalized min/max:", img_zyx.min(), img_zyx.max())

    # Auto Cellpose params
    diameter, flow_threshold, cellprob_threshold, min_size = auto_cellpose_params(img_zyx)

    print("Auto Cellpose parameters:")
    print("diameter:", diameter)
    print("flow_threshold:", flow_threshold)
    print("cellprob_threshold:", cellprob_threshold)
    print("min_size:", min_size)

    # Load Cellpose cpsam model
    use_gpu = torch.cuda.is_available()
    print("Using Cellpose GPU:", use_gpu)

    model = models.CellposeModel(
        gpu=use_gpu,
        pretrained_model="cpsam"
    )

    # Cellpose 3D inference
    masks, flows, styles = model.eval(
        img_zyx,
        diameter=diameter,
        channel_axis=None,
        z_axis=0,
        do_3D=True,
        normalize=False,
        flow_threshold=flow_threshold,
        cellprob_threshold=cellprob_threshold,
        min_size=min_size,
        batch_size=8
    )

    predicted_volume = masks.astype(np.uint16)
    print("Raw Cellpose labels:", predicted_volume.max())

    # Connected components
    labels_out = cc3d.connected_components(
        predicted_volume,
        connectivity=26
    ).astype(np.uint16)

    print("Connected components before cleanup:", labels_out.max())

    labels_out = remove_small_labels(
        labels_out,
        min_size=min_size
    )

    print("Connected components after cleanup:", labels_out.max())

    # Save NIfTI
    random_base_name = str(uuid.uuid4())[:8]
    predicted_nii = f"{random_base_name}_predicted_mask.nii.gz"
    nii_output_path = os.path.join(output_folder, predicted_nii)

    nib.save(
        nib.Nifti1Image(labels_out.astype(np.uint16), affine=np.eye(4)),
        nii_output_path
    )

    print(f"Predicted mask saved: {predicted_nii}")

    # Save VTP
    vtp_name = save_vtp_from_labels(
        labels_zyx=labels_out,
        output_folder=output_folder,
        base_name=random_base_name
    )

    return vtp_name, predicted_nii
