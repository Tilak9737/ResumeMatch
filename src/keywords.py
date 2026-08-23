from sklearn.feature_extraction.text import TfidfVectorizer
from .config import NGRAM_RANGE, TOP_KEYWORDS

def extract_top_keywords(text: str, top_n: int = TOP_KEYWORDS) -> list[str]:
    """Extracts top n-grams from text using TF-IDF ranking."""
    if not text:
        return []
        
    vectorizer = TfidfVectorizer(
        stop_words='english', 
        ngram_range=NGRAM_RANGE,
        max_features=top_n
    )
    
    try:
        vectorizer.fit([text])
        if hasattr(vectorizer, 'get_feature_names_out'):
            return list(vectorizer.get_feature_names_out())
        else:
            return list(vectorizer.get_feature_names())
    except ValueError:
        return []
