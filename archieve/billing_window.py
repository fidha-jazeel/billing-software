
# import sqlite3
# from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
# from PyQt6.QtGui import QFont
# from PyQt6.QtCore import Qt

# class BillingWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Agency Billing")
#         self.resize(500, 400)
#         self.setStyleSheet("background-color: #f9f9f9; color: #333;")

#         layout = QVBoxLayout()

#         title = QLabel("🧾 Create New Bill")
#         title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(title)

#         # Input fields
#         self.customer_name = QLineEdit()
#         self.customer_name.setPlaceholderText("Customer Name")
#         layout.addWidget(self.customer_name)

#         self.destination = QLineEdit()
#         self.destination.setPlaceholderText("Destination")
#         layout.addWidget(self.destination)

#         self.travel_date = QLineEdit()
#         self.travel_date.setPlaceholderText("Travel Date (YYYY-MM-DD)")
#         layout.addWidget(self.travel_date)

#         self.amount = QLineEdit()
#         self.amount.setPlaceholderText("Amount (₹)")
#         layout.addWidget(self.amount)

#         # Save button
#         save_button = QPushButton("Save Bill")
#         save_button.clicked.connect(self.save_bill)
#         layout.addWidget(save_button)

#         self.setLayout(layout)

#     def save_bill(self):
#         name = self.customer_name.text()
#         destination = self.destination.text()
#         date = self.travel_date.text()
#         amount = self.amount.text()

#         if not (name and destination and date and amount):
#             QMessageBox.warning(self, "Error", "Please fill all fields!")
#             return

#         conn = sqlite3.connect("travel_agency.db")
#         cur = conn.cursor()
#         cur.execute("INSERT INTO bills (customer_name, destination, travel_date, amount) VALUES (?, ?, ?, ?)",
#                     (name, destination, date, amount))
#         conn.commit()
#         conn.close()

#         QMessageBox.information(self, "Success", "✅ Bill saved successfully!")
#         self.customer_name.clear()
#         self.destination.clear()
#         self.travel_date.clear()
#         self.amount.clear()
import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency Billing")
        self.resize(400, 300)

        layout = QVBoxLayout()

        # Input fields
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Customer Name")
        layout.addWidget(self.customer_name)

        self.destination = QLineEdit()
        self.destination.setPlaceholderText("Destination")
        layout.addWidget(self.destination)

        self.travel_date = QLineEdit()
        self.travel_date.setPlaceholderText("Travel Date (YYYY-MM-DD)")
        layout.addWidget(self.travel_date)

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Amount")
        layout.addWidget(self.amount)

        # Save button
        save_button = QPushButton("Save Bill")
        save_button.clicked.connect(self.save_bill)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_bill(self):
        name = self.customer_name.text()
        destination = self.destination.text()
        date = self.travel_date.text()
        amount = self.amount.text()

        # Save to SQLite database
        conn = sqlite3.connect("travel_agency.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                destination TEXT,
                travel_date TEXT,
                amount REAL
            )
        """)
        cur.execute("INSERT INTO bills (customer_name, destination, travel_date, amount) VALUES (?, ?, ?, ?)",
                    (name, destination, date, amount))
        conn.commit()
        conn.close()

        # Success message
        QMessageBox.information(self, "Success", "✅ Bill saved successfully!")

        # Clear inputs
        self.customer_name.clear()
        self.destination.clear()
        self.travel_date.clear()
        self.amount.clear()

import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

DB_NAME = "travel_agency.db"

class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing Window")
        self.setGeometry(300, 200, 400, 250)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Customer Name")
        layout.addWidget(self.name_input)

        self.destination_input = QLineEdit()
        self.destination_input.setPlaceholderText("Destination")
        layout.addWidget(self.destination_input)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Travel Date (YYYY-MM-DD)")
        layout.addWidget(self.date_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        layout.addWidget(self.amount_input)

        save_button = QPushButton("Save Bill")
        save_button.clicked.connect(self.save_bill)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_bill(self):
        name = self.name_input.text()
        destination = self.destination_input.text()
        date = self.date_input.text()
        amount = self.amount_input.text()

        if not name or not destination or not date or not amount:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO bills (customer_name, destination, travel_date, amount) VALUES (?, ?, ?, ?)",
                    (name, destination, date, amount))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Bill saved successfully!")
        self.name_input.clear()
        self.destination_input.clear()
        self.date_input.clear()
        self.amount_input.clear()
def open_billing(self):
    self.billing = BillingWindow()
    self.billing.show()
    self.close()


        
