from .models import Recommendation, RequirementEvidence, SkillEvidence

def generate_evidence_and_recommendations(
    resume_skills_evidence: list[SkillEvidence], 
    job_required_skills: list[str], 
    job_preferred_skills: list[str], 
    skills_dict: dict, 
    missing_kws: list[str]
) -> dict:
    
    canonical_to_parent = {}
    for key, data in skills_dict.items():
        canonical_to_parent[data['canonical']] = data.get('generic_parent')
        
    resume_skill_map = {e.skill: e.source for e in resume_skills_evidence}
    resume_skills = list(resume_skill_map.keys())
    
    evidence_list: list[RequirementEvidence] = []
    recs: list[Recommendation] = []
    
    # REQUIRED
    for skill in job_required_skills:
        if skill in resume_skill_map:
            source = resume_skill_map[skill]
            if source in ["Education", "Other"]:
                level = "WEAK"
            else:
                level = "MATCHED"
            
            evidence_list.append(RequirementEvidence(skill=skill, requirement_type="REQUIRED", evidence_level=level, evidence_source=source))
        else:
            jd_skill_parent = canonical_to_parent.get(skill)
            weak_found = False
            weak_source = "None"
            for r_skill in resume_skills:
                if jd_skill_parent and (r_skill == jd_skill_parent or canonical_to_parent.get(r_skill) == jd_skill_parent):
                    weak_found = True
                    weak_source = resume_skill_map[r_skill]
                    break
                    
            if weak_found:
                # It's an indirect match, so it's always WEAK
                evidence_list.append(RequirementEvidence(skill=skill, requirement_type="REQUIRED", evidence_level="WEAK", evidence_source=weak_source))
            else:
                evidence_list.append(RequirementEvidence(skill=skill, requirement_type="REQUIRED", evidence_level="MISSING", evidence_source="None"))

    # PREFERRED
    for skill in job_preferred_skills:
        if skill in resume_skill_map:
            source = resume_skill_map[skill]
            if source in ["Education", "Other"]:
                level = "WEAK"
            else:
                level = "MATCHED"
            evidence_list.append(RequirementEvidence(skill=skill, requirement_type="PREFERRED", evidence_level=level, evidence_source=source))
        else:
            jd_skill_parent = canonical_to_parent.get(skill)
            weak_found = False
            weak_source = "None"
            for r_skill in resume_skills:
                if jd_skill_parent and (r_skill == jd_skill_parent or canonical_to_parent.get(r_skill) == jd_skill_parent):
                    weak_found = True
                    weak_source = resume_skill_map[r_skill]
                    break
                    
            if weak_found:
                # Indirect match is always WEAK
                evidence_list.append(RequirementEvidence(skill=skill, requirement_type="PREFERRED", evidence_level="WEAK", evidence_source=weak_source))
            else:
                evidence_list.append(RequirementEvidence(skill=skill, requirement_type="PREFERRED", evidence_level="MISSING", evidence_source="None"))
            
    # RECOMMENDATIONS (Deterministic Ordering)
    for ev in evidence_list:
        if ev.requirement_type == "REQUIRED":
            if ev.evidence_level == "MISSING":
                recs.append(Recommendation(impact="HIGH", action=f"Add {ev.skill}", evidence_type="Required skill · Missing. Add evidence if you have genuinely used it in a project, course, or professional work."))
            elif ev.evidence_level == "WEAK":
                recs.append(Recommendation(impact="HIGH", action=f"Add {ev.skill} explicitly", evidence_type=f"Required skill · Weak evidence. Mentioned in {ev.evidence_source} but lacks practical demonstration."))
                
    for ev in evidence_list:
        if ev.requirement_type == "PREFERRED" and ev.evidence_level == "MISSING":
            recs.append(Recommendation(impact="MEDIUM", action=f"Mention {ev.skill}", evidence_type="Preferred skill · Missing. Mention only if you have hands-on experience you can substantiate."))
            
    for kw in missing_kws[:3]:
        recs.append(Recommendation(impact="LOW", action=f"Include '{kw}'", evidence_type="General terminology improvement"))
        
    return {
        "evidence": evidence_list,
        "recommendations": recs
    }

def generate_recommendations(resume_skills: list[str], job_required_skills: list[str], job_preferred_skills: list[str], skills_dict: dict, missing_kws: list[str] = []) -> dict:
    """Backwards compatibility for older tests."""
    # Convert string skills to strong evidence for old tests
    evidence = [SkillEvidence(skill=s, source="Professional Experience") for s in resume_skills]
    res = generate_evidence_and_recommendations(evidence, job_required_skills, job_preferred_skills, skills_dict, missing_kws)
    return {
        "matched_skills": [e.skill for e in res["evidence"] if e.evidence_level == "MATCHED"],
        "missing_skills": [e.skill for e in res["evidence"] if e.evidence_level == "MISSING"],
        "weak_evidence": [e.skill for e in res["evidence"] if e.evidence_level == "WEAK"],
        "recommendations": res["recommendations"]
    }
