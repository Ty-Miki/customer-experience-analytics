from dotenv import dotenv_values
from scripts.oracle_utils.db_handler import OracleDBHandler
from scripts.load_csv import load_reviews
import pandas as pd
import cx_Oracle

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CREDENTIALS_PATH = "config/creds.env" # Chnage this path if you have .env file in other path


if __name__ == "__main__":
    # === 1. Load & Prepare Data ===
    sentiment_df = load_reviews("data/sentiment_output.csv")
    keywords_df = load_reviews("data/review_keywords.csv")

    sentiment_df["date"] = pd.to_datetime(sentiment_df["date"])
    
    df_combined = sentiment_df.merge(keywords_df, on="reviewId", how="left")
    df_combined.drop(columns=["cleaned_review_x", "Unnamed: 0"], inplace=True)
    df_combined.rename(columns={
        "cleaned_review_y": "review_text",
        "reviewId": "review_id",
        "date": "review_date"
    }, inplace=True)
    df_combined["keywords"] = df_combined["keywords"].apply(lambda x: str(x) if not pd.isnull(x) else None)
    df_combined["review_text"] = df_combined["review_text"].apply(lambda x: str(x) if not pd.isnull(x) else None)


    # === 2. Setup DB Connection ===
    creds = dotenv_values(CREDENTIALS_PATH)
    handler = OracleDBHandler(
        user=creds.get("ORACLE_USER"),
        password=creds.get("ORACLE_PASSWORD"),
        host=creds.get("ORACLE_HOST"),
        port=int(creds.get("ORACLE_PORT")),
        service_name=creds.get("ORACLE_SERVICE_NAME")
    )

    try:
        # === 3. Insert banks into `local_banks` table ===
        banks = ["CBE", "Dashen", "BOA"]
        for bank in banks:
            try:
                handler.cursor.execute("INSERT INTO local_banks (bank_name) VALUES (:1)", [bank])
                logging.info(f"Inserted bank: {bank}")
            except cx_Oracle.IntegrityError:
                logging.info(f"Bank '{bank}' already exists, skipping.")

        handler.connection.commit()

        # === 4. Fetch bank_id map ===
        handler.cursor.execute("SELECT bank_id, bank_name FROM local_banks")
        bank_map = {name: bank_id for bank_id, name in handler.cursor.fetchall()}
        logging.info(f"Bank map: {bank_map}")

        # === 5. Map bank name to bank_id ===
        df_combined["bank_id"] = df_combined["bank"].map(bank_map)

        # Check for unmapped banks
        if df_combined["bank_id"].isnull().any():
            unmapped = df_combined[df_combined["bank_id"].isnull()]["bank"].unique()
            logging.warning(f"Some bank names could not be mapped to bank_id: {unmapped}")

        df_combined.drop(columns=["bank"], inplace=True)

        # === 6. Final sanity check ===
        logging.info(f"Final DataFrame shape: {df_combined.shape}")
        print(df_combined.head())

        # === 7. Insert data into `bank_reviews` ===
        handler.insert_dataframe(df_combined, "bank_reviews")

    finally:
        # === 8. Close DB connection ===
        handler.close()
