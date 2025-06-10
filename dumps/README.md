## SQL Dump Files

The `dumps/` directory contains SQL dump files generated from the Oracle database using the provided utility scripts. These files include both the Data Definition Language (DDL) for table creation and the Data Manipulation Language (DML) for inserting data.

### 1. `local_banks_dump.sql`

**Contents:**
- DDL for creating the `local_banks` table, including primary key and unique constraints.
- DML statements to insert all bank records present at the time of the dump.

**Usage Example:**
```sql
-- Create the table
@dumps/local_banks_dump.sql
```

---

### 2. `bank_reviews_dump.sql`

**Contents:**
- DDL for creating the `bank_reviews` table, including primary key, foreign key constraints, and LOB storage for large text fields.
- DML statements to insert all review records present at the time of the dump.

**Usage Example:**
```sql
-- Create the table and insert data
@dumps/bank_reviews_dump.sql
```

---

**Notes:**
- These SQL files can be used to restore the database schema and data on another Oracle instance.
- Ensure that referenced tables (such as `local_banks`) are created before restoring dependent tables (such as `bank_reviews`).
- The dump files are generated using the `sql_dump.py` utility and reflect the state of the database at the time of export.

---