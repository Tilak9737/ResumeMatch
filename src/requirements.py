import re

REQUIRED_MARKERS = [
    r"must have", r"required", r"essential", r"minimum qualifications",
    r"basic qualifications", r"requirements", r"we need", r"you must"
]

PREFERRED_MARKERS = [
    r"preferred", r"bonus", r"nice to have", r"plus",
    r"preferred qualifications", r"good to have", r"ideally"
]

def split_into_sentences(text: str) -> list[str]:
    """Splits text into sentences based on punctuation and newlines."""
    # Split by '.', '!', '?', or newlines.
    sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
    return [s.strip() for s in sentences if s.strip()]

def extract_requirement_sentences(text: str) -> dict:
    """
    Classifies sentences into 'required' or 'preferred' context blocks.
    Returns a dict with lists of sentences.
    """
    sentences = split_into_sentences(text)
    
    required_sentences = []
    preferred_sentences = []
    
    # State tracking for block-based lists (e.g. "Requirements:\n - Python\n - SQL")
    current_context = "neutral"
    
    req_pattern = re.compile(r'\b(' + '|'.join(REQUIRED_MARKERS) + r')\b', re.IGNORECASE)
    pref_pattern = re.compile(r'\b(' + '|'.join(PREFERRED_MARKERS) + r')\b', re.IGNORECASE)
    
    for sentence in sentences:
        if req_pattern.search(sentence):
            current_context = "required"
            required_sentences.append(sentence)
        elif pref_pattern.search(sentence):
            current_context = "preferred"
            preferred_sentences.append(sentence)
        else:
            # If it's a list item (starts with -, *, •) inherit context
            if re.match(r'^[-*•]', sentence) or re.match(r'^\d+\.', sentence):
                if current_context == "required":
                    required_sentences.append(sentence)
                elif current_context == "preferred":
                    preferred_sentences.append(sentence)
            else:
                # Reset context for normal sentences without markers
                current_context = "neutral"
                
    return {
        "required": required_sentences,
        "preferred": preferred_sentences
    }

def get_required_preferred_terms(jd_text: str, skills_dict: dict) -> dict:
    """
    Extracts canonical skills that fall under required and preferred contexts.
    """
    from src.skills import extract_skills
    
    sentences_map = extract_requirement_sentences(jd_text)
    
    required_text = " ".join(sentences_map["required"])
    preferred_text = " ".join(sentences_map["preferred"])
    
    required_skills = extract_skills(required_text, skills_dict)
    preferred_skills = extract_skills(preferred_text, skills_dict)
    
    # Required takes precedence over preferred if there's a contradiction
    preferred_skills = [s for s in preferred_skills if s not in required_skills]
    
    return {
        "required_terms": required_skills,
        "preferred_terms": preferred_skills
    }
