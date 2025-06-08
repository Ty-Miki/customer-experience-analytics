# Notebook: ```data_cleaning.ipynb```
## Data Cleaning and Aggregation of Bank App Reviews

This notebook demonstrates the end-to-end process of collecting, cleaning, and aggregating user reviews from Google Play Store for multiple Ethiopian banks' mobile apps. It leverages utility scripts for scraping, loading, and cleaning review data.

---

## Workflow Overview

1. **Setup and Imports**
   - Adds the project parent directory to `sys.path` for easy script imports.
   - Imports utility functions from the `scripts` directory.

2. **Scraping Reviews**
   - Uses the `GooglePlayReviewScraper` (via the `main` function in `scrape_reviews.py`) to fetch reviews for three banks:
     - Commercial Bank of Ethiopia (CBE)
     - Bank of Abyssinia (BOA)
     - Dashen Bank
   - Saves each bank's reviews as a separate CSV file in the `data` directory.

3. **Loading Data**
   - Loads the saved CSV files using the `load_reviews` function from `load_csv.py`.
   - Each bank's reviews are loaded into a pandas DataFrame for further processing.

4. **Cleaning Data**
   - Cleans each DataFrame using the `clean_reviews` function from `clean_reviews_data.py`:
     - Drops unnecessary columns.
     - Renames columns for consistency.
     - Adds new columns to indicate the bank and data source.
   - Ensures all DataFrames have a uniform structure.

5. **Combining and Inspecting Data**
   - Concatenates the cleaned DataFrames from all banks into a single DataFrame.
   - Checks for missing values and inspects the combined data.

6. **Saving the Final Dataset**
   - Exports the fully cleaned and combined DataFrame to `all_reviews.csv` in the `data` directory.

---

## Key Scripts Utilized

- **`scrape_reviews.py`**: Automates scraping of Google Play Store reviews and saves them to CSV.
- **`load_csv.py`**: Loads CSV files into pandas DataFrames with error handling.
- **`clean_reviews_data.py`**: Cleans and standardizes review DataFrames.

---

## Example Usage in Notebook

```python
# Scrape reviews for a bank
from scripts.scrape_reviews import main as scrape_reviews
scrape_reviews(app_id="com.combanketh.mobilebanking", bank_name="CBE", total_reviews=400, lang="en", file_name="cbe_reviews.csv")

# Load reviews
from scripts.load_csv import load_reviews
cbe_reviews = load_reviews("cbe_reviews.csv")

# Clean reviews
from scripts.clean_reviews_data import clean_reviews
cbe_reviews_cleaned = clean_reviews(df=cbe_reviews, drop_columns=[...], rename_columns={...}, new_columns={...})
```

---

# Notebook: ```sentiment_and_thematic_analysis.ipynb```
## Sentiment and Thematic Analysis of Bank App Reviews

This notebook performs sentiment analysis and thematic keyword extraction on the cleaned and aggregated bank app reviews. It builds on the output of the data cleaning notebook and leverages additional utility scripts for advanced text analytics and visualization.

---

## Workflow Overview

1. **Setup and Imports**
   - Adds the project directory to `sys.path` for script imports.
   - Loads the combined reviews dataset.

2. **Text Preprocessing**
   - Uses the `ReviewPreprocessor` class from `text_preprocessor.py` to clean and tokenize review text.
   - Saves the preprocessed data for reproducibility.

3. **Sentiment Analysis**
   - Applies the `SentimentAnalyzer` from `sentiment_analysis.py` to assign sentiment labels and scores to each review.
   - Saves sentiment results and summary statistics by bank and rating.

4. **Visualization**
   - Utilizes the `PlotGenerator` class from `plot_generator.py` to visualize mean sentiment scores by bank and rating as a bar chart.

5. **Keyword Extraction**
   - Extracts top keywords from each review using the `extract_keywords` function from `extract_keywords.py`.
   - Saves the extracted keywords for further analysis.

6. **Thematic Mapping**
   - Maps extracted keywords to manually defined themes using `map_keywords_to_themes` from `map_keywords_with_themes.py`.
   - Retrieves example reviews for each theme using `get_examples_by_theme`.

---

## Key Scripts Utilized

- **`text_preprocessor.py`**: Cleans and tokenizes review text.
- **`sentiment_analysis.py`**: Performs sentiment analysis using VADER or TextBlob.
- **`plot_generator.py`**: Generates and saves bar chart visualizations.
- **`extract_keywords.py`**: Extracts top keywords from review text using TF-IDF.
- **`map_keywords_with_themes.py`**: Maps keywords to themes and retrieves example reviews per theme.

---

## Example Usage in Notebook

```python
# Preprocess text
from scripts.text_preprocessor import ReviewPreprocessor
pre_processor = ReviewPreprocessor()
df["cleaned_review"] = df["review"].apply(pre_processor.clean_text)
df["tokens"] = df["cleaned_review"].apply(pre_processor.tokenize_text)

# Sentiment analysis
from scripts.sentiment_analysis import SentimentAnalyzer
sentiment_analyzer = SentimentAnalyzer()
df["sentiment_label"], df["sentiment_score"] = zip(*df["cleaned_review"].apply(sentiment_analyzer.predict))

# Visualization
from scripts.plot_generator import PlotGenerator
plot_generator = PlotGenerator(df=summary_df)
plot_generator.plot_barchart(x_value="rating", y_value="mean_sentiment_score", hue="bank", ...)

# Keyword extraction
from scripts.extract_keywords import extract_keywords
df = extract_keywords(df=df, text_column="cleaned_review", top_n=50)

# Thematic mapping
from scripts.map_keywords_with_themes import map_keywords_to_themes, get_examples_by_theme
df['themes'] = df['keywords'].apply(lambda kws: map_keywords_to_themes(kws, keyword_theme_map))
examples = get_examples_by_theme(df=df)
```

---

## Notes

- The notebook is modular and can be extended to include more banks or additional cleaning steps.
- All intermediate and final datasets are saved in the `data` directory for reproducibility.
- Logging is enabled in all scripts for transparency and debugging.

---