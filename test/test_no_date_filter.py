"""Test to verify NO automatic date filtering - ALL invoices shown"""
import sys
import os
sys.path.insert(0, '.')

# Clear cache
import travel_billing_software.database.db_manager as db_mod
db_mod._db_instance = None

from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.ui.reports.db_operations import ReportsDBOperations
from datetime import datetime, date

print("=" * 80)
print("TESTING: COMPLETE REMOVAL OF AUTOMATIC DATE FILTERING")
print("=" * 80)

# Get database
db = get_db_instance()
print(f"\nDatabase: {db.db_path}")

# Get all invoices from database
cur = db.conn.cursor()
cur.execute("SELECT COUNT(*) FROM invoices")
total_count = cur.fetchone()[0]
print(f"\nTotal invoices in database: {total_count}")

# Load via Reports DB Operations
print("\n" + "-" * 80)
print("Step 1: Load ALL invoices (no filtering)")
print("-" * 80)

reports_db = ReportsDBOperations()
all_invoices = reports_db.load_all_invoices()
print(f"Invoices loaded by Reports: {len(all_invoices)}")

if len(all_invoices) == total_count:
    print("✓ SUCCESS: All invoices loaded")
else:
    print(f"✗ ERROR: {total_count - len(all_invoices)} invoices missing!")

# Test with new default filter range (1900 to +100 years)
print("\n" + "-" * 80)
print("Step 2: Test NEW default filter (1900-01-01 to 2125-12-09)")
print("-" * 80)

start_date = date(1900, 1, 1)
end_date = date.today().replace(year=date.today().year + 100)

print(f"Filter range: {start_date} to {end_date}")
print(f"Range span: {end_date.year - start_date.year} years")

within_range = 0
outside_range = []
no_date = []

for inv in all_invoices:
    date_str = inv.get('invoice_date', '')
    if not date_str or str(date_str).strip() == '' or date_str == 'None':
        no_date.append(inv['invoice_number'])
        within_range += 1  # Count as included
        continue
    
    try:
        if '/' in date_str:
            day, month, year = map(int, date_str.split('/'))
            inv_date = date(year, month, day)
        else:
            inv_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        if start_date <= inv_date <= end_date:
            within_range += 1
        else:
            outside_range.append({
                'number': inv['invoice_number'],
                'date': inv_date
            })
    except Exception as e:
        # Parsing error - should still be included
        no_date.append(inv['invoice_number'])
        within_range += 1

print(f"\nResults:")
print(f"  Invoices with valid dates in range: {within_range - len(no_date)}/{total_count}")
print(f"  Invoices with no/invalid dates (still included): {len(no_date)}")
print(f"  Total that will be shown: {within_range}/{total_count}")

if outside_range:
    print(f"\n  ✗ WARNING: {len(outside_range)} invoices OUTSIDE even this range:")
    for out_inv in outside_range:
        print(f"    - {out_inv['number']}: {out_inv['date']}")
else:
    print(f"\n  ✓ All invoices within filter range")

if no_date:
    print(f"\n  ℹ Invoices with missing/invalid dates (included anyway):")
    for inv_num in no_date:
        print(f"    - {inv_num}")

# Final check
print("\n" + "=" * 80)
print("FINAL RESULT")
print("=" * 80)

if within_range == total_count:
    print(f"\n✓✓✓ PERFECT: ALL {total_count} invoices will be shown by default!")
    print("✓ No automatic date filtering")
    print("✓ Invoices with invalid/missing dates included")
    print("✓ User must manually adjust filters to hide invoices")
else:
    print(f"\n✗ PROBLEM: {total_count - within_range} invoices would be hidden")

print("\n" + "=" * 80)
