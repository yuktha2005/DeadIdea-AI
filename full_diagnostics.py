import os
import google.generativeai as genai

# Use the key provided by the user
genai.configure(api_key='AIzaSyA4E2yPlPCvnH-HwsVBzEbSMG9ysvDAo0c')

models_to_test = [
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-2.0-flash-exp',
    'gemini-1.5-flash-8b'
]

print("Starting diagnostics...")
for m in models_to_test:
    print(f"\n--- Testing Model: {m} ---")
    try:
        model = genai.GenerativeModel(m)
        response = model.generate_content("test")
        print(f"SUCCESS: {m}")
    except Exception as e:
        print(f"ERROR with {m}: {e}")

print("\n--- Listing all available models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Available Model: {m.name}")
except Exception as e:
    print(f"LIST_MODELS ERROR: {e}")
