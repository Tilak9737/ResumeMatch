from src.keywords import extract_top_keywords

def test_extract_top_keywords():
    text = "python programming python is good for data science data science"
    keywords = extract_top_keywords(text, top_n=5)
    assert any("data science" in kw or "python" in kw for kw in keywords)

def test_extract_top_keywords_empty():
    assert extract_top_keywords("") == []
