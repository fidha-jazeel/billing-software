"""
Sale Report Sub-Page
Displays comprehensive overview of all sales invoices and revenue.
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
    TableConfigurator,
    ReportExporter,
    SummaryCardManager,
    create_report_header,
    show_no_records_message
)


class SaleReportView(QWidget):
    """
    Sale Report sub-page showing invoice-level sales data.
    
    Features:
    - Filterable invoice list
    - Total sales and average invoice metrics
    - Payment status tracking
    - Export to CSV/PDF
    """
    
    def __init__(
        self,
        colors: dict,
        get_button_style: callable,
        export_callback: callable,
        is_admin: bool = True
    ):
        """
        Initialize Sale Report view.
        
        Args:
            colors: Color scheme dictionary
            get_button_style: Function to get button stylesheet
            export_callback: Callback for export operations (report_type, format)
            is_admin: Whether current user is admin (controls Net Profit visibility)
        """
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self.refresh_callback = None  # Will be set by parent
        self.is_admin = is_admin  # Store admin status
        
        self._init_ui()
        log_info("SaleReportView initialized", 'billing_app')
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}"
        )
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        header = create_report_header(
            "📈 Sale Report",
            "Comprehensive overview of all sales invoices and revenue",
            self.colors
        )
        layout.addWidget(header)
        
        # Filters placeholder (will be added by parent)
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # Payment summary placeholder (will be added by parent)
        self.payment_summary_placeholder = QWidget()
        self.payment_summary_placeholder.setVisible(False)
        layout.addWidget(self.payment_summary_placeholder)
        
        # Summary Cards - Will show 6 cards (or 5 for non-admin users)
        # Total Sales, Total Invoices, Avg Invoice Value, Total Received, Total Due, Net Profit (admin only)
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Total Sales', 'Total Invoices', 'Avg Invoice Value', 'Total Received', 'Total Due', 'Net Profit'],
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # Store reference to Net Profit card for visibility control
        self.net_profit_card = None
        if hasattr(self.summary_frame, 'layout'):
            layout_obj = self.summary_frame.layout()
            if layout_obj and layout_obj.count() >= 6:
                self.net_profit_card = layout_obj.itemAt(5).widget()
                # Hide Net Profit card if not admin
                if self.net_profit_card and not self.is_admin:
                    self.net_profit_card.setVisible(False)
        
        # Export buttons
        export_row = QHBoxLayout()
        
        # Add Refresh button on the left
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(self.get_button_style('primary'))
        refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        refresh_btn.setToolTip("Reload report data from database")
        refresh_btn.clicked.connect(self._on_refresh_clicked)
        export_row.addWidget(refresh_btn)
        
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('sale', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('sale', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.sale_table = QTableWidget(0, 7)
        self.sale_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Contact", "Type", "Total", "Status"
        ])
        
        # Configure table
        TableConfigurator.configure_table(self.sale_table, {
            0: 180,  # Invoice # - Increased width to show full invoice numbers
            1: 100,  # Date
            2: 'stretch',  # Customer
            3: 120,  # Contact
            4: 100,  # Type
            5: 120,  # Total
            6: 120   # Status
        })
        
        # Enable text wrapping in table cells to prevent truncation
        self.sale_table.setWordWrap(True)
        self.sale_table.setMinimumHeight(500)
        layout.addWidget(self.sale_table)
        
        scroll.setWidget(content)
        
        # Container layout
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
    
    def set_filters_widget(self, filters_widget: QWidget):
        """
        Set the filters widget to display.
        
        Args:
            filters_widget: Filters widget from parent
        """
        # Replace placeholder
        layout = self.filters_placeholder.parent().layout()
        index = layout.indexOf(self.filters_placeholder)
        layout.removeWidget(self.filters_placeholder)
        self.filters_placeholder.deleteLater()
        layout.insertWidget(index, filters_widget)
    
    def set_refresh_callback(self, callback: callable):
        """
        Set the refresh callback function.
        
        Args:
            callback: Function to call when refresh button is clicked
        """
        self.refresh_callback = callback
    
    def _on_refresh_clicked(self):
        """Handle refresh button click."""
        if self.refresh_callback:
            self.refresh_callback()
        else:
            log_warning("Refresh callback not set", 'billing_app')
    
    def set_payment_summary_widget(self, payment_summary_widget: QWidget):
        """
        Set the payment summary widget to display.
        
        Args:
            payment_summary_widget: Payment summary widget from parent
        """
        # Replace placeholder
        layout = self.payment_summary_placeholder.parent().layout()
        index = layout.indexOf(self.payment_summary_placeholder)
        layout.removeWidget(self.payment_summary_placeholder)
        self.payment_summary_placeholder.deleteLater()
        layout.insertWidget(index, payment_summary_widget)
    
    def populate(self, invoices: List[Dict[str, Any]]):
        """
        Populate the report with invoice data.
        
        Args:
            invoices: List of filtered invoice dictionaries
        """
        try:
            log_info("Populating sale report", 'billing_app')
            
            self.sale_table.setRowCount(0)
            
            # Check if no records found
            if not invoices:
                log_warning("No records found for sale report with current filters", 'billing_app')
                show_no_records_message(self, "Sale Report")
                
                # Update summary with zeros (6 cards)
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    format_currency(0),  # Total Sales
                    "0",      # Total Invoices
                    format_currency(0),  # Avg Invoice Value
                    format_currency(0),  # Total Received
                    format_currency(0),  # Total Due
                    format_currency(0)   # Net Profit
                ])
                return
            
            total_sales = 0.0
            total_received = 0.0
            net_profit = 0.0
            
            for invoice in invoices:
                try:
                    row = self.sale_table.rowCount()
                    self.sale_table.insertRow(row)
                    
                    # Calculate payments received for this invoice
                    paid_amount = float(invoice.get('paid_amount', 0))
                    total_received += paid_amount
                    
                    # Calculate net profit from tickets (total_amount - cost_price * quantity)
                    tickets = invoice.get('tickets', [])
                    for ticket in tickets:
                        sale_price = float(ticket.get('total_amount', 0))
                        cost_price = float(ticket.get('supplier_amount', 0))
                        quantity = int(ticket.get('quantity', 1))
                        profit = sale_price - (cost_price * quantity)
                        net_profit += profit
                    
                    # Invoice Number
                    self.sale_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_number', '')))
                    
                    # Date
                    self.sale_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_date', '')))
                    
                    # Customer
                    self.sale_table.setItem(row, 2, QTableWidgetItem(invoice.get('customer_name', '')))
                    
                    # Contact
                    self.sale_table.setItem(row, 3, QTableWidgetItem(invoice.get('customer_phone', '')))
                    
                    # Type - Get from first ticket
                    tickets = invoice.get('tickets', [])
                    booking_type = tickets[0].get('booking_type', '') if tickets else ''
                    self.sale_table.setItem(row, 4, QTableWidgetItem(booking_type))
                    
                    # Total
                    total = float(invoice.get('total_amount', 0))
                    total_sales += total
                    
                    total_item = QTableWidgetItem(format_currency(total))
                    total_item.setForeground(QColor(self.colors['accent_gold']))
                    self.sale_table.setItem(row, 5, total_item)
                    
                    # Status
                    payment_status = invoice.get('payment_status', 'UNPAID')
                    if payment_status == 'PAID':
                        status = '✅ Paid'
                        color = self.colors['success']
                    elif payment_status == 'PARTIAL':
                        status = '⏳ Partial'
                        color = self.colors.get('warning', '#FFA500')
                    else:
                        status = '❌ Unpaid'
                        color = self.colors['danger']
                    
                    status_item = QTableWidgetItem(status)
                    status_item.setForeground(QColor(color))
                    self.sale_table.setItem(row, 6, status_item)
                    
                except Exception as row_error:
                    log_error(
                        f"Error adding row for invoice {invoice.get('invoice_number', 'Unknown')}",
                        exception=row_error,
                        logger_name='billing_errors'
                    )
                    continue
            
            # Update summary with all metrics
            avg_value = total_sales / len(invoices) if invoices else 0.0
            total_due = total_sales - total_received
            
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                format_currency(total_sales),      # Total Sales
                str(len(invoices)),           # Total Invoices
                format_currency(avg_value),        # Avg Invoice Value
                format_currency(total_received),   # Total Received
                format_currency(total_due),        # Total Due
                format_currency(net_profit)        # Net Profit
            ])
            
            log_info(
                f"Sale report populated successfully with {len(invoices)} records, "
                f"Total Sales: {format_currency(0)}{total_sales:,.2f}, Received: {format_currency(0)}{total_received:,.2f}, "
                f"Due: {format_currency(0)}{total_due:,.2f}, Net Profit: {format_currency(0)}{net_profit:,.2f}",
                'billing_app'
            )
            
        except Exception as e:
            log_error("Error populating sale report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate sale report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        """
        Get the table widget for export operations.
        
        Returns:
            The sale report table widget
        """
        return self.sale_table
