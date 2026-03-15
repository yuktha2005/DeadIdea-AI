import os
from google.cloud import firestore

def get_db():
    try:
        # Client gracefully falls back to default credentials (e.g. on Cloud Run)
        # If running locally without credentials, this might raise an exception
        db = firestore.Client()
        return db
    except Exception as e:
        print(f"Firestore not initialized (normal if credentials missing locally): {e}")
        return None

def save_analysis(idea_name: str, analysis_data: dict):
    db = get_db()
    if db:
        try:
            doc_ref = db.collection('idea_analyses').document()
            data = {"original_idea": idea_name}
            data.update(analysis_data)
            doc_ref.set(data)
            return doc_ref.id
        except Exception as e:
            print(f"Error saving to Firestore: {e}")
    return None

def get_recent_analyses(limit=10):
    db = get_db()
    if db:
        try:
            docs = db.collection('idea_analyses').limit(limit).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"Error reading from Firestore: {e}")
    return []
