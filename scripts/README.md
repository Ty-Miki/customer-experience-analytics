# Scripts Directory

This directory contains core scripts for customer experience analytics, focused on collecting, cleaning, and loading Google Play Store app reviews.

## Contents

- [`scrape_reviews.py`](./scrape_reviews.py)
- [`clean_reviews_data.py`](./clean_reviews_data.py)
- [`load_csv.py`](./load_csv.py)
- [`text_preprocessor.py`](./text_preprocessor.py)
- [`sentiment_analysis.py`](./sentiment_analysis.py)
- [`plot_generator.py`](./plot_generator.py)
- [`extract_keywords.py`](./extract_keywords.py)
- [`map_keywords_with_themes.py`](./map_keywords_with_themes.py)

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

### 4. `text_preprocessor.py`

**Purpose:**  
Provides a class for cleaning and tokenizing review text using regular expressions and spaCy.

**Key Features:**
- Removes HTML tags, URLs, emails, numbers, punctuation, emojis, and extra spaces.
- Converts text to lowercase.
- Tokenizes text, removes stopwords and short tokens, and lemmatizes using spaCy.
- Designed for preprocessing text data before analysis or modeling.

**Usage Example:**
```python
from scripts.text_preprocessor import ReviewPreprocessor

preprocessor = ReviewPreprocessor()
cleaned = preprocessor.clean_text("Great app! 😃 Visit http://example.com")
tokens = preprocessor.tokenize_text(cleaned)
```

---

### 5. `sentiment_analysis.py`

**Purpose:**  
Performs sentiment analysis on review text using VADER or TextBlob as a fallback.

**Key Features:**
- Uses VADER sentiment analysis if available, otherwise falls back to TextBlob.
- Returns both a sentiment label (`positive`, `neutral`, `negative`) and a score.
- Handles empty or non-string input gracefully.

**Usage Example:**
```python
from scripts.sentiment_analysis import SentimentAnalyzer

analyzer = SentimentAnalyzer()
label, score = analyzer.predict("I love this app!")
```

---

### 6. `plot_generator.py`

**Purpose:**  
Generates and saves bar charts from a pandas DataFrame using seaborn and matplotlib.

**Key Features:**
- Flexible bar chart generation with support for grouping (`hue`), custom titles, axis labels, and legends.
- Saves plots to file and displays them.
- Designed for quick visualization of aggregated review data.

**Usage Example:**
```python
from scripts.plot_generator import PlotGenerator
import pandas as pd

df = pd.DataFrame({"category": ["A", "B"], "value": [10, 20]})
plotter = PlotGenerator(df)
plotter.plot_barchart(
    x_value="category",
    y_value="value",
    title="Category Distribution",
    file_path="category_plot.png"
)
```

---

### 7. `extract_keywords.py`

**Purpose:**  
Extracts top keywords from review text using TF-IDF.

**Key Features:**
- Uses scikit-learn’s `TfidfVectorizer` to identify important keywords in each review.
- Adds a `keywords` column to the DataFrame with the top N keywords per review.
- Useful for topic modeling, theme extraction, or further text analysis.

**Usage Example:**
```python
from scripts.extract_keywords import extract_keywords

df = extract_keywords(df, text_column="cleaned_review", top_n=5)
print(df["keywords"].head())
```

---

### 8. `map_keywords_with_themes.py`

**Purpose:**  
Maps extracted keywords to predefined themes and retrieves example reviews for each theme.

**Key Features:**
- Maps keywords to user-defined themes using substring matching.
- Returns "Other" if no theme matches.
- Collects example review texts for each theme, with a configurable maximum per theme.
- Useful for qualitative analysis and reporting.

**Usage Example:**
```python
from scripts.map_keywords_with_themes import map_keywords_to_themes, get_examples_by_theme

themes = {"login": "Access", "crash": "Stability"}
keywords = ["login", "crash", "fast"]
mapped = map_keywords_to_themes(keywords, themes)

# For examples by theme:
import pandas as pd
df = pd.DataFrame({"themes": [["Access"], ["Stability"]], "cleaned_review": ["review1", "review2"]})
examples = get_examples_by_theme(df)
```

---

## Notes

- All scripts use Python logging for status and error reporting.
- Designed for modular use in data pipelines or as standalone utilities.
- Make sure to install required dependencies from ```requirements.txt``` before running these scripts.

---