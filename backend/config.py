import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, storage


load_dotenv()

FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS", "firebase_key.json")
FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")

if not FIREBASE_STORAGE_BUCKET:
    raise RuntimeError("Missing FIREBASE_STORAGE_BUCKET in .env")

if not os.path.exists(FIREBASE_CREDENTIALS):
    raise RuntimeError(f"Service account file not found: {FIREBASE_CREDENTIALS}")

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred, {"storageBucket": FIREBASE_STORAGE_BUCKET})

db = firestore.client()
bucket = storage.bucket()
