"""
Cash Transactions Sub-Page Template
TODO: Filter for cash payments only

Reference: reports.py lines 2148-2315
Table: 8 columns - Date, Invoice #, Customer, Contact, Cash Received, 
                   Cash Paid, Balance, Status
Summary: Total Cash Received, Total Cash Paid, Net Cash Flow
Logic: Show invoices with cash payment mode
"""
from typing import List, Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor
from travel_billing_software.utils.logger import log_info, log_error, log_warning
from ..utils import (
    TableConfigurator, ReportExporter, SummaryCardManager,
    create_report_header, show_no_records_message
)

class CashTransactionsView(QWidget):
    """Cash Transactions showing cash payments and receipts."""
    
    def __init__(self, colors: dict, get_button_style: callable, export_callback: callable):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("CashTransactionsView initialized", 'billing_app')
    
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
            "💵 Cash Transactions Report",
            "Track who paid cash and who received cash payments",
            self.colors
        )
        layout.addWidget(header)
        
        # Filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # Summary Cards
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Total Cash Received', 'Total Cash Paid', 'Net Cash Flow'],
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('cash_transactions', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('cash_transactions', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.cash_transactions_table = QTableWidget(0, 8)
        self.cash_transactions_table.setHorizontalHeaderLabels([
            "Date", "Invoice #", "Customer (Payer)", "Contact", "Cash Received",
            "Cash Paid", "Balance", "Status"
        ])
        
        TableConfigurator.configure_table(self.cash_transactions_table, {
            0: 100,  # Date
            1: 140,  # Invoice #
            2: 'stretch',  # Customer (Payer)
            3: 120,  # Contact
            4: 130,  # Cash Received
            5: 120,  # Cash Paid
            6: 120,  # Balance
            7: 110   # Status
        })
        self.cash_transactions_table.setMinimumHeight(500)
        layout.addWidget(self.cash_transactions_table)
        
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
        """Populate cash transactions report."""
        try:
            log_info("Populating cash transactions report", 'billing_app')
            
            self.cash_transactions_table.setRowCount(0)
            
            if not invoices:
                log_warning("No records found for cash transactions report", 'billing_app')
                show_no_records_message(self, "Cash Transactions")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    "₹0.00", "₹0.00", "₹0.00"
                ])
                return
            
            total_received = 0.0
            total_paid = 0.0
            
            for invoice in invoices:
                row = self.cash_transactions_table.rowCount()
                self.cash_transactions_table.insertRow(row)
                
                # Calculate cash amounts
                paid_amount = invoice.get('paid_amount', 0.0)
                total_amount = invoice.get('total_amount', 0.0)
                balance = invoice.get('balance', 0.0)
                
                cash_received = paid_amount  # Assume all payments are cash for this report
                cash_paid = 0.0  # Typically no cash paid out, but could be supplier payments
                
                total_received += cash_received
                total_paid += cash_paid
                
                # Date
                self.cash_transactions_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_date', '')))
                
                # Invoice #
                self.cash_transactions_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_number', '')))
                
                # Customer (Payer)
                self.cash_transactions_table.setItem(row, 2, QTableWidgetItem(invoice.get('customer_name', '')))
                
                # Contact
                self.cash_transactions_table.setItem(row, 3, QTableWidgetItem(invoice.get('customer_phone', '')))
                
                # Cash Received
                received_item = QTableWidgetItem(f"₹{cash_received:,.2f}")
                received_item.setForeground(QColor(self.colors['success']))
                self.cash_transactions_table.setItem(row, 4, received_item)
                
                # Cash Paid
                paid_item = QTableWidgetItem(f"₹{cash_paid:,.2f}")
                paid_item.setForeground(QColor(self.colors['danger']))
                self.cash_transactions_table.setItem(row, 5, paid_item)
                
                # Balance
                balance_item = QTableWidgetItem(f"₹{balance:,.2f}")
                if balance > 0:
                    balance_item.setForeground(QColor(self.colors['danger']))
                else:
                    balance_item.setForeground(QColor(self.colors['success']))
                self.cash_transactions_table.setItem(row, 6, balance_item)
                
                # Status
                payment_status = invoice.get('payment_status', 'UNPAID')
                if payment_status == 'PAID' or balance <= 0:
                    status = '✅ Paid'
                    color = self.colors['success']
                elif paid_amount > 0 and balance > 0:
                    status = '🟡 Partial'
                    color = self.colors.get('warning', '#FFA500')
                else:
                    status = '🔴 Unpaid'
                    color = self.colors['danger']
                
                status_item = QTableWidgetItem(status)
                status_item.setForeground(QColor(color))
                self.cash_transactions_table.setItem(row, 7, status_item)
            
            # Update summary
            net_cash_flow = total_received - total_paid
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                f"₹{total_received:,.2f}",
                f"₹{total_paid:,.2f}",
                f"₹{net_cash_flow:,.2f}"
            ])
            
            log_info(f"Cash transactions populated: {len(invoices)} transactions, Net: ₹{net_cash_flow:,.2f}", 'billing_app')
            
        except Exception as e:
            log_error("Error populating cash transactions report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate cash transactions report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        return self.cash_transactions_table
