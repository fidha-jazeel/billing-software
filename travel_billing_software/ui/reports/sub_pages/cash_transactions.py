"""
Cash Transactions Sub-Page Template
TODO: Filter for cash payments only

Reference: reports.py lines 2148-2315
Table: 8 columns - Date, Invoice #, Customer, Contact, Cash Received, 
                   Cash Paid, Balance, Status
Summary: Total Cash Received, Total Cash Paid, Net Cash Flow
Logic: Show invoices with cash payment mode
"""
from datetime import datetime
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
    
    def populate(self, invoices: List[Dict[str, Any]] = None, cash_received: List[Dict[str, Any]] = None, cash_paid: List[Dict[str, Any]] = None):
        """
        Populate cash transactions report.
        
        Args:
            invoices: Not used - kept for compatibility
            cash_received: List of cash payment records received from customers
            cash_paid: List of cash payment records paid to suppliers
        """
        try:
            log_info("Populating cash transactions report", 'billing_app')
            
            self.cash_transactions_table.setRowCount(0)
            
            # Combine both received and paid transactions
            all_transactions = []
            
            if cash_received:
                for payment in cash_received:
                    all_transactions.append({
                        'date': payment.get('date', ''),
                        'reference': payment.get('invoice_number', ''),
                        'party': payment.get('customer_name', ''),
                        'contact': payment.get('customer_phone', ''),
                        'received': payment.get('amount', 0.0),
                        'paid': 0.0,
                        'balance': payment.get('total_amount', 0.0) - payment.get('amount', 0.0),
                        'type': 'RECEIVED'
                    })
            
            if cash_paid:
                for payment in cash_paid:
                    all_transactions.append({
                        'date': payment.get('date', ''),
                        'reference': payment.get('reference_number', '-'),
                        'party': payment.get('supplier_name', ''),
                        'contact': payment.get('supplier_phone', ''),
                        'received': 0.0,
                        'paid': payment.get('amount', 0.0),
                        'balance': -payment.get('amount', 0.0),  # Negative for paid out
                        'type': 'PAID'
                    })
            
            if not all_transactions:
                log_warning("No cash transactions found", 'billing_app')
                show_no_records_message(self, "Cash Transactions")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    "₹0.00", "₹0.00", "₹0.00"
                ])
                return
            
            # Sort by date (most recent first)
            try:
                all_transactions.sort(key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'), reverse=True)
            except:
                pass  # If date parsing fails, keep original order
            
            total_received = 0.0
            total_paid = 0.0
            
            for transaction in all_transactions:
                row = self.cash_transactions_table.rowCount()
                self.cash_transactions_table.insertRow(row)
                
                cash_received_amt = transaction['received']
                cash_paid_amt = transaction['paid']
                balance = transaction['balance']
                
                total_received += cash_received_amt
                total_paid += cash_paid_amt
                
                # Date
                self.cash_transactions_table.setItem(row, 0, QTableWidgetItem(transaction['date']))
                
                # Reference (Invoice # or Payment Reference)
                self.cash_transactions_table.setItem(row, 1, QTableWidgetItem(transaction['reference']))
                
                # Party (Customer or Supplier)
                party_text = transaction['party']
                if transaction['type'] == 'PAID':
                    party_text = f"🔴 {party_text}"  # Mark supplier payments
                else:
                    party_text = f"🟢 {party_text}"  # Mark customer receipts
                self.cash_transactions_table.setItem(row, 2, QTableWidgetItem(party_text))
                
                # Contact
                self.cash_transactions_table.setItem(row, 3, QTableWidgetItem(transaction['contact']))
                
                # Cash Received
                received_item = QTableWidgetItem(f"₹{cash_received_amt:,.2f}")
                if cash_received_amt > 0:
                    received_item.setForeground(QColor("#00FF00"))  # Green
                self.cash_transactions_table.setItem(row, 4, received_item)
                
                # Cash Paid
                paid_item = QTableWidgetItem(f"₹{cash_paid_amt:,.2f}")
                if cash_paid_amt > 0:
                    paid_item.setForeground(QColor("#FF0000"))  # Red
                self.cash_transactions_table.setItem(row, 5, paid_item)
                
                # Balance
                balance_item = QTableWidgetItem(f"₹{abs(balance):,.2f}")
                if balance > 0:
                    balance_item.setForeground(QColor("#FF0000"))  # Red (still owed)
                elif balance < 0:
                    balance_item.setForeground(QColor("#FFA500"))  # Orange (paid out)
                else:
                    balance_item.setForeground(QColor("#00FF00"))  # Green (settled)
                self.cash_transactions_table.setItem(row, 6, balance_item)
                
                # Status
                if transaction['type'] == 'PAID':
                    status = '🔴 Paid Out'
                    color = "#FF0000"
                elif balance <= 0:
                    status = '✅ Received'
                    color = "#00FF00"
                elif cash_received_amt > 0 and balance > 0:
                    status = '🟡 Partial'
                    color = "#FFA500"
                else:
                    status = '🔴 Pending'
                    color = "#FF0000"
                
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
            
            log_info(
                f"Cash transactions populated: {len(all_transactions)} transactions, "
                f"Received: ₹{total_received:,.2f}, Paid: ₹{total_paid:,.2f}, Net: ₹{net_cash_flow:,.2f}",
                'billing_app'
            )
            
        except Exception as e:
            log_error("Error populating cash transactions report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate cash transactions report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        return self.cash_transactions_table
