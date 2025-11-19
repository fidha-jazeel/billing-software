"""
Settings Page for Travel Agency Billing Software
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QFrame, QScrollArea, QGridLayout, QPushButton, QDoubleSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt


class SettingsPage(QWidget):
    """Settings page for configuring company and invoice settings."""
    
    def __init__(self, colors, company_info, invoice_config, get_input_style, get_spinbox_style, 
                 get_button_style, get_scrollarea_style):
        super().__init__()
        self.COLORS = colors
        self.COMPANY_INFO = company_info
        self.INVOICE_CONFIG = invoice_config
        self.get_input_style = get_input_style
        self.get_spinbox_style = get_spinbox_style
        self.get_button_style = get_button_style
        self.get_scrollarea_style = get_scrollarea_style
        self.init_ui()
    
    def init_ui(self):
        """Initialize the Settings page UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        heading = QLabel(f"<h2 style='color:{self.COLORS['accent_secondary']};'>⚙️ Settings</h2>")
        main_layout.addWidget(heading)
        
        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self.get_scrollarea_style())
        
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        layout.setSpacing(20)

        # === COMPANY SETTINGS ===
        company_frame = QFrame()
        company_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLORS['secondary_bg']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        company_layout = QGridLayout(company_frame)
        company_layout.setContentsMargins(0, 0, 0, 0)
        company_layout.setSpacing(15)
        
        company_title = QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:14px;'>🏢 Company Information</b>")
        company_layout.addWidget(company_title, 0, 0, 1, 2)
        
        # Company Name
        lbl_company = QLabel("Company Name:")
        lbl_company.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        lbl_company.setFixedWidth(150)
        company_layout.addWidget(lbl_company, 1, 0)
        self.settings_company_name = QLineEdit(self.COMPANY_INFO['name'])
        self.settings_company_name.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_company_name, 1, 1)
        
        # Address
        lbl_address = QLabel("Address:")
        lbl_address.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        lbl_address.setFixedWidth(150)
        company_layout.addWidget(lbl_address, 2, 0)
        self.settings_address = QLineEdit(self.COMPANY_INFO.get('address', ''))
        self.settings_address.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_address, 2, 1)
        
        # Email
        lbl_email = QLabel("Email:")
        lbl_email.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        lbl_email.setFixedWidth(150)
        company_layout.addWidget(lbl_email, 3, 0)
        self.settings_email = QLineEdit(self.COMPANY_INFO['email'])
        self.settings_email.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_email, 3, 1)
        
        # Phone
        lbl_phone = QLabel("Phone:")
        lbl_phone.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        lbl_phone.setFixedWidth(150)
        company_layout.addWidget(lbl_phone, 4, 0)
        self.settings_phone = QLineEdit(self.COMPANY_INFO['phone'])
        self.settings_phone.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_phone, 4, 1)
        
        # GST Number
        lbl_gst = QLabel("GST Number:")
        lbl_gst.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        lbl_gst.setFixedWidth(150)
        company_layout.addWidget(lbl_gst, 5, 0)
        self.settings_gst = QLineEdit(self.COMPANY_INFO.get('gst_number', ''))
        self.settings_gst.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_gst, 5, 1)
        
        layout.addWidget(company_frame)

        # === INVOICE SETTINGS ===
        invoice_frame = QFrame()
        invoice_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLORS['secondary_bg']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        invoice_layout = QGridLayout(invoice_frame)
        invoice_layout.setContentsMargins(0, 0, 0, 0)
        invoice_layout.setSpacing(15)
        
        invoice_title = QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:14px;'>📝 Invoice Configuration</b>")
        invoice_layout.addWidget(invoice_title, 0, 0, 1, 2)
        
        # Invoice Prefix
        lbl_prefix = QLabel("Invoice Prefix:")
        lbl_prefix.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        lbl_prefix.setFixedWidth(150)
        invoice_layout.addWidget(lbl_prefix, 1, 0)
        self.settings_prefix = QLineEdit(self.INVOICE_CONFIG['number_prefix'])
        self.settings_prefix.setStyleSheet(self.get_input_style())
        invoice_layout.addWidget(self.settings_prefix, 1, 1)
        
        # Currency Symbol
        lbl_currency = QLabel("Currency Symbol:")
        lbl_currency.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        lbl_currency.setFixedWidth(150)
        invoice_layout.addWidget(lbl_currency, 2, 0)
        self.settings_currency = QLineEdit(self.INVOICE_CONFIG['currency_symbol'])
        self.settings_currency.setStyleSheet(self.get_input_style())
        invoice_layout.addWidget(self.settings_currency, 2, 1)
        
        # Default Tax Rate
        lbl_tax = QLabel("Default Tax Rate (%):")
        lbl_tax.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        lbl_tax.setFixedWidth(150)
        invoice_layout.addWidget(lbl_tax, 3, 0)
        self.settings_tax = QDoubleSpinBox()
        self.settings_tax.setValue(self.INVOICE_CONFIG['default_tax_rate'])
        self.settings_tax.setMaximum(100)
        self.settings_tax.setStyleSheet(self.get_spinbox_style())
        invoice_layout.addWidget(self.settings_tax, 3, 1)
        
        layout.addWidget(invoice_frame)
        
        # === SAVE BUTTON ===
        save_btn_layout = QHBoxLayout()
        save_btn_layout.addStretch()
        
        save_settings_btn = QPushButton("💾 Save Settings")
        save_settings_btn.setStyleSheet(self.get_button_style('save'))
        save_settings_btn.setCursor(Qt.PointingHandCursor)
        save_settings_btn.clicked.connect(self.save_settings)
        save_btn_layout.addWidget(save_settings_btn)
        
        layout.addLayout(save_btn_layout)
        layout.addStretch()
        
        scroll.setWidget(settings_widget)
        main_layout.addWidget(scroll)
    
    def save_settings(self):
        """Save settings."""
        try:
            # In a production app, you would update config files or database here
            # For now, just show confirmation
            
            settings_text = f"""Settings Updated:

Company Information:
• Name: {self.settings_company_name.text()}
• Address: {self.settings_address.text()}
• Email: {self.settings_email.text()}
• Phone: {self.settings_phone.text()}
• GST: {self.settings_gst.text()}

Invoice Configuration:
• Prefix: {self.settings_prefix.text()}
• Currency: {self.settings_currency.text()}
• Default Tax: {self.settings_tax.value()}%

Note: These settings are displayed but not persisted.
To persist settings, update config/settings.py file."""
            
            QMessageBox.information(self, "Settings Saved", settings_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings:\n{str(e)}")
