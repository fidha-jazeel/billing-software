"""
Profit & Loss Sub-Page Template
TODO: Calculate profit per invoice

Reference: reports.py lines 1747-1889
Table: 7 columns - Invoice #, Date, Customer, Sales, Cost, Profit, Margin %
Summary: Total Sales, Total Cost, Gross Profit
Logic: For each invoice, calculate: profit = sales - sum(supplier_costs)
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

class ProfitLossView(QWidget):
    """Profit & Loss statement showing invoice-level profitability."""
    
    def __init__(self, colors: dict, get_button_style: callable, export_callback: callable):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("ProfitLossView initialized", 'billing_app')
    
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
            "💰 Profit & Loss",
            "Comprehensive profit and loss statement",
            self.colors
        )
        layout.addWidget(header)
        
        # Filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # Summary Cards
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Total Sales', 'Total Cost', 'Gross Profit'],
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        pdf_btn.clicked.connect(lambda: self.export_callback('profit_loss', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        excel_btn.clicked.connect(lambda: self.export_callback('profit_loss', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.profit_loss_table = QTableWidget(0, 7)
        self.profit_loss_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Sales", "Cost", "Profit", "Margin %"
        ])
        
        TableConfigurator.configure_table(self.profit_loss_table, {
            0: 140,  # Invoice #
            1: 100,  # Date
            2: 'stretch',  # Customer
            3: 130,  # Sales
            4: 130,  # Cost
            5: 130,  # Profit
            6: 100   # Margin %
        })
        self.profit_loss_table.setMinimumHeight(500)
        layout.addWidget(self.profit_loss_table)
        
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
        """Populate profit & loss report with invoice-level profitability."""
        try:
            log_info("Populating profit & loss report", 'billing_app')
            
            self.profit_loss_table.setRowCount(0)
            
            if not invoices:
                log_warning("No records found for profit & loss report", 'billing_app')
                show_no_records_message(self, "Profit & Loss")
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    "₹0.00", "₹0.00", "₹0.00"
                ])
                return
            
            total_sales = 0.0
            total_cost = 0.0
            total_profit = 0.0
            
            for invoice in invoices:
                row = self.profit_loss_table.rowCount()
                self.profit_loss_table.insertRow(row)
                
                # Calculate cost from tickets
                cost = 0.0
                tickets = invoice.get('tickets', [])
                for ticket in tickets:
                    supplier_amount = ticket.get('supplier_amount', 0.0)
                    quantity = ticket.get('quantity', 1)
                    cost += supplier_amount * quantity
                
                sales = invoice.get('total_amount', 0.0)
                profit = sales - cost
                margin = (profit / sales * 100) if sales > 0 else 0.0
                
                total_sales += sales
                total_cost += cost
                total_profit += profit
                
                # Invoice #
                self.profit_loss_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_number', '')))
                
                # Date
                self.profit_loss_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_date', '')))
                
                # Customer
                self.profit_loss_table.setItem(row, 2, QTableWidgetItem(invoice.get('customer_name', '')))
                
                # Sales
                sales_item = QTableWidgetItem(f"₹{sales:,.2f}")
                sales_item.setForeground(QColor(self.colors['success']))
                self.profit_loss_table.setItem(row, 3, sales_item)
                
                # Cost
                cost_item = QTableWidgetItem(f"₹{cost:,.2f}")
                cost_item.setForeground(QColor(self.colors['danger']))
                self.profit_loss_table.setItem(row, 4, cost_item)
                
                # Profit
                profit_item = QTableWidgetItem(f"₹{profit:,.2f}")
                if profit > 0:
                    profit_item.setForeground(QColor(self.colors['success']))
                else:
                    profit_item.setForeground(QColor(self.colors['danger']))
                self.profit_loss_table.setItem(row, 5, profit_item)
                
                # Margin %
                margin_item = QTableWidgetItem(f"{margin:.2f}%")
                if margin > 0:
                    margin_item.setForeground(QColor(self.colors['accent_primary']))
                else:
                    margin_item.setForeground(QColor(self.colors['danger']))
                self.profit_loss_table.setItem(row, 6, margin_item)
            
            # Update summary
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                f"₹{total_sales:,.2f}",
                f"₹{total_cost:,.2f}",
                f"₹{total_profit:,.2f}"
            ])
            
            log_info(f"Profit & loss populated: {len(invoices)} invoices, Profit: ₹{total_profit:,.2f}", 'billing_app')
            
        except Exception as e:
            log_error("Error populating profit & loss report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to populate profit & loss report: {str(e)}")
    
    def get_table_widget(self) -> QTableWidget:
        return self.profit_loss_table
