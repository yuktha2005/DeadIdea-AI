import subprocess
import sys
import os
import time

def main():
    port = os.environ.get("PORT", "8080")
    
    print("[SYSTEM] Starting FastAPI Backend on port 8000...")
    backend_cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
    backend = subprocess.Popen(backend_cmd)
    
    # Give the backend a moment to start before launching frontend
    time.sleep(2) 
    
    print(f"[SYSTEM] Starting Streamlit Frontend on port {port}...")
    frontend_cmd = [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", port, "--server.address", "0.0.0.0"]
    frontend = subprocess.Popen(frontend_cmd)
    
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down services...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("[SYSTEM] Successfully cleanly shut down.")

if __name__ == "__main__":
    main()
