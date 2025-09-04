import pytest
from backend.generate_letter import generate_cover_letter

@pytest.mark.skip(reason="Integration test - requires OpenAI API key")
def test_generate_cover_letter_real():
    job_desc = "We are hiring a Python developer."
    resume_text = "Experienced Python developer with Flask and Firebase."
    letter = generate_cover_letter(job_desc, resume_text)
    assert isinstance(letter, str)
    assert "Python" in letter or "developer" in letter