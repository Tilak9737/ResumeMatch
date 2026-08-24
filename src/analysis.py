import os
import time
from .models import AnalysisResult
from .validation import validate_pdf, validate_texts
from .parser import extract_text_from_pdf
from .preprocess import clean_text
from .keywords import extract_top_keywords
from .similarity import calculate_cosine_similarity
from .skills import load_skills_dict, extract_skills_with_evidence
from .requirements import get_required_preferred_terms
from .recommendations import generate_evidence_and_recommendations
from .scoring import calculate_match_score
from .logging_config import logger
from .analytics import log_analysis_started, log_analysis_completed, log_analysis_failed

def analyze_resume_match(resume_pdf_path: str = None, jd_text: str = "", resume_text: str = None) -> AnalysisResult:
    logger.info("Starting analysis flow")
    log_analysis_started()
    start_time = time.time()
    
    if resume_text is not None:
        resume_raw = resume_text
        resume_page_count = 1
    else:
        # 1. Validate PDF
        pdf_errors = validate_pdf(resume_pdf_path)
        if pdf_errors:
            log_analysis_failed("validation")
            return AnalysisResult(similarity_score=0.0, resume_text_length=0, job_text_length=0, errors=pdf_errors)
            
        # 2. Extract Text
        try:
            resume_raw, resume_page_count = extract_text_from_pdf(resume_pdf_path)
        except Exception as e:
            log_analysis_failed("parsing")
            return AnalysisResult(similarity_score=0.0, resume_text_length=0, job_text_length=0, errors=[f"PDF Extraction failed: {str(e)}"])
        
    # 3. Validate Texts
    text_errors = validate_texts(resume_raw, jd_text)
    if text_errors:
        log_analysis_failed("validation")
        return AnalysisResult(
            similarity_score=0.0,
            resume_text_length=len(resume_raw) if resume_raw else 0,
            job_text_length=len(jd_text) if jd_text else 0,
            resume_page_count=resume_page_count if 'resume_page_count' in locals() else None,
            errors=text_errors
        )
        
    # 4. Preprocess
    resume_clean = clean_text(resume_raw)
    job_clean = clean_text(jd_text)
    
    # 5. Keyword Coverage
    resume_kws = extract_top_keywords(resume_clean)
    job_kws = extract_top_keywords(job_clean)
    matched_kws = list(set(resume_kws) & set(job_kws))
    missing_kws = list(set(job_kws) - set(resume_kws))
    kw_cov = (len(matched_kws) / len(job_kws) * 100) if job_kws else 100.0
    
    # 6. Semantic Similarity
    sim_score = calculate_cosine_similarity(resume_clean, job_clean)
    
    # 7. Skills & Evidence Extraction
    skills_dict = load_skills_dict()
    resume_skills_evidence = extract_skills_with_evidence(resume_clean, skills_dict)
    resume_skills_canonical = [e.skill for e in resume_skills_evidence]
    job_skills_canonical = extract_skills_with_evidence(job_clean, skills_dict)
    job_skills_canonical = [e.skill for e in job_skills_canonical]
    
    # 8. Requirements Analysis
    req_pref = get_required_preferred_terms(jd_text, skills_dict)
    reqs = {"required": req_pref["required_terms"], "preferred": req_pref["preferred_terms"]}
    
    # 9. Evidence & Recommendations
    rec_results = generate_evidence_and_recommendations(
        resume_skills_evidence=resume_skills_evidence,
        job_required_skills=reqs["required"],
        job_preferred_skills=reqs["preferred"],
        skills_dict=skills_dict,
        missing_kws=missing_kws
    )
    
    # 10. Provisional Scoring
    evidence = rec_results["evidence"]
    matched_skills = [e.skill for e in evidence if e.evidence_level == "MATCHED"]
    
    # Calculate coverage
    matched_req = [s for s in reqs["required"] if s in resume_skills_canonical]
    req_cov = (len(matched_req) / len(reqs["required"]) * 100) if reqs["required"] else 100.0
    matched_skills_cov = (len(matched_skills) / len(job_skills_canonical) * 100) if job_skills_canonical else 100.0
    
    prov_score = calculate_match_score(
        similarity=sim_score,
        keyword_coverage=kw_cov,
        skills_overlap=matched_skills_cov,
        required_term_coverage=req_cov
    )
    
    # Track metrics
    high_impact_count = sum(1 for r in rec_results["recommendations"] if r.impact == "HIGH")
    medium_impact_count = sum(1 for r in rec_results["recommendations"] if r.impact == "MEDIUM")
    
    log_analysis_completed(
        duration_ms=int((time.time() - start_time) * 1000),
        resume_page_count=resume_page_count,
        recommendation_count=len(rec_results["recommendations"]),
        high_impact_count=high_impact_count,
        medium_impact_count=medium_impact_count
    )
    
    return AnalysisResult(
        similarity_score=sim_score,
        resume_text_length=len(resume_raw),
        job_text_length=len(jd_text),
        resume_page_count=resume_page_count,
        keywords=job_kws,
        matched_keywords=matched_kws,
        missing_keywords=missing_kws,
        keyword_coverage=kw_cov,
        
        provisional_score=prov_score,
        resume_skills=resume_skills_canonical,
        job_skills=job_skills_canonical,
        evidence=evidence,
        required_terms=reqs["required"],
        preferred_terms=reqs["preferred"],
        required_term_coverage=req_cov,
        recommendations=rec_results["recommendations"]
    )
