"""
Sale Report Sub-Page
Displays comprehensive overview of all sales invoices and revenue.
"""
from typing import List, Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QMenu
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

    def _delete_invoice_row(self, row_idx, invoice):
        """
        Delete the invoice row from the table and perform any backend deletion logic.
        """
        # TODO: Add backend/database deletion logic here if needed
        self.sale_table.removeRow(row_idx)
        log_info(f"Deleted invoice {invoice.get('invoice_number', '')}", 'billing_app')

    def _add_context_menu(self):
        """Add right-click context menu to sale table for printing invoices."""
        self.sale_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sale_table.customContextMenuRequested.connect(self._show_context_menu)

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        print_action = menu.addAction("Print Invoice")
        action = menu.exec(self.sale_table.viewport().mapToGlobal(pos))
        if action == print_action:
            selected_row = self.sale_table.currentRow()
            if selected_row >= 0:
                self._print_invoice_for_row(selected_row)

    def _print_invoice_for_row(self, row):
        """Open print preview for the selected invoice (row) with up-to-date paid/balance values."""
        try:
            invoice_number = self.sale_table.item(row, 0).text()
            # Always fetch the latest invoice from the database
            from travel_billing_software.database.db_manager import get_db_instance
            db = get_db_instance()
            invoice = db.get_invoice(invoice_number)
            if not invoice:
                return  # Silently do nothing if not found
            # Optionally, fetch payments and calculate paid/balance if not present
            # (If your db.get_invoice does not already include paid_amount/balance)
            from travel_billing_software.database.db_operations import ReportsDBOperations
            db_ops = ReportsDBOperations()
            all_invoices = db_ops.load_all_invoices()
            for inv in all_invoices:
                if inv.get('invoice_number', '') == invoice_number:
                    invoice['paid_amount'] = inv.get('paid_amount', 0)
                    invoice['balance'] = inv.get('balance', invoice.get('total_amount', 0) - inv.get('paid_amount', 0))
                    break
            ReportExporter.print_invoice(invoice, parent=self)
        except Exception as e:
            log_error("Error printing invoice from report page", exception=e, logger_name='billing_errors')
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
        self.sale_table = QTableWidget(0, 8)
        # Add context menu for reprinting invoices
        self._add_context_menu()
        self.sale_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Contact", "Type", "Total", "Status", "Actions"
        ])
        
        # Configure table
        TableConfigurator.configure_table(self.sale_table, {
            0: 160,  # Invoice # - Increased width to show full invoice numbers
            1: 100,  # Date
            2: 160,  # Customer - Increased width for full names
            3: 120,  # Contact
            4: 80,  # Type
            5: 100,  # Total
            6: 120,  # Status
            7: 130   # Actions (wider for two buttons)
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
            # Store the last invoices for context menu actions
            self._last_invoices = invoices
            
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

                    # Print Button
                    print_btn = QPushButton("🖨️")
                    print_btn.setToolTip("Print Invoice")
                    print_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    print_btn.setStyleSheet(self.get_button_style('primary'))
                    def make_print_handler(inv=invoice):
                        return lambda: ReportExporter.print_invoice(inv, parent=self)
                    print_btn.clicked.connect(make_print_handler())

                    # Delete Button
                    delete_btn = QPushButton("🗑️")
                    delete_btn.setToolTip("Delete Invoice")
                    delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    delete_btn.setStyleSheet(self.get_button_style('danger'))
                    def make_delete_handler(row_idx=row, inv=invoice):
                        def handler():
                            reply = QMessageBox.question(
                                self,
                                "Delete Invoice",
                                f"Are you sure you want to delete invoice {inv.get('invoice_number', '')}?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                            )
                            if reply == QMessageBox.StandardButton.Yes:
                                self._delete_invoice_row(row_idx, inv)
                        return handler
                    delete_btn.clicked.connect(make_delete_handler())

                    # Add both buttons to a horizontal layout in the cell
                    from PyQt6.QtWidgets import QWidget, QHBoxLayout
                    btn_widget = QWidget()
                    btn_layout = QHBoxLayout(btn_widget)
                    btn_layout.setContentsMargins(0, 0, 0, 0)
                    btn_layout.setSpacing(2)
                    btn_layout.addWidget(print_btn)
                    btn_layout.addWidget(delete_btn)
                    btn_widget.setLayout(btn_layout)
                    self.sale_table.setCellWidget(row, 7, btn_widget)
                    def _delete_invoice_row(self, row_idx, invoice):
                        """
                        Delete the invoice row from the table and perform any backend deletion logic.
                        """
                        # TODO: Add backend/database deletion logic here if needed
                        self.sale_table.removeRow(row_idx)
                        log_info(f"Deleted invoice {invoice.get('invoice_number', '')}", 'billing_app')
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
