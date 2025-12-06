"""
Supplier Management Page Module
Comprehensive supplier management with CRUD operations, search, and export functionality.
"""
import os
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QTableWidget, QPushButton,
                             QLineEdit, QTableWidgetItem, QMessageBox, 
                             QFileDialog, QHeaderView, QDialog, QTextEdit,
                             QFormLayout, QDialogButtonBox, QComboBox, QDoubleSpinBox,
                             QGroupBox, QSpinBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont
from travel_billing_software.database.db_manager import get_db_instance


class SupplierDialog(QDialog):
    """Dialog for adding/editing supplier details."""
    
    def __init__(self, colors, get_input_style, get_button_style, supplier_data=None, parent=None):
        super().__init__(parent)
        self.colors = colors
        self.get_input_style = get_input_style
        self.get_button_style = get_button_style
        self.supplier_data = supplier_data
        
        self.setWindowTitle("Add Supplier" if not supplier_data else "Edit Supplier")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self._init_ui()
        
        if supplier_data:
            self._populate_fields()
    
    def _init_ui(self):
        """Initialize dialog UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel("Supplier Details")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
        """)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Supplier Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter supplier name")
        self.name_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Supplier Name: *", self.name_input)
        
        # Contact Person
        self.contact_person_input = QLineEdit()
        self.contact_person_input.setPlaceholderText("Enter contact person name")
        self.contact_person_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Contact Person:", self.contact_person_input)
        
        # Phone Number
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Phone Number: *", self.phone_input)
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Email:", self.email_input)
        
        # Company Name
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Enter company name")
        self.company_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Company Name:", self.company_input)
        
        # Address
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Enter full address")
        self.address_input.setMaximumHeight(80)
        self.address_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Address:", self.address_input)
        
        # GST Number
        self.gst_input = QLineEdit()
        self.gst_input.setPlaceholderText("Enter GST number")
        self.gst_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("GST Number:", self.gst_input)
        
        # PAN Number
        self.pan_input = QLineEdit()
        self.pan_input.setPlaceholderText("Enter PAN number")
        self.pan_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("PAN Number:", self.pan_input)
        
        # Payment Terms
        self.payment_terms = QComboBox()
        self.payment_terms.addItems(["Cash", "Credit - 7 Days", "Credit - 15 Days", 
                                     "Credit - 30 Days", "Credit - 45 Days", "Credit - 60 Days"])
        self.payment_terms.setStyleSheet(self.get_input_style())
        form_layout.addRow("Payment Terms:", self.payment_terms)
        
        # Bank Details
        self.bank_name_input = QLineEdit()
        self.bank_name_input.setPlaceholderText("Enter bank name")
        self.bank_name_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Bank Name:", self.bank_name_input)
        
        self.account_number_input = QLineEdit()
        self.account_number_input.setPlaceholderText("Enter account number")
        self.account_number_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Account Number:", self.account_number_input)
        
        self.ifsc_input = QLineEdit()
        self.ifsc_input.setPlaceholderText("Enter IFSC code")
        self.ifsc_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("IFSC Code:", self.ifsc_input)
        
        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional notes or comments")
        self.notes_input.setMaximumHeight(60)
        self.notes_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Notes:", self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet(f"color: {self.colors['danger']}; font-size: 11px; font-style: italic;")
        layout.addWidget(required_note)
        
        # Buttons
        button_box = QDialogButtonBox()
        save_btn = QPushButton("💾 Save Supplier")
        save_btn.setStyleSheet(self.get_button_style('add'))
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("✖ Cancel")
        cancel_btn.setStyleSheet(self.get_button_style('cancel'))
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addButton(save_btn, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton(cancel_btn, QDialogButtonBox.ButtonRole.RejectRole)
        
        layout.addWidget(button_box)
    
    def _populate_fields(self):
        """Populate fields with existing supplier data."""
        self.name_input.setText(self.supplier_data.get('name', ''))
        self.contact_person_input.setText(self.supplier_data.get('contact_person', ''))
        self.phone_input.setText(self.supplier_data.get('phone', ''))
        self.email_input.setText(self.supplier_data.get('email', ''))
        self.company_input.setText(self.supplier_data.get('company', ''))
        self.address_input.setPlainText(self.supplier_data.get('address', ''))
        self.gst_input.setText(self.supplier_data.get('gst', ''))
        self.pan_input.setText(self.supplier_data.get('pan', ''))
        
        payment_terms = self.supplier_data.get('payment_terms', 'Cash')
        index = self.payment_terms.findText(payment_terms)
        if index >= 0:
            self.payment_terms.setCurrentIndex(index)
        
        self.bank_name_input.setText(self.supplier_data.get('bank_name', ''))
        self.account_number_input.setText(self.supplier_data.get('account_number', ''))
        self.ifsc_input.setText(self.supplier_data.get('ifsc', ''))
        self.notes_input.setPlainText(self.supplier_data.get('notes', ''))
    
    def get_supplier_data(self):
        """Get supplier data from form fields."""
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Validation Error", "Supplier name is required!")
            return None
        
        if not phone:
            QMessageBox.warning(self, "Validation Error", "Phone number is required!")
            return None
        
        data = {
            'name': name,
            'phone': phone,
            'email': self.email_input.text().strip(),
            'company': self.company_input.text().strip(),
            'address': self.address_input.toPlainText().strip(),
            'gst': self.gst_input.text().strip(),
            'contact_person': self.contact_person_input.text().strip(),
            'pan': self.pan_input.text().strip(),
            'payment_terms': self.payment_terms.currentText(),
            'bank_name': self.bank_name_input.text().strip(),
            'account_number': self.account_number_input.text().strip(),
            'ifsc': self.ifsc_input.text().strip(),
            'notes': self.notes_input.toPlainText().strip(),
            'opening_balance': 0.0
        }
        
        # Add ID only if editing existing supplier
        if self.supplier_data and 'id' in self.supplier_data:
            data['id'] = self.supplier_data['id']
        
        return data


class SupplierPage(QWidget):
    """Comprehensive Supplier Management Page."""
    
    def __init__(self, colors, get_table_style, get_button_style, get_input_style, parent=None):
        super().__init__()
        self.colors = colors
        self.get_table_style = get_table_style
        self.get_button_style = get_button_style
        self.get_input_style = get_input_style
        self.parent_window = parent
        
        # Database connection
        self.db = get_db_instance()
        
        self.suppliers = []
        self._load_suppliers()
        self._calculate_all_supplier_financials()
        
        self._init_ui()
        self._populate_table()
    
    def _init_ui(self):
        """Initialize the UI."""
        
        self.dark_theme = {
            'bg_primary': '#121212',
            'bg_secondary': '#1E1E1E',
            'bg_tertiary': '#161616',
            'bg_hover': '#3A3A3A',
            'border': '#333333',
            'text_primary': '#FFFFFF',
            'text_secondary': '#EEEEEE',
            'text_muted': '#AAAAAA',
            'accent_blue': '#4A9EFF',
            'accent_blue_hover': '#3A8EEF',
            'accent_green': '#10B981',
            'accent_red': '#FF4444',
            'accent_purple': '#A78BFA',
            'button_bg': '#2D2D2D',
            'button_hover': '#3A3A3A'
        }
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header Section
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        
        title = QLabel("👥 Supplier Management")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Manage all your supplier information in one place")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 14px;
            }}
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Action Bar
        action_bar = QFrame()
        action_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        action_layout = QHBoxLayout(action_bar)
        action_layout.setSpacing(15)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search suppliers by name, phone, email, or company...")
        self.search_input.setStyleSheet(self.get_input_style() + """
            QLineEdit {
                padding: 12px 15px;
                font-size: 14px;
                min-width: 400px;
            }
        """)
        self.search_input.textChanged.connect(self._filter_suppliers)
        action_layout.addWidget(self.search_input)
        
        action_layout.addStretch()
        
        # Add Supplier Button
        add_btn = QPushButton("➕ Add New Supplier")
        add_btn.setStyleSheet(self.get_button_style('add') + """
            QPushButton {
                padding: 12px 25px;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self._add_supplier)
        action_layout.addWidget(add_btn)
        
        # Export Button
        export_btn = QPushButton("📊 Export to CSV")
        export_btn.setStyleSheet(self.get_button_style('primary') + """
            QPushButton {
                padding: 12px 25px;
                font-size: 14px;
            }
        """)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.clicked.connect(self._export_suppliers)
        action_layout.addWidget(export_btn)
        
        layout.addWidget(action_bar)
        
        # Statistics Cards - Row 1
        stats_frame1 = QFrame()
        stats_layout1 = QHBoxLayout(stats_frame1)
        stats_layout1.setSpacing(20)
        
        self.total_suppliers_label = self._create_stat_card("Total Suppliers", "0", self.colors['accent_primary'])
        self.active_suppliers_label = self._create_stat_card("Active Suppliers", "0", self.colors['success'])
        self.credit_suppliers_label = self._create_stat_card("Credit Suppliers", "0", self.colors['accent_gold'])
        
        stats_layout1.addWidget(self.total_suppliers_label)
        stats_layout1.addWidget(self.active_suppliers_label)
        stats_layout1.addWidget(self.credit_suppliers_label)
        
        layout.addWidget(stats_frame1)
        
        # Statistics Cards - Row 2 (Financial Summary)
        stats_frame2 = QFrame()
        stats_layout2 = QHBoxLayout(stats_frame2)
        stats_layout2.setSpacing(20)
        
        self.total_pending_label = self._create_stat_card("Total Pending to Pay", "₹0.00", self.colors['danger'])
        self.total_paid_label = self._create_stat_card("Total Amount Paid", "₹0.00", self.colors['success'])
        self.total_received_label = self._create_stat_card("Total Received from Suppliers", "₹0.00", self.colors['accent_cyan'])
        
        stats_layout2.addWidget(self.total_pending_label)
        stats_layout2.addWidget(self.total_paid_label)
        stats_layout2.addWidget(self.total_received_label)
        
        layout.addWidget(stats_frame2)
        
        # Suppliers Table
        table_frame = QFrame()
        table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setSpacing(15)
        
        table_title = QLabel("📋 Supplier Directory")
        table_title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 16px;
                font-weight: bold;
            }}
        """)
        table_layout.addWidget(table_title)
        
        # Create table
        self.suppliers_table = QTableWidget(0, 13)
        self.suppliers_table.setHorizontalHeaderLabels([
            "Supplier Name", "Contact Person", "Phone", "Email", "Company", 
            "Payment Terms", "Pending Amount", "Amount Paid", "Received from Supplier", 
            "GST", "Created Date", "Actions", "ID"
        ])
        
        # Configure table
        self._configure_table()
        
        table_layout.addWidget(self.suppliers_table)
        
        layout.addWidget(table_frame)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        # Update statistics
        self._update_statistics()
    
    def _create_stat_card(self, title, value, color):
        """Create a statistics card."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 20px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 13px;
                font-weight: 500;
            }}
        """)
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 28px;
                font-weight: bold;
            }}
        """)
        value_label.setProperty('stat_value', True)
        card_layout.addWidget(value_label)
        
        return card
    
    def _configure_table(self):
        """Configure table appearance and behavior."""
        # Configure header FIRST before enabling sorting
        header = self.suppliers_table.horizontalHeader()
        header.setVisible(True)  # Ensure header is visible
        # header.setStyleSheet(f"""
        #     QHeaderView::section {{
        #         background-color: {self.colors['accent_primary']};
        #         color: white;
        #         padding: 6px;
        #         border: 1px solid {self.colors['primary_bg']};
        #         font-weight: 600;
        #         font-size: 13px;
        #         text-align: left;
        #     }}
        #     QHeaderView::section:hover {{
        #         background-color: {self.colors['accent_secondary']};
        #     }}
        # """)
        # HARD RESET STYLE - Forces flat design and perfect alignment
        # HARD RESET STYLE - Forces flat design and perfect alignment
        header.setStyleSheet(f"""
            /* 1. RESET THE MAIN TABLE */
            QTableWidget {{
                background-color: #1E1E1E;
                color: #FFFFFF;
                border: 1px solid {self.dark_theme['border']};
                border-radius: 4px;
                gridline-color: #333333;
                selection-background-color: {self.dark_theme['accent_blue']};
                selection-color: #FFFFFF;
                outline: none; /* Removes focus dotted line */
            }}

            /* 2. FORCE THE HEADER CONTAINER TO BE FLAT */
            QHeaderView {{
                background-color: #202020;
                border: none;
                border-bottom: 1px solid {self.dark_theme['border']};
                margin: 0px;
                padding: 0px;
            }}

            /* 3. STYLE THE INDIVIDUAL SECTIONS (COLUMNS) */
            QHeaderView::section {{
                background-color: #202020;
                color: #FFFFFF;
                padding: 4px;
                border: none; /* KEY: Removes the box around every header */
                border-right: 1px solid #333333; /* separator between columns */
                margin: 0px;  /* KEY: Removes the gap causing misalignment */
                border-radius: 0px; /* KEY: Removes rounded corners */
                font-weight: bold;
                font-size: 13px;
                min-height: 40px;
            }}

            /* Remove border for the last header column to look cleaner */
            QHeaderView::section:last {{
                border-right: none;
            }}

            /* 4. ALIGN THE DATA CELLS TO MATCH HEADERS */
            QTableWidget::item {{
                padding-left: 5px; /* Adjust to match Header text alignment */
                border-bottom: 1px solid #252525;
            }}
            
            /* 5. FIX THE TOP-LEFT CORNER BUTTON */
            QTableCornerButton::section {{
                background-color: #202020;
                border: none;
                border-bottom: 1px solid {self.dark_theme['border']};
                border-right: 1px solid {self.dark_theme['border']};
            }}
        """)
        header.setMinimumHeight(60)
        header.setDefaultSectionSize(150)
        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Enable sorting AFTER header is configured
        self.suppliers_table.setSortingEnabled(True)
        
        # Set column widths
        column_widths = {
            0: 180,   # Supplier Name
            1: 150,   # Contact Person
            2: 120,   # Phone
            3: 180,   # Email
            4: 150,   # Company
            5: 140,   # Payment Terms
            6: 150,   # Pending Amount
            7: 140,   # Amount Paid
            8: 180,   # Received from Supplier
            9: 110,   # GST
            10: 120,  # Created Date
            11: 220,  # Actions
            12: 0     # ID (hidden)
        }
        
        for col, width in column_widths.items():
            if width == 0:
                self.suppliers_table.setColumnHidden(col, True)
            else:
                self.suppliers_table.setColumnWidth(col, width)
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        
        # Configure vertical header - hide row numbers
        self.suppliers_table.verticalHeader().setVisible(False)
        self.suppliers_table.verticalHeader().setDefaultSectionSize(55)
        
        # Table styling - Dark theme compatible
        self.suppliers_table.setAlternatingRowColors(True)
        self.suppliers_table.setStyleSheet(self.get_table_style() + f"""
            QTableWidget {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_primary']};
                gridline-color: #3a3a3a;
                font-size: 13px;
                selection-background-color: {self.colors['accent_primary']};
                selection-color: white;
                border: 1px solid #3a3a3a;
            }}
            QTableWidget::item {{
                padding: 8px 10px;
                border: none;
                color: {self.colors['text_primary']};
                background-color: {self.colors['secondary_bg']};
            }}
            QTableWidget::item:alternate {{
                background-color: {self.colors['primary_bg']};
            }}
            QTableWidget::item:selected {{
                background-color: {self.colors['accent_primary']};
                color: white;
            }}
        """)
        
        self.suppliers_table.setMinimumHeight(500)
        self.suppliers_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.suppliers_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    def _load_suppliers(self):
        """Load suppliers from database."""
        try:
            contacts = self.db.get_contacts('SUPPLIER')
            # Convert database format to expected format
            self.suppliers = []
            for contact in contacts:
                supplier = {
                    'id': contact['id'],
                    'name': contact['name'],
                    'contact_person': contact.get('company_name', ''),  # Using company_name as contact_person
                    'phone': contact.get('phone', ''),
                    'email': contact.get('email', ''),
                    'company': contact.get('company_name', ''),
                    'address': contact.get('address', ''),
                    'gst': contact.get('gstin', ''),
                    'opening_balance': float(contact.get('opening_balance', 0)),
                    'financial': {'amount_pending': 0.0, 'amount_paid': 0.0, 'amount_received': 0.0}
                }
                self.suppliers.append(supplier)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load suppliers:\n{str(e)}")
            self.suppliers = []
    
    def _save_suppliers(self):
        """Suppliers are saved directly to database."""
        return True  # No-op, kept for compatibility
    
    def _populate_table(self, suppliers_list=None):
        """Populate table with suppliers including financial data."""
        if suppliers_list is None:
            suppliers_list = self.suppliers
        
        self.suppliers_table.setRowCount(0)
        self.suppliers_table.setSortingEnabled(False)
        
        for supplier in suppliers_list:
            row = self.suppliers_table.rowCount()
            self.suppliers_table.insertRow(row)
            
            # Get financial data
            financial = supplier.get('financial', {
                'amount_pending': 0.0,
                'amount_paid': 0.0,
                'amount_received': 0.0
            })
            
            # Supplier Name
            name_item = QTableWidgetItem(supplier.get('name', ''))
            name_item.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            self.suppliers_table.setItem(row, 0, name_item)
            
            # Contact Person
            self.suppliers_table.setItem(row, 1, QTableWidgetItem(supplier.get('contact_person', 'N/A')))
            
            # Phone
            phone_item = QTableWidgetItem(supplier.get('phone', ''))
            phone_item.setForeground(QColor(self.colors['accent_primary']))
            self.suppliers_table.setItem(row, 2, phone_item)
            
            # Email
            self.suppliers_table.setItem(row, 3, QTableWidgetItem(supplier.get('email', 'N/A')))
            
            # Company
            self.suppliers_table.setItem(row, 4, QTableWidgetItem(supplier.get('company', 'N/A')))
            
            # Payment Terms
            payment_item = QTableWidgetItem(supplier.get('payment_terms', 'Cash'))
            if 'Credit' in supplier.get('payment_terms', ''):
                payment_item.setForeground(QColor(self.colors['accent_gold']))
            else:
                payment_item.setForeground(QColor(self.colors['success']))
            self.suppliers_table.setItem(row, 5, payment_item)
            
            # Pending Amount (Amount Not Yet Paid to Supplier)
            pending = financial.get('amount_pending', 0.0)
            pending_item = QTableWidgetItem(f"₹{pending:,.2f}")
            if pending > 0:
                pending_item.setForeground(QColor(self.colors['danger']))
                pending_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            else:
                pending_item.setForeground(QColor(self.colors['success']))
            self.suppliers_table.setItem(row, 6, pending_item)
            
            # Amount Paid
            paid = financial.get('amount_paid', 0.0)
            paid_item = QTableWidgetItem(f"₹{paid:,.2f}")
            paid_item.setForeground(QColor(self.colors['success']))
            self.suppliers_table.setItem(row, 7, paid_item)
            
            # Amount Received from Supplier
            received = financial.get('amount_received', 0.0)
            received_item = QTableWidgetItem(f"₹{received:,.2f}")
            if received > 0:
                received_item.setForeground(QColor(self.colors['accent_cyan']))
                received_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            else:
                received_item.setForeground(QColor(self.colors['text_secondary']))
            self.suppliers_table.setItem(row, 8, received_item)
            
            # GST
            self.suppliers_table.setItem(row, 9, QTableWidgetItem(supplier.get('gst', 'N/A')))
            
            # Created Date
            created_date = supplier.get('created_date', '')
            if created_date:
                try:
                    date_obj = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
                    formatted_date = date_obj.strftime('%d-%m-%Y')
                except:
                    formatted_date = created_date
            else:
                formatted_date = 'N/A'
            self.suppliers_table.setItem(row, 10, QTableWidgetItem(formatted_date))
            
            # Actions
            actions_widget = self._create_action_buttons(supplier)
            self.suppliers_table.setCellWidget(row, 11, actions_widget)
            
            # ID (hidden)
            self.suppliers_table.setItem(row, 12, QTableWidgetItem(supplier.get('id', '')))
        
        self.suppliers_table.setSortingEnabled(True)
        self._update_statistics()
    
    def _create_action_buttons(self, supplier):
        """Create action buttons for each row."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(4)
        
        # Financial Button
        financial_btn = QPushButton("Pay")
        financial_btn.setToolTip("Manage Payments")
        financial_btn.setFixedSize(45, 28)
        financial_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        financial_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        financial_btn.clicked.connect(lambda: self._manage_supplier_finances(supplier))
        layout.addWidget(financial_btn)
        
        # View Button
        view_btn = QPushButton("View")
        view_btn.setToolTip("View Details")
        view_btn.setFixedSize(45, 28)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #3a8eef;
            }
        """)
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.clicked.connect(lambda: self._view_supplier(supplier))
        layout.addWidget(view_btn)
        
        # Edit Button
        edit_btn = QPushButton("Edit")
        edit_btn.setToolTip("Edit Supplier")
        edit_btn.setFixedSize(45, 28)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5a623;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #e59613;
            }
        """)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(lambda: self._edit_supplier(supplier))
        layout.addWidget(edit_btn)
        
        # Delete Button
        delete_btn = QPushButton("Del")
        delete_btn.setToolTip("Delete Supplier")
        delete_btn.setFixedSize(40, 28)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #ee3333;
            }
        """)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda: self._delete_supplier(supplier))
        layout.addWidget(delete_btn)
        
        layout.addStretch()
        return widget
    
    def _add_supplier(self):
        """Open dialog to add new supplier."""
        dialog = SupplierDialog(self.colors, self.get_input_style, self.get_button_style, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            supplier_data = dialog.get_supplier_data()
            if supplier_data:
                # Add to database
                contact_id = self.db.add_contact(
                    'SUPPLIER',
                    supplier_data['name'],
                    company_name=supplier_data.get('company', ''),
                    phone=supplier_data.get('phone', ''),
                    email=supplier_data.get('email', ''),
                    address=supplier_data.get('address', ''),
                    gstin=supplier_data.get('gst', ''),
                    opening_balance=supplier_data.get('opening_balance', 0)
                )
                
                if contact_id > 0:
                    # Silent save - no popup
                    self._load_suppliers()
                    self._calculate_all_supplier_financials()
                    self._populate_table()
                else:
                    QMessageBox.critical(self, "Error", "Failed to add supplier")
    
    def _edit_supplier(self, supplier):
        """Open dialog to edit supplier."""
        dialog = SupplierDialog(self.colors, self.get_input_style, self.get_button_style, 
                                supplier_data=supplier, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_supplier_data()
            if updated_data:
                # Update in database
                success = self.db.update_contact(
                    supplier['id'],
                    name=updated_data['name'],
                    company_name=updated_data.get('company', ''),
                    phone=updated_data.get('phone', ''),
                    email=updated_data.get('email', ''),
                    address=updated_data.get('address', ''),
                    gstin=updated_data.get('gst', ''),
                    opening_balance=updated_data.get('opening_balance', 0)
                )
                
                if success:
                    # Silent update - no popup
                    self._load_suppliers()
                    self._calculate_all_supplier_financials()
                    self._populate_table()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update supplier")
    
    def _delete_supplier(self, supplier):
        """Delete supplier after confirmation."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete supplier '{supplier['name']}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Delete from database
            success = self.db.delete_contact(supplier['id'])
            
            if success:
                # Silent delete - no popup
                self._load_suppliers()
                self._calculate_all_supplier_financials()
                self._populate_table()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete supplier")
    
    def _view_supplier(self, supplier):
        """View supplier details in a dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Supplier Details")
        dialog.setModal(True)
        dialog.setMinimumWidth(550)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel(f"📋 {supplier.get('name', 'N/A')}")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 22px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(title)
        
        # Details
        details_text = f"""
        <table style='width:100%; border-collapse: collapse;'>
            <tr><td style='padding:8px; font-weight:bold; width:40%;'>Contact Person:</td><td style='padding:8px;'>{supplier.get('contact_person', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Phone:</td><td style='padding:8px;'>{supplier.get('phone', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>Email:</td><td style='padding:8px;'>{supplier.get('email', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Company:</td><td style='padding:8px;'>{supplier.get('company', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>Address:</td><td style='padding:8px;'>{supplier.get('address', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>GST Number:</td><td style='padding:8px;'>{supplier.get('gst', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>PAN Number:</td><td style='padding:8px;'>{supplier.get('pan', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Payment Terms:</td><td style='padding:8px;'>{supplier.get('payment_terms', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>Bank Name:</td><td style='padding:8px;'>{supplier.get('bank_name', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Account Number:</td><td style='padding:8px;'>{supplier.get('account_number', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>IFSC Code:</td><td style='padding:8px;'>{supplier.get('ifsc', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Notes:</td><td style='padding:8px;'>{supplier.get('notes', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>Created Date:</td><td style='padding:8px;'>{supplier.get('created_date', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Modified Date:</td><td style='padding:8px;'>{supplier.get('modified_date', 'N/A')}</td></tr>
        </table>
        """
        
        details_label = QLabel(details_text)
        details_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        details_label.setWordWrap(True)
        layout.addWidget(details_label)
        
        # Close button
        close_btn = QPushButton("✖ Close")
        close_btn.setStyleSheet(self.get_button_style('cancel'))
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec()
    
    def _filter_suppliers(self):
        """Filter suppliers based on search text."""
        search_text = self.search_input.text().lower().strip()
        
        if not search_text:
            self._populate_table()
            return
        
        filtered = [
            s for s in self.suppliers
            if search_text in s.get('name', '').lower()
            or search_text in s.get('phone', '').lower()
            or search_text in s.get('email', '').lower()
            or search_text in s.get('company', '').lower()
            or search_text in s.get('contact_person', '').lower()
        ]
        
        self._populate_table(filtered)
    
    def _update_statistics(self):
        """Update statistics cards including financial summaries."""
        total = len(self.suppliers)
        credit_count = sum(1 for s in self.suppliers if 'Credit' in s.get('payment_terms', ''))
        
        # Calculate financial totals
        total_pending = 0.0
        total_paid = 0.0
        total_received = 0.0
        
        for supplier in self.suppliers:
            financial = supplier.get('financial', {})
            total_pending += financial.get('amount_pending', 0.0)
            total_paid += financial.get('amount_paid', 0.0)
            total_received += financial.get('amount_received', 0.0)
        
        # Update stat cards
        for card in [self.total_suppliers_label, self.active_suppliers_label, self.credit_suppliers_label,
                     self.total_pending_label, self.total_paid_label, self.total_received_label]:
            for label in card.findChildren(QLabel):
                if label.property('stat_value'):
                    if card == self.total_suppliers_label:
                        label.setText(str(total))
                    elif card == self.active_suppliers_label:
                        label.setText(str(total))
                    elif card == self.credit_suppliers_label:
                        label.setText(str(credit_count))
                    elif card == self.total_pending_label:
                        label.setText(f"₹{total_pending:,.2f}")
                    elif card == self.total_paid_label:
                        label.setText(f"₹{total_paid:,.2f}")
                    elif card == self.total_received_label:
                        label.setText(f"₹{total_received:,.2f}")
    
    def _export_suppliers(self):
        """Export suppliers to CSV."""
        if not self.suppliers:
            QMessageBox.warning(self, "No Data", "No suppliers to export!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Suppliers",
            f"suppliers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if filename:
            try:
                import csv
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Headers
                    writer.writerow([
                        'Supplier Name', 'Contact Person', 'Phone', 'Email', 'Company',
                        'Address', 'GST', 'PAN', 'Payment Terms', 'Bank Name',
                        'Account Number', 'IFSC', 'Notes', 'Created Date', 'Modified Date'
                    ])
                    
                    # Data
                    for supplier in self.suppliers:
                        writer.writerow([
                            supplier.get('name', ''),
                            supplier.get('contact_person', ''),
                            supplier.get('phone', ''),
                            supplier.get('email', ''),
                            supplier.get('company', ''),
                            supplier.get('address', ''),
                            supplier.get('gst', ''),
                            supplier.get('pan', ''),
                            supplier.get('payment_terms', ''),
                            supplier.get('bank_name', ''),
                            supplier.get('account_number', ''),
                            supplier.get('ifsc', ''),
                            supplier.get('notes', ''),
                            supplier.get('created_date', ''),
                            supplier.get('modified_date', '')
                        ])
                
                QMessageBox.information(self, "Success", f"Suppliers exported successfully!\n{filename}")
            
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export suppliers:\n{str(e)}")
    
    def _calculate_all_supplier_financials(self):
        """Calculate financial data for all suppliers from database."""
        # Get supplier balances from database
        for supplier in self.suppliers:
            if 'id' in supplier:
                try:
                    balance_info = self.db.get_supplier_balance(supplier['id'])
                    supplier['financial'] = {
                        'total_payable': balance_info.get('total_payable', 0.0),
                        'amount_paid': balance_info.get('total_paid', 0.0),
                        'amount_pending': balance_info.get('balance', 0.0),
                        'amount_received': 0.0,
                        'transactions': []
                    }
                except Exception as e:
                    print(f"Error calculating financials for supplier {supplier.get('name')}: {e}")
                    supplier['financial'] = {
                        'total_payable': 0.0,
                        'amount_paid': 0.0,
                        'amount_pending': 0.0,
                        'amount_received': 0.0,
                        'transactions': []
                    }
    
    def _manage_supplier_finances(self, supplier):
        """Open dialog to manage supplier financial transactions."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Financial Management - {supplier.get('name')}")
        dialog.setModal(True)
        dialog.setMinimumWidth(700)
        dialog.setMinimumHeight(600)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel(f"💰 Financial Overview - {supplier.get('name')}")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 20px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(title)
        
        # Financial Summary Cards
        summary_frame = QFrame()
        summary_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        summary_layout = QVBoxLayout(summary_frame)
        
        financial = supplier.get('financial', {
            'total_payable': 0.0,
            'amount_paid': 0.0,
            'amount_pending': 0.0,
            'amount_received': 0.0
        })
        
        summary_text = f"""
        <table style='width:100%; border-collapse: collapse;'>
            <tr style='background-color:#fee; border-left:5px solid #ff4444;'>
                <td style='padding:15px; font-weight:bold; font-size:14px;'>Amount Not Yet Paid to Supplier:</td>
                <td style='padding:15px; font-weight:bold; font-size:18px; color:#ff4444; text-align:right;'>₹{financial.get('amount_pending', 0.0):,.2f}</td>
            </tr>
            <tr style='background-color:#efe; border-left:5px solid #10b981;'>
                <td style='padding:15px; font-weight:bold; font-size:14px;'>Amount Already Paid to Supplier:</td>
                <td style='padding:15px; font-weight:bold; font-size:18px; color:#10b981; text-align:right;'>₹{financial.get('amount_paid', 0.0):,.2f}</td>
            </tr>
            <tr style='background-color:#eff; border-left:5px solid #06b6d4;'>
                <td style='padding:15px; font-weight:bold; font-size:14px;'>Amount Received from Supplier:</td>
                <td style='padding:15px; font-weight:bold; font-size:18px; color:#06b6d4; text-align:right;'>₹{financial.get('amount_received', 0.0):,.2f}</td>
            </tr>
            <tr style='background-color:#f5f5f5; border-left:5px solid #7c3aed;'>
                <td style='padding:15px; font-weight:bold; font-size:14px;'>Total Payable (from invoices):</td>
                <td style='padding:15px; font-weight:bold; font-size:16px; color:#7c3aed; text-align:right;'>₹{financial.get('total_payable', 0.0):,.2f}</td>
            </tr>
        </table>
        """
        
        summary_label = QLabel(summary_text)
        summary_label.setWordWrap(True)
        summary_layout.addWidget(summary_label)
        
        layout.addWidget(summary_frame)
        
        # Payment Actions
        actions_group = QGroupBox("Record Transaction")
        actions_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.colors['accent_primary']};
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {self.colors['accent_primary']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setSpacing(15)
        
        # Payment to Supplier
        payment_frame = QFrame()
        payment_layout = QHBoxLayout(payment_frame)
        
        payment_label = QLabel("Payment to Supplier:")
        payment_label.setMinimumWidth(180)
        payment_layout.addWidget(payment_label)
        
        payment_input = QDoubleSpinBox()
        payment_input.setRange(0, 999999999)
        payment_input.setDecimals(2)
        payment_input.setPrefix("₹ ")
        payment_input.setStyleSheet(self.get_input_style())
        payment_layout.addWidget(payment_input)
        
        payment_btn = QPushButton("💵 Record Payment")
        payment_btn.setStyleSheet(self.get_button_style('add'))
        payment_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        payment_btn.clicked.connect(lambda: self._record_payment(supplier, payment_input.value(), dialog))
        payment_layout.addWidget(payment_btn)
        
        actions_layout.addWidget(payment_frame)
        
        # Receipt from Supplier
        receipt_frame = QFrame()
        receipt_layout = QHBoxLayout(receipt_frame)
        
        receipt_label = QLabel("Receipt from Supplier:")
        receipt_label.setMinimumWidth(180)
        receipt_layout.addWidget(receipt_label)
        
        receipt_input = QDoubleSpinBox()
        receipt_input.setRange(0, 999999999)
        receipt_input.setDecimals(2)
        receipt_input.setPrefix("₹ ")
        receipt_input.setStyleSheet(self.get_input_style())
        receipt_layout.addWidget(receipt_input)
        
        receipt_btn = QPushButton("📥 Record Receipt")
        receipt_btn.setStyleSheet(self.get_button_style('primary'))
        receipt_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        receipt_btn.clicked.connect(lambda: self._record_receipt(supplier, receipt_input.value(), dialog))
        receipt_layout.addWidget(receipt_btn)
        
        actions_layout.addWidget(receipt_frame)
        
        layout.addWidget(actions_group)
        
        # Transaction History
        history_label = QLabel("📜 Transaction History")
        history_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }}
        """)
        layout.addWidget(history_label)
        
        # Transaction table
        transactions_table = QTableWidget(0, 4)
        transactions_table.setHorizontalHeaderLabels(["Date", "Type", "Amount", "Description"])
        transactions_table.horizontalHeader().setStretchLastSection(True)
        transactions_table.horizontalHeader().setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {self.colors['accent_primary']};
                color: white;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid {self.colors['primary_bg']};
                font-weight: 600;
                font-size: 15px;
            }}
        """)
        transactions_table.horizontalHeader().setMinimumHeight(35)
        transactions_table.setAlternatingRowColors(True)
        transactions_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        transactions_table.setMinimumHeight(200)
        
        # Populate transaction history
        transactions = financial.get('transactions', [])
        for trans in reversed(transactions):  # Show newest first
            row = transactions_table.rowCount()
            transactions_table.insertRow(row)
            
            transactions_table.setItem(row, 0, QTableWidgetItem(trans.get('date', '')))
            
            trans_type = trans.get('type', '')
            type_item = QTableWidgetItem(trans_type)
            if trans_type == 'Payment':
                type_item.setForeground(QColor(self.colors['success']))
            elif trans_type == 'Receipt':
                type_item.setForeground(QColor(self.colors['accent_cyan']))
            transactions_table.setItem(row, 1, type_item)
            
            amount = trans.get('amount', 0.0)
            amount_item = QTableWidgetItem(f"₹{amount:,.2f}")
            amount_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            transactions_table.setItem(row, 2, amount_item)
            
            transactions_table.setItem(row, 3, QTableWidgetItem(trans.get('description', '')))
        
        layout.addWidget(transactions_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh from Invoices")
        refresh_btn.setStyleSheet(self.get_button_style('primary'))
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(lambda: self._refresh_supplier_financials(supplier, dialog))
        button_layout.addWidget(refresh_btn)
        
        close_btn = QPushButton("✖ Close")
        close_btn.setStyleSheet(self.get_button_style('cancel'))
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec()
    
    def _record_payment(self, supplier, amount, dialog):
        """Record a payment made to the supplier."""
        if amount <= 0:
            QMessageBox.warning(self, "Invalid Amount", "Please enter a valid payment amount.")
            return
        
        # Add transaction
        if 'financial' not in supplier:
            supplier['financial'] = {
                'total_payable': 0.0,
                'amount_paid': 0.0,
                'amount_pending': 0.0,
                'amount_received': 0.0,
                'transactions': []
            }
        
        transaction = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'Payment',
            'amount': amount,
            'description': f'Payment made to {supplier.get("name")}'
        }
        
        supplier['financial']['transactions'].append(transaction)
        supplier['financial']['amount_paid'] += amount
        supplier['financial']['amount_pending'] = max(0, supplier['financial']['total_payable'] - supplier['financial']['amount_paid'])
        
        if self._save_suppliers():
            QMessageBox.information(self, "Success", f"Payment of ₹{amount:,.2f} recorded successfully!")
            self._populate_table()
            dialog.accept()
    
    def _record_receipt(self, supplier, amount, dialog):
        """Record a receipt/return from the supplier."""
        if amount <= 0:
            QMessageBox.warning(self, "Invalid Amount", "Please enter a valid receipt amount.")
            return
        
        # Add transaction
        if 'financial' not in supplier:
            supplier['financial'] = {
                'total_payable': 0.0,
                'amount_paid': 0.0,
                'amount_pending': 0.0,
                'amount_received': 0.0,
                'transactions': []
            }
        
        transaction = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': 'Receipt',
            'amount': amount,
            'description': f'Receipt/return from {supplier.get("name")}'
        }
        
        supplier['financial']['transactions'].append(transaction)
        supplier['financial']['amount_received'] += amount
        
        if self._save_suppliers():
            QMessageBox.information(self, "Success", f"Receipt of ₹{amount:,.2f} recorded successfully!")
            self._populate_table()
            dialog.accept()
    
    def _refresh_supplier_financials(self, supplier, dialog):
        """Refresh financial calculations from invoices for a specific supplier."""
        self._calculate_all_supplier_financials()
        self._populate_table()
        dialog.accept()
        QMessageBox.information(self, "Refreshed", "Financial data has been recalculated from invoices.")
        # Reopen dialog with updated data
        self._manage_supplier_finances(supplier)
