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
            "📅 Day Book",
            "Daily summary of sales, purchases, and profit",
            self.colors
        )
        layout.addWidget(header)
        
        # Filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # Summary Cards
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Daily Sales', 'Daily Purchases', 'Net Profit'],
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('daybook', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('daybook', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.daybook_table = QTableWidget(0, 5)
        self.daybook_table.setHorizontalHeaderLabels([
            "Date", "Invoices", "Sales", "Purchases", "Profit"
        ])
        
        TableConfigurator.configure_table(self.daybook_table, {
            0: 'stretch',  # Date
            1: 100,  # Invoices
            2: 'stretch',  # Sales
            3: 'stretch',  # Purchases
            4: 'stretch'   # Profit
        })
        self.daybook_table.setMinimumHeight(500)
        layout.addWidget(self.daybook_table)
        
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
        """Populate day book with filtered data - groups by date."""
        try:
            log_info("Populating day book report", 'billing_app')
            
            self.daybook_table.setRowCount(0)
            
            if not invoices:
                log_warning("No records found for day book report", 'billing_app')
                show_no_records_message(self, "Day Book")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    "₹0.00", "₹0.00", "₹0.00"
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
                        'purchases': 0.0
                    }
                
                daily_data[date]['invoices'] += 1
                daily_data[date]['sales'] += invoice.get('total_amount', 0.0)
                
                # Calculate purchases from tickets
                tickets = invoice.get('tickets', [])
                for ticket in tickets:
                    supplier_amount = ticket.get('supplier_amount', 0.0)
                    quantity = ticket.get('quantity', 1)
                    daily_data[date]['purchases'] += supplier_amount * quantity
            
            # Populate table
            total_sales = 0.0
            total_purchases = 0.0
            total_profit = 0.0
            
            for date, data in sorted(daily_data.items(), reverse=True):
                row = self.daybook_table.rowCount()
                self.daybook_table.insertRow(row)
                
                profit = data['sales'] - data['purchases']
                total_sales += data['sales']
                total_purchases += data['purchases']
                total_profit += profit
                
                # Date
                self.daybook_table.setItem(row, 0, QTableWidgetItem(date))
                
                # Invoices
                self.daybook_table.setItem(row, 1, QTableWidgetItem(str(data['invoices'])))
                
                # Sales
                sales_item = QTableWidgetItem(f"₹{data['sales']:,.2f}")
                sales_item.setForeground(QColor("#00FF00"))  # Green for sales
                self.daybook_table.setItem(row, 2, sales_item)
                
                # Purchases
                purchases_item = QTableWidgetItem(f"₹{data['purchases']:,.2f}")
                purchases_item.setForeground(QColor("#FF0000"))  # Red for purchases
                self.daybook_table.setItem(row, 3, purchases_item)
                
                # Profit
                profit_color = "#00FF00" if profit >= 0 else "#FF0000"
                profit_item = QTableWidgetItem(f"₹{profit:,.2f}")
                profit_item.setForeground(QColor(profit_color))
                self.daybook_table.setItem(row, 4, profit_item)
            
            # Update summary
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                f"₹{total_sales:,.2f}",
                f"₹{total_purchases:,.2f}",
                f"₹{total_profit:,.2f}"
            ])
            
            log_info(f"Day book populated: {len(daily_data)} days, Profit: ₹{total_profit:,.2f}", 'billing_app')
            
        except Exception as e:
            log_error("Error populating day book report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate day book report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        return self.daybook_table
