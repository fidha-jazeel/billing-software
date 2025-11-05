# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
# import sqlite3
# from pathlib import Path

# DB_PATH = Path(__file__).resolve().parent / "database" / "travel_billing.db"

# class BillingWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Billing Form")
#         self.resize(400, 300)

#         layout = QVBoxLayout()

#         self.customer = QLineEdit()
#         self.customer.setPlaceholderText("Customer Name")
#         layout.addWidget(self.customer)

#         self.item = QLineEdit()
#         self.item.setPlaceholderText("Item Name")
#         layout.addWidget(self.item)

#         self.quantity = QLineEdit()
#         self.quantity.setPlaceholderText("Quantity")
#         layout.addWidget(self.quantity)

#         self.price = QLineEdit()
#         self.price.setPlaceholderText("Price")
#         layout.addWidget(self.price)

#         save_btn = QPushButton("Save Bill")
#         save_btn.clicked.connect(self.save_bill)
#         layout.addWidget(save_btn)

#         self.msg = QLabel("")
#         layout.addWidget(self.msg)

#         self.setLayout(layout)

#     def save_bill(self):
#         conn = sqlite3.connect(DB_PATH)
#         cur = conn.cursor()
#         cur.execute("INSERT INTO bills (customer_name, item_name, quantity, price, total) VALUES (?, ?, ?, ?, ?)",
#                     (self.customer.text(), self.item.text(), int(self.quantity.text()), float(self.price.text()),
#                      int(self.quantity.text()) * float(self.price.text())))
#         conn.commit()
#         conn.close()
#         self.msg.setText("✅ Bill Saved Successfully!")
# import sqlite3
# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
# from PyQt6.QtCore import Qt

# class BillingWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Billing System")
#         self.resize(700, 400)

#         layout = QVBoxLayout()

#         # Title
#         title = QLabel("🧾 Billed Item/s List")
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(title)

#         # Table for items
#         self.table = QTableWidget(3, 5)  # 3 rows, 5 columns
#         self.table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Price/Unit (₹)", "Tax (%)", "Amount (₹)"])
#         layout.addWidget(self.table)

#         # Save Button
#         save_btn = QPushButton("💾 Save")
#         save_btn.clicked.connect(self.save_data)
#         layout.addWidget(save_btn)

#         self.setLayout(layout)

#     def save_data(self):
#         conn = sqlite3.connect("travel_agency.db")
#         cur = conn.cursor()
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS bills (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 item_name TEXT,
#                 quantity INTEGER,
#                 price REAL,
#                 tax REAL,
#                 amount REAL
#             )
#         """)

#         for row in range(self.table.rowCount()):
#             item_name = self.table.item(row, 0)
#             qty = self.table.item(row, 1)
#             price = self.table.item(row, 2)
#             tax = self.table.item(row, 3)
#             amount = self.table.item(row, 4)

#             if item_name and qty and price and amount:
#                 cur.execute("INSERT INTO bills (item_name, quantity, price, tax, amount) VALUES (?, ?, ?, ?, ?)",
#                             (item_name.text(), qty.text(), price.text(), tax.text() if tax else 0, amount.text()))

#         conn.commit()
#         conn.close()
#         QMessageBox.information(self, "Success", "Bill Saved Successfully!")
#     # billing_window.py
# import sqlite3
# from pathlib import Path
# from PyQt6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#     QTableWidget, QTableWidgetItem, QPushButton,
#     QMessageBox
# )
# from database.db import DB_PATH  # reuse same path

# class BillingWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Billing System")
#         self.resize(600, 400)

#         layout = QVBoxLayout()
#         layout.addWidget(QLabel("🧾 Billed Item's List"))

#         # create table
#         self.table = QTableWidget(3, 5)
#         self.table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Price/Unit (₹)", "Tax (%)", "Amount (₹)"])
#         layout.addWidget(self.table)

#         # Save button
#         save_btn = QPushButton("💾 Save")
#         save_btn.clicked.connect(self.save_bill)
#         layout.addWidget(save_btn)

#         self.setLayout(layout)

#     def save_bill(self):
#         """Save all rows to database"""
#         conn = sqlite3.connect(DB_PATH)
#         cur = conn.cursor()

#         for row in range(self.table.rowCount()):
#             item = self.table.item(row, 0)
#             qty = self.table.item(row, 1)
#             price = self.table.item(row, 2)
#             tax = self.table.item(row, 3)
#             amt = self.table.item(row, 4)

#             if item and qty and price:  # skip empty rows
#                 cur.execute("""
#                     INSERT INTO bills (customer_name, item_name, quantity, price, tax, date)
#                     VALUES (?, ?, ?, ?, ?, DATE('now'))
#                 """, (
#                     "Walk-in Customer",  # later you can add a textbox for name
#                     item.text(),
#                     int(qty.text()),
#                     float(price.text()),
#                     float(tax.text()) if tax else 0
#                 ))

#         conn.commit()
#         conn.close()
#         QMessageBox.information(self, "Saved", "✅ Bill saved successfully!")
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from database.ui.models.controllers.billing_controller import BillingController
from database.ui.models.transaction import Transaction

class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Billing System")
        self.resize(600, 400)
        self.controller = BillingController()

        layout = QVBoxLayout()

        # Table
        self.table = QTableWidget(3, 5)
        self.table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Price/Unit (₹)", "Tax (%)", "Amount (₹)"])
        layout.addWidget(self.table)

        # Save button
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.save_billing)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save_billing(self):
        """Collect data from table and save into DB"""
        try:
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 0)
                if item and item.text().strip():
                    tx = Transaction(
                        customer_name="Walk-in",
                        item_name=item.text(),
                        quantity=int(self.table.item(row, 1).text()),
                        price=float(self.table.item(row, 2).text()),
                        tax=float(self.table.item(row, 3).text())
                    )
                    self.controller.add_transaction(tx)
            QMessageBox.information(self, "Success", "Bills saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
