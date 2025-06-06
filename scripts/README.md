# Scripts Directory

This directory contains core scripts for customer experience analytics, focused on collecting, cleaning, and loading Google Play Store app reviews.

## Contents

- [`scrape_reviews.py`](./scrape_reviews.py)
- [`clean_reviews_data.py`](./clean_reviews_data.py)
- [`load_csv.py`](./load_csv.py)

---

## Script Overviews

### 1. `scrape_reviews.py`

**Purpose:**  
Automates the process of scraping user reviews for a specified app from the Google Play Store and saves them to a CSV file.

**Key Features:**
- Fetches a specified number of reviews using the `google_play_scraper` library.
- Saves the reviews to a CSV file with customizable naming.
- Includes logging for progress and error tracking.
- Can be used as a standalone script or imported as a module.

**Usage Example:**
```python
from scripts.scrape_reviews import main

main(
    app_id="com.example.app",
    bank_name="ExampleBank",
    total_reviews=200,
    lang="en",
    file_name="example_reviews.csv"
)
```

---

### 2. `clean_reviews_data.py`

**Purpose:**  
Provides utilities to clean and preprocess the reviews DataFrame.

**Key Features:**
- Drops unnecessary columns.
- Renames columns for consistency.
- Adds new columns with default values.
- Logs the cleaning process.

**Usage Example:**
```python
from scripts.clean_reviews_data import clean_reviews

cleaned_df = clean_reviews(
    df,
    drop_columns=["unwanted_column"],
    rename_columns={"old_name": "new_name"},
    new_columns={"processed": True}
)
```

---

### 3. `load_csv.py`

**Purpose:**  
Safely loads review data from a CSV file into a pandas DataFrame.

**Key Features:**
- Checks for file existence before loading.
- Handles exceptions and logs errors.
- Returns the loaded DataFrame or `None` if loading fails.

**Usage Example:**
```python
from scripts.load_csv import load_reviews

df = load_reviews("example_reviews.csv")
if df is not None:
    # Proceed with analysis
    pass
```

---

## Notes

- All scripts use Python logging for status and error reporting.
- Designed for modular use in data pipelines or as standalone utilities.
- Make sure to install required dependencies from ```requirements.txt``` before running these scripts.

---