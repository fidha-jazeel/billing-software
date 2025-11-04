
import sqlite3


# Connect to or create the database file
conn = sqlite3.connect("travel_agency.db")

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Create table (without # comments inside the SQL command)
cur.execute("""
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    destination TEXT,
    travel_date TEXT,
    amount REAL
)
""")

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()

print("✅ Database & Table created successfully!")
import sqlite3

def create_pin_table():
    conn = sqlite3.connect("travel_agency.db")
    cur = conn.cursor()

    # Create table for PIN if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pin_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pin TEXT NOT NULL
    )
    """)

    # Insert default PIN only if table is empty
    cur.execute("SELECT COUNT(*) FROM pin_table")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO pin_table (pin) VALUES ('1234')")

    conn.commit()
    conn.close()

create_pin_table()
print("✅ PIN table created successfully!")
import sqlite3

def check_pin(self):
    entered_pin = self.pin_box.text()

    conn = sqlite3.connect("travel_agency.db")
    cur = conn.cursor()
    cur.execute("SELECT pin FROM pin_table LIMIT 1")
    correct_pin = cur.fetchone()[0]
    conn.close()

    if entered_pin == correct_pin:
        self.feedback.setText("✅ Login Successful!")
        self.feedback.setStyleSheet("color: green;")
        self.open_billing()# Open billing window here
    else:
        self.feedback.setText("❌ Incorrect PIN. Try again.")
        self.feedback.setStyleSheet("color: red;")
# def open_billing(self):
#     self.billing = BillingWindow()
#     self.billing.show()
def open_billing(self):
    print("Billing window function called!")  # test
    self.billing = BillingWindow()
    self.billing.show()


# Removed interactive PIN-update prompt to avoid blocking the GUI startup.
# If you need to change the PIN programmatically, call update_pin(new_pin) from code.
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
# from PyQt6.QtGui import QFont
# from PyQt6.QtCore import Qt
# import sys
# import sqlite3

# class LoginWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Agency Login")
#         self.resize(400, 250)

#         layout = QVBoxLayout()

#         title = QLabel("Enter PIN to Login")
#         title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(title)

#         self.pin_box = QLineEdit()
#         self.pin_box.setPlaceholderText("Enter 4-digit PIN")
#         self.pin_box.setEchoMode(QLineEdit.EchoMode.Password)
#         layout.addWidget(self.pin_box)

#         login_btn = QPushButton("Login")
#         login_btn.clicked.connect(self.check_pin)
#         layout.addWidget(login_btn)

#         self.setLayout(layout)

#     def check_pin(self):
#         pin = self.pin_box.text()
#         if pin == "1234":  # 🔒 You can change the PIN
#             self.billing = BillingWindow()
#             self.billing.show()
#             self.close()
#         else:
#             QMessageBox.warning(self, "Error", "Incorrect PIN!")

# # 🧾 Billing Window
# class BillingWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Billing System")
#         self.resize(400, 300)

#         layout = QVBoxLayout()

#         self.name_input = QLineEdit()
#         self.name_input.setPlaceholderText("Customer Name")
#         layout.addWidget(self.name_input)

#         self.dest_input = QLineEdit()
#         self.dest_input.setPlaceholderText("Destination")
#         layout.addWidget(self.dest_input)

#         self.date_input = QLineEdit()
#         self.date_input.setPlaceholderText("Travel Date (DD-MM-YYYY)")
#         layout.addWidget(self.date_input)

#         self.amount_input = QLineEdit()
#         self.amount_input.setPlaceholderText("Amount")
#         layout.addWidget(self.amount_input)

#         save_btn = QPushButton("Save Bill")
#         save_btn.clicked.connect(self.save_data)
#         layout.addWidget(save_btn)

#         self.setLayout(layout)

#     def save_data(self):
#         name = self.name_input.text()
#         dest = self.dest_input.text()
#         date = self.date_input.text()
#         amount = self.amount_input.text()

#         if not (name and dest and date and amount):
#             QMessageBox.warning(self, "Error", "Please fill all fields!")
#             return

#         conn = sqlite3.connect("travel_agency.db")
#         cur = conn.cursor()
#         cur.execute("INSERT INTO bills (customer_name, destination, travel_date, amount) VALUES (?, ?, ?, ?)",
#                     (name, dest, date, amount))
#         conn.commit()
#         conn.close()

#         QMessageBox.information(self, "Success", "✅ Bill saved successfully!")

#         # Clear inputs
#         self.name_input.clear()
#         self.dest_input.clear()
#         self.date_input.clear()
#         self.amount_input.clear()


# # Run app
# app = QApplication(sys.argv)
# window = LoginWindow()
# window.show()
# sys.exit(app.exec())
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys
import sqlite3

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency Login")
        self.resize(400, 250)

        layout = QVBoxLayout()

        title = QLabel("Enter PIN to Login")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.pin_box = QLineEdit()
        self.pin_box.setPlaceholderText("Enter 4-digit PIN")
        self.pin_box.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pin_box)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.check_pin)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def check_pin(self):
        pin = self.pin_box.text()
        if pin == "1234":  # 🔒 You can change the PIN
            self.billing = BillingWindow()
            self.billing.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Incorrect PIN!")

# 🧾 Billing Window
class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Billing System")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Customer Name")
        layout.addWidget(self.name_input)

        self.dest_input = QLineEdit()
        self.dest_input.setPlaceholderText("Destination")
        layout.addWidget(self.dest_input)

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Travel Date (DD-MM-YYYY)")
        layout.addWidget(self.date_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        layout.addWidget(self.amount_input)

        save_btn = QPushButton("Save Bill")
        save_btn.clicked.connect(self.save_data)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_data(self):
        name = self.name_input.text()
        dest = self.dest_input.text()
        date = self.date_input.text()
        amount = self.amount_input.text()

        if not (name and dest and date and amount):
            QMessageBox.warning(self, "Error", "Please fill all fields!")
            return

        conn = sqlite3.connect("travel_agency.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO bills (customer_name, destination, travel_date, amount) VALUES (?, ?, ?, ?)",
                    (name, dest, date, amount))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "✅ Bill saved successfully!")

        # Clear inputs
        self.name_input.clear()
        self.dest_input.clear()
        self.date_input.clear()
        self.amount_input.clear()


# Run app
app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec())
import sqlite3

def check_pin(self):
    entered_pin = self.pin_box.text()

    conn = sqlite3.connect("travel_agency.db")
    cur = conn.cursor()
    cur.execute("SELECT pin FROM pin_table LIMIT 1")
    correct_pin = cur.fetchone()[0]
    conn.close()

    if entered_pin == correct_pin:
        self.feedback.setText("✅ Login Successful!")
        self.feedback.setStyleSheet("color: green;")
        # Open billing window here
    else:
        self.feedback.setText("❌ Incorrect PIN. Try again.")
        self.feedback.setStyleSheet("color: red;")
import sqlite3

new_pin = input("Enter new PIN: ")

conn = sqlite3.connect("travel_agency.db")
cur = conn.cursor()
cur.execute("UPDATE pin_table SET pin = ?", (new_pin,))
conn.commit()
conn.close()

print("✅ PIN updated successfully!")
import sqlite3

def check_pin(self):
    entered_pin = self.pin_box.text()

    # Connect to the SQLite database
    conn = sqlite3.connect("travel_agency.db")
    cur = conn.cursor()

    # Read the stored PIN from the pin_table
    cur.execute("SELECT pin FROM pin_table LIMIT 1")
    correct_pin = cur.fetchone()[0]

    # Close the connection
    conn.close()

    # Compare entered PIN with database PIN
    if entered_pin == correct_pin:
        self.feedback.setText("✅ Login Successful!")
        self.feedback.setStyleSheet("color: green;")
        # 🔹 Open billing window here in the next step
    else:
        self.feedback.setText("❌ Incorrect PIN. Try again.")
        self.feedback.setStyleSheet("color: red;")
import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class BillingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency Billing")
        self.resize(500, 400)
        self.setStyleSheet("background-color: #f5f5f5; color: #333;")

        layout = QVBoxLayout()

        # Title
        title = QLabel("🧾 Travel Agency Billing")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Input fields
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Customer Name")
        layout.addWidget(self.customer_name)

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Amount")
        layout.addWidget(self.amount)

        self.date = QLineEdit()
        self.date.setPlaceholderText("Date (YYYY-MM-DD)")
        layout.addWidget(self.date)

        # Save button
        save_btn = QPushButton("Save Bill")
        save_btn.clicked.connect(self.save_bill)
        layout.addWidget(save_btn)

        # Feedback
        self.feedback = QLabel("")
        self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback)

        self.setLayout(layout)

        # Create table if not exists
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect("travel_agency.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                amount REAL,
                date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_bill(self):
        name = self.customer_name.text()
        amt = self.amount.text()
        date = self.date.text()

        if name == "" or amt == "" or date == "":
            self.feedback.setText("⚠️ Please fill all fields.")
            self.feedback.setStyleSheet("color: red;")
            return

        conn = sqlite3.connect("travel_agency.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO bills (customer_name, amount, date) VALUES (?, ?, ?)", (name, amt, date))
        conn.commit()
        conn.close()

        self.feedback.setText("✅ Bill Saved Successfully!")
        self.feedback.setStyleSheet("color: green;")

        # Clear fields
        self.customer_name.clear()
        self.amount.clear()
        self.date.clear()
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import sys
from billing_window import BillingWindow   # ✅ import the BillingWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency Login")
        self.resize(400, 300)
        self.setStyleSheet("background-color: #f5f5f5; color: #333;")

        layout = QVBoxLayout()

        title = QLabel("Welcome to Travel Agency")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        logo = QLabel()
        pixmap = QPixmap("logo.png")
        logo.setPixmap(pixmap.scaled(120, 80, Qt.AspectRatioMode.KeepAspectRatio))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)

        self.pin_box = QLineEdit()
        self.pin_box.setPlaceholderText("Enter PIN")
        self.pin_box.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pin_box)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.check_pin)
        layout.addWidget(login_button)

        self.feedback = QLabel("")
        self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback)

        self.setLayout(layout)

    def check_pin(self):
        entered_pin = self.pin_box.text()

        conn = sqlite3.connect("travel_agency.db")
        cur = conn.cursor()
        cur.execute("SELECT pin FROM pin_table LIMIT 1")
        correct_pin = cur.fetchone()[0]
        conn.close()

        if entered_pin == correct_pin:
            self.feedback.setText("✅ Login Successful!")
            self.feedback.setStyleSheet("color: green;")

            self.open_billing()
        else:
            self.feedback.setText("❌ Incorrect PIN.")
            self.feedback.setStyleSheet("color: red;")

    def open_billing(self):
        self.billing = BillingWindow()
        self.billing.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
