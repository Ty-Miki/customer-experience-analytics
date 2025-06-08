import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from scripts.extract_keywords import get_top_keywords, extract_keywords

def test_get_top_keywords_basic():
    # Simulate a sparse row vector with 5 features
    row_vector = csr_matrix([[0.1, 0.5, 0.0, 0.3, 0.2]])
    feature_names = np.array(["apple", "banana", "cat", "dog", "egg"])
    top_n = 3
    result = get_top_keywords(row_vector, feature_names, top_n)
    # Should return the top 3 nonzero features in descending order
    assert result == ["banana", "dog", "egg"]

def test_get_top_keywords_handles_zeros():
    row_vector = csr_matrix([[0, 0, 0, 0, 0]])
    feature_names = np.array(["a", "b", "c", "d", "e"])
    result = get_top_keywords(row_vector, feature_names, 2)
    assert result == []

def test_extract_keywords_adds_column():
    df = pd.DataFrame({
        "review": [
            "the app is good and easy to use",
            "bad experience, app crashes often",
            "excellent service and friendly staff"
        ]
    })
    result = extract_keywords(df.copy(), text_column="review", top_n=2)
    assert "keywords" in result.columns
    assert isinstance(result["keywords"].iloc[0], list)
    assert len(result["keywords"].iloc[0]) <= 2