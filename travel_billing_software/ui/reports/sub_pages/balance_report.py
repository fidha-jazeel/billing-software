"""
Balance Report Sub-Page Template
TODO: Group by customer to show outstanding balances

Reference: reports.py lines 2317-2533
Table: 8 columns - Customer, Contact, Total Invoiced, Received, Balance Due,
                   % Paid, Status, Last Invoice Date
Summary: Total Balance Due, Total Received, Total Invoiced
Logic: Use db_operations.calculate_balance_report() for customer grouping
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

class BalanceReportView(QWidget):
    """Balance Report showing customer-wise outstanding balances."""
    
    def __init__(self, colors: dict, get_button_style: callable, export_callback: callable):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("BalanceReportView initialized", 'billing_app')
    
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
            "💰 Balance Report",
            "Customer-wise outstanding balances and payment status",
            self.colors
        )
        layout.addWidget(header)
        
        # Filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # Summary Cards
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Total Balance Due', 'Total Received', 'Total Invoiced'],
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('balance_report', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('balance_report', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.balance_table = QTableWidget(0, 8)
        self.balance_table.setHorizontalHeaderLabels([
            "Customer Name", "Contact", "No. of Invoices", "Total Invoiced",
            "Total Received", "Balance Due", "% Paid", "Status"
        ])
        
        TableConfigurator.configure_table(self.balance_table, {
            0: 'stretch',  # Customer Name
            1: 120,        # Contact
            2: 120,        # No. of Invoices
            3: 130,        # Total Invoiced
            4: 130,        # Total Received
            5: 130,        # Balance Due
            6: 100,        # % Paid
            7: 110         # Status
        })
        self.balance_table.setMinimumHeight(500)
        layout.addWidget(self.balance_table)
        
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
        """Populate balance report with customer-wise grouping."""
        try:
            log_info("Populating balance report", 'billing_app')
            
            self.balance_table.setRowCount(0)
            
            if not invoices:
                log_warning("No records found for balance report", 'billing_app')
                show_no_records_message(self, "Balance Report")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    "₹0.00", "₹0.00", "₹0.00"
                ])
                return
            
            # Group by customer
            customer_balances = {}
            
            for invoice in invoices:
                customer_name = invoice.get('customer_name', 'Unknown')
                customer_phone = invoice.get('customer_phone', '')
                total_amount = invoice.get('total_amount', 0.0)
                paid_amount = invoice.get('paid_amount', 0.0)
                balance = invoice.get('balance', 0.0)
                
                if customer_name not in customer_balances:
                    customer_balances[customer_name] = {
                        'contact': customer_phone,
                        'invoice_count': 0,
                        'total_invoiced': 0.0,
                        'total_received': 0.0,
                        'balance_due': 0.0
                    }
                
                customer_balances[customer_name]['invoice_count'] += 1
                customer_balances[customer_name]['total_invoiced'] += total_amount
                customer_balances[customer_name]['total_received'] += paid_amount
                customer_balances[customer_name]['balance_due'] += balance
            
            # Populate table
            overall_balance = 0.0
            overall_received = 0.0
            overall_invoiced = 0.0
            
            for customer_name, data in customer_balances.items():
                row = self.balance_table.rowCount()
                self.balance_table.insertRow(row)
                
                invoice_count = data['invoice_count']
                total_invoiced = data['total_invoiced']
                total_received = data['total_received']
                balance_due = data['balance_due']
                
                overall_balance += balance_due
                overall_received += total_received
                overall_invoiced += total_invoiced
                
                # Calculate % paid
                percent_paid = (total_received / total_invoiced * 100) if total_invoiced > 0 else 0
                
                # Customer Name
                self.balance_table.setItem(row, 0, QTableWidgetItem(customer_name))
                
                # Contact
                self.balance_table.setItem(row, 1, QTableWidgetItem(data['contact']))
                
                # No. of Invoices
                count_item = QTableWidgetItem(str(invoice_count))
                count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.balance_table.setItem(row, 2, count_item)
                
                # Total Invoiced
                self.balance_table.setItem(row, 3, QTableWidgetItem(f"₹{total_invoiced:,.2f}"))
                
                # Total Received
                received_item = QTableWidgetItem(f"₹{total_received:,.2f}")
                received_item.setForeground(QColor(self.colors['success']))
                self.balance_table.setItem(row, 4, received_item)
                
                # Balance Due
                balance_item = QTableWidgetItem(f"₹{balance_due:,.2f}")
                if balance_due > 0:
                    balance_item.setForeground(QColor(self.colors['danger']))
                else:
                    balance_item.setForeground(QColor(self.colors['success']))
                self.balance_table.setItem(row, 5, balance_item)
                
                # % Paid
                percent_item = QTableWidgetItem(f"{percent_paid:.1f}%")
                percent_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if percent_paid >= 100:
                    percent_item.setForeground(QColor(self.colors['success']))
                elif percent_paid >= 50:
                    percent_item.setForeground(QColor(self.colors.get('warning', '#FFA500')))
                else:
                    percent_item.setForeground(QColor(self.colors['danger']))
                self.balance_table.setItem(row, 6, percent_item)
                
                # Status
                if balance_due <= 0:
                    status = '✅ Cleared'
                    color = self.colors['success']
                elif total_received > 0:
                    status = '🟡 Partial'
                    color = self.colors.get('warning', '#FFA500')
                else:
                    status = '🔴 Pending'
                    color = self.colors['danger']
                
                status_item = QTableWidgetItem(status)
                status_item.setForeground(QColor(color))
                self.balance_table.setItem(row, 7, status_item)
            
            # Update summary
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                f"₹{overall_balance:,.2f}",
                f"₹{overall_received:,.2f}",
                f"₹{overall_invoiced:,.2f}"
            ])
            
            log_info(f"Balance report populated: {len(customer_balances)} customers, Balance: ₹{overall_balance:,.2f}", 'billing_app')
            
        except Exception as e:
            log_error("Error populating balance report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate balance report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        return self.balance_table
