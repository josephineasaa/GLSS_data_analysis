**Check If Tables Exist (script guide)**

This file documents the small utility script `check_if_tables_exist.py` included in this repository. The script connects to a PostgreSQL database and checks whether a short list of tables exist in the `public` schema.

**Purpose:**
- Quickly verify presence of expected tables in a Postgres database before running downstream ETL or data-push scripts.

**What the script does:**
- Opens a connection to Postgres using `psycopg2` with connection parameters defined at the top of the script.
- Iterates over the `tables_to_check` list and runs a query against `pg_tables` to determine whether each table exists in the `public` schema.
- Prints: `Table <tablename> exists: <True|False>` for each table.

**Default tables checked (in the current script):**
- `GHA_2017_income`
- `GHA_2013_income`
- `GHA_2005_income`

**Requirements:**
- Python 3.7 or later.
- `psycopg2` or `psycopg2-binary`.

Install dependency (PowerShell / pwsh):

```powershell
pip install psycopg2-binary
```

**Usage:**
- From the repository root run:

```powershell
python check_if_tables_exist.py
```

**Configuration & security notes:**
- The script currently contains hard-coded connection credentials (`dbname`, `user`, `password`, `host`, `port`). Storing plaintext credentials in source files is unsafe for most workflows.
- Recommended alternatives:
  - Use environment variables and read them with `os.environ`.
  - Store credentials in a config file excluded via `.gitignore`.
  - Use a secrets manager if available in your environment.
- To check additional tables, update the `tables_to_check` list in `check_if_tables_exist.py` or run an updated script that accepts table names as CLI arguments.

**Example output:**

```
Table GHA_2017_income exists: True
Table GHA_2013_income exists: True
Table GHA_2005_income exists: False
```

**Next steps (optional improvements I can implement):**
- Replace hard-coded credentials with environment-variable support.
- Add a simple CLI (e.g., `--tables`) so you can pass table names at runtime.
- Return non-zero exit codes when missing tables are considered fatal (useful for CI checks).

Tell me which of the optional improvements you want and I will implement them (I can add env var support and a `--tables` CLI flag in one change).
