# yuka-ak

## Purpose

This project goes beyond creating meal plan(s) based on what is in my refrigerator to what is in my blood test report and what am I eating. This project:

- uses Tesseract ocr https://tesseract-ocr.github.io/ to convert scanned images to .txt file(s)
 
- uses deepseek-v4-pro model to refine the tesseract ocr output & using the same model provides insights on nutrition (along with a disclaimer)

- IS ONLY FOR DEMO/LEARNING PURPOSE

## Getting Started

1. Install Tesseract on the system

```bash
sudo apt install tesseract-ocr -y 
sudo apt install libtesseract-dev -y
#Test
/usr/bin/tesseract
```

1. Install Python & required packages

```bash
sudo apt-get update
sudo apt install python3-pip -y
pip install pytesseract
pip install dotenv openai
```

1. `recognize.py` transforms the grocery receipt(s) and blood test report(s) to .txt file(s) using tesseract ocr.

1. `extract.py` sends the .txt file(s) generated previously to `deepseek-v4-pro` & formats the .txt file(s) 

1. `recommend.py` sends a merged .txt file with both blood report and food items to `deepseek-v4-pro` & gets recommendation on nutrition (along with a disclaimer)

1. Sample grocery receipt(s) and blood test report(s) images with no personal data are available under `images` folder

1. Outputs from various steps above are available under `outputs` folder