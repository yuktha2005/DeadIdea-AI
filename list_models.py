import os
import google.generativeai as genai

genai.configure(api_key='AIzaSyA4E2yPlPCvnH-HwsVBzEbSMG9ysvDAo0c')

try:
    models = genai.list_models()
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")
except Exception as e:
    print(f"Error: {e}")
