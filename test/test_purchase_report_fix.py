"""
Test Purchase Report Functionality
Verifies that the Purchase Report loads invoices correctly and displays all data.
"""
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from travel_billing_software.database.db_manager import get_db_instance, DatabaseManager
from travel_billing_software.database.db_operations import ReportsDBOperations

def test_purchase_report_flow():
    """Test the complete Purchase Report data flow."""
    print("=" * 80)
    print("TESTING PURCHASE REPORT DATA FLOW")
    print("=" * 80)
    
    # Step 1: Initialize database
    print("\n1. DATABASE INITIALIZATION")
    print("-" * 80)
    
    # Reset singleton to ensure fresh connection
    import travel_billing_software.database.db_manager as db_module
    db_module._db_instance = None
    
    db = get_db_instance()
    print(f"✓ Database connected: {db.db_path}")
    
    # Step 2: Load invoices using Reports DB Operations (what the UI uses)
    print("\n2. LOADING INVOICES VIA REPORTS DB OPERATIONS")
    print("-" * 80)
    
    reports_db = ReportsDBOperations()
    invoices = reports_db.load_all_invoices()
    
    print(f"✓ Loaded {len(invoices)} invoices")
    
    if not invoices:
        print("✗ ERROR: No invoices found!")
        print("  The Purchase Report will show empty because no data is loaded.")
        return False
    
    # Step 3: Check invoice structure
    print("\n3. VALIDATING INVOICE DATA STRUCTURE")
    print("-" * 80)
    
    first_invoice = invoices[0]
    print(f"Invoice Number: {first_invoice.get('invoice_number')}")
    print(f"Invoice Date: {first_invoice.get('invoice_date')}")
    print(f"Customer: {first_invoice.get('customer_name')}")
    print(f"Total Amount: {first_invoice.get('total_amount')}")
    
    # Check passengers
    passengers = first_invoice.get('passengers', [])
    print(f"\nPassengers: {len(passengers)}")
    if passengers:
        print(f"  First Passenger: {passengers[0].get('name')}")
    
    # Check tickets
    tickets = first_invoice.get('tickets', [])
    print(f"\nTickets: {len(tickets)}")
    
    if not tickets:
        print("✗ ERROR: Invoice has NO TICKETS!")
        print("  The Purchase Report populate() method skips invoices with no tickets.")
        print("  This is why the report appears blank.")
        return False
    
    # Step 4: Validate ticket data (what Purchase Report displays)
    print("\n4. VALIDATING TICKET DATA (Purchase Report Columns)")
    print("-" * 80)
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\nTicket {i}:")
        print(f"  Passenger: {ticket.get('passenger_name')} {'✓' if ticket.get('passenger_name') else '✗ MISSING'}")
        print(f"  Supplier: {ticket.get('supplier_name')} {'✓' if ticket.get('supplier_name') else '✗ MISSING'}")
        print(f"  Sector: {ticket.get('sector')} {'✓' if ticket.get('sector') else '✗ MISSING'}")
        print(f"  PNR: {ticket.get('pnr')} {'✓' if ticket.get('pnr') else '✗ MISSING'}")
        print(f"  Cost (supplier_amount): {ticket.get('supplier_amount')} {'✓' if ticket.get('supplier_amount') else '✗ MISSING'}")
        print(f"  Price (unit_price): {ticket.get('unit_price')} {'✓' if ticket.get('unit_price') else '✗ MISSING'}")
        print(f"  Total Amount: {ticket.get('total_amount')} {'✓' if ticket.get('total_amount') else '✗ MISSING'}")
        print(f"  Quantity: {ticket.get('quantity')} {'✓' if ticket.get('quantity') else '✗ MISSING'}")
        
        # Calculate what would be displayed
        try:
            cost = float(ticket.get('supplier_amount', 0))
            price = float(ticket.get('unit_price', 0))
            if price == 0:
                price = float(ticket.get('total_amount', 0))
            qty = float(ticket.get('quantity', 1))
            
            ticket_cost = cost * qty
            ticket_sell = price * qty
            profit = ticket_sell - ticket_cost
            margin = (profit / ticket_sell * 100) if ticket_sell > 0 else 0
            
            print(f"\n  CALCULATED VALUES:")
            print(f"    Cost: {ticket_cost:.2f}")
            print(f"    Sell: {ticket_sell:.2f}")
            print(f"    Profit: {profit:.2f}")
            print(f"    Margin: {margin:.1f}%")
            
            if ticket_cost == 0 and ticket_sell == 0:
                print("    ⚠ WARNING: Both cost and sell are 0 - row will show zeros")
        except Exception as e:
            print(f"    ✗ ERROR calculating financials: {e}")
    
    # Step 5: Simulate populate() logic
    print("\n5. SIMULATING PURCHASE REPORT POPULATE() METHOD")
    print("-" * 80)
    
    row_count = 0
    invoices_with_tickets = 0
    invoices_without_tickets = 0
    
    for invoice in invoices:
        tickets = invoice.get('tickets', [])
        if not tickets:
            invoices_without_tickets += 1
            continue
        
        invoices_with_tickets += 1
        row_count += len(tickets)
    
    print(f"Total Invoices: {len(invoices)}")
    print(f"  With Tickets: {invoices_with_tickets}")
    print(f"  Without Tickets: {invoices_without_tickets} (skipped)")
    print(f"Expected Table Rows: {row_count}")
    
    if row_count == 0:
        print("\n✗ CRITICAL ISSUE: Purchase Report will show ZERO rows!")
        print("  Reason: All invoices either have no tickets or are filtered out.")
        return False
    
    # Step 6: Check if date filtering might exclude invoices
    print("\n6. CHECKING DATE FILTER COMPATIBILITY")
    print("-" * 80)
    
    from datetime import datetime
    
    for invoice in invoices[:3]:  # Check first 3 invoices
        date_str = invoice.get('invoice_date') or invoice.get('date', '')
        print(f"\nInvoice {invoice.get('invoice_number')}:")
        print(f"  Date String: '{date_str}'")
        
        try:
            if '/' in str(date_str):
                parts = str(date_str).split('/')
                day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                parsed_date = datetime(year, month, day).date()
            elif ' ' in str(date_str):
                date_part = str(date_str).split()[0]
                parsed_date = datetime.strptime(date_part, '%Y-%m-%d').date()
            else:
                parsed_date = datetime.strptime(str(date_str), '%Y-%m-%d').date()
            
            print(f"  Parsed Date: {parsed_date}")
            print(f"  ✓ Date filter compatible")
        except Exception as e:
            print(f"  ✗ Date parsing failed: {e}")
            print(f"  ℹ Invoice will be INCLUDED (date filter is optional)")
    
    # Final Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"✓ Database Connection: Working")
    print(f"✓ Invoice Loading: {len(invoices)} invoices")
    print(f"✓ Ticket Data: {row_count} rows expected")
    
    if row_count > 0:
        print(f"\n✅ SUCCESS: Purchase Report should display {row_count} rows")
        print(f"   If the report still shows blank:")
        print(f"   1. Check date filter settings (ensure date range is wide enough)")
        print(f"   2. Check filter dropdowns (Supplier, Type should be 'All')")
        print(f"   3. Verify Reports page is calling load_report_data() on tab switch")
        print(f"   4. Check browser console for JavaScript errors (if web-based)")
        return True
    else:
        print(f"\n✗ FAILURE: Purchase Report will show 0 rows")
        return False

if __name__ == "__main__":
    success = test_purchase_report_flow()
    sys.exit(0 if success else 1)
