from src.preprocess import clean_text

def test_clean_text_technical_terms():
    text = "C++ C# .NET Node.js React.js CI/CD Power BI PostgreSQL AWS Azure Machine Learning"
    cleaned = clean_text(text)
    assert "c++" in cleaned
    assert "c#" in cleaned
    assert ".net" in cleaned
    assert "node.js" in cleaned
    assert "ci/cd" in cleaned
    assert "power bi" in cleaned
    assert "postgresql" in cleaned

def test_clean_text_basic():
    assert clean_text("Hello, World!") == "hello world"

def test_clean_text_empty():
    assert clean_text("") == ""
    assert clean_text(None) == ""

def test_clean_text_extra_whitespace():
    # Since we preserve dots now, it might be "this is a test."
    # Let's adjust to check the stripping behavior
    assert clean_text("  This \n is \t  a TEST.  ") == "this is a test."
