import os
import shutil

original_folder_path = (
    r"C:\SMU-SCIS-Project\what makes a hugging face model popular\5 May new "
    r"collection of data\03 - readme collection\readmes"
)
target_folder_path = (
    r"C:\SMU-SCIS-Project\what makes a hugging face model popular\5 May new "
    r"collection of data\03 - readme collection\format-readmes"
)

if not os.path.exists(target_folder_path):
    os.makedirs(target_folder_path)

for filename in os.listdir(original_folder_path):
    if '_README' in filename:
        new_filename = filename.replace('_README', '')
        original_file_path = os.path.join(original_folder_path, filename)
        new_file_path = os.path.join(target_folder_path, new_filename)
        shutil.move(original_file_path, new_file_path)

print("All files have been renamed and moved to the new directory.")
