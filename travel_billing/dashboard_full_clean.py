from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QDoubleSpinBox, QStackedWidget
)
import sys


class DashboardFull(QMainWindow):
    """Minimal, stable DashboardFull implementation used by main.py.

    Provides a table with Add Item, per-row amount calculation, and totals.
    Multi-page navigation with sidebar buttons (Home, About, Settings, Reports).
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency - Billing Software")
        self.resize(1100, 700)
        
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
        """Create the Home/Dashboard page."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)

        heading = QLabel("<h2 style='color:#9b9bff;'>Welcome to Travel Agency Billing</h2>")
        layout.addWidget(heading)

        # Invoice header fields
        form = QHBoxLayout()
        self.invoice_number = QLineEdit()
        self.invoice_number.setPlaceholderText("Invoice #")
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Customer name")
        form.addWidget(QLabel("Invoice #:"))
        form.addWidget(self.invoice_number)
        form.addWidget(QLabel("Customer:"))
        form.addWidget(self.customer_name)
        layout.addLayout(form)

        # Table
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Item Name", "Ticket #", "Sector", "Supplier", "Price", "Qty", "Tax (%)", "Amount (₹)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Invoice calculation section at the bottom
        calc_frame = QFrame()
        calc_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 5px;
                border: 1px solid #444;
                padding: 15px;
            }
        """)
        calc_layout = QHBoxLayout(calc_frame)
        calc_layout.setContentsMargins(20, 15, 20, 15)
        calc_layout.setSpacing(25)

        # Subtotal
        subtotal_label = QLabel("Subtotal:")
        subtotal_label.setStyleSheet("color: #ddd; font-weight: 600; min-width: 80px;")
        self.lbl_subtotal = QLabel("₹0.00")
        self.lbl_subtotal.setStyleSheet("color: #9b9bff; font-weight: bold; font-size: 12px;")
        calc_layout.addWidget(subtotal_label)
        calc_layout.addWidget(self.lbl_subtotal)

        # Tax
        tax_label = QLabel("Tax:")
        tax_label.setStyleSheet("color: #ddd; font-weight: 600; min-width: 80px;")
        self.lbl_tax = QLabel("₹0.00")
        self.lbl_tax.setStyleSheet("color: #9b9bff; font-weight: bold; font-size: 12px;")
        calc_layout.addWidget(tax_label)
        calc_layout.addWidget(self.lbl_tax)

        # Total (highlighted)
        total_label = QLabel("Total:")
        total_label.setStyleSheet("color: #fff; font-weight: 700; min-width: 80px;")
        self.lbl_total = QLabel("₹0.00")
        self.lbl_total.setStyleSheet("""
            color: #FFD700;
            font-weight: bold;
            font-size: 14px;
            background-color: #1a1a1a;
            padding: 5px 10px;
            border-radius: 3px;
            border: 1px solid #9b9bff;
        """)
        calc_layout.addWidget(total_label)
        calc_layout.addWidget(self.lbl_total)

        calc_layout.addSpacing(30)

        # Received Amount (input field)
        received_label = QLabel("Received:")
        received_label.setStyleSheet("color: #ddd; font-weight: 600; min-width: 80px;")
        self.txt_received = QLineEdit()
        self.txt_received.setPlaceholderText("₹0.00")
        self.txt_received.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #fff;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
                font-weight: bold;
                min-width: 80px;
            }
            QLineEdit:focus {
                border: 1px solid #9b9bff;
            }
        """)
        self.txt_received.textChanged.connect(self.calculate_balance)
        calc_layout.addWidget(received_label)
        calc_layout.addWidget(self.txt_received)

        # Balance (calculated)
        balance_label = QLabel("Balance:")
        balance_label.setStyleSheet("color: #ddd; font-weight: 600; min-width: 80px;")
        self.lbl_balance = QLabel("₹0.00")
        self.lbl_balance.setStyleSheet("""
            color: #FF6B6B;
            font-weight: bold;
            font-size: 12px;
        """)
        calc_layout.addWidget(balance_label)
        calc_layout.addWidget(self.lbl_balance)

        calc_layout.addStretch()
        layout.addWidget(calc_frame)

        # Add item button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.btn_add_item = QPushButton("+ Add Item")
        self.btn_add_item.setStyleSheet("""
            QPushButton {
                background-color: #5b5bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a7aff;
            }
        """)
        self.btn_add_item.clicked.connect(self.add_item_row)
        button_layout.addWidget(self.btn_add_item)
        layout.addLayout(button_layout)
        layout.addStretch()

        # compatibility alias for older code
        self.items_table = self.table

        return page

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
            "<p>Version 1.0.0</p>"
            "<p>A comprehensive invoicing and billing system designed for travel agencies.</p>"
            "<p style='margin-top: 20px;'><b>Features:</b></p>"
            "<ul>"
            "<li>✓ Invoice generation</li>"
            "<li>✓ Real-time calculations</li>"
            "<li>✓ Multi-page dashboard</li>"
            "<li>✓ Reporting tools</li>"
            "</ul>"
            "<p style='margin-top: 20px; color: #888;'>© 2025 Travel Agency. All rights reserved.</p>"
        )
        info.setStyleSheet("color: #ddd; line-height: 1.8;")
        layout.addWidget(info)

        layout.addStretch()
        return page


    def add_item_row(self):
        table = self.items_table
        row = table.rowCount()
        table.insertRow(row)

        # Item name
        item_name = QLineEdit()
        item_name.setPlaceholderText("Item name")
        table.setCellWidget(row, 0, item_name)

        # Ticket
        ticket = QLineEdit()
        ticket.setPlaceholderText("Ticket #")
        table.setCellWidget(row, 1, ticket)

        # Sector
        sector = QLineEdit()
        table.setCellWidget(row, 2, sector)

        # Supplier
        supplier = QLineEdit()
        table.setCellWidget(row, 3, supplier)

        # Price
        price = QDoubleSpinBox()
        price.setMaximum(1_000_000)
        price.setPrefix("₹ ")
        price.valueChanged.connect(lambda _: self.calculate_row_total(row))
        table.setCellWidget(row, 4, price)

        # Qty
        qty = QDoubleSpinBox()
        qty.setMinimum(1)
        qty.setMaximum(9999)
        qty.setValue(1)
        qty.valueChanged.connect(lambda _: self.calculate_row_total(row))
        table.setCellWidget(row, 5, qty)

        # Tax %
        tax = QDoubleSpinBox()
        tax.setSuffix('%')
        tax.setMaximum(100)
        tax.valueChanged.connect(lambda _: self.calculate_row_total(row))
        table.setCellWidget(row, 6, tax)

        # Amount (read-only)
        amount = QLineEdit("₹ 0.00")
        amount.setReadOnly(True)
        table.setCellWidget(row, 7, amount)

        table.scrollToBottom()

    def calculate_row_total(self, row: int):
        table = self.items_table
        try:
            price_w = table.cellWidget(row, 4)
            qty_w = table.cellWidget(row, 5)
            tax_w = table.cellWidget(row, 6)
            amount_w = table.cellWidget(row, 7)
            price = float(price_w.value() if price_w else 0)
            qty = float(qty_w.value() if qty_w else 0)
            tax_pct = float(tax_w.value() if tax_w else 0)
            total = price * qty * (1 + tax_pct / 100)
            if amount_w:
                amount_w.setText(f"₹ {total:.2f}")
        except Exception:
            pass
        finally:
            self.update_invoice_totals()

    def update_invoice_totals(self):
        subtotal = 0.0
        table = self.items_table
        for r in range(table.rowCount()):
            amt_w = table.cellWidget(r, 7)
            if amt_w:
                txt = amt_w.text().replace('₹', '').replace(',', '').strip()
                try:
                    subtotal += float(txt or 0)
                except Exception:
                    pass
        tax = subtotal * 0.05
        total = subtotal + tax
        self.lbl_subtotal.setText(f"Subtotal: ₹{subtotal:.2f}")
        self.lbl_tax.setText(f"Tax: ₹{tax:.2f}")
        self.lbl_total.setText(f"Total: ₹{total:.2f}")
        # Recalculate balance when totals change
        self.calculate_balance()

    def calculate_balance(self):
        """Calculate balance as Total - Received Amount."""
        try:
            # Get total amount from label
            total_text = self.lbl_total.text().replace('Total:', '').replace('₹', '').strip()
            total = float(total_text) if total_text else 0.0

            # Get received amount from input field
            received_text = self.txt_received.text().replace('₹', '').replace(',', '').strip()
            received = float(received_text) if received_text else 0.0

            # Calculate balance
            balance = total - received

            # Update balance label with color coding
            if balance > 0:
                # Red if balance is due
                self.lbl_balance.setStyleSheet("color: #FF6B6B; font-weight: bold; font-size: 12px;")
                self.lbl_balance.setText(f"₹{balance:.2f}")
            elif balance < 0:
                # Green if overpaid
                self.lbl_balance.setStyleSheet("color: #51CF66; font-weight: bold; font-size: 12px;")
                self.lbl_balance.setText(f"₹{abs(balance):.2f}")
            else:
                # Gray if fully paid
                self.lbl_balance.setStyleSheet("color: #888; font-weight: bold; font-size: 12px;")
                self.lbl_balance.setText("₹0.00")
        except Exception:
            self.lbl_balance.setText("₹0.00")

    def load_invoice_page(self):
        try:
            from travel_billing.main_manual import InvoicePage
        except Exception as e:
            print("Could not import InvoicePage:", e)
            return
        win = InvoicePage()
        win.show()

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
                padding: 5px;
                border: none;
                border-bottom: 1px solid #444;
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
            QStackedWidget {
                background-color: #1a1a1a;
            }
        """
        self.setStyleSheet(dark_stylesheet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DashboardFull()
    w.show()
    sys.exit(app.exec_())
