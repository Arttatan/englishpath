"""
Runs one or more .sql files against the Supabase Postgres database.

Usage (PowerShell):
    $env:SUPA_DB_URL = "postgresql://...:PASSWORD@...pooler.supabase.com:6543/postgres"
    python database/run_sql.py database/schema.sql database/make-admin.sql database/seed-sample.sql

The connection string is read from the SUPA_DB_URL environment variable, so the
password is never hard-coded into the project files.
"""

import os
import sys

try:
    import psycopg2
except ImportError:
    print("The 'psycopg2-binary' package is not installed. Run: python -m pip install psycopg2-binary")
    sys.exit(1)


def main():
    db_url = os.environ.get("SUPA_DB_URL")
    if not db_url:
        print("ERROR: environment variable SUPA_DB_URL is not set.")
        sys.exit(1)

    files = sys.argv[1:]
    if not files:
        print("ERROR: pass one or more .sql files to run.")
        sys.exit(1)

    conn = psycopg2.connect(db_url, sslmode="require", connect_timeout=15)
    conn.autocommit = True
    try:
        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                sql = f.read()
            print(f"\n--- Running {path} ---")
            with conn.cursor() as cur:
                cur.execute(sql)
                # Print any result rows from the last statement (e.g. the admin check)
                if cur.description:
                    for row in cur.fetchall():
                        print(row)
            print(f"--- OK: {path} ---")
    finally:
        conn.close()

    print("\nAll done.")


if __name__ == "__main__":
    main()
