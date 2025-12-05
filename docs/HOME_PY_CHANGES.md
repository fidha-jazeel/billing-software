# Home.py Migration - Specific Line Changes

## Summary
Update home.py (1275 lines) to work with new database schema instead of JSON files.

## Key Changes Required

### 1. Add Database Import (Line ~19)
**After line 19** (`from travel_billing_software.utils.styles import get_label_style`)

**ADD**:
```python
from travel_billing_software.database.db_manager import get_db_instance
```

### 2. Initialize Database in __init__ (Find line with `def __init__`)
Look for the HomePage class __init__ method (around line 200-250)

**ADD after `super().__init__()`**:
```python
self.db = get_db_instance()
# Load service types for dropdown
self.service_types = [st['name'] for st in self.db.get_service_types()]
# Load suppliers for dropdown  
suppliers = self.db.get_contacts('SUPPLIER')
self.suppliers = [s['name'] for s in suppliers]
```

### 3. Update Table Structure (Line 536-537)
**FIND**:
```python
self.table = QTableWidget(0, 9)
self.table.setHorizontalHeaderLabels(["Passenger Name", "PNR", "Sector", "Supplier", "Passport No.", "Qty", "Supp. Amt (₹)", "Cust. Amt (₹)", "Actions"])
```

**REPLACE WITH**:
```python
self.table = QTableWidget(0, 12)
self.table.setHorizontalHeaderLabels([
    "Service Type", "Passenger Name", "PNR", "Sector", "Supplier", 
    "Passport No.", "Qty", "Cost Price (₹)", "Selling Price (₹)", 
    "Tax %", "Total (₹)", "Actions"
])
```

### 4. Update add_item_row Method
This method needs complete rewrite to add 3 new columns. Find it around line 740.

The new structure for each row should be:
- Col 0: Service Type QComboBox (populated from self.service_types)
- Col 1: Passenger Name QLineEdit
- Col 2: PNR QLineEdit
- Col 3: Sector QComboBox
- Col 4: Supplier QComboBox (populated from self.suppliers)
- Col 5: Passport QLineEdit
- Col 6: Qty QDoubleSpinBox
- Col 7: Cost Price QDoubleSpinBox
- Col 8: Selling Price QDoubleSpinBox
- Col 9: Tax % QDoubleSpinBox
- Col 10: Total QLabel (calculated: (selling_price * qty) + tax)
- Col 11: Delete Button

### 5. Replace save_invoice Method (Line 1089)
**Complete replacement** - see MIGRATION_ROADMAP.md section 3.3 for full code.

Key points:
- Remove ALL JSON file operations
- Use `self.db.save_invoice(invoice_data)` 
- Silent save (no success popup)
- Reset form after successful save

### 6. Remove _save_to_db Helper Method (Line ~1150)
**DELETE THIS METHOD** - it's no longer needed since we save directly to DB.

### 7. Update Passenger History Methods
Find `_update_passenger_history` method - needs to use DB instead of JSON.

**REPLACE with**:
```python
def _update_passenger_history(self, invoice_data):
    """Passenger history is now automatic via database relationships."""
    pass  # No action needed - DB handles this
```

### 8. Add Helper Method for Currency Parsing
**ADD somewhere after save_invoice**:
```python
def _parse_currency(self, text):
    """Remove currency symbols and parse to float."""
    return float(text.replace('₹', '').replace(',', '').strip() or 0)
```

## Testing After Changes
1. Run the app: `python -m travel_billing_software.main`
2. Login with admin/admin
3. Create an invoice with multiple passengers
4. Check database: `sqlite3 billing.db "SELECT * FROM invoices;"`
5. Verify NO JSON files created in invoices/ folder

## Files Modified
- `travel_billing_software/ui/home.py` (8 changes across 1275 lines)

## Estimated Time
- 30-45 minutes for careful implementation
- Additional 15 minutes for testing

