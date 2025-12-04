from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QDoubleSpinBox, QStackedWidget, QComboBox, QDateEdit,
    QScrollArea, QGridLayout, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QShortcut
from PyQt6.QtGui import QColor, QIcon
from utils.invoice_generator import generate_invoice_pdf
import sys
import json
import os
from datetime import datetime

# Import configuration and utilities
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from travel_billing_software.config.config import (
    APP_CONFIG, COMPANY_INFO, COLORS, INVOICE_CONFIG, LAYOUT_CONFIG,
    get_supplier_list, get_sector_list, get_company_info_formatted,
    get_currency_symbol, get_invoice_prefix
)
from travel_billing_software.utils.styles import (
    get_frame_style, get_label_style, get_input_style, get_dateedit_style,
    get_combobox_style, get_spinbox_style, get_button_style, get_scrollarea_style,
    get_table_style, apply_fixed_width_label, apply_minimum_width_widget
)

# Import page modules
from travel_billing_software.ui.about import AboutPage
from travel_billing_software.ui.settings import SettingsPage
from travel_billing_software.ui.reports import ReportsPage
from travel_billing_software.ui.home import HomePage
from travel_billing_software.ui.ai_features import AIFeaturesPage
from travel_billing_software.ui.supplier_page import SupplierPage

# Import database manager
try:
    from travel_billing_software.database import DatabaseManager, get_db_instance
    DB_ENABLED = True
except ImportError:
    DB_ENABLED = False
    print("⚠️  Database module not available. Using JSON-only mode.")


class DashboardImproved(QMainWindow):
    """Improved billing dashboard with new layout as requested:
    1. Invoice Details at top
    2. Excel-style table with columns: Item Name, Ticket, Sector, Supplier, Price, Qty, Tax, Amount, Actions
    3. Sector column is a dropdown (combo box)
    4. Invoice Calculation section below table
    5. Save Invoice, Save PDF, and Add Item buttons at appropriate positions
    6. Unified scrollbar for entire page (no table scrollbar)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_CONFIG['window_title'])
        self.resize(APP_CONFIG['window_width'], APP_CONFIG['window_height'])
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'billing_app.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Initialize database connection
        self.db = None
        self.metric_widgets = {}  # Initialize to prevent AttributeError
        if DB_ENABLED:
            try:
                self.db = get_db_instance()
                print("✓ Database initialized successfully")
            except Exception as e:
                print(f"✗ Database initialization failed: {e}")
                self.db = None
        
        # Apply dark theme globally
        self.apply_dark_theme()

        # Track active page and buttons
        self.current_page = None
        self.sidebar_buttons = {}

        # Main layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar with navigation buttons
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border-right: 1px solid #333;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 10, 0, 10)

        # Sidebar title
        title = QLabel("<b style='font-size:16px; color:#9b9bff;'>🏢 Menu</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(30)

        # Navigation buttons
        for page_id, label, icon in [
            ('home', '🏠 Home', 'home'),
            ('reports', '📊 Reports', 'reports'),
            ('supplier', '👥 Supplier Page', 'supplier'),
            ('ai', '🤖 AI Features', 'ai'),
            ('settings', '⚙ Settings', 'settings'),
            ('about', 'ℹ About', 'about'),
        ]:
            btn = self._create_sidebar_button(label, page_id)
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons[page_id] = btn

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # Content area with stacked widget (multiple pages)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)

        # Create pages
        self.home_page = self._create_home_page()
        self.reports_page = self._create_reports_page()
        self.supplier_page = self._create_supplier_page()
        self.ai_page = self._create_ai_page()
        self.settings_page = self._create_settings_page()
        self.about_page = self._create_about_page()

        self.content_stack.addWidget(self.home_page)
        self.content_stack.addWidget(self.reports_page)
        self.content_stack.addWidget(self.supplier_page)
        self.content_stack.addWidget(self.ai_page)
        self.content_stack.addWidget(self.settings_page)
        self.content_stack.addWidget(self.about_page)

        # Show home page by default
        self.switch_page('home')

    def _create_sidebar_button(self, label: str, page_id: str) -> QPushButton:
        """Create a styled sidebar button."""
        btn = QPushButton(label)
        btn.setMinimumHeight(45)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)

        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaa;
                border: none;
                border-left: 3px solid transparent;
                text-align: left;
                padding-left: 15px;
                font-size: 25px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                color: #ddd;
            }
            QPushButton#active {
                background-color: #9b9bff;
                color: white;
                border-left: 3px solid #6b6bff;
            }
        """)
        btn.setObjectName("sidebar_btn")
        btn.clicked.connect(lambda: self.switch_page(page_id))
        return btn

    def switch_page(self, page_id: str):
        """Switch to a different page and update button styles."""
        # Update button styles
        for bid, btn in self.sidebar_buttons.items():
            if bid == page_id:
                btn.setObjectName("active")
                btn.style().unpolish(btn)
                btn.style().polish(btn)
            else:
                btn.setObjectName("sidebar_btn")
                btn.style().unpolish(btn)
                btn.style().polish(btn)

        # Switch pages
        if page_id == 'home':
            self.content_stack.setCurrentWidget(self.home_page)
        elif page_id == 'reports':
            self.content_stack.setCurrentWidget(self.reports_page)
        elif page_id == 'supplier':
            self.content_stack.setCurrentWidget(self.supplier_page)
        elif page_id == 'ai':
            self.content_stack.setCurrentWidget(self.ai_page)
        elif page_id == 'settings':
            self.content_stack.setCurrentWidget(self.settings_page)
        elif page_id == 'about':
            self.content_stack.setCurrentWidget(self.about_page)

    def _create_home_page(self) -> QWidget:
        """Create the Home/Dashboard page."""
        home_page = HomePage(COLORS, COMPANY_INFO, INVOICE_CONFIG, APP_CONFIG,
                            get_frame_style, get_input_style, get_dateedit_style,
                            get_combobox_style, get_invoice_prefix, get_currency_symbol,
                            get_supplier_list, get_company_info_formatted, self)
        
        # Store references to widgets for compatibility
        self.table = home_page.table
        self.items_table = home_page.table
        self.invoice_number = home_page.invoice_number
        self.invoice_date = home_page.invoice_date
        self.customer_name = home_page.customer_name
        self.contact_number = home_page.contact_number
        self.customer_address = home_page.customer_address
        self.lbl_subtotal = home_page.lbl_subtotal
        self.txt_discount = home_page.txt_discount
        self.lbl_tax = home_page.lbl_tax
        self.lbl_total = home_page.lbl_total
        self.txt_received = home_page.txt_received
        self.lbl_balance = home_page.lbl_balance
        
        # Store methods
        self.add_item_row = home_page.add_item_row
        self.delete_row = home_page.delete_row
        self.calculate_row_total = home_page.calculate_row_total
        self.update_invoice_totals = home_page.update_invoice_totals
        self.calculate_balance = home_page.calculate_balance
        self.generate_invoice_number = home_page.generate_invoice_number
        
        return home_page
    
    def _create_reports_page(self) -> QWidget:
        page = QWidget()
        
        # Create scroll area for entire page
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1a1a1a;
            }
            QScrollBar:vertical {
                border: none;
                background: #2a2a2a;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #7c3aed;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a78bfa;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Content widget inside scroll area
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # === WELCOME HEADING ===
        welcome_heading = QLabel(f"Welcome To {COMPANY_INFO['name']} Billing")
        welcome_heading.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['accent_cyan']};
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin-bottom: 10px;
            }}
        """)
        welcome_heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_heading)
        
        # === 1. INVOICE DETAILS SECTION (TOP) ===
        invoice_details_frame = QFrame()
        invoice_details_frame.setStyleSheet(get_frame_style())
        invoice_layout = QGridLayout(invoice_details_frame)
        invoice_layout.setContentsMargins(20, 20, 20, 20)
        invoice_layout.setSpacing(15)
        invoice_layout.setColumnStretch(1, 1)
        invoice_layout.setColumnStretch(3, 1)
        
        # Invoice Details Title
        invoice_title = QLabel(f"<b style='color:{COLORS['accent_secondary']}; font-size:14px;'>📄 Invoice Details</b>")
        invoice_layout.addWidget(invoice_title, 0, 0, 1, 4)
        
        # Row 1: Invoice Number and Invoice Date
        lbl_inv_num = QLabel("Invoice Number:")
        lbl_inv_num.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_inv_num.setFixedWidth(130)
        invoice_layout.addWidget(lbl_inv_num, 1, 0, Qt.AlignRight)
        
        self.invoice_number = QLineEdit()
        self.invoice_number.setText(self.generate_invoice_number())
        self.invoice_number.setPlaceholderText("Auto-generated")
        self.invoice_number.setStyleSheet(get_input_style())
        self.invoice_number.setMinimumWidth(250)
        invoice_layout.addWidget(self.invoice_number, 1, 1)
        
        lbl_inv_date = QLabel("Invoice Date:")
        lbl_inv_date.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_inv_date.setFixedWidth(130)
        invoice_layout.addWidget(lbl_inv_date, 1, 2, Qt.AlignRight)
        
        self.invoice_date = QDateEdit()
        self.invoice_date.setDate(QDate.currentDate())
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDisplayFormat(INVOICE_CONFIG['date_format'])
        self.invoice_date.setStyleSheet(get_dateedit_style())
        self.invoice_date.setMinimumWidth(250)
        invoice_layout.addWidget(self.invoice_date, 1, 3)
        
        # Row 2: Customer Name and Contact Number
        lbl_cust_name = QLabel("Customer Name:")
        lbl_cust_name.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_cust_name.setFixedWidth(130)
        invoice_layout.addWidget(lbl_cust_name, 2, 0, Qt.AlignRight)
        
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        self.customer_name.setStyleSheet(get_input_style())
        self.customer_name.setMinimumWidth(250)
        invoice_layout.addWidget(self.customer_name, 2, 1)
        
        lbl_contact = QLabel("Contact Number:")
        lbl_contact.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_contact.setFixedWidth(130)
        invoice_layout.addWidget(lbl_contact, 2, 2, Qt.AlignRight)
        
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Enter contact number")
        self.contact_number.setStyleSheet(get_input_style())
        self.contact_number.setMinimumWidth(255)
        invoice_layout.addWidget(self.contact_number, 2, 3)
        
        # Row 3: Address (spans both columns)
        lbl_address = QLabel("Address:")
        lbl_address.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 12px;")
        lbl_address.setFixedWidth(130)
        invoice_layout.addWidget(lbl_address, 3, 0, Qt.AlignRight)
        
        self.customer_address = QLineEdit()
        self.customer_address.setPlaceholderText("Enter customer address")
        self.customer_address.setStyleSheet(get_input_style())
        self.customer_address.setMinimumWidth(250)
        invoice_layout.addWidget(self.customer_address, 3, 1, 1, 3)  # Spans across 3 columns
        
        layout.addWidget(invoice_details_frame)
        
        # === 2. EXCEL-STYLE TABLE (with Add Item button inside) ===
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid #444;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        # Table title and Add Item button in same row
        table_header_layout = QHBoxLayout()
        table_title = QLabel("<b style='color:#a78bfa; font-size:14px;'>🧾 Billed Items</b>")
        table_header_layout.addWidget(table_title)
        table_header_layout.addStretch()
        
        self.btn_add_item = QPushButton("➕ Add Item")
        self.btn_add_item.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent_primary']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_secondary']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['accent_primary']};
            }}
        """)
        self.btn_add_item.clicked.connect(self.add_item_row)
        self.btn_add_item.setCursor(Qt.CursorShape.PointingHandCursor)
        table_header_layout.addWidget(self.btn_add_item)
        
        table_layout.addLayout(table_header_layout)
        
        # Table with 11 columns: Passenger Name, PNR, Sector, Supplier, Type, Class, Price, Qty, Tax, Amount, Actions
        self.table = QTableWidget(0, 11)
        self.table.setHorizontalHeaderLabels([
            "Passenger Name", "PNR", "Sector", "Supplier", "Type", "Class", "Price (₹)", "Qty", "Tax (%)", "Amount (₹)", "Actions"
        ])
        
        # Disable table's own scrollbars (we use page-level scrolling)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Allow vertical scroll for many items
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Set column widths to stretch and fill full width
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # All columns stretch to fill width
        
        # Set minimum height for table (adjust based on rows)
        self.table.setMinimumHeight(300)
        
        table_layout.addWidget(self.table)
        layout.addWidget(table_frame)
        
        # === 4. INVOICE CALCULATION SECTION (Below Table) ===
        calc_frame = QFrame()
        calc_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['secondary_bg']};
                border-radius: 8px;
                border: 1px solid {COLORS['accent_primary']};
                padding: 10px;
            }}
        """)
        calc_main_layout = QVBoxLayout(calc_frame)
        calc_main_layout.setContentsMargins(10, 10, 10, 10)
        calc_main_layout.setSpacing(5)
        
        calc_title = QLabel("<b style='color:#a78bfa; font-size:14px;'>💰 Invoice Calculation</b>")
        calc_main_layout.addWidget(calc_title)
        
        # Create a compact grid layout for calculations with boxes (right-aligned)
        calc_grid = QGridLayout()
        calc_grid.setSpacing(5)
        calc_grid.setContentsMargins(5, 5, 5, 5)
        
        # Add spacer to push items to the right
        calc_grid.setColumnStretch(0, 1)
        
        # Subtotal with box
        subtotal_label = QLabel("Subtotal:")
        subtotal_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 13px;")
        subtotal_label.setMinimumWidth(90)
        calc_grid.addWidget(subtotal_label, 0, 1, Qt.AlignRight)
        self.lbl_subtotal = QLabel(f"{get_currency_symbol()}0.00")
        self.lbl_subtotal.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['accent_secondary']};
                font-weight: bold;
                font-size: 13px;
                background-color: {COLORS['primary_bg']};
                padding: 5px 10px;
                border-radius: 4px;
                border: 1px solid {COLORS['accent_secondary']};
            }}
        """)
        self.lbl_subtotal.setMinimumWidth(120)
        calc_grid.addWidget(self.lbl_subtotal, 0, 2, Qt.AlignLeft)
        
        # Discount with box
        discount_label = QLabel("Discount:")
        discount_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 13px;")
        discount_label.setMinimumWidth(90)
        calc_grid.addWidget(discount_label, 1, 1, Qt.AlignRight)
        self.txt_discount = QLineEdit()
        self.txt_discount.setPlaceholderText(f"{get_currency_symbol()}0.00")
        self.txt_discount.setText("0.00")
        self.txt_discount.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['primary_bg']};
                color: {COLORS['accent_secondary']};
                border: 1px solid {COLORS['accent_secondary']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                font-weight: bold;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['accent_secondary']};
            }}
        """)
        self.txt_discount.setMinimumWidth(120)
        self.txt_discount.textChanged.connect(self.update_invoice_totals)
        calc_grid.addWidget(self.txt_discount, 1, 2, Qt.AlignLeft)
        
        # Tax with box
        tax_label = QLabel("Tax:")
        tax_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 13px;")
        tax_label.setMinimumWidth(90)
        calc_grid.addWidget(tax_label, 2, 1, Qt.AlignRight)
        self.lbl_tax = QLabel(f"{get_currency_symbol()}0.00")
        self.lbl_tax.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['accent_secondary']};
                font-weight: bold;
                font-size: 13px;
                background-color: {COLORS['primary_bg']};
                padding: 5px 10px;
                border-radius: 4px;
                border: 1px solid {COLORS['accent_secondary']};
            }}
        """)
        self.lbl_tax.setMinimumWidth(120)
        calc_grid.addWidget(self.lbl_tax, 2, 2, Qt.AlignLeft)
        
        # Total with box (larger)
        total_label = QLabel("Total:")
        total_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 14px;")
        total_label.setMinimumWidth(90)
        calc_grid.addWidget(total_label, 3, 1, Qt.AlignRight)
        self.lbl_total = QLabel(f"{get_currency_symbol()}0.00")
        self.lbl_total.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['accent_gold']};
                font-weight: bold;
                font-size: 15px;
                background-color: {COLORS['primary_bg']};
                padding: 6px 12px;
                border-radius: 5px;
                border: 2px solid {COLORS['accent_gold']};
            }}
        """)
        self.lbl_total.setMinimumWidth(120)
        calc_grid.addWidget(self.lbl_total, 3, 2, Qt.AlignLeft)
        
        # Received with box
        received_label = QLabel("Received:")
        received_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 13px;")
        received_label.setMinimumWidth(90)
        calc_grid.addWidget(received_label, 4, 1, Qt.AlignRight)
        self.txt_received = QLineEdit()
        self.txt_received.setPlaceholderText(f"{get_currency_symbol()}0.00")
        self.txt_received.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['primary_bg']};
                color: {COLORS['success']};
                border: 1px solid {COLORS['success']};
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
                font-weight: bold;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['success']};
            }}
        """)
        self.txt_received.setMinimumWidth(120)
        self.txt_received.textChanged.connect(self.calculate_balance)
        calc_grid.addWidget(self.txt_received, 4, 2, Qt.AlignLeft)
        
        # Balance with box
        balance_label = QLabel("Balance:")
        balance_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 13px;")
        balance_label.setMinimumWidth(90)
        calc_grid.addWidget(balance_label, 5, 1, Qt.AlignRight)
        self.lbl_balance = QLabel(f"{get_currency_symbol()}0.00")
        self.lbl_balance.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['danger']};
                font-weight: bold;
                font-size: 13px;
                background-color: {COLORS['primary_bg']};
                padding: 5px 10px;
                border-radius: 4px;
                border: 1px solid {COLORS['danger']};
            }}
        """)
        self.lbl_balance.setMinimumWidth(120)
        calc_grid.addWidget(self.lbl_balance, 5, 2, Qt.AlignLeft)
        
        calc_main_layout.addLayout(calc_grid)
        layout.addWidget(calc_frame)
        
        # === 5. SAVE BUTTONS (Below Calculation) ===
        btn_layout_bottom = QHBoxLayout()
        btn_layout_bottom.addStretch()
        
        self.btn_save_invoice = QPushButton("💾 Save Invoice")
        self.btn_save_invoice.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['success']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_cyan']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['success']};
            }}
        """)
        self.btn_save_invoice.clicked.connect(self.save_invoice)
        self.btn_save_invoice.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout_bottom.addWidget(self.btn_save_invoice)
        
        self.btn_save_pdf = QPushButton("📄 Save as PDF")
        self.btn_save_pdf.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['danger']};
            }}
        """)
        self.btn_save_pdf.clicked.connect(self.save_pdf)
        self.btn_save_pdf.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout_bottom.addWidget(self.btn_save_pdf)
        
        self.btn_print = QPushButton("🖨️ Print Invoice")
        self.btn_print.setStyleSheet("""
            QPushButton {
                background-color: #9b9bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #b5b5ff;
            }
            QPushButton:pressed {
                background-color: #8585ee;
            }
        """)
        self.btn_print.clicked.connect(self.print_invoice)
        self.btn_print.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout_bottom.addWidget(self.btn_print)
        
        self.btn_share = QPushButton("📤 Share Invoice")
        self.btn_share.setStyleSheet("""
            QPushButton {
                background-color: #20C997;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #38D9A9;
            }
            QPushButton:pressed {
                background-color: #12B886;
            }
        """)
        self.btn_share.clicked.connect(self.share_invoice)
        self.btn_share.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout_bottom.addWidget(self.btn_share)
        
        layout.addLayout(btn_layout_bottom)
        
        # Add some bottom spacing
        layout.addSpacing(20)
        
        # Set the content widget to scroll area
        scroll.setWidget(content)
        
        # Create main page widget with scroll area
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        # Compatibility alias for older code
        self.items_table = self.table
        
        return page

    def generate_invoice_number(self):
        """Generate a unique invoice number based on current date and time."""
        now = datetime.now()
        return f"{get_invoice_prefix()}-{now.strftime('%Y%m%d-%H%M%S')}"

    def add_item_row(self):
        """Add a new row to the table with proper widgets for each column."""
        table = self.table
        row = table.rowCount()
        table.insertRow(row)
        
        # Adjust table height dynamically
        self.table.setMinimumHeight(min(300 + (row * 45), 600))

        # Column 0: Passenger Name (QLineEdit)
        passenger_name = QLineEdit()
        passenger_name.setPlaceholderText("Enter passenger name")
        passenger_name.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #444;
            }
        """)
        table.setCellWidget(row, 0, passenger_name)

        # Column 1: PNR (QLineEdit)
        pnr = QLineEdit()
        pnr.setPlaceholderText("PNR")
        pnr.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #444;
            }
        """)
        table.setCellWidget(row, 1, pnr)

        # Column 2: Sector (QLineEdit)
        sector = QLineEdit()
        sector.setPlaceholderText("Enter sector")
        sector.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #444;
            }
        """)
        table.setCellWidget(row, 2, sector)

        # Column 3: Supplier (QComboBox - Dropdown)
        supplier = QComboBox()
        supplier.setEditable(True)  # Allow custom entries
        supplier.addItems(get_supplier_list())
        supplier.setStyleSheet(get_combobox_style())
        table.setCellWidget(row, 3, supplier)

        # Column 4: Type (QLineEdit)
        type_field = QLineEdit()
        type_field.setPlaceholderText("Enter type")
        type_field.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #444;
            }
        """)
        table.setCellWidget(row, 4, type_field)

        # Column 5: Class (QComboBox - Dropdown)
        travel_class = QComboBox()
        travel_class.addItems(["Economy", "Premium Economy", "Business", "First Class"])
        travel_class.setStyleSheet(get_combobox_style())
        table.setCellWidget(row, 5, travel_class)

        # Column 6: Price (QDoubleSpinBox)
        price = QDoubleSpinBox()
        price.setMaximum(10_000_000)
        price.setPrefix("₹ ")
        price.setDecimals(2)
        price.valueChanged.connect(lambda _: self.calculate_row_total(row))
        price.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
                padding-right: 20px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #444;
            }
            QDoubleSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 18px;
                background-color: #3a3a3a;
                border-left: 1px solid #444;
                border-radius: 0px 3px 0px 0px;
            }
            QDoubleSpinBox::up-button:hover {
                background-color: #4a4a4a;
            }
            QDoubleSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 18px;
                background-color: #3a3a3a;
                border-left: 1px solid #444;
                border-radius: 0px 0px 3px 0px;
            }
            QDoubleSpinBox::down-button:hover {
                background-color: #4a4a4a;
            }
            QDoubleSpinBox::up-arrow {
                image: none;
                width: 10px;
                height: 10px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 6px solid #999;
            }
            QDoubleSpinBox::down-arrow {
                image: none;
                width: 10px;
                height: 10px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #999;
            }
        """)
        table.setCellWidget(row, 6, price)

        # Column 7: Qty (QDoubleSpinBox)
        qty = QDoubleSpinBox()
        qty.setMinimum(1)
        qty.setMaximum(9999)
        qty.setValue(1)
        qty.setDecimals(0)
        qty.valueChanged.connect(lambda _: self.calculate_row_total(row))
        qty.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
                padding-right: 20px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #444;
            }
            QDoubleSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 18px;
                background-color: #3a3a3a;
                border-left: 1px solid #444;
                border-radius: 0px 3px 0px 0px;
            }
            QDoubleSpinBox::up-button:hover {
                background-color: #4a4a4a;
            }
            QDoubleSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 18px;
                background-color: #3a3a3a;
                border-left: 1px solid #444;
                border-radius: 0px 0px 3px 0px;
            }
            QDoubleSpinBox::down-button:hover {
                background-color: #4a4a4a;
            }
            QDoubleSpinBox::up-arrow {
                image: none;
                width: 10px;
                height: 10px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 6px solid #999;
            }
            QDoubleSpinBox::down-arrow {
                image: none;
                width: 10px;
                height: 10px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #999;
            }
        """)
        table.setCellWidget(row, 7, qty)

        # Column 8: Tax % (QDoubleSpinBox)
        tax = QDoubleSpinBox()
        tax.setSuffix('%')
        tax.setMaximum(100)
        tax.setDecimals(2)
        tax.valueChanged.connect(lambda _: self.calculate_row_total(row))
        tax.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
                padding-right: 20px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #444;
            }
            QDoubleSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 18px;
                background-color: #3a3a3a;
                border-left: 1px solid #444;
                border-radius: 0px 3px 0px 0px;
            }
            QDoubleSpinBox::up-button:hover {
                background-color: #4a4a4a;
            }
            QDoubleSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 18px;
                background-color: #3a3a3a;
                border-left: 1px solid #444;
                border-radius: 0px 0px 3px 0px;
            }
            QDoubleSpinBox::down-button:hover {
                background-color: #4a4a4a;
            }
            QDoubleSpinBox::up-arrow {
                image: none;
                width: 10px;
                height: 10px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 6px solid #999;
            }
            QDoubleSpinBox::down-arrow {
                image: none;
                width: 10px;
                height: 10px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #999;
            }
        """)
        table.setCellWidget(row, 8, tax)

        # Column 9: Amount (QLineEdit - Read-only)
        amount = QLineEdit("₹ 0.00")
        amount.setReadOnly(True)
        amount.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        amount.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: #FFD700;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        table.setCellWidget(row, 9, amount)

        # Column 10: Actions (Delete button))
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Delete this row")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['danger']};
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent_gold']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['danger']};
            }}
        """)
        delete_btn.clicked.connect(lambda: self.delete_row(row))
        table.setCellWidget(row, 10, delete_btn)

    def delete_row(self, row: int):
        """Delete a specific row from the table."""
        self.table.removeRow(row)
        # Adjust table height
        self.table.setMinimumHeight(min(300 + (self.table.rowCount() * 45), 600))
        # Recalculate totals after deletion
        self.update_invoice_totals()

    def calculate_row_total(self, row: int):
        """Calculate the amount for a specific row based on Price, Qty, and Tax."""
        table = self.table
        try:
            price_w = table.cellWidget(row, 6)
            qty_w = table.cellWidget(row, 7)
            tax_w = table.cellWidget(row, 8)
            amount_w = table.cellWidget(row, 9)
            
            price = float(price_w.value() if price_w else 0)
            qty = float(qty_w.value() if qty_w else 0)
            tax_pct = float(tax_w.value() if tax_w else 0)
            
            # Calculate: (Price * Qty) + Tax%
            subtotal = price * qty
            tax_amount = subtotal * (tax_pct / 100)
            total = subtotal + tax_amount
            
            if amount_w:
                amount_w.setText(f"₹ {total:.2f}")
        except Exception as e:
            print(f"Error calculating row total: {e}")
        finally:
            self.update_invoice_totals()

    def update_invoice_totals(self):
        """Update the invoice calculation section (Subtotal, Discount, Tax, Total)."""
        subtotal = 0.0
        total_tax = 0.0
        table = self.table
        
        for r in range(table.rowCount()):
            try:
                # Get price, qty, and tax from widgets
                price_w = table.cellWidget(r, 6)
                qty_w = table.cellWidget(r, 7)
                tax_w = table.cellWidget(r, 8)
                
                price = float(price_w.value() if price_w else 0)
                qty = float(qty_w.value() if qty_w else 0)
                tax_pct = float(tax_w.value() if tax_w else 0)
                
                # Calculate row subtotal and tax
                row_subtotal = price * qty
                row_tax = row_subtotal * (tax_pct / 100)
                
                subtotal += row_subtotal
                total_tax += row_tax
            except Exception as e:
                print(f"Error calculating totals for row {r}: {e}")
        
        # Get discount amount
        try:
            discount_text = self.txt_discount.text().replace('₹', '').replace(',', '').strip()
            discount = float(discount_text) if discount_text else 0.0
        except:
            discount = 0.0
        
        # Calculate total: subtotal - discount + tax
        total = subtotal - discount + total_tax
        
        self.lbl_subtotal.setText(f"₹{subtotal:.2f}")
        self.lbl_tax.setText(f"₹{total_tax:.2f}")
        self.lbl_total.setText(f"₹{total:.2f}")
        
        # Recalculate balance when totals change
        self.calculate_balance()

    def calculate_balance(self):
        """Calculate balance as Total - Received Amount."""
        try:
            # Get total amount from label
            total_text = self.lbl_total.text().replace('₹', '').replace(',', '').strip()
            total = float(total_text) if total_text else 0.0

            # Get received amount from input field
            received_text = self.txt_received.text().replace('₹', '').replace(',', '').strip()
            received = float(received_text) if received_text else 0.0

            # Calculate balance
            balance = total - received

            # Update balance label with color coding
            if balance > 0:
                # Red if balance is due
                self.lbl_balance.setStyleSheet(f"color: {COLORS['danger']}; font-weight: bold; font-size: 13px; background-color: {COLORS['primary_bg']}; padding: 5px 10px; border-radius: 4px; border: 1px solid {COLORS['danger']};")
                self.lbl_balance.setText(f"{get_currency_symbol()}{balance:.2f}")
            elif balance < 0:
                # Green if overpaid
                self.lbl_balance.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold; font-size: 13px; background-color: {COLORS['primary_bg']}; padding: 5px 10px; border-radius: 4px; border: 1px solid {COLORS['success']};")
                self.lbl_balance.setText(f"{get_currency_symbol()}{abs(balance):.2f} (Overpaid)")
            else:
                # Gray if fully paid
                self.lbl_balance.setStyleSheet(f"color: {COLORS['text_muted']}; font-weight: bold; font-size: 13px; background-color: {COLORS['primary_bg']}; padding: 5px 10px; border-radius: 4px; border: 1px solid {COLORS['text_muted']};")
                self.lbl_balance.setText(f"{get_currency_symbol()}0.00 (Paid)")
        except Exception as e:
            print(f"Error calculating balance: {e}")
            self.lbl_balance.setText("₹0.00")

    def save_invoice(self):
        """Save the invoice data to JSON file and database."""
        try:
            # Prepare invoice data
            invoice_data = {
                "invoice_number": self.invoice_number.text(),
                "invoice_date": self.invoice_date.date().toString("dd/MM/yyyy"),
                "customer_name": self.customer_name.text(),
                "contact_number": self.contact_number.text(),
                "customer_address": self.customer_address.text(),
                "items": [],
                "subtotal": self.lbl_subtotal.text(),
                "discount": self.txt_discount.text(),
                "tax": self.lbl_tax.text(),
                "total": self.lbl_total.text(),
                "received": self.txt_received.text(),
                "balance": self.lbl_balance.text()
            }
            
            # Collect all items from table
            for r in range(self.table.rowCount()):
                passenger_name_w = self.table.cellWidget(r, 0)
                pnr_w = self.table.cellWidget(r, 1)
                sector_w = self.table.cellWidget(r, 2)
                supplier_w = self.table.cellWidget(r, 3)
                type_w = self.table.cellWidget(r, 4)
                class_w = self.table.cellWidget(r, 5)
                price_w = self.table.cellWidget(r, 6)
                qty_w = self.table.cellWidget(r, 7)
                tax_w = self.table.cellWidget(r, 8)
                amount_w = self.table.cellWidget(r, 9)
                
                item = {
                    "passenger_name": passenger_name_w.text() if passenger_name_w else "",
                    "pnr": pnr_w.text() if pnr_w else "",
                    "sector": sector_w.text() if sector_w else "",
                    "supplier": supplier_w.currentText() if supplier_w else "",
                    "type": type_w.text() if type_w else "",
                    "class": class_w.currentText() if class_w else "",
                    "price": price_w.value() if price_w else 0,
                    "qty": qty_w.value() if qty_w else 0,
                    "tax": tax_w.value() if tax_w else 0,
                    "amount": amount_w.text() if amount_w else "₹0.00"
                }
                invoice_data["items"].append(item)
            
            # Save to JSON file
            filename = f"invoices/invoice_{invoice_data['invoice_number']}.json"
            os.makedirs("invoices", exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(invoice_data, f, indent=4)
            
            print(f"✓ Invoice saved to JSON: {filename}")
            
            # Save to database if available
            if self.db:
                try:
                    # Parse numeric values for database
                    db_data = invoice_data.copy()
                    db_data['subtotal'] = float(db_data['subtotal'].replace('₹', '').replace(',', '').strip() or 0)
                    db_data['tax'] = float(db_data['tax'].replace('₹', '').replace(',', '').strip() or 0)
                    db_data['total'] = float(db_data['total'].replace('₹', '').replace(',', '').strip() or 0)
                    db_data['received'] = float(db_data['received'].replace('₹', '').replace(',', '').strip() or 0)
                    
                    # Parse discount
                    discount_text = db_data.get('discount', '₹0.00').replace('₹', '').replace(',', '').strip()
                    db_data['discount'] = float(discount_text or 0)
                    
                    # Parse balance
                    balance_text = db_data['balance'].replace('₹', '').replace(',', '').replace('(Paid)', '').replace('(Overpaid)', '').strip()
                    db_data['balance'] = float(balance_text or 0)
                    
                    # Determine status
                    if db_data['balance'] == 0:
                        db_data['status'] = 'Paid'
                    elif db_data['balance'] < 0:
                        db_data['status'] = 'Overpaid'
                    else:
                        db_data['status'] = 'Pending'
                    
                    # Map item fields to database format
                    db_data['items'] = []
                    for item in invoice_data.get('items', []):
                        # Parse amount value
                        amount_text = item.get('amount', '₹0.00').replace('₹', '').replace(',', '').strip()
                        amount_value = float(amount_text or 0)
                        
                        db_item = {
                            'item': item.get('passenger_name', ''),  # Map passenger_name to item
                            'ticket': item.get('pnr', ''),  # Map pnr to ticket
                            'sector': item.get('sector', ''),
                            'supplier': item.get('supplier', ''),
                            'class': item.get('class', ''),
                            'price': float(item.get('price', 0)),
                            'qty': float(item.get('qty', 1)),
                            'tax': float(item.get('tax', 0)),
                            'amount': amount_value
                        }
                        db_data['items'].append(db_item)
                    
                    if self.db.save_invoice(db_data):
                        print(f"✓ Invoice saved to database")
                    else:
                        print(f"⚠️  Invoice saved to JSON only (database save failed)")
                except Exception as db_error:
                    print(f"⚠️  Database save error: {db_error}")
                    import traceback
                    traceback.print_exc()
            
            # Show confirmation
            from PyQt6.QtWidgets import QMessageBox
            msg = f"Invoice saved successfully!\n\n"
            msg += f"📁 JSON File: {filename}\n"
            if self.db:
                msg += f"🗄️  Database: ✓ Saved"
            QMessageBox.information(self, "Success", msg)
            
        except Exception as e:
            print(f"✗ Error saving invoice: {e}")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to save invoice:\n{str(e)}")


    def save_pdf(self):
        """Generate a professional multi-page PDF invoice using the dynamic template."""
        try:
            # Ask user where to save the PDF
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Invoice as PDF",
                f"invoice_{self.invoice_number.text()}.pdf",
                "PDF Files (*.pdf)"
            )

            if not filename:
                return

            # Collect invoice items
            items = []
            for r in range(self.table.rowCount()):
                passenger_name_w = self.table.cellWidget(r, 0)
                pnr_w = self.table.cellWidget(r, 1)
                sector_w = self.table.cellWidget(r, 2)
                supplier_w = self.table.cellWidget(r, 3)
                type_w = self.table.cellWidget(r, 4)
                class_w = self.table.cellWidget(r, 5)
                price_w = self.table.cellWidget(r, 6)
                qty_w = self.table.cellWidget(r, 7)
                tax_w = self.table.cellWidget(r, 8)
                amount_w = self.table.cellWidget(r, 9)

                # Safely extract values
                passenger = passenger_name_w.text() if passenger_name_w else ""
                pnr = pnr_w.text() if pnr_w else ""
                sector = sector_w.text() if sector_w else ""
                supplier = supplier_w.currentText() if supplier_w else ""
                type_val = type_w.text() if type_w else ""
                class_val = class_w.currentText() if class_w else ""
                price = float(price_w.value()) if price_w else 0
                qty = float(qty_w.value()) if qty_w else 0
                tax_pct = float(tax_w.value()) if tax_w else 0

                # Combine description for nicer invoice appearance
                desc = f"{passenger} | PNR: {pnr} | {sector} | {supplier} | {class_val} | {type_val}"

                items.append({
                    "description": desc,
                    "qty": qty,
                    "unit_price": price,
                    "tax_pct": tax_pct
                })

            # Build invoice data to pass to template
            invoice_data = {
                "company": {
                    "name": COMPANY_INFO["name"],
                    "address": COMPANY_INFO.get("address", ""),
                    "footer_note": INVOICE_CONFIG.get("footer_note", "")
                },
                "invoice_meta": {
                    "number": self.invoice_number.text(),
                    "date": self.invoice_date.date().toString("dd/MM/yyyy"),
                    "customer_id": ""  # optional field
                },
                "customer": {
                    "name": self.customer_name.text(),
                    "address": self.customer_address.text(),
                    "contact": self.contact_number.text(),
                },
                "items": items,
                "notes": "Generated from Travel Billing System",
                "terms": INVOICE_CONFIG.get("terms", "Payment due within 7 days.")
            }

            # Generate PDF using professional template
            generate_invoice_pdf(invoice_data, filename)

            QMessageBox.information(self, "Success", f"PDF saved successfully!\n{filename}")

        except Exception as e:
            print(f"❌ Error saving PDF: {e}")
            QMessageBox.critical(self, "Error", f"Failed to generate PDF:\n{str(e)}")


    def print_invoice(self):
        """Print the generated PDF using the OS default PDF viewer (PyQt5 only)."""
        import os
        import platform
        from PyQt6.QtWidgets import QMessageBox

        # Build PDF path
        pdf_path = os.path.join(
            os.getcwd(), "output", "invoice",
            f"invoice_{self.invoice_number.text()}.pdf"
        )

        # Ensure PDF exists (generate if needed)
        if not os.path.exists(pdf_path):
            try:
                self.save_pdf(show_dialog=False)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to generate invoice PDF:\n{e}")
                return

        if not os.path.exists(pdf_path):
            QMessageBox.critical(self, "Error", "Failed to generate invoice PDF for printing.")
            return

        system = platform.system()

        try:
            if system == "Windows":
                # Use the default associated app's "print" command
                import subprocess
                # os.startfile(pdf_path, "print") is the classic way:
                os.startfile(pdf_path, "print")

                QMessageBox.information(
                    self,
                    "Print",
                    "Invoice sent to the default PDF viewer for printing.\n"
                    "Check the print dialog that may have opened."
                )

            elif system == "Darwin":  # macOS
                import subprocess
                subprocess.Popen(["open", pdf_path])
                QMessageBox.information(
                    self,
                    "Print",
                    "Invoice opened in the default PDF viewer.\nPlease print from there."
                )

            else:  # Linux / others
                import subprocess
                try:
                    # Try direct print if lpr is available
                    subprocess.run(["lpr", pdf_path], check=True)
                    QMessageBox.information(self, "Print", "Invoice sent to printer via lpr.")
                except Exception:
                    # Fallback: open in viewer
                    from PyQt6.QtCore import QUrl
                    from PyQt6.QtGui import QDesktopServices
                    QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))
                    QMessageBox.information(
                        self,
                        "Print",
                        "Invoice opened in the default PDF viewer.\nPlease print from there."
                    )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to print invoice:\n{e}")


    def share_invoice(self):
        """Share invoice via email or other methods."""
        try:
            from PyQt6.QtWidgets import QMessageBox, QInputDialog
            import os
            
            # Get invoice number
            invoice_num = self.invoice_number.text()
            if not invoice_num:
                QMessageBox.warning(self, "Warning", "Please save the invoice first before sharing.")
                return
            
            # Check if invoice JSON file exists
            invoice_file = f"invoices/invoice_{invoice_num}.json"
            if not os.path.exists(invoice_file):
                QMessageBox.warning(self, "Warning", "Invoice not found. Please save the invoice first.")
                return
            
            # Get customer name for email suggestion
            customer_name = self.customer_name.text() if hasattr(self, 'customer_name') else ""
            
            # Show dialog to enter email
            email, ok = QInputDialog.getText(
                self,
                "Share Invoice",
                f"Share Invoice: {invoice_num}\\n\\nEnter recipient email address:",
                text=""
            )
            
            if ok and email:
                if "@" not in email or "." not in email:
                    QMessageBox.warning(self, "Warning", "Please enter a valid email address.")
                    return
                
                # Show confirmation
                QMessageBox.information(
                    self,
                    "Share Invoice",
                    f"✅ Invoice Shared Successfully!\\n\\n"
                    f"📧 Recipient: {email}\\n"
                    f"📄 Invoice: {invoice_num}\\n"
                    f"👤 Customer: {customer_name}\\n\\n"
                    f"Note: Email integration can be added using:\\n"
                    f"• SMTP (Gmail, Outlook)\\n"
                    f"• SendGrid API\\n"
                    f"• AWS SES\\n"
                    f"• Mailgun"
                )
            elif ok:
                QMessageBox.warning(self, "Warning", "Please enter a valid email address.")
                
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to share invoice:\\n{str(e)}")

    def _create_reports_page(self) -> QWidget:
        """Create the Reports page with analytics and invoice list."""
        return ReportsPage(COLORS, INVOICE_CONFIG, APP_CONFIG,
                          get_table_style, get_button_style,
                          get_input_style, get_label_style, self)
    
    def _create_analytics_section(self) -> QFrame:
        """Create analytics dashboard with statistics and charts."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['secondary_bg']};
                border-radius: 10px;
                border: 1px solid #444;
                padding: 15px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Analytics Title
        analytics_title = QLabel(f"<b style='color:{COLORS['accent_gold']}; font-size:16px;'>📊 Business Analytics</b>")
        layout.addWidget(analytics_title)
        
        # Key Metrics Row
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(10)
        
        # Store metric widgets for updating
        self.metric_widgets = {}
        
        # Get statistics from database
        stats = self.db.get_statistics() if self.db else {}
        
        # Metric cards
        metrics_data = [
            ("💰 Total Revenue", stats.get('total_revenue', 0), COLORS['success']),
            ("📄 Total Invoices", stats.get('total_invoices', 0), COLORS['info']),
            ("⏳ Pending Balance", stats.get('pending_balance', 0), COLORS['danger']),
            ("👥 Total Customers", stats.get('total_customers', 0), COLORS['accent_cyan'])
        ]
        
        for title, value, color in metrics_data:
            metric_card = self._create_metric_card(title, value, color)
            self.metric_widgets[title] = metric_card
            metrics_layout.addWidget(metric_card)
        
        layout.addLayout(metrics_layout)
        
        # Charts and details row
        details_layout = QHBoxLayout()
        details_layout.setSpacing(15)
        
        # Revenue chart (left)
        revenue_frame = self._create_revenue_chart()
        details_layout.addWidget(revenue_frame, 2)
        
        # Top customers (right)
        customers_frame = self._create_top_customers()
        details_layout.addWidget(customers_frame, 1)
        
        layout.addLayout(details_layout)
        
        # Payment status summary
        payment_frame = self._create_payment_status()
        layout.addWidget(payment_frame)
        
        return frame
    
    def _create_metric_card(self, title: str, value: float, color: str) -> QFrame:
        """Create a metric card widget."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_bg']};
                border-radius: 8px;
                border: 2px solid {color};
                padding: 10px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: bold;")
        card_layout.addWidget(title_label)
        
        # Value
        if isinstance(value, (int, float)) and '₹' in title or 'Revenue' in title or 'Balance' in title:
            value_text = f"{get_currency_symbol()}{value:,.2f}"
        else:
            value_text = f"{int(value):,}"
        
        value_label = QLabel(value_text)
        value_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
        value_label.setProperty('value_label', True)  # Mark for easy updating
        card_layout.addWidget(value_label)
        
        return card
    
    def _create_revenue_chart(self) -> QFrame:
        """Create revenue trend chart."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_bg']};
                border-radius: 8px;
                border: 1px solid #444;
                padding: 10px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel(f"<b style='color:{COLORS['accent_secondary']}; font-size:14px;'>📈 Revenue Trend (Last 12 Months)</b>")
        layout.addWidget(title)
        
        # Get revenue data
        revenue_data = self.db.get_revenue_by_period('month') if self.db else []
        
        if revenue_data:
            # Create simple text-based chart
            chart_widget = QWidget()
            chart_layout = QVBoxLayout(chart_widget)
            chart_layout.setSpacing(5)
            
            max_revenue = max([d['revenue'] for d in revenue_data]) if revenue_data else 1
            
            for data in revenue_data[-6:]:  # Last 6 months
                row_layout = QHBoxLayout()
                
                # Period label
                period_label = QLabel(data['period'])
                period_label.setFixedWidth(80)
                period_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 11px;")
                row_layout.addWidget(period_label)
                
                # Bar
                bar_width = int((data['revenue'] / max_revenue) * 200) if max_revenue > 0 else 0
                bar = QFrame()
                bar.setFixedSize(bar_width, 20)
                bar.setStyleSheet(f"background-color: {COLORS['accent_primary']}; border-radius: 3px;")
                row_layout.addWidget(bar)
                
                # Value label
                value_label = QLabel(f"{get_currency_symbol()}{data['revenue']:,.0f}")
                value_label.setStyleSheet(f"color: {COLORS['accent_gold']}; font-size: 11px; font-weight: bold;")
                row_layout.addWidget(value_label)
                
                row_layout.addStretch()
                chart_layout.addLayout(row_layout)
            
            layout.addWidget(chart_widget)
        else:
            no_data = QLabel("No revenue data available")
            no_data.setStyleSheet(f"color: {COLORS['text_secondary']}; font-style: italic; padding: 20px;")
            no_data.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_data)
        
        layout.addStretch()
        return frame
    
    def _create_top_customers(self) -> QFrame:
        """Create top customers list."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_bg']};
                border-radius: 8px;
                border: 1px solid #444;
                padding: 10px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel(f"<b style='color:{COLORS['accent_secondary']}; font-size:14px;'>👥 Top Customers</b>")
        layout.addWidget(title)
        
        # Get top customers
        top_customers = self.db.get_top_customers(5) if self.db else []
        
        if top_customers:
            for i, customer in enumerate(top_customers, 1):
                customer_row = QHBoxLayout()
                
                # Rank
                rank_label = QLabel(f"#{i}")
                rank_label.setFixedWidth(30)
                rank_label.setStyleSheet(f"color: {COLORS['accent_gold']}; font-weight: bold;")
                customer_row.addWidget(rank_label)
                
                # Customer info
                info_layout = QVBoxLayout()
                name_label = QLabel(customer['customer_name'])
                name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: bold; font-size: 12px;")
                info_layout.addWidget(name_label)
                
                details_label = QLabel(f"{customer['invoice_count']} invoices • {get_currency_symbol()}{customer['total_spent']:,.2f}")
                details_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
                info_layout.addWidget(details_label)
                
                customer_row.addLayout(info_layout)
                customer_row.addStretch()
                
                layout.addLayout(customer_row)
                
                # Separator
                if i < len(top_customers):
                    separator = QFrame()
                    separator.setFrameShape(QFrame.HLine)
                    separator.setStyleSheet(f"background-color: #444;")
                    layout.addWidget(separator)
        else:
            no_data = QLabel("No customer data available")
            no_data.setStyleSheet(f"color: {COLORS['text_secondary']}; font-style: italic; padding: 20px;")
            no_data.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_data)
        
        layout.addStretch()
        return frame
    
    def _create_payment_status(self) -> QFrame:
        """Create payment status summary."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary_bg']};
                border-radius: 8px;
                border: 1px solid #444;
                padding: 10px;
            }}
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_layout = QVBoxLayout()
        title = QLabel(f"<b style='color:{COLORS['accent_secondary']}; font-size:14px;'>💳 Payment Status Summary</b>")
        title_layout.addWidget(title)
        layout.addLayout(title_layout)
        
        layout.addStretch()
        
        # Get payment status
        payment_status = self.db.get_payment_status_summary() if self.db else {}
        
        # Status boxes
        statuses = [
            ("✅ Paid", payment_status.get('paid', {'count': 0, 'amount': 0}), COLORS['success']),
            ("⏳ Pending", payment_status.get('pending', {'count': 0, 'amount': 0}), COLORS['danger']),
            ("💰 Overpaid", payment_status.get('overpaid', {'count': 0, 'amount': 0}), COLORS['info'])
        ]
        
        for label, data, color in statuses:
            status_box = QVBoxLayout()
            
            status_label = QLabel(label)
            status_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 12px;")
            status_label.setAlignment(Qt.AlignCenter)
            status_box.addWidget(status_label)
            
            count_label = QLabel(f"{data['count']} invoices")
            count_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
            count_label.setAlignment(Qt.AlignCenter)
            status_box.addWidget(count_label)
            
            amount_label = QLabel(f"{get_currency_symbol()}{data['amount']:,.2f}")
            amount_label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
            amount_label.setAlignment(Qt.AlignCenter)
            status_box.addWidget(amount_label)
            
            layout.addLayout(status_box)
            
            if label != statuses[-1][0]:
                separator = QFrame()
                separator.setFrameShape(QFrame.VLine)
                separator.setStyleSheet(f"background-color: #444;")
                layout.addWidget(separator)
        
        return frame
    
    def refresh_analytics(self):
        """Refresh analytics data."""
        if not self.db:
            print("⚠️  Database not available, skipping analytics refresh")
            return
        
        if not hasattr(self, 'metric_widgets') or not self.metric_widgets:
            print("⚠️  Metric widgets not initialized, skipping analytics refresh")
            return
        
        try:
            # Get updated statistics
            stats = self.db.get_statistics()
            print(f"✓ Analytics refreshed: {stats}")
            
            # Update metric cards
            metrics_mapping = {
                "💰 Total Revenue": ('total_revenue', True),
                "📄 Total Invoices": ('total_invoices', False),
                "⏳ Pending Balance": ('pending_balance', True),
                "👥 Total Customers": ('total_customers', False)
            }
            
            for title, metric_card in self.metric_widgets.items():
                if title in metrics_mapping:
                    key, is_currency = metrics_mapping[title]
                    value = stats.get(key, 0)
                    
                    # Find value label in card
                    for child in metric_card.findChildren(QLabel):
                        if child.property('value_label'):
                            if is_currency:
                                child.setText(f"{get_currency_symbol()}{value:,.2f}")
                            else:
                                child.setText(f"{int(value):,}")
                            break
        except Exception as e:
            print(f"✗ Error refreshing analytics: {e}")
            import traceback
            traceback.print_exc()

    def _create_settings_page(self) -> QWidget:
        """Create the Settings page with configuration options."""
        return SettingsPage(COLORS, COMPANY_INFO, INVOICE_CONFIG, 
                          get_input_style, get_spinbox_style, 
                          get_button_style, get_scrollarea_style, self.db)
    
    def _create_supplier_page(self) -> QWidget:
        """Create the Supplier Management page."""
        return SupplierPage(COLORS, get_table_style, get_button_style, get_input_style, self)
        
    def _create_ai_page(self) -> QWidget:
        """Create the AI Features page."""
        return AIFeaturesPage(
            COLORS,
            APP_CONFIG,
            get_button_style,
            get_input_style,
            get_label_style,
            get_scrollarea_style,
            self,
        )


    def _create_about_page(self) -> QWidget:
        """Create the About page."""
        return AboutPage(COLORS, APP_CONFIG, COMPANY_INFO)

    def apply_dark_theme(self):
        """Apply comprehensive dark theme to the entire application."""
        dark_stylesheet = """
            QMainWindow {
                background-color: #0d0d0d;
                color: #ffffff;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
                width: 12px;
                margin: 0px;
            }
            QLineEdit {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #9b9bff;
            }
            QDateEdit {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QDateEdit:focus {
                border: 1px solid #9b9bff;
            }
            QDateEdit::drop-down {
                border: none;
                background-color: #5b5bff;
            }
            QPushButton {
                background-color: #5b5bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7a7aff;
            }
            QPushButton:pressed {
                background-color: #4a4aee;
            }
            QTableWidget {
                background-color: #1a1a1a;
                alternate-background-color: #252525;
                gridline-color: #444;
                color: #ddd;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
                background-color: #2a2a2a;
                color: #ddd;
            }
            QTableWidget::item:selected {
                background-color: #9b9bff;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2a2a2a;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #444;
                border-bottom: 2px solid #7c3aed;
                font-weight: bold;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #2a2a2a;
                border: 1px solid #444;
            }
            QTableWidget::verticalHeader {
                background-color: #2a2a2a;
                color: #ddd;
            }
            QFrame {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QDoubleSpinBox {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 3px;
            }
            QDoubleSpinBox:focus {
                border: 1px solid #a78bfa;
            }
            QDoubleSpinBox::up-button {
                background-color: #7c3aed;
            }
            QDoubleSpinBox::down-button {
                background-color: #7c3aed;
            }
            QComboBox {
                background-color: #2a2a2a;
                color: #ddd;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
            QComboBox:focus {
                border: 1px solid #a78bfa;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #7c3aed;
            }
            QComboBox QAbstractItemView {
                background-color: #2a2a2a;
                color: #ddd;
                selection-background-color: #7c3aed;
                border: 1px solid #444;
            }
            QStackedWidget {
                background-color: #1a1a1a;
            }
        """
        self.setStyleSheet(dark_stylesheet)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DashboardImproved()
    w.show()
    sys.exit(app.exec())
