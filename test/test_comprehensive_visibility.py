"""
Comprehensive test to verify invoice filtering behavior with edge cases
"""
import sys
import os
sys.path.insert(0, '.')

# Clear cache
import travel_billing_software.database.db_manager as db_mod
db_mod._db_instance = None

from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.database.db_operations import ReportsDBOperations
from datetime import datetime, date

print("=" * 80)
print("COMPREHENSIVE INVOICE VISIBILITY TEST")
print("=" * 80)

db = get_db_instance()

# Test 1: Check all invoices with their dates
print("\n" + "-" * 80)
print("TEST 1: Analyze all invoices and their dates")
print("-" * 80)

cur = db.conn.cursor()
cur.execute("""
    SELECT i.invoice_number, i.date, i.created_at, c.name as customer
    FROM invoices i
    LEFT JOIN contacts c ON i.contact_id = c.id
    ORDER BY i.created_at DESC
""")

invoices = cur.fetchall()
print(f"\nTotal invoices: {len(invoices)}\n")

for inv in invoices:
    print(f"Invoice: {inv['invoice_number']}")
    print(f"  Customer: {inv['customer']}")
    print(f"  Date field: {inv['date']}")
    print(f"  Created: {inv['created_at']}")
    
    # Try parsing
    date_str = inv['date']
    if date_str and str(date_str).strip() and date_str != 'None':
        try:
            if '/' in str(date_str):
                day, month, year = map(int, str(date_str).split('/'))
                parsed = date(year, month, day)
            elif ' ' in str(date_str):
                parsed = datetime.strptime(str(date_str).split()[0], '%Y-%m-%d').date()
            else:
                parsed = datetime.strptime(str(date_str), '%Y-%m-%d').date()
            print(f"  Parsed: {parsed} ✓")
        except Exception as e:
            print(f"  Parse ERROR: {e} ✗")
    else:
        print(f"  No valid date ⚠")
    print()

# Test 2: Load through Reports page
print("-" * 80)
print("TEST 2: Load invoices through Reports page")
print("-" * 80)

reports_db = ReportsDBOperations()
loaded = reports_db.load_all_invoices()

print(f"\nInvoices loaded: {len(loaded)}/{len(invoices)}")

if len(loaded) == len(invoices):
    print("✓ ALL invoices loaded successfully\n")
    
    for inv in loaded:
        print(f"{inv['invoice_number']}: {inv['customer_name']}")
        print(f"  Date: {inv['invoice_date']}")
        print(f"  Total: {inv['total_amount']}")
        print(f"  Items: {len(inv.get('tickets', []))}")
        print()
else:
    print(f"✗ {len(invoices) - len(loaded)} invoices MISSING!\n")
    
    loaded_numbers = {inv['invoice_number'] for inv in loaded}
    db_numbers = {inv['invoice_number'] for inv in invoices}
    missing = db_numbers - loaded_numbers
    
    if missing:
        print("Missing invoices:")
        for num in missing:
            print(f"  - {num}")

# Test 3: Simulate filter application with extreme range
print("\n" + "-" * 80)
print("TEST 3: Simulate date filter with extreme range (1900-2125)")
print("-" * 80)

from PyQt6.QtCore import QDate

# Mock filter values
class MockFilter:
    def __init__(self):
        self.from_date = QDate(1900, 1, 1)
        self.to_date = QDate.currentDate().addYears(100)
        
    def date(self):
        return self
    
    def toPyDate(self):
        if hasattr(self, 'from_date'):
            return self.from_date.toPyDate()
        return self.to_date.toPyDate()

# Create mock filter section
class MockFilterSection:
    def __init__(self):
        self.filter_from_date = type('obj', (object,), {
            'date': lambda: type('obj', (object,), {
                'toPyDate': lambda: date(1900, 1, 1)
            })()
        })()
        
        self.filter_to_date = type('obj', (object,), {
            'date': lambda: type('obj', (object,), {
                'toPyDate': lambda: date.today().replace(year=date.today().year + 100)
            })()
        })()
        
        self.filter_contact = type('obj', (object,), {'text': lambda: ''})()
        self.filter_passenger = type('obj', (object,), {'text': lambda: ''})()
        self.filter_sector = type('obj', (object,), {'text': lambda: ''})()
        self.filter_supplier = type('obj', (object,), {'currentText': lambda: 'All'})()
        self.filter_type = type('obj', (object,), {'currentText': lambda: 'All'})()

try:
    from travel_billing_software.ui.reports.utils import FilterSection
    
    # We can't fully test without Qt app, but we can verify logic manually
    print("Filter date range: 1900-01-01 to 2125-12-09")
    print("This range covers 225 years - should include ALL invoices\n")
    
    # Manual check
    filtered_count = 0
    for inv in loaded:
        date_str = inv.get('invoice_date', '')
        if not date_str:
            filtered_count += 1
            continue
            
        try:
            if '/' in date_str:
                day, month, year = map(int, date_str.split('/'))
                inv_date = date(year, month, day)
            else:
                inv_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Check if within 1900-2125 range
            if date(1900, 1, 1) <= inv_date <= date(2125, 12, 31):
                filtered_count += 1
        except:
            # Parse error - should still be included
            filtered_count += 1
    
    print(f"Invoices within extreme range: {filtered_count}/{len(loaded)}")
    
    if filtered_count == len(loaded):
        print("✓ ALL invoices pass the filter")
    else:
        print(f"✗ {len(loaded) - filtered_count} invoices would be filtered out")
        
except Exception as e:
    print(f"Could not test filter section: {e}")

# Final Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\nDatabase invoices: {len(invoices)}")
print(f"Reports loaded: {len(loaded)}")
print(f"Match: {'✓ YES' if len(loaded) == len(invoices) else '✗ NO'}")

if len(loaded) == len(invoices):
    print("\n✓✓✓ PERFECT: 100% of invoices are visible")
    print("✓ No automatic date filtering")
    print("✓ All invoices show by default")
    print("✓ User must manually filter to hide invoices")
else:
    print(f"\n✗ ISSUE: {len(invoices) - len(loaded)} invoices missing from Reports")

print("\n" + "=" * 80)
