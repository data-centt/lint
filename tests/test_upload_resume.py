from backend.upload_resume import parse_resume
import tempfile, os

def test_parse_docx(tmp_path):
    file_path = tmp_path / "resume.docx"
    file_path.write_text("Hello\nWorld")
    text = parse_resume(str(file_path))
    assert "Hello" in text or "World" in text