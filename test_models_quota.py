import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

load_dotenv(override=True)
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

models_to_test = [
    'gemini-2.0-flash-lite-001',
    'gemini-2.0-flash-lite',
    'gemini-2.0-flash',
    'gemini-flash-latest',
    'gemini-2.5-pro',
    'gemma-4-26b-a4b-it'
]

for model_name in models_to_test:
    model = genai.GenerativeModel(model_name)
    try:
        res = model.generate_content("Hello")
        print(f"SUCCESS with model: {model_name}")
        break
    except ResourceExhausted as e:
        print(f"RATE LIMITED: {model_name}")
    except Exception as e:
        print(f"ERROR on {model_name}: {str(e)}")
