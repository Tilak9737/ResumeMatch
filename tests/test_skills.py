import pytest
from src.skills import extract_skills

@pytest.fixture
def dummy_skills_dict():
    return {
        "r": {
            "canonical": "R",
            "aliases": ["r", "r programming"]
        },
        "c++": {
            "canonical": "C++",
            "aliases": ["c++", "cpp"]
        },
        ".net": {
            "canonical": ".NET",
            "aliases": [".net", "dotnet"]
        },
        "postgresql": {
            "canonical": "PostgreSQL",
            "aliases": ["postgres", "postgresql"]
        }
    }

def test_extract_skills_true_positives(dummy_skills_dict):
    text = "I have 5 years of experience with R programming, C++, and Postgres."
    skills = extract_skills(text, dummy_skills_dict)
    assert "R" in skills
    assert "C++" in skills
    assert "PostgreSQL" in skills
    assert len(skills) == 3

def test_extract_skills_false_positives(dummy_skills_dict):
    # 'Our' contains 'r', 'C++' without boundaries could trigger on things, etc.
    text = "Our company develops software. We use internet technologies."
    skills = extract_skills(text, dummy_skills_dict)
    assert "R" not in skills
    assert ".NET" not in skills

def test_extract_skills_boundaries_special_chars(dummy_skills_dict):
    # Testing that .NET matches properly even if starting with dot
    text1 = "I am a .NET developer."
    skills1 = extract_skills(text1, dummy_skills_dict)
    assert ".NET" in skills1

def test_alias_equivalence(dummy_skills_dict):
    # Both alias forms should map to exactly the same canonical output
    skills_1 = extract_skills("I use Postgres", dummy_skills_dict)
    skills_2 = extract_skills("I use PostgreSQL", dummy_skills_dict)
    assert skills_1 == ["PostgreSQL"]
    assert skills_2 == ["PostgreSQL"]

def test_f1_false_positive(dummy_skills_dict):
    text = "Our company develops software."
    skills = extract_skills(text, dummy_skills_dict)
    assert "R" not in skills

def test_f2_true_positive(dummy_skills_dict):
    text = "Built models in R."
    skills = extract_skills(text, dummy_skills_dict)
    assert "R" in skills

def test_ugly_resume_text():
    from src.skills import load_skills_dict
    real_skills = load_skills_dict()
    text = """
TECHNICAL SKILLS

Python | SQL | PostgreSQL | AWS
Docker / Kubernetes
Node.js
C++
C#
.NET
Power BI
CI/CD
Machine Learning
Python, Python, Python
"""
    extracted = extract_skills(text, real_skills)
    
    assert "Python" in extracted
    assert "SQL" in extracted
    assert "PostgreSQL" in extracted
    assert "AWS" in extracted
    assert "Docker" in extracted
    assert "Kubernetes" in extracted
    assert "Node.js" in extracted
    assert "C++" in extracted
    assert "C#" in extracted
    assert ".NET" in extracted
    assert "Power BI" in extracted
    assert "CI/CD" in extracted
    assert "Machine Learning" in extracted
    
    # Should only return one unique Python
    assert extracted.count("Python") == 1

def test_cross_category_false_matches():
    from src.skills import load_skills_dict
    real_skills = load_skills_dict()
    
    # JD: "Go programming". Resume: "go to market strategy"
    skills = extract_skills("I have a go to market strategy", real_skills)
    assert "Go" not in skills
    
    skills = extract_skills("Programming in Go.", real_skills)
    assert "Go" in skills
    
    # C 
    skills = extract_skills("I have a c level position.", real_skills)
    assert "C" not in skills # 'c' is extremely hard. If isolated 'c', it might match. Let's see if we can fix this if it fails.
    
    skills = extract_skills("Developed in C and C++.", real_skills)
    assert "C" in skills
    assert "C++" in skills

