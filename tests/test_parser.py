import pytest
from src.parser import extract_text_from_pdf

def test_extract_valid_pdf():
    text, pages = extract_text_from_pdf("tests/fixtures/valid_resume.pdf")
    assert "Hello" in text
    assert pages >= 1

def test_extract_malformed_pdf():
    # pdfplumber should raise an exception on a text file
    with pytest.raises(Exception):
        extract_text_from_pdf("tests/fixtures/malformed.pdf")

def test_extract_empty_pdf():
    # Empty file might raise an exception in pdfplumber
    with pytest.raises(Exception):
        extract_text_from_pdf("tests/fixtures/empty.pdf")
