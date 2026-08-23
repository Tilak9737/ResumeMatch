import os
from src.analysis import analyze_resume_match
from src.skills import load_skills_dict

def run_realistic_test():
    jd_raw = """
    Job Title: Data Analyst
    
    Required:
    - Python
    - SQL
    - PostgreSQL
    - Power BI
    
    Preferred:
    - AWS
    - Docker
    """
    
    resume_raw = """
    Experienced Data Analyst.
    Skills: Python, SQL, MySQL, Power BI, Pandas, Excel.
    Built dashboards and automated data analysis workflows.
    """
    
    from scripts.evaluate_day3 import analyze_raw_text
    skills_dict = load_skills_dict()
    
    res = analyze_raw_text(resume_raw, jd_raw, skills_dict)
    
    print("=== REALISTIC RESUMEMATCH TEST ===")
    print(f"Required coverage: {res['provisional_score']:.1f}%")
    print(f"Matched Skills: 🟢 {res['matched_skills']}")
    print(f"Weak Evidence:  🟡 {res['weak_evidence']}")
    print(f"Missing Skills: 🔴 {res['missing_skills']}")
    
    print("\nRecommendations:")
    for r in res['recommendations']:
        print(f"- {r}")

if __name__ == "__main__":
    run_realistic_test()
