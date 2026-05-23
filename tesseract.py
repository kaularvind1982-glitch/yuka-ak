from PIL import Image
from pathlib import Path

#Import Tesseract & set path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Directories
groceries_dir=Path(r"/home/arkaul/tesseract-ocr/images/groceries")
groceries_dir_txt=Path(r"/home/arkaul/tesseract-ocr/work/groceries_txt")
medicalreports_dir=Path(r"/home/arkaul/tesseract-ocr/images/medicalreports")
medicalreports_dir_txt=Path(r"/home/arkaul/tesseract-ocr/work/medicalreports_txt")


# Generic function for Tesseract invocation
def ocr_file(file_path):
    file_text=pytesseract.image_to_string(Image.open(file_path))
    return file_text


# Process images & write a .txt file
for grocery_file in groceries_dir.iterdir():
    if not grocery_file.is_file():
        continue
    print(f"Processing: {grocery_file.name}")
    try:
        grocery_text = ocr_file(grocery_file)
        grocery_text_file = groceries_dir_txt / f"{grocery_file.name}_output.txt"
        with open(grocery_text_file, "w", encoding="utf-8") as f:
            f.write(grocery_text)
    
    except Exception as e:
        print(f"Error : {e}")
    
    print("Done.")


# GPT Key
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