import os
import uuid
from typing import Optional, Dict
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from firebase_admin import firestore
from google.cloud.exceptions import GoogleCloudError
from config import db, bucket


"""
This file handles the imports and outputs of the files and automatically pick the most recent file
upload.
"""

def _parse_pdf(path: str) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        try:
            t = page.extract_text() or ""
            if t.strip():
                texts.append(t)
        except Exception:
            # Skip unreadable pages but continue
            continue
    return "\n".join(texts).strip()

def _parse_docx(path: str) -> str:
    """Extract text from a DOCX file."""
    doc = DocxDocument(path)
    return "\n".join(p.text for p in doc.paragraphs).strip()

def parse_resume(local_path: str) -> str:
    """
    Parse a resume file (.pdf or .docx) and return extracted text.
    Raises ValueError for unsupported types.
    """
    ext = os.path.splitext(local_path)[1].lower()
    if ext == ".pdf":
        return _parse_pdf(local_path)
    if ext == ".docx":
        return _parse_docx(local_path)
    raise ValueError("Unsupported file type. Please upload .pdf or .docx")

def upload_resume_file(local_path: str, user_id: str) -> Dict:
    """
    Upload the original resume to Firebase Storage,
    parse text, and save metadata + parsed text in Firestore.

    Returns a dict containing the Firestore document fields plus 'id'.
    """
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"File not found: {local_path}")
    file_name = f"{uuid.uuid4().hex}_{os.path.basename(local_path)}"

    # Path in your bucket (organize per-user)
    blob = bucket.blob(f"resumes/{user_id}/{file_name}")
    try:
        blob.upload_from_filename(local_path)
        # make public for now
        blob.make_public()
    except GoogleCloudError as e:
        raise RuntimeError(f"Upload to Storage failed: {e}")
    
    parsed_text = parse_resume(local_path)

    # Write Firestore doc with metadata + parsed text
    doc_ref = db.collection("resumes").add({
        "user_id": user_id,
        "file_name": file_name,
        "download_url": blob.public_url,   # consider signed URLs in production
        "parsed_text": parsed_text,
        "created_at": firestore.SERVER_TIMESTAMP,
    })
    
    snap = doc_ref[1].get()
    data = snap.to_dict() or {}
    data["id"] = snap.id
    return data

def get_latest_resume(user_id: str) -> Optional[Dict]:
    """
    Fetch the most recently uploaded resume document for a given user.
    Returns None if the user has no resumes.
    """
    q = (
        db.collection("resumes")
          .where("user_id", "==", user_id)
          .order_by("created_at", direction=firestore.Query.DESCENDING)
          .limit(1)
    )

    docs = list(q.stream())
    if not docs:
        return None
    
    d = docs[0]
    