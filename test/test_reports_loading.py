"""Simple test to see what Reports page loads"""
import sys
import os
sys.path.insert(0, '.')

# Clear cache
import travel_billing_software.database.db_manager as db_mod
db_mod._db_instance = None

from travel_billing_software.database.db_operations import ReportsDBOperations

print("Testing Reports page invoice loading...")
print("=" * 60)

try:
    reports_db = ReportsDBOperations()
    invoices = reports_db.load_all_invoices()
    
    print(f"\nTotal invoices loaded: {len(invoices)}")
    
    for inv in invoices:
        print(f"\n  Invoice: {inv['invoice_number']}")
        print(f"  Date: {inv['invoice_date']}")
        print(f"  Customer: {inv['customer_name']}")
        print(f"  Total: {inv['total_amount']}")
        print(f"  Items/Tickets: {len(inv.get('tickets', []))}")
        print(f"  Passengers: {len(inv.get('passengers', []))}")
        
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
