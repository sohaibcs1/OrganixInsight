import numpy as np
import nibabel as nib
from scipy.spatial import ConvexHull, distance
from scipy.spatial.distance import pdist
from skimage import measure
import json

def compute_cell_properties_from_nifti(nifti_file):
    # Load NIfTI file
    img = nib.load(nifti_file)
    
    # Get the 3D data array
    data = img.get_fdata()
    
    # Assuming the data is binary and represents nuclei
    # You might need to threshold or apply other preprocessing steps
    # Segmentation
    labeled_mask, num_labels = measure.label(data, return_num=True)
    
    # Calculate properties for each labeled region (cell)
    props = measure.regionprops(labeled_mask)
    
    # Initialize variables to accumulate covariance matrices and areas
    sum_cov_matrix = np.zeros((3, 3))
    total_volume = 0
    num_cells = 0
    
    for prop in props:
        cell_pixels = np.array(prop.coords)
        if len(cell_pixels) >= 4:  # Ensure there are enough points for Delaunay triangulation
            # Compute covariance matrix for the transformed point cloud
            cov_matrix = np.cov(cell_pixels, rowvar=False)
            
            # Accumulate covariance matrices
            sum_cov_matrix += cov_matrix
            
            # Accumulate area
            total_volume += len(cell_pixels)
            num_cells += 1  # Increment the cell count
    
    volume_nulci = total_volume / num_cells if num_cells > 0 else 0
    # Compute properties based on the summed covariance matrix
    eigenvalues, _ = np.linalg.eigh(sum_cov_matrix)
    eigenvalues.sort()
    principal_moments = np.sqrt(eigenvalues)
    elongation = principal_moments[2] / principal_moments[0]
    flatness = principal_moments[2] / principal_moments[1]
    
    return {
        "Nuclear Elongation": float(elongation),
        "Nuclear Flatness": float(flatness),
        "Nuclear Volume": float(volume_nulci),
    }


def compute_colony_properties_from_nifti(nifti_file):
    # Load NIfTI file
    img = nib.load(nifti_file)

    # Get the 3D data array
    data = img.get_fdata()

    # Assuming the data is binary and represents nuclei
    # You might need to threshold or apply other preprocessing steps
    # Segmentation
    labeled_mask, num_labels = measure.label(data, return_num=True)

    # Calculate properties for each labeled region (cell)
    props = measure.regionprops(labeled_mask)

    cell_pixels_list = []
    total_nuclei_volume = 0
    for prop in props:
        cell_pixels = np.array(prop.coords)
        if len(cell_pixels) >= 4:  # Ensure there are enough points for Delaunay triangulation
            cell_pixels_list.append(cell_pixels)
            total_nuclei_volume += len(cell_pixels)

    # Combine all cell pixels into a single point cloud
    all_cell_pixels = np.vstack(cell_pixels_list)

    # Compute covariance matrix for the combined point cloud
    cov_matrix = np.cov(all_cell_pixels, rowvar=False)

    # Compute eigenvalues and eigenvectors of the covariance matrix
    eigenvalues, _ = np.linalg.eigh(cov_matrix)

    # Sort eigenvalues in ascending order
    eigenvalues.sort()

    # Principal moments (sorted)
    principal_moments = np.sqrt(eigenvalues)

    # Elongation
    elongation = principal_moments[2] / principal_moments[0]

    # Flatness
    flatness = principal_moments[2] / principal_moments[1]

    # Compute the Convex Hull
    hull = ConvexHull(all_cell_pixels)
    convex_hull_area = hull.area
    convex_hull_voulme= hull.volume
    # Calculate diameter and radius
    hull_points = all_cell_pixels[hull.vertices]
    # pairwise Euclidean distances between all points
    distances = pdist(hull_points)
    diameter = np.max(distances)
    radius = diameter / 2
    
    # mean edge length
    mean_edge_length = np.mean(distances)
    
    # Maximum and minimum edge lengths
    max_edge_length = np.max(distances)
    
    # Calculate the lumen volume index
#     print(convex_hull_voulme," ", total_nuclei_volume)
    lumen_volume_index = convex_hull_voulme - total_nuclei_volume
    # Ensure lumen volume index is not negative
    lumen_volume_index = max(lumen_volume_index, 0)


    return {
        "Colony Elongation": float(elongation),
        "Colony Flatness": float(flatness),
        "Colony Diameter": float(diameter),
        "Colony Radius": float(radius),
        "Number of Cells in Colony": len(cell_pixels_list),
        "Max Neighbourhood Distance": float(max_edge_length),
        "Mean Neighbourhood Distance": float(mean_edge_length),
        "Volume of Colony Convex Hull": float(convex_hull_voulme),
        "Lumen Volume": float(lumen_volume_index)
    }

def properties_from_nifti(nifti_file):
    colony_properties = compute_colony_properties_from_nifti(nifti_file)
    cell_properties = compute_cell_properties_from_nifti(nifti_file)
    # Combine colony and cell properties
    combined_properties = cell_properties.copy()
    combined_properties.update(colony_properties)
    # colony_properties_json_str = json.dumps(combined_properties, indent=4)
    colony_properties_json_str = json.dumps(combined_properties, separators=(',', ':'))
    return colony_properties_json_str

