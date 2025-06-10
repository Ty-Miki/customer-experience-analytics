from dotenv import dotenv_values
from db_handler import OracleDBHandler

CREDENTIALS_PATH = "config/creds.env" 

def create_table():
    # Define table schemas
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
        "CONSTRAINT fk_bank": "FOREIGN KEY (bank_id) REFERENCES local_banks(bank_id)"
    }

    # Load credentials
    creds = dotenv_values(CREDENTIALS_PATH)

    # Set up DB handler
    handler = OracleDBHandler(
        user=creds.get("ORACLE_USER"),
        password=creds.get("ORACLE_PASSWORD"),
        host=creds.get("ORACLE_HOST"),
        port=int(creds.get("ORACLE_PORT")),
        service_name=creds.get("ORACLE_SERVICE_NAME")
    )

    try:
        # Drop tables if they exist
        handler.drop_table_if_exists("bank_reviews")
        handler.drop_table_if_exists("local_banks")

        # Create tables
        handler.create_table("local_banks", banks_schema)
        handler.create_table("bank_reviews", reviews_schema)

    finally:
        handler.close()


if __name__ == "__main__":
    create_table()
    print("Tables created successfully.")