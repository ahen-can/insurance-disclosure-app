# extractor.py
# import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from prompt import build_prompt
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

#genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#model = genai.GenerativeModel("gemini-2.5-flash")

def extract_from_pdf(pdf_bytes: bytes) -> dict:
    prompt = build_prompt()
    
    # response = model.generate_content([
    #     {"mime_type": "application/pdf", "data": pdf_bytes},
    #     prompt
    # ])
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf",
            ),
            prompt,
        ],
    )
    
    raw = response.text.strip()
    
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    
    return json.loads(raw)
