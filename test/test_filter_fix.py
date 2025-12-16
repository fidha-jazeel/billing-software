"""Test to verify all invoices appear after fixes"""
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
print("TESTING INVOICE VISIBILITY AFTER FIXES")
print("=" * 80)

# Get database
db = get_db_instance()
print(f"\nDatabase: {db.db_path}")

# Get all invoices
cur = db.conn.cursor()
cur.execute("SELECT COUNT(*) FROM invoices")
total_count = cur.fetchone()[0]
print(f"\nTotal invoices in database: {total_count}")

# Load via Reports DB Operations
print("\n" + "-" * 80)
print("Step 1: Load invoices via ReportsDBOperations")
print("-" * 80)

reports_db = ReportsDBOperations()
all_invoices = reports_db.load_all_invoices()
print(f"Invoices loaded: {len(all_invoices)}")

if len(all_invoices) == total_count:
    print("✓ All invoices loaded successfully")
else:
    print(f"✗ WARNING: {total_count - len(all_invoices)} invoices missing!")

# Test date filter with old default (10 years)
print("\n" + "-" * 80)
print("Step 2: Test with OLD default filter (10 years ago)")
print("-" * 80)

ten_years_ago = date.today().replace(year=date.today().year - 10)
today = date.today()

print(f"Filter range: {ten_years_ago} to {today}")

within_old_range = []
outside_old_range = []

for inv in all_invoices:
    date_str = inv.get('invoice_date', '')
    if date_str:
        try:
            if '/' in date_str:
                day, month, year = map(int, date_str.split('/'))
                inv_date = date(year, month, day)
            else:
                inv_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            if ten_years_ago <= inv_date <= today:
                within_old_range.append(inv['invoice_number'])
            else:
                outside_old_range.append({
                    'number': inv['invoice_number'],
                    'date': inv_date
                })
        except Exception as e:
            print(f"  Error parsing date for {inv['invoice_number']}: {e}")

print(f"\nWithin 10-year range: {len(within_old_range)}/{len(all_invoices)}")
if outside_old_range:
    print(f"✗ OUTSIDE 10-year range (would be HIDDEN): {len(outside_old_range)}")
    for out_inv in outside_old_range:
        print(f"  - {out_inv['number']}: {out_inv['date']}")
else:
    print("✓ All invoices are within 10-year range")

# Test date filter with new default (50 years)
print("\n" + "-" * 80)
print("Step 3: Test with NEW default filter (50 years ago) - FIXED")
print("-" * 80)

fifty_years_ago = date.today().replace(year=date.today().year - 50)

print(f"Filter range: {fifty_years_ago} to {today}")

within_new_range = []
outside_new_range = []

for inv in all_invoices:
    date_str = inv.get('invoice_date', '')
    if date_str:
        try:
            if '/' in date_str:
                day, month, year = map(int, date_str.split('/'))
                inv_date = date(year, month, day)
            else:
                inv_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            if fifty_years_ago <= inv_date <= today:
                within_new_range.append(inv['invoice_number'])
            else:
                outside_new_range.append({
                    'number': inv['invoice_number'],
                    'date': inv_date
                })
        except Exception as e:
            print(f"  Error parsing date for {inv['invoice_number']}: {e}")

print(f"\nWithin 50-year range: {len(within_new_range)}/{len(all_invoices)}")
if outside_new_range:
    print(f"⚠ STILL OUTSIDE 50-year range: {len(outside_new_range)}")
    for out_inv in outside_new_range:
        print(f"  - {out_inv['number']}: {out_inv['date']}")
else:
    print("✓ All invoices are within 50-year range")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\nTotal invoices in database: {total_count}")
print(f"Invoices loaded by Reports: {len(all_invoices)}")
print(f"Would show with old 10-year filter: {len(within_old_range)}")
print(f"Will show with new 50-year filter: {len(within_new_range)}")

if len(within_new_range) == total_count:
    print("\n✓✓✓ SUCCESS: All invoices will now appear in Reports page!")
elif len(within_new_range) > len(within_old_range):
    print(f"\n✓ IMPROVED: {len(within_new_range) - len(within_old_range)} more invoices will appear")
    if len(within_new_range) < total_count:
        print(f"  But {total_count - len(within_new_range)} invoices still outside range")
else:
    print(f"\n✗ No improvement: {total_count - len(within_new_range)} invoices still hidden")

print("\n" + "=" * 80)
