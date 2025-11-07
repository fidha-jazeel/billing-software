import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "travel_billing.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Create Bills table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            ticket_no TEXT,
            supplier TEXT,
            total REAL,
            profit REAL,
            balance REAL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create Suppliers table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT
        )
    """)

    # Create Company Info table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS company_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            logo_path TEXT
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully!")
