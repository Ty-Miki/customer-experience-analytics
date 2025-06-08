import pytest
from scripts.text_preprocessor import ReviewPreprocessor

@pytest.fixture(scope="module")
def preprocessor():
    return ReviewPreprocessor()

def test_clean_text_removes_html(preprocessor):
    text = "This is <b>bold</b> text."
    cleaned = preprocessor.clean_text(text)
    assert "<b>" not in cleaned and "bold" in cleaned

def test_clean_text_removes_url_email_number_punct(preprocessor):
    text = "Contact me at test@example.com! Visit http://example.com. Price: $100."
    cleaned = preprocessor.clean_text(text)
    assert "@" not in cleaned
    assert "http" not in cleaned
    assert "100" not in cleaned
    assert "$" not in cleaned
    assert "." not in cleaned

def test_clean_text_removes_emojis(preprocessor):
    text = "Great app! 😃👍"
    cleaned = preprocessor.clean_text(text)
    assert "😃" not in cleaned and "👍" not in cleaned

def test_clean_text_handles_non_string(preprocessor):
    assert preprocessor.clean_text(None) == ""
    assert preprocessor.clean_text(12345) == ""

def test_clean_text_lowercases(preprocessor):
    text = "HeLLo WoRLd"
    cleaned = preprocessor.clean_text(text)
    assert cleaned == "hello world"

def test_tokenize_text_filters_stopwords_and_short_tokens(preprocessor):
    # "the" is a stopword, "is" is a stopword, "app" and "good" should remain and be lemmatized
    tokens = preprocessor.tokenize_text("The app is good.")
    assert "app" in tokens
    assert "good" in tokens
    assert "the" not in tokens
    assert "is" not in tokens
    # All tokens should be at least 3 characters
    assert all(len(t) > 2 for t in tokens)