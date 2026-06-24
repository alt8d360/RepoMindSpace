import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

try:
    for i in range(25):
        print(f"Request {i}")
        res = model.generate_content("Hello")
except Exception as e:
    print(f"EXCEPTION TYPE: {type(e).__name__}")
    print(f"EXCEPTION MODULE: {type(e).__module__}")
    print(f"EXCEPTION: {str(e)}")
