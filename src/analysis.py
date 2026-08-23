import os
from .models import AnalysisResult
from .validation import validate_pdf, validate_texts
from .parser import extract_text_from_pdf
from .preprocess import clean_text
from .similarity import calculate_cosine_similarity
from .keywords import extract_top_keywords
from .scoring import calculate_similarity_score, calculate_match_score
from .skills import load_skills_dict, extract_skills
from .requirements import get_required_preferred_terms
from .recommendations import generate_recommendations
from .logging_config import logger

def analyze_resume_match(resume_pdf_path: str, jd_text: str) -> AnalysisResult:
    logger.info("Starting analysis flow")
    
    # 1. Validate PDF
    pdf_errors = validate_pdf(resume_pdf_path)
    if pdf_errors:
        return AnalysisResult(similarity_score=0.0, resume_text_length=0, job_text_length=0, errors=pdf_errors)
        
    # 2. Extract Text
    try:
        resume_raw = extract_text_from_pdf(resume_pdf_path)
    except Exception as e:
        return AnalysisResult(similarity_score=0.0, resume_text_length=0, job_text_length=0, errors=[f"PDF Extraction failed: {str(e)}"])
        
    # 3. Validate Texts
    text_errors = validate_texts(resume_raw, jd_text)
    if text_errors:
        return AnalysisResult(
            similarity_score=0.0,
            resume_text_length=len(resume_raw) if resume_raw else 0,
            job_text_length=len(jd_text) if jd_text else 0,
            errors=text_errors
        )
        
    # 4. Preprocess
    resume_clean = clean_text(resume_raw)
    job_clean = clean_text(jd_text)
    
    # 5. Math & Similarity
    similarity = calculate_cosine_similarity(resume_clean, job_clean)
    
    # 6. Keywords
    resume_keywords = extract_top_keywords(resume_clean)
    job_keywords = extract_top_keywords(job_clean)
    
    matched_kws = list(set(resume_keywords) & set(job_keywords))
    missing_kws = list(set(job_keywords) - set(resume_keywords))
    keyword_cov = (len(matched_kws) / len(job_keywords) * 100) if job_keywords else 100.0
    
    # 7. Day 3: NLP Intelligence (Skills & Requirements)
    try:
        skills_dict = load_skills_dict()
    except FileNotFoundError:
        skills_dict = {}
        logger.warning("skills.json not found, skill matching will be empty.")
        
    resume_skills = extract_skills(resume_clean, skills_dict)
    job_skills = extract_skills(job_clean, skills_dict)
    
    req_pref = get_required_preferred_terms(jd_text, skills_dict) # Passing raw jd_text for sentence splitting
    req_terms = req_pref["required_terms"]
    pref_terms = req_pref["preferred_terms"]
    
    recs_output = generate_recommendations(resume_skills, req_terms, pref_terms, skills_dict)
    
    # Calculate coverage
    skills_cov = (len(recs_output["matched_skills"]) / len(job_skills) * 100) if job_skills else 100.0
    
    matched_req = [s for s in req_terms if s in resume_skills]
    req_cov = (len(matched_req) / len(req_terms) * 100) if req_terms else 100.0
    
    # Calculate provisional score
    prov_score = calculate_match_score(
        similarity=similarity,
        keyword_coverage=keyword_cov,
        skills_overlap=skills_cov,
        required_term_coverage=req_cov
    )
    
    logger.info("Analysis flow completed successfully")
    return AnalysisResult(
        similarity_score=similarity, # Still returning raw similarity for reference
        resume_text_length=len(resume_raw),
        job_text_length=len(jd_text),
        keywords=job_keywords,
        matched_keywords=matched_kws,
        missing_keywords=missing_kws,
        keyword_coverage=keyword_cov,
        
        provisional_score=prov_score,
        resume_skills=resume_skills,
        job_skills=job_skills,
        matched_skills=recs_output["matched_skills"],
        missing_skills=recs_output["missing_skills"],
        weak_evidence=recs_output["weak_evidence"],
        required_terms=req_terms,
        preferred_terms=pref_terms,
        required_term_coverage=req_cov,
        recommendations=recs_output["recommendations"]
    )
