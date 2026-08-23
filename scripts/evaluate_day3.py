import json
from src.preprocess import clean_text
from src.similarity import calculate_cosine_similarity
from src.keywords import extract_top_keywords
from src.skills import load_skills_dict, extract_skills
from src.requirements import get_required_preferred_terms
from src.recommendations import generate_recommendations
from src.scoring import calculate_match_score

def analyze_raw_text(resume_raw: str, jd_raw: str, skills_dict: dict):
    resume_clean = clean_text(resume_raw)
    job_clean = clean_text(jd_raw)
    
    similarity = calculate_cosine_similarity(resume_clean, job_clean)
    
    resume_keywords = extract_top_keywords(resume_clean)
    job_keywords = extract_top_keywords(job_clean)
    
    matched_kws = list(set(resume_keywords) & set(job_keywords))
    keyword_cov = (len(matched_kws) / len(job_keywords) * 100) if job_keywords else 100.0
    
    resume_skills = extract_skills(resume_clean, skills_dict)
    job_skills = extract_skills(job_clean, skills_dict)
    
    req_pref = get_required_preferred_terms(jd_raw, skills_dict)
    req_terms = req_pref["required_terms"]
    pref_terms = req_pref["preferred_terms"]
    
    recs_output = generate_recommendations(resume_skills, req_terms, pref_terms, skills_dict)
    
    skills_cov = (len(recs_output["matched_skills"]) / len(job_skills) * 100) if job_skills else 100.0
    matched_req = [s for s in req_terms if s in resume_skills]
    req_cov = (len(matched_req) / len(req_terms) * 100) if req_terms else 100.0
    
    prov_score = calculate_match_score(
        similarity=similarity,
        keyword_coverage=keyword_cov,
        skills_overlap=skills_cov,
        required_term_coverage=req_cov
    )
    
    return {
        "similarity": similarity,
        "provisional_score": prov_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "required_terms": req_terms,
        "matched_skills": recs_output["matched_skills"],
        "weak_evidence": recs_output["weak_evidence"],
        "missing_skills": recs_output["missing_skills"],
        "recommendations": recs_output["recommendations"]
    }

def run_evaluation():
    skills_dict = load_skills_dict()
    
    tests = [
        {
            "id": "A",
            "name": "Test A — Lexical Stuffing",
            "jd": "Required: Python, SQL, AWS, Docker.",
            "res": "Python Python Python SQL SQL SQL AWS AWS AWS Docker Docker Docker"
        },
        {
            "id": "B",
            "name": "Test B — Generic Terminology",
            "jd": "Required: PostgreSQL.",
            "res": "I have experience with SQL databases and MySQL."
        },
        {
            "id": "C",
            "name": "Test C — Exact Skill",
            "jd": "Must have: Python and Docker.",
            "res": "I used Python and Docker in my last project."
        },
        {
            "id": "D",
            "name": "Test D — Missing Skill",
            "jd": "Requirements: PostgreSQL.",
            "res": "I used Python."
        },
        {
            "id": "E",
            "name": "Test E — Alias Equivalence",
            "jd": "Required: PostgreSQL.",
            "res": "Built a system using Postgres."
        },
        {
            "id": "F1",
            "name": "Test F1 — False Positive",
            "jd": "R programming experience required.",
            "res": "Our company develops software."
        },
        {
            "id": "F2",
            "name": "Test F2 — True Positive",
            "jd": "R programming experience required.",
            "res": "Built statistical models in R."
        }
    ]
    
    print("="*60)
    print("DAY 3 EVALUATION REPORT: SKILL-AWARE MATCHING")
    print("="*60)
    
    for t in tests:
        res = analyze_raw_text(t["res"], t["jd"], skills_dict)
        print(f"\n{t['name']}")
        print(f"Day 1 TF-IDF similarity:       {res['similarity']:.1f}%")
        print(f"Day 3 provisional score:       {res['provisional_score']:.1f}%")
        
        print("\nClassification:")
        if res['matched_skills']: print(f"MATCHED: {res['matched_skills']}")
        if res['weak_evidence']: print(f"WEAK EVIDENCE: {res['weak_evidence']}")
        if res['missing_skills']: print(f"MISSING: {res['missing_skills']}")
        
        if res['recommendations']:
            print("\nRecommendations:")
            for r in res['recommendations']:
                print(f"- {r}")
                
        print("-" * 40)

if __name__ == "__main__":
    run_evaluation()
