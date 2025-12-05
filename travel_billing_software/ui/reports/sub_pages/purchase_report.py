"""
Purchase Report Sub-Page
Shows supplier purchases and costs breakdown.

TODO: Complete this file following the template pattern from sale_report.py
Line reference: Original reports.py lines 1316-1440
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
    TableConfigurator,
    ReportExporter,
    SummaryCardManager,
    create_report_header,
    show_no_records_message
)


class PurchaseReportView(QWidget):
    """
    Purchase Report showing supplier costs and items purchased.
    
    Table Columns: Passenger, Supplier, Sector, PNR, Qty, Supplier Amount
    Summary Cards: Total Purchases, Total Items, Avg Cost
    """
    
    def __init__(self, colors: dict, get_button_style: callable, export_callback: callable):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("PurchaseReportView initialized", 'billing_app')
    
    def _init_ui(self):
        """Initialize UI - COPY PATTERN FROM sale_report.py"""
        # TODO: Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # TODO: Add header - Change emoji to 📉 and title to "Purchase Report"
        header = create_report_header(
            "📉 Purchase Report",
            "Detailed breakdown of supplier purchases and costs",
            self.colors
        )
        layout.addWidget(header)
        
        # TODO: Add filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # TODO: Create summary cards - Update titles to match Purchase Report
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Total Purchases', 'Total Items', 'Avg Cost'],  # ← UPDATE THESE TITLES
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # TODO: Add export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('purchase', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('purchase', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # TODO: Create table - UPDATE COLUMN COUNT TO 6 and headers
        self.purchase_table = QTableWidget(0, 6)  # ← 6 COLUMNS
        self.purchase_table.setHorizontalHeaderLabels([
            "Passenger", "Supplier", "Sector", "PNR", "Qty", "Supplier Amount"  # ← UPDATE HEADERS
        ])
        
        # TODO: Configure table with appropriate column widths
        TableConfigurator.configure_table(self.purchase_table, {
            0: 'stretch',  # Passenger
            1: 'stretch',  # Supplier
            2: 120,  # Sector
            3: 100,  # PNR
            4: 60,   # Qty
            5: 150   # Supplier Amount
        })
        self.purchase_table.setMinimumHeight(500)
        layout.addWidget(self.purchase_table)
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
    
    def set_filters_widget(self, filters_widget: QWidget):
        """Set filters widget - SAME AS sale_report.py"""
        layout = self.filters_placeholder.parent().layout()
        index = layout.indexOf(self.filters_placeholder)
        layout.removeWidget(self.filters_placeholder)
        self.filters_placeholder.deleteLater()
        layout.insertWidget(index, filters_widget)
    
    def populate(self, invoices: List[Dict[str, Any]]):
        """
        Populate purchase report with invoice data.
        
        TODO: Implement this method by referring to original _populate_purchase_report()
        Line reference: reports.py lines 1395-1440
        
        Logic:
        1. Clear table
        2. Check if no invoices → show message and update summary to zeros
        3. Loop through invoices
           → Loop through invoice['tickets'] (each ticket is a purchase)
        4. For each ticket, extract:
           - passenger_name (from ticket or passengers list)
           - supplier_name
           - sector
           - pnr
           - quantity
           - supplier_amount (cost_price * quantity)
        5. Add row to table with 6 columns
        6. Accumulate totals: total_purchases, total_items
        7. Update summary cards with calculated totals
        """
        try:
            log_info("Populating purchase report", 'billing_app')
            
            self.purchase_table.setRowCount(0)
            
            if not invoices:
                log_warning("No records found for purchase report", 'billing_app')
                show_no_records_message(self, "Purchase Report")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    "₹0.00", "0", "₹0.00"
                ])
                return
            
            # TODO: Initialize counters
            total_purchases = 0.0
            total_items = 0
            
            # TODO: Loop through invoices and tickets
            for invoice in invoices:
                tickets = invoice.get('tickets', [])
                for ticket in tickets:
                    row = self.purchase_table.rowCount()
                    self.purchase_table.insertRow(row)
                    
                    # TODO: Column 0 - Passenger name
                    passenger_name = ticket.get('passenger_name', '')
                    if not passenger_name:
                        # Try to get from passengers list
                        passengers = invoice.get('passengers', [])
                        passenger_name = passengers[0].get('name', '') if passengers else ''
                    self.purchase_table.setItem(row, 0, QTableWidgetItem(passenger_name))
                    
                    # TODO: Column 1 - Supplier
                    self.purchase_table.setItem(row, 1, QTableWidgetItem(ticket.get('supplier_name', '')))
                    
                    # TODO: Column 2 - Sector
                    self.purchase_table.setItem(row, 2, QTableWidgetItem(ticket.get('sector', '')))
                    
                    # TODO: Column 3 - PNR
                    self.purchase_table.setItem(row, 3, QTableWidgetItem(ticket.get('pnr', '')))
                    
                    # TODO: Column 4 - Quantity
                    qty = ticket.get('quantity', 1)
                    self.purchase_table.setItem(row, 4, QTableWidgetItem(str(qty)))
                    total_items += qty
                    
                    # TODO: Column 5 - Supplier Amount (with color)
                    supplier_amount = ticket.get('supplier_amount', 0.0) * qty
                    total_purchases += supplier_amount
                    
                    amount_item = QTableWidgetItem(f"₹{supplier_amount:,.2f}")
                    amount_item.setForeground(QColor(self.colors['accent_gold']))
                    self.purchase_table.setItem(row, 5, amount_item)
            
            # TODO: Update summary cards
            avg_cost = total_purchases / total_items if total_items > 0 else 0.0
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                f"₹{total_purchases:,.2f}",
                str(total_items),
                f"₹{avg_cost:,.2f}"
            ])
            
            log_info(f"Purchase report populated: {total_items} items, Total: ₹{total_purchases:,.2f}", 'billing_app')
            
        except Exception as e:
            log_error("Error populating purchase report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate purchase report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        """Get table for export operations"""
        return self.purchase_table
