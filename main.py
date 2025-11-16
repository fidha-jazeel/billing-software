# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#     QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
# )
# from PyQt6.QtCore import Qt
# import sys
# import csv
# from datetime import datetime
# from PyQt6.QtWidgets import QFileDialog, QMessageBox


# class BillingApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Agency - Billing Software")
#         self.setGeometry(200, 100, 1000, 600)
#         self.setStyleSheet("background-color: #1e1e1e; color: white; font-size: 14px;")

#         # Main Layout
#         container = QWidget()
#         layout = QVBoxLayout(container)

#         # Title
#         title = QLabel("💼 Travel Agency Billing System")
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         title.setStyleSheet("font-size: 20px; color: #4FC3F7; font-weight: bold;")
#         layout.addWidget(title)

#         # Customer info section
#         customer_layout = QHBoxLayout()
#         customer_layout.addWidget(QLabel("Customer Name:"))
#         self.name_input = QLineEdit()
#         customer_layout.addWidget(self.name_input)

#         customer_layout.addWidget(QLabel("Contact No:"))
#         self.contact_input = QLineEdit()
#         customer_layout.addWidget(self.contact_input)
#         layout.addLayout(customer_layout)

#         # Table
#         self.table = QTableWidget(1, 5)
#         self.table.setHorizontalHeaderLabels(["Item", "Qty", "Price", "Tax %", "Amount"])
#         layout.addWidget(self.table)
        
#         # save_btn = QPushButton("💾 Save Bill")
#         # save_btn.setStyleSheet("background-color: #FFD54F; color: black;")
#         # save_btn.clicked.connect(self.save_bill)
#         # btn_layout.addWidget(save_btn)

#         # Buttons
#         btn_layout = QHBoxLayout()
#         add_btn = QPushButton("+ Add Item")
#         add_btn.setStyleSheet("background-color: #4FC3F7; color: black;")
#         add_btn.clicked.connect(self.add_item)
#         btn_layout.addWidget(add_btn)

#         calc_btn = QPushButton("Calculate Total")
#         calc_btn.setStyleSheet("background-color: #81C784; color: black;")
#         calc_btn.clicked.connect(self.calculate_total)
#         btn_layout.addWidget(calc_btn)
        
#         reset_btn = QPushButton("🧾 New Bill")
#         reset_btn.setStyleSheet("background-color: #E57373; color: black;")
#         reset_btn.clicked.connect(self.new_bill)
#         btn_layout.addWidget(reset_btn)

#         save_btn = QPushButton("💾 Save Bill")
#         save_btn.setStyleSheet("background-color: #FFD54F; color: black;")
#         save_btn.clicked.connect(self.save_bill)
#         btn_layout.addWidget(save_btn)
#         btn_layout.addWidget(add_btn)
#         btn_layout.addWidget(calc_btn)
#         layout.addLayout(btn_layout)

#         # Total Label
#         self.total_label = QLabel("Total: ₹ 0.00")
#         self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
#         self.total_label.setStyleSheet("font-size: 16px; color: #81C784; font-weight: bold;")
#         layout.addWidget(self.total_label)

#         self.setCentralWidget(container)
#         # QMessageBox.information(self, "Saved", "Bill saved successfully!")
#         # self.new_bill()

#     def add_item(self):
#         row = self.table.rowCount()
#         self.table.insertRow(row)

#     def calculate_total(self):
#         total = 0.0
#         for row in range(self.table.rowCount()):
#             try:
#                 qty = float(self.table.item(row, 1).text()) if self.table.item(row, 1) else 0
#                 price = float(self.table.item(row, 2).text()) if self.table.item(row, 2) else 0
#                 tax = float(self.table.item(row, 3).text()) if self.table.item(row, 3) else 0
#                 amount = qty * price * (1 + tax / 100)
#                 total += amount
#                 self.table.setItem(row, 4, QTableWidgetItem(f"{amount:.2f}"))
#             except Exception:
#                 pass
#         self.total_label.setText(f"Total: ₹ {total:.2f}")
 
#     def save_bill(self):
#         customer_name = self.customer_name_input.text().strip()
#         contact = self.contact_input.text().strip()

#         if self.table.rowCount() == 0 or not customer_name:
#             QMessageBox.warning(self, "Error", "Please add at least one item and enter customer name.")
#             return

#         if not contact:
#             QMessageBox.warning(self, "Error", "Please enter contact number.")
#             return

#         filename, _ = QFileDialog.getSaveFileName(
#             self,
#             "Save Bill",
#             f"{customer_name}_bill.csv",
#             "CSV Files (*.csv)"
#         )

#         if filename:
#             with open(filename, mode='w', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(["Customer Name", customer_name])
#                 writer.writerow(["Contact No", contact])
#                 writer.writerow([])
#                 writer.writerow(["Item", "Qty", "Price", "Tax %", "Amount"])

#                 for row in range(self.table.rowCount()):
#                     row_data = []
#                     for col in range(self.table.columnCount()):
#                         item = self.table.item(row, col)
#                         row_data.append(item.text() if item else "")
#                     writer.writerow(row_data)

#                 writer.writerow([])
#                 total_text = self.total_label.text().replace("Total:", "").replace("₹", "").strip()
#             # try:
#             #     total_value = float(total_text.replace(",", ""))
#             #     total_text = f"{total_value:.2f}"
#             # except ValueError:
#             #     total_text = total_text or "0.00"
#             try:
#                 total_value = float(
#                     self.total_label.text()
#                     .replace("Total:", "")
#                     .replace("₹", "")
#                     .replace(",", "")
#                     .strip()
#             )
#                 total_text = f"{total_value:.2f}"
#             except ValueError:
#                 total_text = "0.00"

#                 writer.writerow(["Total", total_text])

#             QMessageBox.information(self, "Saved", "Bill saved successfully!")

#             # Clear inputs after saving
#             self.customer_name_input.clear()
#             self.contact_input.clear()
#             self.table.setRowCount(0)
#             self.total_label.setText("Total: ₹ 0.00")

#     # def save_bill(self):
#     #    # Get customer name first
#     #     customer_name = self.customer_name_input.text().strip()
#     #     contact = self.contact_input.text().strip()

#     # # Prevent saving empty bills
#     #     if self.table.rowCount() == 0 or not customer_name:
#     #         QMessageBox.warning(self, "Error", "Please add at least one item and enter customer name.")
#     #         return

#     #     if not contact:
#     #         QMessageBox.warning(self, "Error", "Please enter contact number.")
#     #         return

#     # Get customer name first
#         # customer_name = self.customer_name_input.text().strip()

#     # Prevent saving empty bills
#         # if self.table.rowCount() == 0 or not customer_name:
#         #     QMessageBox.warning(self, "Error", "Please add at least one item and enter customer name.")
#         # return

#     # Prevent saving empty bills
#         # if self.table.rowCount() == 0 or not customer_name = self.customer_name_input.text().strip()
#         #     QMessageBox.warning(self, "Error", "Please add at least one item and enter customer name.")
#         #     return

#         # if self.table.rowCount() == 0 or not self.customer_name_input.text().strip():
#     #     customer_name = self.name_input.text().strip()
#     #     contact = self.contact_input.text().strip()

#     #     if not customer_name:
#     #         QMessageBox.warning(self, "Warning", "Please enter Customer Name!")
#     #         return

#     #     filename, _ = QFileDialog.getSaveFileName(
#     #         self, "Save Bill", f"{customer_name}_bill.csv", "CSV Files (*.csv)"
#     #     )

#     #     if filename:
#     #         with open(filename, mode='w', newline='', encoding='utf-8') as file:
#     #             writer = csv.writer(file)
#     #             writer.writerow(["Customer Name", customer_name])
#     #             writer.writerow(["Contact No", contact])
#     #             writer.writerow([])
#     #             writer.writerow(["Item", "Qty", "Price", "Tax %", "Amount"])

#     #             for row in range(self.table.rowCount()):
#     #                 row_data = []
#     #                 for col in range(self.table.columnCount()):
#     #                     item = self.table.item(row, col)
#     #                     row_data.append(item.text() if item else "")
#     #                 writer.writerow(row_data)

#     #             writer.writerow([])
#     #             writer.writerow(["Total", self.total_label.text().split("₹")[1].strip()])

#     #         QMessageBox.information(self, "Saved", "Bill saved successfully!")
#     #         self.new_bill()
#     def new_bill(self):
#     # Clear all input fields
#             self.customer_name_input.clear()
#             self.contact_input.clear()

#     # Clear all rows from the table
#             self.table.setRowCount(0)

#     # Reset total label
#             self.total_label.setText("Total: ₹ 0.00")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = BillingApp()
#     window.show()
#     sys.exit(app.exec())
# import sys
# from PyQt5 import QtWidgets
# from ui.dashboard import Ui_MainWindow  # Import the UI from dashboard.py

# class DashboardApp(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = DashboardApp()
#     window.show()
#     sys.exit(app.exec_())
from PyQt5.QtWidgets import QApplication
import sys

# Import the new improved dashboard
from travel_billing.dashboard_improved import DashboardImproved

app = QApplication(sys.argv)
window = DashboardImproved()
window.show()
sys.exit(app.exec_())