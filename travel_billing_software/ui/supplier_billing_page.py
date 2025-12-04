"""
Supplier Billing Page Module
Manage supplier bills with items, payments, and automatic calculations.
"""
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QTableWidget, QPushButton,
                             QLineEdit, QTableWidgetItem, QMessageBox, 
                             QComboBox, QDoubleSpinBox, QDateEdit, QCheckBox,
                             QHeaderView, QSpinBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont, QIcon


class SupplierBillingPage(QWidget):
    """Supplier Billing Page with Purchase window style layout."""
    
    def __init__(self, colors, get_input_style, get_button_style, get_combobox_style, parent=None):
        super().__init__()
        self.colors = colors
        self.get_input_style = get_input_style
        self.get_button_style = get_button_style
        self.get_combobox_style = get_combobox_style
        self.parent_window = parent
        
        # Data file paths
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'supplier_bills')
        os.makedirs(self.data_dir, exist_ok=True)
        self.data_file = os.path.join(self.data_dir, 'supplier_bills.json')
        
        # Suppliers directory
        self.suppliers_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'suppliers')
        
        self.bills = []
        self.payment_rows = []
        
        self._load_bills()
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
        
        title = QLabel("📋 Supplier Billing")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Create and manage supplier bills")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 14px;
            }}
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Main Content Frame
        content_frame = QFrame()
        content_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 25px;
            }}
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        
        # TOP ROW - Supplier Details
        top_row = QHBoxLayout()
        top_row.setSpacing(15)
        
        # Supplier ComboBox
        supplier_container = QVBoxLayout()
        supplier_label = QLabel("Supplier *")
        supplier_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        self.supplier_combo = QComboBox()
        self.supplier_combo.setEditable(True)
        self.supplier_combo.addItems(self._get_supplier_list())
        self.supplier_combo.setStyleSheet(self.get_combobox_style() + """
            QComboBox {
                padding: 10px;
                font-size: 14px;
                min-width: 250px;
            }
        """)
        self.supplier_combo.currentTextChanged.connect(self._on_supplier_changed)
        supplier_container.addWidget(supplier_label)
        supplier_container.addWidget(self.supplier_combo)
        top_row.addLayout(supplier_container)
        
        # Phone Number
        phone_container = QVBoxLayout()
        phone_label = QLabel("Phone No.")
        phone_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone number")
        self.phone_input.setReadOnly(True)
        self.phone_input.setStyleSheet(self.get_input_style() + """
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                min-width: 180px;
                background-color: #f5f5f5;
            }
        """)
        phone_container.addWidget(phone_label)
        phone_container.addWidget(self.phone_input)
        top_row.addLayout(phone_container)
        
        # Bill Number
        bill_num_container = QVBoxLayout()
        bill_num_label = QLabel("Bill Number")
        bill_num_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        self.bill_number_input = QLineEdit()
        self.bill_number_input.setPlaceholderText("Auto-generated")
        self.bill_number_input.setText(self._generate_bill_number())
        self.bill_number_input.setStyleSheet(self.get_input_style() + """
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                min-width: 180px;
            }
        """)
        bill_num_container.addWidget(bill_num_label)
        bill_num_container.addWidget(self.bill_number_input)
        top_row.addLayout(bill_num_container)
        
        # Bill Date
        date_container = QVBoxLayout()
        date_label = QLabel("Bill Date")
        date_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 13px;")
        self.bill_date = QDateEdit()
        self.bill_date.setCalendarPopup(True)
        self.bill_date.setDate(QDate.currentDate())
        self.bill_date.setDisplayFormat("dd/MM/yyyy")
        self.bill_date.setStyleSheet(self.get_input_style() + """
            QDateEdit {
                padding: 10px;
                font-size: 14px;
                min-width: 160px;
            }
        """)
        date_container.addWidget(date_label)
        date_container.addWidget(self.bill_date)
        top_row.addLayout(date_container)
        
        top_row.addStretch()
        content_layout.addLayout(top_row)
        
        # ITEM TABLE AREA
        table_section = QVBoxLayout()
        table_section.setSpacing(10)
        
        table_label = QLabel("Items")
        table_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        table_section.addWidget(table_label)
        
        # Items Table
        self.items_table = QTableWidget(0, 4)
        self.items_table.setHorizontalHeaderLabels(["#", "ITEM", "AMOUNT", "DELETE"])
        self.items_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                gridline-color: #e0e0e0;
                font-size: 13px;
            }}
            QHeaderView::section {{
                background-color: {self.colors['accent_primary']};
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
            }}
        """)
        
        # Configure table
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        
        self.items_table.setColumnWidth(0, 50)   # #
        self.items_table.setColumnWidth(2, 150)  # AMOUNT
        self.items_table.setColumnWidth(3, 80)   # DELETE
        
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.setMinimumHeight(250)
        self.items_table.setMaximumHeight(400)
        
        table_section.addWidget(self.items_table)
        
        # Add Row Button
        add_row_btn = QPushButton("➕ ADD ROW")
        add_row_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent_primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {self.colors['accent_secondary']};
            }}
        """)
        add_row_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_row_btn.clicked.connect(self._add_item_row)
        table_section.addWidget(add_row_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        content_layout.addLayout(table_section)
        
        # BOTTOM SECTION - Payments and Summary
        bottom_section = QHBoxLayout()
        bottom_section.setSpacing(30)
        
        # LEFT SIDE - Payment Section
        payment_section = QVBoxLayout()
        payment_section.setSpacing(10)
        
        payment_label = QLabel("Payments")
        payment_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        payment_section.addWidget(payment_label)
        
        # Payment rows container
        self.payment_container = QVBoxLayout()
        self.payment_container.setSpacing(10)
        payment_section.addLayout(self.payment_container)
        
        # Add first two payment rows by default
        self._add_payment_row()
        self._add_payment_row()
        
        # Add Payment Row Button
        add_payment_btn = QPushButton("➕ Add Payment")
        add_payment_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['success']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        add_payment_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_payment_btn.clicked.connect(self._add_payment_row)
        payment_section.addWidget(add_payment_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        payment_section.addStretch()
        bottom_section.addLayout(payment_section, 1)
        
        # RIGHT SIDE - Summary Panel
        summary_section = QVBoxLayout()
        summary_section.setSpacing(15)
        
        summary_frame = QFrame()
        summary_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary_bg']};
                border: 2px solid {self.colors['accent_primary']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setSpacing(12)
        
        summary_title = QLabel("Summary")
        summary_title.setStyleSheet(f"color: {self.colors['accent_primary']}; font-weight: bold; font-size: 15px;")
        summary_layout.addWidget(summary_title)
        
        # Round Off Checkbox and Input
        roundoff_layout = QHBoxLayout()
        self.roundoff_checkbox = QCheckBox("Round Off")
        self.roundoff_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {self.colors['text_primary']};
                font-size: 13px;
                font-weight: bold;
            }}
        """)
        self.roundoff_checkbox.stateChanged.connect(self._calculate_totals)
        roundoff_layout.addWidget(self.roundoff_checkbox)
        
        self.roundoff_input = QLineEdit("0.00")
        self.roundoff_input.setReadOnly(True)
        self.roundoff_input.setStyleSheet(self.get_input_style() + """
            QLineEdit {
                padding: 8px;
                font-size: 13px;
                max-width: 100px;
                background-color: #f5f5f5;
            }
        """)
        roundoff_layout.addWidget(self.roundoff_input)
        roundoff_layout.addStretch()
        summary_layout.addLayout(roundoff_layout)
        
        # Total
        total_layout = QHBoxLayout()
        total_label = QLabel("Total:")
        total_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        total_layout.addWidget(total_label)
        
        self.total_input = QLineEdit("₹0.00")
        self.total_input.setReadOnly(True)
        self.total_input.setStyleSheet(self.get_input_style() + f"""
            QLineEdit {{
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                color: {self.colors['accent_primary']};
                background-color: #f0f0ff;
                border: 2px solid {self.colors['accent_primary']};
            }}
        """)
        total_layout.addWidget(self.total_input)
        summary_layout.addLayout(total_layout)
        
        # Paid
        paid_layout = QHBoxLayout()
        paid_label = QLabel("Paid:")
        paid_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        paid_layout.addWidget(paid_label)
        
        self.paid_input = QLineEdit("₹0.00")
        self.paid_input.setReadOnly(True)
        self.paid_input.setStyleSheet(self.get_input_style() + f"""
            QLineEdit {{
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                color: {self.colors['success']};
                background-color: #f0fff0;
                border: 2px solid {self.colors['success']};
            }}
        """)
        paid_layout.addWidget(self.paid_input)
        summary_layout.addLayout(paid_layout)
        
        # Balance
        balance_layout = QHBoxLayout()
        balance_label = QLabel("Balance:")
        balance_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold; font-size: 14px;")
        balance_layout.addWidget(balance_label)
        
        self.balance_input = QLineEdit("₹0.00")
        self.balance_input.setReadOnly(True)
        self.balance_input.setStyleSheet(self.get_input_style() + f"""
            QLineEdit {{
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                color: {self.colors['danger']};
                background-color: #fff0f0;
                border: 2px solid {self.colors['danger']};
            }}
        """)
        balance_layout.addWidget(self.balance_input)
        summary_layout.addLayout(balance_layout)
        
        summary_section.addWidget(summary_frame)
        summary_section.addStretch()
        
        bottom_section.addLayout(summary_section, 1)
        
        content_layout.addLayout(bottom_section)
        
        # BOTTOM BUTTONS
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addStretch()
        
        # Share Button
        share_btn = QPushButton("📤 Share")
        share_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.colors['accent_secondary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #9333EA;
            }}
        """)
        share_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        share_btn.clicked.connect(self._share_bill)
        button_layout.addWidget(share_btn)
        
        # Save Button (Primary Blue)
        save_btn = QPushButton("💾 Save")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #4a9eff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 40px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #3a8eef;
            }}
        """)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._save_bill)
        button_layout.addWidget(save_btn)
        
        content_layout.addLayout(button_layout)
        
        layout.addWidget(content_frame)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        # Add first item row
        self._add_item_row()
    
    def _get_supplier_list(self):
        """Get list of suppliers from suppliers.json."""
        suppliers_file = os.path.join(self.suppliers_dir, 'suppliers.json')
        if os.path.exists(suppliers_file):
            try:
                with open(suppliers_file, 'r', encoding='utf-8') as f:
                    suppliers = json.load(f)
                return [s.get('name', '') for s in suppliers if s.get('name')]
            except:
                pass
        return ["Supplier 1", "Supplier 2", "Supplier 3"]
    
    def _on_supplier_changed(self):
        """Update phone number when supplier is selected."""
        supplier_name = self.supplier_combo.currentText()
        suppliers_file = os.path.join(self.suppliers_dir, 'suppliers.json')
        
        if os.path.exists(suppliers_file):
            try:
                with open(suppliers_file, 'r', encoding='utf-8') as f:
                    suppliers = json.load(f)
                
                for supplier in suppliers:
                    if supplier.get('name') == supplier_name:
                        self.phone_input.setText(supplier.get('phone', ''))
                        return
            except:
                pass
        
        self.phone_input.setText('')
    
    def _generate_bill_number(self):
        """Generate unique bill number."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"SBILL-{timestamp}"
    
    def _add_item_row(self):
        """Add a new item row to the table."""
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        
        # Column 0: # (Serial Number)
        serial_item = QTableWidgetItem(str(row + 1))
        serial_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        serial_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.items_table.setItem(row, 0, serial_item)
        
        # Column 1: ITEM (LineEdit)
        item_input = QLineEdit()
        item_input.setPlaceholderText("Enter item description")
        item_input.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 8px;
                font-size: 13px;
                background-color: transparent;
            }
            QLineEdit:focus {
                background-color: #f0f0ff;
            }
        """)
        self.items_table.setCellWidget(row, 1, item_input)
        
        # Column 2: AMOUNT (DoubleSpinBox)
        amount_input = QDoubleSpinBox()
        amount_input.setRange(0, 9999999)
        amount_input.setDecimals(2)
        amount_input.setPrefix("₹ ")
        amount_input.setValue(0.0)
        amount_input.setStyleSheet("""
            QDoubleSpinBox {
                border: none;
                padding: 8px;
                font-size: 13px;
                background-color: transparent;
            }
            QDoubleSpinBox:focus {
                background-color: #f0f0ff;
            }
        """)
        amount_input.valueChanged.connect(self._calculate_totals)
        self.items_table.setCellWidget(row, 2, amount_input)
        
        # Column 3: DELETE (Button)
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Delete Row")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ee3333;
            }
        """)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda: self._delete_item_row(row))
        self.items_table.setCellWidget(row, 3, delete_btn)
        
        self.items_table.setRowHeight(row, 45)
    
    def _delete_item_row(self, row):
        """Delete an item row from the table."""
        self.items_table.removeRow(row)
        # Update serial numbers
        for i in range(self.items_table.rowCount()):
            item = self.items_table.item(i, 0)
            if item:
                item.setText(str(i + 1))
        self._calculate_totals()
    
    def _add_payment_row(self):
        """Add a new payment row."""
        payment_row_layout = QHBoxLayout()
        payment_row_layout.setSpacing(10)
        
        # Payment Type ComboBox
        payment_type = QComboBox()
        payment_type.addItems(["Cash", "Bank Transfer", "Credit Card", "Debit Card", "UPI", "Cheque"])
        payment_type.setStyleSheet(self.get_combobox_style() + """
            QComboBox {
                padding: 8px;
                font-size: 13px;
                min-width: 150px;
            }
        """)
        payment_row_layout.addWidget(payment_type)
        
        # Amount Input
        amount_input = QDoubleSpinBox()
        amount_input.setRange(0, 9999999)
        amount_input.setDecimals(2)
        amount_input.setPrefix("₹ ")
        amount_input.setValue(0.0)
        amount_input.setStyleSheet(self.get_input_style() + """
            QDoubleSpinBox {
                padding: 8px;
                font-size: 13px;
                min-width: 150px;
            }
        """)
        amount_input.valueChanged.connect(self._calculate_totals)
        payment_row_layout.addWidget(amount_input)
        
        # Delete Button
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Remove Payment")
        delete_btn.setFixedSize(35, 35)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ee3333;
            }
        """)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda: self._delete_payment_row(payment_row_layout))
        payment_row_layout.addWidget(delete_btn)
        
        payment_row_layout.addStretch()
        
        # Store reference
        payment_row = {
            'layout': payment_row_layout,
            'type': payment_type,
            'amount': amount_input,
            'delete_btn': delete_btn
        }
        self.payment_rows.append(payment_row)
        
        self.payment_container.addLayout(payment_row_layout)
    
    def _delete_payment_row(self, layout):
        """Delete a payment row."""
        # Find and remove from payment_rows list
        for payment_row in self.payment_rows:
            if payment_row['layout'] == layout:
                self.payment_rows.remove(payment_row)
                break
        
        # Remove widgets from layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Remove layout from container
        self.payment_container.removeItem(layout)
        layout.deleteLater()
        
        self._calculate_totals()
    
    def _calculate_totals(self):
        """Calculate total, paid, and balance amounts."""
        # Calculate total from items
        total = 0.0
        for row in range(self.items_table.rowCount()):
            amount_widget = self.items_table.cellWidget(row, 2)
            if amount_widget:
                total += amount_widget.value()
        
        # Apply round off if checked
        roundoff = 0.0
        if self.roundoff_checkbox.isChecked():
            rounded_total = round(total)
            roundoff = rounded_total - total
            total = rounded_total
        
        self.roundoff_input.setText(f"{roundoff:.2f}")
        
        # Calculate paid from payments
        paid = 0.0
        for payment_row in self.payment_rows:
            paid += payment_row['amount'].value()
        
        # Calculate balance
        balance = total - paid
        
        # Update display
        self.total_input.setText(f"₹{total:,.2f}")
        self.paid_input.setText(f"₹{paid:,.2f}")
        self.balance_input.setText(f"₹{balance:,.2f}")
        
        # Update balance color
        if balance > 0:
            self.balance_input.setStyleSheet(self.get_input_style() + f"""
                QLineEdit {{
                    padding: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    color: {self.colors['danger']};
                    background-color: #fff0f0;
                    border: 2px solid {self.colors['danger']};
                }}
            """)
        elif balance < 0:
            self.balance_input.setStyleSheet(self.get_input_style() + f"""
                QLineEdit {{
                    padding: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    color: {self.colors['warning']};
                    background-color: #fff8f0;
                    border: 2px solid {self.colors['warning']};
                }}
            """)
        else:
            self.balance_input.setStyleSheet(self.get_input_style() + f"""
                QLineEdit {{
                    padding: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    color: {self.colors['success']};
                    background-color: #f0fff0;
                    border: 2px solid {self.colors['success']};
                }}
            """)
    
    def _save_bill(self):
        """Save supplier bill."""
        supplier = self.supplier_combo.currentText().strip()
        
        if not supplier:
            QMessageBox.warning(self, "Validation Error", "Please select a supplier!")
            return
        
        # Collect items
        items = []
        for row in range(self.items_table.rowCount()):
            item_widget = self.items_table.cellWidget(row, 1)
            amount_widget = self.items_table.cellWidget(row, 2)
            
            if item_widget and amount_widget:
                item_name = item_widget.text().strip()
                amount = amount_widget.value()
                
                if item_name and amount > 0:
                    items.append({
                        'item': item_name,
                        'amount': amount
                    })
        
        if not items:
            QMessageBox.warning(self, "Validation Error", "Please add at least one item with amount!")
            return
        
        # Collect payments
        payments = []
        for payment_row in self.payment_rows:
            payment_type = payment_row['type'].currentText()
            amount = payment_row['amount'].value()
            
            if amount > 0:
                payments.append({
                    'type': payment_type,
                    'amount': amount
                })
        
        # Calculate totals
        total = sum(item['amount'] for item in items)
        if self.roundoff_checkbox.isChecked():
            roundoff = round(total) - total
            total = round(total)
        else:
            roundoff = 0.0
        
        paid = sum(p['amount'] for p in payments)
        balance = total - paid
        
        # Create bill data
        bill_data = {
            'id': str(datetime.now().timestamp()),
            'bill_number': self.bill_number_input.text(),
            'supplier': supplier,
            'phone': self.phone_input.text(),
            'bill_date': self.bill_date.date().toString("yyyy-MM-dd"),
            'items': items,
            'payments': payments,
            'roundoff': roundoff,
            'total': total,
            'paid': paid,
            'balance': balance,
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to file
        self.bills.append(bill_data)
        if self._save_bills():
            QMessageBox.information(
                self, 
                "Success", 
                f"Supplier bill saved successfully!\n\nBill Number: {bill_data['bill_number']}\nTotal: ₹{total:,.2f}\nBalance: ₹{balance:,.2f}"
            )
            self._reset_form()
        else:
            QMessageBox.critical(self, "Error", "Failed to save supplier bill!")
    
    def _reset_form(self):
        """Reset form to default state."""
        self.supplier_combo.setCurrentIndex(-1)
        self.phone_input.clear()
        self.bill_number_input.setText(self._generate_bill_number())
        self.bill_date.setDate(QDate.currentDate())
        
        # Clear items table
        self.items_table.setRowCount(0)
        self._add_item_row()
        
        # Clear payment rows
        for payment_row in self.payment_rows[:]:
            self._delete_payment_row(payment_row['layout'])
        
        self.payment_rows = []
        self._add_payment_row()
        self._add_payment_row()
        
        self.roundoff_checkbox.setChecked(False)
        self._calculate_totals()
    
    def _share_bill(self):
        """Share bill (placeholder for future implementation)."""
        QMessageBox.information(
            self, 
            "Share Bill", 
            "Share functionality will be implemented soon!\n\nYou can export the bill as PDF or send via email/WhatsApp."
        )
    
    def _load_bills(self):
        """Load bills from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.bills = json.load(f)
            except:
                self.bills = []
        else:
            self.bills = []
    
    def _save_bills(self):
        """Save bills to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.bills, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving bills: {e}")
            return False
