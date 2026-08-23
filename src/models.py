from dataclasses import dataclass, field
from typing import List

@dataclass
class AnalysisResult:
    similarity_score: float
    resume_text_length: int
    job_text_length: int
    
    # Day 1 - TF-IDF Keywords
    keywords: List[str] = field(default_factory=list)
    matched_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)
    keyword_coverage: float = 0.0
    
    # Day 3 - NLP Intelligence
    provisional_score: float = 0.0
    resume_skills: List[str] = field(default_factory=list)
    job_skills: List[str] = field(default_factory=list)
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    weak_evidence: List[str] = field(default_factory=list)
    
    required_terms: List[str] = field(default_factory=list)
    preferred_terms: List[str] = field(default_factory=list)
    required_term_coverage: float = 0.0
    
    recommendations: List[str] = field(default_factory=list)
    
    errors: List[str] = field(default_factory=list)
