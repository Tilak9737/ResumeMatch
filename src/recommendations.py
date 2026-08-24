from .models import Recommendation

def generate_recommendations(resume_skills: list[str], job_required_skills: list[str], job_preferred_skills: list[str], skills_dict: dict, missing_kws: list[str]) -> dict:
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
    recs: list[Recommendation] = []
    
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
                recs.append(Recommendation(
                    impact="HIGH",
                    action=f"Add {skill} explicitly",
                    evidence_type="Required skill • Weak evidence detected"
                ))
            else:
                missing.append(skill)
                recs.append(Recommendation(
                    impact="HIGH",
                    action=f"Add {skill}",
                    evidence_type="Required skill • Missing"
                ))
                
    # Preferred skills - less strict
    for skill in job_preferred_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill) # Consider it missing but preferred
            recs.append(Recommendation(
                impact="MEDIUM",
                action=f"Mention {skill} if you have used it",
                evidence_type="Preferred skill • Missing"
            ))
            
    # Low impact keywords
    for kw in missing_kws[:3]: # Limit to top 3 missing general keywords
        recs.append(Recommendation(
            impact="LOW",
            action=f"Include '{kw}' in your experience where applicable",
            evidence_type="General terminology improvement"
        ))
            
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "weak_evidence": weak,
        "recommendations": recs
    }
