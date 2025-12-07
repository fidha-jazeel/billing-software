"""
Payments Management Page
Record and track customer payments against invoices.
"""
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QTableWidget, QPushButton,
                             QLineEdit, QTableWidgetItem, QMessageBox, 
                             QHeaderView, QDateEdit, QComboBox, QDoubleSpinBox,
                             QDialog, QFormLayout, QDialogButtonBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.utils.custom_widgets import NoWheelDoubleSpinBox
from travel_billing_software.config.config import format_currency, get_currency_symbol


class AddPaymentDialog(QDialog):
    """Dialog for recording a new payment."""
    
    def __init__(self, invoice_data, colors, parent=None):
        super().__init__(parent)
        self.invoice_data = invoice_data
        self.colors = colors
        self.payment_data = {}
        
        self.setWindowTitle(f"Record Payment - Invoice {invoice_data['invoice_number']}")
        self.setMinimumWidth(500)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # Invoice Info Card
        info_card = QFrame()
        info_card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #e0e0e0;
            }}
        """)
        info_layout = QVBoxLayout(info_card)
        
        customer_lbl = QLabel(f"<b>Customer:</b> {self.invoice_data.get('customer_name', 'N/A')}")
        invoice_lbl = QLabel(f"<b>Invoice:</b> {self.invoice_data['invoice_number']}")
        total_lbl = QLabel(f"<b>Total Amount:</b> {format_currency(self.invoice_data.get('total_amount', 0))}")
        
        # Calculate already paid
        paid_amount = self.invoice_data.get('paid_amount', 0)
        balance = self.invoice_data.get('total_amount', 0) - paid_amount
        
        paid_lbl = QLabel(f"<b>Already Paid:</b> {format_currency(paid_amount)}")
        balance_lbl = QLabel(f"<b>Balance Due:</b> <span style='color: {self.colors['danger']}'>{format_currency(balance)}</span>")
        
        info_layout.addWidget(customer_lbl)
        info_layout.addWidget(invoice_lbl)
        info_layout.addWidget(total_lbl)
        info_layout.addWidget(paid_lbl)
        info_layout.addWidget(balance_lbl)
        
        layout.addWidget(info_card)
        
        # Payment Form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setStyleSheet(f"padding: 8px; border: 1px solid #d0d0d0; border-radius: 4px;")
        form_layout.addRow("Date:", self.date_edit)
        
        # Amount
        self.amount_spin = NoWheelDoubleSpinBox()
        self.amount_spin.setRange(0.01, balance)
        self.amount_spin.setValue(balance)
        self.amount_spin.setDecimals(2)
        self.amount_spin.setPrefix(f"{get_currency_symbol()} ")
        self.amount_spin.setStyleSheet(f"padding: 8px; border: 1px solid #d0d0d0; border-radius: 4px;")
        form_layout.addRow("Amount:", self.amount_spin)
        
        # Payment Mode
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['CASH', 'BANK', 'UPI', 'CHEQUE', 'CARD'])
        self.mode_combo.setStyleSheet(f"padding: 8px; border: 1px solid #d0d0d0; border-radius: 4px;")
        form_layout.addRow("Payment Mode:", self.mode_combo)
        
        # Reference Number
        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("Transaction ID / Cheque No.")
        self.reference_input.setStyleSheet(f"padding: 8px; border: 1px solid #d0d0d0; border-radius: 4px;")
        form_layout.addRow("Reference #:", self.reference_input)
        
        # Notes
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Additional notes (optional)")
        self.notes_input.setStyleSheet(f"padding: 8px; border: 1px solid #d0d0d0; border-radius: 4px;")
        form_layout.addRow("Notes:", self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.save_payment)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def save_payment(self):
        """Validate and save payment data."""
        if self.amount_spin.value() <= 0:
            QMessageBox.warning(self, "Invalid Amount", "Payment amount must be greater than zero.")
            return
        
        self.payment_data = {
            'date': self.date_edit.date().toString("yyyy-MM-dd"),
            'amount': self.amount_spin.value(),
            'payment_mode': self.mode_combo.currentText(),
            'reference_number': self.reference_input.text().strip(),
            'notes': self.notes_input.text().strip()
        }
        
        self.accept()


class PaymentsPage(QWidget):
    """Payments management page for recording customer payments."""
    
    def __init__(self, colors, get_table_style, get_button_style, get_input_style, dashboard_ref):
        super().__init__()
        self.colors = colors
        self.get_table_style = get_table_style
        self.get_button_style = get_button_style
        self.get_input_style = get_input_style
        self.dashboard = dashboard_ref
        
        # Initialize database
        self.db = get_db_instance()
        
        # Store data
        self.unpaid_invoices = []
        self.payment_history = []
        
        self._init_ui()
        self._load_data()
    
    def _init_ui(self):
        """Initialize the UI."""
        # Main container layout
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Scroll area for entire page
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            /* Custom dark grey scrollbar styling */
            QScrollBar:vertical {
                border: none;
                background: #2b2b2b;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #444444;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #555555;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #2b2b2b;
            }
        """)
        
        # Content widget inside scroll area
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        header = QLabel("💰 Payments Management")
        header.setStyleSheet(f"""
            QLabel {{
                color: {self.colors['accent_primary']};
                font-size: 28px;
                font-weight: bold;
                padding: 10px 0px;
            }}
        """)
        main_layout.addWidget(header)
        
        # Summary Cards
        cards_layout = QHBoxLayout()
        
        self.pending_card = self._create_stat_card("Pending Amount", format_currency(0), self.colors['danger'])
        self.received_card = self._create_stat_card("Received Today", format_currency(0), self.colors['success'])
        self.invoices_card = self._create_stat_card("Unpaid Invoices", "0", self.colors['warning'])
        
        cards_layout.addWidget(self.pending_card)
        cards_layout.addWidget(self.received_card)
        cards_layout.addWidget(self.invoices_card)
        cards_layout.addStretch()
        
        main_layout.addLayout(cards_layout)
        
        # Tabs/Sections
        tabs_layout = QHBoxLayout()
        
        self.unpaid_btn = QPushButton("📋 Unpaid Invoices")
        self.unpaid_btn.setStyleSheet(self.get_button_style('primary'))
        self.unpaid_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.unpaid_btn.clicked.connect(lambda: self._switch_view('unpaid'))
        
        self.history_btn = QPushButton("📜 Payment History")
        self.history_btn.setStyleSheet(self.get_button_style('secondary'))
        self.history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.history_btn.clicked.connect(lambda: self._switch_view('history'))
        
        tabs_layout.addWidget(self.unpaid_btn)
        tabs_layout.addWidget(self.history_btn)
        tabs_layout.addStretch()
        
        main_layout.addLayout(tabs_layout)
        
        # Search Bar
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by invoice number or customer name...")
        self.search_input.setStyleSheet(self.get_input_style())
        self.search_input.textChanged.connect(self._filter_data)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet(self.get_button_style('secondary'))
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self._load_data)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(search_layout)
        
        # Table for Unpaid Invoices
        self.unpaid_table = QTableWidget(0, 7)
        self.unpaid_table.setHorizontalHeaderLabels([
            "Invoice #", "Date", "Customer", "Total", "Paid", "Balance", "Action"
        ])
        
        # Enhanced table styling with better spacing and readability
        self.unpaid_table.setStyleSheet(self.get_table_style() + f"""
            QTableWidget {{
                border: 1px solid {self.colors.get('border', '#3a3a3a')};
                gridline-color: {self.colors.get('border', '#3a3a3a')};
                font-size: 15px;
            }}
            QTableWidget::item {{
                padding: 12px 10px;
                border-bottom: 1px solid {self.colors.get('border', '#3a3a3a')};
            }}
            /* Custom dark grey scrollbar styling */
            QScrollBar:vertical {{
                border: none;
                background: #2b2b2b;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #444444;
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #555555;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: #2b2b2b;
            }}
        """)
        
        # Configure header with better height and styling
        header = self.unpaid_table.horizontalHeader()
        header.setMinimumHeight(50)
        header.setDefaultSectionSize(150)
        header.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: #3a3a3a;
                color: white;
                padding: 15px 10px;
                border: none;
                border-right: 1px solid {self.colors.get('primary_bg', '#1a1a1a')};
                font-weight: 600;
                font-size: 16px;
                text-align: left;
            }}
            QHeaderView::section:hover {{
                background-color: #4a4a4a;
            }}
        """)
        
        # Configure vertical header for row heights
        v_header = self.unpaid_table.verticalHeader()
        v_header.setDefaultSectionSize(55)  # Increased row height for better spacing
        v_header.setVisible(False)
        
        # Configure column widths with optimal proportions
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.unpaid_table.setColumnWidth(0, 200)  # Invoice # 
        self.unpaid_table.setColumnWidth(1, 130)  # Date
        self.unpaid_table.setColumnWidth(2, 180)  # Customer
        self.unpaid_table.setColumnWidth(3, 130)  # Total
        self.unpaid_table.setColumnWidth(4, 130)  # Paid
        self.unpaid_table.setColumnWidth(5, 130)  # Balance
        self.unpaid_table.setColumnWidth(6, 200)  # Action
        
        # Set last column to stretch for full width utilization
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        
        # Table display settings - Remove max height to allow full expansion within scroll area
        self.unpaid_table.setMinimumHeight(400)
        self.unpaid_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.unpaid_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.unpaid_table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.unpaid_table.setShowGrid(True)
        self.unpaid_table.setAlternatingRowColors(True)
        self.unpaid_table.setWordWrap(False)
        main_layout.addWidget(self.unpaid_table)
        
        # Table for Payment History
        self.history_table = QTableWidget(0, 6)
        self.history_table.setHorizontalHeaderLabels([
            "Date", "Payment #", "Customer", "Invoice #", "Amount", "Mode"
        ])
        
        # Enhanced table styling with better spacing and readability
        self.history_table.setStyleSheet(self.get_table_style() + f"""
            QTableWidget {{
                border: 1px solid {self.colors.get('border', '#3a3a3a')};
                gridline-color: {self.colors.get('border', '#3a3a3a')};
                font-size: 15px;
            }}
            QTableWidget::item {{
                padding: 12px 10px;
                border-bottom: 1px solid {self.colors.get('border', '#3a3a3a')};
            }}
            /* Custom dark grey scrollbar styling */
            QScrollBar:vertical {{
                border: none;
                background: #2b2b2b;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: #444444;
                min-height: 30px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #555555;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: #2b2b2b;
            }}
        """)
        
        # Configure header with better height and styling
        history_header = self.history_table.horizontalHeader()
        history_header.setMinimumHeight(50)
        history_header.setDefaultSectionSize(150)
        history_header.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: #3a3a3a;
                color: white;
                padding: 15px 10px;
                border: none;
                border-right: 1px solid {self.colors.get('primary_bg', '#1a1a1a')};
                font-weight: 600;
                font-size: 16px;
                text-align: left;
            }}
            QHeaderView::section:hover {{
                background-color: #4a4a4a;
            }}
        """)
        
        # Configure vertical header for row heights
        history_v_header = self.history_table.verticalHeader()
        history_v_header.setDefaultSectionSize(55)  # Increased row height for better spacing
        history_v_header.setVisible(False)
        
        # Configure column widths with optimal proportions
        history_header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.history_table.setColumnWidth(0, 130)  # Date
        self.history_table.setColumnWidth(1, 200)  # Payment #
        self.history_table.setColumnWidth(2, 180)  # Customer
        self.history_table.setColumnWidth(3, 200)  # Invoice #
        self.history_table.setColumnWidth(4, 130)  # Amount
        self.history_table.setColumnWidth(5, 130)  # Mode
        
        # Set last column to stretch for full width utilization
        history_header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        
        # Table display settings - Remove max height to allow full expansion within scroll area
        self.history_table.setMinimumHeight(400)
        self.history_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.history_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.history_table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.history_table.setShowGrid(True)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setWordWrap(False)
        self.history_table.hide()
        main_layout.addWidget(self.history_table)
        
        # Set content widget to scroll area and add to container
        scroll_area.setWidget(content_widget)
        container_layout.addWidget(scroll_area)
        
        self.current_view = 'unpaid'
    
    def _create_stat_card(self, title, value, color):
        """Create a statistics card."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['secondary_bg']};
                border-radius: 10px;
                border-left: 4px solid {color};
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 14px;")
        
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        value_lbl.setObjectName("value_label")
        
        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        
        card.setMaximumWidth(250)
        return card
    
    def _switch_view(self, view):
        """Switch between unpaid and history views."""
        self.current_view = view
        
        if view == 'unpaid':
            self.unpaid_btn.setStyleSheet(self.get_button_style('primary'))
            self.history_btn.setStyleSheet(self.get_button_style('secondary'))
            self.unpaid_table.show()
            self.history_table.hide()
            self._populate_unpaid_table()
        else:
            self.unpaid_btn.setStyleSheet(self.get_button_style('secondary'))
            self.history_btn.setStyleSheet(self.get_button_style('primary'))
            self.unpaid_table.hide()
            self.history_table.show()
            self._populate_history_table()
    
    def _load_data(self):
        """Load invoices and payment data from database."""
        try:
            # Get all invoices
            all_invoices = self.db.get_all_invoices()
            
            # Filter unpaid/partially paid invoices
            self.unpaid_invoices = []
            for inv in all_invoices:
                total = inv.get('total_amount', 0)
                paid = inv.get('paid_amount', 0) if inv.get('paid_amount') else 0
                
                # Calculate paid from payments_received table
                payments = self.db.get_payments_by_contact(inv['contact_id'])
                invoice_payments = [p for p in payments if p.get('invoice_id') == inv['id']]
                paid = sum(p['amount'] for p in invoice_payments)
                
                balance = total - paid
                
                if balance > 0.01:  # Has pending balance
                    inv_copy = dict(inv)
                    inv_copy['paid_amount'] = paid
                    inv_copy['balance'] = balance
                    self.unpaid_invoices.append(inv_copy)
            
            # Get all payments
            self.payment_history = self.db.get_all_payments_received()
            
            # Update statistics
            self._update_statistics()
            
            # Populate current view
            if self.current_view == 'unpaid':
                self._populate_unpaid_table()
            else:
                self._populate_history_table()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data:\n{str(e)}")
            print(f"Error loading payments data: {e}")
    
    def refresh_data(self):
        """Refresh payment data from database."""
        self._load_data()
    
    def _update_statistics(self):
        """Update the statistics cards."""
        # Total pending
        total_pending = sum(inv['balance'] for inv in self.unpaid_invoices)
        
        # Received today
        today = datetime.now().strftime('%Y-%m-%d')
        today_payments = [p for p in self.payment_history if p.get('date') == today]
        received_today = sum(p['amount'] for p in today_payments)
        
        # Update cards
        self.pending_card.findChild(QLabel, "value_label").setText(format_currency(total_pending))
        self.received_card.findChild(QLabel, "value_label").setText(format_currency(received_today))
        self.invoices_card.findChild(QLabel, "value_label").setText(str(len(self.unpaid_invoices)))
    
    def _populate_unpaid_table(self):
        """Populate the unpaid invoices table."""
        self.unpaid_table.setRowCount(0)
        
        search_text = self.search_input.text().lower()
        
        for inv in self.unpaid_invoices:
            # Filter by search
            if search_text:
                invoice_num = inv.get('invoice_number', '').lower()
                customer = inv.get('customer_name', '').lower()
                if search_text not in invoice_num and search_text not in customer:
                    continue
            
            row = self.unpaid_table.rowCount()
            self.unpaid_table.insertRow(row)
            
            # Invoice Number
            self.unpaid_table.setItem(row, 0, QTableWidgetItem(str(inv.get('invoice_number') or '')))
            
            # Date
            self.unpaid_table.setItem(row, 1, QTableWidgetItem(str(inv.get('date') or '')))
            
            # Customer
            self.unpaid_table.setItem(row, 2, QTableWidgetItem(str(inv.get('customer_name') or '')))
            
            # Total
            total_item = QTableWidgetItem(format_currency(inv.get('total_amount', 0)))
            self.unpaid_table.setItem(row, 3, total_item)
            
            # Paid
            paid_item = QTableWidgetItem(format_currency(inv.get('paid_amount', 0)))
            paid_item.setForeground(QColor(self.colors['success']))
            self.unpaid_table.setItem(row, 4, paid_item)
            
            # Balance
            balance_item = QTableWidgetItem(format_currency(inv.get('balance', 0)))
            balance_item.setForeground(QColor(self.colors['danger']))
            self.unpaid_table.setItem(row, 5, balance_item)
            
            # Action Button
            btn = QPushButton("💰 Record Payment")
            btn.setStyleSheet(self.get_button_style('add'))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, inv_data=inv: self._record_payment(inv_data))
            self.unpaid_table.setCellWidget(row, 6, btn)
    
    def _populate_history_table(self):
        """Populate the payment history table."""
        self.history_table.setRowCount(0)
        
        search_text = self.search_input.text().lower()
        
        print(f"🔍 Populating payment history - Total payments: {len(self.payment_history)}")
        print(f"   Search text: '{search_text}'")
        
        displayed_count = 0
        displayed_count = 0
        for payment in self.payment_history:
            # Filter by search
            if search_text:
                customer = payment.get('customer_name', '').lower()
                invoice_num = payment.get('invoice_number', '').lower()
                if search_text not in customer and search_text not in invoice_num:
                    continue
            
            displayed_count += 1
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            # Date
            self.history_table.setItem(row, 0, QTableWidgetItem(str(payment.get('date') or '')))
            
            # Payment Number
            self.history_table.setItem(row, 1, QTableWidgetItem(str(payment.get('payment_number') or '')))
            
            # Customer
            self.history_table.setItem(row, 2, QTableWidgetItem(str(payment.get('customer_name') or '')))
            
            # Invoice Number
            self.history_table.setItem(row, 3, QTableWidgetItem(str(payment.get('invoice_number') or 'N/A')))
            
            # Amount
            amount_item = QTableWidgetItem(format_currency(payment.get('amount', 0)))
            amount_item.setForeground(QColor(self.colors['success']))
            self.history_table.setItem(row, 4, amount_item)
            
            # Mode
            self.history_table.setItem(row, 5, QTableWidgetItem(str(payment.get('payment_mode') or '')))
        
        print(f"✅ Displayed {displayed_count} payment records in history table")
    
    def _filter_data(self):
        """Filter data based on search input."""
        if self.current_view == 'unpaid':
            self._populate_unpaid_table()
        else:
            self._populate_history_table()
    
    def _record_payment(self, invoice_data):
        """Open dialog to record a payment."""
        dialog = AddPaymentDialog(invoice_data, self.colors, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            payment_data = dialog.payment_data
            
            try:
                # Add payment to database
                payment_id = self.db.add_payment_received(
                    invoice_data['contact_id'],
                    invoice_data['id'],
                    payment_data['amount'],
                    payment_data['payment_mode'],
                    payment_data['date'],
                    payment_data['notes']
                )
                
                if payment_id > 0:
                    # Update invoice payment status
                    total_paid = invoice_data.get('paid_amount', 0) + payment_data['amount']
                    if total_paid >= invoice_data.get('total_amount', 0):
                        self.db.update_invoice_status(invoice_data['id'], 'PAID')
                    
                    print(f"✅ Payment recorded: {format_currency(payment_data['amount'])} for invoice {invoice_data['invoice_number']}")
                    
                    # Reload data
                    self._load_data()
                else:
                    QMessageBox.warning(self, "Error", "Failed to record payment.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to record payment:\n{str(e)}")
                print(f"Error recording payment: {e}")
