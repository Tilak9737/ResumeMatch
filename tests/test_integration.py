import pytest
import os
from src.analysis import analyze_resume_match
from src.parser import extract_text_from_pdf

def test_full_pipeline_with_dummy_pdf(tmp_path):
    # Create a dummy text file, then "parse" it by faking a PDF
    # Since we need a PDF, let's create a real minimal PDF if possible.
    # Actually, the parser uses PyMuPDF, let's just create a PDF using reportlab or PyMuPDF, or mock it.
    # We can just write a text file and mock the PDF extraction function, or generate a PDF using fpdf.
    pass

def test_full_pipeline_with_real_pdf_mocked(monkeypatch):
    from src.analysis import extract_text_from_pdf
    
    # Mock PDF extraction to return specific string and page count
    def mock_extract(path):
        return "Experience: Experienced with Python, PostgreSQL, AWS, and Docker. I have a lot of experience doing things. This is extra text to ensure the resume is long enough to pass validation.", 1
    
    monkeypatch.setattr('src.analysis.extract_text_from_pdf', mock_extract)
    monkeypatch.setattr('src.analysis.validate_pdf', lambda x: [])
    
    jd_text = """
    Required: Python, SQL.
    Preferred: Docker.
    This job requires a lot of things. Extra text here to ensure that the job description is long enough to pass the one hundred character validation limit that was set in day one.
    """
    
    res = analyze_resume_match("dummy.pdf", jd_text)
    
    # Check that all fields are populated and not None
    assert res.similarity_score is not None
    assert res.keyword_coverage is not None
    assert isinstance(res.resume_skills, list)
    assert isinstance(res.job_skills, list)
    assert isinstance(res.matched_skills, list)
    assert isinstance(res.missing_skills, list)
    assert isinstance(res.weak_evidence, list)
    assert isinstance(res.required_terms, list)
    assert isinstance(res.preferred_terms, list)
    assert res.required_term_coverage is not None
    assert isinstance(res.recommendations, list)
    assert res.provisional_score is not None
    
    # Specific assertions based on the text
    assert "Python" in res.resume_skills
    assert "PostgreSQL" in res.resume_skills
    assert "Docker" in res.resume_skills
    
    assert "Python" in res.required_terms
    assert "SQL" in res.required_terms
    assert "Docker" in res.preferred_terms
    
    assert "Python" in res.matched_skills
    assert "Docker" in res.matched_skills
    assert "SQL" in res.weak_evidence
