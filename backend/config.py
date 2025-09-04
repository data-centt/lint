import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Load .env
load_dotenv()
