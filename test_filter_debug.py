from travel_billing_software.ui.reports.db_operations import ReportsDBOperations
from datetime import datetime, date

# Load data
db = ReportsDBOperations()
all_invoices = db.load_all_invoices()

print(f"Loaded {len(all_invoices)} invoices")

# Simulate filter logic
from_date = date.today().replace(month=date.today().month-1 if date.today().month > 1 else 12)
to_date = date.today()

print(f"\nFilter date range: {from_date} to {to_date}")

for idx, invoice in enumerate(all_invoices[:3], 1):  # Test first 3
    print(f"\n=== Invoice {idx}: {invoice.get('invoice_number')} ===")
    try:
        # Date filter
        date_str = invoice.get('invoice_date') or invoice.get('date') or invoice.get('created_at', '')
        print(f"  date_str: '{date_str}' (type: {type(date_str)})")
        print(f"  date_str == 'None': {date_str == 'None'}")
        print(f"  bool(date_str): {bool(date_str)}")
        
        if date_str and date_str != 'None':
            print("  -> Has valid date string, parsing...")
        else:
            print("  -> No valid date, should PASS filter")
        
        # Contact filter
        contact = ''  # Empty in test
        customer_phone = invoice.get('customer_phone', '')
        print(f"  customer_phone: '{customer_phone}'")
        if contact and contact not in customer_phone.lower():
            print(f"  -> BLOCKED by contact filter")
        else:
            print(f"  -> Passed contact filter")
        
        # Booking type filter
        booking_type = "All"  # Default
        if booking_type != "All":
            print(f"  -> Checking booking type")
        else:
            print(f"  -> Passed booking type filter (All)")
        
        # Passenger/sector/supplier filter
        passenger = ''
        sector = ''
        supplier = "All"
        
        if passenger or sector or supplier != "All":
            print(f"  -> Checking passenger/sector/supplier filters")
        else:
            print(f"  -> Passed passenger/sector/supplier filter")
        
        print(f"  ✓ Invoice PASSED all filters")
        
    except Exception as e:
        print(f"  ✗ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
