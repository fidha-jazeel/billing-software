"""
Invoice Form Widget Module
Handles invoice metadata and customer information input.
"""
from PyQt6.QtWidgets import (
    QFrame, QGridLayout, QLabel, QLineEdit,
    QDateEdit, QComboBox, QWidget, QPushButton, QVBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QCursor
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
        
        # Collapse state and animation
        self.is_collapsed = False
        self.animation = None
        self.collapsed_height = 0
        self.expanded_height = 0
        
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
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Header with title and collapse button
        header_layout = QGridLayout()
        header_layout.setSpacing(10)
        
        title = QLabel(
            f"<b style='color:{self.colors['accent_secondary']}; font-size:18px;'>"
            f"📄 Invoice Details</b>"
        )
        header_layout.addWidget(title, 0, 0, 1, 5)
        
        # Collapse button
        self.btn_collapse = QPushButton("▼")
        self.btn_collapse.setStyleSheet(
            f"QPushButton {{ "
            f"background-color: transparent; "
            f"color: {self.colors['accent_secondary']}; "
            f"border: 1px solid {self.colors['accent_secondary']}; "
            f"border-radius: 3px; "
            f"padding: 4px 8px; "
            f"font-size: 14px; "
            f"font-weight: bold; "
            f"}} "
            f"QPushButton:hover {{ "
            f"background-color: {self.colors['accent_secondary']}; "
            f"color: white; "
            f"}}"
        )
        self.btn_collapse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_collapse.clicked.connect(self._toggle_collapse)
        self.btn_collapse.setMaximumWidth(40)
        header_layout.addWidget(self.btn_collapse, 0, 5, Qt.AlignmentFlag.AlignRight)
        
        main_layout.addLayout(header_layout)
        
        # Always visible section: Customer Name & Contact
        always_visible = QGridLayout()
        always_visible.setSpacing(15)
        
        lbl_cust_name = QLabel("Customer Name:")
        lbl_cust_name.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 15px;"
        )
        lbl_cust_name.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        always_visible.addWidget(lbl_cust_name, 0, 0)
        
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        self.customer_name.setStyleSheet(self._get_custom_input_style())
        self.customer_name.setMinimumWidth(250)
        always_visible.addWidget(self.customer_name, 0, 1)
        
        lbl_contact = QLabel("Contact Number:")
        lbl_contact.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 15px;"
        )
        lbl_contact.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        always_visible.addWidget(lbl_contact, 0, 2)
        
        self.contact_number = QLineEdit()
        self.contact_number.setPlaceholderText("Enter contact number")
        self.contact_number.setStyleSheet(self._get_custom_input_style())
        self.contact_number.setMinimumWidth(250)
        self.contact_number.textChanged.connect(self._on_contact_changed)
        always_visible.addWidget(self.contact_number, 0, 3)
        
        main_layout.addLayout(always_visible)
        
        # Collapsible section container with stable styling
        self.collapsible_widget = QWidget()
        # Set transparent background so parent styling shows through
        self.collapsible_widget.setStyleSheet("QWidget { background: transparent; }")
        # Set size policy to maintain width but allow height changes
        self.collapsible_widget.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Maximum
        )
        
        collapsible_layout = QGridLayout(self.collapsible_widget)
        collapsible_layout.setContentsMargins(0, 10, 0, 0)
        collapsible_layout.setSpacing(15)
        
        # Row 1: Email & Type
        lbl_email = QLabel("Email:")
        lbl_email.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 15px;"
        )
        lbl_email.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        collapsible_layout.addWidget(lbl_email, 0, 0)
        
        self.customer_email = QLineEdit()
        self.customer_email.setPlaceholderText("Enter customer email")
        self.customer_email.setStyleSheet(self._get_custom_input_style())
        self.customer_email.setMinimumWidth(250)
        collapsible_layout.addWidget(self.customer_email, 0, 1)
        
        lbl_type = QLabel("Type:")
        lbl_type.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 15px;"
        )
        lbl_type.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        collapsible_layout.addWidget(lbl_type, 0, 2)
        
        self.invoice_type = QComboBox()
        self.invoice_type.addItems(["Visa", "Ticket", "Hajj", "Umra"])
        self.invoice_type.setStyleSheet(self._get_custom_combobox_style())
        self.invoice_type.setMinimumWidth(250)
        collapsible_layout.addWidget(self.invoice_type, 0, 3)
        
        # Row 2: Invoice Number & Invoice Date
        lbl_inv_num = QLabel("Invoice Number:")
        lbl_inv_num.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 15px;"
        )
        lbl_inv_num.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        collapsible_layout.addWidget(lbl_inv_num, 1, 0)
        
        self.invoice_number = QLineEdit()
        self.invoice_number.setText(self.generate_invoice_number())
        self.invoice_number.setPlaceholderText("Auto-generated")
        self.invoice_number.setStyleSheet(self._get_custom_input_style())
        self.invoice_number.setMinimumWidth(250)
        collapsible_layout.addWidget(self.invoice_number, 1, 1)
        
        lbl_inv_date = QLabel("Invoice Date:")
        lbl_inv_date.setStyleSheet(
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; font-size: 15px;"
        )
        lbl_inv_date.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        collapsible_layout.addWidget(lbl_inv_date, 1, 2)
        
        self.invoice_date = QDateEdit()
        self.invoice_date.setDate(QDate.currentDate())
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDisplayFormat(self.invoice_config['date_format'])
        self.invoice_date.setStyleSheet(self._get_custom_dateedit_style())
        self.invoice_date.setMinimumWidth(250)
        collapsible_layout.addWidget(self.invoice_date, 1, 3)
        
        main_layout.addWidget(self.collapsible_widget)
        
        # Set explicit tab order for speed
        QWidget.setTabOrder(self.customer_name, self.contact_number)
        QWidget.setTabOrder(self.contact_number, self.customer_email)
        QWidget.setTabOrder(self.customer_email, self.invoice_type)
        QWidget.setTabOrder(self.invoice_type, self.invoice_number)
        QWidget.setTabOrder(self.invoice_number, self.invoice_date)
        
        # Initialize animation after all widgets are created
        self.animation = QPropertyAnimation(self.collapsible_widget, b"maximumHeight")
        self.animation.setDuration(300)  # 300ms animation
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        
        # Ensure widgets maintain their appearance during animation
        self.collapsible_widget.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        
        # Connect animation finished signal to ensure clean state
        self.animation.finished.connect(self._on_animation_finished)
        
        # Calculate heights after widget is fully laid out
        # Use QTimer to defer height calculation until after layout is complete
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, self._calculate_heights)
    
    def _calculate_heights(self):
        """Calculate collapsed and expanded heights after layout is complete."""
        try:
            # Force layout update to get accurate size
            self.collapsible_widget.layout().activate()
            self.collapsible_widget.updateGeometry()
            
            # Get the natural height of the collapsible widget
            natural_height = self.collapsible_widget.sizeHint().height()
            self.expanded_height = max(natural_height, 100)  # Minimum 100px
            
            # Collapsed height is 0 (completely hidden)
            self.collapsed_height = 0
            
            # Set initial state to expanded with both min and max
            self.collapsible_widget.setMinimumHeight(0)
            self.collapsible_widget.setMaximumHeight(self.expanded_height)
            
            log_info(
                f"Heights calculated - Collapsed: {self.collapsed_height}, "
                f"Expanded: {self.expanded_height}",
                "invoice_form"
            )
        except Exception as e:
            log_error(
                "Error calculating heights",
                exception=e,
                logger_name="invoice_form_errors"
            )
    
    def _toggle_collapse(self):
        """Toggle the collapsible section with smooth animation."""
        if not self.animation:
            return
        
        self.is_collapsed = not self.is_collapsed
        
        # Stop any running animation
        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.stop()
        
        # Get current height
        current_height = self.collapsible_widget.height()
        
        if self.is_collapsed:
            # Collapse animation
            self.animation.setStartValue(current_height)
            self.animation.setEndValue(self.collapsed_height)
            self.btn_collapse.setText("▶")
        else:
            # Expand animation - restore to expanded height
            self.animation.setStartValue(current_height)
            self.animation.setEndValue(self.expanded_height)
            self.btn_collapse.setText("▼")
        
        # Start animation
        self.animation.start()
    
    def _on_animation_finished(self):
        """Called when animation finishes to ensure clean final state."""
        try:
            # Ensure the widget has the correct final height
            if self.is_collapsed:
                self.collapsible_widget.setMaximumHeight(self.collapsed_height)
            else:
                self.collapsible_widget.setMaximumHeight(self.expanded_height)
            
            # Force geometry update
            self.collapsible_widget.updateGeometry()
            self.updateGeometry()
            
        except Exception as e:
            log_error(
                "Error in animation finished handler",
                exception=e,
                logger_name="invoice_form_errors"
            )
    
    def _get_custom_input_style(self) -> str:
        """Get custom input style with larger font size - stable styling."""
        # Use !important-like specificity by being very explicit
        return f"""
            QLineEdit {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_secondary']};
                border: 1px solid {self.colors['border_primary']};
                border-radius: 5px;
                padding: 8px;
                font-size: 15px;
                min-height: 30px;
            }}
            QLineEdit:focus {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_secondary']};
                border: 1px solid {self.colors['border_focus']};
                border-radius: 5px;
            }}
            QLineEdit:hover {{
                background-color: {self.colors['secondary_bg']};
                border: 1px solid {self.colors['border_primary']};
            }}
        """
    
    def _get_custom_combobox_style(self) -> str:
        """Get custom combobox style with larger font size - stable styling."""
        return f"""
            QComboBox {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_secondary']};
                border: 1px solid {self.colors['border_primary']};
                border-radius: 5px;
                padding: 8px;
                font-size: 15px;
                min-height: 30px;
            }}
            QComboBox:focus {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_secondary']};
                border: 1px solid {self.colors['border_focus']};
                border-radius: 5px;
            }}
            QComboBox:hover {{
                background-color: {self.colors['secondary_bg']};
                border: 1px solid {self.colors['border_primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                background-color: {self.colors['accent_primary']};
                width: 25px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_secondary']};
                selection-background-color: {self.colors['accent_primary']};
                border: 1px solid {self.colors['border_primary']};
                font-size: 15px;
            }}
        """
    
    def _get_custom_dateedit_style(self) -> str:
        """Get custom date edit style with larger font size - stable styling."""
        return f"""
            QDateEdit {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_secondary']};
                border: 1px solid {self.colors['border_primary']};
                border-radius: 5px;
                padding: 8px;
                font-size: 15px;
                min-height: 30px;
            }}
            QDateEdit:focus {{
                background-color: {self.colors['secondary_bg']};
                color: {self.colors['text_secondary']};
                border: 1px solid {self.colors['border_focus']};
                border-radius: 5px;
            }}
            QDateEdit:hover {{
                background-color: {self.colors['secondary_bg']};
                border: 1px solid {self.colors['border_primary']};
            }}
            QDateEdit::drop-down {{
                border: none;
                background-color: {self.colors['accent_primary']};
                width: 25px;
            }}
        """
    
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
                "customer_email": self.customer_email.text().strip(),
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
            self.customer_email.clear()
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
    
    def get_customer_email(self) -> str:
        """Get customer email."""
        return self.customer_email.text().strip()
    
    def get_invoice_number(self) -> str:
        """Get invoice number."""
        return self.invoice_number.text().strip()
    
    def get_invoice_date_string(self) -> str:
        """Get invoice date as formatted string."""
        return self.invoice_date.date().toString("yyyy-MM-dd")
    
    def get_invoice_type(self) -> str:
        """Get invoice type."""
        return self.invoice_type.currentText().strip()
