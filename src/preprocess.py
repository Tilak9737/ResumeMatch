import re

def clean_text(text: str) -> str:
    """Cleans and normalizes text for NLP processing."""
    if not text:
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Remove punctuation and non-alphanumeric characters EXCEPT specific ones (+, #, ., /, -)
    # This preserves terms like C++, C#, .NET, Node.js, CI/CD
    text = re.sub(r'[^a-z0-9\s\+\#\.\/\-]', ' ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
