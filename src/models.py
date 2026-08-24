from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SkillEvidence:
    skill: str
    source: str

@dataclass
class RequirementEvidence:
    skill: str
    requirement_type: str # "REQUIRED" | "PREFERRED"
    evidence_level: str # "MATCHED" | "WEAK" | "MISSING"
    evidence_source: str

@dataclass
class Recommendation:
    impact: str # "HIGH", "MEDIUM", "LOW"
    action: str
    evidence_type: str

@dataclass
class AnalysisResult:
    similarity_score: float
    resume_text_length: int
    job_text_length: int
    resume_page_count: Optional[int] = None
    
    # Day 1 - TF-IDF Keywords
    keywords: List[str] = field(default_factory=list)
    matched_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)
    keyword_coverage: float = 0.0
    
    # Day 3 - NLP Intelligence
    provisional_score: float = 0.0
    resume_skills: List[str] = field(default_factory=list)
    job_skills: List[str] = field(default_factory=list)
    
    evidence: List[RequirementEvidence] = field(default_factory=list)
    
    @property
    def matched_skills(self) -> List[str]:
        return [e.skill for e in self.evidence if e.evidence_level == "MATCHED"]
        
    @property
    def weak_evidence(self) -> List[str]:
        return [e.skill for e in self.evidence if e.evidence_level == "WEAK"]
        
    @property
    def missing_skills(self) -> List[str]:
        return [e.skill for e in self.evidence if e.evidence_level == "MISSING"]
    
    required_terms: List[str] = field(default_factory=list)
    preferred_terms: List[str] = field(default_factory=list)
    required_term_coverage: float = 0.0
    
    recommendations: List[Recommendation] = field(default_factory=list)
    
    errors: List[str] = field(default_factory=list)
