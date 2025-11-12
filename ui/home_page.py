from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
                             QDateEdit, QFrame, QGridLayout, QHeaderView, QComboBox,
                             QMessageBox, QDoubleSpinBox, QCompleter, QFileDialog, QScrollArea)
from PyQt6.QtCore import Qt, QDate, QStringListModel
from PyQt6.QtGui import QFont
from database.db_manager import DatabaseManager
from utils.pdf_generator import PDFGenerator
from datetime import datetime

class HomePage(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.pdf_generator = PDFGenerator(db_manager)
        self.current_invoice_id = None
        self.init_ui()
        self.load_initial_data()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header (Fixed at top - not scrollable)
        header_layout = QHBoxLayout()
        title = QLabel("Welcome to Travel Agency Billing")
        title.setObjectName("titleLabel")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # New Invoice button
        new_invoice_btn = QPushButton("📄 New Invoice")
        new_invoice_btn.setMinimumHeight(35)
        new_invoice_btn.clicked.connect(self.reset_form)
        header_layout.addWidget(new_invoice_btn)
        
        layout.addLayout(header_layout)
        
        # Subtitle
        subtitle = QLabel("Enter details to make your invoice 🚀")
        subtitle.setStyleSheet("font-size: 11pt; color: #a0a0a0;")
        layout.addWidget(subtitle)
        
        # Create scroll area for the main form
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Main form content widget
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(0, 0, 10, 0)  # Right margin for scrollbar
        
        # Invoice and Customer Details Section
        details_layout = QHBoxLayout()
        
        # Invoice Details Card
        invoice_card = self.create_invoice_details_card()
        details_layout.addWidget(invoice_card, 1)
        
        # Customer Details Card
        customer_card = self.create_customer_details_card()
        details_layout.addWidget(customer_card, 1)
        
        form_layout.addLayout(details_layout)
        
        # Items Table Section
        items_section = self.create_items_section()
        form_layout.addWidget(items_section)
        
        # Invoice Calculation Section
        calc_section = self.create_calculation_section()
        form_layout.addWidget(calc_section)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Save Invoice")
        save_btn.setMinimumHeight(40)
        save_btn.setMinimumWidth(150)
        save_btn.clicked.connect(self.save_invoice)
        button_layout.addWidget(save_btn)
        
        pdf_btn = QPushButton("📄 Save as PDF")
        pdf_btn.setObjectName("secondaryBtn")
        pdf_btn.setMinimumHeight(40)
        pdf_btn.setMinimumWidth(150)
        pdf_btn.clicked.connect(self.save_as_pdf)
        button_layout.addWidget(pdf_btn)
        
        form_layout.addLayout(button_layout)
        
        # Set the form widget to scroll area
        scroll_area.setWidget(form_widget)
        
        # Add scroll area to main layout
        layout.addWidget(scroll_area)
    
    def create_invoice_details_card(self):
        """Create invoice details card"""
        card = QFrame()
        card.setObjectName("card")
        
        layout = QVBoxLayout(card)
        
        # Title
        title = QLabel("📝 Invoice Details :")
        title.setObjectName("sectionLabel")
        layout.addWidget(title)
        
        # Invoice Number
        inv_layout = QHBoxLayout()
        inv_label = QLabel("Invoice Number :")
        inv_label.setMinimumWidth(120)
        self.invoice_number = QLineEdit()
        self.invoice_number.setReadOnly(True)
        self.invoice_number.setPlaceholderText("Auto-generated")
        self.invoice_number.setMinimumHeight(30)
        inv_layout.addWidget(inv_label)
        inv_layout.addWidget(self.invoice_number)
        layout.addLayout(inv_layout)
        
        # Invoice Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Invoice Date :")
        date_label.setMinimumWidth(120)
        self.invoice_date = QDateEdit()
        self.invoice_date.setCalendarPopup(True)
        self.invoice_date.setDate(QDate.currentDate())
        self.invoice_date.setDisplayFormat("dd-MM-yyyy")
        self.invoice_date.setMinimumHeight(30)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.invoice_date)
        layout.addLayout(date_layout)
        
        layout.addStretch()
        
        return card
    
    def create_customer_details_card(self):
        """Create customer details card"""
        card = QFrame()
        card.setObjectName("card")
        
        layout = QVBoxLayout(card)
        
        # Title
        title = QLabel("👤 Bill To :")
        title.setObjectName("sectionLabel")
        layout.addWidget(title)
        
        # Customer Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Customer Name* :")
        name_label.setMinimumWidth(140)
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Enter customer name")
        self.customer_name.setMinimumHeight(30)
        
        # Add autocomplete
        self.customer_completer = QCompleter()
        self.customer_name.setCompleter(self.customer_completer)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.customer_name)
        layout.addLayout(name_layout)
        
        # Contact Number
        contact_layout = QHBoxLayout()
        contact_label = QLabel("Contact Number :")
        contact_label.setMinimumWidth(140)
        self.customer_contact = QLineEdit()
        self.customer_contact.setPlaceholderText("Enter contact number")
        self.customer_contact.setMinimumHeight(30)
        contact_layout.addWidget(contact_label)
        contact_layout.addWidget(self.customer_contact)
        layout.addLayout(contact_layout)
        
        layout.addStretch()
        
        return card
    
    def create_items_section(self):
        """Create items table section"""
        section = QFrame()
        section.setObjectName("card")
        
        layout = QVBoxLayout(section)
        
        # Header with Add Item button
        header_layout = QHBoxLayout()
        title = QLabel("📋 Billed Items")
        title.setObjectName("sectionLabel")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        add_btn = QPushButton("➕ Add Item")
        add_btn.setFixedHeight(30)
        add_btn.clicked.connect(self.add_item_row)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(10)
        self.items_table.setHorizontalHeaderLabels([
            "Item Name", "Ticket #", "Sector", "Supplier", 
            "Quantity", "Price/Unit (₹)", "Tax (%)", "Tax (₹)", "Amount (₹)", "Actions"
        ])
        
        # Set column widths with proper sizing
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.items_table.setColumnWidth(1, 120)  # Ticket #
        self.items_table.setColumnWidth(2, 100)  # Sector
        self.items_table.setColumnWidth(3, 120)  # Supplier
        self.items_table.setColumnWidth(4, 80)   # Quantity
        self.items_table.setColumnWidth(5, 120)  # Price/Unit
        self.items_table.setColumnWidth(6, 80)   # Tax %
        self.items_table.setColumnWidth(7, 100)  # Tax Amount
        self.items_table.setColumnWidth(8, 120)  # Amount
        self.items_table.setColumnWidth(9, 80)   # Actions
        
        # Ensure text is not cut off
        header.setStretchLastSection(False)
        self.items_table.verticalHeader().setDefaultSectionSize(40)  # Row height
        
        # Set alternating row colors
        self.items_table.setAlternatingRowColors(True)
        
        # Remove scrollbars from table - let it grow naturally
        self.items_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.items_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Make table resize to fit all rows
        self.items_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        layout.addWidget(self.items_table)
        
        return section
    
    def create_calculation_section(self):
        """Create invoice calculation section"""
        section = QFrame()
        section.setObjectName("card")
        
        layout = QVBoxLayout(section)
        
        title = QLabel("🧮 Invoice Calculation :")
        title.setObjectName("sectionLabel")
        layout.addWidget(title)
        
        # Create grid for calculations
        calc_layout = QVBoxLayout()
        calc_layout.setSpacing(4)
        # Ensure there is spacing between rows in the calculation layout
        calc_layout.setSpacing(12)
        calc_layout.setContentsMargins(6, 6, 6, 6)

        # helper to create rows with consistent spacing
        def _row():
            r = QHBoxLayout()
            r.setSpacing(12)
            return r

        # Subtotal row
        subtotal_row = _row()
        subtotal_label = QLabel("Subtotal :")
        subtotal_label.setStyleSheet("font-size: 11pt;")
        self.subtotal_value = QLabel("₹ 0.00")
        self.subtotal_value.setStyleSheet("font-size: 12pt; font-weight: bold;")
        self.subtotal_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        subtotal_row.addWidget(subtotal_label)
        subtotal_row.addStretch()
        subtotal_row.addWidget(self.subtotal_value)
        calc_layout.addLayout(subtotal_row)
        
        # Tax Amount row
        tax_row = QHBoxLayout()
        tax_label = QLabel("Tax Amount :")
        tax_label.setStyleSheet("font-size: 11pt;")
        self.tax_value = QLabel("₹ 0.00")
        self.tax_value.setStyleSheet("font-size: 12pt; font-weight: bold;")
        self.tax_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        tax_row.addWidget(tax_label)
        tax_row.addStretch()
        tax_row.addWidget(self.tax_value)
        calc_layout.addLayout(tax_row)
        
        # Total row
        total_row = QHBoxLayout()
        total_label = QLabel("Invoice Amount* :")
        total_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #0d7377;")
        self.total_value = QLabel("₹ 0.00")
        self.total_value.setStyleSheet("font-size: 13pt; font-weight: bold; color: #0d7377;")
        self.total_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        total_row.addWidget(total_label)
        total_row.addStretch()
        total_row.addWidget(self.total_value)
        calc_layout.addLayout(total_row)
        
        # Received Amount row
        received_row = QHBoxLayout()
        received_label = QLabel("Received :")
        received_label.setStyleSheet("font-size: 11pt;")
        self.received_input = QDoubleSpinBox()
        self.received_input.setMaximum(999999.99)
        self.received_input.setPrefix("₹ ")
        self.received_input.setMinimumHeight(35)
        self.received_input.valueChanged.connect(self.calculate_balance)
        received_row.addWidget(received_label)
        received_row.addStretch()
        received_row.addWidget(self.received_input)
        calc_layout.addLayout(received_row)
        
        # Balance (in colored box)
        balance_frame = QFrame()
        balance_frame.setStyleSheet("""
            # background-color: rgba(0, 122, 204, 0.5);
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 5px;
            padding: 1px;
            margin-top: 10px;
        """)
        balance_layout = QHBoxLayout(balance_frame)
        balance_layout.setContentsMargins(15, 15, 15, 15)
        balance_label = QLabel("Balance :")
        balance_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #1b5e20;")
        self.balance_value = QLabel("₹ 0.00")
        self.balance_value.setStyleSheet("font-size: 16pt; font-weight: bold; color: #2e7d32;")
        self.balance_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        balance_layout.addWidget(balance_label)
        balance_layout.addStretch()
        balance_layout.addWidget(self.balance_value)
        
        layout.addLayout(calc_layout)
        layout.addWidget(balance_frame)
        
        return section
    
    def add_item_row(self):
        """Add a new row to items table"""
        row_position = self.items_table.rowCount()
        self.items_table.insertRow(row_position)
        
        # Item Name
        item_name = QLineEdit()
        item_name.setPlaceholderText("Enter item/visa type")
        self.items_table.setCellWidget(row_position, 0, item_name)
        
        # Ticket Number
        ticket_num = QLineEdit()
        ticket_num.setPlaceholderText("Ticket #")
        self.items_table.setCellWidget(row_position, 1, ticket_num)
        
        # Sector
        sector = QLineEdit()
        sector.setPlaceholderText("Sector")
        self.items_table.setCellWidget(row_position, 2, sector)
        
        # Supplier
        supplier = QLineEdit()
        supplier.setPlaceholderText("Supplier name")
        self.items_table.setCellWidget(row_position, 3, supplier)
        
        # Quantity
        quantity = QDoubleSpinBox()
        quantity.setMinimum(1)
        quantity.setMaximum(999)
        quantity.setValue(1)
        quantity.valueChanged.connect(lambda: self.calculate_row_total(row_position))
        self.items_table.setCellWidget(row_position, 4, quantity)
        
        # Price per unit
        price = QDoubleSpinBox()
        price.setMaximum(999999.99)
        price.setPrefix("₹ ")
        price.valueChanged.connect(lambda: self.calculate_row_total(row_position))
        self.items_table.setCellWidget(row_position, 5, price)
        
        # Tax percentage
        tax_pct = QDoubleSpinBox()
        tax_pct.setMaximum(100)
        tax_pct.setSuffix("%")
        tax_pct.valueChanged.connect(lambda: self.calculate_row_total(row_position))
        self.items_table.setCellWidget(row_position, 6, tax_pct)
        
        # Tax amount (read-only)
        tax_amt = QLineEdit("₹ 0.00")
        tax_amt.setReadOnly(True)
        tax_amt.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.items_table.setCellWidget(row_position, 7, tax_amt)
        
        # Total amount (read-only)
        total_amt = QLineEdit("₹ 0.00")
        total_amt.setReadOnly(True)
        total_amt.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_amt.setStyleSheet("font-weight: bold;")
        self.items_table.setCellWidget(row_position, 8, total_amt)
        
        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setObjectName("dangerBtn")
        delete_btn.setMaximumWidth(60)
        delete_btn.clicked.connect(lambda: self.delete_item_row(row_position))
        self.items_table.setCellWidget(row_position, 9, delete_btn)
        
        # Update table height to fit all rows
        self.update_table_height()
    
    def update_table_height(self):
        """Update table height to show all rows without scrolling"""
        # Calculate height needed for all rows
        row_count = self.items_table.rowCount()
        if row_count == 0:
            row_count = 1  # Minimum height for empty table
        
        header_height = self.items_table.horizontalHeader().height()
        row_height = self.items_table.verticalHeader().defaultSectionSize()
        total_height = header_height + (row_height * row_count) + 2  # +2 for borders
        
        self.items_table.setMinimumHeight(total_height)
        self.items_table.setMaximumHeight(total_height)
    
    def delete_item_row(self, row):
        """Delete a row from items table"""
        self.items_table.removeRow(row)
        self.update_table_height()  # Update height after deleting
        self.calculate_totals()
    
    def calculate_row_total(self, row):
        """Calculate total for a specific row"""
        try:
            quantity_widget = self.items_table.cellWidget(row, 4)
            price_widget = self.items_table.cellWidget(row, 5)
            tax_pct_widget = self.items_table.cellWidget(row, 6)
            tax_amt_widget = self.items_table.cellWidget(row, 7)
            total_widget = self.items_table.cellWidget(row, 8)
            
            if all([quantity_widget, price_widget, tax_pct_widget, tax_amt_widget, total_widget]):
                quantity = quantity_widget.value()
                price = price_widget.value()
                tax_pct = tax_pct_widget.value()
                
                subtotal = quantity * price
                tax_amt = subtotal * (tax_pct / 100)
                total = subtotal + tax_amt
                
                tax_amt_widget.setText(f"₹ {tax_amt:.2f}")
                total_widget.setText(f"₹ {total:.2f}")
                
                self.calculate_totals()
        except Exception as e:
            print(f"Error calculating row total: {e}")
    
    def calculate_totals(self):
        """Calculate invoice totals"""
        subtotal = 0
        tax_total = 0
        
        for row in range(self.items_table.rowCount()):
            try:
                quantity_widget = self.items_table.cellWidget(row, 4)
                price_widget = self.items_table.cellWidget(row, 5)
                tax_pct_widget = self.items_table.cellWidget(row, 6)
                
                if all([quantity_widget, price_widget, tax_pct_widget]):
                    quantity = quantity_widget.value()
                    price = price_widget.value()
                    tax_pct = tax_pct_widget.value()
                    
                    row_subtotal = quantity * price
                    row_tax = row_subtotal * (tax_pct / 100)
                    
                    subtotal += row_subtotal
                    tax_total += row_tax
            except Exception as e:
                print(f"Error calculating totals: {e}")
        
        total = subtotal + tax_total
        
        self.subtotal_value.setText(f"₹ {subtotal:.2f}")
        self.tax_value.setText(f"₹ {tax_total:.2f}")
        self.total_value.setText(f"₹ {total:.2f}")
        
        self.calculate_balance()
    
    def calculate_balance(self):
        """Calculate balance amount"""
        try:
            total_text = self.total_value.text().replace("₹", "").replace(",", "").strip()
            total = float(total_text) if total_text else 0
            received = self.received_input.value()
            balance = total - received
            
            self.balance_value.setText(f"₹ {balance:.2f}")
        except Exception as e:
            print(f"Error calculating balance: {e}")
    
    def save_invoice(self):
        """Save invoice to database"""
        try:
            # Validate
            customer_name = self.customer_name.text().strip()
            if not customer_name:
                QMessageBox.warning(self, "Validation Error", "Please enter customer name!")
                return
            
            if self.items_table.rowCount() == 0:
                QMessageBox.warning(self, "Validation Error", "Please add at least one item!")
                return
            
            # Generate invoice number
            invoice_number = self.invoice_number.text()
            if not invoice_number:
                invoice_number = self.db.get_next_invoice_number()
                self.invoice_number.setText(invoice_number)
            
            # Prepare invoice data
            total_text = self.total_value.text().replace("₹", "").replace(",", "").strip()
            subtotal_text = self.subtotal_value.text().replace("₹", "").replace(",", "").strip()
            tax_text = self.tax_value.text().replace("₹", "").replace(",", "").strip()
            
            invoice_data = {
                'invoice_number': invoice_number,
                'customer_name': customer_name,
                'invoice_date': self.invoice_date.date().toString("yyyy-MM-dd"),
                'subtotal': float(subtotal_text) if subtotal_text else 0,
                'tax_amount': float(tax_text) if tax_text else 0,
                'total_amount': float(total_text) if total_text else 0,
                'received_amount': self.received_input.value(),
                'balance': float(self.balance_value.text().replace("₹", "").replace(",", "").strip())
            }
            
            # Prepare items
            items = []
            for row in range(self.items_table.rowCount()):
                item_name_widget = self.items_table.cellWidget(row, 0)
                ticket_widget = self.items_table.cellWidget(row, 1)
                sector_widget = self.items_table.cellWidget(row, 2)
                supplier_widget = self.items_table.cellWidget(row, 3)
                quantity_widget = self.items_table.cellWidget(row, 4)
                price_widget = self.items_table.cellWidget(row, 5)
                tax_pct_widget = self.items_table.cellWidget(row, 6)
                tax_amt_widget = self.items_table.cellWidget(row, 7)
                total_widget = self.items_table.cellWidget(row, 8)
                
                if item_name_widget and item_name_widget.text().strip():
                    items.append({
                        'item_name': item_name_widget.text(),
                        'ticket_number': ticket_widget.text() if ticket_widget else '',
                        'sector': sector_widget.text() if sector_widget else '',
                        'supplier': supplier_widget.text() if supplier_widget else '',
                        'quantity': quantity_widget.value() if quantity_widget else 1,
                        'price_per_unit': price_widget.value() if price_widget else 0,
                        'tax_percentage': tax_pct_widget.value() if tax_pct_widget else 0,
                        'tax_amount': float(tax_amt_widget.text().replace("₹", "").strip()) if tax_amt_widget else 0,
                        'amount': float(total_widget.text().replace("₹", "").strip()) if total_widget else 0
                    })
            
            # Save to database
            invoice_id = self.db.create_invoice(invoice_data, items)
            self.current_invoice_id = invoice_id
            
            QMessageBox.information(self, "Success", f"Invoice {invoice_number} saved successfully!")
            # Don't reset form after save, so user can export to PDF
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save invoice: {str(e)}")
    
    def save_as_pdf(self):
        """Save invoice as PDF"""
        if not self.current_invoice_id:
            QMessageBox.warning(self, "No Invoice", "Please save the invoice first before exporting to PDF!")
            return
        
        # Get file name from user
        invoice_number = self.invoice_number.text()
        default_filename = f"Invoice_{invoice_number}.pdf"
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Invoice as PDF",
            default_filename,
            "PDF Files (*.pdf)"
        )
        
        if filename:
            try:
                success = self.pdf_generator.generate_invoice_pdf(self.current_invoice_id, filename)
                if success:
                    QMessageBox.information(self, "Success", f"Invoice saved as PDF:\n{filename}")
                else:
                    QMessageBox.warning(self, "Error", "Failed to generate PDF!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save PDF: {str(e)}")
    
    def reset_form(self):
        """Reset the form"""
        self.current_invoice_id = None
        self.invoice_number.clear()
        self.invoice_date.setDate(QDate.currentDate())
        self.customer_name.clear()
        self.customer_contact.clear()
        self.items_table.setRowCount(0)
        self.received_input.setValue(0)
        self.subtotal_value.setText("₹ 0.00")
        self.tax_value.setText("₹ 0.00")
        self.total_value.setText("₹ 0.00")
        self.balance_value.setText("₹ 0.00")
        
        # Add one default row
        self.add_item_row()
    
    def load_initial_data(self):
        """Load initial data"""
        # Load customers for autocomplete
        customers = self.db.get_all_customers()
        customer_names = [c['name'] for c in customers]
        
        # Set up the completer model
        model = QStringListModel(customer_names)
        self.customer_completer.setModel(model)
        
        # Add one default row
        self.add_item_row()
