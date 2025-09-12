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