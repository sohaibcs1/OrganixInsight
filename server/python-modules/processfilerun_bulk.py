
import os
import shutil
import psycopg2
import json

def simple_experiment_2d(file_path, study_id, experiment_id, file_name, is_phase):
    # Create destination folder if it doesn't exist
    save_img_folder_name = os.path.join("images", "exp" + experiment_id)
    os.makedirs(save_img_folder_name, exist_ok=True)

    # Build destination path
    file_base_name = os.path.basename(file_path)
    image_filepath = os.path.join(save_img_folder_name, file_base_name)

    # Copy the image file to new location
    shutil.copy2(file_path, image_filepath)
    print(f"✅ Copied {file_path} → {image_filepath}")

    # Dummy metadata (or you can set it to None)
    json_details = json.dumps({
        "source": "copied_only",
        "note": "No Bioformats processing applied"
    }, indent=4)

    # Save to DB
    conn = psycopg2.connect(database="datacollection", user="new_user", host='134.197.75.35', password="1234", port=5432)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO processed_files (study_id, experiment_id, file_name, encrypt_image) VALUES (%s, %s, %s, %s)",
                   (study_id, experiment_id, file_name, image_filepath))
    cursor.execute("UPDATE files SET process = %s WHERE experiment_id = %s", ('yes', experiment_id))
    cursor.execute("UPDATE files SET file_meta = %s WHERE experiment_id = %s AND file_addr = %s",
                   (json_details, experiment_id, file_name))
    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Image reference saved to database:", image_filepath)

def execute_query(query):
    conn = psycopg2.connect(database="datacollection", user="new_user", host='134.197.75.35', password="1234", port=5432)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def combine_process():
    query = "SELECT study_id, experiment_id, file_addr, ex_type, phase_info, random_id,file_type FROM files WHERE process IS NULL"
    results = execute_query(query)

    if not results:
        print("⚠️ No unprocessed files found.")
        return

    try:
        random_id = results[0][5]
        upload_directory = os.path.join("imagesbulk", "randomId" + random_id)

        if not os.path.exists(upload_directory):
            os.makedirs(upload_directory)
    except Exception as e:
        print(f"❌ Failed to create upload directory: {e}")
        return

    for idx, result in enumerate(results):
        try:
            if len(result) < 6:
                print(f"⚠️ Skipping result at index {idx}: insufficient fields → {result}")
                continue

            study_id, experiment_id, file_addr, ex_type, phase_info, random_id, file_type = result
            base, _ = os.path.splitext(file_addr)
            file_name = base + ".jpg"
            full_file_path = os.path.join(upload_directory,str(file_type), file_name)

            # Ensure the file exists before processing
            if not os.path.isfile(full_file_path):
                print(f"⚠️ File not found: {full_file_path}")
                continue

            simple_experiment_2d(full_file_path, study_id, experiment_id, file_name, phase_info)

        except Exception as e:
            print(f"❌ Error processing file {result[2]}: {e}")


if __name__ == "__main__":
    combine_process()
