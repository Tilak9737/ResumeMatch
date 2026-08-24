import json
import re
import os
from .models import SkillEvidence

def load_skills_dict(filepath=None):
    """Loads the skills dictionary from a JSON file."""
    if filepath is None:
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "skills.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def _get_section_for_match(text: str, match_start: int) -> str:
    headers = {
        "Professional Experience": [r"\bexperience\b", r"\bwork history\b", r"\bemployment\b", r"\bprofessional\b", r"\bcareer\b"],
        "Project": [r"\bprojects\b", r"\bportfolio\b"],
        "Technical Skills": [r"\bskills\b", r"\btechnologies\b", r"\btechnical\b", r"\bcompetencies\b"],
        "Education": [r"\beducation\b", r"\bcoursework\b", r"\bacademic\b", r"\bdegree\b", r"\buniversity\b", r"\bcollege\b"]
    }
    
    closest_header = "Other"
    closest_dist = float('inf')
    
    # We only look backwards up to 2000 characters to avoid finding a header from way too far away
    # and we look for the *last* occurrence of a header before the match.
    text_before = text[max(0, match_start - 2000):match_start].lower()
    
    for section, patterns in headers.items():
        for pat in patterns:
            for m in re.finditer(pat, text_before):
                dist = len(text_before) - m.start()
                if dist < closest_dist:
                    closest_dist = dist
                    closest_header = section
                    
    return closest_header

def extract_skills_with_evidence(text: str, skills_dict: dict) -> list[SkillEvidence]:
    if not text:
        return []
        
    extracted = {}
    
    for key, data in skills_dict.items():
        canonical = data['canonical']
        aliases = data.get('aliases', [])
        
        for alias in aliases:
            escaped_alias = re.escape(alias)
            pattern = rf"(?<![a-zA-Z0-9_]){escaped_alias}(?![a-zA-Z0-9_])"
            flags = re.IGNORECASE
            
            if alias.lower() in ["c", "r", "go"]:
                flags = 0
                if alias == "go": escaped_alias = "Go"
                if alias == "c": escaped_alias = "C"
                if alias == "r": escaped_alias = "R"
                pattern = rf"(?<![a-zA-Z0-9_]){escaped_alias}(?![a-zA-Z0-9_])"
                
            for match in re.finditer(pattern, text, flags):
                source = _get_section_for_match(text, match.start())
                if canonical not in extracted:
                    extracted[canonical] = []
                extracted[canonical].append(source)
                
    source_hierarchy = {
        "Professional Experience": 5,
        "Project": 4,
        "Technical Skills": 3,
        "Education": 2,
        "Other": 1
    }
    
    results = []
    for skill, sources in extracted.items():
        best_source = max(sources, key=lambda s: source_hierarchy[s])
        results.append(SkillEvidence(skill=skill, source=best_source))
        
    # Sort alphabetically by skill name
    results.sort(key=lambda x: x.skill)
    return results

def extract_skills(text: str, skills_dict: dict) -> list[str]:
    """Backwards compatibility for older code"""
    evidences = extract_skills_with_evidence(text, skills_dict)
    return [e.skill for e in evidences]
