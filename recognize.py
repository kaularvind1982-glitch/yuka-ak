# OCR using tesseract
from PIL import Image
from pathlib import Path
import os
#Import Tesseract & set path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Directories
groceries_dir=Path(r"/home/arkaul/yuka-ak/images/groceries")
groceries_dir_txt=Path(r"/home/arkaul/yuka-ak/work/groceries_txt")
medicalreports_dir=Path(r"/home/arkaul/yuka-ak/images/medicalreports")
medicalreports_dir_txt=Path(r"/home/arkaul/yuka-ak/work/medicalreports_txt")


# Generic function for Tesseract invocation
def ocr_file(file_path):
    file_text=pytesseract.image_to_string(Image.open(file_path))
    return file_text


# Function to iterate over a folder & convert images to .txt file

def processfolder(source_folder_path,target_folder_path):

    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    processed_count = 0
    error_count = 0

    for srcfile in source_folder_path.iterdir():
        if not srcfile.is_file():
            continue
        print(f"Processing: {srcfile.name}")
        try:
            srcfile_text = ocr_file(srcfile)
            target_file = target_folder_path / f"{srcfile.name}_output.txt"
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(srcfile_text)
            processed_count += 1
    
        except Exception as e:
            print(f"Error : {e}")
            error_count += 1
    
    print(f"Successfully processed: {processed_count} files")
    print(f"Errors: {error_count} files")



processfolder(groceries_dir,groceries_dir_txt)
processfolder(medicalreports_dir,medicalreports_dir_txt)