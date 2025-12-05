"""
Invoice Form Widget Module
Handles invoice metadata and customer information input.
"""
from PyQt6.QtWidgets import (
    QFrame, QGridLayout, QLabel, QLineEdit,
    QDateEdit, QComboBox, QWidget
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from travel_billing_software.utils.logger import log_info, log_error


class InvoiceFormWidget(QFrame):
    """
    Widget for invoice details and customer information.
    
    Features:
    - Customer name, contact, address
    - Invoice number, date, type
    - Proper tab order for fast data entry
    - Signal emission on contact change for auto-completion
    
    Signals:
    - contact_changed: Emitted when contact number changes (for passenger history)
    """
    
    contact_changed = pyqtSignal(str)  # Signal with contact number
    
    def __init__(
        self,
        colors: dict,
        invoice_config: dict,
        get_frame_style: callable,
        get_input_style: callable,
        get_dateedit_style: callable,
        get_combobox_style: callable,
        generate_invoice_number: callable,
        parent=None
    ):
        """
        Initialize invoice form widget.
        
        Args:
            colors: Color scheme dictionary
            invoice_config: Invoice configuration dictionary
            get_frame_style: Function to get frame stylesheet
            get_input_style: Function to get input stylesheet
            get_dateedit_style: Function to get date edit stylesheet
            get_combobox_style: Function to get combobox stylesheet
            generate_invoice_number: Function to generate invoice number
            parent: Parent widget
        """
        super().__init__(parent)
        self.colors = colors
        self.invoice_config = invoice_config
        self.get_frame_style = get_frame_style
        self.get_input_style = get_input_style
        self.get_dateedit_style = get_dateedit_style
        self.get_combobox_style = get_combobox_style
        self.generate_invoice_number = generate_invoice_number
        
        try:
            self._init_ui()
            log_info("Invoice form widget initialized", "invoice_form")
        except Exception as e:
            log_error(
                "Failed to initialize invoice form widget",
                exception=e,
                logger_name="invoice_form_errors"
            )
            raise
    
    def _init_ui(self):
        """Initialize the UI components."""
        self.setStyleSheet(self.get_frame_style())
        
        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel(
            f"<b style='color:{self.colors['accent_secondary']}; font-size:16px;'>"
            f"📄 Invoice Details</b>"
        )
        layout.addWidget(title, 0, 0, 1, 6)
        
        # Row 1: Customer Name & Contact
        lbl_cust_name = QLabel("Customer Name:")
        lbl_cust_name.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 14px;"
        )
        lbl_cust_name.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(lbl_cust_name, 1, 0)
        
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        self.customer_name.setStyleSheet(self.get_input_style())
        self.customer_name.setMinimumWidth(250)
        layout.addWidget(self.customer_name, 1, 1)
        
        lbl_contact = QLabel("Contact Number:")
        lbl_contact.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 14px;"
        )
        lbl_contact.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(lbl_contact, 1, 2)
        
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Enter contact number")
        self.contact_number.setStyleSheet(self.get_input_style())
        self.contact_number.setMinimumWidth(250)
        # Emit signal when contact changes
        self.contact_number.textChanged.connect(self._on_contact_changed)
        layout.addWidget(self.contact_number, 1, 3)
        
        # Row 2: Address & Type
        lbl_address = QLabel("Address:")
        lbl_address.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 14px;"
        )
        lbl_address.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(lbl_address, 2, 0)
        
        self.customer_address = QLineEdit()
        self.customer_address.setPlaceholderText("Enter customer address")
        self.customer_address.setStyleSheet(self.get_input_style())
        self.customer_address.setMinimumWidth(250)
        layout.addWidget(self.customer_address, 2, 1, 1, 3)
        
        lbl_type = QLabel("Type:")
        lbl_type.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 14px;"
        )
        lbl_type.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(lbl_type, 2, 4)
        
        self.invoice_type = QComboBox()
        self.invoice_type.addItems([
            "Select Type", "Flight", "Hotel", "Tour Package",
            "Visa", "Insurance", "Other"
        ])
        self.invoice_type.setEditable(True)
        self.invoice_type.setStyleSheet(self.get_combobox_style())
        self.invoice_type.setMinimumWidth(250)
        layout.addWidget(self.invoice_type, 2, 5)
        
        # Row 3: Invoice Number & Date
        lbl_inv_num = QLabel("Invoice Number:")
        lbl_inv_num.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 14px;"
        )
        lbl_inv_num.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(lbl_inv_num, 3, 0)
        
        self.invoice_number = QLineEdit()
        self.invoice_number.setText(self.generate_invoice_number())
        self.invoice_number.setPlaceholderText("Auto-generated")
        self.invoice_number.setStyleSheet(self.get_input_style())
        self.invoice_number.setMinimumWidth(250)
        layout.addWidget(self.invoice_number, 3, 1)
        
        lbl_inv_date = QLabel("Invoice Date:")
        lbl_inv_date.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 14px;"
        )
        lbl_inv_date.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(lbl_inv_date, 3, 2)
        
        self.invoice_date = QDateEdit()
        self.invoice_date.setDate(QDate.currentDate())
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDisplayFormat(self.invoice_config['date_format'])
        self.invoice_date.setStyleSheet(self.get_dateedit_style())
        self.invoice_date.setMinimumWidth(250)
        layout.addWidget(self.invoice_date, 3, 3)
        
        # Set explicit tab order for speed
        QWidget.setTabOrder(self.customer_name, self.contact_number)
        QWidget.setTabOrder(self.contact_number, self.customer_address)
        QWidget.setTabOrder(self.customer_address, self.invoice_type)
        QWidget.setTabOrder(self.invoice_type, self.invoice_date)
        QWidget.setTabOrder(self.invoice_date, self.invoice_number)
    
    def _on_contact_changed(self, contact: str):
        """
        Handle contact number change.
        
        Args:
            contact: New contact number
        """
        try:
            self.contact_changed.emit(contact)
            log_info(f"Contact changed: {contact}", "invoice_form")
        except Exception as e:
            log_error(
                f"Error handling contact change: {contact}",
                exception=e,
                logger_name="invoice_form_errors"
            )
    
    def get_invoice_data(self) -> dict:
        """
        Get invoice form data.
        
        Returns:
            Dictionary with invoice metadata and customer info
        """
        try:
            data = {
                "invoice_number": self.invoice_number.text().strip(),
                "invoice_date": self.invoice_date.date().toString("yyyy-MM-dd"),
                "customer_name": self.customer_name.text().strip(),
                "customer_phone": self.contact_number.text().strip(),
                "customer_address": self.customer_address.text().strip(),
                "invoice_type": self.invoice_type.currentText().strip()
            }
            
            log_info(
                f"Retrieved invoice data: {data['invoice_number']}, "
                f"customer: {data['customer_name']}",
                "invoice_form"
            )
            
            return data
            
        except Exception as e:
            log_error(
                "Error getting invoice data",
                exception=e,
                logger_name="invoice_form_errors"
            )
            return {}
    
    def reset_form(self):
        """Reset all form fields to default values."""
        try:
            self.invoice_number.setText(self.generate_invoice_number())
            self.invoice_date.setDate(QDate.currentDate())
            self.customer_name.clear()
            self.contact_number.clear()
            self.customer_address.clear()
            self.invoice_type.setCurrentIndex(0)
            
            log_info("Invoice form reset", "invoice_form")
            
        except Exception as e:
            log_error(
                "Error resetting invoice form",
                exception=e,
                logger_name="invoice_form_errors"
            )
    
    def set_focus_to_first_field(self):
        """Set focus to first input field (customer name)."""
        try:
            self.customer_name.setFocus()
        except Exception as e:
            log_error(
                "Error setting focus to first field",
                exception=e,
                logger_name="invoice_form_errors"
            )
    
    def get_customer_name(self) -> str:
        """Get customer name."""
        return self.customer_name.text().strip()
    
    def get_contact_number(self) -> str:
        """Get contact number."""
        return self.contact_number.text().strip()
    
    def get_customer_address(self) -> str:
        """Get customer address."""
        return self.customer_address.text().strip()
    
    def get_invoice_number(self) -> str:
        """Get invoice number."""
        return self.invoice_number.text().strip()
    
    def get_invoice_date_string(self) -> str:
        """Get invoice date as formatted string."""
        return self.invoice_date.date().toString("yyyy-MM-dd")
    
    def get_invoice_type(self) -> str:
        """Get invoice type."""
        return self.invoice_type.currentText().strip()
