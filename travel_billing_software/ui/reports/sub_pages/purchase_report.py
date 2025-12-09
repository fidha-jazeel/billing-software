"""
Purchase Report Sub-Page
Shows supplier purchases with profitability analysis.
Displays purchase cost vs selling price with margins for business insights.
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


class PurchaseReportView(QWidget):
    """
    Purchase Report showing supplier purchases with profitability analysis.
    
    Table Columns: Date, Invoice#, Passenger, Supplier, Sector, PNR, Purchase Cost, Selling Price, Profit, Margin%
    Summary Cards: Total Purchase Cost, Total Revenue, Gross Profit, Avg Margin%, Total Tickets, Best Supplier
    """
    
    def __init__(self, colors: dict, get_button_style: callable, export_callback: callable):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("PurchaseReportView initialized", 'billing_app')
    
    def _init_ui(self):
        """Initialize UI with profitability analysis focus."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        header = create_report_header(
            "� Purchase & Profitability Report",
            "Analyze supplier purchases with profit margins and business insights",
            self.colors
        )
        layout.addWidget(header)
        
        # Filters placeholder
        self.filters_placeholder = QWidget()
        self.filters_placeholder.setVisible(False)
        layout.addWidget(self.filters_placeholder)
        
        # Summary cards with profitability metrics
        self.summary_frame = SummaryCardManager.create_summary_cards(
            ['Total Purchase Cost', 'Total Revenue', 'Gross Profit', 'Avg Margin %', 'Total Tickets', 'Best Supplier'],
            self.colors
        )
        layout.addWidget(self.summary_frame)
        
        # Export buttons
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
        
        # Table with expanded columns for profitability
        self.purchase_table = QTableWidget(0, 10)
        self.purchase_table.setHorizontalHeaderLabels([
            "Date", "Invoice#", "Passenger", "Supplier", "Sector", "PNR", 
            "Purchase Cost", "Selling Price", "Profit", "Margin %"
        ])
        
        # Configure table with appropriate column widths
        TableConfigurator.configure_table(self.purchase_table, {
            0: 90,   # Date
            1: 100,  # Invoice#
            2: 150,  # Passenger - increased width
            3: 150,  # Supplier - increased width
            4: 100,  # Sector
            5: 100,  # PNR
            6: 130,  # Purchase Cost
            7: 130,  # Selling Price
            8: 110,  # Profit
            9: 90    # Margin %
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
        Populate the Purchase Report table with invoice data.
        Shows one row per ticket/item with profitability analysis.
        """
        try:
            log_info(f"Populating purchase report with {len(invoices)} invoices", 'billing_app')
            
            # Clear the table
            self.purchase_table.setRowCount(0)
            
            # Check if no records found
            if not invoices:
                log_warning("No records found for purchase report with current filters", 'billing_app')
                show_no_records_message(self, "Purchase Report")
                
                # Update summary with zeros (6 cards)
                SummaryCardManager.update_summary_cards(self.summary_frame, [
                    format_currency(0),  # Total Purchase Cost
                    format_currency(0),  # Total Revenue
                    format_currency(0),  # Gross Profit
                    "0.0%",              # Avg Margin %
                    "0",                 # Total Tickets
                    "-"                  # Best Supplier
                ])
                return
            
            # Calculate summary metrics
            total_cost = 0.0
            total_revenue = 0.0
            total_tickets = 0
            supplier_profits = {}  # Track profit by supplier
            
            log_info(f"Processing {len(invoices)} invoices for purchase report", 'billing_app')

            for invoice in invoices:
                # Get invoice basic info
                invoice_number = str(invoice.get('invoice_number', 'N/A'))
                inv_date = invoice.get('invoice_date') or invoice.get('date') or 'N/A'
                
                # Get tickets for this invoice
                tickets = invoice.get('tickets', [])
                if not tickets:
                    log_warning(f"Invoice {invoice_number} has no tickets - skipping", 'billing_app')
                    continue
                
                log_info(f"Processing invoice {invoice_number} with {len(tickets)} tickets", 'billing_app')

                for ticket in tickets:
                    try:
                        # Insert a new row
                        row = self.purchase_table.rowCount()
                        self.purchase_table.insertRow(row)
                        total_tickets += 1

                        # --- COL 0: DATE ---
                        self.purchase_table.setItem(row, 0, QTableWidgetItem(str(inv_date)))

                        # --- COL 1: INVOICE NUMBER ---
                        self.purchase_table.setItem(row, 1, QTableWidgetItem(invoice_number))

                        # --- COL 2: PASSENGER ---
                        # Try ticket name -> then invoice passenger list -> then empty
                        pass_name = ticket.get('passenger_name') or ticket.get('name') or ''
                        if not pass_name and invoice.get('passengers'):
                            pass_name = invoice['passengers'][0].get('name', '')
                        self.purchase_table.setItem(row, 2, QTableWidgetItem(str(pass_name)))

                        # --- COL 3: SUPPLIER ---
                        sup_name = str(ticket.get('supplier_name', ''))
                        self.purchase_table.setItem(row, 3, QTableWidgetItem(sup_name))

                        # --- COL 4: SECTOR ---
                        sector = str(ticket.get('sector', ''))
                        self.purchase_table.setItem(row, 4, QTableWidgetItem(sector))

                        # --- COL 5: PNR ---
                        pnr = str(ticket.get('pnr') or ticket.get('ticket_number') or '')
                        self.purchase_table.setItem(row, 5, QTableWidgetItem(pnr))

                        # --- FINANCIAL CALCULATIONS ---
                        try:
                            # Helper to safely get float
                            def get_float(val):
                                if not val: return 0.0
                                return float(str(val).replace(',', ''))

                            cost = get_float(ticket.get('supplier_amount'))
                            
                            # Logic: Use unit_price, fallback to total_amount
                            sell = get_float(ticket.get('unit_price'))
                            if sell == 0:
                                sell = get_float(ticket.get('total_amount'))
                                
                            qty = get_float(ticket.get('quantity')) or 1.0
                            
                            ticket_cost = cost * qty
                            ticket_sell = sell * qty
                            profit = ticket_sell - ticket_cost
                            margin = (profit / ticket_sell * 100) if ticket_sell > 0 else 0
                            
                            # Update summary totals
                            total_cost += ticket_cost
                            total_revenue += ticket_sell
                            
                            # Track supplier profits
                            supplier = sup_name if sup_name else "Unknown"
                            if supplier not in supplier_profits:
                                supplier_profits[supplier] = 0.0
                            supplier_profits[supplier] += profit

                            # --- COL 6: COST ---
                            self.purchase_table.setItem(row, 6, QTableWidgetItem(f"{ticket_cost:.2f}"))

                            # --- COL 7: SELL ---
                            self.purchase_table.setItem(row, 7, QTableWidgetItem(f"{ticket_sell:.2f}"))

                            # --- COL 8: PROFIT ---
                            self.purchase_table.setItem(row, 8, QTableWidgetItem(f"{profit:.2f}"))

                            # --- COL 9: MARGIN ---
                            self.purchase_table.setItem(row, 9, QTableWidgetItem(f"{margin:.1f}%"))

                        except Exception as math_err:
                            log_error(f"Financial calculation error on row {row}", exception=math_err, logger_name='billing_errors')
                            self.purchase_table.setItem(row, 6, QTableWidgetItem("0.00"))
                            self.purchase_table.setItem(row, 7, QTableWidgetItem("0.00"))
                            self.purchase_table.setItem(row, 8, QTableWidgetItem("0.00"))
                            self.purchase_table.setItem(row, 9, QTableWidgetItem("0.0%"))

                    except Exception as row_err:
                        log_error(f"Error processing ticket row {row} for invoice {invoice_number}", 
                                exception=row_err, logger_name='billing_errors')
    
            # Calculate summary metrics
            gross_profit = total_revenue - total_cost
            avg_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
            
            # Find best supplier (highest profit)
            best_supplier = "-"
            if supplier_profits:
                best_supplier = max(supplier_profits.items(), key=lambda x: x[1])[0]
            
            # Update summary cards
            SummaryCardManager.update_summary_cards(self.summary_frame, [
                format_currency(total_cost),       # Total Purchase Cost
                format_currency(total_revenue),    # Total Revenue
                format_currency(gross_profit),     # Gross Profit
                f"{avg_margin:.1f}%",             # Avg Margin %
                str(total_tickets),                # Total Tickets
                best_supplier                      # Best Supplier
            ])
            
            log_info(
                f"Purchase report populated: {self.purchase_table.rowCount()} rows, "
                f"Cost: {total_cost:.2f}, Revenue: {total_revenue:.2f}, "
                f"Profit: {gross_profit:.2f}, Tickets: {total_tickets}",
                'billing_app'
            )
            
        except Exception as e:
            log_error("Error populating purchase report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(
                self,
                "Population Error",
                f"Failed to populate purchase report:\n{str(e)}"
            )
    
    def get_table_widget(self) -> QTableWidget:
        """Get table for export operations"""
        return self.purchase_table
