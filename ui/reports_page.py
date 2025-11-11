from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QFrame,
                             QDateEdit, QGridLayout, QHeaderView, QComboBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from database.db_manager import DatabaseManager
from datetime import datetime, timedelta

class ReportsPage(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_reports()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("📊 Reports & Analytics")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_reports)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Date filter section
        filter_section = self.create_filter_section()
        layout.addWidget(filter_section)
        
        # Summary cards
        summary_section = self.create_summary_cards()
        layout.addWidget(summary_section)
        
        # Sales table
        table_section = self.create_table_section()
        layout.addWidget(table_section, 1)
    
    def create_filter_section(self):
        """Create date filter section"""
        section = QFrame()
        section.setObjectName("card")
        
        layout = QHBoxLayout(section)
        
        # Date range label
        range_label = QLabel("Date Range:")
        range_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(range_label)
        
        # Quick filters
        today_btn = QPushButton("Today")
        today_btn.setObjectName("secondaryBtn")
        today_btn.clicked.connect(lambda: self.apply_quick_filter('today'))
        layout.addWidget(today_btn)
        
        week_btn = QPushButton("This Week")
        week_btn.setObjectName("secondaryBtn")
        week_btn.clicked.connect(lambda: self.apply_quick_filter('week'))
        layout.addWidget(week_btn)
        
        month_btn = QPushButton("This Month")
        month_btn.setObjectName("secondaryBtn")
        month_btn.clicked.connect(lambda: self.apply_quick_filter('month'))
        layout.addWidget(month_btn)
        
        all_btn = QPushButton("All Time")
        all_btn.setObjectName("secondaryBtn")
        all_btn.clicked.connect(lambda: self.apply_quick_filter('all'))
        layout.addWidget(all_btn)
        
        layout.addSpacing(20)
        
        # Custom date range
        from_label = QLabel("From:")
        layout.addWidget(from_label)
        
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate().addMonths(-1))
        self.from_date.setDisplayFormat("dd-MM-yyyy")
        layout.addWidget(self.from_date)
        
        to_label = QLabel("To:")
        layout.addWidget(to_label)
        
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setDisplayFormat("dd-MM-yyyy")
        layout.addWidget(self.to_date)
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.load_reports)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        
        return section
    
    def create_summary_cards(self):
        """Create summary statistics cards"""
        section = QFrame()
        layout = QGridLayout(section)
        layout.setSpacing(15)
        
        # Total Sales Card
        self.total_sales_card = self.create_stat_card("💰 Total Sales", "₹ 0.00", "#0d7377")
        layout.addWidget(self.total_sales_card, 0, 0)
        
        # Total Invoices Card
        self.total_invoices_card = self.create_stat_card("📄 Total Invoices", "0", "#2196F3")
        layout.addWidget(self.total_invoices_card, 0, 1)
        
        # Received Amount Card
        self.received_card = self.create_stat_card("✅ Received", "₹ 0.00", "#4CAF50")
        layout.addWidget(self.received_card, 0, 2)
        
        # Pending Balance Card
        self.balance_card = self.create_stat_card("⏳ Pending", "₹ 0.00", "#FF9800")
        layout.addWidget(self.balance_card, 0, 3)
        
        # Average Sale Card
        self.average_card = self.create_stat_card("📊 Average Sale", "₹ 0.00", "#9C27B0")
        layout.addWidget(self.average_card, 1, 0)
        
        return section
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(f"""
            QFrame#card {{
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 10pt; color: #a0a0a0;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("valueLabel")
        value_label.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {color};")
        layout.addWidget(value_label)
        
        # Store reference to value label
        card.value_label = value_label
        
        return card
    
    def create_table_section(self):
        """Create recent invoices table section"""
        section = QFrame()
        section.setObjectName("card")
        
        layout = QVBoxLayout(section)
        
        # Title
        title = QLabel("📋 Recent Invoices")
        title.setObjectName("sectionLabel")
        layout.addWidget(title)
        
        # Table
        self.invoices_table = QTableWidget()
        self.invoices_table.setColumnCount(6)
        self.invoices_table.setHorizontalHeaderLabels([
            "Invoice #", "Customer", "Date", "Total (₹)", "Received (₹)", "Balance (₹)"
        ])
        
        # Set column widths
        header = self.invoices_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.invoices_table.setAlternatingRowColors(True)
        self.invoices_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.invoices_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.invoices_table)
        
        return section
    
    def apply_quick_filter(self, filter_type):
        """Apply quick date filters"""
        today = QDate.currentDate()
        
        if filter_type == 'today':
            self.from_date.setDate(today)
            self.to_date.setDate(today)
        elif filter_type == 'week':
            # Start of week (Monday)
            days_since_monday = (today.dayOfWeek() - 1) % 7
            start_of_week = today.addDays(-days_since_monday)
            self.from_date.setDate(start_of_week)
            self.to_date.setDate(today)
        elif filter_type == 'month':
            # Start of month
            start_of_month = QDate(today.year(), today.month(), 1)
            self.from_date.setDate(start_of_month)
            self.to_date.setDate(today)
        elif filter_type == 'all':
            # All time - set from date to 1 year ago
            self.from_date.setDate(today.addYears(-1))
            self.to_date.setDate(today)
        
        self.load_reports()
    
    def load_reports(self):
        """Load and display reports"""
        try:
            # Get date range
            from_date_str = self.from_date.date().toString("yyyy-MM-dd")
            to_date_str = self.to_date.date().toString("yyyy-MM-dd")
            
            # Get summary
            summary = self.db.get_sales_summary(from_date_str, to_date_str)
            
            # Update summary cards
            self.total_sales_card.value_label.setText(f"₹ {summary['total_sales']:,.2f}")
            self.total_invoices_card.value_label.setText(str(summary['total_invoices']))
            self.received_card.value_label.setText(f"₹ {summary['total_received']:,.2f}")
            self.balance_card.value_label.setText(f"₹ {summary['total_balance']:,.2f}")
            self.average_card.value_label.setText(f"₹ {summary['average_sale']:,.2f}")
            
            # Load invoices
            invoices = self.db.get_all_invoices(limit=100)
            
            # Filter by date range
            filtered_invoices = []
            for inv in invoices:
                inv_date = datetime.strptime(inv['invoice_date'], '%Y-%m-%d').date()
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
                
                if from_date <= inv_date <= to_date:
                    filtered_invoices.append(inv)
            
            # Populate table
            self.invoices_table.setRowCount(0)
            for inv in filtered_invoices:
                row_position = self.invoices_table.rowCount()
                self.invoices_table.insertRow(row_position)
                
                # Invoice number
                self.invoices_table.setItem(row_position, 0, 
                    QTableWidgetItem(inv['invoice_number']))
                
                # Customer
                self.invoices_table.setItem(row_position, 1, 
                    QTableWidgetItem(inv['customer_name']))
                
                # Date
                date_obj = datetime.strptime(inv['invoice_date'], '%Y-%m-%d')
                date_str = date_obj.strftime('%d-%m-%Y')
                self.invoices_table.setItem(row_position, 2, 
                    QTableWidgetItem(date_str))
                
                # Total
                total_item = QTableWidgetItem(f"₹ {inv['total_amount']:,.2f}")
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.invoices_table.setItem(row_position, 3, total_item)
                
                # Received
                received_item = QTableWidgetItem(f"₹ {inv['received_amount']:,.2f}")
                received_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.invoices_table.setItem(row_position, 4, received_item)
                
                # Balance
                balance_item = QTableWidgetItem(f"₹ {inv['balance']:,.2f}")
                balance_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                
                # Color code balance
                if inv['balance'] > 0:
                    balance_item.setForeground(Qt.GlobalColor.yellow)
                else:
                    balance_item.setForeground(Qt.GlobalColor.green)
                
                self.invoices_table.setItem(row_position, 5, balance_item)
            
        except Exception as e:
            print(f"Error loading reports: {e}")
