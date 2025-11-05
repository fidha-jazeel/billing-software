# import sqlite3
# from pathlib import Path

# DB_PATH = Path(__file__).resolve().parent / "travel_billing.db"

# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()

#     # Bills table
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS bills (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         customer_name TEXT NOT NULL,
#         item_name TEXT,
#         quantity INTEGER,
#         price REAL,
#         tax REAL,
#         total REAL,
#         date TEXT
#     )
#     """)

#     # Login PIN table
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS pin_table (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         pin TEXT NOT NULL
#     )
#     """)

#     # Add default pin if not exists
#     cur.execute("SELECT COUNT(*) FROM pin_table")
#     if cur.fetchone()[0] == 0:
#         cur.execute("INSERT INTO pin_table (pin) VALUES ('1234')")

#     conn.commit()
#     conn.close()
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "travel_billing.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ✅ Create table for PIN login
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pin_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pin TEXT NOT NULL
        )
    """)

    # ✅ Insert default pin (only once)
    cur.execute("SELECT COUNT(*) FROM pin_table")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO pin_table (pin) VALUES ('1234')")

    # ✅ Create Bills table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            item_name TEXT,
            quantity INTEGER,
            price REAL,
            tax REAL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully with pin_table and bills table!")
