"""
Home Page Widget - Main Invoice Creation Interface
Orchestrates all sub-widgets for complete invoice workflow.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QCursor
from travel_billing_software.utils.logger import log_info, log_error, log_warning

# Import sub-modules
from .db_operations import InvoiceDBOperations
from .invoice_form import InvoiceFormWidget
from .items_table import ItemsTableWidget
from .calculations import CalculationsWidget
from .utils import (
    InvoiceNumberGenerator,
    PDFOperations,
    KeyboardShortcutsManager,
    prepare_items_for_pdf,
    format_date_for_display
)


class HomePage(QWidget):
    """
    Main home page widget for invoice creation and management.
    
    Architecture:
    - Composed of specialized sub-widgets (invoice form, table, calculations)
    - Database operations isolated in db_operations module
    - PDF and utility functions in separate utils module
    - Clean separation between UI and business logic
    
    Features:
    - High-speed data entry with keyboard shortcuts
    - Auto-completion for repeat customers
    - Passport details integration
    - Real-time calculations
    - PDF generation and printing
    """
    
    def __init__(
        self,
        colors: dict,
        company_info: dict,
        invoice_config: dict,
        app_config: dict,
        get_frame_style: callable,
        get_input_style: callable,
        get_dateedit_style: callable,
        get_combobox_style: callable,
        get_invoice_prefix: callable,
        get_currency_symbol: callable,
        get_supplier_list: callable,
        get_company_info_formatted: callable,
        dashboard_ref
    ):
        """
        Initialize home page.
        
        Args:
            colors: Color scheme dictionary
            company_info: Company information dictionary
            invoice_config: Invoice configuration
            app_config: Application configuration
            get_frame_style: Function to get frame style
            get_input_style: Function to get input style
            get_dateedit_style: Function to get date edit style
            get_combobox_style: Function to get combobox style
            get_invoice_prefix: Function to get invoice prefix
            get_currency_symbol: Function to get currency symbol
            get_supplier_list: Function to get supplier list
            get_company_info_formatted: Function to get formatted company info
            dashboard_ref: Reference to dashboard widget
        """
        super().__init__()
        
        # Store references
        self.colors = colors
        self.company_info = company_info
        self.invoice_config = invoice_config
        self.app_config = app_config
        self.get_frame_style = get_frame_style
        self.get_input_style = get_input_style
        self.get_dateedit_style = get_dateedit_style
        self.get_combobox_style = get_combobox_style
        self.get_invoice_prefix = get_invoice_prefix
        self.get_currency_symbol = get_currency_symbol
        self.get_supplier_list = get_supplier_list
        self.get_company_info_formatted = get_company_info_formatted
        self.dashboard = dashboard_ref
        
        # Initialize components
        try:
            self.db_ops = InvoiceDBOperations()
            self.invoice_generator = InvoiceNumberGenerator(get_invoice_prefix)
            self.pdf_ops = PDFOperations(company_info, invoice_config, get_currency_symbol)
            
            log_info("Home page initializing...", "home_page")
            
            self._init_ui()
            self._setup_connections()
            self._load_data()
            self._setup_keyboard_shortcuts()
            
            log_info("Home page initialized successfully", "home_page")
            
        except Exception as e:
            log_error(
                "Failed to initialize home page",
                exception=e,
                logger_name="home_page_errors"
            )
            raise
    
    def _init_ui(self):
        """Initialize the user interface."""
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
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
        
        # Content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(12, 15, 12, 15)
        layout.setSpacing(12)
        
        # Welcome heading
        welcome_heading = QLabel(f"Welcome To {self.company_info['name']} Billing")
        welcome_heading.setStyleSheet(
            f"QLabel {{ "
            f"color: {self.colors['accent_cyan']}; "
            f"font-size: 26px; font-weight: bold; "
            f"font-family: 'Segoe UI', Arial, sans-serif; "
            f"margin-bottom: 10px; "
            f"}}"
        )
        welcome_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_heading)
        
        # Invoice form widget
        self.invoice_form = InvoiceFormWidget(
            colors=self.colors,
            invoice_config=self.invoice_config,
            get_frame_style=self.get_frame_style,
            get_input_style=self.get_input_style,
            get_dateedit_style=self.get_dateedit_style,
            get_combobox_style=self.get_combobox_style,
            generate_invoice_number=self.invoice_generator.generate,
            db=self.db_ops.db
        )
        layout.addWidget(self.invoice_form)
        
        # Items table widget
        self.items_table = ItemsTableWidget(
            colors=self.colors,
            get_supplier_list=self.get_supplier_list
        )
        layout.addWidget(self.items_table)
        
        # Calculations widget
        self.calculations = CalculationsWidget(
            colors=self.colors,
            get_currency_symbol=self.get_currency_symbol
        )
        layout.addWidget(self.calculations)
        
        # Action buttons
        btn_layout = self._create_action_buttons()
        layout.addLayout(btn_layout)
        
        # Bottom spacing
        layout.addSpacing(20)
        
        # Set scroll widget
        scroll.setWidget(content)
        
        # Main layout
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)
        
        # Compatibility: items_table.table alias
        self.table = self.items_table.table
        
        # Expose widgets for backward compatibility with main_window.py
        self.invoice_number = self.invoice_form.invoice_number
        self.invoice_date = self.invoice_form.invoice_date
        self.customer_name = self.invoice_form.customer_name
        self.contact_number = self.invoice_form.contact_number
        self.customer_email = self.invoice_form.customer_email
        self.payment_mode = self.calculations.payment_mode
        self.lbl_total = self.calculations.lbl_total
        self.txt_received = self.calculations.txt_received
        self.lbl_balance = self.calculations.lbl_balance
    
    def _create_action_buttons(self) -> QHBoxLayout:
        """Create action button layout."""
        btn_layout = QHBoxLayout()
        
        # Reset button
        self.btn_reset = QPushButton("🔄 Reset (Ctrl+N)")
        self.btn_reset.setStyleSheet(
            f"QPushButton {{ "
            f"background-color: {self.colors['warning']}; "
            f"color: white; border: none; border-radius: 5px; "
            f"padding: 12px 22px; font-weight: bold; font-size: 14px; "
            f"}} "
            f"QPushButton:hover {{ background-color: #f59e0b; }}"
        )
        self.btn_reset.clicked.connect(self.reset_invoice)
        btn_layout.addWidget(self.btn_reset)
        
        btn_layout.addStretch()
        
        # Save button
        self.btn_save_invoice = QPushButton("💾 Save (Ctrl+S)")
        self.btn_save_invoice.setStyleSheet(
            f"QPushButton {{ "
            f"background-color: {self.colors['success']}; "
            f"color: white; border: none; border-radius: 5px; "
            f"padding: 12px 22px; font-weight: bold; font-size: 14px; "
            f"}} "
            f"QPushButton:hover {{ background-color: {self.colors['accent_cyan']}; }}"
        )
        self.btn_save_invoice.clicked.connect(self.save_invoice)
        btn_layout.addWidget(self.btn_save_invoice)
        
        # PDF button
        self.btn_save_pdf = QPushButton("📄 PDF")
        self.btn_save_pdf.setStyleSheet(
            f"QPushButton {{ "
            f"background-color: {self.colors['danger']}; "
            f"color: white; border: none; border-radius: 5px; "
            f"padding: 12px 22px; font-weight: bold; font-size: 14px; "
            f"}} "
            f"QPushButton:hover {{ background-color: {self.colors['accent_gold']}; }}"
        )
        self.btn_save_pdf.clicked.connect(self.save_pdf)
        btn_layout.addWidget(self.btn_save_pdf)
        
        # Print button
        self.btn_print = QPushButton("🖨️ Print (Ctrl+P)")
        self.btn_print.setStyleSheet(
            "QPushButton { "
            "background-color: #9b9bff; color: white; "
            "border: none; border-radius: 5px; "
            "padding: 12px 22px; font-weight: bold; font-size: 14px; "
            "} "
            "QPushButton:hover { background-color: #b5b5ff; }"
        )
        self.btn_print.clicked.connect(self.print_invoice)
        btn_layout.addWidget(self.btn_print)
        
        # Share button
        self.btn_share = QPushButton("📤 Share")
        self.btn_share.setStyleSheet(
            "QPushButton { "
            "background-color: #20C997; color: white; "
            "border: none; border-radius: 5px; "
            "padding: 12px 22px; font-weight: bold; font-size: 14px; "
            "} "
            "QPushButton:hover { background-color: #38D9A9; }"
        )
        self.btn_share.clicked.connect(self.share_invoice)
        btn_layout.addWidget(self.btn_share)
        
        # Set cursor for all buttons
        for btn in [self.btn_reset, self.btn_save_invoice, self.btn_save_pdf,
                   self.btn_print, self.btn_share]:
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        return btn_layout
    
    def _setup_connections(self):
        """Setup signal/slot connections between widgets."""
        try:
            # Contact changed -> Update table's current contact for auto-completion
            self.invoice_form.contact_changed.connect(
                self.items_table.set_current_contact
            )
            
            # Items changed -> Update calculations
            self.items_table.items_changed.connect(self._update_calculations)
            
            log_info("Widget connections established", "home_page")
            
        except Exception as e:
            log_error(
                "Error setting up widget connections",
                exception=e,
                logger_name="home_page_errors"
            )
    
    def _load_data(self):
        """Load passenger history and initialize data."""
        try:
            # Load passenger history from database
            passenger_history = self.db_ops.load_passenger_history()
            self.items_table.set_passenger_history(passenger_history)
            
            # Set initial focus
            self.invoice_form.set_focus_to_first_field()
            
            log_info("Initial data loaded", "home_page")
            
        except Exception as e:
            log_error(
                "Error loading initial data",
                exception=e,
                logger_name="home_page_errors"
            )
    
    def _setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for actions."""
        try:
            self.shortcuts_manager = KeyboardShortcutsManager(self)
            self.shortcuts_manager.setup_shortcuts(
                save_callback=self.save_invoice,
                print_callback=self.print_invoice,
                reset_callback=self.reset_invoice,
                add_item_callback=self.items_table.add_item_row
            )
            
            log_info("Keyboard shortcuts configured", "home_page")
            
        except Exception as e:
            log_error(
                "Error setting up keyboard shortcuts",
                exception=e,
                logger_name="home_page_errors"
            )
    
    def _update_calculations(self):
        """Update invoice calculations based on table data."""
        try:
            # Calculate total from all items
            items = self.items_table.get_all_items()
            total = sum(item.get("selling_price", 0) for item in items)
            
            # Update calculations widget
            self.calculations.update_total(total)
            
        except Exception as e:
            log_error(
                "Error updating calculations",
                exception=e,
                logger_name="home_page_errors"
            )
    
    def save_invoice(self):
        """Save invoice to database."""
        try:
            log_info("Save invoice initiated", "home_page")
            
            # Validate invoice has items
            if self.items_table.get_row_count() == 0:
                QMessageBox.warning(
                    self,
                    "No Items",
                    "Please add at least one item to the invoice."
                )
                return
            
            # Collect invoice data
            invoice_form_data = self.invoice_form.get_invoice_data()
            financial_data = self.calculations.get_financial_data()
            items = self.items_table.get_all_items()
            
            # Combine all data
            invoice_data = {
                **invoice_form_data,
                **financial_data,
                "items": items,
                "payment_method": "Cash"  # Default
            }
            
            # Save to database
            invoice_id = self.db_ops.save_invoice(invoice_data)
            
            if invoice_id > 0:
                # Success
                QMessageBox.information(
                    self,
                    "Success",
                    f"Invoice {invoice_data['invoice_number']} saved successfully!\n"
                    f"Invoice ID: {invoice_id}"
                )
                
                # Update passenger history
                self._update_passenger_history(invoice_data)
                
                log_info(
                    f"Invoice saved successfully: {invoice_data['invoice_number']}, "
                    f"ID: {invoice_id}",
                    "home_page"
                )
            else:
                # Failure
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to save invoice {invoice_data['invoice_number']}\n\n"
                    "Possible issues:\n"
                    "- Duplicate invoice number\n"
                    "- Invalid data format\n"
                    "- Database constraint violation\n\n"
                    "Check logs for details."
                )
                
                log_error(
                    f"Invoice save failed: {invoice_data['invoice_number']}",
                    logger_name="home_page_errors"
                )
                
        except ValueError as e:
            # Validation error
            QMessageBox.warning(self, "Validation Error", str(e))
            log_warning(f"Invoice validation failed: {e}", logger_name="home_page")
            
        except Exception as e:
            # Unexpected error
            log_error("Unexpected error saving invoice", exception=e, logger_name="home_page_errors")
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred:\n{str(e)}"
            )
    
    def _update_passenger_history(self, invoice_data: dict):
        """Update passenger history after saving invoice."""
        try:
            contact = invoice_data.get("customer_phone", "").strip()
            if not contact:
                return
            
            # Prepare passenger data
            passengers = []
            for item in invoice_data["items"]:
                passenger = {
                    "passenger_name": item.get("passenger_name", ""),
                    "pnr": item.get("pnr", ""),
                    "sector": item.get("sector", ""),
                    "supplier": item.get("supplier", ""),
                    "passport_number": item.get("passport_number", ""),
                    "qty": item.get("qty", 1),
                    "supplier_amount": item.get("cost_price", 0),
                    "amount": item.get("selling_price", 0),
                    "passport_details": item.get("passport_details", None)
                }
                passengers.append(passenger)
            
            # Update history in items table
            current_history = self.items_table.passenger_history
            updated_history = self.db_ops.update_passenger_history(
                contact, passengers, current_history
            )
            self.items_table.set_passenger_history(updated_history)
            
            log_info(f"Passenger history updated for contact: {contact}", "home_page")
            
        except Exception as e:
            log_error(
                "Error updating passenger history",
                exception=e,
                logger_name="home_page_errors"
            )
    
    def save_pdf(self):
        """Generate and save PDF invoice."""
        try:
            log_info("PDF generation initiated", "home_page")
            
            # Get invoice data
            invoice_number = self.invoice_form.get_invoice_number()
            items = self.items_table.get_all_items()
            
            if not items:
                QMessageBox.warning(
                    self,
                    "No Items",
                    "Please add items before generating PDF."
                )
                return
            
            # Prepare data for PDF
            pdf_items = prepare_items_for_pdf(items, self.get_currency_symbol)
            
            invoice_data = {
                "invoice_number": invoice_number,
                "invoice_date_formatted": format_date_for_display(
                    self.invoice_form.invoice_date.date()
                ),
                "customer_name": self.invoice_form.get_customer_name(),
                "customer_address": self.invoice_form.get_customer_address(),
                "customer_phone": self.invoice_form.get_contact_number(),
                "pdf_items": pdf_items
            }
            
            # Generate PDF
            self.pdf_ops.generate_pdf(invoice_number, invoice_data, show_dialog=True)
            
        except Exception as e:
            log_error("Error generating PDF", exception=e, logger_name="home_page_errors")
            QMessageBox.critical(
                self,
                "PDF Error",
                f"Failed to generate PDF:\n{str(e)}"
            )
    
    def print_invoice(self):
        """Print invoice."""
        try:
            invoice_number = self.invoice_form.get_invoice_number()
            self.pdf_ops.print_invoice(invoice_number, parent_widget=self)
            
        except Exception as e:
            log_error("Error printing invoice", exception=e, logger_name="home_page_errors")
    
    def share_invoice(self):
        """Share invoice via email."""
        try:
            invoice_number = self.invoice_form.get_invoice_number()
            self.pdf_ops.share_invoice(invoice_number, parent_widget=self)
            
        except Exception as e:
            log_error("Error sharing invoice", exception=e, logger_name="home_page_errors")
    
    def reset_invoice(self):
        """Reset all invoice fields."""
        try:
            reply = QMessageBox.question(
                self,
                'Reset Invoice',
                'Reset all fields? (Ctrl+N)',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.invoice_form.reset_form()
                self.items_table.clear_table()
                self.calculations.reset_calculations()
                
                # Set focus back to first field
                self.invoice_form.set_focus_to_first_field()
                
                log_info("Invoice reset", "home_page")
                
        except Exception as e:
            log_error("Error resetting invoice", exception=e, logger_name="home_page_errors")
    
    # ====================================================================
    # BACKWARD COMPATIBILITY METHODS (for main_window.py)
    # ====================================================================
    
    def add_item_row(self):
        """Compatibility method - delegates to items_table."""
        try:
            self.items_table.add_item_row()
        except Exception as e:
            log_error("Error in add_item_row compatibility method", exception=e, logger_name="home_page_errors")
    
    def delete_row(self, row: int):
        """Compatibility method - delegates to items_table."""
        try:
            self.items_table.delete_row(row)
        except Exception as e:
            log_error(f"Error in delete_row compatibility method for row {row}", exception=e, logger_name="home_page_errors")
    
    def calculate_row_total(self, row: int):
        """Compatibility method - triggers calculations update."""
        try:
            self._update_calculations()
        except Exception as e:
            log_error(f"Error in calculate_row_total compatibility method for row {row}", exception=e, logger_name="home_page_errors")
    
    def update_invoice_totals(self):
        """Compatibility method - delegates to calculations."""
        try:
            self._update_calculations()
        except Exception as e:
            log_error("Error in update_invoice_totals compatibility method", exception=e, logger_name="home_page_errors")
    
    def calculate_balance(self):
        """Compatibility method - delegates to calculations."""
        try:
            self.calculations.calculate_balance()
        except Exception as e:
            log_error("Error in calculate_balance compatibility method", exception=e, logger_name="home_page_errors")
    
    def generate_invoice_number(self) -> str:
        """Compatibility method - delegates to invoice generator."""
        try:
            return self.invoice_generator.generate()
        except Exception as e:
            log_error("Error in generate_invoice_number compatibility method", exception=e, logger_name="home_page_errors")
            from datetime import datetime
            return f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
