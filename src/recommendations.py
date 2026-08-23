def generate_recommendations(resume_skills: list[str], job_required_skills: list[str], job_preferred_skills: list[str], skills_dict: dict) -> dict:
    """
    Compares resume skills against job requirements to produce:
    - matched_skills
    - missing_skills
    - weak_evidence
    - recommendations
    """
    
    # We need a reverse mapping for canonical -> generic_parent
    canonical_to_parent = {}
    for key, data in skills_dict.items():
        canonical_to_parent[data['canonical']] = data.get('generic_parent')
        
    matched = []
    missing = []
    weak = []
    recs = []
    
    # Check Required Skills
    for skill in job_required_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            jd_skill_parent = canonical_to_parent.get(skill)
            
            weak_found = False
            for r_skill in resume_skills:
                # JD required PostgreSQL (parent: SQL Database). Resume has "SQL Database" or "MySQL" (parent: SQL Database)
                if jd_skill_parent and (r_skill == jd_skill_parent or canonical_to_parent.get(r_skill) == jd_skill_parent):
                    weak_found = True
                    break
                    
            if weak_found:
                weak.append(skill)
                recs.append(f"If you have used {skill}, consider specifying it explicitly (you mentioned related skills).")
            else:
                missing.append(skill)
                recs.append(f"If you have used {skill}, consider specifying it explicitly.")
                
    # Preferred skills - less strict
    for skill in job_preferred_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            recs.append(f"If you have used {skill}, consider specifying it explicitly (Bonus).")
            
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "weak_evidence": weak,
        "recommendations": recs
    }
