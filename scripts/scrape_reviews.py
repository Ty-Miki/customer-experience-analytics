import logging
import pandas as pd
import time
from google_play_scraper import reviews, Sort

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GooglePlayReviewScraper:
    def __init__(self, app_id: str, bank_name: str, total_reviews: int, lang: str = 'en', file_name: str = None):
        self.app_id = app_id
        self.bank_name = bank_name
        self.total_reviews = total_reviews
        self.lang = lang
        self.file_name = file_name

    def fetch_reviews(self) -> list:
        """
        Fetches user reviews for a specified app from the Google Play Store.
        Returns a list of review dictionaries.
        """
        all_reviews = []
        token = None
        batch_size = 100

        while len(all_reviews) < self.total_reviews:
            count = min(batch_size, self.total_reviews - len(all_reviews))
            logging.info(f"Fetching {count} reviews... (collected so far: {len(all_reviews)})")

            result, token = reviews(
                self.app_id,
                lang=self.lang,
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

    def save_reviews_to_csv(self, reviews_list: list):
        """
        Saves a list of review dictionaries to a CSV file.
        """
        final_file = self.file_name or f"{self.bank_name}_reviews_{len(reviews_list)}.csv"
        df = pd.DataFrame(reviews_list)
        df.to_csv(final_file, index=False)
        logging.info(f"Saved reviews to {final_file}")

    def scrape_and_save(self):
        """
        Orchestrates fetching reviews and saving them to a CSV file.
        """
        try:
            logging.info(f"Starting review scrape for {self.bank_name} (App ID: {self.app_id})")
            all_reviews = self.fetch_reviews()
            self.save_reviews_to_csv(all_reviews)
        except Exception as e:
            logging.error(f"An error occurred while scraping: {str(e)}")

def main(app_id: str, bank_name: str, total_reviews: int, lang: str = 'en', file_name: str = None):
    scraper = GooglePlayReviewScraper(
        app_id=app_id,
        bank_name=bank_name,
        total_reviews=total_reviews,
        lang=lang,
        file_name=file_name
    )
    scraper.scrape_and_save()