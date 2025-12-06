import sqlite3
import pandas as pd
import os

def sqlite_to_csv(db_path, output_folder="sqlite_csv_output"):
    # Create output folder if not exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Connect to SQLite DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in database.")
        return

    # Convert each table to CSV
    for table_name in tables:
        table = table_name[0]
        print(f"Exporting table: {table}")

        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        csv_path = os.path.join(output_folder, f"{table}.csv")
        df.to_csv(csv_path, index=False)

    conn.close()
    print(f"\n✔ Export complete! CSV files saved in: {output_folder}")

# Usage
sqlite_to_csv("../travel_billing_software/billing.db")
