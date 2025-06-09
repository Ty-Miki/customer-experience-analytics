import cx_Oracle

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OracleDBHandler:
    def __init__(self, user, password, host, port, service_name):
        try:
            dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
            self.connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
            self.cursor = self.connection.cursor()
            logging.info("Successfully connected to Oracle DB.")
        except cx_Oracle.Error as e:
            logging.error(f"Database connection failed: {e}")
            raise

    def create_table(self, table_name, schema_dict):
        """
        Creates a table with the given name and schema.

        :param table_name: str, name of the table to create
        :param schema_dict: dict, column definitions {col_name: data_type}
        """
        try:
            # Step 1: Construct CREATE TABLE SQL
            columns = []
            for col_name, data_type in schema_dict.items():
                columns.append(f'"{col_name}" {data_type}')  # Use double quotes for safety
            column_definitions = ", ".join(columns)
            create_sql = f'CREATE TABLE "{table_name}" ({column_definitions})'

            # Step 2: Execute SQL
            self.cursor.execute(create_sql)
            self.connection.commit()
            logging.info(f"Table '{table_name}' created successfully.")

        except cx_Oracle.DatabaseError as e:
            error_obj, = e.args
            if error_obj.code == 955:  # ORA-00955: name is already used by an existing object
                logging.error(f"Table '{table_name}' already exists.")
            else:
                logging.error(f"Error creating table '{table_name}': {e}")
            raise

        except Exception as e:
            logging.error(f"Unexpected error during table creation: {e}")
            raise

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            logging.info("Database connection closed.")
        except Exception as e:
            logging.error(f"Error while closing the connection: {e}")

