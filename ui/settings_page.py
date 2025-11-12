from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QFrame,
                             QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from database.db_manager import DatabaseManager

class SettingsPage(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("⚙️ Settings")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Company Information Section
        company_section = self.create_company_section()
        layout.addWidget(company_section)
        
        # Invoice Settings Section
        invoice_section = self.create_invoice_section()
        layout.addWidget(invoice_section)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setMinimumHeight(40)
        save_btn.setMinimumWidth(150)
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("🔄 Reset")
        reset_btn.setObjectName("secondaryBtn")
        reset_btn.setMinimumHeight(40)
        reset_btn.setMinimumWidth(120)
        reset_btn.clicked.connect(self.load_settings)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
    
    def create_company_section(self):
        """Create company information section"""
        section = QFrame()
        section.setObjectName("card")
        
        layout = QVBoxLayout(section)
        
        # Title
        title = QLabel("🏢 Company Information")
        title.setObjectName("sectionLabel")
        layout.addWidget(title)
        
        # Form grid
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        
        # Company Name
        form_layout.addWidget(QLabel("Company Name:"), 0, 0)
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Enter company name")
        form_layout.addWidget(self.company_name, 0, 1)
        
        # Company Address
        form_layout.addWidget(QLabel("Address:"), 1, 0, Qt.AlignmentFlag.AlignTop)
        self.company_address = QTextEdit()
        self.company_address.setPlaceholderText("Enter company address")
        self.company_address.setMinimumHeight(60)
        form_layout.addWidget(self.company_address, 1, 1)
        
        # Contact Number
        form_layout.addWidget(QLabel("Contact Number:"), 2, 0)
        self.company_contact = QLineEdit()
        self.company_contact.setPlaceholderText("Enter contact number")
        form_layout.addWidget(self.company_contact, 2, 1)
        
        # Email
        form_layout.addWidget(QLabel("Email:"), 3, 0)
        self.company_email = QLineEdit()
        self.company_email.setPlaceholderText("Enter email address")
        form_layout.addWidget(self.company_email, 3, 1)
        
        # GST Number
        form_layout.addWidget(QLabel("GST Number:"), 4, 0)
        self.company_gst = QLineEdit()
        self.company_gst.setPlaceholderText("Enter GST number (optional)")
        form_layout.addWidget(self.company_gst, 4, 1)
        
        layout.addLayout(form_layout)
        
        return section
    
    def create_invoice_section(self):
        """Create invoice settings section"""
        section = QFrame()
        section.setObjectName("card")
        
        layout = QVBoxLayout(section)
        
        # Title
        title = QLabel("📄 Invoice Settings")
        title.setObjectName("sectionLabel")
        layout.addWidget(title)
        
        # Form grid
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        
        # Invoice Prefix
        prefix_container = QHBoxLayout()
        form_layout.addWidget(QLabel("Invoice Prefix:"), 0, 0)
        self.invoice_prefix = QLineEdit()
        self.invoice_prefix.setPlaceholderText("e.g., INV, BILL")
        prefix_container.addWidget(self.invoice_prefix, 1)
        prefix_container.addStretch(2)
        form_layout.addLayout(prefix_container, 0, 1)
        
        help_label = QLabel("Format: PREFIX-0001, PREFIX-0002, etc.")
        help_label.setStyleSheet("color: #6a6a6a; font-size: 9pt;")
        form_layout.addWidget(help_label, 1, 1)
        
        # Currency Symbol
        currency_container = QHBoxLayout()
        form_layout.addWidget(QLabel("Currency Symbol:"), 2, 0)
        self.currency_symbol = QLineEdit()
        self.currency_symbol.setPlaceholderText("₹")
        currency_container.addWidget(self.currency_symbol, 1)
        currency_container.addStretch(4)
        form_layout.addLayout(currency_container, 2, 1)
        
        layout.addLayout(form_layout)
        
        return section
    
    def load_settings(self):
        """Load settings from database"""
        try:
            settings = self.db.get_settings()
            
            self.company_name.setText(settings.get('company_name', ''))
            self.company_address.setPlainText(settings.get('company_address', ''))
            self.company_contact.setText(settings.get('company_contact', ''))
            self.company_email.setText(settings.get('company_email', ''))
            self.company_gst.setText(settings.get('company_gst', ''))
            self.invoice_prefix.setText(settings.get('invoice_prefix', 'INV'))
            self.currency_symbol.setText(settings.get('currency_symbol', '₹'))
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load settings: {str(e)}")
    
    def save_settings(self):
        """Save settings to database"""
        try:
            settings = {
                'company_name': self.company_name.text(),
                'company_address': self.company_address.toPlainText(),
                'company_contact': self.company_contact.text(),
                'company_email': self.company_email.text(),
                'company_gst': self.company_gst.text(),
                'invoice_prefix': self.invoice_prefix.text() or 'INV',
                'currency_symbol': self.currency_symbol.text() or '₹'
            }
            
            self.db.update_settings(settings)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
