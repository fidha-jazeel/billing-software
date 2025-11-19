"""
Dynamic Home Page (Billing Page) for Travel Agency Billing Software
This module creates a dynamic, modular billing interface with:
- Real-time calculation updates
- Dynamic table row management  
- Auto-save functionality
- Invoice number generation
- Responsive layout
"""

from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QDoubleSpinBox,
    QComboBox, QDateEdit, QScrollArea, QGridLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QColor
from datetime import datetime
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import configuration and utilities
from config import (
    APP_CONFIG, COMPANY_INFO, COLORS, INVOICE_CONFIG, LAYOUT_CONFIG,
    get_supplier_list, get_sector_list, get_company_info_formatted,
    get_currency_symbol, get_invoice_prefix
)
from utils.styles import (
    get_frame_style, get_label_style, get_input_style, get_dateedit_style,
    get_combobox_style, get_spinbox_style, get_button_style
)

# Import database manager
try:
    from database import DatabaseManager, get_db_instance
    DB_ENABLED = True
except ImportError:
    DB_ENABLED = False
    print("⚠️  Database module not available in home_page. Using JSON-only mode.")


class HomePage(QWidget):
    """
    Dynamic Home/Billing Page with real-time updates and intelligent features.
    
    Features:
    - Auto-generates invoice numbers with timestamp
    - Real-time calculation as user types
    - Dynamic table row addition/removal
    - Dropdown menus for sectors and suppliers
    - Automatic subtotal, tax, and balance calculation
    - Save to JSON and Database
    - PDF generation support
    """
    
    # Signals for communication with main window
    invoice_saved = pyqtSignal(str)  # Emits invoice number when saved
    calculation_updated = pyqtSignal(float, float, float)  # subtotal, tax, total
    
    def __init__(self, db_manager=None, parent=None):
        super().__init__(parent)
        
        # Database instance
        self.db = db_manager if db_manager else (get_db_instance() if DB_ENABLED else None)
        
        # Track invoice state
        self.current_invoice_id = None
        self.is_modified = False
        
        self._init_ui()
        
        # Add initial row
        self.add_item_row()
        
    def _init_ui(self):
        """Initialize the dynamic UI with all components."""
        
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area for entire page
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS['primary_bg']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {COLORS['secondary_bg']};
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['accent_primary']};
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {COLORS['accent_secondary']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Welcome heading
        welcome_heading = QLabel(f"✈️ {COMPANY_INFO['name']} - New Invoice")
        welcome_heading.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['accent_cyan']};
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin-bottom: 10px;
            }}
        """)
        welcome_heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_heading)
        
        # Create sections
        layout.addWidget(self._create_invoice_details_section())
        layout.addWidget(self._create_table_section())
        layout.addWidget(self._create_calculation_section())
        layout.addLayout(self._create_action_buttons())
        
        layout.addSpacing(20)
        
        # Set content to scroll area
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def _create_invoice_details_section(self) -> QFrame:
        """Create the invoice details input section."""
        frame = QFrame()
        frame.setStyleSheet(get_frame_style())
        layout = QGridLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Title
        title = QLabel(f"<b style='color:{COLORS['accent_secondary']}; font-size:14px;'>📄 Invoice Details</b>")
        layout.addWidget(title, 0, 0, 1, 4)
        
        # Row 1: Invoice Number and Date
        layout.addWidget(self._create_label("Invoice Number:"), 1, 0, Qt.AlignRight)
        self.invoice_number = QLineEdit()
        self.invoice_number.setText(self._generate_invoice_number())
        self.invoice_number.setPlaceholderText("Auto-generated")
        self.invoice_number.setStyleSheet(get_input_style())
        self.invoice_number.setFixedWidth(220)
        self.invoice_number.textChanged.connect(lambda: self._mark_modified())
        layout.addWidget(self.invoice_number, 1, 1, Qt.AlignLeft)
        
        layout.addWidget(self._create_label("Invoice Date:"), 1, 2, Qt.AlignRight)
        self.invoice_date = QDateEdit()
        self.invoice_date.setDate(QDate.currentDate())
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDisplayFormat(INVOICE_CONFIG['date_format'])
        self.invoice_date.setStyleSheet(get_dateedit_style())
        self.invoice_date.setFixedWidth(220)
        self.invoice_date.dateChanged.connect(lambda: self._mark_modified())
        layout.addWidget(self.invoice_date, 1, 3, Qt.AlignLeft)
        
        # Row 2: Customer Name and Contact
        layout.addWidget(self._create_label("Customer Name:"), 2, 0, Qt.AlignRight)
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        self.customer_name.setStyleSheet(get_input_style())
        self.customer_name.setFixedWidth(220)
        self.customer_name.textChanged.connect(lambda: self._mark_modified())
        layout.addWidget(self.customer_name, 2, 1, Qt.AlignLeft)
        
        layout.addWidget(self._create_label("Contact Number:"), 2, 2, Qt.AlignRight)
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Enter contact number")
        self.contact_number.setStyleSheet(get_input_style())
        self.contact_number.setFixedWidth(220)
        self.contact_number.textChanged.connect(lambda: self._mark_modified())
        layout.addWidget(self.contact_number, 2, 3, Qt.AlignLeft)
        
        return frame
    
    def _create_table_section(self) -> QFrame:
        """Create the dynamic items table section."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['secondary_bg']};
                border-radius: 8px;
                border: 1px solid #444;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header with Add Item button
        header_layout = QHBoxLayout()
        title = QLabel(f"<b style='color:{COLORS['accent_secondary']}; font-size:14px;'>🧾 Billed Items</b>")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        btn_add_item = QPushButton("➕ Add Item")
        btn_add_item.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_secondary']};
            }}
        """)
        btn_add_item.clicked.connect(self.add_item_row)
        btn_add_item.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(btn_add_item)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "Item Name", "Ticket", "Sector", "Supplier", "Price (₹)", "Qty", "Tax (%)", "Amount (₹)", "Actions"
        ])
        
        # Configure table
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 200)
        for col in range(1, 9):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        
        self.table.setMinimumHeight(300)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLORS['primary_bg']};
                color: {COLORS['text_primary']};
                gridline-color: #444;
                border: 1px solid #444;
                border-radius: 5px;
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {COLORS['accent_primary']};
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
            }}
        """)
        
        layout.addWidget(self.table)
        
        return frame
    
    def _create_calculation_section(self) -> QFrame:
        """Create the invoice calculation section with real-time updates."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['secondary_bg']};
                border-radius: 8px;
                border: 1px solid {COLORS['accent_primary']};
                padding: 10px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        title = QLabel(f"<b style='color:{COLORS['accent_secondary']}; font-size:14px;'>💰 Invoice Calculation</b>")
        layout.addWidget(title)
        
        # Grid for calculations
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.setContentsMargins(5, 5, 5, 5)
        
        # Subtotal
        grid.addWidget(self._create_label("Subtotal:"), 0, 0, Qt.AlignRight)
        self.lbl_subtotal = self._create_value_label(f"{get_currency_symbol()}0.00", COLORS['accent_secondary'])
        grid.addWidget(self.lbl_subtotal, 0, 1, Qt.AlignLeft)
        
        # Tax
        grid.addWidget(self._create_label("Tax:"), 1, 0, Qt.AlignRight)
        self.lbl_tax = self._create_value_label(f"{get_currency_symbol()}0.00", COLORS['accent_secondary'])
        grid.addWidget(self.lbl_tax, 1, 1, Qt.AlignLeft)
        
        # Total
        grid.addWidget(self._create_label("Total:", size=14), 2, 0, Qt.AlignRight)
        self.lbl_total = self._create_value_label(f"{get_currency_symbol()}0.00", COLORS['accent_gold'], size=15, border=2)
        grid.addWidget(self.lbl_total, 2, 1, Qt.AlignLeft)
        
        # Received
        grid.addWidget(self._create_label("Received:"), 3, 0, Qt.AlignRight)
        self.txt_received = QLineEdit()
        self.txt_received.setPlaceholderText(f"{get_currency_symbol()}0.00")
        self.txt_received.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['primary_bg']};
                color: {COLORS['success']};
                border: 1px solid {COLORS['success']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                font-weight: bold;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['success']};
            }}
        """)
        self.txt_received.setMinimumWidth(120)
        self.txt_received.textChanged.connect(self._calculate_balance)
        grid.addWidget(self.txt_received, 3, 1, Qt.AlignLeft)
        
        # Balance
        grid.addWidget(self._create_label("Balance:"), 4, 0, Qt.AlignRight)
        self.lbl_balance = self._create_value_label(f"{get_currency_symbol()}0.00", COLORS['danger'])
        grid.addWidget(self.lbl_balance, 4, 1, Qt.AlignLeft)
        
        layout.addLayout(grid)
        
        return frame
    
    def _create_action_buttons(self) -> QHBoxLayout:
        """Create action buttons for saving and exporting."""
        layout = QHBoxLayout()
        layout.addStretch()
        
        # Save Invoice
        btn_save = QPushButton("💾 Save Invoice")
        btn_save.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
                min-width: 110px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_cyan']};
            }}
        """)
        btn_save.clicked.connect(self.save_invoice)
        btn_save.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_save)
        
        # Save PDF
        btn_pdf = QPushButton("📄 Download PDF")
        btn_pdf.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
                min-width: 110px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold']};
            }}
        """)
        btn_pdf.clicked.connect(self.save_pdf)
        btn_pdf.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_pdf)
        
        # Print
        btn_print = QPushButton("🖨️ Print")
        btn_print.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
                min-width: 110px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_secondary']};
            }}
        """)
        btn_print.clicked.connect(self.print_invoice)
        btn_print.setCursor(Qt.PointingHandCursor)
        layout.addWidget(btn_print)
        
        return layout
    
    def _create_label(self, text: str, size: int = 12) -> QLabel:
        """Helper to create styled labels."""
        label = QLabel(text)
        label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-weight: bold;
            font-size: {size}px;
        """)
        label.setMinimumWidth(90)
        return label
    
    def _create_value_label(self, text: str, color: str, size: int = 13, border: int = 1) -> QLabel:
        """Helper to create styled value labels."""
        label = QLabel(text)
        label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-weight: bold;
                font-size: {size}px;
                background-color: {COLORS['primary_bg']};
                padding: 5px 10px;
                border-radius: 4px;
                border: {border}px solid {color};
            }}
        """)
        label.setMinimumWidth(120)
        return label
    
    def _generate_invoice_number(self) -> str:
        """Generate unique invoice number with timestamp."""
        now = datetime.now()
        return f"{get_invoice_prefix()}-{now.strftime('%Y%m%d-%H%M%S')}"
    
    def _mark_modified(self):
        """Mark invoice as modified."""
        self.is_modified = True
    
    def add_item_row(self):
        """Dynamically add a new row to the table."""
        table = self.table
        row = table.rowCount()
        table.insertRow(row)
        
        # Adjust table height
        self.table.setMinimumHeight(min(300 + (row * 45), 600))
        
        # Item Name
        item_name = QLineEdit()
        item_name.setPlaceholderText("Enter item name")
        item_name.setStyleSheet(get_input_style())
        item_name.textChanged.connect(lambda: self._mark_modified())
        table.setCellWidget(row, 0, item_name)
        
        # Ticket
        ticket = QLineEdit()
        ticket.setPlaceholderText("Ticket #")
        ticket.setStyleSheet(get_input_style())
        ticket.textChanged.connect(lambda: self._mark_modified())
        table.setCellWidget(row, 1, ticket)
        
        # Sector (Dropdown)
        sector = QComboBox()
        sector.addItems(get_sector_list())
        sector.setStyleSheet(get_combobox_style())
        sector.currentIndexChanged.connect(lambda: self._mark_modified())
        table.setCellWidget(row, 2, sector)
        
        # Supplier (Dropdown)
        supplier = QComboBox()
        supplier.setEditable(True)
        supplier.addItems(get_supplier_list())
        supplier.setStyleSheet(get_combobox_style())
        supplier.currentIndexChanged.connect(lambda: self._mark_modified())
        table.setCellWidget(row, 3, supplier)
        
        # Price
        price = QDoubleSpinBox()
        price.setMaximum(10_000_000)
        price.setPrefix("₹ ")
        price.setDecimals(2)
        price.valueChanged.connect(lambda _: self._calculate_row_total(row))
        price.setStyleSheet(get_spinbox_style())
        table.setCellWidget(row, 4, price)
        
        # Quantity
        qty = QDoubleSpinBox()
        qty.setMinimum(1)
        qty.setMaximum(9999)
        qty.setValue(1)
        qty.valueChanged.connect(lambda _: self._calculate_row_total(row))
        qty.setStyleSheet(get_spinbox_style())
        table.setCellWidget(row, 5, qty)
        
        # Tax
        tax = QDoubleSpinBox()
        tax.setMaximum(100)
        tax.setPrefix("")
        tax.setSuffix(" %")
        tax.setValue(0)
        tax.valueChanged.connect(lambda _: self._calculate_row_total(row))
        tax.setStyleSheet(get_spinbox_style())
        table.setCellWidget(row, 6, tax)
        
        # Amount (read-only label)
        amount_label = QLabel(f"{get_currency_symbol()}0.00")
        amount_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['accent_gold']};
                font-weight: bold;
                padding: 5px;
            }}
        """)
        amount_label.setAlignment(Qt.AlignCenter)
        table.setCellWidget(row, 7, amount_label)
        
        # Delete button
        btn_delete = QPushButton("🗑️")
        btn_delete.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #ff3333;
            }}
        """)
        btn_delete.clicked.connect(lambda: self._delete_row(row))
        btn_delete.setCursor(Qt.PointingHandCursor)
        btn_delete.setMaximumWidth(40)
        table.setCellWidget(row, 8, btn_delete)
        
        self._mark_modified()
    
    def _delete_row(self, row: int):
        """Delete a row from the table."""
        self.table.removeRow(row)
        self._calculate_totals()
        self._mark_modified()
    
    def _calculate_row_total(self, row: int):
        """Calculate total for a specific row and update grand totals."""
        table = self.table
        
        price_widget = table.cellWidget(row, 4)
        qty_widget = table.cellWidget(row, 5)
        tax_widget = table.cellWidget(row, 6)
        amount_label = table.cellWidget(row, 7)
        
        if price_widget and qty_widget and tax_widget and amount_label:
            price = price_widget.value()
            qty = qty_widget.value()
            tax_rate = tax_widget.value() / 100
            
            subtotal = price * qty
            tax_amount = subtotal * tax_rate
            total = subtotal + tax_amount
            
            amount_label.setText(f"{get_currency_symbol()}{total:.2f}")
            
            # Update grand totals
            self._calculate_totals()
            self._mark_modified()
    
    def _calculate_totals(self):
        """Calculate and update subtotal, tax, and grand total."""
        table = self.table
        subtotal = 0.0
        tax_total = 0.0
        
        for row in range(table.rowCount()):
            price_widget = table.cellWidget(row, 4)
            qty_widget = table.cellWidget(row, 5)
            tax_widget = table.cellWidget(row, 6)
            
            if price_widget and qty_widget and tax_widget:
                price = price_widget.value()
                qty = qty_widget.value()
                tax_rate = tax_widget.value() / 100
                
                row_subtotal = price * qty
                row_tax = row_subtotal * tax_rate
                
                subtotal += row_subtotal
                tax_total += row_tax
        
        total = subtotal + tax_total
        
        # Update labels
        symbol = get_currency_symbol()
        self.lbl_subtotal.setText(f"{symbol}{subtotal:.2f}")
        self.lbl_tax.setText(f"{symbol}{tax_total:.2f}")
        self.lbl_total.setText(f"{symbol}{total:.2f}")
        
        # Update balance
        self._calculate_balance()
        
        # Emit signal
        self.calculation_updated.emit(subtotal, tax_total, total)
    
    def _calculate_balance(self):
        """Calculate and update the balance."""
        try:
            received_text = self.txt_received.text().replace(get_currency_symbol(), "").strip()
            received = float(received_text) if received_text else 0.0
            
            total_text = self.lbl_total.text().replace(get_currency_symbol(), "").strip()
            total = float(total_text) if total_text else 0.0
            
            balance = total - received
            
            symbol = get_currency_symbol()
            if balance > 0:
                self.lbl_balance.setText(f"{symbol}{balance:.2f}")
                self.lbl_balance.setStyleSheet(f"""
                    QLabel {{
                        color: {COLORS['danger']};
                        font-weight: bold;
                        font-size: 13px;
                        background-color: {COLORS['primary_bg']};
                        padding: 5px 10px;
                        border-radius: 4px;
                        border: 1px solid {COLORS['danger']};
                    }}
                """)
            elif balance < 0:
                self.lbl_balance.setText(f"{symbol}{abs(balance):.2f} (Change)")
                self.lbl_balance.setStyleSheet(f"""
                    QLabel {{
                        color: {COLORS['success']};
                        font-weight: bold;
                        font-size: 13px;
                        background-color: {COLORS['primary_bg']};
                        padding: 5px 10px;
                        border-radius: 4px;
                        border: 1px solid {COLORS['success']};
                    }}
                """)
            else:
                self.lbl_balance.setText(f"{symbol}0.00")
                self.lbl_balance.setStyleSheet(f"""
                    QLabel {{
                        color: {COLORS['success']};
                        font-weight: bold;
                        font-size: 13px;
                        background-color: {COLORS['primary_bg']};
                        padding: 5px 10px;
                        border-radius: 4px;
                        border: 1px solid {COLORS['success']};
                    }}
                """)
        except ValueError:
            pass
    
    def save_invoice(self):
        """Save invoice to JSON and database."""
        # Validate invoice
        if not self.customer_name.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter customer name!")
            return
        
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Validation Error", "Please add at least one item!")
            return
        
        # Collect invoice data
        invoice_data = {
            "invoice_number": self.invoice_number.text(),
            "date": self.invoice_date.date().toString("yyyy-MM-dd"),
            "customer_name": self.customer_name.text(),
            "contact_number": self.contact_number.text(),
            "items": [],
            "subtotal": self.lbl_subtotal.text(),
            "tax": self.lbl_tax.text(),
            "total": self.lbl_total.text(),
            "received": self.txt_received.text(),
            "balance": self.lbl_balance.text()
        }
        
        # Collect items
        for row in range(self.table.rowCount()):
            item_name_widget = self.table.cellWidget(row, 0)
            ticket_widget = self.table.cellWidget(row, 1)
            sector_widget = self.table.cellWidget(row, 2)
            supplier_widget = self.table.cellWidget(row, 3)
            price_widget = self.table.cellWidget(row, 4)
            qty_widget = self.table.cellWidget(row, 5)
            tax_widget = self.table.cellWidget(row, 6)
            amount_widget = self.table.cellWidget(row, 7)
            
            if item_name_widget and item_name_widget.text().strip():
                invoice_data["items"].append({
                    "item_name": item_name_widget.text(),
                    "ticket": ticket_widget.text() if ticket_widget else "",
                    "sector": sector_widget.currentText() if sector_widget else "",
                    "supplier": supplier_widget.currentText() if supplier_widget else "",
                    "price": price_widget.value() if price_widget else 0,
                    "quantity": qty_widget.value() if qty_widget else 0,
                    "tax": tax_widget.value() if tax_widget else 0,
                    "amount": amount_widget.text() if amount_widget else ""
                })
        
        # Save to JSON
        invoice_dir = "invoices"
        os.makedirs(invoice_dir, exist_ok=True)
        
        filename = f"invoice_{invoice_data['invoice_number']}.json"
        filepath = os.path.join(invoice_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(invoice_data, f, indent=4)
        
        # Save to database if available
        if self.db:
            try:
                self.db.save_invoice(invoice_data)
                QMessageBox.information(self, "Success", f"Invoice {invoice_data['invoice_number']} saved successfully!\n\nSaved to:\n- Database\n- {filepath}")
            except Exception as e:
                QMessageBox.information(self, "Partial Success", f"Invoice saved to JSON but database save failed:\n{str(e)}\n\nFile: {filepath}")
        else:
            QMessageBox.information(self, "Success", f"Invoice {invoice_data['invoice_number']} saved to:\n{filepath}")
        
        self.is_modified = False
        self.invoice_saved.emit(invoice_data['invoice_number'])
        
        # Generate new invoice number for next invoice
        self.invoice_number.setText(self._generate_invoice_number())
    
    def save_pdf(self):
        """Save invoice as PDF."""
        QMessageBox.information(self, "PDF Export", "PDF export feature will be implemented with reportlab library.")
    
    def print_invoice(self):
        """Print invoice."""
        QMessageBox.information(self, "Print", "Print feature will be implemented.")
    
    def clear_form(self):
        """Clear all form fields."""
        self.invoice_number.setText(self._generate_invoice_number())
        self.invoice_date.setDate(QDate.currentDate())
        self.customer_name.clear()
        self.contact_number.clear()
        self.txt_received.clear()
        
        # Clear table
        self.table.setRowCount(0)
        self.add_item_row()
        
        self.is_modified = False
