import pdfplumber
from .logging_config import logger

def extract_text_from_pdf(file_path: str) -> tuple[str, int]:
    """Extracts text from a given PDF file and returns (text, page_count)."""
    logger.info(f"PDF extraction started for {file_path}")
    text_content = []
    
    try:
        with pdfplumber.open(file_path) as pdf:
            page_count = len(pdf.pages)
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content.append(extracted)
                    
        full_text = "\n".join(text_content)
        logger.info(f"PDF extraction completed. Characters extracted: {len(full_text)}, Pages: {page_count}")
        return full_text, page_count
        
    except Exception as e:
        logger.error(f"PDF extraction failed: {str(e)}")
        raise
