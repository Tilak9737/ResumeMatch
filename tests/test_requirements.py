import pytest
from src.requirements import extract_requirement_sentences, get_required_preferred_terms

@pytest.fixture
def dummy_skills_dict():
    return {
        "python": {"canonical": "Python", "aliases": ["python"]},
        "sql": {"canonical": "SQL", "aliases": ["sql"]},
        "postgresql": {"canonical": "PostgreSQL", "aliases": ["postgresql"]},
        "aws": {"canonical": "AWS", "aliases": ["aws"]},
        "docker": {"canonical": "Docker", "aliases": ["docker"]},
        "spark": {"canonical": "Spark", "aliases": ["spark"]}
    }

def test_extract_requirement_sentences():
    text = """
    We are looking for a great developer.
    
    Required:
    - Python
    - SQL
    - PostgreSQL
    
    Preferred:
    - AWS
    - Docker
    
    Nice to have: Spark.
    """
    
    sentences_map = extract_requirement_sentences(text)
    
    req_text = " ".join(sentences_map["required"]).lower()
    pref_text = " ".join(sentences_map["preferred"]).lower()
    
    assert "python" in req_text
    assert "postgresql" in req_text
    assert "aws" not in req_text # Should not be in required
    
    assert "aws" in pref_text
    assert "docker" in pref_text
    assert "spark" in pref_text

def test_get_required_preferred_terms(dummy_skills_dict):
    text = """
    Minimum qualifications: Python and SQL.
    Bonus: AWS and Docker.
    """
    result = get_required_preferred_terms(text, dummy_skills_dict)
    
    assert "Python" in result["required_terms"]
    assert "SQL" in result["required_terms"]
    
    assert "AWS" in result["preferred_terms"]
    assert "Docker" in result["preferred_terms"]
    
    assert "Spark" not in result["required_terms"]
    assert "Spark" not in result["preferred_terms"]

def test_adversarial_requirements():
    text1 = "Required: Python. Preferred: AWS."
    res1 = extract_requirement_sentences(text1)
    assert any('Python' in s for s in res1['required'])
    assert not any('AWS' in s for s in res1['required'])
    assert any('AWS' in s for s in res1['preferred'])

    text2 = "Python is required. AWS is preferred."
    res2 = extract_requirement_sentences(text2)
    assert any('Python' in s for s in res2['required'])
    assert any('AWS' in s for s in res2['preferred'])
    
    text3 = """Requirements:
- Python
- SQL
- PostgreSQL

Preferred:
- AWS
- Docker"""
    res3 = extract_requirement_sentences(text3)
    req_text = ' '.join(res3['required'])
    pref_text = ' '.join(res3['preferred'])
    assert 'Python' in req_text
    assert 'PostgreSQL' in req_text
    assert 'AWS' in pref_text
    assert 'Docker' in pref_text
    assert 'AWS' not in req_text
    assert 'Python' not in pref_text

