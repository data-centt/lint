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

