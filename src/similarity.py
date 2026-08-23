from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(resume_text: str, jd_text: str) -> float:
    """Calculates cosine similarity between resume and job description."""
    if not resume_text or not jd_text:
        return 0.0
        
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        # Normalize to 0-100 scale
        return float(similarity * 100)
    except ValueError:
        # Happens if vocab is empty (e.g. only stop words)
        return 0.0
