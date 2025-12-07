"""
Supplier Payments Page Module
Record payments made to suppliers.
"""
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QTableWidget, QPushButton,
                             QLineEdit, QTableWidgetItem, QMessageBox, 
                             QComboBox, QDoubleSpinBox, QDateEdit, QTextEdit,
                             QHeaderView, QFormLayout)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont
from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.utils.custom_widgets import NoWheelDoubleSpinBox
from travel_billing_software.config.config import format_currency, get_currency_symbol


class SupplierBillingPage(QWidget):
    """Supplier Payments Page - Record payments to suppliers."""
    
    def __init__(self, colors, get_input_style, get_button_style, get_combobox_style, parent=None):
        super().__init__()
        self.colors = colors
        self.get_input_style = get_input_style
        self.get_button_style = get_button_style
        self.get_combobox_style = get_combobox_style
        self.parent_window = parent
        
        # Database connection
        self.db = get_db_instance()
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Header Section
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(10)
        
        title = QLabel("💵 Supplier Payments")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 28px;
                font-weight: bold;
            }}
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Record payments made to suppliers")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 16px;
            }}
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Payment Form Section
        form_frame = QFrame()
        form_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 25px;
            }}
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Form Title
        form_title = QLabel("Payment Details")
        form_title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 22px;
                font-weight: bold;
                margin: 0px;
                padding: 0px 0px 10px 0px;
            }}
        """)
        form_layout.addWidget(form_title)
        
        # Form Fields - Horizontal Layout
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(15)
        fields_layout.setContentsMargins(0, 0, 0, 0)
        
        # Custom input style to prevent interference
        custom_input_style = f"""
            QLineEdit, QDateEdit, QDoubleSpinBox, QComboBox {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_primary']};
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                min-height: 40px;
                margin: 0px;
            }}
            QLineEdit:focus, QDateEdit:focus, QDoubleSpinBox:focus, QComboBox:focus {{
                border: 2px solid {self.colors['accent_primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 35px;
                padding-right: 5px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 10px solid {self.colors['text_primary']};
                margin-right: 8px;
            }}
            QDateEdit::drop-down {{
                border: none;
                width: 35px;
                padding-right: 5px;
            }}
            QDateEdit::down-arrow {{
                image: none;
                border-left: 8px solid transparent;
                border-right: 8px solid transparent;
                border-top: 10px solid {self.colors['text_primary']};
                margin-right: 8px;
            }}
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
                border: none;
                background: transparent;
                width: 30px;
                subcontrol-origin: border;
            }}
            QDoubleSpinBox::up-button {{
                subcontrol-position: top right;
                border-left: 1px solid #3a3a3a;
            }}
            QDoubleSpinBox::down-button {{
                subcontrol-position: bottom right;
                border-left: 1px solid #3a3a3a;
            }}
            QDoubleSpinBox::up-arrow {{
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-bottom: 8px solid {self.colors['text_primary']};
                width: 12px;
                height: 12px;
                margin: 3px;
            }}
            QDoubleSpinBox::down-arrow {{
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid {self.colors['text_primary']};
                width: 12px;
                height: 12px;
                margin: 3px;
            }}
        """
        
        # Supplier Selection
        supplier_row = QHBoxLayout()
        supplier_row.setSpacing(15)
        supplier_row.setContentsMargins(0, 0, 0, 0)
        
        supplier_label = QLabel("Select Supplier *")
        supplier_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 17px; margin: 0px; padding: 0px;")
        supplier_label.setMinimumWidth(180)
        supplier_label.setMaximumWidth(180)
        supplier_row.addWidget(supplier_label)
        
        self.supplier_combo = QComboBox()
        self.supplier_combo.setEditable(True)
        self.supplier_combo.addItems(self._get_supplier_list())
        self.supplier_combo.setStyleSheet(custom_input_style)
        self.supplier_combo.currentTextChanged.connect(self._on_supplier_changed)
        supplier_row.addWidget(self.supplier_combo)
        fields_layout.addLayout(supplier_row)
        
        # Supplier Balance Info (Read-only labels)
        balance_info_layout = QHBoxLayout()
        balance_info_layout.setSpacing(30)
        balance_info_layout.setContentsMargins(180, 5, 0, 5)
        
        self.total_payable_label = QLabel(f"Total Payable: {format_currency(0)}")
        self.total_payable_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-size: 16px; font-weight: bold; margin: 0px; padding: 0px;")
        balance_info_layout.addWidget(self.total_payable_label)
        
        self.already_paid_label = QLabel(f"Already Paid: {format_currency(0)}")
        self.already_paid_label.setStyleSheet(f"color: {self.colors['success']}; font-size: 16px; font-weight: bold; margin: 0px; padding: 0px;")
        balance_info_layout.addWidget(self.already_paid_label)
        
        self.pending_label = QLabel(f"Pending: {format_currency(0)}")
        self.pending_label.setStyleSheet(f"color: {self.colors['danger']}; font-size: 16px; font-weight: bold; margin: 0px; padding: 0px;")
        balance_info_layout.addWidget(self.pending_label)
        
        balance_info_layout.addStretch()
        
        fields_layout.addLayout(balance_info_layout)
        
        # Payment Date
        date_row = QHBoxLayout()
        date_row.setSpacing(15)
        date_row.setContentsMargins(0, 0, 0, 0)
        
        date_label = QLabel("Payment Date *")
        date_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 17px; margin: 0px; padding: 0px;")
        date_label.setMinimumWidth(180)
        date_label.setMaximumWidth(180)
        date_row.addWidget(date_label)
        
        self.payment_date = QDateEdit()
        self.payment_date.setCalendarPopup(True)
        self.payment_date.setDate(QDate.currentDate())
        self.payment_date.setDisplayFormat("dd/MM/yyyy")
        self.payment_date.setStyleSheet(custom_input_style)
        date_row.addWidget(self.payment_date)
        fields_layout.addLayout(date_row)
        
        # Payment Amount
        amount_row = QHBoxLayout()
        amount_row.setSpacing(15)
        amount_row.setContentsMargins(0, 0, 0, 0)
        
        amount_label = QLabel("Payment Amount *")
        amount_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 17px; margin: 0px; padding: 0px;")
        amount_label.setMinimumWidth(180)
        amount_label.setMaximumWidth(180)
        amount_row.addWidget(amount_label)
        
        self.payment_amount = NoWheelDoubleSpinBox()
        self.payment_amount.setRange(0, 9999999)
        self.payment_amount.setDecimals(2)
        self.payment_amount.setPrefix(f"{get_currency_symbol()} ")
        self.payment_amount.setValue(0.0)
        self.payment_amount.setStyleSheet(custom_input_style)
        amount_row.addWidget(self.payment_amount)
        fields_layout.addLayout(amount_row)
        
        # Payment Mode
        mode_row = QHBoxLayout()
        mode_row.setSpacing(15)
        mode_row.setContentsMargins(0, 0, 0, 0)
        
        mode_label = QLabel("Payment Mode *")
        mode_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 17px; margin: 0px; padding: 0px;")
        mode_label.setMinimumWidth(180)
        mode_label.setMaximumWidth(180)
        mode_row.addWidget(mode_label)
        
        self.payment_mode = QComboBox()
        self.payment_mode.addItems(["CASH", "BANK", "UPI", "CHEQUE", "CARD"])
        self.payment_mode.setStyleSheet(custom_input_style)
        mode_row.addWidget(self.payment_mode)
        fields_layout.addLayout(mode_row)
        
        # Reference Number
        ref_row = QHBoxLayout()
        ref_row.setSpacing(15)
        ref_row.setContentsMargins(0, 0, 0, 0)
        
        ref_label = QLabel("Reference Number")
        ref_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 17px; margin: 0px; padding: 0px;")
        ref_label.setMinimumWidth(180)
        ref_label.setMaximumWidth(180)
        ref_row.addWidget(ref_label)
        
        self.reference_number = QLineEdit()
        self.reference_number.setPlaceholderText("Transaction ID / Cheque No / Reference")
        self.reference_number.setStyleSheet(custom_input_style)
        ref_row.addWidget(self.reference_number)
        fields_layout.addLayout(ref_row)
        
        # Notes
        notes_row = QHBoxLayout()
        notes_row.setSpacing(15)
        notes_row.setContentsMargins(0, 0, 0, 0)
        notes_row.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        notes_label = QLabel("Notes")
        notes_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 17px; margin: 0px; padding: 8px 0px 0px 0px;")
        notes_label.setMinimumWidth(180)
        notes_label.setMaximumWidth(180)
        notes_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        notes_row.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional notes (optional)")
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_primary']};
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                margin: 0px;
            }}
            QTextEdit:focus {{
                border: 2px solid {self.colors['accent_primary']};
            }}
        """)
        notes_row.addWidget(self.notes_input)
        fields_layout.addLayout(notes_row)
        
        form_layout.addLayout(fields_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Save Payment")
        save_btn.setMinimumHeight(45)
        save_btn.setMinimumWidth(150)
        save_btn.setStyleSheet(self.get_button_style('add') + """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
            }
        """)
        save_btn.clicked.connect(self._save_payment)
        button_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setMinimumHeight(45)
        reset_btn.setMinimumWidth(120)
        reset_btn.setStyleSheet(self.get_button_style('cancel') + """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
            }
        """)
        reset_btn.clicked.connect(self._reset_form)
        button_layout.addWidget(reset_btn)
        
        form_layout.addLayout(button_layout)
        
        layout.addWidget(form_frame)
        
        # Recent Payments Table
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
        
        table_title = QLabel("📋 Recent Payments")
        table_title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 18px;
                font-weight: bold;
            }}
        """)
        table_layout.addWidget(table_title)
        
        # Create table
        self.payments_table = QTableWidget(0, 7)
        self.payments_table.setHorizontalHeaderLabels([
            "Date", "Supplier", "Amount", "Mode", "Reference", "Notes", "Actions"
        ])
        
        # Complete custom table styling to prevent interference
        self.payments_table.setStyleSheet(f"""
            /* Main Table Widget */
            QTableWidget {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_primary']};
                border: 1px solid #3a3a3a;
                gridline-color: #3a3a3a;
                font-size: 15px;
                selection-background-color: {self.colors['accent_primary']};
                selection-color: white;
                margin: 0px;
                padding: 0px;
                outline: none;
            }}
            
            /* Table Items */
            QTableWidget::item {{
                padding: 12px 10px;
                border: none;
                border-bottom: 1px solid #3a3a3a;
                margin: 0px;
            }}
            
            QTableWidget::item:selected {{
                background-color: {self.colors['accent_primary']};
                color: white;
            }}
            
            /* Header View */
            QHeaderView {{
                background-color: #3a3a3a;
                border: none;
                margin: 0px;
                padding: 0px;
            }}
            
            /* Header Sections */
            QHeaderView::section {{
                background-color: #3a3a3a;
                color: white;
                padding: 15px 10px;
                border: none;
                border-right: 1px solid #2a2a2a;
                border-bottom: 1px solid #2a2a2a;
                font-weight: 600;
                font-size: 16px;
                text-align: left;
                margin: 0px;
            }}
            
            QHeaderView::section:hover {{
                background-color: #4a4a4a;
            }}
            
            QHeaderView::section:first {{
                border-left: none;
            }}
            
            QHeaderView::section:last {{
                border-right: none;
            }}
            
            /* Corner Button */
            QTableCornerButton::section {{
                background-color: #3a3a3a;
                border: none;
                border-right: 1px solid #2a2a2a;
                border-bottom: 1px solid #2a2a2a;
            }}
            
            /* Scrollbars */
            QScrollBar:vertical {{
                background-color: {self.colors['secondary_bg']};
                width: 12px;
                margin: 0px;
                padding: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: #4a4a4a;
                border-radius: 6px;
                min-height: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: #5a5a5a;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
                border: none;
                background: none;
            }}
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            
            QScrollBar:horizontal {{
                background-color: {self.colors['secondary_bg']};
                height: 12px;
                margin: 0px;
                padding: 0px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: #4a4a4a;
                border-radius: 6px;
                min-width: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: #5a5a5a;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
                border: none;
                background: none;
            }}
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
        """)
        
        # Configure header
        header = self.payments_table.horizontalHeader()
        header.setMinimumHeight(50)
        header.setMaximumHeight(50)
        header.setDefaultSectionSize(150)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        header.setSectionsClickable(True)
        header.setHighlightSections(True)
        
        # Configure vertical header
        v_header = self.payments_table.verticalHeader()
        v_header.setDefaultSectionSize(55)
        v_header.setMinimumSectionSize(55)
        v_header.setMaximumSectionSize(55)
        v_header.setVisible(False)
        
        # Configure column widths with fixed sizing
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.payments_table.setColumnWidth(0, 120)  # Date
        self.payments_table.setColumnWidth(1, 180)  # Supplier
        self.payments_table.setColumnWidth(2, 130)  # Amount
        self.payments_table.setColumnWidth(3, 110)  # Mode
        self.payments_table.setColumnWidth(4, 150)  # Reference
        self.payments_table.setColumnWidth(5, 200)  # Notes
        self.payments_table.setColumnWidth(6, 120)  # Actions
        
        # Set last column to stretch
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        
        # Table display settings with explicit values
        self.payments_table.setMinimumHeight(400)
        self.payments_table.setMaximumHeight(600)
        self.payments_table.setAlternatingRowColors(True)
        self.payments_table.setShowGrid(True)
        self.payments_table.setWordWrap(False)
        self.payments_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.payments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.payments_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.payments_table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.payments_table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.payments_table.setCornerButtonEnabled(True)
        self.payments_table.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Remove any margins and padding
        self.payments_table.setContentsMargins(0, 0, 0, 0)
        self.payments_table.setViewportMargins(0, 0, 0, 0)
        
        table_layout.addWidget(self.payments_table)
        
        layout.addWidget(table_frame)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        # Load recent payments
        self._load_recent_payments()
    
    def _get_supplier_list(self):
        """Get list of suppliers from database."""
        try:
            suppliers = self.db.get_contacts('SUPPLIER')
            return [s['name'] for s in suppliers if s.get('name')]
        except:
            return []
    
    def refresh_data(self):
        """Refresh supplier billing data from database."""
        # Reload supplier list in combo box
        current_supplier = self.supplier_combo.currentText()
        self.supplier_combo.clear()
        self.supplier_combo.addItems(self._get_supplier_list())
        
        # Try to restore the previously selected supplier
        if current_supplier:
            index = self.supplier_combo.findText(current_supplier)
            if index >= 0:
                self.supplier_combo.setCurrentIndex(index)
        
        # Reload recent payments
        self._load_recent_payments()
        
        # Update supplier balance display
        self._on_supplier_changed()
    
    def _on_supplier_changed(self):
        """Update supplier balance info when supplier is selected."""
        supplier_name = self.supplier_combo.currentText().strip()
        
        if not supplier_name:
            self.total_payable_label.setText("Total Payable: ₹0.00")
            self.already_paid_label.setText("Already Paid: ₹0.00")
            self.pending_label.setText("Pending: ₹0.00")
            return
        
        try:
            # Get supplier balance from database
            balance_data = self.db.get_supplier_balance(supplier_name)
            
            if balance_data:
                total_payable = balance_data.get('total_payable', 0.0)
                amount_paid = balance_data.get('amount_paid', 0.0)
                pending = balance_data.get('pending', 0.0)
                
                self.total_payable_label.setText(f"Total Payable: {format_currency(total_payable)}")
                self.already_paid_label.setText(f"Already Paid: {format_currency(amount_paid)}")
                self.pending_label.setText(f"Pending: {format_currency(pending)}")
                
                # Auto-fill payment amount with pending amount if positive
                if pending > 0:
                    self.payment_amount.setValue(pending)
            else:
                self.total_payable_label.setText("Total Payable: ₹0.00")
                self.already_paid_label.setText("Already Paid: ₹0.00")
                self.pending_label.setText("Pending: ₹0.00")
        except Exception as e:
            print(f"Error loading supplier balance: {e}")
            self.total_payable_label.setText("Total Payable: ₹0.00")
            self.already_paid_label.setText("Already Paid: ₹0.00")
            self.pending_label.setText("Pending: ₹0.00")
    
    def _save_payment(self):
        """Save payment to database."""
        supplier_name = self.supplier_combo.currentText().strip()
        
        if not supplier_name:
            QMessageBox.warning(self, "Validation Error", "Please select a supplier!")
            return
        
        amount = self.payment_amount.value()
        if amount <= 0:
            QMessageBox.warning(self, "Validation Error", "Please enter a valid payment amount!")
            return
        
        # Get supplier_id from database
        try:
            suppliers = self.db.get_contacts('SUPPLIER')
            supplier_id = None
            for supplier in suppliers:
                if supplier.get('name') == supplier_name:
                    supplier_id = supplier['id']
                    break
            
            if not supplier_id:
                QMessageBox.warning(self, "Validation Error", "Supplier not found in database!")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get supplier: {str(e)}")
            return
        
        # Get payment details
        payment_date = self.payment_date.date().toString("yyyy-MM-dd")
        payment_mode = self.payment_mode.currentText()
        reference = self.reference_number.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        # Save to database
        try:
            payment_id = self.db.add_supplier_payment(
                supplier_id=supplier_id,
                amount=amount,
                payment_mode=payment_mode,
                date=payment_date,
                reference_number=reference,
                notes=notes
            )
            
            if payment_id > 0:
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Payment recorded successfully!\n\nSupplier: {supplier_name}\nAmount: ₹{amount:,.2f}\nMode: {payment_mode}"
                )
                
                # Refresh supplier balance
                self._on_supplier_changed()
                
                # Reload recent payments
                self._load_recent_payments()
                
                # Reset form except supplier selection
                self.payment_amount.setValue(0.0)
                self.reference_number.clear()
                self.notes_input.clear()
                self.payment_date.setDate(QDate.currentDate())
            else:
                QMessageBox.critical(self, "Error", "Failed to save payment to database!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save payment:\n{str(e)}")
    
    def _reset_form(self):
        """Reset form to default state."""
        self.supplier_combo.setCurrentIndex(-1)
        self.payment_date.setDate(QDate.currentDate())
        self.payment_amount.setValue(0.0)
        self.payment_mode.setCurrentIndex(0)
        self.reference_number.clear()
        self.notes_input.clear()
        
        self.total_payable_label.setText("Total Payable: ₹0.00")
        self.already_paid_label.setText("Already Paid: ₹0.00")
        self.pending_label.setText("Pending: ₹0.00")
    
    def _load_recent_payments(self, limit=50):
        """Load recent payments from database."""
        try:
            self.payments_table.setRowCount(0)
            
            # Get recent payments from database
            payments = self.db.get_supplier_payments(limit=limit)
            
            for payment in payments:
                row = self.payments_table.rowCount()
                self.payments_table.insertRow(row)
                
                # Date
                date_item = QTableWidgetItem(payment.get('date', ''))
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.payments_table.setItem(row, 0, date_item)
                
                # Supplier
                supplier_item = QTableWidgetItem(payment.get('supplier_name', ''))
                self.payments_table.setItem(row, 1, supplier_item)
                
                # Amount
                amount = payment.get('amount', 0.0)
                amount_item = QTableWidgetItem(format_currency(amount))
                amount_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.payments_table.setItem(row, 2, amount_item)
                
                # Mode
                mode_item = QTableWidgetItem(payment.get('payment_mode', ''))
                mode_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.payments_table.setItem(row, 3, mode_item)
                
                # Reference
                ref_item = QTableWidgetItem(payment.get('reference', '-'))
                self.payments_table.setItem(row, 4, ref_item)
                
                # Notes
                notes_item = QTableWidgetItem(payment.get('notes', '-'))
                self.payments_table.setItem(row, 5, notes_item)
                
                # Delete button
                delete_btn = QPushButton("🗑️ Delete")
                delete_btn.setStyleSheet(self.get_button_style('delete'))
                delete_btn.clicked.connect(lambda checked, pid=payment['id']: self._delete_payment(pid))
                self.payments_table.setCellWidget(row, 6, delete_btn)
                
        except Exception as e:
            print(f"Error loading recent payments: {e}")
            import traceback
            traceback.print_exc()
    
    def _delete_payment(self, payment_id):
        """Delete a payment record."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this payment record?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.db.delete_supplier_payment(payment_id)
                if success:
                    QMessageBox.information(self, "Success", "Payment record deleted successfully!")
                    self._load_recent_payments()
                    self._on_supplier_changed()  # Refresh balance if same supplier selected
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete payment record!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete payment:\n{str(e)}")
