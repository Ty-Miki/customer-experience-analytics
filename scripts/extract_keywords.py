from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Extract top N keywords per document
def get_top_keywords(row_vector, feature_names, top_n):
    row_array = row_vector.toarray().flatten()
    top_indices = row_array.argsort()[-top_n:][::-1]
    return [feature_names[i] for i in top_indices if row_array[i] > 0]

def extract_keywords(df: pd.DataFrame, text_column: str, top_n: int = 5) -> pd.DataFrame:
    """
    Extracts top keywords per review using TF-IDF and appends them to a new 'keywords' column.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the review text.
    - text_column (str): Name of the column with cleaned, preprocessed text.
    - top_n (int): Number of top keywords to extract per review.

    Returns:
    - pd.DataFrame: Modified DataFrame with an additional 'keywords' column.
    """
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(df[text_column])
    feature_names = vectorizer.get_feature_names_out()

    df['keywords'] = [get_top_keywords(tfidf_matrix[i], feature_names, top_n) for i in range(tfidf_matrix.shape[0])]
    logging.info(f"Extracted keywords from the given df")
    return df
