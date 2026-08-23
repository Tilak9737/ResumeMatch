import os
import pytest
from src.validation import validate_pdf, validate_texts

def test_validate_pdf_not_found():
    errors = validate_pdf("nonexistent.pdf")
    assert any("File not found" in e for e in errors)

def test_validate_pdf_wrong_extension():
    # create a dummy txt file
    with open("dummy.txt", "w") as f:
        f.write("text")
    errors = validate_pdf("dummy.txt")
    assert any("must be a PDF" in e for e in errors)
    os.remove("dummy.txt")

def test_validate_pdf_valid():
    errors = validate_pdf("tests/fixtures/valid_resume.pdf")
    assert not errors

def test_validate_texts_empty_resume():
    errors = validate_texts("", "some valid job description here"*10)
    assert any("Resume text is empty or too short" in e for e in errors)

def test_validate_texts_empty_jd():
    errors = validate_texts("some valid resume text here"*10, "")
    assert any("Job description text is empty or too short" in e for e in errors)

def test_validate_texts_valid():
    errors = validate_texts("valid resume text here"*10, "valid job description text here"*10)
    assert not errors
