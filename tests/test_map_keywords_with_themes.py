import pandas as pd
from scripts.map_keywords_with_themes import map_keywords_to_themes, get_examples_by_theme

def test_map_keywords_to_themes_basic():
    keywords = ["login", "crash", "fast"]
    theme_map = {"login": "Access", "crash": "Stability", "fast": "Performance"}
    result = map_keywords_to_themes(keywords, theme_map)
    assert set(result) == {"Access", "Stability", "Performance"}

def test_map_keywords_to_themes_partial_and_other():
    keywords = ["unknown", "login"]
    theme_map = {"login": "Access"}
    result = map_keywords_to_themes(keywords, theme_map)
    assert "Access" in result
    # If no theme matched, should return ["Other"]
    result = map_keywords_to_themes(["unknown"], theme_map)
    assert result == ["Other"]

def test_get_examples_by_theme_basic():
    df = pd.DataFrame({
        "themes": [["A", "B"], ["A"], ["B"], ["C"]],
        "cleaned_review": ["review1", "review2", "review3", "review4"]
    })
    examples = get_examples_by_theme(df, theme_col="themes", text_col="cleaned_review", max_examples=2)
    assert set(examples.keys()) == {"A", "B", "C"}
    assert len(examples["A"]) == 2
    assert "review1" in examples["A"]
    assert "review2" in examples["A"]
    assert len(examples["B"]) == 2
    assert len(examples["C"]) == 1

def test_get_examples_by_theme_max_examples():
    df = pd.DataFrame({
        "themes": [["A"], ["A"], ["A"], ["A"]],
        "cleaned_review": ["r1", "r2", "r3", "r4"]
    })
    examples = get_examples_by_theme(df, theme_col="themes", text_col="cleaned_review", max_examples=2)
    assert len(examples["A"]) == 2
    assert examples["A"] == ["r1", "r2"]