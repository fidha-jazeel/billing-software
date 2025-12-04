"""
Comprehensive Supplier Management Page
With Basic Info, Financial Details, Bank Details, and Payment Tracking
"""
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QPushButton,
                             QLineEdit, QMessageBox, QComboBox, QDoubleSpinBox,
                             QGridLayout, QGroupBox, QTextEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont


class SupplierPage(QWidget):
    """Comprehensive Supplier Management with Payment Tracking."""
    
    def __init__(self, colors, get_table_style, get_button_style, get_input_style, parent=None):
        super().__init__()
        self.colors = colors
        self.get_table_style = get_table_style
        self.get_button_style = get_button_style
        self.get_input_style = get_input_style
        self.parent_window = parent
        
        # Data paths
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'suppliers')
        os.makedirs(self.data_dir, exist_ok=True)
        self.suppliers_file = os.path.join(self.data_dir, 'suppliers_data.json')
        self.payments_file = os.path.join(self.data_dir, 'supplier_payments.json')
        self.invoices_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'invoices')
        
        self.suppliers = []
        self.payments = []
        self.current_supplier_id = None
        
        self._load_data()
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the comprehensive UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Header
        header = QLabel("👥 Supplier Management System")
        header.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 32px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
        """)
        layout.addWidget(header)
        
        subtitle = QLabel("Complete supplier information, financial tracking, and payment management")
        subtitle.setStyleSheet(f"QLabel {{ color: {self.colors['text_secondary']}; font-size: 15px; }}")
        layout.addWidget(subtitle)
        
        # Main Content in Grid
        grid = QGridLayout()
        grid.setSpacing(20)
        
        # SECTION 1: Basic Information
        basic_info = self._create_basic_info_section()
        grid.addWidget(basic_info, 0, 0)
        
        # SECTION 2: Financial Details
        financial_details = self._create_financial_details_section()
        grid.addWidget(financial_details, 0, 1)
        
        # SECTION 3: Bank Details
        # bank_details = self._create_bank_details_section()
        # grid.addWidget(bank_details, 1, 0)
        
        # SECTION 4: Payment Tracking
        payment_tracking = self._create_payment_tracking_section()
        grid.addWidget(payment_tracking, 1, 1)
        
        layout.addLayout(grid)
        
        # Action Buttons
        button_bar = self._create_action_buttons()
        layout.addWidget(button_bar)
        
        # Supplier List Table
        supplier_list = self._create_supplier_list_section()
        layout.addWidget(supplier_list)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        self._populate_supplier_table()
    
    def _create_basic_info_section(self):
        """Create Basic Information section."""
        group = QGroupBox("📋 Basic Information")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: bold;
                color: {self.colors['accent_primary']};
                border: 2px solid {self.colors['accent_primary']};
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        
        layout = QGridLayout(group)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Supplier Name
        layout.addWidget(QLabel("Supplier Name: *"), 0, 0)
        self.supplier_name = QLineEdit()
        self.supplier_name.setPlaceholderText("Enter supplier name")
        self.supplier_name.setStyleSheet(self.get_input_style())
        layout.addWidget(self.supplier_name, 0, 1)
        
        # Supplier Type
        layout.addWidget(QLabel("Supplier Type:"), 1, 0)
        self.supplier_type = QComboBox()
        self.supplier_type.addItems(["Regular", "Premium", "Wholesale", "Retail", "Manufacturer", "Distributor"])
        self.supplier_type.setStyleSheet(self.get_input_style())
        layout.addWidget(self.supplier_type, 1, 1)
        
        # Contact Number
        layout.addWidget(QLabel("Contact Number: *"), 2, 0)
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Enter contact number")
        self.contact_number.setStyleSheet(self.get_input_style())
        layout.addWidget(self.contact_number, 2, 1)
        
        # Alternate Number
        layout.addWidget(QLabel("Alternate Number:"), 3, 0)
        self.alternate_number = QLineEdit()
        self.alternate_number.setPlaceholderText("Enter alternate number")
        self.alternate_number.setStyleSheet(self.get_input_style())
        layout.addWidget(self.alternate_number, 3, 1)
        
        # Email
        layout.addWidget(QLabel("Email:"), 4, 0)
        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter email address")
        self.email.setStyleSheet(self.get_input_style())
        layout.addWidget(self.email, 4, 1)
        
        # Country
        layout.addWidget(QLabel("Country:"), 5, 0)
        self.country = QComboBox()
        self.country.addItems(["India", "USA", "UK", "UAE", "Singapore", "Malaysia", "Other"])
        self.country.setStyleSheet(self.get_input_style())
        layout.addWidget(self.country, 5, 1)
        
        # City
        layout.addWidget(QLabel("City:"), 6, 0)
        self.city = QLineEdit()
        self.city.setPlaceholderText("Enter city")
        self.city.setStyleSheet(self.get_input_style())
        layout.addWidget(self.city, 6, 1)
        
        # Address
        layout.addWidget(QLabel("Address:"), 7, 0)
        self.address = QTextEdit()
        self.address.setPlaceholderText("Enter complete address")
        self.address.setMaximumHeight(80)
        self.address.setStyleSheet(self.get_input_style())
        layout.addWidget(self.address, 7, 1)
        
        return group
    
    def _create_financial_details_section(self):
        """Create Financial Details section."""
        group = QGroupBox("💰 Financial Details")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: bold;
                color: {self.colors['success']};
                border: 2px solid {self.colors['success']};
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        
        layout = QGridLayout(group)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Opening Balance
        layout.addWidget(QLabel("Opening Balance:"), 0, 0)
        self.opening_balance = QDoubleSpinBox()
        self.opening_balance.setRange(0, 99999999.99)
        self.opening_balance.setPrefix("₹ ")
        self.opening_balance.setDecimals(2)
        self.opening_balance.setStyleSheet(self.get_input_style())
        self.opening_balance.valueChanged.connect(self._calculate_current_balance)
        layout.addWidget(self.opening_balance, 0, 1)
        
        # Balance Type
        layout.addWidget(QLabel("Balance Type:"), 1, 0)
        self.balance_type = QComboBox()
        self.balance_type.addItems(["Payable", "Receivable"])
        self.balance_type.setStyleSheet(self.get_input_style())
        layout.addWidget(self.balance_type, 1, 1)
        
        # Credit Limit
        layout.addWidget(QLabel("Credit Limit:"), 2, 0)
        self.credit_limit = QDoubleSpinBox()
        self.credit_limit.setRange(0, 99999999.99)
        self.credit_limit.setPrefix("₹ ")
        self.credit_limit.setDecimals(2)
        self.credit_limit.setStyleSheet(self.get_input_style())
        layout.addWidget(self.credit_limit, 2, 1)
        
        # Payment Terms
        layout.addWidget(QLabel("Payment Terms:"), 3, 0)
        self.payment_terms = QComboBox()
        self.payment_terms.addItems(["Cash", "Credit - 7 Days", "Credit - 15 Days", 
                                     "Credit - 30 Days", "Credit - 45 Days", "Credit - 60 Days"])
        self.payment_terms.setStyleSheet(self.get_input_style())
        layout.addWidget(self.payment_terms, 3, 1)
        
        # GST Number
        layout.addWidget(QLabel("GST Number:"), 4, 0)
        self.gst_number = QLineEdit()
        self.gst_number.setPlaceholderText("Enter GST number")
        self.gst_number.setStyleSheet(self.get_input_style())
        layout.addWidget(self.gst_number, 4, 1)
        
        # PAN Number
        layout.addWidget(QLabel("PAN Number:"), 5, 0)
        self.pan_number = QLineEdit()
        self.pan_number.setPlaceholderText("Enter PAN number")
        self.pan_number.setStyleSheet(self.get_input_style())
        layout.addWidget(self.pan_number, 5, 1)
        
        # Current Balance (Auto-calculated, Read-only)
        layout.addWidget(QLabel("Current Balance:"), 6, 0)
        self.current_balance_label = QLabel("₹ 0.00")
        self.current_balance_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['accent_gold']};
                padding: 10px;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
                border: 2px solid {self.colors['accent_gold']};
            }}
        """)
        layout.addWidget(self.current_balance_label, 6, 1)
        
        return group
    
    # def _create_bank_details_section(self):
    #     """Create Bank Details section."""
    #     group = QGroupBox("🏦 Supplier Bank Details")
    #     group.setStyleSheet(f"""
    #         QGroupBox {{
    #             font-size: 16px;
    #             font-weight: bold;
    #             color: {self.colors['accent_gold']};
    #             border: 2px solid {self.colors['accent_gold']};
    #             border-radius: 10px;
    #             margin-top: 15px;
    #             padding-top: 20px;
    #         }}
    #         QGroupBox::title {{
    #             subcontrol-origin: margin;
    #             left: 15px;
    #             padding: 0 10px;
    #         }}
    #     """)
        
    #     layout = QGridLayout(group)
    #     layout.setSpacing(12)
    #     layout.setContentsMargins(20, 25, 20, 20)
        
    #     # Bank Name
    #     layout.addWidget(QLabel("Bank Name:"), 0, 0)
    #     self.bank_name = QLineEdit()
    #     self.bank_name.setPlaceholderText("Enter bank name")
    #     self.bank_name.setStyleSheet(self.get_input_style())
    #     layout.addWidget(self.bank_name, 0, 1)
        
    #     # Account Number
    #     layout.addWidget(QLabel("Account Number:"), 1, 0)
    #     self.account_number = QLineEdit()
    #     self.account_number.setPlaceholderText("Enter account number")
    #     self.account_number.setStyleSheet(self.get_input_style())
    #     layout.addWidget(self.account_number, 1, 1)
        
    #     # IBAN
    #     layout.addWidget(QLabel("IBAN:"), 2, 0)
    #     self.iban = QLineEdit()
    #     self.iban.setPlaceholderText("Enter IBAN")
    #     self.iban.setStyleSheet(self.get_input_style())
    #     layout.addWidget(self.iban, 2, 1)
        
    #     # SWIFT Code
    #     layout.addWidget(QLabel("SWIFT Code:"), 3, 0)
    #     self.swift_code = QLineEdit()
    #     self.swift_code.setPlaceholderText("Enter SWIFT code")
    #     self.swift_code.setStyleSheet(self.get_input_style())
    #     layout.addWidget(self.swift_code, 3, 1)
        
    #     # Branch Name
    #     layout.addWidget(QLabel("Branch Name:"), 4, 0)
    #     self.branch_name = QLineEdit()
    #     self.branch_name.setPlaceholderText("Enter branch name")
    #     self.branch_name.setStyleSheet(self.get_input_style())
    #     layout.addWidget(self.branch_name, 4, 1)
        
    #     # IFSC Code
    #     layout.addWidget(QLabel("IFSC Code:"), 5, 0)
    #     self.ifsc_code = QLineEdit()
    #     self.ifsc_code.setPlaceholderText("Enter IFSC code")
    #     self.ifsc_code.setStyleSheet(self.get_input_style())
    #     layout.addWidget(self.ifsc_code, 5, 1)
        
    #     return group
    
    def _create_payment_tracking_section(self):
        """Create Payment Tracking section."""
        group = QGroupBox("💳 Payment Tracking & Ledger")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: bold;
                color: {self.colors['danger']};
                border: 2px solid {self.colors['danger']};
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        
        layout = QGridLayout(group)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Amount Payable to Supplier
        payable_label = QLabel("Amount Payable to Supplier:")
        payable_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(payable_label, 0, 0)
        
        self.amount_payable_label = QLabel("₹ 0.00")
        self.amount_payable_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.colors['danger']};
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(self.amount_payable_label, 0, 1)
        
        # Amount Paid to Supplier
        paid_label = QLabel("Amount Paid to Supplier:")
        paid_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(paid_label, 1, 0)
        
        self.amount_paid_label = QLabel("₹ 0.00")
        self.amount_paid_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.colors['success']};
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(self.amount_paid_label, 1, 1)
        
        # Remaining Balance
        balance_label = QLabel("Remaining Balance:")
        balance_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(balance_label, 2, 0)
        
        self.remaining_balance_label = QLabel("₹ 0.00")
        self.remaining_balance_label.setStyleSheet(f"""
            QLabel {{
                background-color: {self.colors['accent_gold']};
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(self.remaining_balance_label, 2, 1)
        
        # Record Payment Button
        record_payment_btn = QPushButton("💵 Record Payment")
        record_payment_btn.setStyleSheet(self.get_button_style('add') + """
            QPushButton {
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        record_payment_btn.clicked.connect(self._record_payment)
        layout.addWidget(record_payment_btn, 3, 0, 1, 2)
        
        # View Ledger Button
        view_ledger_btn = QPushButton("📊 View Supplier Ledger")
        view_ledger_btn.setStyleSheet(self.get_button_style('primary') + """
            QPushButton {
                padding: 12px;
                font-size: 14px;
            }
        """)
        view_ledger_btn.clicked.connect(self._view_ledger)
        layout.addWidget(view_ledger_btn, 4, 0, 1, 2)
        
        return group
    
    def _create_action_buttons(self):
        """Create action buttons bar."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(15)
        
        # Add/Save Button
        save_btn = QPushButton("💾 Add/Save Supplier")
        save_btn.setStyleSheet(self.get_button_style('add') + """
            QPushButton {
                padding: 15px 30px;
                font-size: 15px;
                font-weight: bold;
            }
        """)
        save_btn.clicked.connect(self._save_supplier)
        layout.addWidget(save_btn)
        
        # Update Button
        update_btn = QPushButton("✏️ Update Supplier")
        update_btn.setStyleSheet(self.get_button_style('primary') + """
            QPushButton {
                padding: 15px 30px;
                font-size: 15px;
            }
        """)
        update_btn.clicked.connect(self._update_supplier)
        layout.addWidget(update_btn)
        
        # Delete Button
        delete_btn = QPushButton("🗑️ Delete Supplier")
        delete_btn.setStyleSheet(self.get_button_style('cancel') + """
            QPushButton {
                padding: 15px 30px;
                font-size: 15px;
            }
        """)
        delete_btn.clicked.connect(self._delete_supplier)
        layout.addWidget(delete_btn)
        
        # Clear Form Button
        clear_btn = QPushButton("🔄 Clear Form")
        clear_btn.setStyleSheet(self.get_button_style('secondary') + """
            QPushButton {
                padding: 15px 30px;
                font-size: 15px;
            }
        """)
        clear_btn.clicked.connect(self._clear_form)
        layout.addWidget(clear_btn)
        
        layout.addStretch()
        
        return frame
    
    def _create_supplier_list_section(self):
        """Create supplier list table."""
        group = QGroupBox("📋 All Suppliers")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 18px;
                font-weight: bold;
                color: {self.colors['accent_primary']};
                border: 2px solid {self.colors['accent_primary']};
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 20px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Search
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Search:")
        self.supplier_search = QLineEdit()
        self.supplier_search.setPlaceholderText("Search by name, phone, email...")
        self.supplier_search.setStyleSheet(self.get_input_style())
        self.supplier_search.textChanged.connect(self._filter_supplier_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.supplier_search)
        layout.addLayout(search_layout)
        
        # Table
        self.supplier_table = QTableWidget(0, 8)
        self.supplier_table.setHorizontalHeaderLabels([
            "Supplier Name", "Type", "Contact", "Email", "Balance Type", 
            "Current Balance", "Payment Terms", "ID"
        ])
        
        # Configure table
        header = self.supplier_table.horizontalHeader()
        header.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {self.colors['accent_primary']};
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }}
        """)
        
        self.supplier_table.setColumnWidth(0, 200)
        self.supplier_table.setColumnWidth(1, 120)
        self.supplier_table.setColumnWidth(2, 120)
        self.supplier_table.setColumnWidth(3, 180)
        self.supplier_table.setColumnWidth(4, 120)
        self.supplier_table.setColumnWidth(5, 150)
        self.supplier_table.setColumnWidth(6, 150)
        self.supplier_table.setColumnHidden(7, True)
        
        self.supplier_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.supplier_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.supplier_table.setAlternatingRowColors(True)
        self.supplier_table.setStyleSheet(self.get_table_style())
        self.supplier_table.setMinimumHeight(400)
        self.supplier_table.itemClicked.connect(self._load_supplier_to_form)
        
        layout.addWidget(self.supplier_table)
        
        return group
    
    def _load_data(self):
        """Load suppliers and payments data."""
        if os.path.exists(self.suppliers_file):
            try:
                with open(self.suppliers_file, 'r', encoding='utf-8') as f:
                    self.suppliers = json.load(f)
            except:
                self.suppliers = []
        
        if os.path.exists(self.payments_file):
            try:
                with open(self.payments_file, 'r', encoding='utf-8') as f:
                    self.payments = json.load(f)
            except:
                self.payments = []
    
    def _save_data(self):
        """Save suppliers and payments data."""
        try:
            with open(self.suppliers_file, 'w', encoding='utf-8') as f:
                json.dump(self.suppliers, f, indent=4, ensure_ascii=False)
            
            with open(self.payments_file, 'w', encoding='utf-8') as f:
                json.dump(self.payments, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data:\n{str(e)}")
            return False
    
    def _save_supplier(self):
        """Add/Save new supplier."""
        name = self.supplier_name.text().strip()
        contact = self.contact_number.text().strip()
        
        if not name or not contact:
            QMessageBox.warning(self, "Validation Error", "Supplier Name and Contact Number are required!")
            return
        
        supplier_data = {
            'id': str(datetime.now().timestamp()),
            'name': name,
            'type': self.supplier_type.currentText(),
            'contact': contact,
            'alternate_contact': self.alternate_number.text().strip(),
            'email': self.email.text().strip(),
            'country': self.country.currentText(),
            'city': self.city.text().strip(),
            'address': self.address.toPlainText().strip(),
            'opening_balance': self.opening_balance.value(),
            'balance_type': self.balance_type.currentText(),
            'credit_limit': self.credit_limit.value(),
            'payment_terms': self.payment_terms.currentText(),
            'gst': self.gst_number.text().strip(),
            'pan': self.pan_number.text().strip(),
            'bank_name': self.bank_name.text().strip(),
            'account_number': self.account_number.text().strip(),
            'iban': self.iban.text().strip(),
            'swift': self.swift_code.text().strip(),
            'branch': self.branch_name.text().strip(),
            'ifsc': self.ifsc_code.text().strip(),
            'amount_payable': 0.0,
            'amount_paid': 0.0,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.suppliers.append(supplier_data)
        
        if self._save_data():
            QMessageBox.information(self, "Success", f"Supplier '{name}' added successfully!")
            self._clear_form()
            self._populate_supplier_table()
    
    def _update_supplier(self):
        """Update existing supplier."""
        if not self.current_supplier_id:
            QMessageBox.warning(self, "No Selection", "Please select a supplier to update!")
            return
        
        name = self.supplier_name.text().strip()
        contact = self.contact_number.text().strip()
        
        if not name or not contact:
            QMessageBox.warning(self, "Validation Error", "Supplier Name and Contact Number are required!")
            return
        
        for i, supplier in enumerate(self.suppliers):
            if supplier['id'] == self.current_supplier_id:
                # Preserve payment data
                amount_payable = supplier.get('amount_payable', 0.0)
                amount_paid = supplier.get('amount_paid', 0.0)
                
                self.suppliers[i] = {
                    'id': self.current_supplier_id,
                    'name': name,
                    'type': self.supplier_type.currentText(),
                    'contact': contact,
                    'alternate_contact': self.alternate_number.text().strip(),
                    'email': self.email.text().strip(),
                    'country': self.country.currentText(),
                    'city': self.city.text().strip(),
                    'address': self.address.toPlainText().strip(),
                    'opening_balance': self.opening_balance.value(),
                    'balance_type': self.balance_type.currentText(),
                    'credit_limit': self.credit_limit.value(),
                    'payment_terms': self.payment_terms.currentText(),
                    'gst': self.gst_number.text().strip(),
                    'pan': self.pan_number.text().strip(),
                    'bank_name': self.bank_name.text().strip(),
                    'account_number': self.account_number.text().strip(),
                    'iban': self.iban.text().strip(),
                    'swift': self.swift_code.text().strip(),
                    'branch': self.branch_name.text().strip(),
                    'ifsc': self.ifsc_code.text().strip(),
                    'amount_payable': amount_payable,
                    'amount_paid': amount_paid,
                    'created_date': supplier.get('created_date'),
                    'modified_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                break
        
        if self._save_data():
            QMessageBox.information(self, "Success", f"Supplier '{name}' updated successfully!")
            self._clear_form()
            self._populate_supplier_table()
    
    def _delete_supplier(self):
        """Delete supplier."""
        if not self.current_supplier_id:
            QMessageBox.warning(self, "No Selection", "Please select a supplier to delete!")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this supplier?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.suppliers = [s for s in self.suppliers if s['id'] != self.current_supplier_id]
            
            if self._save_data():
                QMessageBox.information(self, "Success", "Supplier deleted successfully!")
                self._clear_form()
                self._populate_supplier_table()
    
    def _clear_form(self):
        """Clear all form fields."""
        self.current_supplier_id = None
        self.supplier_name.clear()
        self.supplier_type.setCurrentIndex(0)
        self.contact_number.clear()
        self.alternate_number.clear()
        self.email.clear()
        self.country.setCurrentIndex(0)
        self.city.clear()
        self.address.clear()
        self.opening_balance.setValue(0)
        self.balance_type.setCurrentIndex(0)
        self.credit_limit.setValue(0)
        self.payment_terms.setCurrentIndex(0)
        self.gst_number.clear()
        self.pan_number.clear()
        self.bank_name.clear()
        self.account_number.clear()
        self.iban.clear()
        self.swift_code.clear()
        self.branch_name.clear()
        self.ifsc_code.clear()
        self.current_balance_label.setText("₹ 0.00")
        self.amount_payable_label.setText("₹ 0.00")
        self.amount_paid_label.setText("₹ 0.00")
        self.remaining_balance_label.setText("₹ 0.00")
    
    def _populate_supplier_table(self):
        """Populate supplier table."""
        self.supplier_table.setRowCount(0)
        
        for supplier in self.suppliers:
            row = self.supplier_table.rowCount()
            self.supplier_table.insertRow(row)
            
            self.supplier_table.setItem(row, 0, QTableWidgetItem(supplier.get('name', '')))
            self.supplier_table.setItem(row, 1, QTableWidgetItem(supplier.get('type', '')))
            self.supplier_table.setItem(row, 2, QTableWidgetItem(supplier.get('contact', '')))
            self.supplier_table.setItem(row, 3, QTableWidgetItem(supplier.get('email', 'N/A')))
            self.supplier_table.setItem(row, 4, QTableWidgetItem(supplier.get('balance_type', '')))
            
            # Calculate current balance
            balance = supplier.get('opening_balance', 0.0) + supplier.get('amount_payable', 0.0) - supplier.get('amount_paid', 0.0)
            self.supplier_table.setItem(row, 5, QTableWidgetItem(f"₹ {balance:,.2f}"))
            
            self.supplier_table.setItem(row, 6, QTableWidgetItem(supplier.get('payment_terms', '')))
            self.supplier_table.setItem(row, 7, QTableWidgetItem(supplier.get('id', '')))
    
    def _filter_supplier_table(self):
        """Filter supplier table based on search."""
        search_text = self.supplier_search.text().lower()
        
        for row in range(self.supplier_table.rowCount()):
            show = False
            for col in range(7):
                item = self.supplier_table.item(row, col)
                if item and search_text in item.text().lower():
                    show = True
                    break
            self.supplier_table.setRowHidden(row, not show)
    
    def _load_supplier_to_form(self, item):
        """Load selected supplier to form."""
        row = item.row()
        supplier_id = self.supplier_table.item(row, 7).text()
        
        supplier = next((s for s in self.suppliers if s['id'] == supplier_id), None)
        if not supplier:
            return
        
        self.current_supplier_id = supplier_id
        
        self.supplier_name.setText(supplier.get('name', ''))
        self.supplier_type.setCurrentText(supplier.get('type', 'Regular'))
        self.contact_number.setText(supplier.get('contact', ''))
        self.alternate_number.setText(supplier.get('alternate_contact', ''))
        self.email.setText(supplier.get('email', ''))
        self.country.setCurrentText(supplier.get('country', 'India'))
        self.city.setText(supplier.get('city', ''))
        self.address.setPlainText(supplier.get('address', ''))
        self.opening_balance.setValue(supplier.get('opening_balance', 0.0))
        self.balance_type.setCurrentText(supplier.get('balance_type', 'Payable'))
        self.credit_limit.setValue(supplier.get('credit_limit', 0.0))
        self.payment_terms.setCurrentText(supplier.get('payment_terms', 'Cash'))
        self.gst_number.setText(supplier.get('gst', ''))
        self.pan_number.setText(supplier.get('pan', ''))
        self.bank_name.setText(supplier.get('bank_name', ''))
        self.account_number.setText(supplier.get('account_number', ''))
        self.iban.setText(supplier.get('iban', ''))
        self.swift_code.setText(supplier.get('swift', ''))
        self.branch_name.setText(supplier.get('branch', ''))
        self.ifsc_code.setText(supplier.get('ifsc', ''))
        
        # Update payment tracking
        self._update_payment_tracking(supplier)
        self._calculate_current_balance()
    
    def _calculate_current_balance(self):
        """Calculate and display current balance."""
        opening = self.opening_balance.value()
        
        if self.current_supplier_id:
            supplier = next((s for s in self.suppliers if s['id'] == self.current_supplier_id), None)
            if supplier:
                payable = supplier.get('amount_payable', 0.0)
                paid = supplier.get('amount_paid', 0.0)
                current_balance = opening + payable - paid
                self.current_balance_label.setText(f"₹ {current_balance:,.2f}")
            else:
                self.current_balance_label.setText(f"₹ {opening:,.2f}")
        else:
            self.current_balance_label.setText(f"₹ {opening:,.2f}")
    
    def _update_payment_tracking(self, supplier):
        """Update payment tracking displays."""
        payable = supplier.get('amount_payable', 0.0)
        paid = supplier.get('amount_paid', 0.0)
        remaining = payable - paid
        
        self.amount_payable_label.setText(f"₹ {payable:,.2f}")
        self.amount_paid_label.setText(f"₹ {paid:,.2f}")
        self.remaining_balance_label.setText(f"₹ {remaining:,.2f}")
    
    def _record_payment(self):
        """Record payment to supplier."""
        if not self.current_supplier_id:
            QMessageBox.warning(self, "No Supplier", "Please select a supplier first!")
            return
        
        # Simple payment dialog
        from PyQt6.QtWidgets import QDialog, QFormLayout, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Record Payment")
        dialog.setModal(True)
        
        layout = QFormLayout(dialog)
        
        amount_spin = QDoubleSpinBox()
        amount_spin.setRange(0, 99999999.99)
        amount_spin.setPrefix("₹ ")
        amount_spin.setDecimals(2)
        amount_spin.setStyleSheet(self.get_input_style())
        layout.addRow("Payment Amount:", amount_spin)
        
        notes_edit = QTextEdit()
        notes_edit.setMaximumHeight(60)
        notes_edit.setStyleSheet(self.get_input_style())
        layout.addRow("Notes:", notes_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            amount = amount_spin.value()
            notes = notes_edit.toPlainText()
            
            if amount <= 0:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a valid payment amount!")
                return
            
            # Update supplier payment data
            for supplier in self.suppliers:
                if supplier['id'] == self.current_supplier_id:
                    supplier['amount_paid'] = supplier.get('amount_paid', 0.0) + amount
                    break
            
            # Record payment transaction
            payment_record = {
                'id': str(datetime.now().timestamp()),
                'supplier_id': self.current_supplier_id,
                'amount': amount,
                'notes': notes,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.payments.append(payment_record)
            
            if self._save_data():
                QMessageBox.information(self, "Success", f"Payment of ₹{amount:,.2f} recorded successfully!")
                self._load_supplier_to_form(self.supplier_table.item(self.supplier_table.currentRow(), 0))
                self._populate_supplier_table()
    
    def _view_ledger(self):
        """View supplier ledger."""
        if not self.current_supplier_id:
            QMessageBox.warning(self, "No Supplier", "Please select a supplier first!")
            return
        
        QMessageBox.information(self, "Supplier Ledger", 
                               "Ledger feature will show all transactions, payments, and balance history.\n\n"
                               "This will be fully integrated with the Balance Report.")
