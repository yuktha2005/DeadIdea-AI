from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.gemini_agent import analyze_idea
from database.firestore import save_analysis, get_recent_analyses

app = FastAPI(title="DeadIdea AI API", description="Backend for resurrecting failed startups")

class IdeaRequest(BaseModel):
    idea_name: str
    api_key: str = None

@app.post("/analyze")
def analyze(request: IdeaRequest):
    if not request.idea_name:
        raise HTTPException(status_code=400, detail="Idea name is required")
        
    analysis_result = analyze_idea(request.idea_name, api_key=request.api_key)
    
    # Save to Firestore (works if Firestore is configured in the environment)
    # We catch exceptions in firestore.py so it won't crash if un-configured during local dev
    save_analysis(request.idea_name, analysis_result)
    
    return analysis_result

@app.get("/history")
def history():
    return {"history": get_recent_analyses()}
