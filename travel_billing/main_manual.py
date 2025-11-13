# from PyQt5 import QtWidgets, QtCore, QtGui
# import sys

# class DashboardApp(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Agency - Billing Software")
#         self.setGeometry(100, 100, 1200, 700)
#         self.setStyleSheet("background-color: #181818; color: white; font-family: Segoe UI;")

#         # ======= Left Sidebar =======
#         self.sidebar = QtWidgets.QFrame(self)
#         self.sidebar.setGeometry(0, 0, 200, 700)
#         self.sidebar.setStyleSheet("background-color: #202020;")

#         self.logo = QtWidgets.QLabel("🧳 Travel Agency", self.sidebar)
#         self.logo.setGeometry(30, 20, 160, 40)
#         self.logo.setStyleSheet("font-weight: bold; font-size: 16px; color: #00c896;")

#         self.btn_home = QtWidgets.QPushButton("🏠  Home", self.sidebar)
#         self.btn_home.setGeometry(20, 80, 160, 40)
#         self.btn_home.setStyleSheet("text-align: left; padding-left: 20px;")

#         self.btn_reports = QtWidgets.QPushButton("📄  Reports", self.sidebar)
#         self.btn_reports.setGeometry(20, 130, 160, 40)
#         self.btn_reports.setStyleSheet("text-align: left; padding-left: 20px;")

#         self.btn_settings = QtWidgets.QPushButton("⚙️  Settings", self.sidebar)
#         self.btn_settings.setGeometry(20, 180, 160, 40)
#         self.btn_settings.setStyleSheet("text-align: left; padding-left: 20px;")

#         self.btn_about = QtWidgets.QPushButton("ℹ️  About", self.sidebar)
#         self.btn_about.setGeometry(20, 230, 160, 40)
#         self.btn_about.setStyleSheet("text-align: left; padding-left: 20px;")

#         # ======= Main Area =======
#         self.main_frame = QtWidgets.QFrame(self)
#         self.main_frame.setGeometry(200, 0, 1000, 700)
#         self.main_frame.setStyleSheet("background-color: #181818;")

#         self.title = QtWidgets.QLabel("Welcome to Travel Agency Billing", self.main_frame)
#         self.title.setGeometry(40, 20, 600, 30)
#         self.title.setStyleSheet("font-size: 18px;")

#         self.subtitle = QtWidgets.QLabel("Enter details to make your invoice 🚀", self.main_frame)
#         self.subtitle.setGeometry(40, 50, 400, 25)
#         self.subtitle.setStyleSheet("color: #c0c0c0;")

#         # Example Input Field
#         self.invoice_label = QtWidgets.QLabel("Invoice Number:", self.main_frame)
#         self.invoice_label.setGeometry(40, 100, 150, 30)
#         self.invoice_input = QtWidgets.QLineEdit(self.main_frame)
#         self.invoice_input.setGeometry(180, 100, 200, 30)

#         # Save Button
#         self.btn_save = QtWidgets.QPushButton("💾 Save Invoice", self.main_frame)
#         self.btn_save.setGeometry(800, 630, 150, 40)
#         self.btn_save.setStyleSheet("background-color: #5b5bff; border-radius: 8px; color: white;")

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = DashboardApp()
#     window.show()
#     sys.exit(app.exec_())
# from travel_billing.dashboard_manual import DashboardManual
# from PyQt5.QtWidgets import QApplication
# import sys

# app = QApplication(sys.argv)
# window = DashboardManual()
# window.show()
# sys.exit(app.exec_())
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox,
    QTableWidget, QTableWidgetItem, QPushButton, QDateEdit, QGridLayout
)
from PyQt5.QtCore import QDate, Qt


# class InvoicePage(QWidget):
#     def __init__(self):
#         super().__init__()

#         # === MAIN LAYOUT ===
#         main_layout = QVBoxLayout(self)
# from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

class InvoicePage(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main_manual.ui', self)

# class InvoicePage(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi('ui/main_manual.ui', self)

        # ---------- INVOICE DETAILS ----------
        invoice_group = QGroupBox("📄 Invoice Details")
        invoice_layout = QGridLayout()

        lbl_invoice_number = QLabel("Invoice Number:")
        self.txt_invoice_number = QLineEdit("Auto-generated")
        self.txt_invoice_number.setReadOnly(True)

        lbl_invoice_date = QLabel("Invoice Date:")
        self.date_invoice = QDateEdit()
        self.date_invoice.setDate(QDate.currentDate())
        self.date_invoice.setCalendarPopup(True)

        invoice_layout.addWidget(lbl_invoice_number, 0, 0)
        invoice_layout.addWidget(self.txt_invoice_number, 0, 1)
        invoice_layout.addWidget(lbl_invoice_date, 0, 2)
        invoice_layout.addWidget(self.date_invoice, 0, 3)
        invoice_group.setLayout(invoice_layout)

        # ---------- BILL TO ----------
        billto_group = QGroupBox("👤 Bill To")
        billto_layout = QGridLayout()

        lbl_customer_name = QLabel("Customer Name:")
        self.txt_customer_name = QLineEdit()
        lbl_contact = QLabel("Contact Number:")
        self.txt_contact = QLineEdit()

        billto_layout.addWidget(lbl_customer_name, 0, 0)
        billto_layout.addWidget(self.txt_customer_name, 0, 1)
        billto_layout.addWidget(lbl_contact, 0, 2)
        billto_layout.addWidget(self.txt_contact, 0, 3)
        billto_group.setLayout(billto_layout)

        # ---------- BILLED ITEMS TABLE ----------
        items_group = QGroupBox("🧾 Billed Items")
        self.tbl_items = QTableWidget(5, 6)
        self.tbl_items.setHorizontalHeaderLabels(
            ["Item Name", "Ticket #", "Sector", "Supplier", "Price", "Qty"]
        )
        self.tbl_items.horizontalHeader().setStretchLastSection(True)
        items_layout = QVBoxLayout()
        items_layout.addWidget(self.tbl_items)
        items_group.setLayout(items_layout)

        # ---------- INVOICE TOTAL ----------
        total_group = QGroupBox("💰 Invoice Calculation")
        total_layout = QGridLayout()

        lbl_subtotal = QLabel("Subtotal:")
        self.txt_subtotal = QLineEdit("₹0.00")
        lbl_tax = QLabel("Tax (5%):")
        self.txt_tax = QLineEdit("₹0.00")
        lbl_total = QLabel("Total:")
        self.txt_total = QLineEdit("₹0.00")

        self.txt_subtotal.setReadOnly(True)
        self.txt_tax.setReadOnly(True)
        self.txt_total.setReadOnly(True)

        total_layout.addWidget(lbl_subtotal, 0, 0)
        total_layout.addWidget(self.txt_subtotal, 0, 1)
        total_layout.addWidget(lbl_tax, 0, 2)
        total_layout.addWidget(self.txt_tax, 0, 3)
        total_layout.addWidget(lbl_total, 1, 2)
        total_layout.addWidget(self.txt_total, 1, 3)
        total_group.setLayout(total_layout)

        # ---------- BUTTONS ----------
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 Save Invoice")
        self.pdf_btn = QPushButton("📄 Save as PDF")
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.pdf_btn)

        # ---------- ADD ALL TO MAIN ----------
        # main_layout.addWidget(invoice_group)
        # main_layout.addWidget(billto_group)
        # main_layout.addWidget(items_group)
        # main_layout.addWidget(total_group)
        # main_layout.addLayout(button_layout)

        # Connect signals
        self.save_btn.clicked.connect(self.save_invoice)
        self.pdf_btn.clicked.connect(self.save_pdf)

    # ---------- FUNCTIONS ----------
    def save_invoice(self):
        print("Invoice Saved!")

    def save_pdf(self):
        print("Invoice exported to PDF!")
