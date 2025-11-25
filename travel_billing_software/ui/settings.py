"""
Settings Page for Travel Agency Billing Software
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QFrame, QScrollArea, QGridLayout, QPushButton, QDoubleSpinBox, QMessageBox,
    QListWidget, QInputDialog
)
from PyQt5.QtCore import Qt
import os
import json

from numpy import size


class SettingsPage(QWidget):
    """Settings page for configuring company and invoice settings."""
    
    def __init__(self, colors, company_info, invoice_config, get_input_style, get_spinbox_style, 
                 get_button_style, get_scrollarea_style, db=None):
        super().__init__()
        self.COLORS = colors
        self.COMPANY_INFO = company_info
        self.INVOICE_CONFIG = invoice_config
        self.get_input_style = get_input_style
        self.get_spinbox_style = get_spinbox_style
        self.get_button_style = get_button_style
        self.get_scrollarea_style = get_scrollarea_style
        self.db = db
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
        
        company_title = QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:25px;'>🏢 Company Information</b>")
        company_layout.addWidget(company_title, 0, 0, 1, 2)
        
        # Company Name
        lbl_company = QLabel("Company Name:")
        lbl_company.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        lbl_company.setFixedWidth(250)
        company_layout.addWidget(lbl_company, 1, 0)
        self.settings_company_name = QLineEdit(self.COMPANY_INFO['name'])
        self.settings_company_name.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_company_name, 1, 1)
        
        # Address
        lbl_address = QLabel("Address:")
        lbl_address.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        lbl_address.setFixedWidth(250)
        company_layout.addWidget(lbl_address, 2, 0)
        self.settings_address = QLineEdit(self.COMPANY_INFO.get('address', ''))
        self.settings_address.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_address, 2, 1)
        
        # Email
        lbl_email = QLabel("Email:")
        lbl_email.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        lbl_email.setFixedWidth(250)
        company_layout.addWidget(lbl_email, 3, 0)
        self.settings_email = QLineEdit(self.COMPANY_INFO['email'])
        self.settings_email.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_email, 3, 1)
        
        # Phone
        lbl_phone = QLabel("Phone:")
        lbl_phone.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        lbl_phone.setFixedWidth(250)
        company_layout.addWidget(lbl_phone, 4, 0)
        self.settings_phone = QLineEdit(self.COMPANY_INFO['phone'])
        self.settings_phone.setStyleSheet(self.get_input_style())
        company_layout.addWidget(self.settings_phone, 4, 1)
        
        # GST Number
        lbl_gst = QLabel("GST Number:")
        lbl_gst.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;  font-size:20px;")
        lbl_gst.setFixedWidth(250)
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
        
        invoice_title = QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:25px;'>📝 Invoice Configuration</b>")
        invoice_layout.addWidget(invoice_title, 0, 0, 1, 2)
        
        # Invoice Prefix
        lbl_prefix = QLabel("Invoice Prefix:")
        lbl_prefix.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        lbl_prefix.setFixedWidth(250)
        invoice_layout.addWidget(lbl_prefix, 1, 0)
        self.settings_prefix = QLineEdit(self.INVOICE_CONFIG['number_prefix'])
        self.settings_prefix.setStyleSheet(self.get_input_style())
        invoice_layout.addWidget(self.settings_prefix, 1, 1)
        
        # Currency Symbol
        lbl_currency = QLabel("Currency Symbol:")
        lbl_currency.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        lbl_currency.setFixedWidth(250)
        invoice_layout.addWidget(lbl_currency, 2, 0)
        self.settings_currency = QLineEdit(self.INVOICE_CONFIG['currency_symbol'])
        self.settings_currency.setStyleSheet(self.get_input_style())
        invoice_layout.addWidget(self.settings_currency, 2, 1)
        
        # Default Tax Rate
        lbl_tax = QLabel("Default Tax Rate (%):")
        lbl_tax.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        lbl_tax.setFixedWidth(250)
        invoice_layout.addWidget(lbl_tax, 3, 0)
        self.settings_tax = QDoubleSpinBox()
        self.settings_tax.setValue(self.INVOICE_CONFIG['default_tax_rate'])
        self.settings_tax.setMaximum(100)
        self.settings_tax.setStyleSheet(self.get_spinbox_style())
        invoice_layout.addWidget(self.settings_tax, 3, 1)
        
        layout.addWidget(invoice_frame)
    

        # === DROPDOWN ITEMS MANAGEMENT ===
        dropdown_frame = QFrame()
        dropdown_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLORS['secondary_bg']};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        dropdown_layout = QVBoxLayout(dropdown_frame)
        dropdown_layout.setContentsMargins(0, 0, 0, 0)
        dropdown_layout.setSpacing(15)
        
        dropdown_title = QLabel(f"<b style='color:{self.COLORS['accent_primary']}; font-size:25px;'>📋 Dropdown Items Management</b>")
        dropdown_layout.addWidget(dropdown_title)
        
        # Suppliers Section
        suppliers_layout = QVBoxLayout()
        suppliers_label = QLabel("Suppliers:")
        suppliers_label.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        suppliers_layout.addWidget(suppliers_label)
        
        # Input field with Add button attached
        suppliers_action_layout = QHBoxLayout()
        suppliers_action_layout.setSpacing(10)
        self.supplier_input = QLineEdit()
        self.supplier_input.setPlaceholderText("Enter new supplier name...")
        self.supplier_input.setStyleSheet(self.get_input_style())
        suppliers_action_layout.addWidget(self.supplier_input)
        
        remove_supplier_btn = QPushButton("➖ Remove")
        remove_supplier_btn.setStyleSheet(self.get_button_style('remove'))
        remove_supplier_btn.setCursor(Qt.PointingHandCursor)
        remove_supplier_btn.clicked.connect(lambda: self.remove_dropdown_item('supplier'))
        remove_supplier_btn.setFixedWidth(120)
        suppliers_action_layout.addWidget(remove_supplier_btn)
        remove_supplier_btn.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #B71C1C;
            }
        """)


        edit_supplier_btn = QPushButton("✏️ Edit")
        edit_supplier_btn.setStyleSheet(self.get_button_style('edit'))
        edit_supplier_btn.setCursor(Qt.PointingHandCursor)
        edit_supplier_btn.clicked.connect(lambda: self.edit_dropdown_item('supplier'))
        edit_supplier_btn.setFixedWidth(120)
        suppliers_action_layout.addWidget(edit_supplier_btn)
        suppliers_layout.addLayout(suppliers_action_layout)
        # add_supplier_btn = QPushButton("➕ Add")
        # add_supplier_btn.setStyleSheet(self.get_button_style('add'))
        # add_supplier_btn.setCursor(Qt.PointingHandCursor)
        # add_supplier_btn.clicked.connect(lambda: self.add_dropdown_item('supplier'))
        # add_supplier_btn.setFixedWidth(100)
        # suppliers_input_layout.addWidget(add_supplier_btn)
        # suppliers_layout.addLayout(suppliers_input_layout)
        
        # Remove and Edit buttons on separate row
        suppliers_action_layout = QHBoxLayout()
        suppliers_action_layout.addStretch()
    # def add_dropdown_item(self, item_type):
    #     text = ""

    #     if item_type == "supplier":
    #         text = self.supplier_input.text().strip()

    #     if text == "":
    #         QMessageBox.warning(self, "Warning", "Please enter a value before adding!")
    #         return

    #     # Save to DB
    #     self.db.insert_dropdown_item(item_type, text)

    #     # Clear textbox
    #     if item_type == "supplier":
    #         self.supplier_input.clear()

    #     # Refresh list
    #     self.load_dropdown_items()
 
        add_supplier_btn = QPushButton("➕ Add")
        add_supplier_btn.setStyleSheet(self.get_button_style('add'))
        add_supplier_btn.setCursor(Qt.PointingHandCursor)
        add_supplier_btn.clicked.connect(lambda: self.add_dropdown_item('supplier'))
        add_supplier_btn.setFixedWidth(100)
        suppliers_action_layout.addWidget(add_supplier_btn)
        suppliers_layout.addLayout(suppliers_action_layout)
        

        # List widget for displaying and selecting items
        self.suppliers_list = QListWidget()
        self.suppliers_list.setStyleSheet(f"""
            QListWidget {{
                color: {self.COLORS['text_secondary']};
                background: {self.COLORS['primary_bg']};
                border: 4px solid #444;
                border-radius: 8px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 5px;
                border-radius: 8px;
            }}
            QListWidget::item:selected {{
                background-color: {self.COLORS['accent_primary']};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {self.COLORS['secondary_bg']};
            }}
        """)
        # self.suppliers_list.setMaximumHeight(150)
        self.suppliers_list.setMinimumHeight(150)
        self.suppliers_list.setMaximumHeight(300)
        self.suppliers_list.setFixedHeight(160)

        suppliers_layout.addWidget(self.suppliers_list)
        dropdown_layout.addLayout(suppliers_layout)
        
        # Sectors Section
        # sectors_layout = QVBoxLayout()
        # sectors_label = QLabel("Sectors:")
        # sectors_label.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        # sectors_layout.addWidget(sectors_label)
        
        # sectors_input_layout = QHBoxLayout()
        # self.sector_input = QLineEdit()
        # self.sector_input.setPlaceholderText("Enter new sector...")
        # self.sector_input.setStyleSheet(self.get_input_style())
        # sectors_input_layout.addWidget(self.sector_input)
        
        # add_sector_btn = QPushButton("➕ Add")
        # add_sector_btn.setStyleSheet(self.get_button_style('add'))
        # add_sector_btn.setCursor(Qt.PointingHandCursor)
        # add_sector_btn.clicked.connect(lambda: self.add_dropdown_item('sector'))
        # sectors_input_layout.addWidget(add_sector_btn)
        # sectors_layout.addLayout(sectors_input_layout)
        

        # remove_sector_btn = QPushButton("➖ Remove")
        # remove_sector_btn.setStyleSheet(self.get_button_style('remove'))
        # remove_sector_btn.setCursor(Qt.PointingHandCursor)
        # remove_sector_btn.clicked.connect(lambda: self.remove_dropdown_item('sector'))
        # sectors_input_layout.addWidget(remove_sector_btn)
        # sectors_layout.addLayout(sectors_input_layout)
 

        # edit_sector_btn = QPushButton(" Edit")
        # edit_sector_btn.setStyleSheet(self.get_button_style('edit'))
        # edit_sector_btn.setCursor(Qt.PointingHandCursor)
        # edit_sector_btn.clicked.connect(lambda: self.edit_dropdown_item('sector'))
        # sectors_input_layout.addWidget(edit_sector_btn)
        # sectors_layout.addLayout(sectors_input_layout)

        # self.sectors_list = QLabel()
        # self.sectors_list.setWordWrap(True)
        # self.sectors_list.setStyleSheet(f"color: {self.COLORS['text_secondary']}; padding: 10px; background: {self.COLORS['primary_bg']}; border-radius: 5px;")
        # sectors_layout.addWidget(self.sectors_list)
        # dropdown_layout.addLayout(sectors_layout)
        
        # Types Section
        # types_layout = QVBoxLayout()
        # types_label = QLabel("Types:")
        # types_label.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold;")
        # types_layout.addWidget(types_label)
        
        # types_input_layout = QHBoxLayout()
        # self.type_input = QLineEdit()
        # self.type_input.setPlaceholderText("Enter new type...")
        # self.type_input.setStyleSheet(self.get_input_style())
        # types_input_layout.addWidget(self.type_input)
        
        # add_type_btn = QPushButton("➕ Add")
        # add_type_btn.setStyleSheet(self.get_button_style('add'))
        # add_type_btn.setCursor(Qt.PointingHandCursor)
        # add_type_btn.clicked.connect(lambda: self.add_dropdown_item('type'))
        # types_input_layout.addWidget(add_type_btn)
        # types_layout.addLayout(types_input_layout)

        # remove_type_btn = QPushButton("➖ Remove")
        # remove_type_btn.setStyleSheet(self.get_button_style('remove'))
        # remove_type_btn.setCursor(Qt.PointingHandCursor)
        # remove_type_btn.clicked.connect(lambda: self.remove_dropdown_item('type'))
        # types_input_layout.addWidget(remove_type_btn)
        # types_layout.addLayout(types_input_layout)
        
        # edit_type_btn = QPushButton(" Edit")
        # edit_type_btn.setStyleSheet(self.get_button_style('edit'))
        # edit_type_btn.setCursor(Qt.PointingHandCursor)
        # edit_type_btn.clicked.connect(lambda: self.edit_dropdown_item('type'))
        # types_input_layout.addWidget(edit_type_btn)
        # types_layout.addLayout(types_input_layout)

        # self.types_list = QLabel()
        # self.types_list.setWordWrap(True)
        # self.types_list.setStyleSheet(f"color: {self.COLORS['text_secondary']}; padding: 10px; background: {self.COLORS['primary_bg']}; border-radius: 5px;")
        # types_layout.addWidget(self.types_list)
        # dropdown_layout.addLayout(types_layout)
        
        # Classes Section
        classes_layout = QVBoxLayout()
        classes_label = QLabel("Travel Classes:")
        classes_label.setStyleSheet(f"color: {self.COLORS['text_primary']}; font-weight: bold; font-size:20px;")
        classes_layout.addWidget(classes_label)
        
        # Input field with Add button attached
        classes_action_layout = QHBoxLayout()
        classes_action_layout.setSpacing(10)

        self.class_input = QLineEdit()
        self.class_input.setPlaceholderText("Enter new class...")
        self.class_input.setStyleSheet(self.get_input_style())
        classes_action_layout.addWidget(self.class_input)

        remove_class_btn = QPushButton("➖ Remove")
        remove_class_btn.setStyleSheet(self.get_button_style('remove'))
        # remove_class_btn.setCursor(Qt.PointingHandCursor)
        remove_class_btn.clicked.connect(lambda: self.remove_dropdown_item('class'))
        remove_class_btn.setFixedWidth(120)
        classes_action_layout.addWidget(remove_class_btn)
        # classes_layout.addLayout(classes_action_layout)
        remove_class_btn.setStyleSheet("""
            QPushButton {_
                background-color: #E53935;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #B71C1C;
            }
        """)
        
        edit_class_btn = QPushButton("✏️ Edit")
        edit_class_btn.setStyleSheet(self.get_button_style('edit'))
        # edit_class_btn.setCursor(Qt.PointingHandCursor)
        edit_class_btn.clicked.connect(lambda: self.edit_dropdown_item('class'))
        edit_class_btn.setFixedWidth(120)
        classes_action_layout.addWidget(edit_class_btn)
        classes_layout.addLayout(classes_action_layout)




        classes_action_layout = QHBoxLayout()
        classes_action_layout.addStretch()


        # 

        add_class_btn = QPushButton("➕ Add")
        add_class_btn.setStyleSheet(self.get_button_style('add'))
        # add_class_btn.setCursor(Qt.PointingHandCursor)
        add_class_btn.clicked.connect(lambda: self.add_dropdown_item('class'))
        add_class_btn.setFixedWidth(100)
        classes_action_layout.addWidget(add_class_btn)

        # classes_action_layout.addWidget(self.class_input)
        # classes_action_layout.addWidget(remove_class_btn)
        # classes_action_layout.addWidget(edit_class_btn)
        # classes_action_layout.addWidget(add_class_btn)


        classes_layout.addLayout(classes_action_layout)
        
       

        # classes_action_layout = QHBoxLayout()
        self.classes_list = QListWidget()
        self.classes_list.setStyleSheet(f"""
            QListWidget {{
                color: {self.COLORS['text_secondary']};
                background: {self.COLORS['primary_bg']};
                border: 4px solid #444;
                border-radius: 10px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 5px;
                border-radius: 8px;
            }}
            QListWidget::item:selected {{
                background-color: {self.COLORS['accent_primary']};
                color: white;
            }}
            QListWidget::item:hover {{
                background-color: {self.COLORS['secondary_bg']};
            }}
        """)
        # self.classes_list.setMaximumHeight(220)
        self.classes_list.setMinimumHeight(150)
        self.classes_list.setMaximumHeight(300)
        self.classes_list.setFixedHeight(160)


        classes_layout.addWidget(self.classes_list)


        dropdown_layout.addLayout(classes_layout)

        # classes_action_layout = QHBoxLayout()
        # classes_action_layout.addStretch()

        
        layout.addWidget(dropdown_frame)
        
        # Load initial dropdown items
        self.load_dropdown_items()
        
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
    
    def load_dropdown_items(self):
        """Load dropdown items from database (preferred) or JSON file."""
        try:
            # Try loading from database first
            if self.db:
                self.suppliers = self.db.get_dropdown_items('supplier')
                self.classes = self.db.get_dropdown_items('class')
                
                # Initialize defaults if database is empty
                if not self.suppliers:
                    self.db.initialize_default_dropdowns()
                    self.suppliers = self.db.get_dropdown_items('supplier')
                    self.classes = self.db.get_dropdown_items('class')
            else:
                # Fallback to JSON file
                if os.path.exists('dropdown_items.json'):
                    with open('dropdown_items.json', 'r') as f:
                        data = json.load(f)
                        self.suppliers = data.get('suppliers', ['Emirates Airlines', 'Qatar Airways', 'Air India'])
                        self.classes = data.get('classes', ['Economy', 'Premium Economy', 'Business', 'First Class'])
                else:
                    self.suppliers = ['Emirates Airlines', 'Qatar Airways', 'Air India']
                    self.classes = ['Economy', 'Premium Economy', 'Business', 'First Class']
            
            self.update_dropdown_displays()
        except Exception as e:
            print(f"Error loading dropdown items: {e}")
    
    def update_dropdown_displays(self):
        """Update the display of dropdown items."""
        self.suppliers_list.clear()
        self.suppliers_list.addItems(self.suppliers)
        self.classes_list.clear()
        self.classes_list.addItems(self.classes)
    
    def add_dropdown_item(self, item_type):
        """Add new item to dropdown list."""
        try:
            new_item = None
            if item_type == 'supplier':
                new_item = self.supplier_input.text().strip()
                if new_item and new_item not in self.suppliers:
                    if self.db:
                        if self.db.add_dropdown_item('supplier', new_item):
                            self.suppliers.append(new_item)
                            self.supplier_input.clear()
                        else:
                            QMessageBox.warning(self, "Duplicate", "This supplier already exists.")
                            return
                    else:
                        self.suppliers.append(new_item)
                        self.supplier_input.clear()
            elif item_type == 'class':
                new_item = self.class_input.text().strip()
                if new_item and new_item not in self.classes:
                    if self.db:
                        if self.db.add_dropdown_item('class', new_item):
                            self.classes.append(new_item)
                            self.class_input.clear()
                        else:
                            QMessageBox.warning(self, "Duplicate", "This class already exists.")
                            return
                    else:
                        self.classes.append(new_item)
                        self.class_input.clear()
            
            if not new_item:
                QMessageBox.warning(self, "Empty Field", "Please enter a value.")
                return
                
            self.save_dropdown_items()
            self.update_dropdown_displays()
            QMessageBox.information(self, "Success", f"{item_type.capitalize()} added successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add item:\n{str(e)}")
    
    def save_dropdown_items(self):
        """Save dropdown items to JSON file."""
        try:
            data = {
                'suppliers': self.suppliers,
                'classes': self.classes
            }
            with open('dropdown_items.json', 'w') as f:
                json.dump(data, f, indent=4)
            print("✓ Dropdown items saved")
        except Exception as e:
            print(f"Error saving dropdown items: {e}")
    
    def remove_dropdown_item(self, item_type):
        """Remove selected item from dropdown list."""
        try:
            item_text = None
            if item_type == 'supplier':
                current_item = self.suppliers_list.currentItem()
                if current_item:
                    item_text = current_item.text()
                    if self.db:
                        if self.db.delete_dropdown_item('supplier', item_text):
                            self.suppliers.remove(item_text)
                        else:
                            QMessageBox.warning(self, "Error", "Failed to remove from database.")
                            return
                    else:
                        self.suppliers.remove(item_text)
                else:
                    QMessageBox.warning(self, "No Selection", "Please select a supplier to remove.")
                    return
            elif item_type == 'class':
                current_item = self.classes_list.currentItem()
                if current_item:
                    item_text = current_item.text()
                    if self.db:
                        if self.db.delete_dropdown_item('class', item_text):
                            self.classes.remove(item_text)
                        else:
                            QMessageBox.warning(self, "Error", "Failed to remove from database.")
                            return
                    else:
                        self.classes.remove(item_text)
                else:
                    QMessageBox.warning(self, "No Selection", "Please select a class to remove.")
                    return
            
            self.save_dropdown_items()
            self.update_dropdown_displays()
            QMessageBox.information(self, "Success", f"Item removed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to remove item:\n{str(e)}")
    
    def edit_dropdown_item(self, item_type):
        """Edit selected item in dropdown list."""
        try:
            if item_type == 'supplier':
                current_item = self.suppliers_list.currentItem()
                if current_item:
                    old_text = current_item.text()
                    new_text, ok = QInputDialog.getText(
                        self, "Edit Supplier", "Enter new supplier name:", 
                        QLineEdit.Normal, old_text
                    )
                    if ok and new_text.strip():
                        if self.db:
                            if self.db.update_dropdown_item('supplier', old_text, new_text.strip()):
                                idx = self.suppliers.index(old_text)
                                self.suppliers[idx] = new_text.strip()
                            else:
                                QMessageBox.warning(self, "Error", "Failed to update in database.")
                                return
                        else:
                            idx = self.suppliers.index(old_text)
                            self.suppliers[idx] = new_text.strip()
                    else:
                        return
                else:
                    QMessageBox.warning(self, "No Selection", "Please select a supplier to edit.")
                    return
            elif item_type == 'class':
                current_item = self.classes_list.currentItem()
                if current_item:
                    old_text = current_item.text()
                    new_text, ok = QInputDialog.getText(
                        self, "Edit Class", "Enter new class name:", 
                        QLineEdit.Normal, old_text
                    )
                    if ok and new_text.strip():
                        if self.db:
                            if self.db.update_dropdown_item('class', old_text, new_text.strip()):
                                idx = self.classes.index(old_text)
                                self.classes[idx] = new_text.strip()
                            else:
                                QMessageBox.warning(self, "Error", "Failed to update in database.")
                                return
                        else:
                            idx = self.classes.index(old_text)
                            self.classes[idx] = new_text.strip()
                    else:
                        return
                else:
                    QMessageBox.warning(self, "No Selection", "Please select a class to edit.")
                    return
            
            self.save_dropdown_items()
            self.update_dropdown_displays()
            QMessageBox.information(self, "Success", f"Item updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit item:\n{str(e)}")
