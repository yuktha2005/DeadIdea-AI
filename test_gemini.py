import os
import google.generativeai as genai
import json

genai.configure(api_key='AIzaSyA4E2yPlPCvnH-HwsVBzEbSMG9ysvDAo0c')

models_to_test = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-2.0-flash', 'gemini-1.5-pro']

for m in models_to_test:
    print(f"Testing model: {m}...")
    try:
        model = genai.GenerativeModel(m)
        response = model.generate_content("Hello, who are you? Respond in JSON format with a 'name' field.", 
                                         generation_config=genai.GenerationConfig(response_mime_type="application/json"))
        print(f"SUCCESS with {m}: {response.text}")
        break
    except Exception as e:
        print(f"FAILED with {m}: {e}")
