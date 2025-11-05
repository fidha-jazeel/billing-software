import sqlite3
from database.db import DB_PATH
from models.transaction import Transaction

class BillingController:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def add_transaction(self, tx: Transaction):
        """Insert a new billing record into the database"""
        self.cursor.execute("""
            INSERT INTO bills (customer_name, item_name, quantity, price, tax)
            VALUES (?, ?, ?, ?, ?)
        """, (tx.customer_name, tx.item_name, tx.quantity, tx.price, tx.tax))
        self.conn.commit()

    def get_all_bills(self):
        """Fetch all bills"""
        self.cursor.execute("SELECT * FROM bills")
        return self.cursor.fetchall()
