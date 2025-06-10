import os
from datetime import datetime
from db_handler import OracleDBHandler

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def dump_table_to_sql(handler: OracleDBHandler, table_name: str, output_dir: str = "dumps") -> str:
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{table_name}_dump.sql")

    with open(output_path, "w", encoding="utf-8") as f:
        # === Step 1: Get table DDL using DBMS_METADATA ===
        try:
            handler.cursor.execute(
                f"SELECT DBMS_METADATA.GET_DDL('TABLE', UPPER(:1)) FROM dual", [table_name]
            )
            ddl = handler.cursor.fetchone()[0].read()
            f.write(f"-- Table DDL for {table_name}\n")
            f.write(ddl)
            f.write(";\n\n")
        except Exception as e:
            logging.error(f"Failed to get DDL for table {table_name}: {e}")
            return ""

        # === Step 2: Dump data ===
        try:
            handler.cursor.execute(f'SELECT * FROM "{table_name}"')
            columns = [col[0] for col in handler.cursor.description]
            rows = handler.cursor.fetchall()

            f.write(f"-- Data for {table_name}\n")
            for row in rows:
                values = []
                for val in row:
                    if val is None:
                        values.append("NULL")
                    elif isinstance(val, (int, float)):
                        values.append(str(val))
                    elif isinstance(val, str):
                        safe_val = val.replace("'", "''")
                        values.append(f"'{safe_val}'")
                    elif isinstance(val, datetime.datetime):
                        values.append(f"TO_DATE('{val.strftime('%Y-%m-%d %H:%M:%S')}', 'YYYY-MM-DD HH24:MI:SS')")
                    else:
                        # fallback for anything weird (like CLOB)
                        values.append(f"'{str(val).replace('\'', '\'\'')}'")

                insert_stmt = f'INSERT INTO "{table_name}" ({", ".join(columns)}) VALUES ({", ".join(values)});'
                f.write(insert_stmt + "\n")

        except Exception as e:
            logging.error(f"Failed to dump data for table {table_name}: {e}")
            return ""

    logging.info(f"SQL dump for {table_name} written to: {output_path}")
    return output_path

if __name__ == "__main__":
    from dotenv import dotenv_values

    CREDENTIALS_PATH = "config/creds.env"

    creds = dotenv_values(CREDENTIALS_PATH)
    handler = OracleDBHandler(
        user=creds.get("ORACLE_USER"),
        password=creds.get("ORACLE_PASSWORD"),
        host=creds.get("ORACLE_HOST"),
        port=int(creds.get("ORACLE_PORT")),
        service_name=creds.get("ORACLE_SERVICE_NAME")
    )

    try:
        dump_table_to_sql(handler, "local_banks")
        dump_table_to_sql(handler, "bank_reviews")
    finally:
        handler.close()