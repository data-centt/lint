import os
from dotenv import load_dotenv
from openai import OpenAI

"""
generate_letter.py

This file handles the cover letter generation using the uploaded resume on user's account.
"""

load_dotenv
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o"

def generate_cover_letter(job_description:str, resume_text:str, model:str = MODEL) -> str:
    """
    Generate a tailored cover letter using job description and resume text.
    """
    if not job_description.strip():
        raise ValueError("Job description cannot be empty")
    