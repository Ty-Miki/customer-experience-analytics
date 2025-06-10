## Oracle Database Utilities

This set of scripts provides utilities for managing Oracle database tables, loading data from pandas DataFrames, and exporting table data to SQL files. These utilities are designed to support robust data storage, integration, and backup for analytics workflows.

### 1. `db_handler.py`

**Purpose:**  
Provides the `OracleDBHandler` class for connecting to an Oracle database, creating and dropping tables, inserting DataFrame data in batches, and safely closing connections.

**Key Features:**
- Establishes and manages Oracle DB connections using credentials.
- Creates tables with flexible schema definitions.
- Drops tables if they exist, with error handling for non-existent tables.
- Inserts data from pandas DataFrames in configurable batch sizes, with batch error logging.
- Closes database connections cleanly.

**Usage Example:**
```python
from scripts.oracle_utils.db_handler import OracleDBHandler

handler = OracleDBHandler(user, password, host, port, service_name)
handler.create_table("my_table", {"id": "NUMBER PRIMARY KEY", "name": "VARCHAR2(100)"})
handler.insert_dataframe(df, "my_table")
handler.drop_table_if_exists("my_table")
handler.close()
```

---

### 2. `create_tables.py`

**Purpose:**  
Defines and creates the required database tables for the project, including schema for banks and reviews, and sets up foreign key relationships.

**Key Features:**
- Loads Oracle credentials from a `.env` file.
- Drops existing tables to ensure a clean setup.
- Creates `local_banks` and `bank_reviews` tables with appropriate data types and constraints.
- Can be run as a standalone script to initialize the database schema.

**Usage Example:**
```python
# Run as a script to create tables
python scripts/oracle_utils/create_tables.py
```

---

### 3. `sql_dump.py`

**Purpose:**  
Exports the structure and data of Oracle tables to SQL files for backup or migration.

**Key Features:**
- Dumps table DDL (structure) using Oracle’s `DBMS_METADATA`.
- Exports all table data as SQL `INSERT` statements, handling various data types.
- Organizes dumps in a specified output directory.
- Can be run as a script to dump multiple tables.

**Usage Example:**
```python
from scripts.oracle_utils.db_handler import OracleDBHandler
from scripts.oracle_utils.sql_dump import dump_table_to_sql

handler = OracleDBHandler(user, password, host, port, service_name)
dump_table_to_sql(handler, "bank_reviews", output_dir="dumps")
handler.close()
```
Or run as a script:
```sh
python scripts/oracle_utils/sql_dump.py
```

---

## Notes

- All utilities use Python logging for status and error reporting.
- Designed for modular use in ETL/data engineering pipelines.
- Ensure Oracle client libraries and credentials are properly configured before use.
- Table schemas and credentials can be customized as needed for your environment.

---