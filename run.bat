@echo off
echo Starting DeadIdea AI Backend...
start "FastAPI Backend" cmd /c "uvicorn backend.main:app --port 8000 --reload"

echo Starting DeadIdea AI Frontend...
start "Streamlit Frontend" cmd /c "streamlit run frontend/app.py"

echo Both services have been started in separate windows!
