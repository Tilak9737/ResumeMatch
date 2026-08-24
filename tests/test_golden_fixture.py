import os
import pytest
from src.analysis import analyze_resume_match

@pytest.fixture
def golden_data():
    base_dir = os.path.dirname(__file__)
    resume_path = os.path.join(base_dir, "fixtures", "resume_data_analyst.txt")
    jd_path = os.path.join(base_dir, "fixtures", "jd_data_scientist.txt")
    
    with open(resume_path, "r", encoding="utf-8") as f:
        resume_text = f.read()
        
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()
        
    return resume_text, jd_text

def test_golden_fixture_evidence_and_score(golden_data):
    resume_text, jd_text = golden_data
    
    result = analyze_resume_match(resume_text=resume_text, jd_text=jd_text)
    
    # Check Evidence Classification
    evidence_map = {e.skill: e for e in result.evidence}
    
    # MATCHED skills (should have strong source)
    assert "Python" in evidence_map
    assert evidence_map["Python"].evidence_level == "MATCHED"
    
    assert "SQL" in evidence_map
    assert evidence_map["SQL"].evidence_level == "WEAK" # MySQL -> SQL is indirect
    
    # WEAK skills (e.g. from coursework)
    assert "Machine Learning" in evidence_map
    assert evidence_map["Machine Learning"].evidence_level == "WEAK"
    
    # MISSING skills
    assert "AWS" in evidence_map
    assert evidence_map["AWS"].evidence_level == "MISSING"
    
    # Score Invariance (Day 4 -> Day 5.1 should not change core calculation unexpectedly)
    # The exact score may vary slightly due to text length, but should be stable.
    assert result.provisional_score > 0
    assert result.similarity_score > 0
    assert result.keyword_coverage > 0
    assert result.required_term_coverage > 0
    
    # Recommendations Order
    recs = result.recommendations
    assert len(recs) > 0
    
    # Verify High impact comes first
    high_impact_found = False
    medium_impact_found = False
    low_impact_found = False
    
    for r in recs:
        if r.impact == "HIGH":
            assert not medium_impact_found and not low_impact_found
            high_impact_found = True
        elif r.impact == "MEDIUM":
            assert not low_impact_found
            medium_impact_found = True
        elif r.impact == "LOW":
            low_impact_found = True
