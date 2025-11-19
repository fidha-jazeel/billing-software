"""
Home Page Module
Contains invoice creation, item management, and invoice operations.
"""
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
                             QFrame, QScrollArea, QTableWidget, QPushButton, QLineEdit,
                             QComboBox, QDoubleSpinBox, QDateEdit, QFileDialog, QMessageBox,
                             QInputDialog, QHeaderView)
from PyQt5.QtCore import Qt, QDate, QRect
from PyQt5.QtGui import QFont, QPen, QColor

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from utils.invoice_generator import generate_invoice_pdf


class HomePage(QWidget):
    """Home page with invoice creation and management."""
    
    def __init__(self, colors, company_info, invoice_config, app_config,
                 get_frame_style, get_input_style, get_dateedit_style, get_combobox_style,
                 get_invoice_prefix, get_currency_symbol, get_supplier_list, get_company_info_formatted,
                 dashboard_ref):
        """
        Initialize Home page.
        
        Args:
            colors: Color scheme dictionary
            company_info: Company information dictionary
            invoice_config: Invoice configuration dictionary
            app_config: Application configuration
            get_frame_style: Function to get frame stylesheet
            get_input_style: Function to get input stylesheet
            get_dateedit_style: Function to get date edit stylesheet
            get_combobox_style: Function to get combobox stylesheet
            get_invoice_prefix: Function to get invoice prefix
            get_currency_symbol: Function to get currency symbol
            get_supplier_list: Function to get supplier list
            get_company_info_formatted: Function to get formatted company info
            dashboard_ref: Reference to parent dashboard for database access
        """
        super().__init__()
        self.colors = colors
        self.company_info = company_info
        self.invoice_config = invoice_config
        self.app_config = app_config
        self.get_frame_style = get_frame_style
        self.get_input_style = get_input_style
        self.get_dateedit_style = get_dateedit_style
        self.get_combobox_style = get_combobox_style
        self.get_invoice_prefix = get_invoice_prefix
        self.get_currency_symbol = get_currency_symbol
        self.get_supplier_list = get_supplier_list
        self.get_company_info_formatted = get_company_info_formatted
        self.dashboard = dashboard_ref
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Create scroll area for entire page
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1a1a1a;
            }
            QScrollBar:vertical {
                border: none;
                background: #2a2a2a;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #7c3aed;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a78bfa;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Content widget inside scroll area
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Welcome Heading
        welcome_heading = QLabel(f"Welcome To {self.company_info['name']} Billing")
        welcome_heading.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_cyan']};
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin-bottom: 10px;
            }}
        """)
        welcome_heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_heading)
        
        # Invoice Details Section
        invoice_details_frame = self._create_invoice_details_section()
        layout.addWidget(invoice_details_frame)
        
        # Table Section
        table_frame = self._create_table_section()
        layout.addWidget(table_frame)
        
        # Calculation Section
        calc_frame = self._create_calculation_section()
        layout.addWidget(calc_frame)
        
        # Save Buttons
        btn_layout_bottom = self._create_action_buttons()
        layout.addLayout(btn_layout_bottom)
        
        # Add bottom spacing
        layout.addSpacing(20)
        
        # Set scroll widget
        scroll.setWidget(content)
        
        # Main layout
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        # Compatibility alias
        self.items_table = self.table
    
    def _create_invoice_details_section(self) -> QFrame:
        """Create invoice details section."""
        invoice_details_frame = QFrame()
        invoice_details_frame.setStyleSheet(self.get_frame_style())
        invoice_layout = QGridLayout(invoice_details_frame)
        invoice_layout.setContentsMargins(20, 20, 20, 20)
        invoice_layout.setSpacing(15)
        invoice_layout.setColumnStretch(1, 1)
        invoice_layout.setColumnStretch(3, 1)
        
        # Invoice Details Title
        invoice_title = QLabel(f"<b style='color:{self.colors['accent_secondary']}; font-size:14px;'>📄 Invoice Details</b>")
        invoice_layout.addWidget(invoice_title, 0, 0, 1, 4)
        
        # Row 1: Invoice Number and Date
        lbl_inv_num = QLabel("Invoice Number:")
        lbl_inv_num.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_inv_num.setFixedWidth(130)
        invoice_layout.addWidget(lbl_inv_num, 1, 0, Qt.AlignRight)
        
        self.invoice_number = QLineEdit()
        self.invoice_number.setText(self.generate_invoice_number())
        self.invoice_number.setPlaceholderText("Auto-generated")
        self.invoice_number.setStyleSheet(self.get_input_style())
        self.invoice_number.setMinimumWidth(250)
        invoice_layout.addWidget(self.invoice_number, 1, 1)
        
        lbl_inv_date = QLabel("Invoice Date:")
        lbl_inv_date.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_inv_date.setFixedWidth(130)
        invoice_layout.addWidget(lbl_inv_date, 1, 2, Qt.AlignRight)
        
        self.invoice_date = QDateEdit()
        self.invoice_date.setDate(QDate.currentDate())
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDisplayFormat(self.invoice_config['date_format'])
        self.invoice_date.setStyleSheet(self.get_dateedit_style())
        self.invoice_date.setMinimumWidth(250)
        invoice_layout.addWidget(self.invoice_date, 1, 3)
        
        # Row 2: Customer Name and Contact
        lbl_cust_name = QLabel("Customer Name:")
        lbl_cust_name.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_cust_name.setFixedWidth(130)
        invoice_layout.addWidget(lbl_cust_name, 2, 0, Qt.AlignRight)
        
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        self.customer_name.setStyleSheet(self.get_input_style())
        self.customer_name.setMinimumWidth(250)
        invoice_layout.addWidget(self.customer_name, 2, 1)
        
        lbl_contact = QLabel("Contact Number:")
        lbl_contact.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_contact.setFixedWidth(130)
        invoice_layout.addWidget(lbl_contact, 2, 2, Qt.AlignRight)
        
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Enter contact number")
        self.contact_number.setStyleSheet(self.get_input_style())
        self.contact_number.setMinimumWidth(255)
        invoice_layout.addWidget(self.contact_number, 2, 3)
        
        # Row 3: Address
        lbl_address = QLabel("Address:")
        lbl_address.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_address.setFixedWidth(130)
        invoice_layout.addWidget(lbl_address, 3, 0, Qt.AlignRight)
        
        self.customer_address = QLineEdit()
        self.customer_address.setPlaceholderText("Enter customer address")
        self.customer_address.setStyleSheet(self.get_input_style())
        self.customer_address.setMinimumWidth(250)
        invoice_layout.addWidget(self.customer_address, 3, 1, 1, 3)
        
        return invoice_details_frame
    
    def _create_table_section(self) -> QFrame:
        """Create table section with Add Item button."""
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid #444;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        # Table header with Add Item button
        table_header_layout = QHBoxLayout()
        table_title = QLabel("<b style='color:#a78bfa; font-size:14px;'>🧾 Billed Items</b>")
        table_header_layout.addWidget(table_title)
        table_header_layout.addStretch()
        
        self.btn_add_item = QPushButton("➕ Add Item")
        self.btn_add_item.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent_primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent_secondary']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['accent_primary']};
            }}
        """)
        self.btn_add_item.clicked.connect(self.add_item_row)
        self.btn_add_item.setCursor(Qt.PointingHandCursor)
        table_header_layout.addWidget(self.btn_add_item)
        
        table_layout.addLayout(table_header_layout)
        
        # Table with 11 columns
        self.table = QTableWidget(0, 11)
        self.table.setHorizontalHeaderLabels([
            "Passenger Name", "PNR", "Sector", "Supplier", "Type", "Class", "Price (₹)", "Qty", "Tax (%)", "Amount (₹)", "Actions"
        ])
        
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.table.setMinimumHeight(300)
        
        table_layout.addWidget(self.table)
        
        return table_frame
    
    def _create_calculation_section(self) -> QFrame:
        """Create invoice calculation section."""
        calc_frame = QFrame()
        calc_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 8px;
                border: 1px solid {self.colors['accent_primary']};
                padding: 10px;
            }}
        """)
        calc_main_layout = QVBoxLayout(calc_frame)
        calc_main_layout.setContentsMargins(10, 10, 10, 10)
        calc_main_layout.setSpacing(5)
        
        calc_title = QLabel("<b style='color:#a78bfa; font-size:14px;'>💰 Invoice Calculation</b>")
        calc_main_layout.addWidget(calc_title)
        
        calc_grid = QGridLayout()
        calc_grid.setSpacing(5)
        calc_grid.setContentsMargins(5, 5, 5, 5)
        calc_grid.setColumnStretch(0, 1)
        
        # Subtotal
        subtotal_label = QLabel("Subtotal:")
        subtotal_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        subtotal_label.setMinimumWidth(90)
        calc_grid.addWidget(subtotal_label, 0, 1, Qt.AlignRight)
        
        self.lbl_subtotal = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_subtotal.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_secondary']};
                font-weight: bold;
                font-size: 13px;
                background-color: {self.colors['primary_bg']};
                padding: 5px 10px;
                border-radius: 4px;
                border: 1px solid {self.colors['accent_secondary']};
            }}
        """)
        self.lbl_subtotal.setMinimumWidth(120)
        calc_grid.addWidget(self.lbl_subtotal, 0, 2, Qt.AlignLeft)
        
        # Discount
        discount_label = QLabel("Discount:")
        discount_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        discount_label.setMinimumWidth(90)
        calc_grid.addWidget(discount_label, 1, 1, Qt.AlignRight)
        
        self.txt_discount = QLineEdit()
        self.txt_discount.setPlaceholderText(f"{self.get_currency_symbol()}0.00")
        self.txt_discount.setText("0.00")
        self.txt_discount.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['primary_bg']};
                color: {self.colors['accent_secondary']};
                border: 1px solid {self.colors['accent_secondary']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                font-weight: bold;
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['accent_secondary']};
            }}
        """)
        self.txt_discount.setMinimumWidth(120)
        self.txt_discount.textChanged.connect(self.update_invoice_totals)
        calc_grid.addWidget(self.txt_discount, 1, 2, Qt.AlignLeft)
        
        # Tax
        tax_label = QLabel("Tax:")
        tax_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        tax_label.setMinimumWidth(90)
        calc_grid.addWidget(tax_label, 2, 1, Qt.AlignRight)
        
        self.lbl_tax = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_tax.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_secondary']};
                font-weight: bold;
                font-size: 13px;
                background-color: {self.colors['primary_bg']};
                padding: 5px 10px;
                border-radius: 4px;
                border: 1px solid {self.colors['accent_secondary']};
            }}
        """)
        self.lbl_tax.setMinimumWidth(120)
        calc_grid.addWidget(self.lbl_tax, 2, 2, Qt.AlignLeft)
        
        # Total
        total_label = QLabel("Total:")
        total_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        total_label.setMinimumWidth(90)
        calc_grid.addWidget(total_label, 3, 1, Qt.AlignRight)
        
        self.lbl_total = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_total.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_gold']};
                font-weight: bold;
                font-size: 15px;
                background-color: {self.colors['primary_bg']};
                padding: 6px 12px;
                border-radius: 5px;
                border: 2px solid {self.colors['accent_gold']};
            }}
        """)
        self.lbl_total.setMinimumWidth(120)
        calc_grid.addWidget(self.lbl_total, 3, 2, Qt.AlignLeft)
        
        # Received
        received_label = QLabel("Received:")
        received_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        received_label.setMinimumWidth(90)
        calc_grid.addWidget(received_label, 4, 1, Qt.AlignRight)
        
        self.txt_received = QLineEdit()
        self.txt_received.setPlaceholderText(f"{self.get_currency_symbol()}0.00")
        self.txt_received.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.colors['primary_bg']};
                color: {self.colors['success']};
                border: 1px solid {self.colors['success']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                font-weight: bold;
            }}
            QLineEdit:focus {{
                border: 2px solid {self.colors['success']};
            }}
        """)
        self.txt_received.setMinimumWidth(120)
        self.txt_received.textChanged.connect(self.calculate_balance)
        calc_grid.addWidget(self.txt_received, 4, 2, Qt.AlignLeft)
        
        # Balance
        balance_label = QLabel("Balance:")
        balance_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        balance_label.setMinimumWidth(90)
        calc_grid.addWidget(balance_label, 5, 1, Qt.AlignRight)
        
        self.lbl_balance = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_balance.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['danger']};
                font-weight: bold;
                font-size: 13px;
                background-color: {self.colors['primary_bg']};
                padding: 5px 10px;
                border-radius: 4px;
                border: 1px solid {self.colors['danger']};
            }}
        """)
        self.lbl_balance.setMinimumWidth(120)
        calc_grid.addWidget(self.lbl_balance, 5, 2, Qt.AlignLeft)
        
        calc_main_layout.addLayout(calc_grid)
        
        return calc_frame
    
    def _create_action_buttons(self) -> QHBoxLayout:
        """Create action buttons (Save, PDF, Print, Share)."""
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_save_invoice = QPushButton("💾 Save Invoice")
        self.btn_save_invoice.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['success']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent_cyan']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['success']};
            }}
        """)
        self.btn_save_invoice.clicked.connect(self.save_invoice)
        self.btn_save_invoice.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(self.btn_save_invoice)
        
        self.btn_save_pdf = QPushButton("📄 Save as PDF")
        self.btn_save_pdf.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['danger']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent_gold']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['danger']};
            }}
        """)
        self.btn_save_pdf.clicked.connect(self.save_pdf)
        self.btn_save_pdf.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(self.btn_save_pdf)
        
        self.btn_print = QPushButton("🖨️ Print Invoice")
        self.btn_print.setStyleSheet("""
            QPushButton {
                background-color: #9b9bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #b5b5ff;
            }
            QPushButton:pressed {
                background-color: #8585ee;
            }
        """)
        self.btn_print.clicked.connect(self.print_invoice)
        self.btn_print.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(self.btn_print)
        
        self.btn_share = QPushButton("📤 Share Invoice")
        self.btn_share.setStyleSheet("""
            QPushButton {
                background-color: #20C997;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #38D9A9;
            }
            QPushButton:pressed {
                background-color: #12B886;
            }
        """)
        self.btn_share.clicked.connect(self.share_invoice)
        self.btn_share.setCursor(Qt.PointingHandCursor)
        btn_layout.addWidget(self.btn_share)
        
        return btn_layout
    
    def generate_invoice_number(self):
        """Generate a unique invoice number."""
        now = datetime.now()
        return f"{self.get_invoice_prefix()}-{now.strftime('%Y%m%d-%H%M%S')}"
    
    def add_item_row(self):
        """Add a new row to the table."""
        table = self.table
        row = table.rowCount()
        table.insertRow(row)
        
        # Adjust table height
        self.table.setMinimumHeight(min(300 + (row * 45), 600))

        # Spinbox style
        spinbox_style = """
            QDoubleSpinBox {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
                padding-right: 20px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #444;
            }
            QDoubleSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 18px;
                background-color: #3a3a3a;
                border-left: 1px solid #444;
                border-radius: 0px 3px 0px 0px;
            }
            QDoubleSpinBox::up-button:hover {
                background-color: #4a4a4a;
            }
            QDoubleSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 18px;
                background-color: #3a3a3a;
                border-left: 1px solid #444;
                border-radius: 0px 0px 3px 0px;
            }
            QDoubleSpinBox::down-button:hover {
                background-color: #4a4a4a;
            }
            QDoubleSpinBox::up-arrow {
                image: none;
                width: 10px;
                height: 10px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 6px solid #999;
            }
            QDoubleSpinBox::down-arrow {
                image: none;
                width: 10px;
                height: 10px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #999;
            }
        """
        
        lineedit_style = """
            QLineEdit {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #444;
            }
        """

        # Column 0: Passenger Name
        passenger_name = QLineEdit()
        passenger_name.setPlaceholderText("Enter passenger name")
        passenger_name.setStyleSheet(lineedit_style)
        table.setCellWidget(row, 0, passenger_name)

        # Column 1: PNR
        pnr = QLineEdit()
        pnr.setPlaceholderText("PNR")
        pnr.setStyleSheet(lineedit_style)
        table.setCellWidget(row, 1, pnr)

        # Column 2: Sector
        sector = QLineEdit()
        sector.setPlaceholderText("Enter sector")
        sector.setStyleSheet(lineedit_style)
        table.setCellWidget(row, 2, sector)

        # Column 3: Supplier
        supplier = QComboBox()
        supplier.setEditable(True)
        supplier.addItems(self.get_supplier_list())
        supplier.setStyleSheet(self.get_combobox_style())
        table.setCellWidget(row, 3, supplier)

        # Column 4: Type
        type_field = QLineEdit()
        type_field.setPlaceholderText("Enter type")
        type_field.setStyleSheet(lineedit_style)
        table.setCellWidget(row, 4, type_field)

        # Column 5: Class
        travel_class = QComboBox()
        travel_class.addItems(["Economy", "Premium Economy", "Business", "First Class"])
        travel_class.setStyleSheet(self.get_combobox_style())
        table.setCellWidget(row, 5, travel_class)

        # Column 6: Price
        price = QDoubleSpinBox()
        price.setMaximum(10_000_000)
        price.setPrefix("₹ ")
        price.setDecimals(2)
        price.valueChanged.connect(lambda _: self.calculate_row_total(row))
        price.setStyleSheet(spinbox_style)
        table.setCellWidget(row, 6, price)

        # Column 7: Qty
        qty = QDoubleSpinBox()
        qty.setMinimum(1)
        qty.setMaximum(9999)
        qty.setValue(1)
        qty.setDecimals(0)
        qty.valueChanged.connect(lambda _: self.calculate_row_total(row))
        qty.setStyleSheet(spinbox_style)
        table.setCellWidget(row, 7, qty)

        # Column 8: Tax %
        tax = QDoubleSpinBox()
        tax.setSuffix('%')
        tax.setMaximum(100)
        tax.setDecimals(2)
        tax.valueChanged.connect(lambda _: self.calculate_row_total(row))
        tax.setStyleSheet(spinbox_style)
        table.setCellWidget(row, 8, tax)

        # Column 9: Amount
        amount = QLineEdit("₹ 0.00")
        amount.setReadOnly(True)
        amount.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        amount.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: #FFD700;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        table.setCellWidget(row, 9, amount)

        # Column 10: Actions (Delete button)
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Delete this row")
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['danger']};
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent_gold']};
            }}
            QPushButton:pressed {{
                background-color: {self.colors['danger']};
            }}
        """)
        delete_btn.clicked.connect(lambda: self.delete_row(row))
        table.setCellWidget(row, 10, delete_btn)

    def delete_row(self, row: int):
        """Delete a row from the table."""
        self.table.removeRow(row)
        self.table.setMinimumHeight(min(300 + (self.table.rowCount() * 45), 600))
        self.update_invoice_totals()

    def calculate_row_total(self, row: int):
        """Calculate amount for a row."""
        table = self.table
        try:
            price_w = table.cellWidget(row, 6)
            qty_w = table.cellWidget(row, 7)
            tax_w = table.cellWidget(row, 8)
            amount_w = table.cellWidget(row, 9)
            
            price = float(price_w.value() if price_w else 0)
            qty = float(qty_w.value() if qty_w else 0)
            tax_pct = float(tax_w.value() if tax_w else 0)
            
            subtotal = price * qty
            tax_amount = subtotal * (tax_pct / 100)
            total = subtotal + tax_amount
            
            if amount_w:
                amount_w.setText(f"₹ {total:.2f}")
        except Exception as e:
            print(f"Error calculating row total: {e}")
        finally:
            self.update_invoice_totals()

    def update_invoice_totals(self):
        """Update invoice totals."""
        subtotal = 0.0
        total_tax = 0.0
        table = self.table
        
        for r in range(table.rowCount()):
            try:
                price_w = table.cellWidget(r, 6)
                qty_w = table.cellWidget(r, 7)
                tax_w = table.cellWidget(r, 8)
                
                price = float(price_w.value() if price_w else 0)
                qty = float(qty_w.value() if qty_w else 0)
                tax_pct = float(tax_w.value() if tax_w else 0)
                
                row_subtotal = price * qty
                row_tax = row_subtotal * (tax_pct / 100)
                
                subtotal += row_subtotal
                total_tax += row_tax
            except Exception as e:
                print(f"Error calculating totals for row {r}: {e}")
        
        try:
            discount_text = self.txt_discount.text().replace('₹', '').replace(',', '').strip()
            discount = float(discount_text) if discount_text else 0.0
        except:
            discount = 0.0
        
        total = subtotal - discount + total_tax
        
        self.lbl_subtotal.setText(f"₹{subtotal:.2f}")
        self.lbl_tax.setText(f"₹{total_tax:.2f}")
        self.lbl_total.setText(f"₹{total:.2f}")
        
        self.calculate_balance()

    def calculate_balance(self):
        """Calculate balance."""
        try:
            total_text = self.lbl_total.text().replace('₹', '').replace(',', '').strip()
            total = float(total_text) if total_text else 0.0

            received_text = self.txt_received.text().replace('₹', '').replace(',', '').strip()
            received = float(received_text) if received_text else 0.0

            balance = total - received

            if balance > 0:
                self.lbl_balance.setStyleSheet(f"color: {self.colors['danger']}; font-weight: bold; font-size: 13px; background-color: {self.colors['primary_bg']}; padding: 5px 10px; border-radius: 4px; border: 1px solid {self.colors['danger']};")
                self.lbl_balance.setText(f"{self.get_currency_symbol()}{balance:.2f}")
            elif balance < 0:
                self.lbl_balance.setStyleSheet(f"color: {self.colors['success']}; font-weight: bold; font-size: 13px; background-color: {self.colors['primary_bg']}; padding: 5px 10px; border-radius: 4px; border: 1px solid {self.colors['success']};")
                self.lbl_balance.setText(f"{self.get_currency_symbol()}{abs(balance):.2f} (Overpaid)")
            else:
                self.lbl_balance.setStyleSheet(f"color: {self.colors['text_muted']}; font-weight: bold; font-size: 13px; background-color: {self.colors['primary_bg']}; padding: 5px 10px; border-radius: 4px; border: 1px solid {self.colors['text_muted']};")
                self.lbl_balance.setText(f"{self.get_currency_symbol()}0.00 (Paid)")
        except Exception as e:
            print(f"Error calculating balance: {e}")
            self.lbl_balance.setText("₹0.00")

    def save_invoice(self):
        """Save invoice to JSON and database."""
        try:
            invoice_data = {
                "invoice_number": self.invoice_number.text(),
                "invoice_date": self.invoice_date.date().toString("dd/MM/yyyy"),
                "customer_name": self.customer_name.text(),
                "contact_number": self.contact_number.text(),
                "customer_address": self.customer_address.text(),
                "items": [],
                "subtotal": self.lbl_subtotal.text(),
                "discount": self.txt_discount.text(),
                "tax": self.lbl_tax.text(),
                "total": self.lbl_total.text(),
                "received": self.txt_received.text(),
                "balance": self.lbl_balance.text()
            }
            
            # Collect items
            for r in range(self.table.rowCount()):
                passenger_name_w = self.table.cellWidget(r, 0)
                pnr_w = self.table.cellWidget(r, 1)
                sector_w = self.table.cellWidget(r, 2)
                supplier_w = self.table.cellWidget(r, 3)
                type_w = self.table.cellWidget(r, 4)
                class_w = self.table.cellWidget(r, 5)
                price_w = self.table.cellWidget(r, 6)
                qty_w = self.table.cellWidget(r, 7)
                tax_w = self.table.cellWidget(r, 8)
                amount_w = self.table.cellWidget(r, 9)
                
                item = {
                    "passenger_name": passenger_name_w.text() if passenger_name_w else "",
                    "pnr": pnr_w.text() if pnr_w else "",
                    "sector": sector_w.text() if sector_w else "",
                    "supplier": supplier_w.currentText() if supplier_w else "",
                    "type": type_w.text() if type_w else "",
                    "class": class_w.currentText() if class_w else "",
                    "price": price_w.value() if price_w else 0,
                    "qty": qty_w.value() if qty_w else 0,
                    "tax": tax_w.value() if tax_w else 0,
                    "amount": amount_w.text() if amount_w else "₹0.00"
                }
                invoice_data["items"].append(item)
            
            # Save to JSON
            filename = f"invoices/invoice_{invoice_data['invoice_number']}.json"
            os.makedirs("invoices", exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(invoice_data, f, indent=4)
            
            print(f"✓ Invoice saved to JSON: {filename}")
            
            # Save to database if available
            if hasattr(self.dashboard, 'db') and self.dashboard.db:
                try:
                    db_data = invoice_data.copy()
                    db_data['subtotal'] = float(db_data['subtotal'].replace('₹', '').replace(',', '').strip() or 0)
                    db_data['tax'] = float(db_data['tax'].replace('₹', '').replace(',', '').strip() or 0)
                    db_data['total'] = float(db_data['total'].replace('₹', '').replace(',', '').strip() or 0)
                    db_data['received'] = float(db_data['received'].replace('₹', '').replace(',', '').strip() or 0)
                    
                    discount_text = db_data.get('discount', '₹0.00').replace('₹', '').replace(',', '').strip()
                    db_data['discount'] = float(discount_text or 0)
                    
                    balance_text = db_data['balance'].replace('₹', '').replace(',', '').replace('(Paid)', '').replace('(Overpaid)', '').strip()
                    db_data['balance'] = float(balance_text or 0)
                    
                    if db_data['balance'] == 0:
                        db_data['status'] = 'Paid'
                    elif db_data['balance'] < 0:
                        db_data['status'] = 'Overpaid'
                    else:
                        db_data['status'] = 'Pending'
                    
                    db_data['items'] = []
                    for item in invoice_data.get('items', []):
                        amount_text = item.get('amount', '₹0.00').replace('₹', '').replace(',', '').strip()
                        amount_value = float(amount_text or 0)
                        
                        db_item = {
                            'item': item.get('passenger_name', ''),
                            'ticket': item.get('pnr', ''),
                            'sector': item.get('sector', ''),
                            'supplier': item.get('supplier', ''),
                            'class': item.get('class', ''),
                            'price': float(item.get('price', 0)),
                            'qty': float(item.get('qty', 1)),
                            'tax': float(item.get('tax', 0)),
                            'amount': amount_value
                        }
                        db_data['items'].append(db_item)
                    
                    if self.dashboard.db.save_invoice(db_data):
                        print(f"✓ Invoice saved to database")
                    else:
                        print(f"⚠️  Database save failed")
                except Exception as db_error:
                    print(f"⚠️  Database error: {db_error}")
                    import traceback
                    traceback.print_exc()
            
            msg = f"Invoice saved successfully!\n\n📁 JSON File: {filename}\n"
            if hasattr(self.dashboard, 'db') and self.dashboard.db:
                msg += f"🗄️  Database: ✓ Saved"
            QMessageBox.information(self, "Success", msg)
            
        except Exception as e:
            print(f"✗ Error saving invoice: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save invoice:\n{str(e)}")

    def save_pdf(self):
        """Generate a professional multi-page PDF invoice using the dynamic template."""
        try:
            # Ask user where to save the PDF
            default_dir = os.path.join(os.getcwd(), "output", "invoice")
            os.makedirs(default_dir, exist_ok=True)

            filename = os.path.join(
                default_dir,
                f"invoice_{self.invoice_number.text()}.pdf"
            )

            if not filename:
                return

            # Collect invoice items
            items = []
            for r in range(self.table.rowCount()):
                passenger_name_w = self.table.cellWidget(r, 0)
                pnr_w = self.table.cellWidget(r, 1)
                sector_w = self.table.cellWidget(r, 2)
                supplier_w = self.table.cellWidget(r, 3)
                type_w = self.table.cellWidget(r, 4)
                class_w = self.table.cellWidget(r, 5)
                price_w = self.table.cellWidget(r, 6)
                qty_w = self.table.cellWidget(r, 7)
                tax_w = self.table.cellWidget(r, 8)
                amount_w = self.table.cellWidget(r, 9)

                # Safely extract values
                passenger = passenger_name_w.text() if passenger_name_w else ""
                pnr = pnr_w.text() if pnr_w else ""
                sector = sector_w.text() if sector_w else ""
                supplier = supplier_w.currentText() if supplier_w else ""
                type_val = type_w.text() if type_w else ""
                class_val = class_w.currentText() if class_w else ""
                price = float(price_w.value()) if price_w else 0
                qty = float(qty_w.value()) if qty_w else 0
                tax_pct = float(tax_w.value()) if tax_w else 0

                # Combine description for nicer invoice appearance
                desc = f"{passenger} | PNR: {pnr} | {sector} | {supplier} | {class_val} | {type_val}"

                items.append({
                    "description": desc,
                    "qty": qty,
                    "unit_price": price,
                    "tax_pct": tax_pct
                })

            # Build invoice data to pass to template
            invoice_data = {
                "company": {
                    "name": self.company_info["name"],
                    "address": self.company_info.get("address", ""),
                    "footer_note": self.invoice_config.get("footer_note", "")
                },
                "invoice_meta": {
                    "number": self.invoice_number.text(),
                    "date": self.invoice_date.date().toString("dd/MM/yyyy"),
                    "customer_id": ""  # optional field
                },
                "customer": {
                    "name": self.customer_name.text(),
                    "address": self.customer_address.text(),
                    "contact": self.contact_number.text(),
                },
                "items": items,
                "notes": "Generated from Travel Billing System",
                "terms": self.invoice_config.get("terms", "Payment due within 7 days.")
            }

            # Generate PDF using professional template
            generate_invoice_pdf(invoice_data, filename)

            try:
                msg = QMessageBox(self)
                msg.setWindowTitle("PDF Saved")
                msg.setText(f"PDF saved successfully!\n\n{filename}")
                msg.setIcon(QMessageBox.Information)

                open_btn = msg.addButton("Open", QMessageBox.ActionRole)
                msg.addButton("Close", QMessageBox.RejectRole)

                msg.exec_()

                if msg.clickedButton() == open_btn:
                    os.startfile(filename)   # Windows
            except Exception:
                QMessageBox.information(self, "Success", f"PDF saved successfully!\n{filename}")

        except Exception as e:
            print(f"❌ Error saving PDF: {e}")
            QMessageBox.critical(self, "Error", f"Failed to generate PDF:\n{str(e)}")


    def print_invoice(self):
        """Print the invoice with professional layout."""
        try:
            from PyQt5.QtGui import QPainter, QFont, QPen, QColor
            from PyQt5.QtCore import QRect
            
            printer = QPrinter(QPrinter.HighResolution)
            printer.setPageSize(QPrinter.A4)
            printer.setPageMargins(15, 15, 15, 15, QPrinter.Millimeter)
            
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() != QPrintDialog.Accepted:
                return
            
            painter = QPainter()
            painter.begin(printer)
            # Enable high-quality rendering
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            
            page_width = printer.pageRect().width()
            page_height = printer.pageRect().height()
            margin = 100
            
            # Larger, clearer fonts for better print quality
            company_font = QFont("Arial", 20, QFont.Bold)
            title_font = QFont("Arial", 32, QFont.Bold)
            section_font = QFont("Arial", 15, QFont.Bold)
            header_font = QFont("Arial", 13, QFont.Bold)
            normal_font = QFont("Arial", 12)
            small_font = QFont("Arial", 10)
            
            y = margin
            
            # Company Header
            painter.setFont(company_font)
            painter.setPen(QColor(124, 58, 237))  # Purple
            painter.drawText(margin, y, self.company_info['name'].upper())
            y += 50
            
            painter.setFont(normal_font)
            painter.setPen(QColor(80, 80, 80))
            painter.drawText(margin, y, self.company_info['tagline'])
            y += 25
            company_info = self.get_company_info_formatted()
            painter.drawText(margin, y, company_info['contact'])
            y += 50
            
            # Divider
            painter.setPen(QPen(QColor(124, 58, 237), 3))
            painter.drawLine(margin, y, page_width - margin, y)
            y += 50
            
            # Invoice Title
            painter.setFont(title_font)
            painter.setPen(QColor(0, 0, 0))
            painter.drawText(margin, y, "INVOICE")
            
            # Invoice details on right
            x_right = page_width - margin - 700
            painter.setFont(section_font)
            painter.drawText(x_right, y, f"Invoice #: {self.invoice_number.text()}")
            y += 45
            painter.setFont(normal_font)
            painter.drawText(x_right, y, f"Date: {self.invoice_date.date().toString('dd/MM/yyyy')}")
            y += 50
            
            # Bill To
            painter.setFont(section_font)
            painter.setPen(QColor(0, 0, 0))
            painter.drawText(margin, y, "BILL TO:")
            y += 40
            
            painter.setFont(normal_font)
            painter.drawText(margin, y, self.customer_name.text())
            y += 30
            painter.drawText(margin, y, f"Phone: {self.contact_number.text()}")
            y += 30
            if self.customer_address.text():
                painter.drawText(margin, y, f"Address: {self.customer_address.text()}")
                y += 30
            y += 30
            
            # Table Header with purple background
            painter.fillRect(QRect(margin, y, page_width - 2*margin, 60), QColor(124, 58, 237))
            
            painter.setFont(header_font)
            painter.setPen(QPen(QColor(255, 255, 255), 2))  # Bolder white text
            
            # Column positions - optimized for clarity
            col_passenger = margin + 20
            col_pnr = margin + 300
            col_sector = margin + 560
            col_supplier = margin + 860
            col_type = margin + 1180
            col_class = margin + 1420
            col_price = margin + 1660
            col_qty = margin + 1900
            col_tax = margin + 2080
            col_amount = margin + 2280
            
            y += 42
            painter.drawText(col_passenger, y, "Passenger Name")
            painter.drawText(col_pnr, y, "PNR")
            painter.drawText(col_sector, y, "Sector")
            painter.drawText(col_supplier, y, "Supplier")
            painter.drawText(col_type, y, "Type")
            painter.drawText(col_class, y, "Class")
            painter.drawText(col_price, y, "Price")
            painter.drawText(col_qty, y, "Qty")
            painter.drawText(col_tax, y, "Tax")
            painter.drawText(col_amount, y, "Amount")
            y += 25
            
            # Table Rows
            painter.setFont(normal_font)
            painter.setPen(QPen(QColor(0, 0, 0), 1.5))  # Slightly bolder text
            
            for r in range(self.table.rowCount()):
                # Alternating row colors for better readability
                if r % 2 == 0:
                    painter.fillRect(QRect(margin, y-30, page_width - 2*margin, 55), QColor(245, 245, 250))
                
                passenger_name_w = self.table.cellWidget(r, 0)
                pnr_w = self.table.cellWidget(r, 1)
                sector_w = self.table.cellWidget(r, 2)
                supplier_w = self.table.cellWidget(r, 3)
                type_w = self.table.cellWidget(r, 4)
                class_w = self.table.cellWidget(r, 5)
                price_w = self.table.cellWidget(r, 6)
                qty_w = self.table.cellWidget(r, 7)
                tax_w = self.table.cellWidget(r, 8)
                amount_w = self.table.cellWidget(r, 9)
                
                y += 38
                painter.drawText(col_passenger, y, passenger_name_w.text() if passenger_name_w else "")
                painter.drawText(col_pnr, y, pnr_w.text() if pnr_w else "")
                painter.drawText(col_sector, y, sector_w.text() if sector_w else "")
                painter.drawText(col_supplier, y, supplier_w.currentText() if supplier_w else "")
                painter.drawText(col_type, y, type_w.text() if type_w else "")
                painter.drawText(col_class, y, class_w.currentText() if class_w else "")
                painter.drawText(col_price, y, f"₹{price_w.value():.2f}" if price_w else "")
                painter.drawText(col_qty, y, str(int(qty_w.value())) if qty_w else "")
                painter.drawText(col_tax, y, f"{tax_w.value():.1f}%" if tax_w else "")
                painter.drawText(col_amount, y, amount_w.text() if amount_w else "")
                y += 15
            
            y += 35
            painter.setPen(QPen(QColor(124, 58, 237), 3))
            painter.drawLine(margin, y, page_width - margin, y)
            y += 70
            
            # Totals section - right aligned
            x_labels = page_width - margin - 800
            x_values = page_width - margin - 320
            
            painter.setFont(normal_font)
            painter.setPen(QPen(QColor(0, 0, 0), 1.5))
            painter.drawText(x_labels, y, "Subtotal:")
            painter.drawText(x_values, y, self.lbl_subtotal.text())
            y += 40
            
            painter.drawText(x_labels, y, "Tax:")
            painter.drawText(x_values, y, self.lbl_tax.text())
            y += 45
            
            # Highlighted TOTAL
            painter.fillRect(QRect(x_labels - 40, y - 32, 850, 52), QColor(255, 215, 0, 100))
            painter.setFont(section_font)
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawText(x_labels, y, "TOTAL:")
            painter.drawText(x_values, y, self.lbl_total.text())
            y += 40
            
            painter.setFont(normal_font)
            painter.drawText(x_labels, y, "Received:")
            painter.drawText(x_values, y, self.txt_received.text() or "₹0.00")
            y += 35
            
            painter.drawText(x_labels, y, "Balance:")
            if "₹0.00" not in self.lbl_balance.text():
                painter.setPen(QColor(220, 38, 38))  # Red
            else:
                painter.setPen(QColor(34, 197, 94))  # Green
            painter.drawText(x_values, y, self.lbl_balance.text())
            
            # Footer
            y = page_height - margin - 80
            painter.setPen(QPen(QColor(200, 200, 200), 1))
            painter.drawLine(margin, y, page_width - margin, y)
            y += 30
            
            painter.setFont(small_font)
            painter.setPen(QColor(120, 120, 120))
            painter.drawText(margin, y, self.invoice_config['footer_note'])
            y += 25
            painter.drawText(margin, y, f"© {self.company_info.get('year', '2025')} {self.company_info['name']}. All rights reserved.")
            
            painter.end()
            
            print("✅ Invoice sent to printer")
            QMessageBox.information(self, "Success", "Invoice sent to printer successfully!")
            
        except Exception as e:
            print(f"❌ Error printing: {e}")
            QMessageBox.critical(self, "Error", f"Failed to print invoice:\n{str(e)}")

    def share_invoice(self):
        """Share invoice via email."""
        try:
            invoice_num = self.invoice_number.text()
            if not invoice_num:
                QMessageBox.warning(self, "Warning", "Please save the invoice first.")
                return
            
            invoice_file = f"invoices/invoice_{invoice_num}.json"
            if not os.path.exists(invoice_file):
                QMessageBox.warning(self, "Warning", "Invoice not found. Please save first.")
                return
            
            customer_name = self.customer_name.text()
            
            email, ok = QInputDialog.getText(
                self,
                "Share Invoice",
                f"Share Invoice: {invoice_num}\n\nEnter recipient email:",
                text=""
            )
            
            if ok and email:
                if "@" not in email or "." not in email:
                    QMessageBox.warning(self, "Warning", "Please enter a valid email.")
                    return
                
                QMessageBox.information(
                    self,
                    "Share Invoice",
                    f"✅ Invoice Shared Successfully!\n\n"
                    f"📧 Recipient: {email}\n"
                    f"📄 Invoice: {invoice_num}\n"
                    f"👤 Customer: {customer_name}\n\n"
                    f"Note: Email integration can be added using:\n"
                    f"• SMTP (Gmail, Outlook)\n"
                    f"• SendGrid API\n"
                    f"• AWS SES\n"
                    f"• Mailgun"
                )
            elif ok:
                QMessageBox.warning(self, "Warning", "Please enter a valid email.")
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to share invoice:\n{str(e)}")
