from src.recommendations import generate_recommendations

def test_generate_recommendations():
    skills_dict = {
        "postgresql": {"canonical": "PostgreSQL", "generic_parent": "SQL Database"},
        "mysql": {"canonical": "MySQL", "generic_parent": "SQL Database"},
        "sql server": {"canonical": "SQL Server", "generic_parent": "SQL Database"},
        "python": {"canonical": "Python", "generic_parent": "Programming Language"},
        "docker": {"canonical": "Docker", "generic_parent": "DevOps"}
    }
    
    resume_skills = ["Python", "MySQL"]
    job_required = ["Python", "PostgreSQL", "Docker"]
    job_preferred = []
    
    res = generate_recommendations(resume_skills, job_required, job_preferred, skills_dict, [])
    
    # Python should match
    assert "Python" in res["matched_skills"]
    
    # PostgreSQL is required, resume has MySQL (same parent). Under Day 5 rules indirect matches are always WEAK.
    assert "PostgreSQL" in res["weak_evidence"]
    assert "PostgreSQL" not in res["missing_skills"]
    
    # Docker is required, resume has nothing related. Missing.
    assert "Docker" in res["missing_skills"]
    assert "Docker" not in res["weak_evidence"]
    
    # Verify recommendation impacts
    recs = res["recommendations"]
    high_impact_actions = [r.action for r in recs if r.impact == "HIGH"]
    assert "Add PostgreSQL explicitly" in high_impact_actions
    assert "Add Docker" in high_impact_actions
