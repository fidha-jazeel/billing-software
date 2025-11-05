import sys
import sqlite3
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database.db import init_db
from billing_window import BillingWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Billing - Login")
        self.resize(300, 150)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter PIN"))

        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pin_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.check_pin)
        layout.addWidget(login_btn)

        self.feedback = QLabel("")
        layout.addWidget(self.feedback)
   

        self.setLayout(layout)

    def check_pin(self):
        conn = sqlite3.connect("travel_billing.db")
        cur = conn.cursor()
        cur.execute("SELECT pin FROM pin_table LIMIT 1")
        correct_pin = cur.fetchone()[0]
        conn.close()

        if self.pin_input.text() == correct_pin:
            self.open_billing()
        else:
            QMessageBox.warning(self, "Error", "Incorrect PIN")
    def open_billing(self):
      self.billing = BillingWindow()
      self.billing.show()
      self.close()

    def check_pin(self):
        entered_pin = self.pin_input.text()
    
    # ✅ Correct database path (same as db.py)
        db_path = Path(__file__).resolve().parent / "travel_billing.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

    # Fetch stored PIN from the table
        cur.execute("SELECT pin FROM pin_table LIMIT 1")
        correct_pin = cur.fetchone()[0]
        conn.close()

    # Compare entered and stored PIN
        if entered_pin == correct_pin:
          self.feedback.setText("✅ Login Successful!")
          self.feedback.setStyleSheet("color: green;")
          self.open_billing()
        else:
          self.feedback.setText("❌ Incorrect PIN")
          self.feedback.setStyleSheet("color: red;")

    def open_billing(self):
        self.billing = BillingWindow()
        self.billing.show()
        self.close()

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
# import os
# from pathlib import Path

# db_path = Path(__file__).resolve().parent / "travel_billing.db"
# conn = sqlite3.connect(db_path)
