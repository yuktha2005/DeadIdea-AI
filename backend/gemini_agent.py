import os
import json
import time
import google.generativeai as genai

# Setup API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_idea(idea_name: str, api_key: str = None) -> dict:
    # Use the provided key from UI or fall back to environment variable
    active_key = api_key or GEMINI_API_KEY
    
    if not active_key:
        return {
            "error": "MISSING_API_KEY",
            "Idea Summary": "API Key not found.",
            "Failure Analysis": "Please set the GEMINI_API_KEY environment variable or provide it in the sidebar.",
            "What Has Changed Today": "N/A",
            "Revived Startup Concept": "N/A",
            "Revival Potential Score": 0,
            "Visual Concept Prompt": "A warning sign, digital glitch aesthetic."
        }
    
    # Configure on the fly if a new key is provided
    try:
        genai.configure(api_key=active_key)
        
        # Tiered model list for maximum resilience
        models_to_try = [
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-2.0-flash',
            'gemini-pro-latest',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        
        last_error = None
        for model_name in models_to_try:
            print(f"[AI AGENT] Attempting analysis with model: {model_name}")
            try:
                # Add a micro-delay only if we ran into a previous error to respect local rate limits
                if last_error:
                    time.sleep(1.5)
                
                model = genai.GenerativeModel(model_name)
                
                # Load prompt template
                prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "analysis_prompt.txt")
                if not os.path.exists(prompt_path):
                     return {"error": "PROMPT_NOT_FOUND", "Failure Analysis": "Analysis prompt file missing."}

                with open(prompt_path, "r", encoding="utf-8") as f:
                    prompt_template = f.read()
                    
                prompt = prompt_template.format(idea=idea_name)
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json"
                    )
                )
                result = json.loads(response.text)
                
                # Ensure result is a dictionary to prevent 'list' object errors in UI
                if isinstance(result, list) and len(result) > 0:
                    result = result[0]
                
                if not isinstance(result, dict):
                    result = {"Idea Summary": str(result)}
                
                # Ensure expected keys exist
                for key in ["Idea Summary", "Failure Analysis", "What Has Changed Today", "Revived Startup Concept"]:
                    if key not in result:
                        result[key] = "N/A"
                if "Revival Potential Score" not in result:
                    result["Revival Potential Score"] = 50
                if "Visual Concept Prompt" not in result:
                    result["Visual Concept Prompt"] = f"A futuristic concept of {idea_name}"
                if "Market Metrics" not in result:
                    result["Market Metrics"] = {
                        "Innovation": 70, "Scalability": 60, "Feasibility": 50, "Market Fit": 65, "Competitive Edge": 55
                    }
                    
                return result
            except Exception as e:
                last_error = e
                print(f"Failed with {model_name}, trying next... Error: {e}")
                continue
                
        # If we get here, all models failed
        raise last_error or Exception("All models failed")
        
    except Exception as e:
        print(f"Error communicating with Gemini: {e}")
        # Return a more descriptive object with a non-zero default score to avoid 0% confusion
        # unless it's a critical failure.
        return {
            "Idea Summary": "System in standby or quota reached.",
            "Failure Analysis": f"The Neural Link reported an issue: {e}",
            "What Has Changed Today": "Market data currently being cached.",
            "Revived Startup Concept": "Please attempt a re-scan in 60 seconds.",
            "Revival Potential Score": 50, 
            "Visual Concept Prompt": "A digital phoenix rising from glitchy code.",
            "Market Metrics": {
                "Innovation": 50, "Scalability": 50, "Feasibility": 50, "Market Fit": 50, "Competitive Edge": 50
            }
        }
