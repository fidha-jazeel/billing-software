"""
Simple Quick Test - Just run this to verify Bill Wise Profit works
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.ui.reports.db_operations import ReportsDBOperations

print("\n" + "="*80)
print("QUICK TEST: Bill Wise Profit Data Check")
print("="*80 + "\n")

# Initialize
db = get_db_instance()
db_ops = ReportsDBOperations()

# Load data
print("Loading invoices from database...")
invoices = db_ops.load_all_invoices()

print(f"✓ Found {len(invoices)} invoices")

if invoices:
    total_tickets = sum(len(inv.get('tickets', [])) for inv in invoices)
    print(f"✓ Found {total_tickets} tickets/items total")
    
    # Calculate what will be shown
    rows = 0
    for inv in invoices:
        rows += len(inv.get('tickets', []))
    
    print(f"\n✅ Bill Wise Profit report should display {rows} rows")
    
    # Show first few items
    print(f"\nFirst invoice details:")
    first = invoices[0]
    print(f"  Invoice: {first.get('invoice_number')}")
    print(f"  Date: {first.get('invoice_date')}")
    print(f"  Customer: {first.get('customer_name')}")
    print(f"  Tickets: {len(first.get('tickets', []))}")
    
    if first.get('tickets'):
        print(f"\n  First ticket:")
        t = first['tickets'][0]
        print(f"    PNR: {t.get('pnr')}")
        print(f"    Sector: {t.get('sector')}")
        print(f"    Sale: ₹{t.get('total_amount', 0):,.2f}")
        print(f"    Cost: ₹{t.get('supplier_amount', 0):,.2f}")
        print(f"    Profit: ₹{(t.get('total_amount', 0) - t.get('supplier_amount', 0)):,.2f}")
    
    print("\n✅ DATA IS AVAILABLE! If you don't see it in the app, check:")
    print("   1. Date filters (clear them)")
    print("   2. Make sure Bill Wise Profit tab is selected")
    print("   3. Click Refresh button")
else:
    print("\n❌ No invoices found in database!")
    print("   Create some invoices first using the Home page")

print("\n" + "="*80 + "\n")
