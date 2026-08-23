def calculate_similarity_score(similarity: float) -> float:
    """
    Day 1 Scoring Interface.
    Currently just returns the similarity score.
    """
    return similarity

def calculate_match_score(
    similarity: float,
    keyword_coverage: float,
    skills_overlap: float,
    required_term_coverage: float
) -> float:
    """
    Day 3 Provisional Score Formula:
    (30 * keyword + 30 * similarity + 20 * skills + 10 * required) / 90
    
    All inputs should be 0-100 percentages.
    Note: Experience/Education (10%) is deferred to Day 5, so we normalize over 90.
    """
    total_weight = 90.0
    
    # Calculate weighted sum
    weighted_sum = (
        (30.0 * keyword_coverage) +
        (30.0 * similarity) +
        (20.0 * skills_overlap) +
        (10.0 * required_term_coverage)
    )
    
    # Normalize over active weights
    provisional_score = weighted_sum / total_weight
    
    return min(100.0, max(0.0, provisional_score))
