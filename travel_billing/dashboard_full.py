# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#     QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
# )
# from PyQt5.QtCore import Qt
# import sys


# class DashboardFull(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Agency - Billing Software")
#         self.setGeometry(100, 100, 1200, 700)
#         self.setStyleSheet("""
#             QMainWindow { background-color: #121212; color: #ffffff; }
#             QLabel { color: #dddddd; font-size: 14px; }
#             QLineEdit {
#                 background-color: #1e1e1e;
#                 color: #ffffff;
#                 border: 1px solid #555;
#                 border-radius: 5px;
#                 padding: 4px;
#             }
#             QPushButton {
#                 background-color: #5b5bff;
#                 color: white;
#                 border-radius: 6px;
#                 padding: 6px 12px;
#             }
#             QPushButton:hover {
#                 background-color: #7777ff;
#             }
#             QFrame#sidebar {
#                 background-color: #1b1b1b;
#             }
#             QPushButton#sidebtn {
#                 background-color: #1b1b1b;
#                 color: #bbbbbb;
#                 border: none;
#                 text-align: left;
#                 padding: 10px;
#             }
#             QPushButton#sidebtn:hover {
#                 background-color: #333333;
#                 color: white;
#             }
#         """)

#         # ---------- Main Layout ----------
#         main_widget = QWidget()
#         main_layout = QHBoxLayout(main_widget)
#         self.setCentralWidget(main_widget)

#         # ---------- Sidebar ----------
#         sidebar = QFrame()
#         sidebar.setObjectName("sidebar")
#         sidebar.setFixedWidth(200)
#         sidebar_layout = QVBoxLayout(sidebar)

#         title = QLabel("<b style='font-size:16px;'>🏢 Travel Agency</b>")
#         title.setAlignment(Qt.AlignCenter)
#         sidebar_layout.addWidget(title)

#         for text in ["🏠 Home", "📊 Reports", "⚙ Settings", "ℹ About"]:
#             btn = QPushButton(text)
#             btn.setObjectName("sidebtn")
#             sidebar_layout.addWidget(btn)
#         sidebar_layout.addStretch()

#         main_layout.addWidget(sidebar)

#         # ---------- Main content area ----------
#         content = QFrame()
#         content_layout = QVBoxLayout(content)

#         heading = QLabel("<h2>Welcome to Travel Agency Billing</h2>")
#         content_layout.addWidget(heading)

#         # --- Invoice Info Section ---
#         form_layout = QHBoxLayout()

#         invoice_number_label = QLabel("Invoice Number:")
#         self.invoice_number = QLineEdit()
#         self.invoice_number.setPlaceholderText("Auto-generated")

#         customer_name_label = QLabel("Customer Name:")
#         self.customer_name = QLineEdit()
#         self.customer_name.setPlaceholderText("Enter customer name")

#         form_layout.addWidget(invoice_number_label)
#         form_layout.addWidget(self.invoice_number)
#         form_layout.addWidget(customer_name_label)
#         form_layout.addWidget(self.customer_name)
#         content_layout.addLayout(form_layout)

#         # --- Table for Billed Items ---
#         table_label = QLabel("<b>Billed Items:</b>")
#         content_layout.addWidget(table_label)

#         self.table = QTableWidget(3, 6)
#         self.table.setHorizontalHeaderLabels([
#             "Item Name", "Ticket #", "Sector", "Supplier", "Price", "Qty"
#         ])
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         content_layout.addWidget(self.table)

#         # --- Total Calculation ---
#         total_layout = QHBoxLayout()
#         self.subtotal_label = QLabel("Subtotal: ₹0.00")
#         self.tax_label = QLabel("Tax: ₹0.00")
#         self.total_label = QLabel("<b>Total: ₹0.00</b>")
#         total_layout.addWidget(self.subtotal_label)
#         total_layout.addWidget(self.tax_label)
#         total_layout.addWidget(self.total_label)
#         content_layout.addLayout(total_layout)

#         # --- Buttons ---
#         btn_layout = QHBoxLayout()
#         save_btn = QPushButton("💾 Save Invoice")
#         pdf_btn = QPushButton("🧾 Save as PDF")
#         btn_layout.addStretch()
#         btn_layout.addWidget(save_btn)
#         btn_layout.addWidget(pdf_btn)
#         content_layout.addLayout(btn_layout)

#         main_layout.addWidget(content)

#         # ---------- Connections ----------
#         save_btn.clicked.connect(self.save_invoice)

#     def save_invoice(self):
#         customer = self.customer_name.text().strip()
#         if customer:
#             print(f"Invoice saved for {customer}")
#         else:
#             print("Please enter customer name")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DashboardFull()
#     window.show()
#     sys.exit(app.exec_())
# from PyQt5.QtWidgets import QWidget
# from travel_billing.main_manual import InvoicePage

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
)
# from PyQt5.QtCore import Qt
# import sys
# from ui.dashboard import Ui_MainWindow

# class DashboardFull(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.ui.btn_newBill.clicked.connect(self.load_invoice_page)
#         self.setWindowTitle("Travel Agency - Billing Software")

from PyQt5 import QtWidgets
from PyQt5 import uic
from travel_billing.main_manual import InvoicePage
import sys

class DashboardFull(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency - Billing Software")
        self.resize(1200, 700)

        # Create invoice page
        self.invoice_page = InvoicePage()

        # Central layout
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(central_widget)

        # Sidebar (optional)
        sidebar = QtWidgets.QFrame()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet("background-color: #111;")

        # Add sidebar and content
        layout.addWidget(sidebar)
        layout.addWidget(self.invoice_page)

        # Set as central widget
        self.setCentralWidget(central_widget)

# class DashboardFull(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         from ui.dashboard import Ui_MainWindow


#         self.ui = Ui_MainWindow()

#         self.ui.setupUi(self)
#         self.ui.btn_newBill.clicked.connect(self.load_invoice_page)

#         self.setWindowTitle("Travel Agency - Billing Software")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; color: #ffffff; }
            QLabel { color: #dddddd; font-size: 14px; }
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 4px;
            }
            QPushButton {
                background-color: #5b5bff;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #7777ff;
            }
            QFrame#sidebar {
                background-color: #1b1b1b;
            }
            QPushButton#sidebtn {
                background-color: #1b1b1b;
                color: #bbbbbb;
                border: none;
                text-align: left;
                padding: 10px;
            }
            QPushButton#sidebtn:hover {
                background-color: #333333;
                color: white;
            }
        """)

        # ---------- Main Layout ----------
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # ---------- Sidebar ----------
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("<b style='font-size:16px;'>🏢 Travel Agency</b>")
        title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title)

        for text in ["🏠 Home", "📊 Reports", "⚙ Settings", "ℹ About"]:
            btn = QPushButton(text)
            btn.setObjectName("sidebtn")
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        # ---------- Main content area ----------
        content = QFrame()
        content_layout = QVBoxLayout(content)

        heading = QLabel("<h2>Welcome to Travel Agency Billing</h2>")
        content_layout.addWidget(heading)

        # --- Invoice Info Section ---
            
        info_layout = QHBoxLayout()

        # ===== Left: Invoice Details =====
        invoice_group = QFrame()
        invoice_group.setStyleSheet("""
            QFrame {
                background-color: #3a3a3a;
            border-radius: 8px;
                padding: 10px;
            }
        """)
        invoice_layout = QVBoxLayout(invoice_group)

        invoice_title = QLabel("📄 <b>Invoice Details :</b>")
        invoice_title.setStyleSheet("color: #9b9bff; font-size: 14px;")
        invoice_layout.addWidget(invoice_title)

        invoice_no_label = QLabel("Invoice Number :")
        self.invoice_number = QLineEdit()
        self.invoice_number.setPlaceholderText("Auto-generated")

        invoice_date_label = QLabel("Invoice Date :")
        self.invoice_date = QLineEdit("12-11-2025")

        invoice_layout.addWidget(invoice_no_label)
        invoice_layout.addWidget(self.invoice_number)
        invoice_layout.addWidget(invoice_date_label)
        invoice_layout.addWidget(self.invoice_date)

        # ===== Right: Bill To =====
        billto_group = QFrame()
        billto_group.setStyleSheet("""
            QFrame {
                background-color: #3a3a3a;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        billto_layout = QVBoxLayout(billto_group)

        billto_title = QLabel("👤 <b>Bill To :</b>")
        billto_title.setStyleSheet("color: #9b9bff; font-size: 14px;")
        billto_layout.addWidget(billto_title)

        customer_name_label = QLabel("Customer Name* :")
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")

        contact_label = QLabel("Contact Number :")
        self.customer_contact = QLineEdit()
        self.customer_contact.setPlaceholderText("Enter contact number")

        billto_layout.addWidget(customer_name_label)
        billto_layout.addWidget(self.customer_name)
        billto_layout.addWidget(contact_label)
        billto_layout.addWidget(self.customer_contact)

        # Add both group sections to main info layout
        # info_layout.addWidget(invoice_group)
        # info_layout.addWidget(billto_group)
        info_layout = QHBoxLayout()

        info_layout.addWidget(invoice_group)
        info_layout.addWidget(billto_group)
        info_layout.setSpacing(40)  # space between them
        info_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.addLayout(info_layout)
        # form_layout = QHBoxLayout()
        save_btn = QPushButton("Save Invoice")
        form_layout = QHBoxLayout()
        save_btn.clicked.connect(self.save_invoice)

        # save_btn.clicked.connect(self.save_invoice)

        # invoice_number_label = QLabel("Invoice Number:")
        # self.invoice_number = QLineEdit()
        # self.invoice_number.setPlaceholderText("Auto-generated")

        # customer_name_label = QLabel("Customer Name:")
        # self.customer_name = QLineEdit()
        # self.customer_name.setPlaceholderText("Enter customer name")

        # contact_label = QLabel("Contact:")
        # self.customer_contact = QLineEdit()
        # self.customer_contact.setPlaceholderText("Enter contact number")

        # form_layout.addWidget(invoice_number_label)
        # form_layout.addWidget(self.invoice_number)
        # form_layout.addWidget(customer_name_label)
        # form_layout.addWidget(self.customer_name)
        # form_layout.addWidget(contact_label)
        # form_layout.addWidget(self.customer_contact)
        # content_layout.addLayout(form_layout)

        # # --- Table for Billed Items ---
        # table_label = QLabel("<b>Billed Items:</b>")
        # content_layout.addWidget(table_label)

        # self.table = QTableWidget(5, 6)
        # self.table.setHorizontalHeaderLabels([
        #     "Item Name", "Ticket #", "Sector", "Supplier", "Price", "Qty"
        # ])
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # content_layout.addWidget(self.table)

        # # Connect cell changes to calculation
        # self.table.cellChanged.connect(self.calculate_totals)

        # # --- Total Calculation ---
        # total_layout = QHBoxLayout()
        # self.subtotal_label = QLabel("Subtotal: ₹0.00")
        # self.tax_label = QLabel("Tax (5%): ₹0.00")
        # self.total_label = QLabel("<b>Total: ₹0.00</b>")
        # total_layout.addWidget(self.subtotal_label)
        # total_layout.addWidget(self.tax_label)
        # total_layout.addWidget(self.total_label)
        # content_layout.addLayout(total_layout)

        # # --- Buttons ---
        # btn_layout = QHBoxLayout()
        # save_btn = QPushButton("💾 Save Invoice")
        # pdf_btn = QPushButton("🧾 Save as PDF")
        # btn_layout.addStretch()
        # btn_layout.addWidget(save_btn)
        # btn_layout.addWidget(pdf_btn)
        # content_layout.addLayout(btn_layout)

        # main_layout.addWidget(content)

        # ---------- Connections ----------
        save_btn.clicked.connect(self.save_invoice)
        # self.ui.btn_newBill.clicked.connect(self.load_invoice_page)
        uic.loadUi('ui/dashboard.ui', self)
        self.btn_newBill.clicked.connect(self.load_invoice_page)

            # save_btn.clicked.connect(self.save_invoice)

    # === Paste here ===
    def load_invoice_page(self):
        # -------- Clear existing central widget --------
        layout = self.ui.mainContent.layout()
        if layout is None:
            from PyQt5.QtWidgets import QVBoxLayout
            layout = QVBoxLayout(self.ui.mainContent)
            self.ui.mainContent.setLayout(layout)

        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # -------- Load the Invoice Page UI --------
        self.invoice_page = QWidget()
        self.invoice_ui = InvoicePage()

        self.invoice_ui.setupUi(self.invoice_page)

        # -------- Add the invoice page to main content area --------
        layout.addWidget(self.invoice_page)

    # def calculate_totals(self):
    #     subtotal = 0.0
    #     for row in range(self.table.rowCount()):
    #         ...

    
        # self.invoice_ui = Ui_MainManual()
        # self.invoice_ui.setupUi(self.invoice_page)

        # # Add the invoice page to main content area
        # self.ui.mainContent.layout().addWidget(self.invoice_page)

    def calculate_totals(self):
        subtotal = 0.0
        for row in range(self.table.rowCount()):
            try:
                price_item = self.table.item(row, 4)
                qty_item = self.table.item(row, 5)
                if price_item and qty_item:
                    price = float(price_item.text())
                    qty = float(qty_item.text())
                    subtotal += price * qty
            except ValueError:
                pass  # Ignore if not numeric
        tax = subtotal * 0.05
        total = subtotal + tax

        self.subtotal_label.setText(f"Subtotal: ₹{subtotal:.2f}")
        self.tax_label.setText(f"Tax (5%): ₹{tax:.2f}")
        self.total_label.setText(f"<b>Total: ₹{total:.2f}</b>")

    def save_invoice(self):
        customer = self.customer_name.text().strip()
        contact = self.customer_contact.text().strip()
        print(f"Invoice saved for {customer} ({contact})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardFull()
    window.show()
    sys.exit(app.exec_())
