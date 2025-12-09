"""
Test script to diagnose why some invoices don't appear in Reports page.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Clear cached database instance
import travel_billing_software.database.db_manager as db_module
db_module._db_instance = None

from travel_billing_software.database.db_manager import get_db_instance
from datetime import datetime

print("=" * 80)
print("INVOICE VISIBILITY DIAGNOSTIC TEST")
print("=" * 80)

db = get_db_instance()
print(f"\nDatabase: {db.db_path}\n")

# Test 1: Check all invoices in database
print("-" * 80)
print("TEST 1: Check all invoices in database")
print("-" * 80)

cur = db.conn.cursor()
cur.execute("""
    SELECT i.id, i.invoice_number, i.date, i.contact_id, i.total_amount, 
           i.status, i.payment_status, i.created_at,
           c.name as customer_name, c.phone as customer_phone
    FROM invoices i
    LEFT JOIN contacts c ON i.contact_id = c.id
    ORDER BY i.created_at DESC
""")

invoices = cur.fetchall()
print(f"\nTotal invoices in database: {len(invoices)}")

for inv in invoices:
    print(f"\nInvoice #{inv['invoice_number']}")
    print(f"  ID: {inv['id']}")
    print(f"  Date: {inv['date']}")
    print(f"  Created At: {inv['created_at']}")
    print(f"  Customer: {inv['customer_name']} ({inv['customer_phone']})")
    print(f"  Contact ID: {inv['contact_id']}")
    print(f"  Total: {inv['total_amount']}")
    print(f"  Status: {inv['status']}")
    print(f"  Payment Status: {inv['payment_status']}")
    
    # Check items for this invoice
    cur.execute("""
        SELECT COUNT(*) as item_count,
               GROUP_CONCAT(DISTINCT p.name) as passengers,
               GROUP_CONCAT(DISTINCT ii.sector) as sectors
        FROM invoice_items ii
        LEFT JOIN passengers p ON ii.passenger_id = p.id
        WHERE ii.invoice_id = ?
    """, (inv['id'],))
    
    item_info = cur.fetchone()
    print(f"  Items: {item_info['item_count']}")
    print(f"  Passengers: {item_info['passengers'] or 'None'}")
    print(f"  Sectors: {item_info['sectors'] or 'None'}")

# Test 2: Simulate Reports page loading
print("\n" + "=" * 80)
print("TEST 2: Simulate Reports page invoice loading")
print("=" * 80)

try:
    from travel_billing_software.ui.reports.db_operations import ReportsDBOperations
    
    reports_db = ReportsDBOperations()
    loaded_invoices = reports_db.load_all_invoices()
    
    print(f"\nInvoices loaded by Reports page: {len(loaded_invoices)}")
    
    # Check which invoices were loaded
    loaded_invoice_numbers = [inv['invoice_number'] for inv in loaded_invoices]
    all_invoice_numbers = [inv['invoice_number'] for inv in invoices]
    
    missing = set(all_invoice_numbers) - set(loaded_invoice_numbers)
    
    if missing:
        print(f"\n⚠ WARNING: {len(missing)} invoices are MISSING from Reports page!")
        print(f"Missing invoices: {', '.join(missing)}")
    else:
        print(f"\n✓ All invoices are being loaded by Reports page")
    
    # Show details of loaded invoices
    print(f"\nLoaded invoices:")
    for inv in loaded_invoices:
        print(f"  - {inv['invoice_number']}: {inv['customer_name']}, "
              f"Date: {inv['invoice_date']}, "
              f"Items: {len(inv.get('tickets', []))}, "
              f"Passengers: {len(inv.get('passengers', []))}")
        
except Exception as e:
    print(f"\n✗ Error loading invoices through Reports page: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check for common issues
print("\n" + "=" * 80)
print("TEST 3: Check for common data quality issues")
print("=" * 80)

issues_found = []

for inv in invoices:
    invoice_issues = []
    
    # Check for missing/invalid dates
    if not inv['date'] or inv['date'] == 'None':
        invoice_issues.append("Missing or invalid date field")
    
    # Check for missing customer
    if not inv['contact_id']:
        invoice_issues.append("Missing contact_id")
    
    # Check for missing customer name
    if not inv['customer_name']:
        invoice_issues.append("Missing customer name")
    
    # Check for items
    cur.execute("SELECT COUNT(*) as count FROM invoice_items WHERE invoice_id = ?", (inv['id'],))
    item_count = cur.fetchone()['count']
    if item_count == 0:
        invoice_issues.append("No items found")
    
    if invoice_issues:
        issues_found.append({
            'invoice_number': inv['invoice_number'],
            'issues': invoice_issues
        })

if issues_found:
    print(f"\n⚠ Found {len(issues_found)} invoices with data quality issues:")
    for issue_inv in issues_found:
        print(f"\n  Invoice {issue_inv['invoice_number']}:")
        for issue in issue_inv['issues']:
            print(f"    - {issue}")
else:
    print("\n✓ No data quality issues found")

# Test 4: Test filter logic
print("\n" + "=" * 80)
print("TEST 4: Test default filter date range")
print("=" * 80)

from datetime import date, timedelta

today = date.today()
ten_years_ago = today.replace(year=today.year - 10)

print(f"\nDefault filter range: {ten_years_ago} to {today}")

# Check which invoices fall within default date range
cur.execute("""
    SELECT invoice_number, date, created_at
    FROM invoices
""")

all_invoices = cur.fetchall()
within_range = 0
outside_range = []

for inv in all_invoices:
    try:
        inv_date_str = inv['date'] or inv['created_at']
        if inv_date_str and inv_date_str != 'None':
            if ' ' in inv_date_str:
                inv_date_str = inv_date_str.split()[0]
            inv_date = datetime.strptime(inv_date_str, '%Y-%m-%d').date()
            
            if ten_years_ago <= inv_date <= today:
                within_range += 1
            else:
                outside_range.append({
                    'number': inv['invoice_number'],
                    'date': inv_date
                })
    except Exception as e:
        outside_range.append({
            'number': inv['invoice_number'],
            'date': f"Invalid: {inv_date_str}",
            'error': str(e)
        })

print(f"\nInvoices within default date range: {within_range}/{len(all_invoices)}")

if outside_range:
    print(f"\n⚠ {len(outside_range)} invoices are OUTSIDE the default date range:")
    for out_inv in outside_range:
        print(f"  - {out_inv['number']}: {out_inv['date']}")
        if 'error' in out_inv:
            print(f"    Error: {out_inv['error']}")

print("\n" + "=" * 80)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 80)
