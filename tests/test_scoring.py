import pytest
from src.scoring import calculate_match_score

def test_calculate_match_score_boundaries():
    # Minimum
    assert calculate_match_score(0, 0, 0, 0) == 0.0
    
    # Maximum
    assert calculate_match_score(100, 100, 100, 100) == 100.0
    
    # Midpoint
    score = calculate_match_score(50, 50, 50, 50)
    assert score == 50.0

def test_calculate_match_score_bounds():
    # It should not exceed 100 even if inputs somehow go over 100
    assert calculate_match_score(110, 110, 110, 110) == 100.0
    
    # It should not go below 0
    assert calculate_match_score(-10, -10, -10, -10) == 0.0

def test_calculate_match_score_partial():
    # 30 kw, 30 sim, 20 skills, 10 req = 90 total
    # If kw=100, others=0 -> (30*100) / 90 = 33.33
    score = calculate_match_score(0, 100, 0, 0)
    assert round(score, 2) == 33.33
    
    # If req=100, others=0 -> (10*100) / 90 = 11.11
    score = calculate_match_score(0, 0, 0, 100)
    assert round(score, 2) == 11.11
