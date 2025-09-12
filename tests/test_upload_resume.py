import os
import pytest
from backend.upload_resume import parse_resume

def test_parse_unsupported(tmp_path):
    p = tmp_path / "resume.txt"
    p.write_text("hello")
    with pytest.raises(ValueError):
        parse_resume(str(p))