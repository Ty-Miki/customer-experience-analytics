# Tests Directory

This directory contains automated tests for the core scripts in the customer experience analytics project. All tests are written using `pytest` and utilize mocking where appropriate to ensure fast, reliable, and isolated test runs.

---

## Test Modules

### 1. `test_clean_reviews.py`

**Purpose:**  
Tests the `clean_reviews` function from `scripts/clean_reviews_data.py`.

**Coverage:**
- Verifies that specified columns are dropped from the DataFrame.
- Checks that columns are correctly renamed.
- Ensures new columns are added with default values.
- Tests combinations of dropping, renaming, and adding columns.

---

### 2. `test_scrape_reviews.py`

**Purpose:**  
Tests the `GooglePlayReviewScraper` class from `scripts/scrape_reviews.py`.

**Coverage:**
- Mocks the Google Play scraping process to verify the correct number of reviews are fetched.
- Ensures reviews are saved to CSV using pandas.
- Checks that the orchestration method (`scrape_and_save`) calls the appropriate internal methods.

---

### 3. `test_load_csv.py`

**Purpose:**  
Tests the `load_reviews` function from `scripts/load_csv.py`.

**Coverage:**
- Verifies that the function returns `None` if the file does not exist.
- Ensures successful loading of a CSV file returns the correct DataFrame.
- Checks that exceptions during loading are handled gracefully and return `None`.

---

### 4. `test_text_preprocessor.py`

**Purpose:**  
Tests the `ReviewPreprocessor` class from `scripts/text_preprocessor.py`.

**Coverage:**
- Ensures HTML tags, URLs, emails, numbers, punctuation, and emojis are removed from text.
- Checks that text is lowercased and extra spaces are removed.
- Verifies that non-string input is handled gracefully.
- Tests tokenization, stopword removal, and lemmatization.

---

### 5. `test_sentiment_analysis.py`

**Purpose:**  
Tests the `SentimentAnalyzer` class from `scripts/sentiment_analysis.py`.

**Coverage:**
- Mocks VADER and TextBlob to test sentiment prediction logic.
- Verifies correct sentiment label and score for positive, negative, and neutral cases.
- Ensures fallback to TextBlob works as expected.
- Checks handling of empty and non-string input.

---

### 6. `test_plot_generator.py`

**Purpose:**  
Tests the `PlotGenerator` class from `scripts/plot_generator.py`.

**Coverage:**
- Mocks seaborn and matplotlib to verify plotting and saving logic.
- Ensures bar charts are generated with correct parameters.
- Checks legend handling and file saving.

---

### 7. `test_extract_keywords.py`

**Purpose:**  
Tests the `get_top_keywords` and `extract_keywords` functions from `scripts/extract_keywords.py`.

**Coverage:**
- Verifies extraction of top N keywords from TF-IDF vectors.
- Ensures correct handling of all-zero vectors.
- Checks that the `keywords` column is added and contains lists.
- Tests behavior with empty or missing text.

---

### 8. `test_map_keywords_with_themes.py`

**Purpose:**  
Tests the `map_keywords_to_themes` and `get_examples_by_theme` functions from `scripts/map_keywords_with_themes.py`.

**Coverage:**
- Verifies mapping of keywords to user-defined themes, including unmatched keywords.
- Ensures "Other" is returned when no theme matches.
- Checks collection of example texts for each theme, respecting the maximum examples limit.

---

## Running the Tests

From the project root, run:

```sh
pytest tests/
```

All tests are self-contained and do not require network or file system access due to the use of mocking.

---

## Notes

- Tests are designed to be fast and reliable.
- Mocking is used to isolate units of code and avoid side effects.

---