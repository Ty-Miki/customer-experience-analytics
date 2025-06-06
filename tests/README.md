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