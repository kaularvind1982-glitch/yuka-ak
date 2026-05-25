#Get recommendations using AI 
import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import requests



#Load .env
load_dotenv()
api_key=os.getenv("DEEPSEEK_API_KEY")

USER_PROMPT = """Act as both a general physician and a registered dietitian. 
First, as the physician,review the blood report content from #Blood Report Start# to #Blood Report End# and identify abnormalities
Then, as the dietitian, review the food items content from #Food Items Start# to #Food Items End# and recommend specific dietary changes to address those abnormalities.
Only cite government sources from UK, France & Singapore to back your recommendation
Include a disclaimer that you are neither a real doctor nor a real dietitian and just a helpful assistant
"""

def call_ai_with_prompts(fileToProcess:str, content: str, user_prompt: str, api_key: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Combine user prompt with the actual content
    full_user_prompt = f"{user_prompt}\n\n--- Document Content ---\n{content}\n--- End of Document ---"
    payload = {
        "model": "deepseek-v4-pro",
        "messages": [
            {"role": "user", "content": full_user_prompt}
        ],
        "temperature": 0.2
    }
    
    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # Extract the response content
        response_content = result["choices"][0]["message"]["content"]
        

        
        #Write to file
        output_file = f"{fileToProcess.name}_ai_recommendation.txt"
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

fileToProcess=Path("/home/arkaul/yuka-ak/work/groceries_medicalreports.txt")
print(fileToProcess.name)
with open(fileToProcess, "r", encoding="utf-8") as f:
    content=f.read()
call_ai_with_prompts(fileToProcess, content, USER_PROMPT, api_key)