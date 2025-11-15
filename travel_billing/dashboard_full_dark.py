from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QDoubleSpinBox, QStackedWidget, QDateEdit, QGridLayout,
    QFileDialog, QMessageBox, QStyle
)
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter
import sys
import os
import json
from datetime import datetime
from PyQt5.QtCore import QSize


class DashboardFull(QMainWindow):
    """Minimal, stable DashboardFull implementation used by main.py.

    
    Provides a table with Add Item, per-row amount calculation, and totals.
    Multi-page navigation with sidebar buttons (Home, About, Settings, Reports).
    Dark theme applied globally.
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

        # Invoice header fields (two-row grid: invoice+date | customer+contact)
        form = QGridLayout()
        self.invoice_number = QLineEdit()
        self.invoice_number.setReadOnly(True)
        self.invoice_number.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                color: #9b9bff;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        # Auto-generate invoice number with timestamp
        self.invoice_number.setText(datetime.now().strftime("INV-%Y%m%d-%H%M%S"))
        
        self.invoice_date = QDateEdit()
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDate(QDate.currentDate())

        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Customer name")
        self.customer_contact = QLineEdit()
        self.customer_contact.setPlaceholderText("Contact number")

        form.addWidget(QLabel("Invoice number:"), 0, 0)
        form.addWidget(self.invoice_number, 0, 1)
        form.addWidget(QLabel("Invoice Date:"), 1, 0)
        form.addWidget(self.invoice_date, 1, 1)

        form.addWidget(QLabel("Customer Name:"), 0, 2)
        form.addWidget(self.customer_name, 0, 3)
        form.addWidget(QLabel("Contact Number:"), 1, 2)
        form.addWidget(self.customer_contact, 1, 3)

        layout.addLayout(form)

        # Table with Actions column at the end
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "Item Name", "Ticket #", "Sector", "Supplier", "Price", "Qty", "Tax (%)", "Amount (₹)", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Invoice calculation section (vertical, with heading)
        calc_frame = QFrame()
        calc_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 5px;
                border: 1px solid #444;
                padding: 12px;
            }
        """)

        calc_layout = QVBoxLayout(calc_frame)
        calc_layout.setContentsMargins(16, 12, 16, 12)
        calc_layout.setSpacing(8)

        # Heading
        calc_heading = QLabel("Invoice Calculation")
        calc_heading.setStyleSheet("color: #ffffff; font-weight: 700; font-size: 14px; margin-bottom: 6px;")
        calc_layout.addWidget(calc_heading)

        def add_calc_row(label_text, widget):
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet("color: #ddd; font-weight: 600;")
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(widget)
            calc_layout.addLayout(row)

        # Subtotal
        self.lbl_subtotal = QLabel("₹0.00")
        self.lbl_subtotal.setStyleSheet("color: #9b9bff; font-weight: bold; font-size: 12px;")
        add_calc_row("Subtotal:", self.lbl_subtotal)

        # Tax
        self.lbl_tax = QLabel("₹0.00")
        self.lbl_tax.setStyleSheet("color: #9b9bff; font-weight: bold; font-size: 12px;")
        add_calc_row("Tax:", self.lbl_tax)

        # Total (highlighted)
        self.lbl_total = QLabel("₹0.00")
        self.lbl_total.setStyleSheet("""
            color: #FFD700;
            font-weight: bold;
            font-size: 14px;
            background-color: #1a1a1a;
            padding: 4px 8px;
            border-radius: 3px;
            border: 1px solid #9b9bff;
        """)
        add_calc_row("Total:", self.lbl_total)

        # Received Amount (input field)
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
                min-width: 120px;
            }
            QLineEdit:focus {
                border: 1px solid #9b9bff;
            }
        """)
        self.txt_received.textChanged.connect(self.calculate_balance)
        add_calc_row("Received:", self.txt_received)

        # Balance (calculated)
        self.lbl_balance = QLabel("₹0.00")
        self.lbl_balance.setStyleSheet("""
            color: #FF6B6B;
            font-weight: bold;
            font-size: 12px;
        """)
        add_calc_row("Balance:", self.lbl_balance)

        layout.addWidget(calc_frame)

        # Add item button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        # Save invoice button
        self.btn_save_invoice = QPushButton("💾 Save Invoice")
        self.btn_save_invoice.setStyleSheet("""
            QPushButton { background-color: #2e8b57; color: white; border: none; border-radius: 5px; padding: 8px 12px; font-weight: bold; }
            QPushButton:hover { background-color: #3fb16b; }
        """)
        self.btn_save_invoice.clicked.connect(self.save_invoice)
        button_layout.addWidget(self.btn_save_invoice)

        # Save PDF button
        self.btn_save_pdf = QPushButton("🖨️ Save PDF")
        self.btn_save_pdf.setStyleSheet("""
            QPushButton { background-color: #17a2b8; color: white; border: none; border-radius: 5px; padding: 8px 12px; font-weight: bold; }
            QPushButton:hover { background-color: #2bb5c7; }
        """)
        self.btn_save_pdf.clicked.connect(self.save_pdf)
        button_layout.addWidget(self.btn_save_pdf)

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

        # Delete button (last column) — icon only
        delete_btn = QPushButton()
        # use platform standard trash icon
        trash_icon = self.style().standardIcon(QStyle.SP_TrashIcon)
        delete_btn.setIcon(trash_icon)
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setToolTip("Delete row")
        delete_btn.setFixedSize(34, 28)
        delete_btn.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; }
            QPushButton:hover { background-color: rgba(255,0,0,0.06); border-radius: 4px; }
        """)
        delete_btn.clicked.connect(self.delete_row_by_button)
        table.setCellWidget(row, 8, delete_btn)

        table.scrollToBottom()

    def refresh_serial_numbers(self):
        """Deprecated: S/No column removed."""
        pass

    def calculate_row_total(self, row: int):
        table = self.items_table
        try:
            price_w = table.cellWidget(row, 5)
            qty_w = table.cellWidget(row, 6)
            tax_w = table.cellWidget(row, 7)
            amount_w = table.cellWidget(row, 8)
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

    def delete_row_by_button(self):
        """Find the row containing the clicked delete button and remove it."""
        btn = self.sender()
        if not btn:
            return
        table = self.table
        # delete column index is 8
        for r in range(table.rowCount()):
            w = table.cellWidget(r, 8)
            if w is btn:
                table.removeRow(r)
                # update totals after deletion
                self.update_invoice_totals()
                return

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

    def collect_invoice_data(self) -> dict:
        """Collect invoice data from the UI and table into a serializable dict."""
        # Ensure totals are up-to-date
        self.update_invoice_totals()

        invoice_no = self.invoice_number.text().strip()
        if not invoice_no:
            # fallback to timestamp-based invoice number
            invoice_no = datetime.now().strftime("INV-%Y%m%d-%H%M%S")

        items = []
        table = self.items_table
        for r in range(table.rowCount()):
            try:
                item_name_w = table.cellWidget(r, 0)
                ticket_w = table.cellWidget(r, 1)
                sector_w = table.cellWidget(r, 2)
                supplier_w = table.cellWidget(r, 3)
                price_w = table.cellWidget(r, 4)
                qty_w = table.cellWidget(r, 5)
                tax_w = table.cellWidget(r, 6)
                amount_w = table.cellWidget(r, 7)

                price = float(price_w.value()) if price_w else 0.0
                qty = float(qty_w.value()) if qty_w else 0.0
                tax_pct = float(tax_w.value()) if tax_w else 0.0
                amount_txt = amount_w.text() if amount_w else "0"
                amount = float(amount_txt.replace('₹', '').replace(',', '').strip() or 0)

                items.append({
                    'item_name': item_name_w.text() if item_name_w else '',
                    'ticket': ticket_w.text() if ticket_w else '',
                    'sector': sector_w.text() if sector_w else '',
                    'supplier': supplier_w.text() if supplier_w else '',
                    'price': price,
                    'qty': qty,
                    'tax_pct': tax_pct,
                    'amount': amount,
                })
            except Exception:
                continue

        # totals
        subtotal_txt = self.lbl_subtotal.text().replace('Subtotal:', '').replace('₹', '').strip()
        tax_txt = self.lbl_tax.text().replace('Tax:', '').replace('₹', '').strip()
        total_txt = self.lbl_total.text().replace('Total:', '').replace('₹', '').strip()
        try:
            subtotal = float(subtotal_txt or 0)
        except Exception:
            subtotal = 0.0
        try:
            tax = float(tax_txt or 0)
        except Exception:
            tax = 0.0
        try:
            total = float(total_txt or 0)
        except Exception:
            total = 0.0

        received_txt = self.txt_received.text().replace('₹', '').replace(',', '').strip()
        try:
            received = float(received_txt or 0)
        except Exception:
            received = 0.0

        balance_txt = self.lbl_balance.text().replace('₹', '').replace(',', '').strip()
        try:
            balance = float(balance_txt or 0)
        except Exception:
            balance = total - received

        data = {
            'invoice_number': invoice_no,
            'invoice_date': self.invoice_date.date().toString('yyyy-MM-dd'),
            'customer_name': self.customer_name.text().strip(),
            'customer_contact': self.customer_contact.text().strip(),
            'items': items,
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
            'received': received,
            'balance': balance,
            'created_at': datetime.now().isoformat(),
        }
        return data

    def invoice_to_html(self, data: dict) -> str:
        """Render a simple HTML invoice from data for PDF output."""
        header = f"<h2>Invoice: {data['invoice_number']}</h2>"
        meta = (
            f"<p><b>Date:</b> {data['invoice_date']} &nbsp;&nbsp;"
            f"<b>Customer:</b> {data['customer_name']} &nbsp;&nbsp;"
            f"<b>Contact:</b> {data['customer_contact']}</p>"
        )

        rows_html = ''
        for it in data['items']:
            rows_html += (
                f"<tr>"
                f"<td>{it.get('item_name','')}</td>"
                f"<td>{it.get('ticket','')}</td>"
                f"<td>{it.get('sector','')}</td>"
                f"<td>{it.get('supplier','')}</td>"
                f"<td style='text-align:right;'>₹{it.get('price',0):.2f}</td>"
                f"<td style='text-align:right;'>{it.get('qty',0)}</td>"
                f"<td style='text-align:right;'>{it.get('tax_pct',0):.2f}%</td>"
                f"<td style='text-align:right;'>₹{it.get('amount',0):.2f}</td>"
                f"</tr>"
            )

        html = f"""
        <html>
        <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #222; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f4f4f4; text-align: left; }}
            .right {{ text-align: right; }}
        </style>
        </head>
        <body>
        <h1>Travel Agency</h1>
        {header}
        {meta}
        <table>
            <thead>
                <tr>
                    <th>Item</th><th>Ticket</th><th>Sector</th><th>Supplier</th>
                    <th>Price</th><th>Qty</th><th>Tax</th><th>Amount</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        <p style='text-align:right; font-weight:600;'>Subtotal: ₹{data['subtotal']:.2f}</p>
        <p style='text-align:right; font-weight:600;'>Tax: ₹{data['tax']:.2f}</p>
        <p style='text-align:right; font-size:16px; font-weight:700;'>Total: ₹{data['total']:.2f}</p>
        <p style='text-align:right;'>Received: ₹{data['received']:.2f}</p>
        <p style='text-align:right;'>Balance: ₹{data['balance']:.2f}</p>
        </body>
        </html>
        """
        return html

    def save_invoice(self):
        """Save invoice data as a JSON file in an invoices/ directory."""
        data = self.collect_invoice_data()

        # invoices directory at project root (parent of travel_billing)
        project_root = os.path.dirname(os.path.dirname(__file__))
        invoices_dir = os.path.join(project_root, 'invoices')
        os.makedirs(invoices_dir, exist_ok=True)

        # safe filename
        safe_no = ''.join(c for c in data['invoice_number'] if c.isalnum() or c in ('-','_')).strip()
        if not safe_no:
            safe_no = datetime.now().strftime("INV-%Y%m%d-%H%M%S")
        filename = f"invoice_{safe_no}.json"
        path = os.path.join(invoices_dir, filename)

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, 'Saved', f'Invoice saved to:\n{path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Could not save invoice:\n{e}')

    def save_pdf(self):
        """Export the current invoice to a PDF file using Qt's printer support."""
        data = self.collect_invoice_data()
        html = self.invoice_to_html(data)

        # Ask user where to save
        default_name = f"{data['invoice_number']}.pdf"
        path, _ = QFileDialog.getSaveFileName(self, 'Save Invoice as PDF', default_name, 'PDF Files (*.pdf)')
        if not path:
            return

        try:
            doc = QTextDocument()
            doc.setHtml(html)
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(path)
            doc.print_(printer)
            QMessageBox.information(self, 'Saved', f'PDF saved to:\n{path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Could not save PDF:\n{e}')

    def load_invoice_page(self):
        try:
            from travel_billing.main_manual import InvoicePage
        except Exception as e:
            print("Could not import InvoicePage:", e)
            return
        win = InvoicePage()
        win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DashboardFull()
    w.show()
    sys.exit(app.exec_())
