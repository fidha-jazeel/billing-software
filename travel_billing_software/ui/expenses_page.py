"""
Expenses Management Page Module
Record and manage all daily business expenses with automatic report integration.
"""
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QTableWidget, QPushButton,
                             QLineEdit, QTableWidgetItem, QMessageBox, 
                             QFileDialog, QHeaderView, QDialog, QTextEdit,
                             QFormLayout, QDialogButtonBox, QComboBox, QDoubleSpinBox,
                             QDateEdit, QCalendarWidget)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont


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
                font-size: 20px;
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
                font-size: 14px;
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
                font-size: 14px;
            }
        """)
        form_layout.addRow("Category: *", self.category_input)
        
        # Amount
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 9999999)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix("₹ ")
        self.amount_input.setStyleSheet(self.get_input_style() + """
            QDoubleSpinBox {
                padding: 10px;
                font-size: 14px;
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
                font-size: 14px;
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
        required_note.setStyleSheet(f"color: {self.colors['danger']}; font-size: 11px; font-style: italic;")
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
        
        payment_method = self.expense_data.get('payment_method', 'Cash')
        index = self.payment_method.findText(payment_method)
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
        payment_method = self.payment_method.currentText()
        
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
            'payment_method': payment_method,
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
        
        # Data file path
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'expenses')
        os.makedirs(self.data_dir, exist_ok=True)
        self.data_file = os.path.join(self.data_dir, 'expenses.json')
        
        self.expenses = []
        self._load_expenses()
        
        self._init_ui()
        self._populate_table()
    
    def _init_ui(self):
        """Initialize the UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {self.colors['primary_bg']}; }}")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header Section
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        
        title = QLabel("💰 Expenses Management")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Track and manage all daily business expenses")
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 14px;
            }}
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Action Bar
        action_bar = QFrame()
        action_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        action_layout = QHBoxLayout(action_bar)
        action_layout.setSpacing(15)
        
        # Date Filter Section
        date_label = QLabel("Filter by Date:")
        date_label.setStyleSheet(f"color: {self.colors['text_primary']}; font-weight: bold;")
        action_layout.addWidget(date_label)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setDisplayFormat("dd/MM/yyyy")
        self.start_date.setStyleSheet(self.get_input_style() + """
            QDateEdit {
                padding: 10px;
                font-size: 13px;
                min-width: 140px;
            }
        """)
        self.start_date.dateChanged.connect(self._filter_expenses)
        action_layout.addWidget(self.start_date)
        
        to_label = QLabel("to")
        to_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        action_layout.addWidget(to_label)
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setDisplayFormat("dd/MM/yyyy")
        self.end_date.setStyleSheet(self.get_input_style() + """
            QDateEdit {
                padding: 10px;
                font-size: 13px;
                min-width: 140px;
            }
        """)
        self.end_date.dateChanged.connect(self._filter_expenses)
        action_layout.addWidget(self.end_date)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by category, vendor, or description...")
        self.search_input.setStyleSheet(self.get_input_style() + """
            QLineEdit {
                padding: 12px 15px;
                font-size: 14px;
                min-width: 300px;
            }
        """)
        self.search_input.textChanged.connect(self._filter_expenses)
        action_layout.addWidget(self.search_input)
        
        action_layout.addStretch()
        
        # Add Expense Button
        add_btn = QPushButton("➕ Add New Expense")
        add_btn.setStyleSheet(self.get_button_style('add') + """
            QPushButton {
                padding: 12px 25px;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.clicked.connect(self._add_expense)
        action_layout.addWidget(add_btn)
        
        # Export Button
        export_btn = QPushButton("📊 Export to CSV")
        export_btn.setStyleSheet(self.get_button_style('primary') + """
            QPushButton {
                padding: 12px 25px;
                font-size: 14px;
            }
        """)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.clicked.connect(self._export_expenses)
        action_layout.addWidget(export_btn)
        
        layout.addWidget(action_bar)
        
        # Statistics Cards
        stats_frame = QFrame()
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(20)
        
        self.total_expenses_label = self._create_stat_card("Total Expenses", "₹0.00", self.colors['danger'])
        self.expense_count_label = self._create_stat_card("Number of Expenses", "0", self.colors['accent_primary'])
        self.avg_expense_label = self._create_stat_card("Average Expense", "₹0.00", self.colors['accent_secondary'])
        self.cash_expenses_label = self._create_stat_card("Cash Expenses", "₹0.00", self.colors['success'])
        
        stats_layout.addWidget(self.total_expenses_label)
        stats_layout.addWidget(self.expense_count_label)
        stats_layout.addWidget(self.avg_expense_label)
        stats_layout.addWidget(self.cash_expenses_label)
        
        layout.addWidget(stats_frame)
        
        # Expenses Table
        table_frame = QFrame()
        table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: #121212;
                border-radius: 10px;
                border: 1.2px solid #FFFFFF;
                padding: 20px;
            }}
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setSpacing(15)
        
        table_title = QLabel("📋 Expense Records")
        table_title.setStyleSheet(f"""
            QLabel {{
                color: #FFFFFF;
                font-size: 16px;
                font-weight: bold;
            }}
        """)
        table_layout.addWidget(table_title)
        
        # Create table
        self.expenses_table = QTableWidget(0, 11)
        self.expenses_table.setHorizontalHeaderLabels([
            "Date", "Category", "Description", "Vendor", "Amount", 
            "Payment Method", "Reference", "Person Responsible", "Created Date", "Actions", "ID"
        ])
        
        # Configure table
        self._configure_table()
        
        table_layout.addWidget(self.expenses_table)
        
        layout.addWidget(table_frame)
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
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
                padding: 20px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['text_secondary']};
                font-size: 13px;
                font-weight: 500;
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
        # Enable sorting
        self.expenses_table.setSortingEnabled(True)
        
        # Configure header
        header = self.expenses_table.horizontalHeader()
        header.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: #161616;
                color: #FFFFFF;
                padding: 12px 8px;
                border: 1.2px solid #FFFFFF;
                border-right: 1.2px solid #FFFFFF;
                font-weight: bold;
                font-size: 13px;
                min-height: 50px;
            }}
            QHeaderView::section:hover {{
                background-color: #1E1E1E;
            }}
        """)
        
        # Set column widths
        column_widths = {
            0: 110,   # Date
            1: 180,   # Category
            2: 200,   # Description
            3: 150,   # Vendor
            4: 120,   # Amount
            5: 140,   # Payment Method
            6: 120,   # Reference
            7: 150,   # Person Responsible
            8: 140,   # Created Date
            9: 180,   # Actions
            10: 0     # ID (hidden)
        }
        
        for col, width in column_widths.items():
            if width == 0:
                self.expenses_table.setColumnHidden(col, True)
            else:
                self.expenses_table.setColumnWidth(col, width)
        
        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        
        # Configure vertical header
        self.expenses_table.verticalHeader().setVisible(True)
        self.expenses_table.verticalHeader().setDefaultSectionSize(50)
        self.expenses_table.verticalHeader().setStyleSheet(f"""
            QHeaderView::section {{
                background-color: #161616;
                color: #FFFFFF;
                border: 1.2px solid #FFFFFF;
                padding: 5px;
                font-weight: bold;
            }}
        """)
        
        # Table styling
        self.expenses_table.setAlternatingRowColors(True)
        self.expenses_table.setStyleSheet(self.get_table_style() + f"""
            QTableWidget {{
                background-color: #121212;
                gridline-color: #FFFFFF;
                font-size: 13px;
                selection-background-color: #1E1E1E;
                selection-color: #FFFFFF;
                border: 1.2px solid #FFFFFF;
                color: #FFFFFF;
            }}
            QTableWidget::item {{
                padding: 8px 10px;
                border: 1px solid #FFFFFF;
                background-color: #1E1E1E;
                color: #FFFFFF;
            }}
            QTableWidget::item:alternate {{
                background-color: #161616;
            }}
            QTableWidget::item:selected {{
                background-color: #2D2D2D;
                color: #FFFFFF;
            }}
        """)
        
        self.expenses_table.setMinimumHeight(500)
        self.expenses_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.expenses_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    def _load_expenses(self):
        """Load expenses from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.expenses = json.load(f)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load expenses:\n{str(e)}")
                self.expenses = []
        else:
            self.expenses = []
    
    def _save_expenses(self):
        """Save expenses to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.expenses, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save expenses:\n{str(e)}")
            return False
    
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
            date_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            self.expenses_table.setItem(row, 0, date_item)
            
            # Category
            category_item = QTableWidgetItem(expense.get('category', ''))
            category_item.setForeground(QColor(self.colors['accent_primary']))
            category_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
            self.expenses_table.setItem(row, 1, category_item)
            
            # Description
            description = expense.get('description', 'N/A')
            if len(description) > 50:
                description = description[:47] + "..."
            self.expenses_table.setItem(row, 2, QTableWidgetItem(description))
            
            # Vendor
            self.expenses_table.setItem(row, 3, QTableWidgetItem(expense.get('vendor', 'N/A')))
            
            # Amount
            amount = expense.get('amount', 0.0)
            amount_item = QTableWidgetItem(f"₹{amount:,.2f}")
            amount_item.setForeground(QColor(self.colors['danger']))
            amount_item.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            self.expenses_table.setItem(row, 4, amount_item)
            
            # Payment Method
            payment_item = QTableWidgetItem(expense.get('payment_method', 'Cash'))
            if expense.get('payment_method') == 'Cash':
                payment_item.setForeground(QColor(self.colors['success']))
            else:
                payment_item.setForeground(QColor(self.colors['accent_secondary']))
            self.expenses_table.setItem(row, 5, payment_item)
            
            # Reference
            self.expenses_table.setItem(row, 6, QTableWidgetItem(expense.get('reference', 'N/A')))
            
            # Person Responsible
            self.expenses_table.setItem(row, 7, QTableWidgetItem(expense.get('responsible_person', 'N/A')))
            
            # Created Date
            created_date = expense.get('created_date', '')
            if created_date:
                try:
                    date_obj = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
                    formatted_date = date_obj.strftime('%d-%m-%Y %H:%M')
                except:
                    formatted_date = created_date
            else:
                formatted_date = 'N/A'
            self.expenses_table.setItem(row, 8, QTableWidgetItem(formatted_date))
            
            # Actions
            actions_widget = self._create_action_buttons(expense)
            self.expenses_table.setCellWidget(row, 9, actions_widget)
            
            # ID (hidden)
            self.expenses_table.setItem(row, 10, QTableWidgetItem(expense.get('id', '')))
        
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
                self.expenses.append(expense_data)
                if self._save_expenses():
                    QMessageBox.information(self, "Success", f"Expense '{expense_data['category']}' added successfully!\n\n✅ Expense Report, P&L, and Day Book will be updated automatically.")
                    self._populate_table()
                    self._notify_reports_update()
    
    def _edit_expense(self, expense):
        """Open dialog to edit expense."""
        dialog = ExpenseDialog(self.colors, self.get_input_style, self.get_button_style, 
                               expense_data=expense, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_expense_data()
            if updated_data:
                # Find and update expense
                for i, e in enumerate(self.expenses):
                    if e['id'] == expense['id']:
                        self.expenses[i] = updated_data
                        break
                
                if self._save_expenses():
                    QMessageBox.information(self, "Success", f"Expense updated successfully!\n\n✅ Reports automatically synchronized.")
                    self._populate_table()
                    self._notify_reports_update()
    
    def _delete_expense(self, expense):
        """Delete expense after confirmation."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete this expense?\n\nCategory: {expense['category']}\nAmount: ₹{expense['amount']:,.2f}\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove expense
            self.expenses = [e for e in self.expenses if e['id'] != expense['id']]
            
            if self._save_expenses():
                QMessageBox.information(self, "Success", f"Expense deleted successfully!\n\n✅ Reports automatically updated.")
                self._populate_table()
                self._notify_reports_update()
    
    def _view_expense(self, expense):
        """View expense details in a dialog."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Expense Details")
        dialog.setModal(True)
        dialog.setMinimumWidth(600)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel(f"💰 {expense.get('category', 'N/A')}")
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 22px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(title)
        
        # Amount highlight
        amount_label = QLabel(f"₹{expense.get('amount', 0.0):,.2f}")
        amount_label.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['danger']};
                font-size: 32px;
                font-weight: bold;
                background-color: #fee;
                padding: 15px;
                border-radius: 8px;
                border-left: 5px solid {self.colors['danger']};
            }}
        """)
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(amount_label)
        
        # Details
        date_str = expense.get('date', '')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d %B %Y')
            except:
                formatted_date = date_str
        else:
            formatted_date = 'N/A'
        
        details_text = f"""
        <table style='width:100%; border-collapse: collapse;'>
            <tr><td style='padding:8px; font-weight:bold; width:40%;'>Date:</td><td style='padding:8px;'>{formatted_date}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Category:</td><td style='padding:8px;'>{expense.get('category', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>Payment Method:</td><td style='padding:8px;'>{expense.get('payment_method', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Paid To (Vendor):</td><td style='padding:8px;'>{expense.get('vendor', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>Person Responsible:</td><td style='padding:8px;'>{expense.get('responsible_person', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Reference Number:</td><td style='padding:8px;'>{expense.get('reference', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>Description:</td><td style='padding:8px;'>{expense.get('description', 'N/A')}</td></tr>
            <tr style='background-color:#f5f5f5;'><td style='padding:8px; font-weight:bold;'>Created Date:</td><td style='padding:8px;'>{expense.get('created_date', 'N/A')}</td></tr>
            <tr><td style='padding:8px; font-weight:bold;'>Modified Date:</td><td style='padding:8px;'>{expense.get('modified_date', 'N/A')}</td></tr>
        </table>
        """
        
        details_label = QLabel(details_text)
        details_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        details_label.setWordWrap(True)
        layout.addWidget(details_label)
        
        # Close button
        close_btn = QPushButton("✖ Close")
        close_btn.setStyleSheet(self.get_button_style('cancel'))
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
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
        cash_total = sum(e.get('amount', 0.0) for e in expenses_list if e.get('payment_method') == 'Cash')
        
        # Update stat cards
        for card in [self.total_expenses_label, self.expense_count_label, 
                     self.avg_expense_label, self.cash_expenses_label]:
            for label in card.findChildren(QLabel):
                if label.property('stat_value'):
                    if card == self.total_expenses_label:
                        label.setText(f"₹{total:,.2f}")
                    elif card == self.expense_count_label:
                        label.setText(str(count))
                    elif card == self.avg_expense_label:
                        label.setText(f"₹{avg:,.2f}")
                    elif card == self.cash_expenses_label:
                        label.setText(f"₹{cash_total:,.2f}")
    
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
                            expense.get('payment_method', ''),
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
