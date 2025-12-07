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
        layout.setSpacing(25)
        
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
        form_layout.setSpacing(20)
        
        # Form Title
        form_title = QLabel("Payment Details")
        form_title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 20px;
                font-weight: bold;
            }}
        """)
        form_layout.addWidget(form_title)
        
        # Form Fields
        fields_layout = QFormLayout()
        fields_layout.setSpacing(15)
        fields_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Supplier Selection
        supplier_label = QLabel("Select Supplier: *")
        supplier_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 15px;")
        
        self.supplier_combo = QComboBox()
        self.supplier_combo.setEditable(True)
        self.supplier_combo.addItems(self._get_supplier_list())
        self.supplier_combo.setStyleSheet(self.get_combobox_style())
        self.supplier_combo.currentTextChanged.connect(self._on_supplier_changed)
        fields_layout.addRow(supplier_label, self.supplier_combo)
        
        # Supplier Balance Info (Read-only labels)
        balance_info_layout = QHBoxLayout()
        
        self.total_payable_label = QLabel("Total Payable: ₹0.00")
        self.total_payable_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-size: 14px; font-weight: bold;")
        balance_info_layout.addWidget(self.total_payable_label)
        
        self.already_paid_label = QLabel("Already Paid: ₹0.00")
        self.already_paid_label.setStyleSheet(f"color: {self.colors['success']}; font-size: 14px; font-weight: bold;")
        balance_info_layout.addWidget(self.already_paid_label)
        
        self.pending_label = QLabel("Pending: ₹0.00")
        self.pending_label.setStyleSheet(f"color: {self.colors['danger']}; font-size: 14px; font-weight: bold;")
        balance_info_layout.addWidget(self.pending_label)
        
        balance_info_layout.addStretch()
        
        fields_layout.addRow("", balance_info_layout)
        
        # Payment Date
        date_label = QLabel("Payment Date: *")
        date_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 15px;")
        
        self.payment_date = QDateEdit()
        self.payment_date.setCalendarPopup(True)
        self.payment_date.setDate(QDate.currentDate())
        self.payment_date.setDisplayFormat("dd/MM/yyyy")
        self.payment_date.setStyleSheet(self.get_input_style())
        fields_layout.addRow(date_label, self.payment_date)
        
        # Payment Amount
        amount_label = QLabel("Payment Amount: *")
        amount_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 15px;")
        
        self.payment_amount = QDoubleSpinBox()
        self.payment_amount.setRange(0, 9999999)
        self.payment_amount.setDecimals(2)
        self.payment_amount.setPrefix("₹ ")
        self.payment_amount.setValue(0.0)
        self.payment_amount.setStyleSheet(self.get_input_style())
        fields_layout.addRow(amount_label, self.payment_amount)
        
        # Payment Mode
        mode_label = QLabel("Payment Mode: *")
        mode_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 15px;")
        
        self.payment_mode = QComboBox()
        self.payment_mode.addItems(["CASH", "BANK", "UPI", "CHEQUE", "CARD"])
        self.payment_mode.setStyleSheet(self.get_combobox_style())
        fields_layout.addRow(mode_label, self.payment_mode)
        
        # Reference Number
        ref_label = QLabel("Reference Number:")
        ref_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 15px;")
        
        self.reference_number = QLineEdit()
        self.reference_number.setPlaceholderText("Transaction ID / Cheque No / Reference")
        self.reference_number.setStyleSheet(self.get_input_style())
        fields_layout.addRow(ref_label, self.reference_number)
        
        # Notes
        notes_label = QLabel("Notes:")
        notes_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 15px;")
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional notes (optional)")
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setStyleSheet(self.get_input_style())
        fields_layout.addRow(notes_label, self.notes_input)
        
        form_layout.addLayout(fields_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Save Payment")
        save_btn.setStyleSheet(self.get_button_style('add'))
        save_btn.clicked.connect(self._save_payment)
        button_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setStyleSheet(self.get_button_style('cancel'))
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
        
        # Use standard table styling
        self.payments_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_primary']};
                gridline-color: #3a3a3a;
                font-size: 14px;
                selection-background-color: {self.colors['accent_primary']};
                selection-color: white;
                border: 1px solid #3a3a3a;
            }}
            QHeaderView::section {{
                background-color: {self.colors['accent_primary']};
                color: white;
                padding: 8px;
                border: 1px solid {self.colors['primary_bg']};
                font-weight: bold;
                font-size: 14px;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
        """)
        
        # Configure table
        header = self.payments_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        
        self.payments_table.setColumnWidth(0, 100)
        self.payments_table.setColumnWidth(2, 120)
        self.payments_table.setColumnWidth(3, 100)
        self.payments_table.setColumnWidth(4, 150)
        self.payments_table.setColumnWidth(6, 100)
        
        self.payments_table.verticalHeader().setVisible(False)
        self.payments_table.setAlternatingRowColors(True)
        self.payments_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.payments_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.payments_table.setMinimumHeight(300)
        
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
                
                self.total_payable_label.setText(f"Total Payable: ₹{total_payable:,.2f}")
                self.already_paid_label.setText(f"Already Paid: ₹{amount_paid:,.2f}")
                self.pending_label.setText(f"Pending: ₹{pending:,.2f}")
                
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
                reference=reference,
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
                amount_item = QTableWidgetItem(f"₹{amount:,.2f}")
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
