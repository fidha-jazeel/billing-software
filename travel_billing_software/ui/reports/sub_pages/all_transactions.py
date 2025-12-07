"""
All Transactions Sub-Page Template
TODO: Follow purchase_report.py pattern - already 90% complete!

Reference: reports.py lines 1442-1590
Table: 8 columns - Invoice #, Date, Customer, Contact, Passenger, Type, Total, Status
Summary: Total Transactions, Total Value, Avg Transaction
Logic: Loop invoices → loop tickets → show each ticket as a transaction
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
from ..utils import (
    TableConfigurator, ReportExporter, SummaryCardManager,
    create_report_header, show_no_records_message
)

class AllTransactionsView(QWidget):
    """All transactions showing every invoice item/ticket."""
    
    def __init__(self, colors: dict, get_button_style: callable, export_callback: callable):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("AllTransactionsView initialized", 'billing_app')
    
    def _init_ui(self):
        """Initialize UI components."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        header = create_report_header(
            "📋 All Transactions",
            "Complete list of all invoice items and transactions",
            self.colors
        )
        layout.addWidget(header)
        
        # Filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # Summary Cards
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Total Transactions', 'Total Value', 'Avg Transaction'],
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('transactions', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('transactions', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.transactions_table = QTableWidget(0, 7)
        self.transactions_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Contact", "Type", "Total", "Status"
        ])
        
        TableConfigurator.configure_table(self.transactions_table, {
            0: 140,  # Invoice #
            1: 100,  # Date
            2: 'stretch',  # Customer
            3: 120,  # Contact
            4: 120,  # Type
            5: 120,  # Total
            6: 110   # Status
        })
        self.transactions_table.setMinimumHeight(500)
        layout.addWidget(self.transactions_table)
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
    
    def set_filters_widget(self, filters_widget: QWidget):
        """Set filters widget."""
        layout = self.filters_placeholder.parent().layout()
        index = layout.indexOf(self.filters_placeholder)
        layout.removeWidget(self.filters_placeholder)
        self.filters_placeholder.deleteLater()
        layout.insertWidget(index, filters_widget)
    
    def populate(self, invoices: List[Dict[str, Any]]):
        """Populate all transactions report with invoice data."""
        try:
            log_info("Populating all transactions report", 'billing_app')
            
            self.transactions_table.setRowCount(0)
            
            if not invoices:
                log_warning("No records found for all transactions report", 'billing_app')
                show_no_records_message(self, "All Transactions")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    "0", format_currency(0), format_currency(0)
                ])
                return
            
            total_value = 0.0
            transaction_count = 0
            
            for invoice in invoices:
                row = self.transactions_table.rowCount()
                self.transactions_table.insertRow(row)
                
                transaction_count += 1
                total_value += invoice.get('total_amount', 0.0)
                
                # Invoice #
                self.transactions_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_number', '')))
                
                # Date
                self.transactions_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_date', '')))
                
                # Customer
                self.transactions_table.setItem(row, 2, QTableWidgetItem(invoice.get('customer_name', '')))
                
                # Contact
                self.transactions_table.setItem(row, 3, QTableWidgetItem(invoice.get('customer_phone', '')))
                
                # Type - Get from first ticket or default
                tickets = invoice.get('tickets', [])
                booking_type = tickets[0].get('booking_type', '') if tickets else 'N/A'
                self.transactions_table.setItem(row, 4, QTableWidgetItem(booking_type))
                
                # Total
                amount = invoice.get('total_amount', 0.0)
                amount_item = QTableWidgetItem(format_currency(amount))
                amount_item.setForeground(QColor("#FFFFFF"))
                self.transactions_table.setItem(row, 5, amount_item)
                
                # Status
                payment_status = invoice.get('payment_status', 'UNPAID')
                if payment_status == 'PAID':
                    status = '✅ Paid'
                    color = "#00FF00"
                elif payment_status == 'PARTIAL':
                    status = '⏳ Partial'
                    color = "#FFA500"
                else:
                    status = '❌ Unpaid'
                    color = "#FF0000"
                
                status_item = QTableWidgetItem(status)
                status_item.setForeground(QColor(color))
                self.transactions_table.setItem(row, 6, status_item)
            
            # Update summary
            avg_transaction = total_value / transaction_count if transaction_count > 0 else 0.0
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                str(transaction_count),
                format_currency(total_value),
                format_currency(avg_transaction)
            ])
            
            log_info(f"All transactions populated: {transaction_count} transactions, Total: {get_currency_symbol()}{total_value:,.2f}", 'billing_app')
            
        except Exception as e:
            log_error("Error populating all transactions report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate all transactions report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        return self.transactions_table
