FROM python:3.11-slim

WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose ports for Cloud Run (Cloud Run sets PORT env var)
# We will use the PORT provided by Cloud Run for Streamlit, and run FastAPI on 8000 internally.
EXPOSE $PORT

# Start both services using the universal Python runner
CMD ["python", "run_all.py"]
