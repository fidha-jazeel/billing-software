"""
Reports Page - Main Orchestrator
Vyapar-style reports with sidebar navigation and dynamic content panels.

TODO: Complete this orchestrator following the guide in REFACTORING_GUIDE_REPORTS.md
Reference: Original reports.py lines 19-2533 (entire ReportsPage class)
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QStackedWidget, QListWidget, QListWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from travel_billing_software.utils.logger import log_info, log_error, log_warning

from .db_operations import ReportsDBOperations
from .utils import ReportFilters, ReportExporter
from .sub_pages import (
    SaleReportView,
    PurchaseReportView,
    AllTransactionsView,
    DayBookView,
    ProfitLossView,
    BillWiseProfitView,
    CashTransactionsView,
    BalanceReportView
)


class ReportsPage(QWidget):
    """
    Vyapar-style Reports page with sidebar navigation and dynamic content.
    
    Architecture:
    - Left sidebar: 8 report categories (Sale, Purchase, Transactions, etc.)
    - Right content: Stacked widget showing selected report
    - Shared filters and database operations
    """
    
    def __init__(
        self,
        colors: dict,
        invoice_config: dict,
        app_config: dict,
        get_table_style: callable,
        get_button_style: callable,
        get_input_style: callable,
        get_label_style: callable,
        dashboard_ref
    ):
        """
        Initialize Reports page.
        
        Args:
            colors: Color scheme dictionary
            invoice_config: Invoice configuration
            app_config: Application configuration
            get_table_style: Function to get table stylesheet
            get_button_style: Function to get button stylesheet
            get_input_style: Function to get input stylesheet
            get_label_style: Function to get label stylesheet
            dashboard_ref: Reference to parent dashboard
        """
        super().__init__()
        self.colors = colors
        self.invoice_config = invoice_config
        self.app_config = app_config
        self.get_table_style = get_table_style
        self.get_button_style = get_button_style
        self.get_input_style = get_input_style
        self.get_label_style = get_label_style
        self.dashboard = dashboard_ref
        
        # Initialize database operations
        self.db_operations = ReportsDBOperations()
        
        # Initialize filters
        self.filters = ReportFilters(colors, get_button_style)
        
        # Store all invoices for filtering
        self.all_invoices = []
        
        # Initialize all 8 sub-page views
        self.sale_report = SaleReportView(colors, get_button_style, self._export_report)
        self.purchase_report = PurchaseReportView(colors, get_button_style, self._export_report)
        self.all_transactions = AllTransactionsView(colors, get_button_style, self._export_report)
        self.day_book = DayBookView(colors, get_button_style, self._export_report)
        self.profit_loss = ProfitLossView(colors, get_button_style, self._export_report)
        self.bill_wise_profit = BillWiseProfitView(colors, get_button_style, self._export_report)
        self.cash_transactions = CashTransactionsView(colors, get_button_style, self._export_report)
        self.balance_report = BalanceReportView(colors, get_button_style, self._export_report)
        
        self._init_ui()
        log_info("ReportsPage initialized with modular architecture", 'billing_app')
    
    def _init_ui(self):
        """Initialize the UI components with Vyapar-style layout."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create content stack
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {self.colors['primary_bg']};
                border: none;
            }}
        """)
        self._create_report_views()
        main_layout.addWidget(self.content_stack, 1)
        
        # Load initial report data
        self._refresh_current_report(0)
    
    def showEvent(self, event):
        """Override showEvent to refresh data when page is shown."""
        super().showEvent(event)
        # Refresh current report when page becomes visible
        current_index = self.report_list.currentRow()
        if current_index >= 0:
            self._refresh_current_report(current_index)
            log_info(f"Reports page shown - refreshing report {current_index}", 'billing_app')
    
    def _create_sidebar(self) -> QWidget:
        """Create left sidebar with report categories."""
        sidebar_widget = QFrame()
        sidebar_widget.setFixedWidth(250)
        sidebar_widget.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-right: 2px solid #dcdcdc;
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        # Header
        header_label = QLabel("📊 Reports")
        header_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        header_label.setFont(header_font)
        header_label.setStyleSheet(f"color: {self.colors['text_primary']};")
        sidebar_layout.addWidget(header_label)
        
        # Report list
        self.report_list = QListWidget()
        
        self.report_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.report_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # --------------------------------
        
        self.report_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {self.colors['secondary_bg']};
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                padding: 15px 10px;
                border-radius: 8px;
                margin: 2px 0px;
                color: {self.colors['text_primary']};
                font-size: 13px;
            }}
            QListWidget::item:hover {{
                background-color: {self.colors.get('hover', "#7e7c7c")};
            }}
            QListWidget::item:selected {{
                background-color: {self.colors['accent_primary']};
                color: white;
                font-weight: bold;
            }}
        """)
        
        # Add report items
        report_names = [
            "📊 Sale Report",
            "🛒 Purchase Report",
            "📋 All Transactions",
            "📅 Day Book",
            "💰 Profit & Loss",
            "📈 Bill Wise Profit",
            "💵 Cash Transactions",
            "💳 Balance Report"
        ]
        
        for name in report_names:
            item = QListWidgetItem(name)
            self.report_list.addItem(item)
        
        # Select first item by default (before connecting signal to avoid premature trigger)
        self.report_list.setCurrentRow(0)
        
        # Connect signal AFTER setting initial selection
        self.report_list.currentRowChanged.connect(self._on_report_selected)
        
        sidebar_layout.addWidget(self.report_list)
        
        # Turned off to avoid scrollbar in sidebar
        # sidebar_layout.addStretch()
        
        # Footer info
        footer = QLabel("💡 Select a report category")
        footer.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 11px;
                padding: 15px;
                border-top: 1px solid #dcdcdc;
            }}
        """)
        footer.setWordWrap(True)
        sidebar_layout.addWidget(footer)
        
        return sidebar_widget
    
    def _create_report_views(self):
        """Create all 8 report view widgets and add to stack."""
        # Sale Report (with payment summary)
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.sale_report.set_filters_widget(filters_section)
        payment_summary = self._create_payment_summary_section()
        self.sale_report.set_payment_summary_widget(payment_summary)
        self.content_stack.addWidget(self.sale_report)
        
        # Purchase Report
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.purchase_report.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.purchase_report)
        
        # All Transactions
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.all_transactions.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.all_transactions)
        
        # Day Book
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.day_book.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.day_book)
        
        # Profit & Loss
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.profit_loss.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.profit_loss)
        
        # Bill Wise Profit
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.bill_wise_profit.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.bill_wise_profit)
        
        # Cash Transactions
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.cash_transactions.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.cash_transactions)
        
        # Balance Report
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.balance_report.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.balance_report)
    
    def _create_payment_summary_section(self) -> QFrame:
        """Create payment summary section showing total cash and bank received."""
        summary_frame = QFrame()
        summary_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        
        layout = QHBoxLayout(summary_frame)
        layout.setSpacing(20)
        
        # Cash box
        cash_box = QFrame()
        cash_box.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['success']};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        cash_layout = QVBoxLayout(cash_box)
        
        cash_title = QLabel("💵 Total Cash Received")
        cash_title.setStyleSheet("color: white; font-size: 12px;")
        cash_layout.addWidget(cash_title)
        
        self.lbl_total_cash = QLabel("₹0.00")
        self.lbl_total_cash.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        cash_layout.addWidget(self.lbl_total_cash)
        
        layout.addWidget(cash_box)
        
        # Bank box
        bank_box = QFrame()
        bank_box.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['accent_primary']};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        bank_layout = QVBoxLayout(bank_box)
        
        bank_title = QLabel("🏦 Total Bank Received")
        bank_title.setStyleSheet("color: white; font-size: 12px;")
        bank_layout.addWidget(bank_title)
        
        self.lbl_total_bank = QLabel("₹0.00")
        self.lbl_total_bank.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        bank_layout.addWidget(self.lbl_total_bank)
        
        layout.addWidget(bank_box)
        
        return summary_frame
    
    def _on_report_selected(self, index: int):
        """Handle report category selection from sidebar."""
        if index >= 0:
            self.content_stack.setCurrentIndex(index)
            self._refresh_current_report(index)
            log_info(f"Switched to report index {index}", 'billing_app')
    
    def _refresh_current_report(self, index: int):
        """Refresh data for the currently selected report."""
        try:
            # Load all invoices
            self.all_invoices = self.db_operations.load_all_invoices()
            
            # Apply filters
            filtered = self.filters.apply_filters(self.all_invoices)
            
            # Populate the appropriate report
            if index == 0:
                self.sale_report.populate(filtered)
            elif index == 1:
                self.purchase_report.populate(filtered)
            elif index == 2:
                self.all_transactions.populate(filtered)
            elif index == 3:
                self.day_book.populate(filtered)
            elif index == 4:
                self.profit_loss.populate(filtered)
            elif index == 5:
                self.bill_wise_profit.populate(filtered)
            elif index == 6:
                # Cash Transactions needs special handling - get cash payments from DB
                cash_payments = self.db_operations.get_cash_payments()
                self.cash_transactions.populate(invoices=filtered, cash_payments=cash_payments)
            elif index == 7:
                self.balance_report.populate(filtered)
            
            # Update payment summary
            self._update_payment_summary()
            
            log_info(f"Report refreshed successfully: index {index}", 'billing_app')
            
        except Exception as e:
            log_error(f"Error refreshing report at index {index}", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to refresh report: {str(e)}")
    
    def _update_payment_summary(self):
        """Calculate and update total cash and bank received from all invoices."""
        try:
            summary = self.db_operations.get_all_payments_summary()
            total_cash = summary['cash']
            total_bank = summary['bank']
            
            if hasattr(self, 'lbl_total_cash'):
                self.lbl_total_cash.setText(f"₹{total_cash:,.2f}")
            if hasattr(self, 'lbl_total_bank'):
                self.lbl_total_bank.setText(f"₹{total_bank:,.2f}")
            
            log_info(f"Payment summary updated - Cash: ₹{total_cash:,.2f}, Bank: ₹{total_bank:,.2f}", 'billing_app')
            
        except Exception as e:
            log_error("Error updating payment summary", exception=e, logger_name='billing_errors')
    
    def _handle_filter_change(self):
        """Unified filter change handler that refreshes the current report."""
        try:
            log_info("Handling filter change", 'billing_app')
            current_index = self.content_stack.currentIndex()
            self._refresh_current_report(current_index)
        except Exception as e:
            log_error("Error handling filter change", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to apply filter changes: {str(e)}")
    
    def _clear_filters(self):
        """Clear all filter values and show confirmation."""
        try:
            log_info("Clearing all filters", 'billing_app')
            self.filters.clear_filters()
            self._handle_filter_change()
            QMessageBox.information(self, "Filters Cleared", "All filters have been reset to default values.")
            log_info("Filters cleared successfully", 'billing_app')
        except Exception as e:
            log_error("Error clearing filters", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Error", f"Failed to clear filters: {str(e)}")
    
    def _export_report(self, report_type: str, format: str):
        """Export report to PDF or Excel."""
        try:
            if format == 'excel':
                current_view = self.content_stack.currentWidget()
                table = current_view.get_table_widget()
                ReportExporter.export_to_csv(table, report_type, self)
            else:
                QMessageBox.information(self, "Export PDF", "PDF export feature coming soon!")
        except Exception as e:
            log_error(f"Failed to export {report_type} report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Export Error", f"Failed to export report:\n{str(e)}")
