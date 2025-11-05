import sqlite3
from database.db import DB_PATH

class ReportController:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def get_total_sales(self):
        self.cursor.execute("SELECT SUM(quantity * price) FROM bills")
        return self.cursor.fetchone()[0] or 0
