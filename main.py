from dotenv import dotenv_values
from scripts.oracle_utils.db_handler import OracleDBHandler
from scripts.load_csv import load_reviews

CREDENTIALS_PATH = "config/creds.env" # Chnage this path if you have .env file in other path

def create_table():

    banks_schema = {
    "bank_id": "NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
    "bank_name": "VARCHAR2(100) UNIQUE NOT NULL"
}

    reviews_schema = {
    "review_id": "VARCHAR2(100) PRIMARY KEY",
    "review_text": "CLOB",
    "rating": "NUMBER",
    "review_date": "DATE",
    "sentiment_label": "VARCHAR2(20)",
    "sentiment_score": "FLOAT",
    "keywords": "CLOB",
    "bank_id": "NUMBER",
    "CONSTRAINT fk_bank": "FOREIGN KEY (bank_id) REFERENCES banks(bank_id)"
}

    creds = dotenv_values(CREDENTIALS_PATH)

    handler = OracleDBHandler(
    user=creds.get("ORACLE_USER"),
    password=creds.get("ORACLE_PASSWORD"),
    host=creds.get("ORACLE_HOST"),
    port=int(creds.get("ORACLE_PORT")),
    service_name=creds.get("ORACLE_SERVICE_NAME")
)

    handler.create_table("banks", banks_schema)
    handler.create_table("reviews", {k: v for k, v in reviews_schema.items() if not k.startswith("CONSTRAINT")})
    handler.cursor.execute("""ALTER TABLE reviews ADD CONSTRAINT fk_bank FOREIGN KEY (bank_id) REFERENCES banks(bank_id)""")
    handler.connection.commit()

    handler.close()

def insert_data():
    sentiment_df = load_reviews(filepath="data/sentiment_output.csv")
    keyword_df = load_reviews(filepath="data/review_keywords.csv")
    print(keyword_df.head())

if __name__ == "__main__":
    insert_data()