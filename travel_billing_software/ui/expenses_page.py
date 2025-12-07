"""
Expenses Management Page Module
Record and manage all daily business expenses with automatic report integration.
"""
import os
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QTableWidget, QPushButton,
                             QLineEdit, QTableWidgetItem, QMessageBox, 
                             QFileDialog, QHeaderView, QDialog, QTextEdit,
                             QFormLayout, QDialogButtonBox, QComboBox, QDoubleSpinBox,
                             QDateEdit, QCalendarWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont
from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.utils.custom_widgets import NoWheelDoubleSpinBox
from travel_billing_software.config.config import format_currency, get_currency_symbol


class ExpenseDialog(QDialog):
    """Dialog for adding/editing expense details."""
    
    def __init__(self, colors, get_input_style, get_button_style, expense_data=None, parent=None):
        super().__init__(parent)
        self.colors = colors
        self.get_input_style = get_input_style
        self.get_button_style = get_button_style
        self.expense_data = expense_data
        
        self.setWindowTitle("Add Expense" if not expense_data else "Edit Expense")
        self.setModal(True)
        self.setMinimumWidth(550)
        
        self._init_ui()
        
        if expense_data:
            self._populate_fields()
    
    def _init_ui(self):
        """Initialize dialog UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel("Expense Details")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
        """)
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Expense Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setStyleSheet(self.get_input_style() + """
            QDateEdit {
                padding: 10px;
                font-size: 16px;
            }
        """)
        form_layout.addRow("Expense Date: *", self.date_input)
        
        # Expense Category
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems([
            "Office Rent",
            "Utilities (Electricity, Water)",
            "Internet & Phone",
            "Staff Salaries",
            "Travel & Transportation",
            "Meals & Entertainment",
            "Office Supplies",
            "Marketing & Advertising",
            "Software & Subscriptions",
            "Bank Charges",
            "Professional Fees",
            "Repairs & Maintenance",
            "Insurance",
            "Taxes & Licenses",
            "Fuel",
            "Vehicle Maintenance",
            "Commission Paid",
            "Printing & Stationery",
            "Postage & Courier",
            "Miscellaneous"
        ])
        self.category_input.setStyleSheet(self.get_input_style() + """
            QComboBox {
                padding: 10px;
                font-size: 16px;
            }
        """)
        form_layout.addRow("Category: *", self.category_input)
        
        # Amount
        self.amount_input = NoWheelDoubleSpinBox()
        self.amount_input.setRange(0, 9999999)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix(f"{get_currency_symbol()} ")
        self.amount_input.setStyleSheet(self.get_input_style() + """
            QDoubleSpinBox {
                padding: 10px;
                font-size: 16px;
            }
        """)
        form_layout.addRow("Amount: *", self.amount_input)
        
        # Payment Method
        self.payment_method = QComboBox()
        self.payment_method.addItems([
            "Cash",
            "Bank Transfer",
            "Credit Card",
            "Debit Card",
            "UPI/Digital Wallet",
            "Cheque",
            "Net Banking"
        ])
        self.payment_method.setStyleSheet(self.get_input_style() + """
            QComboBox {
                padding: 10px;
                font-size: 16px;
            }
        """)
        form_layout.addRow("Payment Method: *", self.payment_method)
        
        # Paid To / Vendor
        self.vendor_input = QLineEdit()
        self.vendor_input.setPlaceholderText("Enter vendor/payee name")
        self.vendor_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Paid To:", self.vendor_input)
        
        # Person Responsible
        self.responsible_person = QLineEdit()
        self.responsible_person.setPlaceholderText("Enter person's name")
        self.responsible_person.setStyleSheet(self.get_input_style())
        form_layout.addRow("Person Responsible:", self.responsible_person)
        
        # Reference Number
        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("Invoice/Receipt reference")
        self.reference_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Reference Number:", self.reference_input)
        
        # Description/Notes
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Add detailed description or notes")
        self.description_input.setMaximumHeight(100)
        self.description_input.setStyleSheet(self.get_input_style())
        form_layout.addRow("Description:", self.description_input)
        
        layout.addLayout(form_layout)
        
        # Required fields note
        required_note = QLabel("* Required fields")
        required_note.setStyleSheet(f"color: {self.colors['danger']}; font-size: 13px; font-style: italic;")
        layout.addWidget(required_note)
        
        # Buttons
        button_box = QDialogButtonBox()
        save_btn = QPushButton("💾 Save Expense")
        save_btn.setStyleSheet(self.get_button_style('add'))
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("✖ Cancel")
        cancel_btn.setStyleSheet(self.get_button_style('cancel'))
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addButton(save_btn, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton(cancel_btn, QDialogButtonBox.ButtonRole.RejectRole)
        
        layout.addWidget(button_box)
    
    def _populate_fields(self):
        """Populate fields with existing expense data."""
        # Parse date
        date_str = self.expense_data.get('date', '')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                self.date_input.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
            except:
                pass
        
        self.category_input.setCurrentText(self.expense_data.get('category', ''))
        self.amount_input.setValue(self.expense_data.get('amount', 0.0))
        
        payment_mode = self.expense_data.get('payment_mode', 'Cash')
        index = self.payment_method.findText(payment_mode)
        if index >= 0:
            self.payment_method.setCurrentIndex(index)
        
        self.vendor_input.setText(self.expense_data.get('vendor', ''))
        self.responsible_person.setText(self.expense_data.get('responsible_person', ''))
        self.reference_input.setText(self.expense_data.get('reference', ''))
        self.description_input.setPlainText(self.expense_data.get('description', ''))
    
    def get_expense_data(self):
        """Get expense data from form fields."""
        category = self.category_input.currentText().strip()
        amount = self.amount_input.value()
        payment_mode = self.payment_method.currentText()
        
        if not category:
            QMessageBox.warning(self, "Validation Error", "Expense category is required!")
            return None
        
        if amount <= 0:
            QMessageBox.warning(self, "Validation Error", "Amount must be greater than zero!")
            return None
        
        return {
            'id': self.expense_data.get('id') if self.expense_data else str(datetime.now().timestamp()),
            'date': self.date_input.date().toString("yyyy-MM-dd"),
            'category': category,
            'amount': amount,
            'payment_mode': payment_mode,
            'vendor': self.vendor_input.text().strip(),
            'responsible_person': self.responsible_person.text().strip(),
            'reference': self.reference_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'created_date': self.expense_data.get('created_date') if self.expense_data else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'modified_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


class ExpensesPage(QWidget):
    """Comprehensive Expenses Management Page."""
    
    def __init__(self, colors, get_table_style, get_button_style, get_input_style, parent=None):
        super().__init__()
        self.colors = colors
        self.get_table_style = get_table_style
        self.get_button_style = get_button_style
        self.get_input_style = get_input_style
        self.parent_window = parent
        
        # Database connection
        self.db = get_db_instance()
        self.expenses = []
        self._load_expenses()
        
        self._init_ui()
        self._populate_table()
    
    def _init_ui(self):
        """Initialize the UI."""
        # Main layout - no scroll area for responsive fit
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        
        # Header Section - Compact
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)
        
        title = QLabel("💰 Expenses Management")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Track and manage all daily business expenses")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 13px;
            }}
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Add spacing before action bar
        layout.addSpacing(12)
        
        # Action Bar
        action_bar = QFrame()
        from PyQt6.QtWidgets import QSizePolicy
        action_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        action_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 15px;
                margin: 8px 0px;
            }}
        """)
        action_layout = QHBoxLayout(action_bar)
        action_layout.setSpacing(12)
        
        # Date Filter Section
        date_label = QLabel("Filter by Date:")
        date_label.setStyleSheet(f"""
            color: {self.colors['text_primary']}; 
            font-weight: bold;
            font-size: 14px;
        """)
        action_layout.addWidget(date_label)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setDisplayFormat("dd/MM/yyyy")
        self.start_date.setStyleSheet(self.get_input_style() + """
            QDateEdit {
                padding: 10px 12px;
                font-size: 14px;
                min-width: 140px;
                min-height: 38px;
            }
        """)
        self.start_date.dateChanged.connect(self._filter_expenses)
        action_layout.addWidget(self.start_date)
        
        to_label = QLabel("to")
        to_label.setStyleSheet(f"""
            color: {self.colors['text_secondary']};
            font-size: 14px;
        """)
        action_layout.addWidget(to_label)
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setDisplayFormat("dd/MM/yyyy")
        self.end_date.setStyleSheet(self.get_input_style() + """
            QDateEdit {
                padding: 10px 12px;
                font-size: 14px;
                min-width: 140px;
                min-height: 38px;
            }
        """)
        self.end_date.dateChanged.connect(self._filter_expenses)
        action_layout.addWidget(self.end_date)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by category, vendor, or description...")
        self.search_input.setStyleSheet(self.get_input_style() + """
            QLineEdit {
                padding: 10px 15px;
                font-size: 14px;
                min-width: 300px;
                min-height: 38px;
            }
        """)
        self.search_input.textChanged.connect(self._filter_expenses)
        action_layout.addWidget(self.search_input)
        
        action_layout.addStretch()
        
        # Add Expense Button
        add_btn = QPushButton("✚ Add New Expense")
        add_btn.setStyleSheet(self.get_button_style('add') + """
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
                min-height: 38px;
            }
        """)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self._add_expense)
        action_layout.addWidget(add_btn)
        
        # Export Button
        export_btn = QPushButton("📊 Export to CSV")
        export_btn.setStyleSheet(self.get_button_style('primary') + """
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                min-height: 38px;
            }
        """)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.clicked.connect(self._export_expenses)
        action_layout.addWidget(export_btn)
        
        layout.addWidget(action_bar)
        
        # Add spacing between action bar and stats cards
        layout.addSpacing(20)
        
        # Statistics Cards
        stats_frame = QFrame()
        stats_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(8)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        
        self.total_expenses_label = self._create_stat_card("Total Expenses", format_currency(0), self.colors['danger'])
        self.expense_count_label = self._create_stat_card("Number of Expenses", "0", self.colors['accent_primary'])
        self.avg_expense_label = self._create_stat_card("Average Expense", format_currency(0), self.colors['accent_secondary'])
        self.cash_expenses_label = self._create_stat_card("Cash Expenses", format_currency(0), self.colors['success'])
        
        stats_layout.addWidget(self.total_expenses_label)
        stats_layout.addWidget(self.expense_count_label)
        stats_layout.addWidget(self.avg_expense_label)
        stats_layout.addWidget(self.cash_expenses_label)
        
        layout.addWidget(stats_frame)
        
        # Add spacing between stats cards and table
        layout.addSpacing(15)
        
        # Expenses Table
        table_frame = QFrame()
        table_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #1A1A1A;
                border-radius: 8px;
                border: 1.2px solid #333333;
                padding: 0px;
                margin: 0px;
            }}
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(6, 6, 6, 6)
        table_layout.setSpacing(4)

        # Table title with clean styling
        table_title = QLabel("📋 Expense Records")
        table_title.setStyleSheet(f"""
            QLabel {{
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
                padding: 2px 0px;
                background-color: transparent;
                border: none;
            }}
        """)
        table_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        table_layout.addWidget(table_title)

        # Create table with 6 columns (Date, Category, Amount, Payment Method, Actions, ID)
        self.expenses_table = QTableWidget(0, 6)
        self.expenses_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Configure table
        self._configure_table()
        
        # Add table to layout with stretch factor for full expansion
        table_layout.addWidget(self.expenses_table, 1)

        # Add table frame to main layout with maximum stretch for responsiveness
        layout.addWidget(table_frame, 1)
        
        # Update statistics
        self._update_statistics()
    
    def _create_stat_card(self, title, value, color):
        """Create a statistics card."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 18px;
                min-height: 40px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(12, 12, 12, 12)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 14px;
                font-weight: 600;
            }}
        """)
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 28px;
                font-weight: bold;
            }}
        """)
        value_label.setProperty('stat_value', True)
        card_layout.addWidget(value_label)
        
        return card
    
    def _configure_table(self):
        """Configure table appearance and behavior."""
        # Set column headers - only showing essential columns
        self.expenses_table.setHorizontalHeaderLabels([
            "Date", "Category", "Amount", "Payment Method", "Actions", "ID"
        ])
        
        # Enable sorting
        self.expenses_table.setSortingEnabled(True)

        # Configure header for full-width expansion
        header = self.expenses_table.horizontalHeader()
        header.setVisible(True)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setMinimumHeight(45)
        header.setMaximumHeight(45)
        
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #202020;
                color: #FFFFFF;
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #444444;
                padding: 8px;
                text-align: center;
                min-height: 45px;
            }
            QHeaderView::section:hover {
                background-color: #2A2A2A;
            }
        """)

        # Set minimum column widths and resize modes for responsive layout
        from PyQt6.QtWidgets import QHeaderView
        
        column_config = {
            0: (120, QHeaderView.ResizeMode.Interactive),    # Date
            1: (200, QHeaderView.ResizeMode.Stretch),        # Category
            2: (150, QHeaderView.ResizeMode.Interactive),    # Amount
            3: (150, QHeaderView.ResizeMode.Interactive),    # Payment Method
            4: (150, QHeaderView.ResizeMode.Interactive),    # Actions
            5: (0, None)                                     # ID (hidden)
        }

        for col, (min_width, resize_mode) in column_config.items():
            if min_width == 0:
                self.expenses_table.setColumnHidden(col, True)
            else:
                self.expenses_table.setColumnWidth(col, min_width)
                if resize_mode:
                    header.setSectionResizeMode(col, resize_mode)

        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        header.setSectionsClickable(True)

        # Configure vertical header with increased row height
        self.expenses_table.verticalHeader().setVisible(True)
        self.expenses_table.verticalHeader().setDefaultSectionSize(45)

        # Table styling - Clean dark theme with taller rows
        self.expenses_table.setAlternatingRowColors(True)
        self.expenses_table.setStyleSheet(self.get_table_style() + f"""
            QTableWidget {{
                background-color: #1E1E1E;
                gridline-color: #444444;
                font-size: 13px;
                selection-background-color: #2A2A2A;
                selection-color: #FFFFFF;
                color: #FFFFFF;
                border: 1.2px solid #FFFFFF;
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                border: none;
                background-color: #1E1E1E;
                color: #FFFFFF;
            }}
            QTableWidget::item:alternate {{
                background-color: #161616;
                color: #FFFFFF;
            }}
            QTableWidget::item:selected {{
                background-color: #2A2A2A;
                color: #FFFFFF;
            }}
            QTableWidget::item:hover {{
                background-color: #252525;
            }}
        """)

        self.expenses_table.setMinimumHeight(500)
        
        self.expenses_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.expenses_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    def _load_expenses(self):
        """Load expenses from database."""
        try:
            self.expenses = self.db.get_all_expenses()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load expenses:\n{str(e)}")
            self.expenses = []
    
    def refresh_data(self):
        """Refresh expenses data from database."""
        self._load_expenses()
        self._populate_table()
    
    def refresh_ui(self):
        """Refresh UI elements to reflect updated configuration (e.g., currency changes)."""
        try:
            # Reload data which will update all currency displays
            self.refresh_data()
        except Exception as e:
            print(f"Error refreshing expenses page UI: {e}")
        
    def _save_expenses(self):
        """Save expenses is now handled by individual add/update operations."""
        return True  # No-op, kept for compatibility
    
    def _populate_table(self, expenses_list=None):
        """Populate table with expenses."""
        if expenses_list is None:
            expenses_list = self.expenses
        
        self.expenses_table.setRowCount(0)
        self.expenses_table.setSortingEnabled(False)
        
        for expense in expenses_list:
            row = self.expenses_table.rowCount()
            self.expenses_table.insertRow(row)
            
            # Date
            date_str = expense.get('date', '')
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%d-%m-%Y')
                except:
                    formatted_date = date_str
            else:
                formatted_date = 'N/A'
            date_item = QTableWidgetItem(formatted_date)
            date_item.setFont(QFont('Arial', 13, QFont.Weight.Bold))
            self.expenses_table.setItem(row, 0, date_item)
            
            # Category
            category_item = QTableWidgetItem(expense.get('category', ''))
            category_item.setForeground(QColor(self.colors['accent_primary']))
            category_item.setFont(QFont('Arial', 13, QFont.Weight.Bold))
            self.expenses_table.setItem(row, 1, category_item)
            
            # Amount
            amount = expense.get('amount', 0.0)
            amount_item = QTableWidgetItem(format_currency(amount))
            amount_item.setForeground(QColor(self.colors['danger']))
            amount_item.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            self.expenses_table.setItem(row, 2, amount_item)
            
            # Payment Method
            payment_item = QTableWidgetItem(expense.get('payment_mode', 'Cash'))
            if expense.get('payment_mode', '').upper() == 'CASH':
                payment_item.setForeground(QColor(self.colors['success']))
            else:
                payment_item.setForeground(QColor(self.colors['accent_secondary']))
            self.expenses_table.setItem(row, 3, payment_item)
            
            # Actions
            actions_widget = self._create_action_buttons(expense)
            self.expenses_table.setCellWidget(row, 4, actions_widget)
            
            # ID (hidden)
            self.expenses_table.setItem(row, 5, QTableWidgetItem(expense.get('id', '')))
        
        self.expenses_table.setSortingEnabled(True)
        self._update_statistics(expenses_list)
    
    def _create_action_buttons(self, expense):
        """Create action buttons for each row."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # View Button
        view_btn = QPushButton("👁️")
        view_btn.setToolTip("View Details")
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a8eef;
            }
        """)
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.clicked.connect(lambda: self._view_expense(expense))
        layout.addWidget(view_btn)
        
        # Edit Button
        edit_btn = QPushButton("✏️")
        edit_btn.setToolTip("Edit Expense")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5a623;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e59613;
            }
        """)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(lambda: self._edit_expense(expense))
        layout.addWidget(edit_btn)
        
        # Delete Button
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Delete Expense")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ee3333;
            }
        """)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda: self._delete_expense(expense))
        layout.addWidget(delete_btn)
        
        layout.addStretch()
        return widget
    
    def _add_expense(self):
        """Open dialog to add new expense."""
        dialog = ExpenseDialog(self.colors, self.get_input_style, self.get_button_style, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            expense_data = dialog.get_expense_data()
            if expense_data:
                # Add to database
                expense_id = self.db.add_expense(
                    date=expense_data['date'],
                    category=expense_data['category'],
                    amount=expense_data['amount'],
                    description=expense_data.get('description', ''),
                    payment_mode=expense_data.get('payment_mode', 'CASH'),
                    paid_to=expense_data.get('paid_to', ''),
                    person_responsible=expense_data.get('person_responsible', ''),
                    reference_number=expense_data.get('reference_number', '')
                )
                
                if expense_id > 0:
                    # Silent save - no popup (Vyapar style)
                    self._load_expenses()
                    self._populate_table()
                    self._notify_reports_update()
                else:
                    QMessageBox.critical(self, "Error", "Failed to add expense to database")
    
    def _edit_expense(self, expense):
        """Open dialog to edit expense."""
        dialog = ExpenseDialog(self.colors, self.get_input_style, self.get_button_style, 
                               expense_data=expense, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_expense_data()
            if updated_data:
                # Update in database
                success = self.db.update_expense(
                    expense_id=expense['id'],
                    date=updated_data['date'],
                    category=updated_data['category'],
                    amount=updated_data['amount'],
                    description=updated_data.get('description', ''),
                    payment_mode=updated_data.get('payment_mode', 'CASH'),
                    paid_to=updated_data.get('paid_to', ''),
                    person_responsible=updated_data.get('person_responsible', ''),
                    reference_number=updated_data.get('reference_number', '')
                )
                
                if success:
                    # Silent update - no popup
                    self._load_expenses()
                    self._populate_table()
                    self._notify_reports_update()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update expense")
    
    def _delete_expense(self, expense):
        """Delete expense after confirmation."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this expense?\n\nCategory: {expense['category']}\nAmount: {format_currency(0)}{expense['amount']:,.2f}\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Delete from database
            success = self.db.delete_expense(expense['id'])
            
            if success:
                # Silent delete - no popup
                self._load_expenses()
                self._populate_table()
                self._notify_reports_update()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete expense")
    

    def _view_expense(self, expense):
        """View expense details in a dialog."""
        from PyQt6.QtWidgets import QSizePolicy, QScrollArea
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Expense Details")
        dialog.setModal(True)
        dialog.setMinimumSize(750, 700)
        dialog.resize(800, 750)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1A1A1A;
            }
        """)

        # Main layout for dialog
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1A1A1A;
            }
        """)
        
        # Content widget inside scroll area
        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title with high contrast
        title = QLabel(f"💰 {expense.get('category', 'N/A')}")
        title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        title.setStyleSheet("""
            QLabel {
                color: #B86BFF;
                font-size: 20px;
                font-weight: 600;
                background-color: transparent;
                padding: 10px 0px;
            }
        """)
        layout.addWidget(title)

        # Amount highlight box with high visibility
        amount_label = QLabel(format_currency(expense.get('amount', 0.0)))
        amount_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        amount_label.setMinimumHeight(60)
        amount_label.setStyleSheet("""
            QLabel {
                color: #E60000;
                font-size: 26px;
                font-weight: bold;
                background-color: #FFE5E5;
                padding: 20px;
                border-radius: 10px;
                border: 2px solid #FF9999;
            }
        """)
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(amount_label)

        # Format date
        date_str = expense.get('date', '')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d %B %Y')
            except:
                formatted_date = date_str
        else:
            formatted_date = 'N/A'

        # Details frame with clear styling and full width
        details_frame = QFrame()
        details_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        details_frame.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-radius: 10px;
                border: 1px solid #444444;
            }
        """)
        details_layout = QVBoxLayout(details_frame)
        details_layout.setSpacing(12)
        details_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create detail fields with clear labels and values - ALL fields visible
        details_data = [
            ("Date", formatted_date),
            ("Category", expense.get('category', 'N/A')),
            ("Amount", format_currency(expense.get('amount', 0.0))),
            ("Payment Method", expense.get('payment_mode', 'N/A')),
            ("Vendor (Paid To)", expense.get('vendor', 'N/A')),
            ("Person Responsible", expense.get('responsible_person', 'N/A')),
            ("Reference Number", expense.get('reference', 'N/A')),
            ("Description", expense.get('description', 'N/A')),
            ("Created Date", expense.get('created_date', 'N/A')),
            ("Modified Date", expense.get('modified_date', 'N/A'))
        ]
        
        for label_text, value_text in details_data:
            # Field container with full width expansion
            field_container = QFrame()
            field_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            field_layout = QVBoxLayout(field_container)
            field_layout.setContentsMargins(0, 0, 0, 0)
            field_layout.setSpacing(6)
            
            # Label with high contrast
            label = QLabel(label_text)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            label.setStyleSheet("""
                QLabel {
                    color: #FFFFFF;
                    font-weight: bold;
                    font-size: 13px;
                    background-color: transparent;
                }
            """)
            field_layout.addWidget(label)
            
            # Value field with black background and white text
            value = QLabel(str(value_text))
            value.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            value.setMinimumHeight(40)
            value.setMaximumWidth(16777215)
            value.setStyleSheet("""
                QLabel {
                    color: #FFFFFF;
                    font-size: 13px;
                    background-color: #000000;
                    padding: 10px 15px;
                    border-radius: 6px;
                    border: 1px solid #555555;
                }
            """)
            value.setWordWrap(True)
            field_layout.addWidget(value)
            
            details_layout.addWidget(field_container)

        layout.addWidget(details_frame)
        
        # Close button with clear styling
        close_btn = QPushButton("✖ Close")
        close_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        close_btn.setMinimumWidth(200)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #B86BFF;
                color: #FFFFFF;
                border: none;
                padding: 12px 30px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A050FF;
            }
            QPushButton:pressed {
                background-color: #9030EF;
            }
        """)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(dialog.accept)
        
        # Center the close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Set content widget to scroll area
        scroll.setWidget(content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll)

        dialog.exec()
    
    def _filter_expenses(self):
        """Filter expenses based on date range and search text."""
        search_text = self.search_input.text().lower().strip()
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        
        filtered = []
        for expense in self.expenses:
            # Date filter
            expense_date_str = expense.get('date', '')
            if expense_date_str:
                try:
                    expense_date = datetime.strptime(expense_date_str, '%Y-%m-%d').date()
                    if not (start_date <= expense_date <= end_date):
                        continue
                except:
                    continue
            
            # Search filter
            if search_text:
                searchable_text = f"{expense.get('category', '')} {expense.get('vendor', '')} {expense.get('description', '')} {expense.get('responsible_person', '')}".lower()
                if search_text not in searchable_text:
                    continue
            
            filtered.append(expense)
        
        self._populate_table(filtered)
    
    def _update_statistics(self, expenses_list=None):
        """Update statistics cards."""
        if expenses_list is None:
            expenses_list = self.expenses
        
        total = sum(e.get('amount', 0.0) for e in expenses_list)
        count = len(expenses_list)
        avg = total / count if count > 0 else 0.0
        cash_total = sum(e.get('amount', 0.0) for e in expenses_list if e.get('payment_mode', '').upper() == 'CASH')
        
        # Update stat cards
        for card in [self.total_expenses_label, self.expense_count_label, 
                     self.avg_expense_label, self.cash_expenses_label]:
            for label in card.findChildren(QLabel):
                if label.property('stat_value'):
                    if card == self.total_expenses_label:
                        label.setText(format_currency(total))
                    elif card == self.expense_count_label:
                        label.setText(str(count))
                    elif card == self.avg_expense_label:
                        label.setText(format_currency(avg))
                    elif card == self.cash_expenses_label:
                        label.setText(format_currency(cash_total))
    
    def _export_expenses(self):
        """Export expenses to CSV."""
        if not self.expenses:
            QMessageBox.warning(self, "No Data", "No expenses to export!")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Expenses",
            f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if filename:
            try:
                import csv
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # Headers
                    writer.writerow([
                        'Date', 'Category', 'Amount', 'Payment Method', 'Vendor',
                        'Person Responsible', 'Reference', 'Description', 'Created Date'
                    ])
                    
                    # Data
                    for expense in self.expenses:
                        writer.writerow([
                            expense.get('date', ''),
                            expense.get('category', ''),
                            expense.get('amount', 0.0),
                            expense.get('payment_mode', ''),
                            expense.get('vendor', ''),
                            expense.get('responsible_person', ''),
                            expense.get('reference', ''),
                            expense.get('description', ''),
                            expense.get('created_date', '')
                        ])
                
                QMessageBox.information(self, "Success", f"Expenses exported successfully!\n{filename}")
            
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export expenses:\n{str(e)}")
    
    def _notify_reports_update(self):
        """Notify reports system about expense updates."""
        try:
            # This method will be called by report generation modules
            # to ensure they pull the latest expense data
            print("✅ Expense data updated - Reports will reflect changes on next view")
        except Exception as e:
            print(f"Report notification error: {e}")
    
    def get_expenses_for_period(self, start_date, end_date):
        """Get expenses for a specific period (for report generation)."""
        filtered = []
        for expense in self.expenses:
            expense_date_str = expense.get('date', '')
            if expense_date_str:
                try:
                    expense_date = datetime.strptime(expense_date_str, '%Y-%m-%d').date()
                    if start_date <= expense_date <= end_date:
                        filtered.append(expense)
                except:
                    continue
        return filtered
    
    def get_total_expenses(self, start_date=None, end_date=None):
        """Get total expenses for a period (for P&L calculations)."""
        if start_date and end_date:
            expenses = self.get_expenses_for_period(start_date, end_date)
        else:
            expenses = self.expenses
        
        return sum(e.get('amount', 0.0) for e in expenses)
