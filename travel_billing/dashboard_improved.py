from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QDoubleSpinBox, QStackedWidget, QComboBox, QDateEdit,
    QScrollArea, QGridLayout
)
from PyQt5.QtCore import QDate
import sys
import json
from datetime import datetime


class DashboardImproved(QMainWindow):
    """Improved billing dashboard with new layout as requested:
    1. Invoice Details at top
    2. Excel-style table with columns: Item Name, Ticket, Sector, Supplier, Price, Qty, Tax, Amount, Actions
    3. Sector column is a dropdown (combo box)
    4. Invoice Calculation section below table
    5. Save Invoice, Save PDF, and Add Item buttons at appropriate positions
    6. Unified scrollbar for entire page (no table scrollbar)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency - Billing Software")
        self.resize(1200, 750)
        
        # Apply dark theme globally
        self.apply_dark_theme()

        # Track active page and buttons
        self.current_page = None
        self.sidebar_buttons = {}

        # Main layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar with navigation buttons
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-right: 1px solid #333;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 10, 0, 10)

        # Sidebar title
        title = QLabel("<b style='font-size:16px; color:#9b9bff;'>🏢 Menu</b>")
        title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        # Navigation buttons
        for page_id, label, icon in [
            ('home', '🏠 Home', 'home'),
            ('reports', '📊 Reports', 'reports'),
            ('settings', '⚙ Settings', 'settings'),
            ('about', 'ℹ About', 'about'),
        ]:
            btn = self._create_sidebar_button(label, page_id)
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons[page_id] = btn

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # Content area with stacked widget (multiple pages)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)

        # Create pages
        self.home_page = self._create_home_page()
        self.reports_page = self._create_reports_page()
        self.settings_page = self._create_settings_page()
        self.about_page = self._create_about_page()

        self.content_stack.addWidget(self.home_page)
        self.content_stack.addWidget(self.reports_page)
        self.content_stack.addWidget(self.settings_page)
        self.content_stack.addWidget(self.about_page)

        # Show home page by default
        self.switch_page('home')

    def _create_sidebar_button(self, label: str, page_id: str) -> QPushButton:
        """Create a styled sidebar button."""
        btn = QPushButton(label)
        btn.setMinimumHeight(45)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaa;
                border: none;
                border-left: 3px solid transparent;
                text-align: left;
                padding-left: 15px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                color: #ddd;
            }
            QPushButton#active {
                background-color: #9b9bff;
                color: white;
                border-left: 3px solid #6b6bff;
            }
        """)
        btn.setObjectName("sidebar_btn")
        btn.clicked.connect(lambda: self.switch_page(page_id))
        return btn

    def switch_page(self, page_id: str):
        """Switch to a different page and update button styles."""
        # Update button styles
        for bid, btn in self.sidebar_buttons.items():
            if bid == page_id:
                btn.setObjectName("active")
                btn.style().unpolish(btn)
                btn.style().polish(btn)
            else:
                btn.setObjectName("sidebar_btn")
                btn.style().unpolish(btn)
                btn.style().polish(btn)

        # Switch pages
        if page_id == 'home':
            self.content_stack.setCurrentWidget(self.home_page)
        elif page_id == 'reports':
            self.content_stack.setCurrentWidget(self.reports_page)
        elif page_id == 'settings':
            self.content_stack.setCurrentWidget(self.settings_page)
        elif page_id == 'about':
            self.content_stack.setCurrentWidget(self.about_page)

    def _create_home_page(self) -> QWidget:
        """Create the Home/Dashboard page with new layout:
        1. Invoice Details at top
        2. Add Item button
        3. Excel-style table
        4. Invoice Calculation section
        5. Save Invoice and Save PDF buttons
        """
        # Main container widget
        page = QWidget()
        
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
                background: #5b5bff;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #7a7aff;
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
        
        # === 1. INVOICE DETAILS SECTION (TOP) ===
        invoice_details_frame = QFrame()
        invoice_details_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid #444;
                padding: 15px;
            }
        """)
        invoice_layout = QGridLayout(invoice_details_frame)
        invoice_layout.setContentsMargins(15, 15, 15, 15)
        invoice_layout.setSpacing(10)
        
        # Invoice Details Title
        invoice_title = QLabel("<b style='color:#9b9bff; font-size:14px;'>📄 Invoice Details</b>")
        invoice_layout.addWidget(invoice_title, 0, 0, 1, 4)
        
        # Row 1: Invoice Number and Date
        invoice_layout.addWidget(QLabel("Invoice Number:"), 1, 0)
        self.invoice_number = QLineEdit()
        self.invoice_number.setText(self.generate_invoice_number())
        self.invoice_number.setPlaceholderText("Auto-generated")
        invoice_layout.addWidget(self.invoice_number, 1, 1)
        
        invoice_layout.addWidget(QLabel("Invoice Date:"), 1, 2)
        self.invoice_date = QDateEdit()
        self.invoice_date.setDate(QDate.currentDate())
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDisplayFormat("dd/MM/yyyy")
        invoice_layout.addWidget(self.invoice_date, 1, 3)
        
        # Row 2: Customer Name and Contact
        invoice_layout.addWidget(QLabel("Customer Name:"), 2, 0)
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        invoice_layout.addWidget(self.customer_name, 2, 1)
        
        invoice_layout.addWidget(QLabel("Contact Number:"), 2, 2)
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Enter contact number")
        invoice_layout.addWidget(self.contact_number, 2, 3)
        
        layout.addWidget(invoice_details_frame)
        
        # === 2. ADD ITEM BUTTON (Above Table) ===
        btn_layout_top = QHBoxLayout()
        btn_layout_top.addStretch()
        
        self.btn_add_item = QPushButton("➕ Add Item")
        self.btn_add_item.setStyleSheet("""
            QPushButton {
                background-color: #5b5bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #7a7aff;
            }
            QPushButton:pressed {
                background-color: #4a4aee;
            }
        """)
        self.btn_add_item.clicked.connect(self.add_item_row)
        self.btn_add_item.setCursor(Qt.PointingHandCursor)
        btn_layout_top.addWidget(self.btn_add_item)
        
        layout.addLayout(btn_layout_top)
        
        # === 3. EXCEL-STYLE TABLE ===
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
        
        table_title = QLabel("<b style='color:#9b9bff; font-size:14px;'>🧾 Billed Items</b>")
        table_layout.addWidget(table_title)
        
        # Table with 9 columns: Item Name, Ticket, Sector, Supplier, Price, Qty, Tax, Amount, Actions
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "Item Name", "Ticket", "Sector", "Supplier", "Price (₹)", "Qty", "Tax (%)", "Amount (₹)", "Actions"
        ])
        
        # Disable table's own scrollbars (we use page-level scrolling)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Item Name
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Ticket
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Sector
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Supplier
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Price
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Qty
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Tax
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Amount
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Actions
        
        # Set minimum height for table (adjust based on rows)
        self.table.setMinimumHeight(300)
        
        table_layout.addWidget(self.table)
        layout.addWidget(table_frame)
        
        # === 4. INVOICE CALCULATION SECTION (Below Table) ===
        calc_frame = QFrame()
        calc_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid #444;
                padding: 15px;
            }
        """)
        calc_main_layout = QVBoxLayout(calc_frame)
        calc_main_layout.setContentsMargins(15, 15, 15, 15)
        
        calc_title = QLabel("<b style='color:#9b9bff; font-size:14px;'>💰 Invoice Calculation</b>")
        calc_main_layout.addWidget(calc_title)
        
        calc_layout = QGridLayout()
        calc_layout.setSpacing(10)
        
        # Row 1: Subtotal, Tax, Total
        calc_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        self.lbl_subtotal = QLabel("₹0.00")
        self.lbl_subtotal.setStyleSheet("color: #9b9bff; font-weight: bold; font-size: 13px;")
        calc_layout.addWidget(self.lbl_subtotal, 0, 1)
        
        calc_layout.addWidget(QLabel("Tax:"), 0, 2)
        self.lbl_tax = QLabel("₹0.00")
        self.lbl_tax.setStyleSheet("color: #9b9bff; font-weight: bold; font-size: 13px;")
        calc_layout.addWidget(self.lbl_tax, 0, 3)
        
        calc_layout.addWidget(QLabel("<b>Total:</b>"), 0, 4)
        self.lbl_total = QLabel("₹0.00")
        self.lbl_total.setStyleSheet("""
            color: #FFD700;
            font-weight: bold;
            font-size: 15px;
            background-color: #1a1a1a;
            padding: 5px 10px;
            border-radius: 3px;
            border: 1px solid #9b9bff;
        """)
        calc_layout.addWidget(self.lbl_total, 0, 5)
        
        # Row 2: Received Amount, Balance
        calc_layout.addWidget(QLabel("Received:"), 1, 0)
        self.txt_received = QLineEdit()
        self.txt_received.setPlaceholderText("₹0.00")
        self.txt_received.textChanged.connect(self.calculate_balance)
        calc_layout.addWidget(self.txt_received, 1, 1)
        
        calc_layout.addWidget(QLabel("Balance:"), 1, 2)
        self.lbl_balance = QLabel("₹0.00")
        self.lbl_balance.setStyleSheet("color: #FF6B6B; font-weight: bold; font-size: 13px;")
        calc_layout.addWidget(self.lbl_balance, 1, 3)
        
        calc_main_layout.addLayout(calc_layout)
        layout.addWidget(calc_frame)
        
        # === 5. SAVE BUTTONS (Below Calculation) ===
        btn_layout_bottom = QHBoxLayout()
        btn_layout_bottom.addStretch()
        
        self.btn_save_invoice = QPushButton("💾 Save Invoice")
        self.btn_save_invoice.setStyleSheet("""
            QPushButton {
                background-color: #51CF66;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #69DB7C;
            }
            QPushButton:pressed {
                background-color: #40C057;
            }
        """)
        self.btn_save_invoice.clicked.connect(self.save_invoice)
        self.btn_save_invoice.setCursor(Qt.PointingHandCursor)
        btn_layout_bottom.addWidget(self.btn_save_invoice)
        
        self.btn_save_pdf = QPushButton("📄 Save as PDF")
        self.btn_save_pdf.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #FF8787;
            }
            QPushButton:pressed {
                background-color: #FA5252;
            }
        """)
        self.btn_save_pdf.clicked.connect(self.save_pdf)
        self.btn_save_pdf.setCursor(Qt.PointingHandCursor)
        btn_layout_bottom.addWidget(self.btn_save_pdf)
        
        layout.addLayout(btn_layout_bottom)
        
        # Add some bottom spacing
        layout.addSpacing(20)
        
        # Set the content widget to scroll area
        scroll.setWidget(content)
        
        # Create main page widget with scroll area
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        # Compatibility alias for older code
        self.items_table = self.table
        
        return page

    def generate_invoice_number(self):
        """Generate a unique invoice number based on current date and time."""
        now = datetime.now()
        return f"INV-{now.strftime('%Y%m%d-%H%M%S')}"

    def add_item_row(self):
        """Add a new row to the table with proper widgets for each column."""
        table = self.table
        row = table.rowCount()
        table.insertRow(row)
        
        # Adjust table height dynamically
        self.table.setMinimumHeight(min(300 + (row * 45), 600))

        # Column 0: Item Name (QLineEdit)
        item_name = QLineEdit()
        item_name.setPlaceholderText("Enter item name")
        item_name.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #fff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #9b9bff;
            }
        """)
        table.setCellWidget(row, 0, item_name)

        # Column 1: Ticket (QLineEdit)
        ticket = QLineEdit()
        ticket.setPlaceholderText("Ticket #")
        ticket.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #fff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #9b9bff;
            }
        """)
        table.setCellWidget(row, 1, ticket)

        # Column 2: Sector (QComboBox - Dropdown)
        sector = QComboBox()
        sector.addItems([
            "Select Sector",
            "Domestic",
            "International",
            "Regional",
            "Local",
            "Charter",
            "Corporate"
        ])
        sector.setStyleSheet("""
            QComboBox {
                background-color: #1a1a1a;
                color: #fff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox:focus {
                border: 1px solid #9b9bff;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #5b5bff;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                color: #fff;
                selection-background-color: #5b5bff;
                border: 1px solid #444;
            }
        """)
        table.setCellWidget(row, 2, sector)

        # Column 3: Supplier (QLineEdit)
        supplier = QLineEdit()
        supplier.setPlaceholderText("Supplier name")
        supplier.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #fff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #9b9bff;
            }
        """)
        table.setCellWidget(row, 3, supplier)

        # Column 4: Price (QDoubleSpinBox)
        price = QDoubleSpinBox()
        price.setMaximum(10_000_000)
        price.setPrefix("₹ ")
        price.setDecimals(2)
        price.valueChanged.connect(lambda _: self.calculate_row_total(row))
        price.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #1a1a1a;
                color: #fff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #9b9bff;
            }
            QDoubleSpinBox::up-button {
                background-color: #5b5bff;
                border-radius: 2px;
            }
            QDoubleSpinBox::down-button {
                background-color: #5b5bff;
                border-radius: 2px;
            }
        """)
        table.setCellWidget(row, 4, price)

        # Column 5: Qty (QDoubleSpinBox)
        qty = QDoubleSpinBox()
        qty.setMinimum(1)
        qty.setMaximum(9999)
        qty.setValue(1)
        qty.setDecimals(0)
        qty.valueChanged.connect(lambda _: self.calculate_row_total(row))
        qty.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #1a1a1a;
                color: #fff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #9b9bff;
            }
            QDoubleSpinBox::up-button {
                background-color: #5b5bff;
                border-radius: 2px;
            }
            QDoubleSpinBox::down-button {
                background-color: #5b5bff;
                border-radius: 2px;
            }
        """)
        table.setCellWidget(row, 5, qty)

        # Column 6: Tax % (QDoubleSpinBox)
        tax = QDoubleSpinBox()
        tax.setSuffix('%')
        tax.setMaximum(100)
        tax.setDecimals(2)
        tax.valueChanged.connect(lambda _: self.calculate_row_total(row))
        tax.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #1a1a1a;
                color: #fff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #9b9bff;
            }
            QDoubleSpinBox::up-button {
                background-color: #5b5bff;
                border-radius: 2px;
            }
            QDoubleSpinBox::down-button {
                background-color: #5b5bff;
                border-radius: 2px;
            }
        """)
        table.setCellWidget(row, 6, tax)

        # Column 7: Amount (QLineEdit - Read-only)
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
        table.setCellWidget(row, 7, amount)

        # Column 8: Actions (Delete button)
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Delete this row")
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6B6B;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF8787;
            }
            QPushButton:pressed {
                background-color: #FA5252;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_row(row))
        table.setCellWidget(row, 8, delete_btn)

    def delete_row(self, row: int):
        """Delete a specific row from the table."""
        self.table.removeRow(row)
        # Adjust table height
        self.table.setMinimumHeight(min(300 + (self.table.rowCount() * 45), 600))
        # Recalculate totals after deletion
        self.update_invoice_totals()

    def calculate_row_total(self, row: int):
        """Calculate the amount for a specific row based on Price, Qty, and Tax."""
        table = self.table
        try:
            price_w = table.cellWidget(row, 4)
            qty_w = table.cellWidget(row, 5)
            tax_w = table.cellWidget(row, 6)
            amount_w = table.cellWidget(row, 7)
            
            price = float(price_w.value() if price_w else 0)
            qty = float(qty_w.value() if qty_w else 0)
            tax_pct = float(tax_w.value() if tax_w else 0)
            
            # Calculate: (Price * Qty) + Tax%
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
        """Update the invoice calculation section (Subtotal, Tax, Total)."""
        subtotal = 0.0
        total_tax = 0.0
        table = self.table
        
        for r in range(table.rowCount()):
            try:
                # Get price, qty, and tax from widgets
                price_w = table.cellWidget(r, 4)
                qty_w = table.cellWidget(r, 5)
                tax_w = table.cellWidget(r, 6)
                
                price = float(price_w.value() if price_w else 0)
                qty = float(qty_w.value() if qty_w else 0)
                tax_pct = float(tax_w.value() if tax_w else 0)
                
                # Calculate row subtotal and tax
                row_subtotal = price * qty
                row_tax = row_subtotal * (tax_pct / 100)
                
                subtotal += row_subtotal
                total_tax += row_tax
            except Exception as e:
                print(f"Error calculating totals for row {r}: {e}")
        
        total = subtotal + total_tax
        
        self.lbl_subtotal.setText(f"₹{subtotal:.2f}")
        self.lbl_tax.setText(f"₹{total_tax:.2f}")
        self.lbl_total.setText(f"₹{total:.2f}")
        
        # Recalculate balance when totals change
        self.calculate_balance()

    def calculate_balance(self):
        """Calculate balance as Total - Received Amount."""
        try:
            # Get total amount from label
            total_text = self.lbl_total.text().replace('₹', '').replace(',', '').strip()
            total = float(total_text) if total_text else 0.0

            # Get received amount from input field
            received_text = self.txt_received.text().replace('₹', '').replace(',', '').strip()
            received = float(received_text) if received_text else 0.0

            # Calculate balance
            balance = total - received

            # Update balance label with color coding
            if balance > 0:
                # Red if balance is due
                self.lbl_balance.setStyleSheet("color: #FF6B6B; font-weight: bold; font-size: 13px;")
                self.lbl_balance.setText(f"₹{balance:.2f}")
            elif balance < 0:
                # Green if overpaid
                self.lbl_balance.setStyleSheet("color: #51CF66; font-weight: bold; font-size: 13px;")
                self.lbl_balance.setText(f"₹{abs(balance):.2f} (Overpaid)")
            else:
                # Gray if fully paid
                self.lbl_balance.setStyleSheet("color: #888; font-weight: bold; font-size: 13px;")
                self.lbl_balance.setText("₹0.00 (Paid)")
        except Exception as e:
            print(f"Error calculating balance: {e}")
            self.lbl_balance.setText("₹0.00")

    def save_invoice(self):
        """Save the invoice data to a JSON file."""
        try:
            invoice_data = {
                "invoice_number": self.invoice_number.text(),
                "invoice_date": self.invoice_date.date().toString("dd/MM/yyyy"),
                "customer_name": self.customer_name.text(),
                "contact_number": self.contact_number.text(),
                "items": [],
                "subtotal": self.lbl_subtotal.text(),
                "tax": self.lbl_tax.text(),
                "total": self.lbl_total.text(),
                "received": self.txt_received.text(),
                "balance": self.lbl_balance.text()
            }
            
            # Collect all items from table
            for r in range(self.table.rowCount()):
                item_name_w = self.table.cellWidget(r, 0)
                ticket_w = self.table.cellWidget(r, 1)
                sector_w = self.table.cellWidget(r, 2)
                supplier_w = self.table.cellWidget(r, 3)
                price_w = self.table.cellWidget(r, 4)
                qty_w = self.table.cellWidget(r, 5)
                tax_w = self.table.cellWidget(r, 6)
                amount_w = self.table.cellWidget(r, 7)
                
                item = {
                    "item_name": item_name_w.text() if item_name_w else "",
                    "ticket": ticket_w.text() if ticket_w else "",
                    "sector": sector_w.currentText() if sector_w else "",
                    "supplier": supplier_w.text() if supplier_w else "",
                    "price": price_w.value() if price_w else 0,
                    "qty": qty_w.value() if qty_w else 0,
                    "tax": tax_w.value() if tax_w else 0,
                    "amount": amount_w.text() if amount_w else "₹0.00"
                }
                invoice_data["items"].append(item)
            
            # Save to file
            filename = f"invoices/invoice_{invoice_data['invoice_number']}.json"
            import os
            os.makedirs("invoices", exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(invoice_data, f, indent=4)
            
            print(f"✅ Invoice saved successfully: {filename}")
            
            # Show confirmation (you can add a QMessageBox here)
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Success", f"Invoice saved successfully!\n{filename}")
            
        except Exception as e:
            print(f"❌ Error saving invoice: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to save invoice:\n{str(e)}")

    def save_pdf(self):
        """Save the invoice as a PDF file."""
        try:
            from PyQt5.QtPrintSupport import QPrinter
            from PyQt5.QtGui import QPainter, QFont
            from PyQt5.QtWidgets import QFileDialog
            
            # Ask user for save location
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Invoice as PDF",
                f"invoice_{self.invoice_number.text()}.pdf",
                "PDF Files (*.pdf)"
            )
            
            if not filename:
                return
            
            # Create PDF printer
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filename)
            printer.setPageSize(QPrinter.A4)
            
            # Create painter
            painter = QPainter()
            painter.begin(printer)
            
            # Set fonts
            title_font = QFont("Arial", 18, QFont.Bold)
            header_font = QFont("Arial", 12, QFont.Bold)
            normal_font = QFont("Arial", 10)
            
            y = 100
            
            # Title
            painter.setFont(title_font)
            painter.drawText(100, y, "TRAVEL AGENCY INVOICE")
            y += 80
            
            # Invoice details
            painter.setFont(header_font)
            painter.drawText(100, y, f"Invoice Number: {self.invoice_number.text()}")
            y += 40
            painter.drawText(100, y, f"Date: {self.invoice_date.date().toString('dd/MM/yyyy')}")
            y += 40
            painter.drawText(100, y, f"Customer: {self.customer_name.text()}")
            y += 40
            painter.drawText(100, y, f"Contact: {self.contact_number.text()}")
            y += 80
            
            # Table header
            painter.setFont(header_font)
            painter.drawText(100, y, "Item")
            painter.drawText(1500, y, "Ticket")
            painter.drawText(2000, y, "Sector")
            painter.drawText(2500, y, "Price")
            painter.drawText(2800, y, "Qty")
            painter.drawText(3000, y, "Tax")
            painter.drawText(3300, y, "Amount")
            y += 40
            
            # Draw line
            painter.drawLine(100, y, 3500, y)
            y += 20
            
            # Table items
            painter.setFont(normal_font)
            for r in range(self.table.rowCount()):
                item_name_w = self.table.cellWidget(r, 0)
                ticket_w = self.table.cellWidget(r, 1)
                sector_w = self.table.cellWidget(r, 2)
                price_w = self.table.cellWidget(r, 4)
                qty_w = self.table.cellWidget(r, 5)
                tax_w = self.table.cellWidget(r, 6)
                amount_w = self.table.cellWidget(r, 7)
                
                painter.drawText(100, y, item_name_w.text() if item_name_w else "")
                painter.drawText(1500, y, ticket_w.text() if ticket_w else "")
                painter.drawText(2000, y, sector_w.currentText() if sector_w else "")
                painter.drawText(2500, y, f"₹{price_w.value():.2f}" if price_w else "")
                painter.drawText(2800, y, str(int(qty_w.value())) if qty_w else "")
                painter.drawText(3000, y, f"{tax_w.value():.1f}%" if tax_w else "")
                painter.drawText(3300, y, amount_w.text() if amount_w else "")
                y += 40
            
            y += 40
            painter.drawLine(100, y, 3500, y)
            y += 40
            
            # Totals
            painter.setFont(header_font)
            painter.drawText(2800, y, f"Subtotal: {self.lbl_subtotal.text()}")
            y += 40
            painter.drawText(2800, y, f"Tax: {self.lbl_tax.text()}")
            y += 40
            painter.drawText(2800, y, f"Total: {self.lbl_total.text()}")
            
            painter.end()
            
            print(f"✅ PDF saved successfully: {filename}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Success", f"PDF saved successfully!\n{filename}")
            
        except Exception as e:
            print(f"❌ Error saving PDF: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to save PDF:\n{str(e)}")

    def _create_reports_page(self) -> QWidget:
        """Create the Reports page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)

        heading = QLabel("<h2 style='color:#9b9bff;'>📊 Reports</h2>")
        layout.addWidget(heading)

        info = QLabel(
            "<p>Generate and view billing reports, invoices, and financial summaries.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Daily/Monthly revenue reports</li>"
            "<li>Customer billing history</li>"
            "<li>Tax summary</li>"
            "</ul>"
        )
        info.setStyleSheet("color: #ddd; line-height: 1.6;")
        layout.addWidget(info)

        layout.addStretch()
        return page

    def _create_settings_page(self) -> QWidget:
        """Create the Settings page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)

        heading = QLabel("<h2 style='color:#9b9bff;'>⚙ Settings</h2>")
        layout.addWidget(heading)

        info = QLabel(
            "<p>Configure application preferences and settings.</p>"
            "<p><b>Options:</b></p>"
            "<ul>"
            "<li>Default tax rate</li>"
            "<li>Currency settings</li>"
            "<li>Export preferences</li>"
            "<li>Company details</li>"
            "</ul>"
        )
        info.setStyleSheet("color: #ddd; line-height: 1.6;")
        layout.addWidget(info)

        layout.addStretch()
        return page

    def _create_about_page(self) -> QWidget:
        """Create the About page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)

        heading = QLabel("<h2 style='color:#9b9bff;'>ℹ About</h2>")
        layout.addWidget(heading)

        info = QLabel(
            "<p><b>Travel Agency Billing Software</b></p>"
            "<p>Version 2.0.0 (Improved)</p>"
            "<p>A comprehensive invoicing and billing system designed for travel agencies.</p>"
            "<p style='margin-top: 20px;'><b>Features:</b></p>"
            "<ul>"
            "<li>✓ Invoice generation with auto-numbering</li>"
            "<li>✓ Excel-style table with dropdown sectors</li>"
            "<li>✓ Real-time calculations</li>"
            "<li>✓ Multi-page dashboard</li>"
            "<li>✓ PDF export</li>"
            "<li>✓ JSON data storage</li>"
            "</ul>"
            "<p style='margin-top: 20px; color: #888;'>© 2025 Travel Agency. All rights reserved.</p>"
        )
        info.setStyleSheet("color: #ddd; line-height: 1.8;")
        layout.addWidget(info)

        layout.addStretch()
        return page

    def apply_dark_theme(self):
        """Apply comprehensive dark theme to the entire application."""
        dark_stylesheet = """
            QMainWindow {
                background-color: #0d0d0d;
                color: #ffffff;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            QLineEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #9b9bff;
            }
            QDateEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QDateEdit:focus {
                border: 1px solid #9b9bff;
            }
            QDateEdit::drop-down {
                border: none;
                background-color: #5b5bff;
            }
            QPushButton {
                background-color: #5b5bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a7aff;
            }
            QPushButton:pressed {
                background-color: #4a4aee;
            }
            QTableWidget {
                background-color: #1a1a1a;
                alternate-background-color: #252525;
                gridline-color: #333;
                color: #ffffff;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QTableWidget::item:selected {
                background-color: #9b9bff;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2a2a2a;
                color: #ffffff;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #5b5bff;
                font-weight: bold;
            }
            QFrame {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QDoubleSpinBox {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 3px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #9b9bff;
            }
            QDoubleSpinBox::up-button {
                background-color: #5b5bff;
            }
            QDoubleSpinBox::down-button {
                background-color: #5b5bff;
            }
            QComboBox {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox:focus {
                border: 1px solid #9b9bff;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #5b5bff;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                color: #ffffff;
                selection-background-color: #5b5bff;
                border: 1px solid #444;
            }
            QStackedWidget {
                background-color: #1a1a1a;
            }
        """
        self.setStyleSheet(dark_stylesheet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DashboardImproved()
    w.show()
    sys.exit(app.exec_())
