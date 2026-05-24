#Parse text files using AI & load to DuckDB 
import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import requests



#Load .env
load_dotenv()
api_key=os.getenv("DEEPSEEK_API_KEY")

# Directories
groceries_dir_txt=Path(r"/home/arkaul/yuka-ak/work/groceries_txt")
medicalreports_dir_txt=Path(r"/home/arkaul/yuka-ak/work/medicalreports_txt")



# Define System & User Prompts
SYSTEM_PROMPT = """You are a helpful assistant that extracts and structures information from documents.
"""
    
USER_PROMPT = """Please analyze the following document and extract the list of items. Please 
ignore everything else and return you response in a tabular format."""


# Function to iterate over .txt file(s) & call AI
def processfolder(folder_path):

    processed_count = 0
    error_count = 0

    for fileToProcess in folder_path.iterdir():
        print(f"Processing: {fileToProcess.name}")
        try:
            with open(fileToProcess, "r", encoding="utf-8") as f:
                content=f.read()
            processed_count += 1
    
        except Exception as e:
            print(f"Error : {e}")
            error_count += 1
        
        api_result = call_ai_with_prompts(folder_path,fileToProcess,content, SYSTEM_PROMPT, USER_PROMPT, api_key)
    
    print(f"Successfully processed: {processed_count} files")
    print(f"Errors: {error_count} files")



def call_ai_with_prompts(folder_path:str, fileToProcess:str, content: str, system_prompt: str, user_prompt: str, api_key: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Combine user prompt with the actual content
    full_user_prompt = f"{user_prompt}\n\n--- Document Content ---\n{content}\n--- End of Document ---"
    payload = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_user_prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # Extract the response content
        response_content = result["choices"][0]["message"]["content"]
        
        # Print it
        # print(response_content)
        
        # Write to file
        output_file = folder_path / f"{fileToProcess.name}_ai_response.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response_content)
        
        return {
            "success": True,
            "response": response_content,
            "usage": result["usage"]
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            "success": False,
            "response": None,
            "error": str(e)
        }


processfolder(groceries_dir_txt)
processfolder(medicalreports_dir_txt)