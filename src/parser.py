import pdfplumber
from .logging_config import logger

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a given PDF file."""
    logger.info(f"PDF extraction started for {file_path}")
    text_content = []
    
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content.append(extracted)
                    
        full_text = "\n".join(text_content)
        logger.info(f"PDF extraction completed. Characters extracted: {len(full_text)}")
        return full_text
        
    except Exception as e:
        logger.error(f"PDF extraction failed: {str(e)}")
        raise
