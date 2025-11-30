"""
Settings Page for Travel Agency Billing Software
Updated for Dynamic Persistence and Global Styling
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QFrame, QScrollArea, QGridLayout, QPushButton, QDoubleSpinBox, QMessageBox,
    QListWidget, QInputDialog, QSpinBox, QComboBox, QApplication
)
from PyQt6.QtCore import Qt
from utils.config_manager import ConfigManager

class SettingsPage(QWidget):
    """Settings page for configuring company, invoice, and app appearance."""
    
    def __init__(self, colors, company_info, invoice_config, get_input_style, get_spinbox_style, 
                 get_button_style, get_scrollarea_style, db=None, main_window_ref=None):
        super().__init__()
        self.config_manager = ConfigManager()
        
        # Load live data from ConfigManager instead of static arguments
        self.COMPANY_INFO = self.config_manager.get_company_info()
        self.INVOICE_CONFIG = self.config_manager.get_invoice_config()
        self.APP_SETTINGS = self.config_manager.get_app_settings()
        
        # Keep style references (we will regenerate them later)
        self.COLORS = colors
        self.get_input_style = get_input_style
        self.get_spinbox_style = get_spinbox_style
        self.get_button_style = get_button_style
        self.get_scrollarea_style = get_scrollarea_style
        self.db = db
        self.main_window = main_window_ref # Reference to Dashboard to trigger refreshes

        self.init_ui()
    
    def init_ui(self):
        """Initialize the Settings page UI."""
        # Clear existing layout if re-initializing
        if self.layout():
            QWidget().setLayout(self.layout())
            
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        heading = QLabel(f"<h2 style='color:{self.COLORS['accent_secondary']};'>⚙️ Settings</h2>")
        main_layout.addWidget(heading)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self.get_scrollarea_style())
        
        settings_widget = QWidget()
        self.content_layout = QVBoxLayout(settings_widget)
        self.content_layout.setSpacing(20)

        # 1. APPLICATION APPEARANCE (New Feature)
        self._create_appearance_section()

        # 2. COMPANY SETTINGS
        self._create_company_section()

        # 3. INVOICE SETTINGS
        self._create_invoice_section()

        # 4. DROPDOWN MANAGEMENT
        self._create_dropdown_section()
        
        # Save Button
        save_btn_layout = QHBoxLayout()
        save_btn_layout.addStretch()
        
        save_settings_btn = QPushButton("💾 Save All Settings")
        save_settings_btn.setStyleSheet(self.get_button_style('save'))
        save_settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        save_settings_btn.clicked.connect(self.save_all_settings)
        save_btn_layout.addWidget(save_settings_btn)
        
        self.content_layout.addLayout(save_btn_layout)
        self.content_layout.addStretch()
        
        scroll.setWidget(settings_widget)
        main_layout.addWidget(scroll)

    def _create_frame_style(self):
        return f"""
            QFrame {{
                background-color: {self.COLORS['secondary_bg']};
                border-radius: 8px;
                padding: 20px;
                border: 1px solid #333;
            }}
        """

    def _create_appearance_section(self):
        frame = QFrame()
        frame.setStyleSheet(self._create_frame_style())
        layout = QGridLayout(frame)
        
        title = QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:18px;'>🎨 Appearance</b>")
        layout.addWidget(title, 0, 0, 1, 2)

        # Font Size
        lbl_font = QLabel("Global Font Size (px):")
        lbl_font.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        
        self.spin_font_size = QSpinBox()
        self.spin_font_size.setRange(8, 24)
        self.spin_font_size.setValue(self.APP_SETTINGS.get('font_size', 12))
        self.spin_font_size.setStyleSheet(self.get_spinbox_style())
        
        layout.addWidget(lbl_font, 1, 0)
        layout.addWidget(self.spin_font_size, 1, 1)

        # Theme Accent (Simple Dropdown for now)
        lbl_theme = QLabel("Accent Color:")
        lbl_theme.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Purple", "Blue", "Green", "Orange", "Red"])
        # Map current color to index logic here if needed
        self.combo_theme.setStyleSheet(f"""
            QComboBox {{ background-color: #333; color: white; padding: 5px; border-radius: 5px; }}
        """)

        layout.addWidget(lbl_theme, 2, 0)
        layout.addWidget(self.combo_theme, 2, 1)
        
        # Note
        lbl_note = QLabel("<i>Note: Some appearance changes may require a restart.</i>")
        lbl_note.setStyleSheet("color: #888;")
        layout.addWidget(lbl_note, 3, 0, 1, 2)

        self.content_layout.addWidget(frame)

    def _create_company_section(self):
        frame = QFrame()
        frame.setStyleSheet(self._create_frame_style())
        layout = QGridLayout(frame)
        
        title = QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:18px;'>🏢 Company Information</b>")
        layout.addWidget(title, 0, 0, 1, 2)
        
        fields = [
            ("Company Name:", "name"),
            ("Address:", "address"),
            ("Email:", "email"),
            ("Phone:", "phone"),
            ("GST Number:", "gst_number")
        ]
        
        self.company_inputs = {}
        
        for i, (label_text, key) in enumerate(fields, 1):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
            
            inp = QLineEdit(str(self.COMPANY_INFO.get(key, "")))
            inp.setStyleSheet(self.get_input_style())
            
            layout.addWidget(lbl, i, 0)
            layout.addWidget(inp, i, 1)
            self.company_inputs[key] = inp
            
        self.content_layout.addWidget(frame)

    def _create_invoice_section(self):
        frame = QFrame()
        frame.setStyleSheet(self._create_frame_style())
        layout = QGridLayout(frame)
        
        title = QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:18px;'>📝 Invoice Configuration</b>")
        layout.addWidget(title, 0, 0, 1, 2)
        
        # Prefix
        layout.addWidget(QLabel("Invoice Prefix:", styleSheet=f"color:{self.COLORS['text_primary']}; font-weight:bold;"), 1, 0)
        self.inp_prefix = QLineEdit(self.INVOICE_CONFIG.get('prefix', 'INV'))
        self.inp_prefix.setStyleSheet(self.get_input_style())
        layout.addWidget(self.inp_prefix, 1, 1)

        # Currency
        layout.addWidget(QLabel("Currency Symbol:", styleSheet=f"color:{self.COLORS['text_primary']}; font-weight:bold;"), 2, 0)
        self.inp_currency = QLineEdit(self.INVOICE_CONFIG.get('currency_symbol', '₹'))
        self.inp_currency.setStyleSheet(self.get_input_style())
        layout.addWidget(self.inp_currency, 2, 1)

        # Tax
        layout.addWidget(QLabel("Default Tax Rate (%):", styleSheet=f"color:{self.COLORS['text_primary']}; font-weight:bold;"), 3, 0)
        self.spin_tax = QDoubleSpinBox()
        self.spin_tax.setValue(float(self.INVOICE_CONFIG.get('default_tax_rate', 18.0)))
        self.spin_tax.setMaximum(100)
        self.spin_tax.setStyleSheet(self.get_spinbox_style())
        layout.addWidget(self.spin_tax, 3, 1)
        
        self.content_layout.addWidget(frame)

    def _create_dropdown_section(self):
        frame = QFrame()
        frame.setStyleSheet(self._create_frame_style())
        layout = QVBoxLayout(frame)
        
        layout.addWidget(QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:18px;'>📋 Dropdown Management</b>"))

        # Helper to create list sections
        def create_list_manager(title, key):
            lbl = QLabel(title)
            lbl.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size: 16px;")
            layout.addWidget(lbl)
            
            row = QHBoxLayout()
            inp = QLineEdit()
            inp.setPlaceholderText(f"Add new {title.lower().strip(':')}...")
            inp.setStyleSheet(self.get_input_style())
            
            btn_add = QPushButton("➕")
            btn_add.setFixedWidth(70)
            btn_add.setStyleSheet(self.get_button_style('add'))
            
            row.addWidget(inp)
            row.addWidget(btn_add)
            layout.addLayout(row)
            
            lst = QListWidget()
            lst.setFixedHeight(200)
            lst.setStyleSheet(f"background: {self.COLORS['primary_bg']}; color: #ddd; border: 1px solid #444; border-radius: 4px;")
            
            # Load items
            items = self.config_manager.get_dropdowns(key)
            lst.addItems(items)
            
            layout.addWidget(lst)
            
            # Remove Button
            btn_remove = QPushButton("➖ Remove Selected")
            btn_remove.setStyleSheet("""
                QPushButton { background-color: #ef4444; color: white; border-radius: 4px; padding: 5px; }
                QPushButton:hover { background-color: #dc2626; }
            """)
            layout.addWidget(btn_remove)
            
            # Logic Connections
            def add_item():
                text = inp.text().strip()
                if text:
                    if self.config_manager.add_dropdown_item(key, text):
                        lst.addItem(text)
                        inp.clear()
                    else:
                        QMessageBox.warning(self, "Exists", "Item already exists.")
            
            def remove_item():
                row = lst.currentRow()
                if row >= 0:
                    item = lst.item(row).text()
                    if self.config_manager.remove_dropdown_item(key, item):
                        lst.takeItem(row)

            btn_add.clicked.connect(add_item)
            btn_remove.clicked.connect(remove_item)

        create_list_manager("Suppliers:", "suppliers")
        layout.addSpacing(10)
        create_list_manager("Travel Classes:", "classes")
        
        self.content_layout.addWidget(frame)

    def save_all_settings(self):
        """Persist all settings to config.json and trigger updates."""
        try:
            # 1. Update Company Info
            company_data = {k: v.text() for k, v in self.company_inputs.items()}
            self.config_manager.set_company_info(company_data)

            # 2. Update Invoice Config
            invoice_data = {
                "prefix": self.inp_prefix.text(),
                "currency_symbol": self.inp_currency.text(),
                "default_tax_rate": self.spin_tax.value(),
                "terms": self.INVOICE_CONFIG.get("terms", "") # Preserve terms
            }
            self.config_manager.set_invoice_config(invoice_data)

            # 3. Update App Settings (Font Size)
            new_font_size = self.spin_font_size.value()
            self.config_manager.set_app_setting("font_size", new_font_size)
            
            # 4. Apply Changes Globally
            self.apply_global_styles(new_font_size)

            QMessageBox.information(self, "Saved", "Settings saved successfully!\nUI updated.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")

    def apply_global_styles(self, font_size):
        """
        Dynamically update the application stylesheet.
        This forces the font size to reflect 'everywhere'.
        """
        app = QApplication.instance()
        if app:
            # We construct a generic stylesheet that forces font size on common widgets
            style = f"""
                QWidget {{ font-size: {font_size}px; font-family: 'Segoe UI', Arial; }}
                QLabel {{ font-size: {font_size}px; }}
                QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{ 
                    font-size: {font_size}px; min-height: {font_size + 10}px; 
                }}
                QPushButton {{ font-size: {font_size}px; }}
                QTableWidget {{ font-size: {font_size}px; }}
                QHeaderView::section {{ font-size: {font_size}px; }}
            """
            # Append to existing stylesheet if possible, or replace
            # For this simple implementation, we assume we can append or set
            # But usually, it's better to update the main window's style method.
            
            # If main_window reference exists, call its theme applicator
            if self.main_window and hasattr(self.main_window, 'apply_dark_theme'):
                # We need to hack the main window to accept a font size, 
                # OR set a global variable that main window reads.
                pass 
            
            # Direct application (Brute force method to ensure it works)
            app.setStyleSheet(app.styleSheet() + style)