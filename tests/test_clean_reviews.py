import pandas as pd
from scripts.clean_reviews_data import clean_reviews

def test_clean_reviews_drops_columns():
    df = pd.DataFrame({
        "a": [1, 2],
        "b": [3, 4],
        "c": [5, 6]
    })
    cleaned = clean_reviews(df.copy(), drop_columns=["b"], rename_columns={}, new_columns={})
    assert "b" not in cleaned.columns
    assert cleaned.shape[1] == 2

def test_clean_reviews_renames_columns():
    df = pd.DataFrame({
        "old": [1, 2],
        "keep": [3, 4]
    })
    cleaned = clean_reviews(df.copy(), drop_columns=[], rename_columns={"old": "new"}, new_columns={})
    assert "new" in cleaned.columns
    assert "old" not in cleaned.columns

def test_clean_reviews_adds_new_columns():
    df = pd.DataFrame({
        "x": [1, 2]
    })
    cleaned = clean_reviews(df.copy(), drop_columns=[], rename_columns={}, new_columns={"added": 0})
    assert "added" in cleaned.columns
    assert all(cleaned["added"] == 0)

def test_clean_reviews_combined():
    df = pd.DataFrame({
        "a": [1, 2],
        "b": [3, 4],
        "c": [5, 6]
    })
    cleaned = clean_reviews(
        df.copy(),
        drop_columns=["b"],
        rename_columns={"a": "alpha"},
        new_columns={"new_col": "test"}
    )
    assert "b" not in cleaned.columns
    assert "alpha" in cleaned.columns
    assert "new_col" in cleaned.columns
    assert all(cleaned["new_col"] == "test")