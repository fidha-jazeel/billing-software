# Database Migration Roadmap - Implementation Guide

## ✅ COMPLETED TASKS

### Task 1: Database Manager (100% Complete)
**File**: `travel_billing_software/database/db_manager.py`
- ✅ Production schema with 13 tables implemented
- ✅ Authentication methods (authenticate_user, get_current_user)
- ✅ Contacts CRUD (unified customers & suppliers)
- ✅ Passengers management with auto-creation
- ✅ Passport details tracking
- ✅ Service types methods
- ✅ Complete invoice operations (save, get, update, delete)
- ✅ Payments received tracking
- ✅ Supplier payments & balance calculation
- ✅ Expenses CRUD
- ✅ Purchase bills with items
- ✅ Dashboard statistics
- ✅ Legacy dropdown support
- ✅ Backup functionality

### Task 2: Login Page (100% Complete)
**File**: `travel_billing_software/ui/login_page.py`
- ✅ Updated to use database authentication instead of AuthManager
- ✅ Username + password fields (was password-only)
- ✅ Dark theme matching supplier page
- ✅ Default credentials: admin / admin
- ✅ Vyapar-style silent login (no success popup)
- ✅ Emits login_successful signal

---

## 🔄 IN-PROGRESS TASKS

### Task 3: Update Home Page Invoice Form (30% Complete)
**File**: `travel_billing_software/ui/home.py` (1275 lines - needs major rewrite)

#### Current State:
- 9 columns: Passenger Name, PNR, Sector, Supplier, Passport No., Qty, Supp. Amt, Cust. Amt, Actions
- Saves to JSON file (`invoices/invoice_*.json`)
- Has passport dialog for entering passport details
- Uses old customer model (flat customer_name field)

#### Required Changes:

**1. Table Structure (Line 536-537)**
```python
# OLD: 9 columns
self.table = QTableWidget(0, 9)
self.table.setHorizontalHeaderLabels(["Passenger Name", "PNR", "Sector", "Supplier", "Passport No.", "Qty", "Supp. Amt (₹)", "Cust. Amt (₹)", "Actions"])

# NEW: 12 columns
self.table = QTableWidget(0, 12)
self.table.setHorizontalHeaderLabels([
    "Service Type",      # NEW - dropdown from service_types table
    "Passenger Name",     # Existing
    "PNR",               # Existing
    "Sector",            # Existing
    "Supplier",          # Existing - from contacts where type='SUPPLIER'
    "Passport No.",      # Existing
    "Qty",               # Existing
    "Cost Price (₹)",    # NEW - renamed from Supp. Amt
    "Selling Price (₹)", # NEW - renamed from Cust. Amt
    "Tax %",             # NEW - per-line tax rate
    "Total (₹)",         # NEW - calculated (read-only)
    "Actions"            # Existing
])
```

**2. Add Item Row Method (needs update)**
Location: After line 740 (`def add_item_row`)
- Add Service Type combo box (first column)
- Update all column indices (+1 for new service type column)
- Add Tax % spin box
- Add Total label (read-only calculated field)
- Connect tax_rate change to calculate line total

**3. Update Save Invoice Method (Line 1089)**
```python
def save_invoice(self):
    """Save invoice to database using new schema."""
    try:
        # Validate inputs
        if not self.customer_name.text().strip():
            QMessageBox.warning(self, "Validation", "Customer name is required")
            return
        
        if not self.contact_number.text().strip():
            QMessageBox.warning(self, "Validation", "Contact number is required")
            return
        
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Validation", "Add at least one item")
            return
        
        # Prepare invoice data for new schema
        invoice_data = {
            'invoice_number': self.invoice_number.text(),
            'date': self.invoice_date.date().toString("yyyy-MM-dd"),
            'customer_name': self.customer_name.text().strip(),
            'contact_number': self.contact_number.text().strip(),
            'customer_address': self.customer_address.text().strip(),
            'sub_total': self._parse_currency(self.lbl_subtotal.text()),
            'discount_amount': float(self.txt_discount.text() or 0),
            'tax_amount': self._parse_currency(self.lbl_tax.text()),
            'total_amount': self._parse_currency(self.lbl_total.text()),
            'received_amount': float(self.txt_received.text() or 0),
            'payment_mode': 'CASH',  # Add payment mode dropdown
            'items': []
        }
        
        # Collect items from table
        for r in range(self.table.rowCount()):
            service_type = self.table.cellWidget(r, 0).currentText()
            passenger_name = self.table.cellWidget(r, 1).text()
            pnr_number = self.table.cellWidget(r, 2).text()
            sector = self.table.cellWidget(r, 3).text()
            supplier_name = self.table.cellWidget(r, 4).currentText()
            passport_no = self.table.cellWidget(r, 5).text()
            qty = self.table.cellWidget(r, 6).value()
            cost_price = self.table.cellWidget(r, 7).value()
            unit_price = self.table.cellWidget(r, 8).value()
            tax_rate = self.table.cellWidget(r, 9).value()
            
            tax_amount = (unit_price * qty * tax_rate) / 100
            total = (unit_price * qty) + tax_amount
            
            item = {
                'service_type': service_type,
                'passenger_name': passenger_name,
                'pnr_number': pnr_number,
                'sector': sector,
                'supplier_name': supplier_name,
                'quantity': qty,
                'cost_price': cost_price,
                'unit_price': unit_price,
                'tax_rate': tax_rate,
                'tax_amount': tax_amount,
                'total_amount': total,
                'passport_details': self.passport_data_store.get(passenger_name, {})
            }
            
            # Add travel-specific fields (if service is Flight)
            if service_type == 'Flight':
                item['travel_date'] = self.invoice_date.date().toString("yyyy-MM-dd")
                item['airline_name'] = ''  # Add airline dropdown if needed
            
            invoice_data['items'].append(item)
        
        # Save to database (NO JSON FILES!)
        success, invoice_id = self.db.save_invoice(invoice_data)
        
        if success:
            # Silent save (no popup) - Vyapar style
            self.reset_invoice()  # Clear form for next invoice
        else:
            QMessageBox.critical(self, "Error", "Failed to save invoice to database")
            
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Save failed:\n{str(e)}")
        import traceback
        traceback.print_exc()

def _parse_currency(self, text):
    """Remove currency symbols and parse float."""
    return float(text.replace('₹', '').replace(',', '').strip() or 0)
```

**4. Initialize Database Connection (Line ~200)**
```python
def __init__(self, dashboard=None):
    super().__init__()
    self.dashboard = dashboard
    self.db = get_db_instance()  # ADD THIS LINE
    
    # Load service types for dropdown
    self.service_types = [st['name'] for st in self.db.get_service_types()]
    
    # Load suppliers for dropdown
    suppliers = self.db.get_contacts('SUPPLIER')
    self.suppliers = [s['name'] for s in suppliers]
    
    # Rest of init...
```

**5. Remove JSON File Operations**
- Delete line ~1139: `filename = f"invoices/invoice_{invoice_data['invoice_number']}.json"`
- Delete line ~1140-1142: JSON file write code
- Delete `_save_to_db` method (line ~1150) - no longer needed, save direct to DB

---

## 📋 PENDING TASKS

### Task 4: Create Payments Management Page
**New File**: `travel_billing_software/ui/payments_page.py`

Create a new page for managing customer payments:
- List invoices with pending balance
- Record payment against invoice
- Update invoice payment_status
- Show payment history per customer
- Use `db.add_payment_received()` method

### Task 5: Update Supplier Page
**File**: `travel_billing_software/ui/supplier_page.py`

Changes needed:
- Replace JSON file read/write with `db.get_contacts('SUPPLIER')`
- Use `db.add_contact('SUPPLIER', ...)` for new suppliers
- Use `db.update_contact()` and `db.delete_contact()`
- Add supplier balance display using `db.get_supplier_balance()`

### Task 6: Update Supplier Billing Page
**File**: `travel_billing_software/ui/supplier_billing_page.py`

Changes needed:
- Use `db.get_purchase_bills()` instead of JSON
- Use `db.add_purchase_bill()` for new bills
- Link bills to suppliers via `supplier_id` foreign key
- Show supplier payment history

### Task 7: Update Expenses Page
**File**: `travel_billing_software/ui/expenses_page.py`

Changes needed:
- Replace JSON with `db.get_all_expenses()`
- Use `db.add_expense()` for new expenses
- Use `db.update_expense()` and `db.delete_expense()`
- Remove `expenses/expenses.json` dependency

### Task 8: Update Reports Page
**File**: `travel_billing_software/ui/reports.py`

Changes needed:
- Replace all JSON file reads with database queries
- Use `db.get_all_invoices()` for invoice reports
- Use `db.get_dashboard_stats()` for statistics
- Add profit reports (revenue - cost_price difference)
- Add supplier balance reports
- Add customer outstanding reports

### Task 9: Update Main Window
**File**: `travel_billing_software/ui/main_window.py`

Changes needed:
1. Add login check on startup:
```python
def __init__(self):
    super().__init__()
    self.db = get_db_instance()
    
    # Show login page first
    self.login_page = LoginPage()
    self.login_page.login_successful.connect(self.show_main_window)
    self.login_page.show()
```

2. Add Payments page to navigation menu
3. Pass db instance to all pages

### Task 10: Remove JSON Dependencies
**Files to Clean**:
1. Delete or archive `invoices/` folder
2. Delete or archive `expenses/expenses.json`
3. Delete or archive `suppliers/suppliers.json`
4. Update `config/settings.json` - keep only UI settings, remove data
5. Search codebase for `json.load` and `json.dump` - remove data-related uses

---

## 🎯 TESTING CHECKLIST

After all tasks complete, test:
- [ ] Login with admin/admin works
- [ ] Create invoice with multiple passengers
- [ ] Passengers auto-grouped by contact number
- [ ] Service types dropdown populated
- [ ] Suppliers dropdown populated from DB
- [ ] Cost price and selling price both visible
- [ ] Tax calculation works per line
- [ ] Invoice saves to database (no JSON)
- [ ] Payment recording works
- [ ] Supplier payments work
- [ ] Expenses CRUD works
- [ ] Reports show DB data
- [ ] Dashboard statistics accurate
- [ ] No JSON file operations for data

---

## 🚀 IMPLEMENTATION PRIORITY

**Critical Path** (must be done in order):
1. ✅ Database Manager (DONE)
2. ✅ Login Page (DONE)
3. 🔄 Home Page Invoice Form (IN PROGRESS - 30%)
4. Main Window Login Integration
5. All other pages in parallel

**Recommended Order**:
- Task 3 (Home) - Most complex, most critical
- Task 9 (Main Window) - Enables testing login flow
- Task 8 (Reports) - High visibility, needs DB queries
- Task 5 (Suppliers) - Needed for invoice form
- Task 7 (Expenses) - Simple, quick win
- Task 4 (Payments) - New feature, medium complexity
- Task 6 (Supplier Billing) - Medium complexity
- Task 10 (Cleanup) - Final step

---

## 📊 PROGRESS SUMMARY

| Task | Status | Completion | Complexity |
|------|--------|------------|------------|
| 1. Database Manager | ✅ Done | 100% | High |
| 2. Login Page | ✅ Done | 100% | Low |
| 3. Home Page | 🔄 In Progress | 30% | Very High |
| 4. Payments Page | ⏸️ Pending | 0% | Medium |
| 5. Supplier Page | ⏸️ Pending | 0% | Medium |
| 6. Supplier Billing | ⏸️ Pending | 0% | Medium |
| 7. Expenses Page | ⏸️ Pending | 0% | Low |
| 8. Reports Page | ⏸️ Pending | 0% | High |
| 9. Main Window | ⏸️ Pending | 0% | Low |
| 10. JSON Cleanup | ⏸️ Pending | 0% | Low |

**Overall Progress**: 23% Complete (2.3 / 10 tasks)

---

## 🔧 QUICK REFERENCE

### Database Methods Cheat Sheet

**Authentication**:
```python
db.authenticate_user(username, password)  # Returns user dict or None
db.get_current_user()  # Returns current logged-in user
```

**Contacts** (Customers & Suppliers):
```python
db.add_contact('CUSTOMER', name, phone=..., email=...)
db.get_contacts('CUSTOMER')  # Get all customers
db.get_contacts('SUPPLIER')  # Get all suppliers
db.get_or_create_contact(name, phone, 'CUSTOMER')
db.update_contact(contact_id, name=..., phone=...)
db.delete_contact(contact_id)
db.search_contacts('search_text', 'CUSTOMER')
```

**Passengers**:
```python
db.add_passenger(contact_id, name, contact_number, dob=..., age=...)
db.get_or_create_passenger(contact_id, name, contact_number)
db.get_passengers_by_contact_number(contact_number)
```

**Invoices**:
```python
db.save_invoice(invoice_data)  # Returns (success, invoice_id)
db.get_invoice(invoice_number)  # Returns full invoice with items
db.get_all_invoices(limit=100)
db.update_invoice_status(invoice_id, 'CANCELLED')
db.delete_invoice(invoice_id)
```

**Payments**:
```python
db.add_payment_received(contact_id, invoice_id, amount, payment_mode, date)
db.get_payments_by_contact(contact_id)
db.get_all_payments_received()
```

**Service Types**:
```python
db.get_service_types()  # Returns list of all service types
db.get_service_type_by_name('Flight')  # Returns specific service type
```

**Expenses**:
```python
db.add_expense(date, category, amount, description=..., payment_mode=...)
db.get_all_expenses()
db.update_expense(expense_id, category=..., amount=...)
db.delete_expense(expense_id)
```

**Statistics**:
```python
db.get_dashboard_stats()  # Returns dict with all key metrics
db.get_supplier_balance(supplier_id)  # Returns payable/paid/balance
```

---

## 📝 NOTES

1. **No Success Popups**: Follow Vyapar style - silent saves, no "Save Successful" dialogs
2. **Dark Theme**: All pages should match supplier_page.py aesthetic (#1a1a1a background)
3. **Auto-Creation**: Use get_or_create_* methods to prevent duplicate entries
4. **Foreign Keys**: Always use IDs (contact_id, passenger_id) not names
5. **Validation**: Add proper validation before saving (required fields, numeric checks)
6. **Error Handling**: Wrap all DB operations in try/except blocks
7. **Testing**: Test with the test_db.py script after each major change

---

**Last Updated**: December 5, 2025
**Database Version**: Production Schema v1.0
**Status**: Active Migration - 23% Complete
