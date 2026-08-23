from src.similarity import calculate_cosine_similarity

def test_similarity_identical():
    assert calculate_cosine_similarity("python sql pandas", "python sql pandas") > 99.0

def test_similarity_no_overlap():
    assert calculate_cosine_similarity("python sql", "marketing sales") < 1.0

def test_similarity_empty():
    assert calculate_cosine_similarity("", "python sql") == 0.0
    assert calculate_cosine_similarity("python", "") == 0.0
