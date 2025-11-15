from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QGridLayout, QDoubleSpinBox
)
import sys


class DashboardFull(QMainWindow):
    """Minimal, stable DashboardFull implementation used by main.py.

    Provides a table with Add Item, per-row amount calculation, and totals.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency - Billing Software")
        self.resize(1100, 700)

        # Main layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet("background-color: #111; color: #ddd;")
        main_layout.addWidget(sidebar)

        # Content area
        content = QWidget()
        content_layout = QVBoxLayout(content)
        main_layout.addWidget(content, 1)

        heading = QLabel("<h2>Welcome to Travel Agency Billing</h2>")
        content_layout.addWidget(heading)

        # Invoice header fields
        form = QHBoxLayout()
        self.invoice_number = QLineEdit()
        self.invoice_number.setPlaceholderText("Invoice #")
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("Customer name")
        form.addWidget(QLabel("Invoice #:"))
        form.addWidget(self.invoice_number)
        form.addWidget(QLabel("Customer:"))
        form.addWidget(self.customer_name)
        content_layout.addLayout(form)

        # Table
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Item Name", "Ticket #", "Sector", "Supplier", "Price", "Qty", "Tax (%)", "Amount (₹)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        content_layout.addWidget(self.table)

        # Add item button and totals
        top_buttons = QHBoxLayout()
        self.btn_add_item = QPushButton("+ Add Item")
        self.btn_add_item.clicked.connect(self.add_item_row)
        top_buttons.addWidget(self.btn_add_item)
        top_buttons.addStretch()

        # Totals
        self.lbl_subtotal = QLabel("Subtotal: ₹0.00")
        self.lbl_tax = QLabel("Tax: ₹0.00")
        self.lbl_total = QLabel("Total: ₹0.00")
        self.lbl_total.setStyleSheet("font-weight:bold; color:#9b9bff;")
        top_buttons.addWidget(self.lbl_subtotal)
        top_buttons.addWidget(self.lbl_tax)
        top_buttons.addWidget(self.lbl_total)

        content_layout.addLayout(top_buttons)

        # keep compatibility alias
        self.items_table = self.table

    def add_item_row(self):
        """Insert a new editable row with widgets for price/qty/tax and a read-only amount."""
        table = self.items_table
        row = table.rowCount()
        table.insertRow(row)

        # Item name
        item_name = QLineEdit()
        item_name.setPlaceholderText("Item name")
        table.setCellWidget(row, 0, item_name)

        # Ticket
        ticket = QLineEdit()
        ticket.setPlaceholderText("Ticket #")
        table.setCellWidget(row, 1, ticket)

        # Sector
        sector = QLineEdit()
        table.setCellWidget(row, 2, sector)

        # Supplier
        supplier = QLineEdit()
        table.setCellWidget(row, 3, supplier)

        # Price
        price = QDoubleSpinBox()
        price.setMaximum(1_000_000)
        price.setPrefix("₹ ")
        price.valueChanged.connect(lambda _: self.calculate_row_total(row))
        table.setCellWidget(row, 4, price)

        # Qty
        qty = QDoubleSpinBox()
        qty.setMinimum(1)
        qty.setMaximum(9999)
        qty.setValue(1)
        qty.valueChanged.connect(lambda _: self.calculate_row_total(row))
        table.setCellWidget(row, 5, qty)

        # Tax %
        tax = QDoubleSpinBox()
        tax.setSuffix('%')
        tax.setMaximum(100)
        tax.valueChanged.connect(lambda _: self.calculate_row_total(row))
        table.setCellWidget(row, 6, tax)

        # Amount (read-only)
        amount = QLineEdit("₹ 0.00")
        amount.setReadOnly(True)
        table.setCellWidget(row, 7, amount)

        table.scrollToBottom()

    def calculate_row_total(self, row: int):
        """Compute amount for a row and update totals."""
        table = self.items_table
        try:
            price_w = table.cellWidget(row, 4)
            qty_w = table.cellWidget(row, 5)
            tax_w = table.cellWidget(row, 6)
            amount_w = table.cellWidget(row, 7)
            price = float(price_w.value() if price_w else 0)
            qty = float(qty_w.value() if qty_w else 0)
            tax_pct = float(tax_w.value() if tax_w else 0)
            total = price * qty * (1 + tax_pct / 100)
            if amount_w:
                amount_w.setText(f"₹ {total:.2f}")
        except Exception:
            pass
        finally:
            self.update_invoice_totals()

    def update_invoice_totals(self):
        subtotal = 0.0
        table = self.items_table
        for r in range(table.rowCount()):
            amt_w = table.cellWidget(r, 7)
            if amt_w:
                txt = amt_w.text().replace('₹', '').replace(',', '').strip()
                try:
                    subtotal += float(txt or 0)
                except Exception:
                    pass
        tax = subtotal * 0.05
        total = subtotal + tax
        self.lbl_subtotal.setText(f"Subtotal: ₹{subtotal:.2f}")
        self.lbl_tax.setText(f"Tax: ₹{tax:.2f}")
        self.lbl_total.setText(f"Total: ₹{total:.2f}")

    def load_invoice_page(self):
        try:
            from travel_billing.main_manual import InvoicePage
        except Exception as e:
            print("Could not import InvoicePage:", e)
            return
        win = InvoicePage()
        win.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DashboardFull()
    w.show()
    sys.exit(app.exec_())
 ----------
        # save_btn.clicked.connect(self.save_invoice)
        # self.btn_add_item.clicked.connect(self.add_item_row)
       # ---------- Buttons ----------
        top_buttons = QHBoxLayout()
        top_buttons.addStretch()

        self.btn_add_item = QPushButton("+ Add Item")
        self.btn_add_item.clicked.connect(self.add_item_row)
        top_buttons.addWidget(self.btn_add_item)

        content_layout.addLayout(top_buttons)
                # self.btn_add_item = QPushButton("+ Add Item")
        # self.btn_add_item.clicked.connect(self.add_item_row)
        # table_layout.addWidget(self.btn_add_item)
        content_layout.addLayout(table_layout)

        self.btn_add_item.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #63B3FF;
            }
        """)

        top_buttons.addWidget(self.btn_add_item)
        content_layout.addLayout(top_buttons)

        # ---------- Table ----------
        content_layout.addWidget(self.table)
        # ---------------- Invoice Calculation Section ----------------
        calc_layout = QGridLayout()
        title = QLabel("🧮 Invoice Calculation :")
        title.setObjectName("sectionLabel")
        content_layout.addWidget(title)
        

        lbl_subtotal = QLabel("Subtotal:")
        lbl_tax = QLabel("Tax Amount:")
        lbl_total = QLabel("Invoice Amount ₹:")
        lbl_received = QLabel("Received:")
        lbl_balance = QLabel("Balance:")

        self.txt_subtotal = QLabel("₹ 0.00")
        self.txt_tax = QLabel("₹ 0.00")
        self.txt_total = QLabel("₹ 0.00")
        self.txt_received = QLineEdit()
        self.txt_balance = QLabel("₹ 0.00")

        # Styling
        for label in [lbl_subtotal, lbl_tax, lbl_total, lbl_received, lbl_balance]:
            label.setStyleSheet("font-weight: 600; color: white;")
        self.txt_total.setStyleSheet("color: #00FF00; font-weight: bold;")

        calc_layout.addWidget(lbl_subtotal, 0, 0)
        calc_layout.addWidget(self.txt_subtotal, 0, 1)
        calc_layout.addWidget(lbl_tax, 1, 0)
        calc_layout.addWidget(self.txt_tax, 1, 1)
        calc_layout.addWidget(lbl_total, 2, 0)
        calc_layout.addWidget(self.txt_total, 2, 1)
        calc_layout.addWidget(lbl_received, 3, 0)
        calc_layout.addWidget(self.txt_received, 3, 1)
        calc_layout.addWidget(lbl_balance, 4, 0)
        calc_layout.addWidget(self.txt_balance, 4, 1)

        content_layout.addLayout(calc_layout)


        # ---------- Bottom Buttons (Save & PDF) ----------
        bottom_buttons = QHBoxLayout()
        bottom_buttons.addStretch()
        # title = QLabel("🧮 Invoice Calculation :")
        # title.setObjectName("sectionLabel")
        # content_layout.addWidget(title)
        
        self.save_btn = QPushButton("💾 Save Invoice")
        self.pdf_btn = QPushButton("🧾 Save as PDF")

        for btn in [self.save_btn, self.pdf_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #5C5CFF;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #7A7AFF;
                }
            """)

        bottom_buttons.addWidget(self.save_btn)
        bottom_buttons.addWidget(self.pdf_btn)
        content_layout.addLayout(bottom_buttons)

        # ---------- Connect signals ----------
        # self.btn_add_item.clicked.connect(lambda: self.add_item_row())
        # self.btn_add_item.clicked.connect(self.add_item_row)
        self.save_btn.clicked.connect(self.save_invoice)
        self.pdf_btn.clicked.connect(self.save_pdf)

        # Add this before adding content to main layout
        main_layout.addWidget(content)
        

        # def add_item_row(self):
        #     row_position = self.table.rowCount()
        #     self.table.insertRow(row_position)
        #     row = self.items_table.rowCount()
        #     self.items_table.insertRow(row)
        #     self.items_table.setVerticalHeaderItem(row, QTableWidgetItem(str(row + 1)))

            # row = self.table.rowCount()
            # self.table.insertRow(row)
            # self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))


#    --- Billed Items Label ---
    #     table_label = QLabel("<b>Billed Items:</b>")
    #     content_layout.addWidget(table_label)

    # # --- Table ---
    #     self.table = QTableWidget(3, 6)
    #     self.table.setHorizontalHeaderLabels([
    #         "Item Name", "Ticket #", "Sector", "Supplier", "Price", "Qty"
    #     ])
    #     self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # # Wrap table and Add Item button together
    #     table_section = QVBoxLayout()
    #     table_section.addWidget(self.table)

    #     # --- Add Item button (right side, blue) ---
    #     add_item_layout = QHBoxLayout()
    #     add_item_layout.addStretch()
    #     self.btn_add_item = QPushButton("+ Add Item")
    #     self.btn_add_item.setStyleSheet("""
    #             QPushButton {
    #                 background-color: #3B82F6;
    #                 color: white;
    #                 border: none;
    #                 border-radius: 6px;
    #                 padding: 6px 12px;
    #                 font-weight: bold;
    #         }
    #         QPushButton:hover {
    #             background-color: #2563EB;
    #             }
    #         """)
    #     add_item_layout.addWidget(self.btn_add_item)
    #     table_section.addLayout(add_item_layout)

    #     # --- Save Buttons (below Add Item) ---
    #     btn_layout = QHBoxLayout()
    #     btn_layout.addStretch()
    #     save_btn = QPushButton("💾 Save Invoice")
    #     pdf_btn = QPushButton("🧾 Save as PDF")
    #     btn_layout.addWidget(save_btn)
    #     btn_layout.addWidget(pdf_btn)
    #     table_section.addLayout(btn_layout)

    # # --- Add everything to content layout ---
    #     content_layout.addLayout(table_section)
    #     self.load_invoice_page()
        self.table.itemChanged.connect(self.update_invoice_totals)
    # def add_item_row(self):
    #         row_count = self.table.rowCount()
    #         self.table.insertRow(row_count)

    #         number_item = QTableWidgetItem(str(row_count + 1))
    #         self.table.setItem(row_count, 0, number_item)
    # def add_item_row(self):
    #         # Determine which table is being used
    #         table = None
    #         if hasattr(self, "items_table"):
    #             table = self.items_table
    #         elif hasattr(self, "table"):
    #             table = self.table
    #         else:
    #             return   # No table found

    #         row_count = table.rowCount()
    #         table.insertRow(row_count)

    #         number_item = QTableWidgetItem(str(row_count + 1))
    #         number_item.setFlags(Qt.ItemIsEnabled)
    #         table.setItem(row_count, 0, number_item)
    def add_item_row(self):
        """Add a new row to the invoice table (supports either `self.table` or legacy `self.items_table`)."""
        table = getattr(self, 'items_table', None) or getattr(self, 'table', None)
        if table is None:
            return

        row_position = table.rowCount()
        table.insertRow(row_position)

        # Item Name
        item_name = QLineEdit()
        item_name.setPlaceholderText("Enter item/visa type")
        table.setCellWidget(row_position, 0, item_name)

        # Ticket Number
        ticket_num = QLineEdit()
        ticket_num.setPlaceholderText("Ticket #")
        table.setCellWidget(row_position, 1, ticket_num)

        # Sector
        sector = QLineEdit()
        sector.setPlaceholderText("Sector")
        table.setCellWidget(row_position, 2, sector)

        # Supplier
        supplier = QLineEdit()
        supplier.setPlaceholderText("Supplier name")
        table.setCellWidget(row_position, 3, supplier)

        # Quantity
        quantity = QDoubleSpinBox()
        quantity.setMinimum(1)
        quantity.setMaximum(999)
        quantity.setValue(1)
        quantity.valueChanged.connect(lambda _: self.calculate_row_total(row_position))
        table.setCellWidget(row_position, 4, quantity)

        # Price per unit
        price = QDoubleSpinBox()
        price.setMaximum(999999.99)
        price.setPrefix("₹ ")
        price.valueChanged.connect(lambda _: self.calculate_row_total(row_position))
        table.setCellWidget(row_position, 5, price)

        # Tax percentage
        tax_pct = QDoubleSpinBox()
        tax_pct.setMaximum(100)
        tax_pct.setSuffix("%")
        tax_pct.valueChanged.connect(lambda _: self.calculate_row_total(row_position))
        table.setCellWidget(row_position, 6, tax_pct)

        # Total amount (read-only)
        total_amt = QLineEdit("₹ 0.00")
        total_amt.setReadOnly(True)
        total_amt.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_amt.setStyleSheet("font-weight: bold;")
        table.setCellWidget(row_position, 7, total_amt)

        # Ensure new row is visible
        table.scrollToBottom()

    # def load_invoice_page(self):
    #         from travel_billing.main_manual import InvoicePage
    #         self.invoice_page = InvoicePage()
    #         self.invoice_page.show()
    #         self.load_invoice_page()
    def load_invoice_page(self):
        """Load invoice page (do not recurse)."""
        try:
            from travel_billing.main_manual import InvoicePage
        except Exception as e:
            # safe fallback: print error but don't crash UI
            print("Could not import InvoicePage:", e)
            return

        self.invoice_page = InvoicePage()
        self.invoice_page.show()
    def update_invoice_totals(self):
        subtotal = 0.0
        for row in range(self.table.rowCount()):
            try:
                price_item = self.table.item(row, 4)  # price column
                qty_item = self.table.item(row, 5)    # qty column
                if price_item and qty_item:
                    price = float(price_item.text() or 0)
                    qty = float(qty_item.text() or 0)
                    subtotal += price * qty
            except:
                pass

            tax = subtotal * 0.05  # 5% tax
            total = subtotal + tax

            self.lbl_subtotal.setText(f"Subtotal: ₹{subtotal:.2f}")
            self.lbl_tax.setText(f"Tax: ₹{tax:.2f}")
            self.lbl_total.setText(f"Total: ₹{total:.2f}")


    def create_sidebar_button(self, text, page_id):
            """Create a styled sidebar button"""
            btn = QPushButton(text)
            btn.setObjectName("sidebarBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setProperty("active", "false")
            btn.setMinimumHeight(45)
            
            # Set font
            font = btn.font()
            font.setPointSize(11)
            btn.setFont(font)
            
            return btn
    def add_page(self, page_id, page_widget):
        """Add a page to the stack"""
        self.pages[page_id] = page_widget
        self.content_stack.addWidget(page_widget)
    def switch_page(self, page_id):
        """Switch to a different page"""
        if page_id in self.pages:
            # Update active button styling
            for btn_id, btn in self.sidebar_buttons.items():
                if btn_id == page_id:
                    btn.setProperty("active", "true")
                else:
                    btn.setProperty("active", "false")
                btn.style().unpolish(btn)
                btn.style().polish(btn)
            
            # Switch to the page
            self.content_stack.setCurrentWidget(self.pages[page_id])
    def save_invoice(self):
            customer = self.customer_name.text().strip()
            if customer:
                print(f"Invoice saved for {customer}")
            else:
                print("Please enter customer name")
    # def add_item_row(self):
    #             # row_position = self.table.rowCount()
    #             # self.table.insertRow(row_position)
    #             row_count = self.table.rowCount()
    #             self.table.insertRow(row_count)
    #             row = self.table.rowCount()
    #             self.table.insertRow(row)
    #             self.table.setVerticalHeaderItem(row, QTableWidgetItem(str(row + 1)))


    #             # Add row number automatically
    #             number_item = QTableWidgetItem(str(row_count + 1))
    #             self.table.setItem(row_count, 0, number_item)
    #             top_buttons = QHBoxLayout()
    #             top_buttons.addStretch()

    #             self.btn_add_item = QPushButton("+ Add Item")
    #             self.btn_add_item.clicked.connect(self.add_item_row)

                # top_buttons.addWidget(self.btn_add_item)
                # content_layout.addLayout(top_buttons)

                # self.btn_add_item.setStyleSheet("""
                #     QPushButton {
                #         background-color: #1E90FF;
                #         color: white;
                #         font-weight: bold;
                #         border-radius: 5px;
                #         padding: 5px 10px;
                #     }
                #     QPushButton:hover {
                #         background-color: #63B3FF;
                #     }
                # """)
  # assuming first column is for serial no.
    # def add_item_row(self):
    #     """Add a new row to items table"""
    #     row_position = self.items_table.rowCount()
    #     self.items_table.insertRow(row_position)
                
    #     # Item Name
    #     item_name = QLineEdit()
    #     item_name.setPlaceholderText("Enter item/visa type")
    #     self.items_table.setCellWidget(row_position, 0, item_name)
        
    #     # Ticket Number
    #     ticket_num = QLineEdit()         
    #         # Sector
    #     sector = QLineEdit()
    #     sector.setPlaceholderText("Sector")
    #     self.items_table.setCellWidget(row_position, 2, sector)
                
    #         # Supplier
    #     supplier = QLineEdit()
    #     supplier.setPlaceholderText("Supplier name")
    #     self.items_table.setCellWidget(row_position, 3, supplier)
                
    #             # Quantity
    #     quantity = QDoubleSpinBox()
    #     quantity.setMinimum(1)
    #     quantity.setMaximum(999)
    #     quantity.setValue(1)
    #     quantity.valueChanged.connect(lambda: self.calculate_row_total(row_position))
    #     self.items_table.setCellWidget(row_position, 4, quantity)
            
    #         # Price per unit
    #     price = QDoubleSpinBox()
    #     price.setMaximum(999999.99)
    #     price.setPrefix("₹ ")
    #     price.valueChanged.connect(lambda: self.calculate_row_total(row_position))
    #     self.items_table.setCellWidget(row_position, 5, price)
            
    #         # Tax percentage
    #     tax_pct = QDoubleSpinBox()
    #     tax_pct.setMaximum(100)
    #     tax_pct.setSuffix("%")
    #             tax_pct.valueChanged.connect(lambda: self.calculate_row_total(row_position))
    #             self.items_table.setCellWidget(row_position, 6, tax_pct)
            
    #         # Tax amount (read-only)
    #             tax_amt = QLineEdit("₹ 0.00")
    #             tax_amt.setReadOnly(True)
    #             tax_amt.setAlignment(Qt.AlignmentFlag.AlignRight)
    #             self.items_table.setCellWidget(row_position, 7, tax_amt)
            
    #         # Total amount (read-only)
    #     total_amt = QLineEdit("₹ 0.00")
    #     total_amt.setReadOnly(True)
    #     total_amt.setAlignment(Qt.AlignmentFlag.AlignRight)
    #     total_amt.setStyleSheet("font-weight: bold;")
    #     self.items_table.setCellWidget(row_position, 8, total_amt)
            
    #         # Delete button
    #     delete_btn = QPushButton("🗑️")
    #     delete_btn.setObjectName("dangerBtn")
    #     delete_btn.setMaximumWidth(60)
    #     delete_btn.clicked.connect(lambda: self.delete_item_row(row_position))
    #     self.items_table.setCellWidget(row_position, 9, delete_btn)
            
    #         # Update table height to fit all rows
    #     self.update_table_height()
    
    # def update_table_height(self):
    #     """Update table height to show all rows without scrolling"""
    #     # Calculate height needed for all rows
    #     row_count = self.items_table.rowCount()
    #     if row_count == 0:
    #         row_count = 1  # Minimum height for empty table
        
    #     header_height = self.items_table.horizontalHeader().height()
    #     row_height = self.items_table.verticalHeader().defaultSectionSize()
    #     total_height = header_height + (row_height * row_count) + 2  # +2 for borders
        
    #     self.items_table.setMinimumHeight(total_height)
    #     self.items_table.setMaximumHeight(total_height)
    
    # def delete_item_row(self, row):
    #     """Delete a row from items table"""
    #     self.items_table.removeRow(row)
    #     self.update_table_height()  # Update height after deleting
    #     self.calculate_totals()
    
    # def calculate_row_total(self, row):
    #     """Calculate total for a specific row"""
    #     try:
    #         quantity_widget = self.items_table.cellWidget(row, 4)
    #         price_widget = self.items_table.cellWidget(row, 5)
    #         tax_pct_widget = self.items_table.cellWidget(row, 6)
    #         tax_amt_widget = self.items_table.cellWidget(row, 7)
    #         total_widget = self.items_table.cellWidget(row, 8)
            
    #         if all([quantity_widget, price_widget, tax_pct_widget, tax_amt_widget, total_widget]):
    #             quantity = quantity_widget.value()
    #             price = price_widget.value()
    #             tax_pct = tax_pct_widget.value()
                
    #             subtotal = quantity * price
    #             tax_amt = subtotal * (tax_pct / 100)
    #             total = subtotal + tax_amt
                
    #             tax_amt_widget.setText(f"₹ {tax_amt:.2f}")
    #             total_widget.setText(f"₹ {total:.2f}")
                
    #             self.calculate_totals()
    #     except Exception as e:
    #         print(f"Error calculating row total: {e}")
    # def get_current_page(self):
    #     """Get the current page widget"""
    #     return self.content_stack.currentWidget()

    # def create_invoice_details_card(self):
    #     """Create invoice details card"""
    #     card = QFrame()
    #     card.setObjectName("card")
        
    #     layout = QVBoxLayout(card)
        
    #     # Title
    #     title = QLabel("📝 Invoice Details :")
    #     title.setObjectName("sectionLabel")
    #     layout.addWidget(title)
        
    #     # Invoice Number
    #     inv_layout = QHBoxLayout()
    #     inv_label = QLabel("Invoice Number :")
    #     inv_label.setMinimumWidth(120)
    #     self.invoice_number = QLineEdit()
    #     self.invoice_number.setReadOnly(True)
    #     self.invoice_number.setPlaceholderText("Auto-generated")
    #     self.invoice_number.setMinimumHeight(30)
    #     inv_layout.addWidget(inv_label)
    #     inv_layout.addWidget(self.invoice_number)
    #     layout.addLayout(inv_layout)
        
    #     # Invoice Date
    #     date_layout = QHBoxLayout()
    #     date_label = QLabel("Invoice Date :")
    #     date_label.setMinimumWidth(120)
    #     self.invoice_date = QDateEdit()
    #     self.invoice_date.setCalendarPopup(True)
    #     self.invoice_date.setDate(QDate.currentDate())
    #     self.invoice_date.setDisplayFormat("dd-MM-yyyy")
    #     self.invoice_date.setMinimumHeight(30)
    #     date_layout.addWidget(date_label)
    #     date_layout.addWidget(self.invoice_date)
    #     layout.addLayout(date_layout)
        
    #     layout.addStretch()
        
    #     return card            
    
    def save_pdf(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Save as PDF", "PDF export feature coming soon!")

    # def export_excel(self):
    #     from PyQt5.QtWidgets import QMessageBox
    #     QMessageBox.information(self, "Export Excel", "Excel export feature coming soon!")

    # def load_invoice_page(self):
    # def update_invoice_totals(self):
    #     subtotal = 0.0
    #     for row in range(self.table.rowCount()):
    #         try:
    #             price_item = self.table.item(row, 4)  # price column
    #             qty_item = self.table.item(row, 5)    # qty column
    #             if price_item and qty_item:
    #                 price = float(price_item.text() or 0)
    #                 qty = float(qty_item.text() or 0)
    #                 subtotal += price * qty
    #         except:
    #             pass

    #         tax = subtotal * 0.05  # 5% tax
    #         total = subtotal + tax

    #         self.lbl_subtotal.setText(f"Subtotal: ₹{subtotal:.2f}")
    #         self.lbl_tax.setText(f"Tax: ₹{tax:.2f}")
    #         self.lbl_total.setText(f"Total: ₹{total:.2f}")
# from PyQt5.QtWidgets import QWidget
# from travel_billing.main_manual import InvoicePage

# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
#     QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
# )
# # from PyQt5.QtCore import Qt
# import sys
# from ui.dashboard import Ui_MainWindow

# class DashboardFull(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.ui.btn_newBill.clicked.connect(self.load_invoice_page)
#         self.setWindowTitle("Travel Agency - Billing Software")

# from PyQt5 import QtWidgets
# from PyQt5 import uic
# from travel_billing.main_manual import InvoicePage
# import sys

# class DashboardFull(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Travel Agency - Billing Software")
#         self.resize(1200, 700)

#         # Create invoice page
#         self.invoice_page = InvoicePage()

#         # Central layout
#         central_widget = QtWidgets.QWidget()
#         layout = QtWidgets.QHBoxLayout(central_widget)

#         # Sidebar (optional)
#         sidebar = QtWidgets.QFrame()
#         sidebar.setFixedWidth(180)
#         sidebar.setStyleSheet("background-color: #111;")

#         # Add sidebar and content
#         layout.addWidget(sidebar)
#         layout.addWidget(self.invoice_page)

#         # Set as central widget
#         self.setCentralWidget(central_widget)

# # class DashboardFull(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #         from ui.dashboard import Ui_MainWindow


# #         self.ui = Ui_MainWindow()

# #         self.ui.setupUi(self)
# #         self.ui.btn_newBill.clicked.connect(self.load_invoice_page)

# #         self.setWindowTitle("Travel Agency - Billing Software")
#         self.setGeometry(100, 100, 1200, 700)
#         self.setStyleSheet("""
#             QMainWindow { background-color: #121212; color: #ffffff; }
#             QLabel { color: #dddddd; font-size: 14px; }
#             QLineEdit {
#                 background-color: #1e1e1e;
#                 color: #ffffff;
#                 border: 1px solid #555;
#                 border-radius: 5px;
#                 padding: 4px;
#             }
#             QPushButton {
#                 background-color: #5b5bff;
#                 color: white;
#                 border-radius: 6px;
#                 padding: 6px 12px;
#             }
#             QPushButton:hover {
#                 background-color: #7777ff;
#             }
#             QFrame#sidebar {
#                 background-color: #1b1b1b;
#             }
#             QPushButton#sidebtn {
#                 background-color: #1b1b1b;
#                 color: #bbbbbb;
#                 border: none;
#                 text-align: left;
#                 padding: 10px;
#             }
#             QPushButton#sidebtn:hover {
#                 background-color: #333333;
#                 color: white;
#             }
#         """)

#         # ---------- Main Layout ----------
#         main_widget = QWidget()
#         main_layout = QHBoxLayout(main_widget)
#         self.setCentralWidget(main_widget)

#         # ---------- Sidebar ----------
#         sidebar = QFrame()
#         sidebar.setObjectName("sidebar")
#         sidebar.setFixedWidth(200)
#         sidebar_layout = QVBoxLayout(sidebar)

#         title = QLabel("<b style='font-size:16px;'>🏢 Travel Agency</b>")
#         title.setAlignment(Qt.AlignCenter)
#         sidebar_layout.addWidget(title)

#         for text in ["🏠 Home", "📊 Reports", "⚙ Settings", "ℹ About"]:
#             btn = QPushButton(text)
#             btn.setObjectName("sidebtn")
#             sidebar_layout.addWidget(btn)
#         sidebar_layout.addStretch()

#         main_layout.addWidget(sidebar)

#         # ---------- Main content area ----------
#         content = QFrame()
#         content_layout = QVBoxLayout(content)

#         heading = QLabel("<h2>Welcome to Travel Agency Billing</h2>")
#         content_layout.addWidget(heading)

#         # --- Invoice Info Section ---
            
#         info_layout = QHBoxLayout()

#         # ===== Left: Invoice Details =====
#         invoice_group = QFrame()
#         invoice_group.setStyleSheet("""
#             QFrame {
#                 background-color: #3a3a3a;
#             border-radius: 8px;
#                 padding: 10px;
#             }
#         """)
#         invoice_layout = QVBoxLayout(invoice_group)

#         invoice_title = QLabel("📄 <b>Invoice Details :</b>")
#         invoice_title.setStyleSheet("color: #9b9bff; font-size: 14px;")
#         invoice_layout.addWidget(invoice_title)

#         invoice_no_label = QLabel("Invoice Number :")
#         self.invoice_number = QLineEdit()
#         self.invoice_number.setPlaceholderText("Auto-generated")

#         invoice_date_label = QLabel("Invoice Date :")
#         self.invoice_date = QLineEdit("12-11-2025")

#         invoice_layout.addWidget(invoice_no_label)
#         invoice_layout.addWidget(self.invoice_number)
#         invoice_layout.addWidget(invoice_date_label)
#         invoice_layout.addWidget(self.invoice_date)

#         # ===== Right: Bill To =====
#         billto_group = QFrame()
#         billto_group.setStyleSheet("""
#             QFrame {
#                 background-color: #3a3a3a;
#                 border-radius: 8px;
#                 padding: 10px;
#             }
#         """)
#         billto_layout = QVBoxLayout(billto_group)

#         billto_title = QLabel("👤 <b>Bill To :</b>")
#         billto_title.setStyleSheet("color: #9b9bff; font-size: 14px;")
#         billto_layout.addWidget(billto_title)

#         customer_name_label = QLabel("Customer Name* :")
#         self.customer_name = QLineEdit()
#         self.customer_name.setPlaceholderText("Enter customer name")

#         contact_label = QLabel("Contact Number :")
#         self.customer_contact = QLineEdit()
#         self.customer_contact.setPlaceholderText("Enter contact number")

#         billto_layout.addWidget(customer_name_label)
#         billto_layout.addWidget(self.customer_name)
#         billto_layout.addWidget(contact_label)
#         billto_layout.addWidget(self.customer_contact)

#         # Add both group sections to main info layout
#         # info_layout.addWidget(invoice_group)
#         # info_layout.addWidget(billto_group)
#         info_layout = QHBoxLayout()

#         info_layout.addWidget(invoice_group)
#         info_layout.addWidget(billto_group)
#         info_layout.setSpacing(40)  # space between them
#         info_layout.setContentsMargins(10, 10, 10, 10)
#         content_layout.addLayout(info_layout)
#         # form_layout = QHBoxLayout()
#         save_btn = QPushButton("Save Invoice")
#         form_layout = QHBoxLayout()
#         save_btn.clicked.connect(self.save_invoice)

#         # save_btn.clicked.connect(self.save_invoice)

#         # invoice_number_label = QLabel("Invoice Number:")
#         # self.invoice_number = QLineEdit()
#         # self.invoice_number.setPlaceholderText("Auto-generated")

#         # customer_name_label = QLabel("Customer Name:")
#         # self.customer_name = QLineEdit()
#         # self.customer_name.setPlaceholderText("Enter customer name")

#         # contact_label = QLabel("Contact:")
#         # self.customer_contact = QLineEdit()
#         # self.customer_contact.setPlaceholderText("Enter contact number")

#         # form_layout.addWidget(invoice_number_label)
#         # form_layout.addWidget(self.invoice_number)
#         # form_layout.addWidget(customer_name_label)
#         # form_layout.addWidget(self.customer_name)
#         # form_layout.addWidget(contact_label)
#         # form_layout.addWidget(self.customer_contact)
#         # content_layout.addLayout(form_layout)

        # # --- Table for Billed Items ---
        # table_label = QLabel("<b>Billed Items:</b>")
        # content_layout.addWidget(table_label)

        # self.table = QTableWidget(5, 6)
        # self.table.setHorizontalHeaderLabels([
        #     "Item Name", "Ticket #", "Sector", "Supplier", "Price", "Qty"
        # ])
        # # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # content_layout.addWidget(self.table)
        # # --- Invoice Calculation Section ---
        # calc_layout = QGridLayout()

        # # Labels
        # lbl_subtotal = QLabel("Subtotal:")
        # lbl_tax = QLabel("Tax Amount:")
        # lbl_total = QLabel("Invoice Amount ₹:")
        # lbl_received = QLabel("Received:")
        # lbl_balance = QLabel("Balance:")

        # # Value fields
        # self.txt_subtotal = QLabel("₹ 0.00")
        # self.txt_tax = QLabel("₹ 0.00")
        # self.txt_total = QLabel("₹ 0.00")
        # self.txt_received = QLineEdit()
        # self.txt_balance = QLabel("₹ 0.00")

        # # Styling (optional)
        # for label in [lbl_subtotal, lbl_tax, lbl_total, lbl_received, lbl_balance]:
        #     label.setStyleSheet("font-weight: bold; color: white;")

        # self.txt_total.setStyleSheet("color: #00FF00; font-weight: bold;")

        # # Add to layout
        # calc_layout.addWidget(lbl_subtotal, 0, 0)
        # calc_layout.addWidget(self.txt_subtotal, 0, 1)

        # calc_layout.addWidget(lbl_tax, 1, 0)
        # calc_layout.addWidget(self.txt_tax, 1, 1)

        # calc_layout.addWidget(lbl_total, 2, 0)
        # calc_layout.addWidget(self.txt_total, 2, 1)

        # calc_layout.addWidget(lbl_received, 3, 0)
        # calc_layout.addWidget(self.txt_received, 3, 1)

        # calc_layout.addWidget(lbl_balance, 4, 0)
        # calc_layout.addWidget(self.txt_balance, 4, 1)

        # content_layout.addLayout(calc_layout)


        # # # Connect cell changes to calculation
        # # self.table.cellChanged.connect(self.calculate_totals)

        # # --- Total Calculation ---
        
        # # --- Buttons ---
        # btn_layout = QHBoxLayout()
        # save_btn = QPushButton("💾 Save Invoice")
        # pdf_btn = QPushButton("🧾 Save as PDF")
        # btn_layout.addStretch()
        # btn_layout.addWidget(save_btn)
        # btn_layout.addWidget(pdf_btn)
        # content_layout.addLayout(btn_layout)

        # main_layout.addWidget(content)

        # ---------- Connections ----------
#         save_btn.clicked.connect(self.save_invoice)
#         # Load the .ui file (this will create widgets as attributes on `self`, e.g. `add_bill_button`)
#         uic.loadUi('ui/dashboard.ui', self)

#         # Connect the UI button to load the invoice page. Support multiple possible names
#         if hasattr(self, 'btn_newBill'):
#             self.btn_newBill.clicked.connect(self.load_invoice_page)
#         elif hasattr(self, 'add_bill_button'):
#             # UI generated from ui/dashboard.ui uses `add_bill_button`
#             self.add_bill_button.clicked.connect(self.load_invoice_page)
#             # keep a legacy alias for other code paths
#             self.btn_newBill = self.add_bill_button
#         else:
#             # try other common fallbacks
#             for name in ('addBill', 'newBill'):
#                 if hasattr(self, name):
#                     btn = getattr(self, name)
#                     try:
#                         btn.clicked.connect(self.load_invoice_page)
#                         self.btn_newBill = btn
#                         break
#                     except Exception:
#                         pass

#             # save_btn.clicked.connect(self.save_invoice)

#     # === Paste here ===
#     def load_invoice_page(self):
#         # -------- Find a container to host the invoice page --------
#         from PyQt5.QtWidgets import QVBoxLayout

#         container = None
#         # If code used a generated `ui` object with `mainContent`, prefer that
#         if hasattr(self, 'ui') and hasattr(self.ui, 'mainContent'):
#             container = self.ui.mainContent
#         # direct attribute created by uic.loadUi
#         if container is None and hasattr(self, 'mainContent'):
#             container = getattr(self, 'mainContent')
#         # fallback to the QMainWindow central widget
#         if container is None:
#             container = self.centralWidget() or getattr(self, 'centralwidget', None) or self

#         layout = container.layout()
#         if layout is None:
#             layout = QVBoxLayout(container)
#             try:
#                 container.setLayout(layout)
#             except Exception:
#                 # some widgets (like QMainWindow) don't accept setLayout; ignore
#                 pass

#         # Clear existing widgets
#         for i in reversed(range(layout.count())):
#             item = layout.itemAt(i)
#             if item is None:
#                 continue
#             widget = item.widget()
#             if widget:
#                 widget.setParent(None)

#         # -------- Create and add the InvoicePage --------
#         invoice_widget = InvoicePage()

#         # If InvoicePage is a QMainWindow with a central widget, embed that central widget
#         central = None
#         try:
#             central = invoice_widget.centralWidget()
#         except Exception:
#             central = None

#         if central:
#             # reparent central widget into our layout
#             layout.addWidget(central)
#         else:
#             layout.addWidget(invoice_widget)

#     # def calculate_totals(self):
#     #     subtotal = 0.0
#     #     for row in range(self.table.rowCount()):
#     #         ...

    
#         # self.invoice_ui = Ui_MainManual()
#         # self.invoice_ui.setupUi(self.invoice_page)

#         # # Add the invoice page to main content area
#         # self.ui.mainContent.layout().addWidget(self.invoice_page)

#     def calculate_totals(self):
#         subtotal = 0.0
#         for row in range(self.table.rowCount()):
#             try:
#                 price_item = self.table.item(row, 4)
#                 qty_item = self.table.item(row, 5)
#                 if price_item and qty_item:
#                     price = float(price_item.text())
#                     qty = float(qty_item.text())
#                     subtotal += price * qty
#             except ValueError:
#                 pass  # Ignore if not numeric
#         tax = subtotal * 0.05
#         total = subtotal + tax

#         self.subtotal_label.setText(f"Subtotal: ₹{subtotal:.2f}")
#         self.tax_label.setText(f"Tax (5%): ₹{tax:.2f}")
#         self.total_label.setText(f"<b>Total: ₹{total:.2f}</b>")

#     def save_invoice(self):
#         customer = self.customer_name.text().strip()
#         contact = self.customer_contact.text().strip()
#         print(f"Invoice saved for {customer} ({contact})")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DashboardFull()
#     window.show()
#     sys.exit(app.exec_())
