"""
Home Page Module
Contains invoice creation, item management, and invoice operations.
Optimized for high-speed data entry.
"""
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
                             QFrame, QScrollArea, QTableWidget, QPushButton, QLineEdit,
                             QComboBox, QDoubleSpinBox, QDateEdit, QHeaderView, 
                              QApplication, QMessageBox, QInputDialog, QDialog)
from PyQt6.QtGui import QShortcut
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QDate, QEvent
from PyQt6.QtGui import QKeySequence

from utils.invoice_generator import generate_invoice_pdf
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from travel_billing_software.utils.styles import get_label_style

class PassportDetailsDialog(QDialog):
    """Dialog for entering passenger passport details."""
    
    def __init__(self, passenger_name="", parent=None):
        super().__init__(parent)
        self.passenger_name = passenger_name
        self.passport_data = {}
        self.setWindowTitle(f"Passport Details - {passenger_name}")
        self.setMinimumWidth(700)
        self.setMinimumHeight(650)
        self._init_ui()
    
    def _init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Set window background to white
        self.setStyleSheet("QWidget { background-color: #f5f5f5; }")
        
        # Create card frame to contain all content
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e5e7eb;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel(f"<h2>Passport Information</h2>")
        title.setStyleSheet("color: #7C3AED; font-weight: bold;")
        card_layout.addWidget(title)
        
        # Passenger name display
        name_label = QLabel(f"<b>Passenger:</b> {self.passenger_name}")
        name_label.setStyleSheet("color: #333; font-size: 14px; padding: 10px; background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 5px;")
        card_layout.addWidget(name_label)
        
        # Form fields
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setColumnMinimumWidth(0, 220)  # Label column
        form_layout.setColumnMinimumWidth(1, 380)  # Input column
        
        field_style = "QLineEdit { background-color: white; color: #1f2937; border: 1px solid #d1d5db; border-radius: 3px; padding: 10px; font-size: 20px; } QLineEdit:focus { border: 2px solid #7C3AED; background-color: #faf5ff; }"
        date_style = "QDateEdit { background-color: white; color: #1f2937; border: 1px solid #d1d5db; border-radius: 3px; padding: 10px; font-size: 20px; } QDateEdit:focus { border: 2px solid #7C3AED; background-color: #faf5ff; }"
        
        # Set label style for all form labels
        label_style = "color: #374151; font-size: 20px; font-weight: 500;"
        
        # Passport Number *
        passport_num_label = QLabel("<b>Passport Number: *</b>")
        passport_num_label.setStyleSheet(label_style)
        form_layout.addWidget(passport_num_label, 0, 0)
        self.passport_number = QLineEdit()
        self.passport_number.setPlaceholderText("Enter passport number")
        self.passport_number.setStyleSheet(field_style)
        form_layout.addWidget(self.passport_number, 0, 1)
        
        # Full Name *
        full_name_label = QLabel("<b>Full Name (as in passport): *</b>")
        full_name_label.setStyleSheet(label_style)
        form_layout.addWidget(full_name_label, 1, 0)
        self.full_name = QLineEdit()
        self.full_name.setText(self.passenger_name)
        self.full_name.setStyleSheet(field_style)
        form_layout.addWidget(self.full_name, 1, 1)
        
        # Date of Birth *
        dob_label = QLabel("<b>Date of Birth: *</b>")
        dob_label.setStyleSheet(label_style)
        form_layout.addWidget(dob_label, 2, 0)
        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDate(QDate.currentDate().addYears(-30))
        self.dob.setStyleSheet(date_style)
        form_layout.addWidget(self.dob, 2, 1)
        
        # Nationality *
        nationality_label = QLabel("<b>Nationality: *</b>")
        nationality_label.setStyleSheet(label_style)
        form_layout.addWidget(nationality_label, 3, 0)
        self.nationality = QLineEdit()
        self.nationality.setPlaceholderText("e.g., Indian")
        self.nationality.setStyleSheet(field_style)
        form_layout.addWidget(self.nationality, 3, 1)
        
        # Gender *
        gender_label = QLabel("<b>Gender: *</b>")
        gender_label.setStyleSheet(label_style)
        form_layout.addWidget(gender_label, 4, 0)
        self.gender = QComboBox()
        self.gender.addItems(["Select", "Male", "Female", "Other"])
        self.gender.setStyleSheet("QComboBox { background-color: white; color: #1f2937; border: 1px solid #d1d5db; padding: 10px; border-radius: 3px; font-size: 14px; } QComboBox:focus { border: 2px solid #7C3AED; background-color: #faf5ff; } QComboBox::drop-down { border: none; } QComboBox QAbstractItemView { background-color: white; color: #1f2937; selection-background-color: #e9d5ff; font-size: 14px; }")
        form_layout.addWidget(self.gender, 4, 1)
        
        # Place of Birth
        pob_label = QLabel("<b>Place of Birth:</b>")
        pob_label.setStyleSheet(label_style)
        form_layout.addWidget(pob_label, 5, 0)
        self.place_of_birth = QLineEdit()
        self.place_of_birth.setPlaceholderText("City, Country")
        self.place_of_birth.setStyleSheet(field_style)
        form_layout.addWidget(self.place_of_birth, 5, 1)
        
        # Issue Date *
        issue_date_label = QLabel("<b>Issue Date: *</b>")
        issue_date_label.setStyleSheet(label_style)
        form_layout.addWidget(issue_date_label, 6, 0)
        self.issue_date = QDateEdit()
        self.issue_date.setCalendarPopup(True)
        self.issue_date.setDate(QDate.currentDate().addYears(-2))
        self.issue_date.setStyleSheet(date_style)
        form_layout.addWidget(self.issue_date, 6, 1)
        
        # Expiry Date *
        expiry_date_label = QLabel("<b>Expiry Date: *</b>")
        expiry_date_label.setStyleSheet(label_style)
        form_layout.addWidget(expiry_date_label, 7, 0)
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate().addYears(8))
        self.expiry_date.setStyleSheet(date_style)
        form_layout.addWidget(self.expiry_date, 7, 1)
        
        # Issuing Authority *
        issuing_auth_label = QLabel("<b>Issuing Authority: *</b>")
        issuing_auth_label.setStyleSheet(label_style)
        form_layout.addWidget(issuing_auth_label, 8, 0)
        self.issuing_authority = QLineEdit()
        self.issuing_authority.setPlaceholderText("e.g., Govt. of India")
        self.issuing_authority.setStyleSheet(field_style)
        form_layout.addWidget(self.issuing_authority, 8, 1)
        
        card_layout.addLayout(form_layout)
        
        # Note about mandatory fields
        note = QLabel("<i>* Mandatory fields</i>")
        note.setStyleSheet("color: #dc2626; font-size: 12px;")
        card_layout.addWidget(note)
        
        card_layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("💾 Save Passport Details")
        save_btn.setStyleSheet("QPushButton { background-color: #10B981; color: white; border: none; border-radius: 5px; padding: 10px 20px; font-weight: bold; } QPushButton:hover { background-color: #059669; }")
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save_btn.clicked.connect(self.save_details)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("QPushButton { background-color: #6B7280; color: white; border: none; border-radius: 5px; padding: 10px 20px; font-weight: bold; } QPushButton:hover { background-color: #4B5563; }")
        cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(cancel_btn)
        
        card_layout.addLayout(btn_layout)
        
        # Add card to main layout
        main_layout.addWidget(card)
    
    def save_details(self):
        """Validate and save passport details."""
        # Validate mandatory fields
        if not self.passport_number.text().strip():
            QMessageBox.warning(self, "Missing Information", "Passport Number is required.")
            return
        if not self.full_name.text().strip():
            QMessageBox.warning(self, "Missing Information", "Full Name is required.")
            return
        if not self.nationality.text().strip():
            QMessageBox.warning(self, "Missing Information", "Nationality is required.")
            return
        if self.gender.currentText() == "Select":
            QMessageBox.warning(self, "Missing Information", "Please select Gender.")
            return
        if not self.issuing_authority.text().strip():
            QMessageBox.warning(self, "Missing Information", "Issuing Authority is required.")
            return
        
        # Save data
        self.passport_data = {
            'passport_number': self.passport_number.text().strip(),
            'full_name': self.full_name.text().strip(),
            'date_of_birth': self.dob.date().toString("yyyy-MM-dd"),
            'nationality': self.nationality.text().strip(),
            'gender': self.gender.currentText(),
            'place_of_birth': self.place_of_birth.text().strip(),
            'issue_date': self.issue_date.date().toString("yyyy-MM-dd"),
            'expiry_date': self.expiry_date.date().toString("yyyy-MM-dd"),
            'issuing_authority': self.issuing_authority.text().strip()
        }
        
        QMessageBox.information(self, "Success", f"Passport details saved for {self.full_name.text()}!")
        self.accept()  # Close dialog with accepted status

class HomePage(QWidget):
    """Home page with invoice creation and management."""
    
    def __init__(self, colors, company_info, invoice_config, app_config,
                 get_frame_style, get_input_style, get_dateedit_style, get_combobox_style,
                 get_invoice_prefix, get_currency_symbol, get_supplier_list, get_company_info_formatted,
                 dashboard_ref):
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
        self.show_dialog_window = False 
        
        self._init_ui()
        self._setup_speed_features() # Initialize speed features

    def _init_ui(self):
        """Initialize the UI components."""
        # Create scroll area for entire page
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

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
        welcome_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        
        # Invoice Details Title
        invoice_title = QLabel(f"<b style='color:{self.colors['accent_secondary']}; font-size:16px;'>📄 Invoice Details</b>")
        invoice_layout.addWidget(invoice_title, 0, 0, 1, 4)
        
        # --- REORDERED FOR SPEED: Customer Name First ---
        
        # Row 1: Customer Name & Contact
        lbl_cust_name = QLabel("Customer Name:")
        lbl_cust_name.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        lbl_cust_name.setAlignment(
    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
)

        invoice_layout.addWidget(lbl_cust_name, 1, 0)
        
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        self.customer_name.setStyleSheet(self.get_input_style())
        self.customer_name.setMinimumWidth(250)
        invoice_layout.addWidget(self.customer_name, 1, 1)
        
        lbl_contact = QLabel("Contact Number:")
        lbl_contact.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        lbl_contact.setAlignment(
    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
)

        invoice_layout.addWidget(lbl_contact, 1, 2)
        
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Enter contact number")
        self.contact_number.setStyleSheet(self.get_input_style())
        self.contact_number.setMinimumWidth(255)
        invoice_layout.addWidget(self.contact_number, 1, 3)
        
        # Row 2: Address
        lbl_address = QLabel("Address:")
        lbl_address.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        lbl_address.setAlignment(
    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
) 
        invoice_layout.addWidget(lbl_address, 2, 0)
        
        self.customer_address = QLineEdit()
        self.customer_address.setPlaceholderText("Enter customer address")
        self.customer_address.setStyleSheet(self.get_input_style())
        self.customer_address.setMinimumWidth(250)
        invoice_layout.addWidget(self.customer_address, 2, 1, 1, 3)

        # Row 3: Invoice Info (Auto-filled usually, so placed last in tab order visual)
        lbl_inv_num = QLabel("Invoice Number:")
        lbl_inv_num.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        lbl_inv_num.setAlignment(
    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
)
        invoice_layout.addWidget(lbl_inv_num, 3, 0)
        
        self.invoice_number = QLineEdit()
        self.invoice_number.setText(self.generate_invoice_number())
        self.invoice_number.setPlaceholderText("Auto-generated")
        self.invoice_number.setStyleSheet(self.get_input_style())
        self.invoice_number.setMinimumWidth(250)
        invoice_layout.addWidget(self.invoice_number, 3, 1)
        
        lbl_inv_date = QLabel("Invoice Date:")
        lbl_inv_date.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        lbl_inv_date.setAlignment(
    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
)
        invoice_layout.addWidget(lbl_inv_date, 3, 2)
        
        self.invoice_date = QDateEdit()
        self.invoice_date.setDate(QDate.currentDate())
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDisplayFormat(self.invoice_config['date_format'])
        self.invoice_date.setStyleSheet(self.get_dateedit_style())
        self.invoice_date.setMinimumWidth(250)
        invoice_layout.addWidget(self.invoice_date, 3, 3)

        # Set Explicit Tab Order for Speed
        QWidget.setTabOrder(self.customer_name, self.contact_number)
        QWidget.setTabOrder(self.contact_number, self.customer_address)
        QWidget.setTabOrder(self.customer_address, self.invoice_date)
        QWidget.setTabOrder(self.invoice_date, self.invoice_number)
        
        return invoice_details_frame

    # ... [Keep _create_table_section, _create_calculation_section, _create_action_buttons exactly as they were in previous code] ...
    # I will paste them here briefly to ensure the file is complete, but the logic remains mostly the same
    # except we need to ensure the "Add Item" button is accessible via Tab

    def _create_table_section(self) -> QFrame:
        table_frame = QFrame()
        table_frame.setStyleSheet("QFrame { background-color: #2a2a2a; border-radius: 8px; border: 1px solid #444; }")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        table_header_layout = QHBoxLayout()
        table_title = QLabel("<b style='color:#a78bfa; font-size:14px;'>🧾 Billed Items </b>")
        table_header_layout.addWidget(table_title)
        table_header_layout.addStretch()
        
        self.btn_add_item = QPushButton("➕ Add Item")
        self.btn_add_item.setStyleSheet(f"QPushButton {{ background-color: {self.colors['accent_primary']}; color: white; border: none; border-radius: 5px; padding: 8px 16px; font-weight: bold; font-size: 12px; }} QPushButton:hover {{ background-color: {self.colors['accent_secondary']}; }}")
        self.btn_add_item.clicked.connect(self.add_item_row)
        self.btn_add_item.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_add_item.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
 # Make sure it catches tab
        table_header_layout.addWidget(self.btn_add_item)
        table_layout.addLayout(table_header_layout)
        
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels(["Passenger Name", "PNR", "Sector", "Supplier", "Type", "Qty", "Supp. Amt (₹)", "Cust. Amt (₹)", "Actions"])
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setMinimumHeight(200)
        table_layout.addWidget(self.table)
        
        # Link Tab Order from Invoice Details to Add Button
        QWidget.setTabOrder(self.invoice_number, self.btn_add_item)
        
        return table_frame

    def _create_calculation_section(self) -> QFrame:
        calc_frame = QFrame()
        calc_frame.setStyleSheet(f"QFrame {{ background-color: {self.colors['secondary_bg']}; border-radius: 8px; border: 1px solid {self.colors['accent_primary']}; padding: 10px; }}")
        calc_main_layout = QVBoxLayout(calc_frame)
        calc_main_layout.setContentsMargins(10, 10, 10, 10)
        
        calc_title = QLabel("<b style='color:#a78bfa; font-size:16px;'>💰 Invoice Calculation</b>")
        calc_main_layout.addWidget(calc_title)
        
        calc_grid = QGridLayout()
        calc_grid.setSpacing(15)
        
        # Labels and Fields
        subtotal_lbl = QLabel("Subtotal:"); subtotal_lbl.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold;")
        self.lbl_subtotal = QLabel(f"{self.get_currency_symbol()}0.00"); self.lbl_subtotal.setStyleSheet(f"color: {self.colors['accent_secondary']}; font-weight: bold; background-color: {self.colors['primary_bg']}; padding: 8px; border-radius: 5px;")
        
        discount_lbl = QLabel("Discount:"); discount_lbl.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold;")
        self.txt_discount = QLineEdit(); self.txt_discount.setPlaceholderText("0.00"); self.txt_discount.setText("0.00")
        self.txt_discount.setStyleSheet(f"QLineEdit {{ background-color: {self.colors['primary_bg']}; color: {self.colors['accent_secondary']}; border: 1px solid {self.colors['accent_secondary']}; padding: 8px; font-weight: bold; }}")
        self.txt_discount.textChanged.connect(self.update_invoice_totals)
        
        tax_lbl = QLabel("Tax:"); tax_lbl.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold;")
        self.lbl_tax = QLabel(f"{self.get_currency_symbol()}0.00"); self.lbl_tax.setStyleSheet(self.lbl_subtotal.styleSheet())
        
        total_lbl = QLabel("Total:"); total_lbl.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold;")
        self.lbl_total = QLabel(f"{self.get_currency_symbol()}0.00"); self.lbl_total.setStyleSheet(f"color: {self.colors['accent_gold']}; font-weight: bold; background-color: {self.colors['primary_bg']}; padding: 8px; border: 2px solid {self.colors['accent_gold']};")
        
        received_lbl = QLabel("Received:"); received_lbl.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold;")
        self.txt_received = QLineEdit(); self.txt_received.setPlaceholderText("0.00")
        self.txt_received.setStyleSheet(f"QLineEdit {{ background-color: {self.colors['primary_bg']}; color: {self.colors['success']}; border: 1px solid {self.colors['success']}; padding: 8px; font-weight: bold; }}")
        self.txt_received.textChanged.connect(self.calculate_balance)
        
        balance_lbl = QLabel("Balance:"); balance_lbl.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold;")
        self.lbl_balance = QLabel(f"{self.get_currency_symbol()}0.00"); self.lbl_balance.setStyleSheet(f"color: {self.colors['danger']}; font-weight: bold; background-color: {self.colors['primary_bg']}; padding: 8px; border: 1px solid {self.colors['danger']};")

        # Layout Placement
        calc_grid.addWidget(subtotal_lbl, 0, 0); calc_grid.addWidget(self.lbl_subtotal, 0, 1)
        calc_grid.addWidget(discount_lbl, 1, 0); calc_grid.addWidget(self.txt_discount, 1, 1)
        calc_grid.addWidget(tax_lbl, 2, 0); calc_grid.addWidget(self.lbl_tax, 2, 1)
        
        calc_grid.setColumnMinimumWidth(2, 60) # Spacer
        
        calc_grid.addWidget(total_lbl, 0, 5); calc_grid.addWidget(self.lbl_total, 0, 6)
        calc_grid.addWidget(received_lbl, 1, 5); calc_grid.addWidget(self.txt_received, 1, 6)
        calc_grid.addWidget(balance_lbl, 2, 5); calc_grid.addWidget(self.lbl_balance, 2, 6)
        
        calc_main_layout.addLayout(calc_grid)
        
        # Link Tab Order (Table -> Discount -> Received)
        QWidget.setTabOrder(self.btn_add_item, self.txt_discount)
        QWidget.setTabOrder(self.txt_discount, self.txt_received)
        
        return calc_frame

    def _create_action_buttons(self) -> QHBoxLayout:
        btn_layout = QHBoxLayout()
        
        self.btn_reset = QPushButton("🔄 Reset (Ctrl+N)")
        self.btn_reset.setStyleSheet(f"QPushButton {{ background-color: {self.colors['warning']}; color: white; border: none; border-radius: 5px; padding: 10px 20px; font-weight: bold; }} QPushButton:hover {{ background-color: #f59e0b; }}")
        self.btn_reset.clicked.connect(self.reset_invoice)
        btn_layout.addWidget(self.btn_reset)
        
        btn_layout.addStretch()
        
        self.btn_save_invoice = QPushButton("💾 Save (Ctrl+S)")
        self.btn_save_invoice.setStyleSheet(f"QPushButton {{ background-color: {self.colors['success']}; color: white; border: none; border-radius: 5px; padding: 10px 20px; font-weight: bold; }} QPushButton:hover {{ background-color: {self.colors['accent_cyan']}; }}")
        self.btn_save_invoice.clicked.connect(self.save_invoice)
        btn_layout.addWidget(self.btn_save_invoice)
        
        self.btn_save_pdf = QPushButton("📄 PDF")
        self.btn_save_pdf.setStyleSheet(f"QPushButton {{ background-color: {self.colors['danger']}; color: white; border: none; border-radius: 5px; padding: 10px 20px; font-weight: bold; }} QPushButton:hover {{ background-color: {self.colors['accent_gold']}; }}")
        self.btn_save_pdf.clicked.connect(self.save_pdf)
        btn_layout.addWidget(self.btn_save_pdf)
        
        self.btn_print = QPushButton("🖨️ Print (Ctrl+P)")
        self.btn_print.setStyleSheet("QPushButton { background-color: #9b9bff; color: white; border: none; border-radius: 5px; padding: 10px 20px; font-weight: bold; } QPushButton:hover { background-color: #b5b5ff; }")
        self.btn_print.clicked.connect(self.print_invoice)
        btn_layout.addWidget(self.btn_print)
        
        self.btn_share = QPushButton("📤 Share")
        self.btn_share.setStyleSheet("QPushButton { background-color: #20C997; color: white; border: none; border-radius: 5px; padding: 10px 20px; font-weight: bold; } QPushButton:hover { background-color: #38D9A9; }")
        self.btn_share.clicked.connect(self.share_invoice)
        btn_layout.addWidget(self.btn_share)
        
        # Link Tab Order (Received -> Save Button)
        QWidget.setTabOrder(self.txt_received, self.btn_save_invoice)
        
        return btn_layout

    # ==========================================
    # SPEED FEATURES & EVENT HANDLING
    # ==========================================

    def _setup_speed_features(self):
        """Install shortcuts and initial focus."""
        # 1. Keyboard Shortcuts
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.save_invoice)
        QShortcut(QKeySequence("Ctrl+P"), self).activated.connect(self.print_invoice)
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.reset_invoice)
        QShortcut(QKeySequence("F2"), self).activated.connect(self.add_item_row)
        QShortcut(QKeySequence("Ctrl+I"), self).activated.connect(self.add_item_row)

        # 2. Install Event Filters on Main Inputs for Enter Navigation
        inputs = [self.customer_name, self.contact_number, self.customer_address, 
                  self.invoice_number, self.invoice_date, self.txt_discount, self.txt_received]
        
        for widget in inputs:
            widget.installEventFilter(self)

        # 3. Auto-Focus on Startup (Customer Name)
        # We use a slight delay or call it at end of init to ensure widget is ready
        self.customer_name.setFocus()

    def eventFilter(self, source, event):
        """
        Intercepts key presses to make Enter act like Tab.
        Also handles smart table navigation.
        """
        from PyQt6.QtCore import QEvent

        if event.type() == QEvent.Type.KeyPress:

            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):

                
                # --- CASE 1: Standard Input Fields (Move to Next) ---
                if isinstance(source, (QLineEdit, QDateEdit, QPushButton)) and source is not self.btn_add_item:
                    self.focusNextChild()
                    return True # Consume event
                
                # --- CASE 2: Inside the Table ---
                # We need to detect if focus is inside the table
                # The 'source' here will be the specific widget (LineEdit/SpinBox) inside the cell
                
                # Check if the source is a child of the table
                if self.table.isAncestorOf(source):
                    return self._handle_table_enter_key(source)

        return super().eventFilter(source, event)

    def _handle_table_enter_key(self, current_widget):
        """Handle Enter key logic specifically for table widgets."""
        # Find which cell this widget belongs to
        index = self.table.indexAt(current_widget.pos())
        if not index.isValid():
            # Sometimes pos() is relative to viewport, need mapping. 
            # Easier approach: iterate rows/cols to find widget (slow) or use focusWidget logic.
            # Fast approach:
            for r in range(self.table.rowCount()):
                for c in range(self.table.columnCount()):
                    if self.table.cellWidget(r, c) == current_widget:
                        
                        # Logic: Move Right
                        next_col = c + 1
                        
                        # If we are at the last input column (Tax/Action), move to next row
                        # Column 8 is Tax, Column 9 is Amount (Read only), 10 is Delete
                        if c >= 8: 
                            # If it's the last row, ADD A NEW ROW
                            if r == self.table.rowCount() - 1:
                                self.add_item_row()
                                # Focus first cell of new row
                                new_widget = self.table.cellWidget(r + 1, 0)
                                if new_widget: new_widget.setFocus()
                            else:
                                # Just move to next row first cell
                                next_widget = self.table.cellWidget(r + 1, 0)
                                if next_widget: next_widget.setFocus()
                        else:
                            # Move to next cell in same row
                            next_widget = self.table.cellWidget(r, next_col)
                            # Skip if widget is None or ReadOnly (like Amount col)
                            while (next_widget is None or isinstance(next_widget, QLabel) or 
                                  (isinstance(next_widget, QLineEdit) and next_widget.isReadOnly())):
                                next_col += 1
                                if next_col >= self.table.columnCount(): break
                                next_widget = self.table.cellWidget(r, next_col)
                            
                            if next_widget:
                                next_widget.setFocus()
                                # select all text for quick overwrite
                                if isinstance(next_widget, (QLineEdit, QDoubleSpinBox)):
                                    next_widget.selectAll()
                        
                        return True # Event consumed
        
        return False # Let default handler take it if not found

    def add_item_row(self):
        """Add a new row to the table."""
        table = self.table
        row = table.rowCount()
        table.insertRow(row)
        
        # Set row height for better visibility
        table.setRowHeight(row, 50)
        
        # Adjust table minimum height with increased row height
        self.table.setMinimumHeight(min(250 + (row * 55), 700))

        # Styles with increased font size
        spinbox_style = """
            QDoubleSpinBox { background-color: #2a2a2a; color: #ddd; border: 1px solid #444; border-radius: 3px; padding: 5px; font-size: 14px; }
            QDoubleSpinBox:focus { border: 1px solid #9b9bff; background-color: #333; }
        """
        lineedit_style = """
            QLineEdit { background-color: #2a2a2a; color: #ddd; border: 1px solid #444; border-radius: 3px; padding: 5px; font-size: 14px; }
            QLineEdit:focus { border: 1px solid #9b9bff; background-color: #333; }
        """
        combobox_style = """
            QComboBox { background-color: #2a2a2a; color: #ddd; border: 1px solid #444; padding: 5px; font-size: 14px; }
            QComboBox:focus { border: 1px solid #9b9bff; }
        """

        # --- Create Widgets ---
        passenger_name = QLineEdit(); passenger_name.setPlaceholderText("Name"); passenger_name.setStyleSheet(lineedit_style)
        pnr = QLineEdit(); pnr.setPlaceholderText("PNR"); pnr.setStyleSheet(lineedit_style)
        sector = QLineEdit(); sector.setPlaceholderText("Sector"); sector.setStyleSheet(lineedit_style)
        
        supplier = QComboBox(); supplier.setEditable(True); supplier.addItems(self.get_supplier_list()); supplier.setStyleSheet(combobox_style)
        
        type_field = QLineEdit(); type_field.setPlaceholderText("Type"); type_field.setStyleSheet(lineedit_style)
        
        
        qty = QDoubleSpinBox(); qty.setMinimum(1); qty.setMaximum(9999); qty.setValue(1); qty.setDecimals(0); qty.setStyleSheet(spinbox_style)
        qty.valueChanged.connect(lambda _: self.calculate_row_total(row))
        
        supplier_amount = QDoubleSpinBox(); supplier_amount.setMinimum(0); supplier_amount.setMaximum(999999); supplier_amount.setValue(0); supplier_amount.setDecimals(2); supplier_amount.setStyleSheet(spinbox_style)
        supplier_amount.setPrefix("₹ "); supplier_amount.valueChanged.connect(lambda _: self.update_invoice_totals())
        
        customer_amount = QDoubleSpinBox(); customer_amount.setMinimum(0); customer_amount.setMaximum(999999); customer_amount.setValue(0); customer_amount.setDecimals(2); customer_amount.setStyleSheet(spinbox_style)
        customer_amount.setPrefix("₹ "); customer_amount.valueChanged.connect(lambda _: self.update_invoice_totals())
       
        # Actions column with Add and Delete buttons
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(5)
        
        add_passport_btn = QPushButton("➕")
        add_passport_btn.setFixedWidth(40)
        add_passport_btn.setToolTip("Add Passport Details")
        add_passport_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        add_passport_btn.setStyleSheet(f"QPushButton {{ background-color: {self.colors['accent_primary']}; color: white; border: none; border-radius: 3px; font-weight: bold; font-size: 14px; }} QPushButton:hover {{ background-color: #9333EA; }}")
        add_passport_btn.clicked.connect(lambda: self.open_passport_dialog(row))
        actions_layout.addWidget(add_passport_btn)
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedWidth(40)
        delete_btn.setToolTip("Delete Row")
        delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        delete_btn.setStyleSheet(f"QPushButton {{ background-color: {self.colors['danger']}; color: white; border: none; border-radius: 3px; font-weight: bold; }} QPushButton:hover {{ background-color: {self.colors['accent_gold']}; }}")
        delete_btn.clicked.connect(lambda: self.delete_row(row))
        actions_layout.addWidget(delete_btn)
        
        # --- Set Widgets in Cells ---
        widgets = [passenger_name, pnr, sector, supplier, type_field, qty, supplier_amount, customer_amount, actions_widget]
        for col, w in enumerate(widgets):
            table.setCellWidget(row, col, w)
            # Install Event Filter for Enter Key Navigation on this new widget
            if isinstance(w, (QLineEdit, QComboBox, QDoubleSpinBox)):
                w.installEventFilter(self)

        # Focus the first item of the new row (Passenger Name)
        passenger_name.setFocus()

    def open_passport_dialog(self, row: int):
        """Open passport details dialog for the specified row."""
        try:
            # Get passenger name from the row
            passenger_name_widget = self.table.cellWidget(row, 0)
            passenger_name = passenger_name_widget.text() if passenger_name_widget else "Passenger"
            
            # Create and show passport dialog as modal
            dialog = PassportDetailsDialog(passenger_name, self)
            dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open passport dialog:\n{str(e)}")

    # ==========================================
    # LOGIC FUNCTIONS (Calculations, Saving, etc.)
    # ==========================================

    def generate_invoice_number(self):
        now = datetime.now()
        return f"{self.get_invoice_prefix()}-{now.strftime('%Y%m%d-%H%M%S')}"

    def delete_row(self, row: int):
        self.table.removeRow(row)
        self.table.setMinimumHeight(min(250 + (self.table.rowCount() * 55), 700))
        self.update_invoice_totals()

    def calculate_row_total(self, row: int):
        # With removed price column, this method just triggers totals update
        self.update_invoice_totals()

    def update_invoice_totals(self):
        subtotal = 0.0
        table = self.table
        
        for r in range(table.rowCount()):
            try:
                customer_amount_w = table.cellWidget(r, 7)  # Customer Amount column
                
                if customer_amount_w:
                    customer_amount = float(customer_amount_w.value())
                    subtotal += customer_amount
            except Exception: pass
        
        try:
            discount_text = self.txt_discount.text().replace('₹', '').replace(',', '').strip()
            discount = float(discount_text) if discount_text else 0.0
        except:
            discount = 0.0
        
        # Tax is now 0 since we're not calculating it from price
        total_tax = 0.0
        total = subtotal - discount
        
        self.lbl_subtotal.setText(f"₹{subtotal:.2f}")
        self.lbl_tax.setText(f"₹{total_tax:.2f}")
        self.lbl_total.setText(f"₹{total:.2f}")
        
        self.calculate_balance()

    def calculate_balance(self):
        try:
            total_text = self.lbl_total.text().replace('₹', '').replace(',', '').strip()
            total = float(total_text) if total_text else 0.0

            received_text = self.txt_received.text().replace('₹', '').replace(',', '').strip()
            received = float(received_text) if received_text else 0.0

            balance = total - received

            if balance > 0:
                self.lbl_balance.setStyleSheet(f"color: {self.colors['danger']}; font-weight: bold; background-color: {self.colors['primary_bg']}; padding: 8px; border: 1px solid {self.colors['danger']};")
                self.lbl_balance.setText(f"{self.get_currency_symbol()}{balance:.2f}")
            elif balance < 0:
                self.lbl_balance.setStyleSheet(f"color: {self.colors['success']}; font-weight: bold; background-color: {self.colors['primary_bg']}; padding: 8px; border: 1px solid {self.colors['success']};")
                self.lbl_balance.setText(f"{self.get_currency_symbol()}{abs(balance):.2f} (Overpaid)")
            else:
                self.lbl_balance.setStyleSheet(f"color: {self.colors['success']}; font-weight: bold; background-color: {self.colors['primary_bg']}; padding: 8px; border: 1px solid {self.colors['success']};")
                self.lbl_balance.setText(f"{self.get_currency_symbol()}0.00 (Paid)")
        except ValueError:
            self.lbl_balance.setText(f"{self.get_currency_symbol()}0.00")
    
    def reset_invoice(self):
        """Reset all invoice fields to default values."""
        reply = QMessageBox.question(
            self, 'Reset Invoice', 
            'Reset all fields? (Ctrl+N)',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No

        )
        
        if reply == QMessageBox.StandardButton.Yes:

            self.invoice_number.setText(self.generate_invoice_number())
            self.invoice_date.setDate(QDate.currentDate())
            self.customer_name.clear()
            self.contact_number.clear()
            self.customer_address.clear()
            self.table.setRowCount(0)
            self.lbl_subtotal.setText(f"{self.get_currency_symbol()}0.00")
            self.txt_discount.setText("0.00")
            self.lbl_tax.setText(f"{self.get_currency_symbol()}0.00")
            self.lbl_total.setText(f"{self.get_currency_symbol()}0.00")
            self.txt_received.clear()
            self.lbl_balance.setText(f"{self.get_currency_symbol()}0.00")
            
            # Reset focus
            self.customer_name.setFocus()

    def save_invoice(self):
        # ... [Logic remains same as previous save_invoice] ...
        # I am collapsing this for brevity, but you must keep the original logic
        # Just ensure you use self.txt_received.text() etc.
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
            
            for r in range(self.table.rowCount()):
                # Extract widget data safely...
                passenger = self.table.cellWidget(r, 0).text()
                pnr = self.table.cellWidget(r, 1).text()
                sector = self.table.cellWidget(r, 2).text()
                supplier = self.table.cellWidget(r, 3).currentText()
                type_v = self.table.cellWidget(r, 4).text()
                qty = self.table.cellWidget(r, 5).value()
                supplier_amount = self.table.cellWidget(r, 6).value()
                customer_amount = self.table.cellWidget(r, 7).value()


                item = {
                    "passenger_name": passenger, "pnr": pnr, "sector": sector,
                    "supplier": supplier, "type": type_v, "qty": qty, "supplier_amount": supplier_amount, "amount": customer_amount
                }
                invoice_data["items"].append(item)
            
            filename = f"invoices/invoice_{invoice_data['invoice_number']}.json"
            os.makedirs("invoices", exist_ok=True)
            with open(filename, 'w') as f: json.dump(invoice_data, f, indent=4)
            
            # Save to DB if available
            if hasattr(self.dashboard, 'db') and self.dashboard.db:
                self._save_to_db(invoice_data) # Helper method call

            msg = f"Invoice saved successfully!\n📁 {filename}"
            QMessageBox.information(self, "Success", msg)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{str(e)}")

    def _save_to_db(self, invoice_data):
        # Helper to keep save_invoice clean
        try:
            db_data = invoice_data.copy()
            # Clean currency symbols
            for k in ['subtotal', 'tax', 'total', 'received']:
                db_data[k] = float(db_data[k].replace('₹', '').replace(',', '').strip() or 0)
            
            disc = db_data.get('discount', '0').replace('₹', '').replace(',', '').strip()
            db_data['discount'] = float(disc or 0)
            
            bal = db_data['balance'].replace('₹', '').replace(',', '').split('(')[0].strip()
            db_data['balance'] = float(bal or 0)
            
            if db_data['balance'] == 0: db_data['status'] = 'Paid'
            elif db_data['balance'] < 0: db_data['status'] = 'Overpaid'
            else: db_data['status'] = 'Pending'
            
            db_data['items'] = []
            for item in invoice_data['items']:
                amt = item['amount'].replace('₹', '').replace(',', '').strip()
                db_item = {
                    'item': item['passenger_name'], 'ticket': item['pnr'],
                    'sector': item['sector'], 'supplier': item['supplier'],
                    'qty': float(item['qty']),'supplier_amount': float(item['supplier_amount']),
                    'customer_amount': float(item['customer_amount'])
                }
                db_data['items'].append(db_item)
            
            self.dashboard.db.save_invoice(db_data)
        except Exception as e:
            print(f"DB Error: {e}")

    def save_pdf(self):
        # ... [Same as previous save_pdf] ...
        try:
            default_dir = os.path.join(os.getcwd(), "output", "invoice")
            os.makedirs(default_dir, exist_ok=True)
            filename = os.path.join(default_dir, f"invoice_{self.invoice_number.text()}.pdf")

            items = []
            for r in range(self.table.rowCount()):
                passenger = self.table.cellWidget(r, 0).text()
                pnr = self.table.cellWidget(r, 1).text()
                sector = self.table.cellWidget(r, 2).text()
                type_v = self.table.cellWidget(r, 4).text()
                qty = self.table.cellWidget(r, 5).value()
                customer_amount = self.table.cellWidget(r, 7).value()
                
                # Calculate per-unit price from customer amount and quantity
                unit_price = customer_amount / qty if qty > 0 else customer_amount
                
                items.append({
                    "passenger_name": passenger,
                    "pnr": pnr,
                    "sector": sector,
                    "type": type_v,
                    "qty": qty,
                    "unit_price": unit_price,
                
                })

            invoice_data = {
                "company": {"name": self.company_info["name"], "address": self.company_info.get("address", ""), "footer_note": self.invoice_config.get("footer_note", "")},
                "invoice_meta": {"number": self.invoice_number.text(), "date": self.invoice_date.date().toString("dd/MM/yyyy")},
                "customer": {"name": self.customer_name.text(), "address": self.customer_address.text(), "contact": self.contact_number.text()},
                "items": items,
                "notes": "Generated from Travel Billing System",
                "terms": self.invoice_config.get("terms", "Payment due within 7 days.")
            }

            generate_invoice_pdf(invoice_data, filename)

            if self.show_dialog_window:
                msg = QMessageBox(self); msg.setWindowTitle("PDF Saved"); msg.setText(f"PDF saved!\n{filename}")
                open_btn = msg.addButton("Open", QMessageBox.ButtonRole.ActionRole); msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)
                msg.exec()
                if msg.clickedButton() == open_btn: os.startfile(filename)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"PDF Error:\n{str(e)}")
        finally:
            self.show_dialog_window = True

    def print_invoice(self):
        # ... [Keep previous print_invoice logic] ...
        import os
        from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
        from PyQt6.QtGui import QPainter, QImage
        import pypdfium2 as pdfium

        pdf_path = os.path.join(os.getcwd(), "output", "invoice", f"invoice_{self.invoice_number.text()}.pdf")
        if not os.path.exists(pdf_path):
            self.show_dialog_window = False
            self.save_pdf()
        
        if not os.path.exists(pdf_path): return

        try:
            pdf = pdfium.PdfDocument(pdf_path)
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec() != QPrintDialog.DialogCode.Accepted: return
            
            painter = QPainter(printer)
            for idx, page in enumerate(pdf):
                bitmap = page.render(scale=2.0)
                img = QImage(bitmap.to_pil().convert("RGBA").tobytes("raw", "RGBA"), bitmap.width, bitmap.height, QImage.Format.Format_RGBA8888)
                
                rect = printer.pageRect(); size = img.size(); size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
                painter.drawImage(rect.x() + (rect.width() - size.width())//2, rect.y(), img.scaled(size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                if idx < len(pdf) - 1: printer.newPage()
            painter.end()
            QMessageBox.information(self, "Print", "Sent to printer!")
        except Exception as e:
            QMessageBox.critical(self, "Print Error", str(e))

    def share_invoice(self):
        # ... [Keep previous share_invoice logic] ...
        try:
            pdf_path = os.path.join(os.getcwd(), "output", "invoice", f"invoice_{self.invoice_number.text()}.pdf")
            if not os.path.exists(pdf_path):
                self.show_dialog_window = False; self.save_pdf()
            
            email, ok = QInputDialog.getText(self, "Share", f"Recipient email for Invoice {self.invoice_number.text()}:")
            if ok and email: QMessageBox.information(self, "Shared", f"Ready to send to {email}\nFile: {pdf_path}")
        except Exception as e: QMessageBox.critical(self, "Error", str(e))