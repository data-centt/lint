import os
from dotenv import load_dotenv
from openai import OpenAI

"""
generate_letter.py

This file handles the cover letter generation using the uploaded resume on user's account.
"""

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o"

def generate_cover_letter(job_description:str, resume_text:str, model:str = MODEL) -> str:
    """
    Generate a tailored cover letter using job description and resume text.
    """
    if not job_description.strip():
        raise ValueError("Job description cannot be empty")
    
    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty")
    
    prompt = f"""
    You are a professional career assistant. Write a concise, tailored cover letter
    based on the following job description and candidate resume.

    Job Description:
    {job_description}

    Candidate Resume:
    {resume_text}

    Guidelines:
    (i)  Write 3 short paragraphs: introduction, alignment with each essential criteria, closing.
    (ii) If there is no criteria, focus on how the resume fits the job.
    (iii) Confident and clear tone
    (iv) Do not fabricate experience
    (v) Return plain text only
    """
    response = client.chat.completions.create(
        model= model,
        messages=[{"role":"user", "content":prompt}],
        temperature=0.4
    )
    
    return response.choices[0].message.content.strip()

