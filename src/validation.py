import os
from .config import MAX_PDF_SIZE_MB, MIN_JD_LENGTH, MIN_RESUME_LENGTH
from .logging_config import logger

def validate_pdf(file_path: str) -> list[str]:
    errors = []
    if not os.path.exists(file_path):
        errors.append(f"File not found: {file_path}")
        return errors
        
    if not file_path.lower().endswith(".pdf"):
        errors.append("File must be a PDF.")
        
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_PDF_SIZE_MB:
        errors.append(f"File size ({size_mb:.2f} MB) exceeds maximum allowed ({MAX_PDF_SIZE_MB} MB).")
        
    return errors

def validate_texts(resume_text: str, jd_text: str) -> list[str]:
    errors = []
    if not resume_text or len(resume_text.strip()) < MIN_RESUME_LENGTH:
        errors.append("Resume text is empty or too short. Check if the PDF is scanned or malformed.")
    if not jd_text or len(jd_text.strip()) < MIN_JD_LENGTH:
        errors.append("Job description text is empty or too short.")
    return errors
