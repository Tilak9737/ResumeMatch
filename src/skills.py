import json
import re
import os

def load_skills_dict(filepath=None):
    """Loads the skills dictionary from a JSON file."""
    if filepath is None:
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "skills.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_skills(text: str, skills_dict: dict) -> list[str]:
    """
    Extracts canonical skills from text using boundary-aware alias matching.
    Returns a unique list of canonical skills found.
    """
    if not text:
        return []
        
    extracted_canonical = set()
    
    for key, data in skills_dict.items():
        canonical = data['canonical']
        aliases = data.get('aliases', [])
        
        for alias in aliases:
            escaped_alias = re.escape(alias)
            pattern = rf"(?<![a-zA-Z0-9_]){escaped_alias}(?![a-zA-Z0-9_])"
            flags = re.IGNORECASE
            
            # For very short common-word aliases (C, R, Go), we should enforce case-sensitivity 
            # if they are single words without special characters to avoid matching "go to market" or "c-level"
            if alias.lower() in ["c", "r", "go"]:
                flags = 0 # Case sensitive
                if alias == "go": escaped_alias = "Go"
                if alias == "c": escaped_alias = "C"
                if alias == "r": escaped_alias = "R"
                pattern = rf"(?<![a-zA-Z0-9_]){escaped_alias}(?![a-zA-Z0-9_])"
                
            if re.search(pattern, text, flags):
                extracted_canonical.add(canonical)
                break
                
    return sorted(list(extracted_canonical))
