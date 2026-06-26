import bioformats
import javabridge
import cv2
import matplotlib
import matplotlib.pyplot as plt
import os
import psycopg2
import base64
import io
import json
import numpy as np
matplotlib.use('Agg')
import nibabel as nib
import uuid
from model import predict_and_save_nifti
from analysis import properties_from_nifti
import torch
from scipy.ndimage import zoom
import SimpleITK as sitk
import tifffile

def config_colors():
    config_path = "colors.json"   # adjust path if needed
    with open(config_path, "r") as f:
        data = json.load(f)
    # Convert JSON lists to tuples
    return {k: tuple(v) for k, v in data.items()}

os.environ["CUDA_VISIBLE_DEVICES"] = "5"
#use python 3.86
#pip install numpy
# pip install python-bioformats
# pip install javabridge   #pip install python-javabridge
#
# pip install matplotlib
#pip install psycopg2
# database python
# https://www.datacamp.com/tutorial/tutorial-postgresql-python
# https://www.psycopg.org/docs/
#phase=nocolor

def get_tiff_channel_name(path):
    """
    Extract channel name from TIFF ImageDescription using key AA_Image_Channel.
    Returns:
        channel name (str) or None if not found.
    """
    try:
        with tifffile.TiffFile(path) as tif:
            desc = tif.pages[0].description
            if not desc:
                return None

            meta = {}
            for item in desc.split():
                if "=" in item:
                    key, val = item.split("=", 1)
                    meta[key] = val.strip('"')

            return meta.get("AA_Image_Channel")
    except Exception:
        return None

def percentile_normalize(img, low=2, high=99.8):
    p1 = np.percentile(img, low)
    p99 = np.percentile(img, high)
    img = np.clip(img, p1, p99)
    img = (img - p1) / (p99 - p1 + 1e-8)
    return (img * 255).astype(np.uint8)


def save_to_nifti(pixel_array, output_path):
    # Save as NIfTI file
    random_base_name = str(uuid.uuid4())[:8]
    imagename_combine_nii=f"{random_base_name}_images_combine.nii.gz"
    nifti_path = os.path.join(output_path, imagename_combine_nii)
    sitk_image = sitk.GetImageFromArray(pixel_array)

    sitk.WriteImage(sitk_image, nifti_path)
    return imagename_combine_nii

def execute_query(query):
    # Connect to your PostgreSQL database
    #psql -U new_user -d datacollection -h localhost -p 5432
    conn = psycopg2.connect(database="datacollection", user="new_user", host='134.197.75.35', password="1234", port=5432)
    cursor = conn.cursor()

    # Execute the provided query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return results


def initialize_jvm():
    javabridge.start_vm(class_path=bioformats.JARS)

def shutdown_jvm():
    try:
        javabridge.kill_vm()
    except Exception:
        pass

def process_any_file(file_path, study_id, experiment_id, file_name):
    save_img_folder_name = os.path.join("images", "exp" + experiment_id)
    if not os.path.exists(save_img_folder_name):
        os.makedirs(save_img_folder_name)

    save_images_combine_nii = os.path.join("images_combine_nii", "exp" + experiment_id)
    if not os.path.exists(save_images_combine_nii):
        os.makedirs(save_images_combine_nii)

    # model_prediction_path= os.path.join("model_prediction", "exp" + experiment_id)
    model_prediction_path= "model_prediction"
    if not os.path.exists(model_prediction_path):
        os.makedirs(model_prediction_path)

    conn = None
    cursor = None  # Initialize cursor and conn to None
    try:
        reader = bioformats.ImageReader(file_path)

        # ---------- NEW: detect TIFF & load TIFF channel name ----------
        ext = os.path.splitext(file_path)[1].lower()
        is_tiff = ext in (".tif", ".tiff")
        tiff_channel_name = get_tiff_channel_name(file_path) if is_tiff else None
        # ---------------------------------------------------------------

        # Get metadata
        metadata = bioformats.get_omexml_metadata(file_path)
        root = bioformats.OMEXML(metadata)
        pixels = root.image().Pixels
        num_channels = pixels.SizeC
        # print(num_channels,"cccc")
        num_slices = pixels.SizeZ
        # Dictionary to map fluorophores to  colors
        fluorophore_colors = config_colors()

        # Extract details
        dimension_order = pixels.DimensionOrder
        physical_size_x = pixels.PhysicalSizeX
        physical_size_y = pixels.PhysicalSizeY
        physical_size_z = pixels.PhysicalSizeZ
        size_c = pixels.SizeC
        size_t = pixels.SizeT
        size_x = pixels.SizeX
        size_y = pixels.SizeY
        size_z = pixels.SizeZ
        print(physical_size_x,physical_size_y,physical_size_z,"phicalXYZ")

        if physical_size_x is not None and physical_size_z is not None:
            if physical_size_x < physical_size_z:
                resize_factor = physical_size_x / physical_size_z
            else:
                resize_factor = physical_size_z / physical_size_x
        else:
            resize_factor = 1.0  # Default value or any appropriate fallback
            print("Warning: One or both physical sizes are None. Using default resize factor.")

        # Extract details
        details = {
            "dimension_order": dimension_order,
            "physical_size_x": f"{physical_size_x} {pixels.PhysicalSizeXUnit}",
            "physical_size_y": f"{physical_size_y} {pixels.PhysicalSizeYUnit}",
            "physical_size_z": f"{physical_size_z} {pixels.PhysicalSizeZUnit}",
            "size_c": size_c,
            "size_t": size_t,
            "size_x": size_x,
            "size_y": size_y,
            "size_z": size_z
        }

        # Convert to JSON
        if details and isinstance(details, dict):
            json_details = json.dumps(details, indent=4)
        else:
            json_details = None
            print("Details are empty or not in a valid format")

        conn = psycopg2.connect(
            database="datacollection",
            user="new_user",
            host='134.197.75.35',
            password="1234",
            port=5432
        )
        cursor = conn.cursor()

        # Loop through slices
        for slice_index in range(num_slices):
            # Initialize merged image with channels
            merged_image = np.zeros(
                (reader.rdr.getSizeY(), reader.rdr.getSizeX(), 3),
                dtype=np.uint8
            )

            # Loop through channels
            for channel_index in range(num_channels):
                channel_image = reader.read(c=channel_index, z=slice_index)
                channel_image = cv2.normalize(
                    channel_image, None, 0, 255,
                    cv2.NORM_MINMAX, cv2.CV_8U
                )

                # ---------- UPDATED: fluorophore name logic with TIFF support ----------
                if is_tiff:
                    fluorophore_name = tiff_channel_name
                else:
                    channel = pixels.Channel(channel_index)
                    fluorophore_name = channel.Name

                if fluorophore_name is not None:
                    fluorophore_name = str(fluorophore_name)

                fluorophore_color = fluorophore_colors.get(fluorophore_name)
                # ----------------------------------------------------------------------

                if fluorophore_color is None:
                    if channel_index == 0:
                        fluorophore_color = (0,0,255)
                    elif channel_index == 1:
                        fluorophore_color = (0,255,0)
                    elif channel_index == 2:
                        fluorophore_color = (255,255,0)
                    elif channel_index == 3:
                        fluorophore_color = (255,0,0)
                    else:
                        fluorophore_color = (255,255,255)

                merged_image = np.maximum(
                    merged_image,
                    (np.array(fluorophore_color) *
                     (channel_image[:, :, np.newaxis] / 255)).astype(np.uint8)
                )

            # brightness_factor = 2
            # merged_image = np.clip(merged_image * brightness_factor, 0, 255).astype(np.uint8)
            resized_image = cv2.resize(
                merged_image,
                (merged_image.shape[1] // 4, merged_image.shape[0] // 4)
            )

            plt.imshow(resized_image)
            # plt.title(f'Slice {slice_index}')
            plt.axis('off')

            file_base_name = os.path.splitext(os.path.basename(file_path))[0]
            image_filename = f'{file_base_name}_Slice_{slice_index}.jpg'
            image_filepath = os.path.join(save_img_folder_name, image_filename)
            plt.savefig(image_filepath, bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()

            query = "INSERT INTO processed_files (study_id, experiment_id, file_name, encrypt_image) VALUES (%s, %s, %s,%s)"
            data = (study_id, experiment_id, file_name, image_filepath)
            cursor.execute(query, data)

        ####################### Model prediction process #####################
        ###############################################################
        # Loop through slices for 3D nii.gz
        pixel_data = []
        for slice_index in range(num_slices):
            channel_data = []
            # Loop through channels
            for channel_index in range(num_channels):
                channel_image = reader.read(c=channel_index, z=slice_index)
                if physical_size_x:
                    resized_image = cv2.resize(
                        channel_image, None,
                        fx=resize_factor, fy=resize_factor,
                        interpolation=cv2.INTER_LINEAR
                    )
                else:
                    resized_image = cv2.resize(
                        channel_image,
                        (channel_image.shape[1] // 4, channel_image.shape[0] // 4)
                    )
                channel_data.append(resized_image)
            # Convert channel data to numpy array
            channel_array = np.array(channel_data)
            # Append only the DAPI channel to pixel_data
            pixel_data.append(channel_array[0])

        # Convert the list of arrays to a numpy array
        pixel_array = np.array(pixel_data)
        # Return name of 3d file combined_nii
        niiname = save_to_nifti(pixel_array, save_images_combine_nii)

        niipath = os.path.join(save_images_combine_nii, niiname)  # make absolute nii path to load it
        model_path = os.path.join("saved_model", "best_metric_model.pth")  # load absolute path of saved_model
        vtp, nii = predict_and_save_nifti(niipath, model_prediction_path, model_path)  # result contain name of predicted files || nii,vtp
        print("Model_VTP", vtp, "Model_Mask", nii)
        torch.cuda.empty_cache()
        ####################### Model prediction process END#####################
        ###############################################################

        ################################Analysis Mask file############
        nifti_file_nii = os.path.join(model_prediction_path, nii)
        graph_properties_json_string = properties_from_nifti(nifti_file_nii)
        #######################################

        # Move the update statement outside the loops
        query_model_files = (
            "INSERT INTO model_files "
            "(study_id, experiment_id, image_combined_file, model_prediction_files, "
            "model_prediction_mask, mask_file_analysis) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        data_model_files = (
            file_name, experiment_id, niiname, vtp, nii, graph_properties_json_string
        )  # i replace the study_id with the filename
        cursor.execute(query_model_files, data_model_files)

        query = "UPDATE files SET process = %s WHERE experiment_id = %s"
        data = ('yes', experiment_id)
        cursor.execute(query, data)

        query2 = "UPDATE files SET file_meta= %s WHERE experiment_id = %s AND file_addr=%s"
        data2 = (json_details, experiment_id, file_name)
        cursor.execute(query2, data2)

        conn.commit()
        print("ALL Processed")

    except Exception as e:
        # Handle the exception as needed, e.g., print an error message or log it
        print(f"Error processing the file: {str(e)}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def process_3dsimple_experiment(file_path, study_id, experiment_id, file_name):
    save_img_folder_name = os.path.join("images", "exp" + experiment_id)
    if not os.path.exists(save_img_folder_name):
        os.makedirs(save_img_folder_name)

    save_images_combine_nii = os.path.join("images_combine_nii", "exp" + experiment_id)
    if not os.path.exists(save_images_combine_nii):
        os.makedirs(save_images_combine_nii)

    # model_prediction_path= os.path.join("model_prediction", "exp" + experiment_id)
    model_prediction_path = "model_prediction"
    if not os.path.exists(model_prediction_path):
        os.makedirs(model_prediction_path)

    conn = None
    cursor = None  # Initialize cursor and conn to None
    try:
        reader = bioformats.ImageReader(file_path)

        # ---------- NEW: detect TIFF & load TIFF channel name ----------
        ext = os.path.splitext(file_path)[1].lower()
        is_tiff = ext in (".tif", ".tiff")
        tiff_channel_name = get_tiff_channel_name(file_path) if is_tiff else None
        # --------------------------------------------------------------

        # Get metadata
        metadata = bioformats.get_omexml_metadata(file_path)
        root = bioformats.OMEXML(metadata)
        pixels = root.image().Pixels
        num_channels = pixels.SizeC
        num_slices = pixels.SizeZ

        # Dictionary to map fluorophores to colors
        fluorophore_colors = config_colors()

        # Extract details
        dimension_order = pixels.DimensionOrder
        physical_size_x = pixels.PhysicalSizeX
        physical_size_y = pixels.PhysicalSizeY
        physical_size_z = pixels.PhysicalSizeZ
        size_c = pixels.SizeC
        size_t = pixels.SizeT
        size_x = pixels.SizeX
        size_y = pixels.SizeY
        size_z = pixels.SizeZ
        print(physical_size_x, physical_size_y, physical_size_z, "phicalXYZ")

        if physical_size_x is not None and physical_size_z is not None:
            if physical_size_x < physical_size_z:
                resize_factor = physical_size_x / physical_size_z
            else:
                resize_factor = physical_size_z / physical_size_x
        else:
            resize_factor = 1.0  # Default value or any appropriate fallback
            print("Warning: One or both physical sizes are None. Using default resize factor.")

        # Extract details
        details = {
            "dimension_order": dimension_order,
            "physical_size_x": f"{physical_size_x} {pixels.PhysicalSizeXUnit}",
            "physical_size_y": f"{physical_size_y} {pixels.PhysicalSizeYUnit}",
            "physical_size_z": f"{physical_size_z} {pixels.PhysicalSizeZUnit}",
            "size_c": size_c,
            "size_t": size_t,
            "size_x": size_x,
            "size_y": size_y,
            "size_z": size_z
        }
        # Convert to JSON
        if details and isinstance(details, dict):
            json_details = json.dumps(details, indent=4)
        else:
            json_details = None
            print("Details are empty or not in a valid format")

        conn = psycopg2.connect(
            database="datacollection",
            user="new_user",
            host='134.197.75.35',
            password="1234",
            port=5432
        )
        cursor = conn.cursor()

        # CLAHE for normalization
        def apply_clahe(image):
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            return clahe.apply(image)

        def apply_gamma_correction(image, gamma=3):
            look_up_table = np.array(
                [((i / 255.0) ** (1 / gamma)) * 255 for i in range(256)]
            ).astype("uint8")
            return cv2.LUT(image, look_up_table)

        # Process slices
        for slice_index in range(num_slices):
            merged_image = np.zeros((pixels.SizeY, pixels.SizeX, 3), dtype=np.uint8)

            for channel_index in range(num_channels):
                # Read channel image
                channel_image = reader.read(c=channel_index, z=slice_index)
                channel_image = ((channel_image - np.min(channel_image)) /
                                 (np.max(channel_image) - np.min(channel_image)) * 255).astype(np.uint8)

                # Apply CLAHE
                channel_image = apply_clahe(channel_image)
                channel_image = apply_gamma_correction(channel_image, gamma=1.5)

                # ---------- UPDATED: fluorophore name logic with TIFF support ----------
                if is_tiff:
                    fluorophore_name = tiff_channel_name
                else:
                    channel = pixels.Channel(channel_index)
                    fluorophore_name = channel.Name

                if fluorophore_name is not None:
                    fluorophore_name = str(fluorophore_name)

                fluorophore_color = fluorophore_colors.get(fluorophore_name)
                # ----------------------------------------------------------------------

                if fluorophore_color is None:
                    if channel_index == 0:
                        fluorophore_color = (0, 0, 255)
                    elif channel_index == 1:
                        fluorophore_color = (0, 255, 0)
                    elif channel_index == 2:
                        fluorophore_color = (255, 255, 0)
                    elif channel_index == 3:
                        fluorophore_color = (255, 0, 0)
                    else:
                        fluorophore_color = (0, 0, 255)

                merged_image = np.maximum(
                    merged_image,
                    (np.array(fluorophore_color) *
                     (channel_image[:, :, np.newaxis] / 255)).astype(np.uint8)
                )

            resized_image = cv2.resize(
                merged_image,
                (merged_image.shape[1] // 4, merged_image.shape[0] // 4)
            )

            plt.imshow(resized_image)
            # plt.title(f'Slice {slice_index}')
            plt.axis('off')

            file_base_name = os.path.splitext(os.path.basename(file_path))[0]
            image_filename = f'{file_base_name}_Slice_{slice_index}.jpg'
            image_filepath = os.path.join(save_img_folder_name, image_filename)
            plt.savefig(image_filepath, bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()

            query = "INSERT INTO processed_files (study_id, experiment_id, file_name, encrypt_image) VALUES (%s, %s, %s,%s)"
            data = (study_id, experiment_id, file_name, image_filepath)
            cursor.execute(query, data)

        ####################### process=yes #####################
        query = "UPDATE files SET process = %s WHERE experiment_id = %s"
        data = ('yes', experiment_id)
        cursor.execute(query, data)

        query2 = "UPDATE files SET file_meta= %s WHERE experiment_id = %s AND file_addr=%s"
        data2 = (json_details, experiment_id, file_name)
        cursor.execute(query2, data2)

        conn.commit()
        print("Simple Experiment-->Processed")

    except Exception as e:
        # Handle the exception as needed, e.g., print an error message or log it
        print(f"Error processing the file: {str(e)}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def experiment_2d(file_path, study_id, experiment_id, file_name,is_phase):
    save_img_folder_name = os.path.join("images", "exp" + experiment_id)
    if not os.path.exists(save_img_folder_name):
        os.makedirs(save_img_folder_name)

    save_images_combine_nii = os.path.join("images_combine_nii", "exp" + experiment_id)
    if not os.path.exists(save_images_combine_nii):
        os.makedirs(save_images_combine_nii)

    model_prediction_path= "model_prediction"
    if not os.path.exists(model_prediction_path):
        os.makedirs(model_prediction_path)

    conn = None
    cursor = None
    try:
        reader = bioformats.ImageReader(file_path)

        # ---------- ONLY NEW LOG LINES ----------
        ext = os.path.splitext(file_path)[1].lower()
        is_tiff = ext in (".tif", ".tiff")
        print("### LOG: is_tiff =", is_tiff)

        tiff_channel_name = get_tiff_channel_name(file_path) if is_tiff else None
        print("### LOG: TIFF channel name =", tiff_channel_name)
        # ----------------------------------------

        metadata = bioformats.get_omexml_metadata(file_path)
        root = bioformats.OMEXML(metadata)
        pixels = root.image().Pixels
        num_channels = pixels.SizeC
        num_slices = pixels.SizeZ

        fluorophore_colors = config_colors()

        dimension_order = pixels.DimensionOrder
        physical_size_x = pixels.PhysicalSizeX
        physical_size_y = pixels.PhysicalSizeY
        physical_size_z = pixels.PhysicalSizeZ
        size_c = pixels.SizeC
        size_t = pixels.SizeT
        size_x = pixels.SizeX
        size_y = pixels.SizeY
        size_z = pixels.SizeZ
        print(physical_size_x,physical_size_y,physical_size_z,"phicalXYZ")

        if physical_size_x is not None and physical_size_z is not None:
            if physical_size_x < physical_size_z:
                resize_factor = physical_size_x / physical_size_z
            else:
                resize_factor = physical_size_z / physical_size_x
        else:
            resize_factor = 1.0
            print("Warning: One or both physical sizes are None. Using default resize factor.")

        details = {
            "dimension_order": dimension_order,
            "physical_size_x": f"{physical_size_x} {pixels.PhysicalSizeXUnit}",
            "physical_size_y": f"{physical_size_y} {pixels.PhysicalSizeYUnit}",
            "physical_size_z": f"{physical_size_z} {pixels.PhysicalSizeZUnit}",
            "size_c": size_c,
            "size_t": size_t,
            "size_x": size_x,
            "size_y": size_y,
            "size_z": size_z
        }

        if details and isinstance(details, dict):
            json_details = json.dumps(details, indent=4)
        else:
            json_details = None
            print("Details are empty or not in a valid format")

        conn = psycopg2.connect(database="datacollection", user="new_user", host='134.197.75.35', password="1234", port=5432)
        cursor = conn.cursor()

        for slice_index in range(num_slices):

            merged_image = np.zeros((reader.rdr.getSizeY(), reader.rdr.getSizeX(), 3), dtype=np.uint8)

            for channel_index in range(num_channels):
                channel_image = reader.read(c=channel_index, z=slice_index)
                channel_image = percentile_normalize(channel_image, low=2, high=99.8)

                if is_phase=='phase':
                    merged_image = cv2.merge([channel_image, channel_image, channel_image])
                else:

                    # ---------------- ONLY MINIMAL LOGGING ADDED ----------------
                    if is_tiff:
                        print(f"### LOG: TIFF mode → using {tiff_channel_name} for channel {channel_index}")
                        fluorophore_name = tiff_channel_name
                    else:
                        channel = pixels.Channel(channel_index)
                        fluorophore_name = channel.Name
                        print(f"### LOG: OMEXML mode → Channel {channel_index} name =", fluorophore_name)
                    # -------------------------------------------------------------

                    fluorophore_color = fluorophore_colors.get(fluorophore_name)

                    if(fluorophore_color is None):
                        if channel_index==0:
                            fluorophore_color=(0,0,255)
                        elif channel_index==1:
                            fluorophore_color=(0,255,0)
                        elif channel_index==2:
                            fluorophore_color=(255,255,0)
                        elif channel_index==3:
                            fluorophore_color=(255,0,0)
                        else:
                            fluorophore_color=(0,0,255)

                    # --- LOG COLOR USED ---
                    print(f"### LOG: Final color for channel {channel_index} =", fluorophore_color)

                    merged_image = np.maximum(merged_image, (fluorophore_color * (channel_image[:, :, np.newaxis] / 255)).astype(np.uint8))

            resized_image = cv2.resize(merged_image, (merged_image.shape[1] // 4, merged_image.shape[0] // 4))

            plt.imshow(resized_image)
            plt.axis('off')

            file_base_name = os.path.splitext(os.path.basename(file_path))[0]
            image_filename = f'{file_base_name}_Slice_{slice_index}.jpg'
            image_filepath = os.path.join(save_img_folder_name, image_filename)
            plt.savefig(image_filepath, bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()

            query = "INSERT INTO processed_files (study_id, experiment_id, file_name, encrypt_image) VALUES (%s, %s, %s,%s)"
            data = (study_id, experiment_id, file_name, image_filepath)
            cursor.execute(query, data)

        query = "UPDATE files SET process = %s WHERE experiment_id = %s"
        data = ('yes',experiment_id)
        cursor.execute(query, data)

        query2 = "UPDATE files SET file_meta= %s WHERE experiment_id = %s AND file_addr=%s"
        data2 = (json_details, experiment_id,file_name)
        cursor.execute(query2, data2)

        conn.commit()
        print("Simple Experiment-->Processed")

    except Exception as e:
        print(f"Error processing the file: {str(e)}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def simple_experiment_2d(file_path, study_id, experiment_id, file_name, is_phase):
    save_img_folder_name = os.path.join("images", "exp" + experiment_id)
    if not os.path.exists(save_img_folder_name):
        os.makedirs(save_img_folder_name)

    save_images_combine_nii = os.path.join("images_combine_nii", "exp" + experiment_id)
    if not os.path.exists(save_images_combine_nii):
        os.makedirs(save_images_combine_nii)

    model_prediction_path = "model_prediction"
    if not os.path.exists(model_prediction_path):
        os.makedirs(model_prediction_path)

    conn = None
    cursor = None  # Initialize cursor and conn to None
    try:
        reader = bioformats.ImageReader(file_path)

        # ---------- NEW: detect TIFF & load TIFF channel name ----------
        ext = os.path.splitext(file_path)[1].lower()
        is_tiff = ext in (".tif", ".tiff")
        tiff_channel_name = get_tiff_channel_name(file_path) if is_tiff else None
        # --------------------------------------------------------------

        # Get metadata
        metadata = bioformats.get_omexml_metadata(file_path)
        root = bioformats.OMEXML(metadata)
        pixels = root.image().Pixels
        num_channels = pixels.SizeC
        num_slices = pixels.SizeZ

        # Dictionary to map fluorophores to colors (loaded from config file)
        fluorophore_colors = config_colors()

        # Extract details
        dimension_order = pixels.DimensionOrder
        physical_size_x = pixels.PhysicalSizeX
        physical_size_y = pixels.PhysicalSizeY
        physical_size_z = pixels.PhysicalSizeZ
        size_c = pixels.SizeC
        size_t = pixels.SizeT
        size_x = pixels.SizeX
        size_y = pixels.SizeY
        size_z = pixels.SizeZ
        print(physical_size_x, physical_size_y, physical_size_z, "phicalXYZ")

        if physical_size_x is not None and physical_size_z is not None:
            if physical_size_x < physical_size_z:
                resize_factor = physical_size_x / physical_size_z
            else:
                resize_factor = physical_size_z / physical_size_x
        else:
            resize_factor = 1.0  # Default value or any appropriate fallback
            print("Warning: One or both physical sizes are None. Using default resize factor.")

        # Extract details
        details = {
            "dimension_order": dimension_order,
            "physical_size_x": f"{physical_size_x} {pixels.PhysicalSizeXUnit}",
            "physical_size_y": f"{physical_size_y} {pixels.PhysicalSizeYUnit}",
            "physical_size_z": f"{physical_size_z} {pixels.PhysicalSizeZUnit}",
            "size_c": size_c,
            "size_t": size_t,
            "size_x": size_x,
            "size_y": size_y,
            "size_z": size_z
        }

        # Convert to JSON
        if details and isinstance(details, dict):
            json_details = json.dumps(details, indent=4)
        else:
            json_details = None
            print("Details are empty or not in a valid format")

        conn = psycopg2.connect(
            database="datacollection",
            user="new_user",
            host='134.197.75.35',
            password="1234",
            port=5432
        )
        cursor = conn.cursor()

        for slice_index in range(num_slices):
            # Initialize merged image with channels
            merged_image = np.zeros(
                (reader.rdr.getSizeY(), reader.rdr.getSizeX(), 3),
                dtype=np.uint8
            )

            # Loop through channels
            for channel_index in range(num_channels):
                channel_image = reader.read(c=channel_index, z=slice_index)
                # channel_image = cv2.normalize(channel_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                channel_image = percentile_normalize(channel_image, low=2, high=99.7)

                if is_phase == 'phase':
                    merged_image = cv2.merge([channel_image, channel_image, channel_image])
                else:
                    # --------- UPDATED: fluorophore name logic with TIFF support ----------
                    if is_tiff:
                        # Use name from TIFF metadata (AA_Image_Channel)
                        fluorophore_name = tiff_channel_name
                    else:
                        # Use OMEXML channel name for non-TIFF (CZI, LIF, etc.)
                        channel = pixels.Channel(channel_index)
                        fluorophore_name = channel.Name

                    # Ensure it's a plain string if not None
                    if fluorophore_name is not None:
                        fluorophore_name = str(fluorophore_name)

                    # Look up color from config
                    fluorophore_color = fluorophore_colors.get(fluorophore_name)
                    # ----------------------------------------------------------------------

                    # Fallback to index-based colors if not found
                    if fluorophore_color is None:
                        if channel_index == 0:
                            fluorophore_color = (0, 0, 255)
                        elif channel_index == 1:
                            fluorophore_color = (0, 255, 0)
                        elif channel_index == 2:
                            fluorophore_color = (255, 255, 0)
                        elif channel_index == 3:
                            fluorophore_color = (255, 0, 0)
                        else:
                            fluorophore_color = (0, 0, 255)

                    merged_image = np.maximum(
                        merged_image,
                        (np.array(fluorophore_color) *
                         (channel_image[:, :, np.newaxis] / 255)).astype(np.uint8)
                    )

            resized_image = cv2.resize(
                merged_image,
                (merged_image.shape[1] // 4, merged_image.shape[0] // 4)
            )

            plt.imshow(resized_image)
            # plt.title(f'Slice {slice_index}')
            plt.axis('off')

            file_base_name = os.path.splitext(os.path.basename(file_path))[0]
            image_filename = f'{file_base_name}_Slice_{slice_index}.jpg'
            image_filepath = os.path.join(save_img_folder_name, image_filename)
            plt.savefig(image_filepath, bbox_inches='tight', pad_inches=0, dpi=300)
            plt.close()

            query = "INSERT INTO processed_files (study_id, experiment_id, file_name, encrypt_image) VALUES (%s, %s, %s,%s)"
            data = (study_id, experiment_id, file_name, image_filepath)
            cursor.execute(query, data)

        # process = yes
        query = "UPDATE files SET process = %s WHERE experiment_id = %s"
        data = ('yes', experiment_id)
        cursor.execute(query, data)

        query2 = "UPDATE files SET file_meta= %s WHERE experiment_id = %s AND file_addr=%s"
        data2 = (json_details, experiment_id, file_name)
        cursor.execute(query2, data2)

        conn.commit()
        print("Simple Experiment-->Processed")

    except Exception as e:
        # Handle the exception as needed, e.g., print an error message or log it
        print(f"Error processing the file: {str(e)}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def combine_process():
    initialize_jvm()
    try:
        query = "SELECT study_id,experiment_id,file_addr,ex_type,phase_info FROM files WHERE process IS NULL"
        results = execute_query(query)
        print(results)

        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        upload_directory = os.path.join(parent_directory, "uploads")

        # List of allowed extensions
        allowed_extensions = [".ics", ".czi", ".tiff", ".tif"]

        for result in results:
            study_id, experiment_id, file_name, ex_type, phase_info = result
            # Check if the file_path ends with any of the allowed extensions
            if any(file_name.endswith(ext) for ext in allowed_extensions):
                # Construct the full path using the parent directory
                full_file_path = os.path.join(upload_directory, file_name)
                if ex_type == "3D morphogenesis":
                    process_any_file(full_file_path, study_id,experiment_id,file_name)
                elif ex_type == "3D non-quantitative Experiment":
                    process_3dsimple_experiment(full_file_path, study_id, experiment_id, file_name)
                elif ex_type == "3D Experiment":
                    process_any_file(full_file_path, study_id, experiment_id, file_name)
                elif ex_type == "2D Experiment":
                    experiment_2d(full_file_path, study_id,experiment_id,file_name,phase_info)
                elif ex_type == "2D non-quantitative Experiment":
                    simple_experiment_2d(full_file_path, study_id,experiment_id,file_name,phase_info)
    finally:
            shutdown_jvm()

if __name__ == "__main__":
    combine_process()
