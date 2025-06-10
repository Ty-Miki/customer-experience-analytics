# customer-experience-analytics

Analysis of customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank.

## Project Overview

This project implements a full data pipeline for customer experience analytics, including:
- Automated scraping of Google Play Store reviews for selected banking apps.
- Data cleaning, preprocessing, and aggregation using modular Python scripts and Jupyter notebooks.
- Sentiment analysis and thematic keyword extraction to identify satisfaction drivers and pain points.
- Visualization of sentiment trends and thematic mapping of user feedback.
- Storage of processed data in an Oracle database for further analysis and reporting.

## Directory Structure

- `scripts/` – Core data processing, analysis, and utility scripts.
- `notebooks/` – Jupyter notebooks for data cleaning, analysis, and visualization.
- `data/` – Input and output datasets.
- `tests/` – Automated tests for scripts and utilities.
- `config/` – Configuration files (e.g., database credentials).
- `main.py` – Project entry point for preparing and loading data into the Oracle database.

---

## Script: `main.py`

**Purpose:**  
Prepares the final DataFrame by merging sentiment and keyword analysis results, maps bank names to IDs, and loads the processed data into the Oracle database.

**Key Steps:**
1. **Load Data:**  
   - Loads sentiment analysis results and keyword extraction results from CSV files.
   - Merges the two DataFrames on the review ID.
   - Cleans and renames columns for consistency.

2. **Database Connection:**  
   - Loads Oracle credentials from a `.env` file.
   - Establishes a connection using the `OracleDBHandler` utility.

3. **Bank Table Population:**  
   - Inserts unique bank names into the `local_banks` table, skipping duplicates.
   - Fetches the mapping of bank names to their corresponding IDs.

4. **Data Preparation:**  
   - Maps each review’s bank name to its `bank_id`.
   - Drops the original bank name column and performs a final sanity check.

5. **Data Insertion:**  
   - Inserts the prepared DataFrame into the `bank_reviews` table in the Oracle database.

6. **Cleanup:**  
   - Closes the database connection.

**Usage Example:**
```sh
python main.py
```