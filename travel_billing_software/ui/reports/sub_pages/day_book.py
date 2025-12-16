"""
Day Book Sub-Page Template
TODO: This one groups by DATE - different pattern!

Reference: reports.py lines 1591-1745
Table: 5 columns - Date, Invoices, Sales, Purchases, Profit
Summary: Daily Sales, Daily Purchases, Net Profit
Logic: Group invoices by date → calculate daily totals
"""
from typing import List, Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor
from travel_billing_software.utils.logger import log_info, log_error, log_warning

from travel_billing_software.config.config import format_currency, get_currency_symbol
from datetime import datetime
from ..utils import (
    TableConfigurator, ReportExporter, SummaryCardManager,
    create_report_header, show_no_records_message
)

class DayBookView(QWidget):
    """Day Book showing daily summaries of sales and purchases."""
    
    def __init__(self, colors: dict, get_button_style: callable, export_callback: callable):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("DayBookView initialized", 'billing_app')
    
    def _init_ui(self):
        """Initialize UI components with page-level vertical scrolling and fixed layout."""
        # Create a scroll area for the entire page
        page_scroll = QScrollArea(self)
        page_scroll.setWidgetResizable(True)
        page_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        page_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        page_scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")

        # Content widget inside scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header
        header = create_report_header(
            "📅 Day Book",
            "Daily summary of sales, purchases, and profit",
            self.colors
        )
        content_layout.addWidget(header)

        # Filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        content_layout.addWidget(self.filters_placeholder)

        # Summary Cards (always visible at top)
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Daily Sales', 'Daily Purchases', 'Expenses', 'Net Profit', 'Balance in Hand'],
            self.colors
        )
        content_layout.addWidget(self.summary_frame)

        # Add vertical spacing between summary cards and export buttons
        from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
        content_layout.addSpacing(24)  # 24px vertical space

        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('daybook', 'pdf'))
        export_row.addWidget(pdf_btn)
        # Add horizontal spacing between buttons
        from PyQt6.QtWidgets import QSpacerItem, QSizePolicy
        export_row.addSpacing(16)  # 16px gap between buttons
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('daybook', 'excel'))
        export_row.addWidget(excel_btn)
        content_layout.addLayout(export_row)
        # Add vertical spacing below export buttons
        content_layout.addSpacing(20)  # 20px gap below buttons

        # Table (no inner scroll area, let page scroll handle overflow)
        self.daybook_table = QTableWidget(0, 9)
        self.daybook_table.setHorizontalHeaderLabels([
            "Date", "Invoices", "Sales", "Purchases", "Cash Received", "Bank Received", "Total Expenses", "Profit", "Balance in Hand"
        ])
        TableConfigurator.configure_table(self.daybook_table, {
            0: 110,        # Date
            1: 80,         # Invoices
            2: 120,        # Sales
            3: 120,        # Purchases
            4: 120,        # Cash Received
            5: 120,        # Bank Received
            6: 130,        # Total Expenses
            7: 120,        # Profit
            8: 140         # Balance in Hand
        })
        self.daybook_table.setMinimumHeight(500)
        content_layout.addWidget(self.daybook_table)

        page_scroll.setWidget(content_widget)

        # Set the main layout to only contain the scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(page_scroll)
    
    def set_filters_widget(self, filters_widget: QWidget):
        """Set filters widget."""
        layout = self.filters_placeholder.parent().layout()
        index = layout.indexOf(self.filters_placeholder)
        layout.removeWidget(self.filters_placeholder)
        self.filters_placeholder.deleteLater()
        layout.insertWidget(index, filters_widget)
    
    def populate(self, invoices: List[Dict[str, Any]]):
        """Populate day book with filtered data - groups by date, includes cash/bank received and expenses."""
        try:
            log_info("Populating day book report (with cash/bank/expenses)", 'billing_app')
            self.daybook_table.setRowCount(0)
            if not invoices:
                log_warning("No records found for day book report", 'billing_app')
                show_no_records_message(self, "Day Book")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    format_currency(0), format_currency(0), format_currency(0), format_currency(0), format_currency(0)
                ])
                return

            # Group by date
            daily_data = {}
            for invoice in invoices:
                date = invoice.get('invoice_date', '')
                if not date:
                    continue
                if date not in daily_data:
                    daily_data[date] = {
                        'invoices': 0,
                        'sales': 0.0,
                        'purchases': 0.0,
                        'cash_received': 0.0,
                        'bank_received': 0.0,
                        'expenses': 0.0  # Will fill below
                    }
                daily_data[date]['invoices'] += 1
                daily_data[date]['sales'] += invoice.get('total_amount', 0.0)
                # Calculate purchases from tickets
                tickets = invoice.get('tickets', [])
                for ticket in tickets:
                    supplier_amount = ticket.get('supplier_amount', 0.0)
                    quantity = ticket.get('quantity', 1)
                    daily_data[date]['purchases'] += supplier_amount * quantity

            # Fetch all payments and group by date/payment_mode
            from travel_billing_software.database.db_manager import get_db_instance
            db = get_db_instance()
            all_payments = db.get_all_payments_received()
            payments_by_date = {}
            for pay in all_payments:
                pay_date = pay.get('date')
                try:
                    # Accept both 'YYYY-MM-DD' and 'DD/MM/YYYY' formats
                    if pay_date and len(pay_date) == 10:
                        if '-' in pay_date:
                            key = datetime.strptime(pay_date, '%Y-%m-%d').strftime('%d/%m/%Y')
                        else:
                            key = pay_date
                        if key not in payments_by_date:
                            payments_by_date[key] = {'CASH': 0.0, 'BANK': 0.0}
                        mode = (pay.get('payment_mode') or '').upper()
                        amt = float(pay.get('amount', 0.0))
                        if mode == 'CASH':
                            payments_by_date[key]['CASH'] += amt
                        elif mode == 'BANK':
                            payments_by_date[key]['BANK'] += amt
                except Exception:
                    continue

            # Fetch all expenses from DB and group by date
            all_expenses = db.get_all_expenses()
            expenses_by_date = {}
            for exp in all_expenses:
                exp_date = exp.get('date')
                try:
                    if exp_date and len(exp_date) == 10:
                        if '-' in exp_date:
                            key = datetime.strptime(exp_date, '%Y-%m-%d').strftime('%d/%m/%Y')
                        else:
                            key = exp_date
                        expenses_by_date.setdefault(key, 0.0)
                        expenses_by_date[key] += float(exp.get('amount', 0.0))
                except Exception:
                    continue
            # Add cash/bank/expenses to daily_data
            for date in daily_data:
                daily_data[date]['cash_received'] = payments_by_date.get(date, {}).get('CASH', 0.0)
                daily_data[date]['bank_received'] = payments_by_date.get(date, {}).get('BANK', 0.0)
                daily_data[date]['expenses'] = expenses_by_date.get(date, 0.0)

            # Populate table and calculate totals
            total_sales = 0.0
            total_purchases = 0.0
            total_expenses = 0.0
            total_profit = 0.0
            total_balance_in_hand = 0.0
            total_cash_received = 0.0
            total_bank_received = 0.0

            for date, data in sorted(daily_data.items(), reverse=True):
                row = self.daybook_table.rowCount()
                self.daybook_table.insertRow(row)
                profit = data['sales'] - data['purchases'] - data['expenses']
                balance_in_hand = data['sales'] - data['expenses']  # Opening balance logic can be added if available
                total_sales += data['sales']
                total_purchases += data['purchases']
                total_expenses += data['expenses']
                total_profit += profit
                total_balance_in_hand += balance_in_hand
                total_cash_received += data['cash_received']
                total_bank_received += data['bank_received']
                # Date
                self.daybook_table.setItem(row, 0, QTableWidgetItem(date))
                # Invoices
                self.daybook_table.setItem(row, 1, QTableWidgetItem(str(data['invoices'])))
                # Sales
                sales_item = QTableWidgetItem(format_currency(data['sales']))
                sales_item.setForeground(QColor("#00FF00"))
                self.daybook_table.setItem(row, 2, sales_item)
                # Purchases
                purchases_item = QTableWidgetItem(format_currency(data['purchases']))
                purchases_item.setForeground(QColor("#FF0000"))
                self.daybook_table.setItem(row, 3, purchases_item)
                # Cash Received
                cash_item = QTableWidgetItem(format_currency(data['cash_received']))
                cash_item.setForeground(QColor("#008000"))  # Dark green for cash
                self.daybook_table.setItem(row, 4, cash_item)
                # Bank Received
                bank_item = QTableWidgetItem(format_currency(data['bank_received']))
                bank_item.setForeground(QColor("#00008B"))  # Dark blue for bank
                self.daybook_table.setItem(row, 5, bank_item)
                # Total Expenses
                expenses_item = QTableWidgetItem(format_currency(data['expenses']))
                expenses_item.setForeground(QColor("#FFA500"))  # Orange for expenses
                self.daybook_table.setItem(row, 6, expenses_item)
                # Profit
                profit_color = "#00FF00" if profit >= 0 else "#FF0000"
                profit_item = QTableWidgetItem(format_currency(profit))
                profit_item.setForeground(QColor(profit_color))
                self.daybook_table.setItem(row, 7, profit_item)
                # Balance in Hand
                balance_item = QTableWidgetItem(format_currency(balance_in_hand))
                balance_item.setForeground(QColor("#1E90FF"))  # Blue for balance
                self.daybook_table.setItem(row, 8, balance_item)

            # Update summary (keep original 5 cards)
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                format_currency(total_sales),
                format_currency(total_purchases),
                format_currency(total_expenses),
                format_currency(total_profit),
                format_currency(total_balance_in_hand)
            ])
            log_info(f"Day book populated: {len(daily_data)} days, Profit: {get_currency_symbol()}{total_profit:,.2f}, Expenses: {get_currency_symbol()}{total_expenses:,.2f}", 'billing_app')
        except Exception as e:
            log_error("Error populating day book report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate day book report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        return self.daybook_table
