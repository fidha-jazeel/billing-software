"""
Reports Page Module
Vyapar-style Reports with sidebar navigation and dynamic content panels.
Contains comprehensive travel billing reports with filters and export options.
"""
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QTableWidget, QPushButton,
                             QLineEdit, QTableWidgetItem, QMessageBox, 
                             QFileDialog, QHeaderView, QDateEdit, QComboBox,
                             QStackedWidget, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont


class ReportsPage(QWidget):
    """Vyapar-style Reports page with sidebar navigation and dynamic content."""
    
    def __init__(self, colors, invoice_config, app_config, get_table_style, get_button_style,
                 get_input_style, get_label_style, dashboard_ref):
        """
        Initialize Reports page.
        
        Args:
            colors: Color scheme dictionary
            invoice_config: Invoice configuration dictionary
            app_config: Application configuration
            get_table_style: Function to get table stylesheet
            get_button_style: Function to get button stylesheet
            get_input_style: Function to get input stylesheet
            get_label_style: Function to get label stylesheet
            dashboard_ref: Reference to parent dashboard for accessing widgets
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
        
        # Store all invoices data for filtering
        self.all_invoices = []
        
        self._init_ui()
    
    def _configure_table(self, table, column_widths=None):
        """Configure table with proper sizing, sorting, and styling.
        
        Args:
            table: QTableWidget to configure
            column_widths: Dict mapping column index to width (None for auto-resize)
        """
        # Enable sorting
        table.setSortingEnabled(True)
        
        # Configure header
        header = table.horizontalHeader()
        header.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {self.colors['accent_primary']};
                color: white;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid {self.colors['primary_bg']};
                font-weight: bold;
                font-size: 13px;
                text-align: left;
            }}
            QHeaderView::section:hover {{
                background-color: {self.colors['accent_secondary']};
            }}
        """)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Make header sticky and non-movable
        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        header.setHighlightSections(True)
        
        # Set column widths
        if column_widths:
            for col, width in column_widths.items():
                if width == 'stretch':
                    header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
                elif isinstance(width, int):
                    table.setColumnWidth(col, width)
                    header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        else:
            # Default: resize to contents
            header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # Configure vertical header
        table.verticalHeader().setVisible(True)
        table.verticalHeader().setDefaultSectionSize(45)  # Row height
        
        # Alternating row colors for better readability
        table.setAlternatingRowColors(True)
        table.setStyleSheet(self.get_table_style() + f"""
            QTableWidget {{
                gridline-color: #e0e0e0;
                font-size: 13px;
                selection-background-color: {self.colors['accent_primary']};
                selection-color: white;
            }}
            QTableWidget::item {{
                padding: 8px 10px;
                border: none;
            }}
            QTableWidget::item:alternate {{
                background-color: #f9f9f9;
            }}
        """)
    
    def _init_ui(self):
        """Initialize the UI components with Vyapar-style layout."""
        # Main layout - horizontal split
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left Sidebar - Report Categories
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Right Panel - Dynamic Content
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"""
            QStackedWidget {{
                background-color: {self.colors['primary_bg']};
            }}
        """)
        
        # Create all report views
        self._create_report_views()
        
        main_layout.addWidget(self.content_stack, 1)
    
    def _create_sidebar(self) -> QWidget:
        """Create left sidebar with report categories."""
        sidebar_widget = QFrame()
        sidebar_widget.setFixedWidth(280)
        sidebar_widget.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-right: 2px solid #dcdcdc;
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Header
        header = QLabel("📊 Reports")
        header.setStyleSheet(f"""
            QLabel {{
                background-color: {self.colors['accent_primary']};
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px 15px;
                border: none;
            }}
        """)
        sidebar_layout.addWidget(header)
        
        # Report categories list
        self.report_list = QListWidget()
        self.report_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {self.colors['secondary_bg']};
                border: none;
                outline: none;
                padding: 10px 0px;
            }}
            QListWidget::item {{
                color: {self.colors['text_primary']};
                padding: 15px 20px;
                margin: 2px 8px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }}
            QListWidget::item:hover {{
                background-color: {self.colors['primary_bg']};
            }}
            QListWidget::item:selected {{
                background-color: {self.colors['accent_primary']};
                color: white;
            }}
        """)
        
        # Add report categories
        report_categories = [
            ("📈 Sale Report", "sale_report"),
            ("📉 Purchase Report", "purchase_report"),
            ("📋 All Transactions", "all_transactions"),
            ("📅 Day Book", "day_book"),
            ("💰 Profit and Loss", "profit_loss"),
            ("📊 Bill Wise Profit", "bill_wise_profit"),
            ("💵 Cash Transactions", "cash_transactions"),
            ("⚖️ Balance Report", "balance_report"),
        ]
        
        for display_name, key in report_categories:
            item = QListWidgetItem(display_name)
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.report_list.addItem(item)
        
        # Select first item by default
        self.report_list.setCurrentRow(0)
        self.report_list.currentRowChanged.connect(self._on_report_selected)
        
        sidebar_layout.addWidget(self.report_list)
        
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
        """Create all report view widgets."""
        # Sale Report
        self.sale_report_view = self._create_sale_report_view()
        self.content_stack.addWidget(self.sale_report_view)
        
        # Initialize payment summary
        self._update_payment_summary()
        
        # Purchase Report
        self.purchase_report_view = self._create_purchase_report_view()
        self.content_stack.addWidget(self.purchase_report_view)
        
        # All Transactions
        self.all_transactions_view = self._create_all_transactions_view()
        self.content_stack.addWidget(self.all_transactions_view)
        
        # Day Book
        self.day_book_view = self._create_day_book_view()
        self.content_stack.addWidget(self.day_book_view)
        
        # Profit and Loss
        self.profit_loss_view = self._create_profit_loss_view()
        self.content_stack.addWidget(self.profit_loss_view)
        
        # Bill Wise Profit
        self.bill_wise_profit_view = self._create_bill_wise_profit_view()
        self.content_stack.addWidget(self.bill_wise_profit_view)
        
        # Cash Transactions
        self.cash_transactions_view = self._create_cash_transactions_view()
        self.content_stack.addWidget(self.cash_transactions_view)
        
        # Balance Report
        self.balance_report_view = self._create_balance_report_view()
        self.content_stack.addWidget(self.balance_report_view)
    
    def _on_report_selected(self, index):
        """Handle report category selection."""
        if index >= 0:
            self.content_stack.setCurrentIndex(index)
            self._refresh_current_report(index)
    
    def _refresh_current_report(self, index):
        """Refresh data for the currently selected report."""
        # Load all invoices
        self._load_all_invoices()
        
        # Refresh based on report type
        if index == 0:  # Sale Report
            self._populate_sale_report()
        elif index == 1:  # Purchase Report
            self._populate_purchase_report()
        elif index == 2:  # All Transactions
            self._populate_all_transactions()
        elif index == 3:  # Day Book
            self._populate_day_book()
        elif index == 4:  # Profit and Loss
            self._populate_profit_loss()
        elif index == 5:  # Bill Wise Profit
            self._populate_bill_wise_profit()
        elif index == 6:  # Cash Transactions
            self._populate_cash_transactions()
        elif index == 7:  # Balance Report
            self._populate_balance_report()
        
        # Update payment summary whenever report is refreshed
        self._update_payment_summary()
    
    def _create_payment_summary_section(self) -> QFrame:
        """Create payment summary section showing total cash and bank received."""
        summary_frame = QFrame()
        summary_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                border: 2px solid {self.colors['accent_primary']};
                padding: 15px;
            }}
        """)
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setContentsMargins(20, 15, 20, 15)
        summary_layout.setSpacing(30)
        
        # Total Cash Received Box
        cash_box = QFrame()
        cash_box.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary_bg']};
                border-radius: 8px;
                border: 2px solid {self.colors['success']};
                padding: 15px;
            }}
        """)
        cash_layout = QVBoxLayout(cash_box)
        cash_layout.setSpacing(8)
        
        cash_title = QLabel("💵 Total Cash Received")
        cash_title.setStyleSheet(f"""
            color: {self.colors['success']};
            font-size: 14px;
            font-weight: bold;
        """)
        cash_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cash_layout.addWidget(cash_title)
        
        self.lbl_total_cash = QLabel("₹0.00")
        self.lbl_total_cash.setStyleSheet(f"""
            color: {self.colors['accent_gold']};
            font-size: 24px;
            font-weight: bold;
        """)
        self.lbl_total_cash.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cash_layout.addWidget(self.lbl_total_cash)
        
        summary_layout.addWidget(cash_box)
        
        # Total Bank Received Box
        bank_box = QFrame()
        bank_box.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['primary_bg']};
                border-radius: 8px;
                border: 2px solid {self.colors['accent_cyan']};
                padding: 15px;
            }}
        """)
        bank_layout = QVBoxLayout(bank_box)
        bank_layout.setSpacing(8)
        
        bank_title = QLabel("🏦 Total Bank Received")
        bank_title.setStyleSheet(f"""
            color: {self.colors['accent_cyan']};
            font-size: 14px;
            font-weight: bold;
        """)
        bank_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bank_layout.addWidget(bank_title)
        
        self.lbl_total_bank = QLabel("₹0.00")
        self.lbl_total_bank.setStyleSheet(f"""
            color: {self.colors['accent_gold']};
            font-size: 24px;
            font-weight: bold;
        """)
        self.lbl_total_bank.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bank_layout.addWidget(self.lbl_total_bank)
        
        summary_layout.addWidget(bank_box)
        
        return summary_frame
    
    def _update_payment_summary(self):
        """Calculate and update total cash and bank received from all invoices."""
        try:
            total_cash = 0.0
            total_bank = 0.0
            
            invoices_dir = self.invoice_config.get('save_directory', 'invoices')
            if not os.path.exists(invoices_dir):
                os.makedirs(invoices_dir, exist_ok=True)
            
            for filename in os.listdir(invoices_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(invoices_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            invoice_data = json.load(f)
                        
                        payment_mode = invoice_data.get("payment_mode", "Cash")
                        received_str = invoice_data.get("received", "0")
                        
                        # Clean the received amount string
                        received = float(received_str.replace('₹', '').replace(',', '').strip() or 0)
                        
                        # Categorize payment
                        if payment_mode == "Cash":
                            total_cash += received
                        else:
                            # All non-cash payments are considered bank
                            total_bank += received
                            
                    except Exception as e:
                        print(f"Error processing invoice {filename}: {e}")
                        continue
            
            # Update labels with formatted currency
            self.lbl_total_cash.setText(f"₹{total_cash:,.2f}")
            self.lbl_total_bank.setText(f"₹{total_bank:,.2f}")
            
        except Exception as e:
            print(f"Error updating payment summary: {e}")
            self.lbl_total_cash.setText("₹0.00")
            self.lbl_total_bank.setText("₹0.00")
    
    def _load_all_invoices(self):
        """Load all invoices from files."""
        self.all_invoices = []
        
        try:
            invoices_dir = self.invoice_config.get('save_directory', 'invoices')
            if not os.path.exists(invoices_dir):
                return
            
            invoice_files = [f for f in os.listdir(invoices_dir) if f.endswith('.json')]
            
            for filename in invoice_files:
                filepath = os.path.join(invoices_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data['_filepath'] = filepath
                        self.all_invoices.append(data)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        except Exception as e:
            print(f"Error loading invoices: {e}")
    
    def _create_common_filters(self) -> QFrame:
        """Create common filter section for reports with enhanced styling."""
        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                padding: 20px;
            }}
        """)
        
        filter_layout = QVBoxLayout(filter_frame)
        filter_layout.setSpacing(15)
        filter_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        filter_title = QLabel("🔍 Filter Options")
        filter_title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 15px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
        """)
        filter_layout.addWidget(filter_title)
        
        # Date Range
        date_row = QHBoxLayout()
        date_row.setSpacing(10)
        
        from_label = QLabel("From:")
        from_label.setStyleSheet(self.get_label_style())
        date_row.addWidget(from_label)
        
        self.filter_from_date = QDateEdit()
        self.filter_from_date.setCalendarPopup(True)
        self.filter_from_date.setDate(QDate.currentDate().addMonths(-1))
        self.filter_from_date.setStyleSheet(self.get_input_style())
        date_row.addWidget(self.filter_from_date)
        
        to_label = QLabel("To:")
        to_label.setStyleSheet(self.get_label_style())
        date_row.addWidget(to_label)
        
        self.filter_to_date = QDateEdit()
        self.filter_to_date.setCalendarPopup(True)
        self.filter_to_date.setDate(QDate.currentDate())
        self.filter_to_date.setStyleSheet(self.get_input_style())
        date_row.addWidget(self.filter_to_date)
        
        filter_layout.addLayout(date_row)
        
        # Contact Number
        contact_row = QHBoxLayout()
        contact_label = QLabel("Contact:")
        contact_label.setStyleSheet(self.get_label_style())
        contact_row.addWidget(contact_label)
        
        self.filter_contact = QLineEdit()
        self.filter_contact.setPlaceholderText("Search by contact number...")
        self.filter_contact.setStyleSheet(self.get_input_style())
        contact_row.addWidget(self.filter_contact)
        
        filter_layout.addLayout(contact_row)
        
        # Passenger Name
        passenger_row = QHBoxLayout()
        passenger_label = QLabel("Passenger:")
        passenger_label.setStyleSheet(self.get_label_style())
        passenger_row.addWidget(passenger_label)
        
        self.filter_passenger = QLineEdit()
        self.filter_passenger.setPlaceholderText("Search by passenger name...")
        self.filter_passenger.setStyleSheet(self.get_input_style())
        passenger_row.addWidget(self.filter_passenger)
        
        filter_layout.addLayout(passenger_row)
        
        # Sector and Supplier
        sector_supplier_row = QHBoxLayout()
        
        sector_label = QLabel("Sector:")
        sector_label.setStyleSheet(self.get_label_style())
        sector_supplier_row.addWidget(sector_label)
        
        self.filter_sector = QLineEdit()
        self.filter_sector.setPlaceholderText("Sector...")
        self.filter_sector.setStyleSheet(self.get_input_style())
        sector_supplier_row.addWidget(self.filter_sector)
        
        supplier_label = QLabel("Supplier:")
        supplier_label.setStyleSheet(self.get_label_style())
        sector_supplier_row.addWidget(supplier_label)
        
        self.filter_supplier = QComboBox()
        self.filter_supplier.addItems(["All", "IndiGo", "Air India", "SpiceJet", "Vistara", "AirAsia", "Other"])
        self.filter_supplier.setStyleSheet(self.get_input_style())
        sector_supplier_row.addWidget(self.filter_supplier)
        
        filter_layout.addLayout(sector_supplier_row)
        
        # Booking Type
        type_row = QHBoxLayout()
        type_label = QLabel("Type:")
        type_label.setStyleSheet(self.get_label_style())
        type_row.addWidget(type_label)
        
        self.filter_type = QComboBox()
        self.filter_type.addItems(["All", "Flight", "Hotel", "Visa", "Tour Package", "Insurance", "Other"])
        self.filter_type.setStyleSheet(self.get_input_style())
        type_row.addWidget(self.filter_type)
        
        filter_layout.addLayout(type_row)
        
        # Apply and Clear buttons
        btn_row = QHBoxLayout()
        
        apply_btn = QPushButton("✓ Apply Filters")
        apply_btn.setStyleSheet(self.get_button_style('add'))
        apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        apply_btn.clicked.connect(self._handle_filter_change)
        btn_row.addWidget(apply_btn)
        
        clear_btn = QPushButton("✕ Clear")
        clear_btn.setStyleSheet(self.get_button_style('delete'))
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear_filters)
        btn_row.addWidget(clear_btn)
        
        filter_layout.addLayout(btn_row)
        
        return filter_frame
    
    def _clear_filters(self):
        """Clear all filter values and show confirmation."""
        self.filter_from_date.setDate(QDate.currentDate().addMonths(-1))
        self.filter_to_date.setDate(QDate.currentDate())
        self.filter_contact.clear()
        self.filter_passenger.clear()
        self.filter_sector.clear()
        self.filter_supplier.setCurrentIndex(0)
        self.filter_type.setCurrentIndex(0)
        
        # Apply the cleared filters
        self._handle_filter_change()
        
        # Show confirmation
        QMessageBox.information(self, "Filters Cleared", "All filters have been reset to default values.")
    
    def _handle_filter_change(self):
        """Unified filter change handler that refreshes the current report.
        
        This method is called whenever any filter changes (month selector, 
        date range, firm selector, etc.). It collects all active filter values
        and applies them to refresh the report data without duplicate calls.
        """
        # Get current report index
        current_index = self.content_stack.currentIndex()
        
        # Load all invoices
        self._load_all_invoices()
        
        # Refresh the current report with updated filters
        self._refresh_current_report(current_index)
    
    def _apply_filters(self, invoices):
        """Apply current filters to invoice list."""
        filtered = []
        
        from_date = self.filter_from_date.date().toPyDate()
        to_date = self.filter_to_date.date().toPyDate()
        contact = self.filter_contact.text().lower()
        passenger = self.filter_passenger.text().lower()
        sector = self.filter_sector.text().lower()
        supplier = self.filter_supplier.currentText()
        booking_type = self.filter_type.currentText()
        
        for invoice in invoices:
            # Date filter
            try:
                date_str = invoice.get('invoice_date', '')
                if date_str:
                    day, month, year = map(int, date_str.split('/'))
                    invoice_date = datetime(year, month, day).date()
                    if not (from_date <= invoice_date <= to_date):
                        continue
            except:
                pass
            
            # Contact filter
            if contact and contact not in invoice.get('contact_number', '').lower():
                continue
            
            # Type filter
            if booking_type != "All" and invoice.get('type', '') != booking_type:
                continue
            
            # Passenger, sector, supplier filters (check items)
            if passenger or sector or supplier != "All":
                match_found = False
                for item in invoice.get('items', []):
                    if passenger and passenger in item.get('passenger_name', '').lower():
                        match_found = True
                    if sector and sector in item.get('sector', '').lower():
                        match_found = True
                    if supplier != "All" and supplier == item.get('supplier', ''):
                        match_found = True
                    if match_found:
                        break
                if not match_found and (passenger or sector or supplier != "All"):
                    continue
            
            filtered.append(invoice)
        
        return filtered
    
    def _show_no_records_message(self, report_name):
        """Show message when no records match the filter criteria."""
        QMessageBox.information(
            self,
            "No Records Found",
            f"No records match the selected filter criteria in {report_name}.\n\n"
            "Please try adjusting your filters and click 'Apply Filters' again."
        )
    
    def _create_report_header(self, title, description="") -> QWidget:
        """Create consistent styled header for reports.
        
        Args:
            title: Main title text with emoji
            description: Optional subtitle/description
            
        Returns:
            QWidget containing the styled header
        """
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 15)
        header_layout.setSpacing(5)
        
        # Main title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 26px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
        """)
        header_layout.addWidget(title_label)
        
        # Description if provided
        if description:
            desc_label = QLabel(description)
            desc_label.setStyleSheet(f"""
                QLabel {{
                    color: {self.colors['text_secondary']};
                    font-size: 14px;
                    font-weight: 400;
                    margin-top: 5px;
                }}
            """)
            header_layout.addWidget(desc_label)
        
        return header_widget
    
    def _create_sale_report_view(self) -> QWidget:
        """Create Sale Report view."""
        container = QWidget()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        header = self._create_report_header(
            "📈 Sale Report",
            "Comprehensive overview of all sales invoices and revenue"
        )
        layout.addWidget(header)
        
        # Payment Summary Section
        payment_summary_frame = self._create_payment_summary_section()
        layout.addWidget(payment_summary_frame)
        
        # Filters
        filters = self._create_common_filters()
        layout.addWidget(filters)
        
        # Summary Cards
        self.sale_summary_frame = self._create_summary_cards(['Total Sales', 'Total Invoices', 'Avg Invoice Value'])
        layout.addWidget(self.sale_summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pdf_btn.clicked.connect(lambda: self._export_report('sale', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(lambda: self._export_report('sale', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.sale_table = QTableWidget(0, 7)
        self.sale_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Contact", "Type", "Total", "Status"
        ])
        # Configure with optimal column widths
        self._configure_table(self.sale_table, {
            0: 140,  # Invoice #
            1: 100,  # Date
            2: 'stretch',  # Customer
            3: 120,  # Contact
            4: 100,  # Type
            5: 120,  # Total
            6: 120   # Status
        })
        self.sale_table.setMinimumHeight(500)
        layout.addWidget(self.sale_table)
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
        
        return container
    
    def _populate_sale_report(self):
        """Populate sale report with filtered data."""
        filtered_invoices = self._apply_filters(self.all_invoices)
        
        self.sale_table.setRowCount(0)
        
        # Check if no records found
        if not filtered_invoices:
            self._show_no_records_message("Sale Report")
            # Update summary with zeros
            self._update_summary_cards(self.sale_summary_frame, [
                "₹0.00",
                "0",
                "₹0.00"
            ])
            return
        
        total_sales = 0.0
        
        for invoice in filtered_invoices:
            row = self.sale_table.rowCount()
            self.sale_table.insertRow(row)
            
            # Invoice Number
            self.sale_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_number', '')))
            
            # Date
            self.sale_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_date', '')))
            
            # Customer
            self.sale_table.setItem(row, 2, QTableWidgetItem(invoice.get('customer_name', '')))
            
            # Contact
            self.sale_table.setItem(row, 3, QTableWidgetItem(invoice.get('contact_number', '')))
            
            # Type
            self.sale_table.setItem(row, 4, QTableWidgetItem(invoice.get('type', '')))
            
            # Total
            total_str = str(invoice.get('total', '₹0.00')).replace('₹', '').replace(',', '').strip()
            try:
                total = float(total_str)
                total_sales += total
            except:
                total = 0.0
            
            total_item = QTableWidgetItem(f"₹{total:,.2f}")
            total_item.setForeground(QColor(self.colors['accent_gold']))
            self.sale_table.setItem(row, 5, total_item)
            
            # Status
            balance_str = str(invoice.get('balance', '₹0.00'))
            if 'Paid' in balance_str or '₹0.00' in balance_str:
                status = '✅ Paid'
                color = self.colors['success']
            else:
                status = '⏳ Pending'
                color = self.colors['danger']
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(color))
            self.sale_table.setItem(row, 6, status_item)
        
        # Update summary
        self._update_summary_cards(self.sale_summary_frame, [
            f"₹{total_sales:,.2f}",
            str(len(filtered_invoices)),
            f"₹{total_sales/len(filtered_invoices):,.2f}" if filtered_invoices else "₹0.00"
        ])
    
    def _create_purchase_report_view(self) -> QWidget:
        """Create Purchase Report view."""
        container = QWidget()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("📉 Purchase Report")
        header.setStyleSheet(f"QLabel {{ color: {self.colors['accent_primary']}; font-size: 22px; font-weight: bold; }}")
        layout.addWidget(header)
        
        # Filters
        filters = self._create_common_filters()
        layout.addWidget(filters)
        
        # Summary Cards
        self.purchase_summary_frame = self._create_summary_cards(['Total Purchases', 'Total Items', 'Avg Cost'])
        layout.addWidget(self.purchase_summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pdf_btn.clicked.connect(lambda: self._export_report('purchase', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(lambda: self._export_report('purchase', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.purchase_table = QTableWidget(0, 6)
        self.purchase_table.setHorizontalHeaderLabels([
            "Passenger", "Supplier", "Sector", "PNR", "Qty", "Supplier Amount"
        ])
        # Configure with optimal column widths
        self._configure_table(self.purchase_table, {
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
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
        
        return container
    
    def _populate_purchase_report(self):
        """Populate purchase report with filtered data."""
        filtered_invoices = self._apply_filters(self.all_invoices)
        
        self.purchase_table.setRowCount(0)
        
        # Check if no records found
        if not filtered_invoices:
            self._show_no_records_message("Purchase Report")
            # Update summary with zeros
            self._update_summary_cards(self.purchase_summary_frame, [
                "₹0.00",
                "0",
                "₹0.00"
            ])
            return
        
        total_purchases = 0.0
        total_items = 0
        
        for invoice in filtered_invoices:
            for item in invoice.get('items', []):
                row = self.purchase_table.rowCount()
                self.purchase_table.insertRow(row)
                
                # Passenger
                self.purchase_table.setItem(row, 0, QTableWidgetItem(item.get('passenger_name', '')))
                
                # Supplier
                self.purchase_table.setItem(row, 1, QTableWidgetItem(item.get('supplier', '')))
                
                # Sector
                self.purchase_table.setItem(row, 2, QTableWidgetItem(item.get('sector', '')))
                
                # PNR
                self.purchase_table.setItem(row, 3, QTableWidgetItem(item.get('pnr', '')))
                
                # Qty
                qty = item.get('qty', 1.0)
                self.purchase_table.setItem(row, 4, QTableWidgetItem(str(qty)))
                total_items += qty
                
                # Supplier Amount
                supp_amt = item.get('supplier_amount', 0.0)
                total_purchases += supp_amt
                
                amt_item = QTableWidgetItem(f"₹{supp_amt:,.2f}")
                amt_item.setForeground(QColor(self.colors['accent_gold']))
                self.purchase_table.setItem(row, 5, amt_item)
        
        # Update summary
        self._update_summary_cards(self.purchase_summary_frame, [
            f"₹{total_purchases:,.2f}",
            str(int(total_items)),
            f"₹{total_purchases/total_items:,.2f}" if total_items > 0 else "₹0.00"
        ])
    
    def _create_all_transactions_view(self) -> QWidget:
        """Create All Transactions view."""
        container = QWidget()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("📋 All Transactions")
        header.setStyleSheet(f"QLabel {{ color: {self.colors['accent_primary']}; font-size: 22px; font-weight: bold; }}")
        layout.addWidget(header)
        
        # Filters
        filters = self._create_common_filters()
        layout.addWidget(filters)
        
        # Summary Cards
        self.transactions_summary_frame = self._create_summary_cards(['Total Transactions', 'Total Value', 'Avg Transaction'])
        layout.addWidget(self.transactions_summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pdf_btn.clicked.connect(lambda: self._export_report('transactions', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(lambda: self._export_report('transactions', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.transactions_table = QTableWidget(0, 8)
        self.transactions_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Contact", "Passenger", "Type", "Total", "Status"
        ])
        # Configure with optimal column widths
        self._configure_table(self.transactions_table, {
            0: 140,  # Invoice #
            1: 100,  # Date
            2: 'stretch',  # Customer
            3: 120,  # Contact
            4: 'stretch',  # Passenger
            5: 100,  # Type
            6: 120,  # Total
            7: 110   # Status
        })
        self.transactions_table.setMinimumHeight(500)
        layout.addWidget(self.transactions_table)
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
        
        return container
    
    def _populate_all_transactions(self):
        """Populate all transactions with filtered data."""
        filtered_invoices = self._apply_filters(self.all_invoices)
        
        self.transactions_table.setRowCount(0)
        
        # Check if no records found
        if not filtered_invoices:
            self._show_no_records_message("All Transactions")
            # Update summary with zeros
            self._update_summary_cards(self.transactions_summary_frame, [
                "0",
                "₹0.00",
                "₹0.00"
            ])
            return
        
        total_value = 0.0
        transaction_count = 0
        
        for invoice in filtered_invoices:
            for item in invoice.get('items', []):
                row = self.transactions_table.rowCount()
                self.transactions_table.insertRow(row)
                
                # Invoice #
                self.transactions_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_number', '')))
                
                # Date
                self.transactions_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_date', '')))
                
                # Customer
                self.transactions_table.setItem(row, 2, QTableWidgetItem(invoice.get('customer_name', '')))
                
                # Contact
                self.transactions_table.setItem(row, 3, QTableWidgetItem(invoice.get('contact_number', '')))
                
                # Passenger
                self.transactions_table.setItem(row, 4, QTableWidgetItem(item.get('passenger_name', '')))
                
                # Type
                self.transactions_table.setItem(row, 5, QTableWidgetItem(invoice.get('type', '')))
                
                # Total (customer amount from item)
                amt = item.get('amount', 0.0)
                # Convert amt to float safely
                amt_clean = str(amt).replace('₹', '').replace(',', '').strip()
                try:
                    amt_value = float(amt_clean)
                except:
                    amt_value = 0.0
                total_value += amt_value
                transaction_count += 1
                
                amt_item = QTableWidgetItem(f"₹{amt_value:,.2f}")
                amt_item.setForeground(QColor(self.colors['accent_gold']))
                self.transactions_table.setItem(row, 6, amt_item)
                
                # Status
                balance_str = str(invoice.get('balance', '₹0.00'))
                if 'Paid' in balance_str or '₹0.00' in balance_str:
                    status = '✅ Paid'
                    color = self.colors['success']
                else:
                    status = '⏳ Pending'
                    color = self.colors['danger']
                
                status_item = QTableWidgetItem(status)
                status_item.setForeground(QColor(color))
                self.transactions_table.setItem(row, 7, status_item)
        
        # Update summary
        self._update_summary_cards(self.transactions_summary_frame, [
            str(transaction_count),
            f"₹{total_value:,.2f}",
            f"₹{total_value/transaction_count:,.2f}" if transaction_count > 0 else "₹0.00"
        ])
    
    def _create_day_book_view(self) -> QWidget:
        """Create Day Book view."""
        container = QWidget()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("📅 Day Book")
        header.setStyleSheet(f"QLabel {{ color: {self.colors['accent_primary']}; font-size: 22px; font-weight: bold; }}")
        layout.addWidget(header)
        
        # Filters
        filters = self._create_common_filters()
        layout.addWidget(filters)
        
        # Summary Cards
        self.daybook_summary_frame = self._create_summary_cards(['Daily Sales', 'Daily Purchases', 'Net Profit'])
        layout.addWidget(self.daybook_summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pdf_btn.clicked.connect(lambda: self._export_report('daybook', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(lambda: self._export_report('daybook', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.daybook_table = QTableWidget(0, 5)
        self.daybook_table.setHorizontalHeaderLabels([
            "Date", "Invoices", "Sales", "Purchases", "Profit"
        ])
        # Configure with optimal column widths
        self._configure_table(self.daybook_table, {
            0: 'stretch',  # Date
            1: 100,  # Invoices
            2: 'stretch',  # Sales
            3: 'stretch',  # Purchases
            4: 'stretch'   # Profit
        })
        self.daybook_table.setMinimumHeight(500)
        layout.addWidget(self.daybook_table)
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
        
        return container
    
    def _populate_day_book(self):
        """Populate day book with filtered data."""
        filtered_invoices = self._apply_filters(self.all_invoices)
        
        # Check if no records found
        if not filtered_invoices:
            self._show_no_records_message("Day Book")
            self.daybook_table.setRowCount(0)
            # Update summary with zeros
            self._update_summary_cards(self.daybook_summary_frame, [
                "₹0.00",
                "₹0.00",
                "₹0.00"
            ])
            return
        
        # Group by date
        daily_data = {}
        
        for invoice in filtered_invoices:
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
            
            # Sales
            total_str = str(invoice.get('total', '₹0.00')).replace('₹', '').replace(',', '').strip()
            try:
                daily_data[date]['sales'] += float(total_str)
            except:
                pass
            
            # Purchases
            for item in invoice.get('items', []):
                daily_data[date]['purchases'] += item.get('supplier_amount', 0.0)
        
        # Populate table
        self.daybook_table.setRowCount(0)
        
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
            sales_item.setForeground(QColor(self.colors['success']))
            self.daybook_table.setItem(row, 2, sales_item)
            
            # Purchases
            purchases_item = QTableWidgetItem(f"₹{data['purchases']:,.2f}")
            purchases_item.setForeground(QColor(self.colors['danger']))
            self.daybook_table.setItem(row, 3, purchases_item)
            
            # Profit
            profit_item = QTableWidgetItem(f"₹{profit:,.2f}")
            profit_item.setForeground(QColor(self.colors['accent_primary']))
            self.daybook_table.setItem(row, 4, profit_item)
        
        # Update summary
        self._update_summary_cards(self.daybook_summary_frame, [
            f"₹{total_sales:,.2f}",
            f"₹{total_purchases:,.2f}",
            f"₹{total_profit:,.2f}"
        ])
    
    def _create_profit_loss_view(self) -> QWidget:
        """Create Profit and Loss view."""
        container = QWidget()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("💰 Profit and Loss Statement")
        header.setStyleSheet(f"QLabel {{ color: {self.colors['accent_primary']}; font-size: 22px; font-weight: bold; }}")
        layout.addWidget(header)
        
        # Filters
        filters = self._create_common_filters()
        layout.addWidget(filters)
        
        # P&L Summary Frame
        self.pl_frame = QFrame()
        self.pl_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        pl_layout = QVBoxLayout(self.pl_frame)
        
        # Revenue Section
        revenue_label = QLabel("📈 Revenue")
        revenue_label.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {self.colors['accent_primary']};")
        pl_layout.addWidget(revenue_label)
        
        self.pl_revenue_label = QLabel("Total Sales: ₹0.00")
        self.pl_revenue_label.setStyleSheet(f"font-size: 18px; color: {self.colors['success']}; padding: 5px 20px;")
        pl_layout.addWidget(self.pl_revenue_label)
        
        pl_layout.addSpacing(10)
        
        # Expenses Section
        expenses_label = QLabel("📉 Expenses")
        expenses_label.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {self.colors['accent_primary']};")
        pl_layout.addWidget(expenses_label)
        
        self.pl_expenses_label = QLabel("Total Purchases: ₹0.00")
        self.pl_expenses_label.setStyleSheet(f"font-size: 18px; color: {self.colors['danger']}; padding: 5px 20px;")
        pl_layout.addWidget(self.pl_expenses_label)
        
        pl_layout.addSpacing(10)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #dcdcdc;")
        pl_layout.addWidget(separator)
        
        pl_layout.addSpacing(10)
        
        # Net Profit
        profit_label = QLabel("💵 Net Profit")
        profit_label.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {self.colors['accent_primary']};")
        pl_layout.addWidget(profit_label)
        
        self.pl_profit_label = QLabel("₹0.00")
        self.pl_profit_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {self.colors['accent_gold']}; padding: 5px 20px;")
        pl_layout.addWidget(self.pl_profit_label)
        
        self.pl_margin_label = QLabel("Profit Margin: 0%")
        self.pl_margin_label.setStyleSheet(f"font-size: 14px; color: {self.colors['text_secondary']}; padding: 5px 20px;")
        pl_layout.addWidget(self.pl_margin_label)
        
        layout.addWidget(self.pl_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pdf_btn.clicked.connect(lambda: self._export_report('profit_loss', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(lambda: self._export_report('profit_loss', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        layout.addStretch()
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
        
        return container
    
    def _populate_profit_loss(self):
        """Populate profit and loss data."""
        filtered_invoices = self._apply_filters(self.all_invoices)
        
        # Check if no records found
        if not filtered_invoices:
            self._show_no_records_message("Profit and Loss")
            # Update labels with zeros
            self.pl_revenue_label.setText("Total Sales: ₹0.00")
            self.pl_expenses_label.setText("Total Purchases: ₹0.00")
            self.pl_profit_label.setText("₹0.00")
            self.pl_margin_label.setText("Profit Margin: 0%")
            return
        
        total_revenue = 0.0
        total_expenses = 0.0
        
        for invoice in filtered_invoices:
            # Revenue
            total_str = str(invoice.get('total', '₹0.00')).replace('₹', '').replace(',', '').strip()
            try:
                total_revenue += float(total_str)
            except:
                pass
            
            # Expenses
            for item in invoice.get('items', []):
                total_expenses += item.get('supplier_amount', 0.0)
        
        net_profit = total_revenue - total_expenses
        margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Update labels
        self.pl_revenue_label.setText(f"Total Sales: ₹{total_revenue:,.2f}")
        self.pl_expenses_label.setText(f"Total Purchases: ₹{total_expenses:,.2f}")
        self.pl_profit_label.setText(f"₹{net_profit:,.2f}")
        self.pl_margin_label.setText(f"Profit Margin: {margin:.2f}%")
    
    def _create_bill_wise_profit_view(self) -> QWidget:
        """Create Bill Wise Profit view."""
        container = QWidget()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("📊 Bill Wise Profit Analysis")
        header.setStyleSheet(f"QLabel {{ color: {self.colors['accent_primary']}; font-size: 22px; font-weight: bold; }}")
        layout.addWidget(header)
        
        # Filters
        filters = self._create_common_filters()
        layout.addWidget(filters)
        
        # Summary Cards
        self.bill_profit_summary_frame = self._create_summary_cards(['Total Profit', 'Avg Profit/Invoice', 'Profit Margin %'])
        layout.addWidget(self.bill_profit_summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pdf_btn.clicked.connect(lambda: self._export_report('bill_profit', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(lambda: self._export_report('bill_profit', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.bill_profit_table = QTableWidget(0, 7)
        self.bill_profit_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Sales", "Purchases", "Profit", "Margin %"
        ])
        # Configure with optimal column widths
        self._configure_table(self.bill_profit_table, {
            0: 140,  # Invoice #
            1: 100,  # Date
            2: 'stretch',  # Customer
            3: 130,  # Sales
            4: 140,  # Purchases
            5: 130,  # Profit
            6: 110   # Margin %
        })
        self.bill_profit_table.setMinimumHeight(500)
        layout.addWidget(self.bill_profit_table)
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
        
        return container
    
    def _populate_bill_wise_profit(self):
        """Populate bill wise profit data."""
        filtered_invoices = self._apply_filters(self.all_invoices)
        
        self.bill_profit_table.setRowCount(0)
        
        # Check if no records found
        if not filtered_invoices:
            self._show_no_records_message("Bill Wise Profit")
            # Update summary with zeros
            self._update_summary_cards(self.bill_profit_summary_frame, [
                "₹0.00",
                "₹0.00",
                "0.00%"
            ])
            return
        
        total_profit = 0.0
        total_sales = 0.0
        total_purchases = 0.0
        
        for invoice in filtered_invoices:
            row = self.bill_profit_table.rowCount()
            self.bill_profit_table.insertRow(row)
            
            # Invoice #
            self.bill_profit_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_number', '')))
            
            # Date
            self.bill_profit_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_date', '')))
            
            # Customer
            self.bill_profit_table.setItem(row, 2, QTableWidgetItem(invoice.get('customer_name', '')))
            
            # Sales
            sale_str = str(invoice.get('total', '₹0.00')).replace('₹', '').replace(',', '').strip()
            try:
                sale_amt = float(sale_str)
            except:
                sale_amt = 0.0
            total_sales += sale_amt
            
            sale_item = QTableWidgetItem(f"₹{sale_amt:,.2f}")
            sale_item.setForeground(QColor(self.colors['success']))
            self.bill_profit_table.setItem(row, 3, sale_item)
            
            # Purchases
            purchase_amt = sum(item.get('supplier_amount', 0.0) for item in invoice.get('items', []))
            total_purchases += purchase_amt
            
            purchase_item = QTableWidgetItem(f"₹{purchase_amt:,.2f}")
            purchase_item.setForeground(QColor(self.colors['danger']))
            self.bill_profit_table.setItem(row, 4, purchase_item)
            
            # Profit
            profit = sale_amt - purchase_amt
            total_profit += profit
            
            profit_item = QTableWidgetItem(f"₹{profit:,.2f}")
            profit_item.setForeground(QColor(self.colors['accent_gold']))
            self.bill_profit_table.setItem(row, 5, profit_item)
            
            # Margin %
            margin = (profit / sale_amt * 100) if sale_amt > 0 else 0
            margin_item = QTableWidgetItem(f"{margin:.2f}%")
            margin_item.setForeground(QColor(self.colors['accent_primary']))
            self.bill_profit_table.setItem(row, 6, margin_item)
        
        # Update summary
        avg_profit = total_profit / len(filtered_invoices) if filtered_invoices else 0
        overall_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
        
        self._update_summary_cards(self.bill_profit_summary_frame, [
            f"₹{total_profit:,.2f}",
            f"₹{avg_profit:,.2f}",
            f"{overall_margin:.2f}%"
        ])
    
    def _create_summary_cards(self, titles) -> QFrame:
        """Create summary cards frame with enhanced styling."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border: none;
                padding: 10px 0px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        
        cards = []
        colors_list = [self.colors['success'], self.colors['accent_gold'], self.colors['accent_primary']]
        
        for idx, title in enumerate(titles):
            card = QFrame()
            accent_color = colors_list[idx % len(colors_list)]
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {self.colors['secondary_bg']};
                    border-radius: 10px;
                    border-left: 5px solid {accent_color};
                    padding: 20px 25px;
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(8)
            card_layout.setContentsMargins(0, 0, 0, 0)
            
            title_label = QLabel(title)
            title_label.setStyleSheet(f"""
                color: {self.colors['text_secondary']}; 
                font-size: 13px; 
                font-weight: 500;
                letter-spacing: 0.5px;
            """)
            card_layout.addWidget(title_label)
            
            value_label = QLabel("₹0.00")
            value_label.setStyleSheet(f"""
                color: {accent_color}; 
                font-size: 24px; 
                font-weight: bold;
                letter-spacing: 0.5px;
            """)
            value_label.setProperty('summary_value', True)
            card_layout.addWidget(value_label)
            
            layout.addWidget(card, 1)
            cards.append(card)
        
        return frame
    
    def _update_summary_cards(self, frame, values):
        """Update summary card values."""
        cards = frame.findChildren(QFrame)
        for i, card in enumerate(cards):
            if i < len(values):
                for label in card.findChildren(QLabel):
                    if label.property('summary_value'):
                        label.setText(values[i])
                        break
    
    def _export_report(self, report_type, format):
        """Export report to PDF or Excel."""
        try:
            if format == 'excel':
                filename, _ = QFileDialog.getSaveFileName(
                    self,
                    f"Export {report_type.title()} Report",
                    f"{report_type}_report.csv",
                    "CSV Files (*.csv);;All Files (*.*)"
                )
                
                if filename:
                    # Get the appropriate table based on report type
                    table = getattr(self, f"{report_type}_table", None)
                    if not table:
                        QMessageBox.warning(self, "Export", "No data to export")
                        return
                    
                    # Export to CSV
                    with open(filename, 'w', encoding='utf-8') as f:
                        # Headers
                        headers = []
                        for col in range(table.columnCount()):
                            headers.append(table.horizontalHeaderItem(col).text())
                        f.write(','.join(headers) + '\n')
                        
                        # Data
                        for row in range(table.rowCount()):
                            row_data = []
                            for col in range(table.columnCount()):
                                item = table.item(row, col)
                                row_data.append(item.text() if item else '')
                            f.write(','.join(row_data) + '\n')
                    
                    QMessageBox.information(self, "Success", f"Report exported successfully!\n{filename}")
            
            else:  # PDF
                QMessageBox.information(self, "Export PDF", "PDF export feature coming soon!")
        
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export report:\n{str(e)}")
    
    def _create_cash_transactions_view(self) -> QWidget:
        """Create Cash Transactions view to track payments and receipts."""
        container = QWidget()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("💵 Cash Transactions Report")
        header.setStyleSheet(f"QLabel {{ color: {self.colors['accent_primary']}; font-size: 22px; font-weight: bold; }}")
        layout.addWidget(header)
        
        # Description
        desc = QLabel("Track who paid cash and who received cash payments")
        desc.setStyleSheet(f"QLabel {{ color: {self.colors['text_secondary']}; font-size: 14px; margin-bottom: 10px; }}")
        layout.addWidget(desc)
        
        # Filters
        filters = self._create_common_filters()
        layout.addWidget(filters)
        
        # Summary Cards
        self.cash_summary_frame = self._create_summary_cards(['Total Cash Received', 'Total Cash Paid', 'Net Cash Flow'])
        layout.addWidget(self.cash_summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pdf_btn.clicked.connect(lambda: self._export_report('cash_transactions', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(lambda: self._export_report('cash_transactions', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.cash_transactions_table = QTableWidget(0, 8)
        self.cash_transactions_table.setHorizontalHeaderLabels([
            "Date", "Invoice #", "Customer (Payer)", "Contact", "Cash Received", "Cash Paid", "Balance", "Status"
        ])
        # Configure with optimal column widths
        self._configure_table(self.cash_transactions_table, {
            0: 100,  # Date
            1: 140,  # Invoice #
            2: 'stretch',  # Customer (Payer)
            3: 120,  # Contact
            4: 130,  # Cash Received
            5: 120,  # Cash Paid
            6: 120,  # Balance
            7: 110   # Status
        })
        self.cash_transactions_table.setMinimumHeight(500)
        layout.addWidget(self.cash_transactions_table)
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
        
        return container
    
    def _populate_cash_transactions(self):
        """Populate cash transactions with filtered data showing who paid/received cash."""
        filtered_invoices = self._apply_filters(self.all_invoices)
        
        self.cash_transactions_table.setRowCount(0)
        
        # Check if no records found
        if not filtered_invoices:
            self._show_no_records_message("Cash Transactions")
            # Update summary with zeros
            self._update_summary_cards(self.cash_summary_frame, [
                "₹0.00",
                "₹0.00",
                "₹0.00"
            ])
            return
        
        total_received = 0.0
        total_paid = 0.0
        
        for invoice in filtered_invoices:
            row = self.cash_transactions_table.rowCount()
            self.cash_transactions_table.insertRow(row)
            
            # Date
            self.cash_transactions_table.setItem(row, 0, QTableWidgetItem(invoice.get('invoice_date', '')))
            
            # Invoice #
            self.cash_transactions_table.setItem(row, 1, QTableWidgetItem(invoice.get('invoice_number', '')))
            
            # Customer (Payer)
            customer_name = invoice.get('customer_name', 'N/A')
            self.cash_transactions_table.setItem(row, 2, QTableWidgetItem(customer_name))
            
            # Contact
            self.cash_transactions_table.setItem(row, 3, QTableWidgetItem(invoice.get('contact_number', '')))
            
            # Cash Received (amount customer paid)
            received_str = str(invoice.get('received', '₹0.00')).replace('₹', '').replace(',', '').strip()
            try:
                received_amt = float(received_str)
            except:
                received_amt = 0.0
            total_received += received_amt
            
            received_item = QTableWidgetItem(f"₹{received_amt:,.2f}")
            received_item.setForeground(QColor(self.colors['success']))
            self.cash_transactions_table.setItem(row, 4, received_item)
            
            # Cash Paid (supplier amounts - what we paid out)
            paid_amt = sum(item.get('supplier_amount', 0.0) for item in invoice.get('items', []))
            total_paid += paid_amt
            
            paid_item = QTableWidgetItem(f"₹{paid_amt:,.2f}")
            paid_item.setForeground(QColor(self.colors['danger']))
            self.cash_transactions_table.setItem(row, 5, paid_item)
            
            # Balance (what customer owes)
            balance_str = str(invoice.get('balance', '₹0.00')).replace('₹', '').replace(',', '').strip()
            try:
                balance_amt = float(balance_str)
            except:
                balance_amt = 0.0
            
            balance_item = QTableWidgetItem(f"₹{balance_amt:,.2f}")
            if balance_amt > 0:
                balance_item.setForeground(QColor(self.colors['accent_gold']))
            else:
                balance_item.setForeground(QColor(self.colors['text_secondary']))
            self.cash_transactions_table.setItem(row, 6, balance_item)
            
            # Status
            if balance_amt <= 0:
                status = '✅ Paid'
                color = self.colors['success']
            else:
                status = '⏳ Pending'
                color = self.colors['danger']
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(color))
            self.cash_transactions_table.setItem(row, 7, status_item)
        
        # Calculate net cash flow
        net_cash_flow = total_received - total_paid
        
        # Update summary
        self._update_summary_cards(self.cash_summary_frame, [
            f"₹{total_received:,.2f}",
            f"₹{total_paid:,.2f}",
            f"₹{net_cash_flow:,.2f}"
        ])
    
    def _create_balance_report_view(self) -> QWidget:
        """Create Balance Report view showing comprehensive balance and payment tracking."""
        container = QWidget()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("⚖️ Balance Report")
        header.setStyleSheet(f"QLabel {{ color: {self.colors['accent_primary']}; font-size: 22px; font-weight: bold; }}")
        layout.addWidget(header)
        
        # Description
        desc = QLabel("Comprehensive overview of balances, payments received, and amounts outstanding")
        desc.setStyleSheet(f"QLabel {{ color: {self.colors['text_secondary']}; font-size: 14px; margin-bottom: 10px; }}")
        layout.addWidget(desc)
        
        # Filters
        filters = self._create_common_filters()
        layout.addWidget(filters)
        
        # Summary Cards
        self.balance_summary_frame = self._create_summary_cards(['Total Outstanding', 'Total Received', 'Total Sales'])
        layout.addWidget(self.balance_summary_frame)
        
        # Export buttons
        export_row = QHBoxLayout()
        export_row.addStretch()
        
        pdf_btn = QPushButton("📄 Export PDF")
        pdf_btn.setStyleSheet(self.get_button_style('add'))
        pdf_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pdf_btn.clicked.connect(lambda: self._export_report('balance_report', 'pdf'))
        export_row.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 Export Excel")
        excel_btn.setStyleSheet(self.get_button_style('add'))
        excel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        excel_btn.clicked.connect(lambda: self._export_report('balance_report', 'excel'))
        export_row.addWidget(excel_btn)
        
        layout.addLayout(export_row)
        
        # Table
        self.balance_table = QTableWidget(0, 8)
        self.balance_table.setHorizontalHeaderLabels([
            "Customer Name", "Contact", "Total Amount", "Amount Paid", "Balance Due", "% Paid", "Status", "Last Invoice Date"
        ])
        # Configure with optimal column widths
        self._configure_table(self.balance_table, {
            0: 'stretch',  # Customer Name
            1: 120,  # Contact
            2: 140,  # Total Amount
            3: 130,  # Amount Paid
            4: 130,  # Balance Due
            5: 90,   # % Paid
            6: 120,  # Status
            7: 130   # Last Invoice Date
        })
        self.balance_table.setMinimumHeight(500)
        layout.addWidget(self.balance_table)
        
        scroll.setWidget(content)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll)
        
        return container
    
    def _populate_balance_report(self):
        """Populate balance report with comprehensive payment tracking by customer."""
        filtered_invoices = self._apply_filters(self.all_invoices)
        
        self.balance_table.setRowCount(0)
        
        # Check if no records found
        if not filtered_invoices:
            self._show_no_records_message("Balance Report")
            # Update summary with zeros
            self._update_summary_cards(self.balance_summary_frame, [
                "₹0.00",
                "₹0.00",
                "₹0.00"
            ])
            return
        
        # Group by customer
        customer_data = {}
        
        for invoice in filtered_invoices:
            customer_name = invoice.get('customer_name', 'Unknown')
            contact = invoice.get('contact_number', '')
            invoice_date = invoice.get('invoice_date', '')
            
            # Parse amounts
            total_str = str(invoice.get('total', '₹0.00')).replace('₹', '').replace(',', '').strip()
            received_str = str(invoice.get('received', '₹0.00')).replace('₹', '').replace(',', '').strip()
            balance_str = str(invoice.get('balance', '₹0.00')).replace('₹', '').replace(',', '').strip()
            
            try:
                total_amt = float(total_str)
            except:
                total_amt = 0.0
            
            try:
                received_amt = float(received_str)
            except:
                received_amt = 0.0
            
            try:
                balance_amt = float(balance_str)
            except:
                balance_amt = 0.0
            
            # Initialize or update customer data
            if customer_name not in customer_data:
                customer_data[customer_name] = {
                    'contact': contact,
                    'total': 0.0,
                    'received': 0.0,
                    'balance': 0.0,
                    'last_date': invoice_date
                }
            
            customer_data[customer_name]['total'] += total_amt
            customer_data[customer_name]['received'] += received_amt
            customer_data[customer_name]['balance'] += balance_amt
            
            # Update last invoice date (assuming later dates come later)
            if invoice_date > customer_data[customer_name]['last_date']:
                customer_data[customer_name]['last_date'] = invoice_date
        
        # Populate table
        grand_total = 0.0
        grand_received = 0.0
        grand_balance = 0.0
        
        for customer_name, data in sorted(customer_data.items()):
            row = self.balance_table.rowCount()
            self.balance_table.insertRow(row)
            
            # Customer Name
            self.balance_table.setItem(row, 0, QTableWidgetItem(customer_name))
            
            # Contact
            self.balance_table.setItem(row, 1, QTableWidgetItem(data['contact']))
            
            # Total Amount
            total_item = QTableWidgetItem(f"₹{data['total']:,.2f}")
            total_item.setForeground(QColor(self.colors['text_primary']))
            self.balance_table.setItem(row, 2, total_item)
            
            # Amount Paid
            received_item = QTableWidgetItem(f"₹{data['received']:,.2f}")
            received_item.setForeground(QColor(self.colors['success']))
            self.balance_table.setItem(row, 3, received_item)
            
            # Balance Due
            balance_item = QTableWidgetItem(f"₹{data['balance']:,.2f}")
            if data['balance'] > 0:
                balance_item.setForeground(QColor(self.colors['danger']))
            else:
                balance_item.setForeground(QColor(self.colors['text_secondary']))
            self.balance_table.setItem(row, 4, balance_item)
            
            # % Paid
            if data['total'] > 0:
                percent_paid = (data['received'] / data['total']) * 100
            else:
                percent_paid = 0.0
            
            percent_item = QTableWidgetItem(f"{percent_paid:.1f}%")
            if percent_paid >= 100:
                percent_item.setForeground(QColor(self.colors['success']))
            elif percent_paid >= 50:
                percent_item.setForeground(QColor(self.colors['accent_gold']))
            else:
                percent_item.setForeground(QColor(self.colors['danger']))
            self.balance_table.setItem(row, 5, percent_item)
            
            # Status
            if data['balance'] <= 0:
                status = '✅ Fully Paid'
                color = self.colors['success']
            elif data['received'] > 0:
                status = '🟡 Partial'
                color = self.colors['accent_gold']
            else:
                status = '🔴 Unpaid'
                color = self.colors['danger']
            
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(color))
            self.balance_table.setItem(row, 6, status_item)
            
            # Last Invoice Date
            self.balance_table.setItem(row, 7, QTableWidgetItem(data['last_date']))
            
            # Update grand totals
            grand_total += data['total']
            grand_received += data['received']
            grand_balance += data['balance']
        
        # Update summary
        self._update_summary_cards(self.balance_summary_frame, [
            f"₹{grand_balance:,.2f}",
            f"₹{grand_received:,.2f}",
            f"₹{grand_total:,.2f}"
        ])
