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
        
        # Store filter widgets for each report (indexed by report index)
        self.filter_widgets = {}
        
        # Initialize all 8 sub-page views
        self.sale_report = SaleReportView(colors, get_button_style, self._export_report)
        self.purchase_report = PurchaseReportView(colors, get_button_style, self._export_report)
        self.all_transactions = AllTransactionsView(colors, get_button_style, self._export_report)
        self.day_book = DayBookView(colors, get_button_style, self._export_report)
        self.profit_loss = ProfitLossView(colors, get_button_style, self._export_report)
        self.bill_wise_profit = BillWiseProfitView(colors, get_button_style, self._export_report)
        self.cash_transactions = CashTransactionsView(colors, get_button_style, self._export_report)
        self.balance_report = BalanceReportView(colors, get_button_style, self._export_report)
        
        # Set refresh callbacks for all reports
        for report in [self.sale_report, self.purchase_report, self.all_transactions,
                       self.day_book, self.profit_loss, self.bill_wise_profit,
                       self.cash_transactions, self.balance_report]:
            if hasattr(report, 'set_refresh_callback'):
                report.set_refresh_callback(lambda: self.load_report_data())
        
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
        
        # Load initial report data using the reusable function
        self.load_report_data()
    
    def showEvent(self, event):
        """Override showEvent to auto-refresh data when page is shown."""
        super().showEvent(event)
        # Auto-refresh current report when page becomes visible
        try:
            log_info("Reports page shown - auto-refreshing data", 'billing_app')
            self.load_report_data()
        except Exception as e:
            log_error("Error in showEvent auto-refresh", exception=e, logger_name='billing_errors')
    
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
        self.filter_widgets[0] = filters_section  # Store filter widget by report index
        self.sale_report.set_filters_widget(filters_section)
        payment_summary = self._create_payment_summary_section()
        self.sale_report.set_payment_summary_widget(payment_summary)
        self.content_stack.addWidget(self.sale_report)
        
        # Purchase Report
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.filter_widgets[1] = filters_section  # Store filter widget by report index
        self.purchase_report.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.purchase_report)
        
        # All Transactions
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.filter_widgets[2] = filters_section  # Store filter widget by report index
        self.all_transactions.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.all_transactions)
        
        # Day Book
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.filter_widgets[3] = filters_section  # Store filter widget by report index
        self.day_book.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.day_book)
        
        # Profit & Loss
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.filter_widgets[4] = filters_section  # Store filter widget by report index
        self.profit_loss.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.profit_loss)
        
        # Bill Wise Profit
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.filter_widgets[5] = filters_section  # Store filter widget by report index
        self.bill_wise_profit.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.bill_wise_profit)
        
        # Cash Transactions
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.filter_widgets[6] = filters_section  # Store filter widget by report index
        self.cash_transactions.set_filters_widget(filters_section)
        self.content_stack.addWidget(self.cash_transactions)
        
        # Balance Report
        filters_section = self.filters.create_filter_section(
            apply_callback=self._handle_filter_change,
            clear_callback=self._clear_filters
        )
        self.filter_widgets[7] = filters_section  # Store filter widget by report index
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
            # Auto-load data when switching reports
            self.load_report_data()
            log_info(f"Switched to report index {index}", 'billing_app')
    
    def load_report_data(self, filters=None):
        """
        Central reusable function to load report data with optional filters.
        
        This function:
        1. Loads all invoices from database
        2. Applies filters if provided (otherwise uses current filter values)
        3. Populates the current report view
        4. Updates payment summary
        5. Handles no-records scenarios
        
        Args:
            filters: Optional dict of filter values. If None, reads from filter widgets.
        """
        try:
            current_index = self.content_stack.currentIndex()
            log_info(f"Loading report data for index {current_index}", 'billing_app')
            
            # Load all invoices from database
            self.all_invoices = self.db_operations.load_all_invoices()
            log_info(f"Loaded {len(self.all_invoices)} invoices from database", 'billing_app')
            
            # Apply filters - switch to current report's filter widget first
            if filters is None:
                # Update filter references to current report's widgets before filtering
                self._switch_filter_context(current_index)
                filtered_invoices = self.filters.apply_filters(self.all_invoices)
            else:
                # Apply provided filter dict (future enhancement)
                self._switch_filter_context(current_index)
                filtered_invoices = self.filters.apply_filters(self.all_invoices)
            
            log_info(
                f"Filters applied: {len(filtered_invoices)} of {len(self.all_invoices)} invoices matched",
                'billing_app'
            )
            
            # Populate the current report
            self._populate_report_by_index(current_index, filtered_invoices)
            
            # Update payment summary
            self._update_payment_summary()
            
            log_info(f"Report data loaded successfully for index {current_index}", 'billing_app')
            
        except Exception as e:
            log_error("Error in load_report_data", exception=e, logger_name='billing_errors')
            QMessageBox.critical(
                self,
                "Data Load Error",
                f"Failed to load report data:\n{str(e)}"
            )
    
    def _populate_report_by_index(self, index: int, filtered_invoices: list):
        """Populate specific report by index with filtered data."""
        if index == 0:
            self.sale_report.populate(filtered_invoices)
        elif index == 1:
            self.purchase_report.populate(filtered_invoices)
        elif index == 2:
            self.all_transactions.populate(filtered_invoices)
        elif index == 3:
            self.day_book.populate(filtered_invoices)
        elif index == 4:
            self.profit_loss.populate(filtered_invoices)
        elif index == 5:
            self.bill_wise_profit.populate(filtered_invoices)
        elif index == 6:
            # Cash Transactions needs special handling - get cash payments from DB
            cash_payments = self.db_operations.get_cash_payments()
            self.cash_transactions.populate(invoices=filtered_invoices, cash_payments=cash_payments)
        elif index == 7:
            self.balance_report.populate(filtered_invoices)
    
    def _refresh_current_report(self, index: int = None):
        """
        Refresh data for the currently selected report.
        This is a convenience wrapper around load_report_data.
        
        Args:
            index: Optional report index (unused, kept for compatibility)
        """
        log_info("Refreshing current report", 'billing_app')
        self.load_report_data()
    
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
    
    def _switch_filter_context(self, report_index: int):
        """
        Switch the ReportFilters instance to read from the specified report's widgets.
        This ensures apply_filters() reads from the correct filter widget.
        
        Args:
            report_index: Index of the report (0-7) whose filter widgets to use
        """
        try:
            if report_index not in self.filter_widgets:
                log_warning(f"No filter widget found for report index {report_index}", 'billing_app')
                return
            
            current_filter_frame = self.filter_widgets[report_index]
            
            # Retrieve widget references that were stored as properties on the filter_frame
            # These were set in ReportFilters.create_filter_section()
            if hasattr(current_filter_frame, 'filter_from_date'):
                self.filters.filter_from_date = current_filter_frame.filter_from_date
                self.filters.filter_to_date = current_filter_frame.filter_to_date
                self.filters.filter_contact = current_filter_frame.filter_contact
                self.filters.filter_passenger = current_filter_frame.filter_passenger
                self.filters.filter_sector = current_filter_frame.filter_sector
                self.filters.filter_supplier = current_filter_frame.filter_supplier
                self.filters.filter_type = current_filter_frame.filter_type
                
                log_info(f"Switched filter context to report index {report_index}", 'billing_app')
            else:
                log_error(f"Filter widgets not found on filter_frame for report {report_index}", logger_name='billing_errors')
            
        except Exception as e:
            log_error(f"Error switching filter context to report {report_index}", exception=e, logger_name='billing_errors')
    
    def _handle_filter_change(self):
        """
        Handle Apply Filters button click.
        Refreshes the current report with filtered data.
        """
        try:
            log_info("Apply Filters clicked - refreshing report with filter values", 'billing_app')
            # Simply call load_report_data which will read current filter values
            self.load_report_data()
            log_info("Filters applied successfully", 'billing_app')
        except Exception as e:
            log_error("Error applying filters", exception=e, logger_name='billing_errors')
            QMessageBox.critical(
                self,
                "Filter Error",
                f"Failed to apply filters:\n{str(e)}"
            )
    
    def _clear_filters(self):
        """
        Handle Clear Filters button click.
        Resets all filter fields and reloads all data from database.
        """
        try:
            log_info("Clear Filters clicked - resetting all filters", 'billing_app')
            
            # Switch to current report's filter context first
            current_index = self.content_stack.currentIndex()
            self._switch_filter_context(current_index)
            
            # Reset all filter input fields to initial state
            self.filters.clear_filters()
            
            # Reload all data without filters (load_report_data will use cleared values)
            self.load_report_data()
            
            log_info("Filters cleared and data reloaded successfully", 'billing_app')
            
        except Exception as e:
            log_error("Error clearing filters", exception=e, logger_name='billing_errors')
            QMessageBox.critical(
                self,
                "Clear Error",
                f"Failed to clear filters:\n{str(e)}"
            )
    
    def _export_report(self, report_type: str, format: str):
        """Export report to PDF or Excel, then auto-refresh."""
        try:
            if format == 'excel':
                current_view = self.content_stack.currentWidget()
                table = current_view.get_table_widget()
                ReportExporter.export_to_csv(table, report_type, self)
                log_info(f"Exported {report_type} report to Excel successfully", 'billing_app')
                # Auto-refresh after export
                self.load_report_data()
            else:
                QMessageBox.information(self, "Export PDF", "PDF export feature coming soon!")
        except Exception as e:
            log_error(f"Failed to export {report_type} report", exception=e, logger_name='billing_errors')
            QMessageBox.critical(self, "Export Error", f"Failed to export report:\n{str(e)}")
