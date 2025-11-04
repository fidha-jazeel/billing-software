from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QFont
import sys

class BillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency Billing System")
        self.resize(400, 400)
        self.setStyleSheet("background-color: #f0f0f0; color: #000;")
        
        layout = QVBoxLayout()

        title = QLabel("🧳 Travel Agency Billing")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Customer Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Customer Name")
        layout.addWidget(QLabel("Customer Name:"))
        layout.addWidget(self.name_input)

        # Destination
        self.destination_input = QLineEdit()
        self.destination_input.setPlaceholderText("Enter Destination")
        layout.addWidget(QLabel("Destination:"))
        layout.addWidget(self.destination_input)

        # Number of Tickets
        self.tickets_input = QLineEdit()
        self.tickets_input.setPlaceholderText("Enter No. of Tickets")
        layout.addWidget(QLabel("Number of Tickets:"))
        layout.addWidget(self.tickets_input)

        # Price per ticket
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter Price per Ticket")
        layout.addWidget(QLabel("Price per Ticket:"))
        layout.addWidget(self.price_input)

        # Total Label
        self.total_label = QLabel("Total: ₹0")
        self.total_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.total_label)

        # Buttons
        button_layout = QHBoxLayout()

        calc_button = QPushButton("Calculate")
        calc_button.clicked.connect(self.calculate_total)
        button_layout.addWidget(calc_button)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def calculate_total(self):
        try:
            tickets = int(self.tickets_input.text())
            price = float(self.price_input.text())
            total = tickets * price
            self.total_label.setText(f"Total: ₹{total:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers for tickets and price.")

    def clear_fields(self):
        self.name_input.clear()
        self.destination_input.clear()
        self.tickets_input.clear()
        self.price_input.clear()
        self.total_label.setText("Total: ₹0")

if __name__ == "__main__":
    from PyQt6.QtCore import Qt
    app = QApplication(sys.argv)
    window = BillingApp()
    window.showMaximized() 
    sys.exit(app.exec())
