"""
Bill Wise Profit Sub-Page Template
TODO: Most detailed - shows profit per ticket/item

Reference: reports.py lines 1891-2146
Table: 12 columns! - Invoice #, Date, Passenger, Supplier, PNR, Sector, 
                     Booking Type, Qty, Sale Price, Cost Price, Profit, Margin %
Summary: Total Sale, Total Cost, Total Profit
Logic: For each ticket, calculate item-level profit
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

class BillWiseProfitView(QWidget):
    """Bill Wise Profit showing detailed item-level profitability."""
    
    def __init__(self, colors: dict, get_button_style: callable, export_callback: callable):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("BillWiseProfitView initialized", 'billing_app')
    
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
            "💎 Bill Wise Profit",
            "Detailed profit breakdown for each ticket/item",
            self.colors
        )
        layout.addWidget(header)
        
        # Filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # Summary Cards
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Total Sale', 'Total Cost', 'Total Profit'],
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('bill_wise_profit', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('bill_wise_profit', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table with 12 columns
        self.bill_wise_profit_table = QTableWidget(0, 12)
        self.bill_wise_profit_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Passenger", "Supplier", "PNR", "Sector",
            "Booking Type", "Qty", "Sale Price", "Cost Price", "Profit", "Margin %"
        ])
        
        TableConfigurator.configure_table(self.bill_wise_profit_table, {
            0: 120,  # Invoice #
            1: 90,   # Date
            2: 'stretch',  # Passenger
            3: 'stretch',  # Supplier
            4: 100,  # PNR
            5: 100,  # Sector
            6: 110,  # Booking Type
            7: 50,   # Qty
            8: 110,  # Sale Price
            9: 110,  # Cost Price
            10: 110, # Profit
            11: 80   # Margin %
        })
        self.bill_wise_profit_table.setMinimumHeight(500)
        layout.addWidget(self.bill_wise_profit_table)
        
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
        """Populate bill wise profit report with item-level profitability."""
        try:
            log_info("Populating bill wise profit report", 'billing_app')
            
            self.bill_wise_profit_table.setRowCount(0)
            
            if not invoices:
                log_warning("No records found for bill wise profit report", 'billing_app')
                show_no_records_message(self, "Bill Wise Profit")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    "₹0.00", "₹0.00", "₹0.00"
                ])
                return
            
            total_sale = 0.0
            total_cost = 0.0
            total_profit = 0.0
            
            for invoice in invoices:
                tickets = invoice.get('tickets', [])
                passengers = invoice.get('passengers', [])
                
                for ticket in tickets:
                    row = self.bill_wise_profit_table.rowCount()
                    self.bill_wise_profit_table.insertRow(row)
                    
                    # Calculate per-item values
                    quantity = ticket.get('quantity', 1)
                    total_amount = ticket.get('total_amount', 0.0)
                    supplier_amount = ticket.get('supplier_amount', 0.0)
                    
                    sale_price = total_amount / quantity if quantity > 0 else total_amount
                    cost_price = supplier_amount
                    profit = sale_price - cost_price
                    margin = (profit / sale_price * 100) if sale_price > 0 else 0.0
                    
                    total_sale += total_amount
                    total_cost += cost_price * quantity
                    total_profit += profit * quantity
                    
                    # Column 0: Invoice #
                    self.bill_wise_profit_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_number', '')))
                    
                    # Column 1: Date
                    self.bill_wise_profit_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_date', '')))
                    
                    # Column 2: Passenger
                    passenger_name = ''
                    if passengers:
                        passenger_name = passengers[0].get('name', '')
                    self.bill_wise_profit_table.setItem(row, 2, QTableWidgetItem(passenger_name))
                    
                    # Column 3: Supplier
                    self.bill_wise_profit_table.setItem(row, 3, QTableWidgetItem(ticket.get('supplier_name', '')))
                    
                    # Column 4: PNR
                    self.bill_wise_profit_table.setItem(row, 4, QTableWidgetItem(ticket.get('pnr', '')))
                    
                    # Column 5: Sector
                    self.bill_wise_profit_table.setItem(row, 5, QTableWidgetItem(ticket.get('sector', '')))
                    
                    # Column 6: Booking Type
                    self.bill_wise_profit_table.setItem(row, 6, QTableWidgetItem(ticket.get('booking_type', '')))
                    
                    # Column 7: Qty
                    self.bill_wise_profit_table.setItem(row, 7, QTableWidgetItem(str(quantity)))
                    
                    # Column 8: Sale Price
                    sale_item = QTableWidgetItem(f"₹{sale_price:,.2f}")
                    sale_item.setForeground(QColor("#00FF00"))  # Green
                    self.bill_wise_profit_table.setItem(row, 8, sale_item)
                    
                    # Column 9: Cost Price
                    cost_item = QTableWidgetItem(f"₹{cost_price:,.2f}")
                    cost_item.setForeground(QColor("#FF0000"))  # Red
                    self.bill_wise_profit_table.setItem(row, 9, cost_item)
                    
                    # Column 10: Profit
                    profit_item = QTableWidgetItem(f"₹{profit:,.2f}")
                    if profit > 0:
                        profit_item.setForeground(QColor("#00FF00"))  # Green
                    else:
                        profit_item.setForeground(QColor("#FF0000"))  # Red
                    self.bill_wise_profit_table.setItem(row, 10, profit_item)
                    
                    # Column 11: Margin %
                    margin_item = QTableWidgetItem(f"{margin:.2f}%")
                    if margin > 0:
                        margin_item.setForeground(QColor("#FFFFFF"))  # White
                    else:
                        margin_item.setForeground(QColor("#FF0000"))  # Red
                    self.bill_wise_profit_table.setItem(row, 11, margin_item)
            
            # Update summary
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                f"₹{total_sale:,.2f}",
                f"₹{total_cost:,.2f}",
                f"₹{total_profit:,.2f}"
            ])
            
            log_info(f"Bill wise profit populated: {self.bill_wise_profit_table.rowCount()} items, Profit: ₹{total_profit:,.2f}", 'billing_app')
            
        except Exception as e:
            log_error("Error populating bill wise profit report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate bill wise profit report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        return self.bill_wise_profit_table
