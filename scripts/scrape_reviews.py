import logging
import pandas as pd
import time
from google_play_scraper import reviews, Sort

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_reviews(app_id: str, total_reviews: int, lang: str = 'en') -> list:
    """
    Fetches user reviews for a specified app from the Google Play Store.
    Returns a list of review dictionaries.
    """
    all_reviews = []
    token = None
    batch_size = 100

    while len(all_reviews) < total_reviews:
        count = min(batch_size, total_reviews - len(all_reviews))
        logging.info(f"Fetching {count} reviews... (collected so far: {len(all_reviews)})")

        result, token = reviews(
            app_id,
            lang=lang,
            sort=Sort.NEWEST,
            count=count,
            continuation_token=token
        )

        if not result:
            logging.warning("No more reviews returned from server.")
            break

        all_reviews.extend(result)
        time.sleep(1)  # Sleep to avoid rate limiting

    logging.info(f"Finished scraping. Total reviews collected: {len(all_reviews)}")
    return all_reviews

def save_reviews_to_csv(reviews_list: list, file_name: str):
    """
    Saves a list of review dictionaries to a CSV file.
    """
    df = pd.DataFrame(reviews_list)
    df.to_csv(file_name, index=False)
    logging.info(f"Saved reviews to {file_name}")

def scrape_reviews_to_csv(
    app_id: str,
    total_reviews: int,
    bank_name: str,
    file_name: str = None,
    lang: str = 'en',
):
    """
    Orchestrates fetching reviews and saving them to a CSV file.
    """
    try:
        logging.info(f"Starting review scrape for {bank_name} (App ID: {app_id})")
        all_reviews = fetch_reviews(app_id, total_reviews, lang)
        final_file = file_name or f"{bank_name}_reviews_{len(all_reviews)}.csv"
        save_reviews_to_csv(all_reviews, final_file)
    except Exception as e:
        logging.error(f"An error occurred while scraping: {str(e)}")