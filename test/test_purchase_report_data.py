"""Test script to check invoice and items data for Purchase Report."""
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.database.db_operations import ReportsDBOperations

def test_database_data():
    """Check what data is in the database."""
    print("=" * 80)
    print("TESTING DATABASE DATA FOR PURCHASE REPORT")
    print("=" * 80)
    
    # Test 1: Raw database queries
    print("\n1. RAW DATABASE CHECK")
    print("-" * 80)
    db = get_db_instance()
    
    # Get all invoices
    invoices = db.get_all_invoices()
    print(f"✓ Total invoices in database: {len(invoices)}")
    
    if invoices:
        first_invoice = invoices[0]
        print(f"\n--- First Invoice ---")
        print(f"  ID: {first_invoice.get('id')}")
        print(f"  Invoice Number: {first_invoice.get('invoice_number')}")
        print(f"  Date: {first_invoice.get('date')}")
        print(f"  Contact ID: {first_invoice.get('contact_id')}")
        print(f"  Customer Name: {first_invoice.get('customer_name')}")
        print(f"  Total Amount: {first_invoice.get('total_amount')}")
        print(f"  All Keys: {list(first_invoice.keys())}")
        
        # Get items for this invoice
        items = db.get_invoice_items(first_invoice.get('id'))
        print(f"\n  Invoice Items: {len(items)} items")
        
        if items:
            first_item = items[0]
            print(f"\n  --- First Item ---")
            print(f"    ID: {first_item.get('id')}")
            print(f"    PNR: {first_item.get('pnr_number')}")
            print(f"    Ticket#: {first_item.get('ticket_number')}")
            print(f"    Sector: {first_item.get('sector')}")
            print(f"    Passenger: {first_item.get('passenger_name')}")
            print(f"    Supplier: {first_item.get('supplier_name')}")
            print(f"    Supplier ID: {first_item.get('supplier_id')}")
            print(f"    Cost Price: {first_item.get('cost_price')}")
            print(f"    Unit Price: {first_item.get('unit_price')}")
            print(f"    Quantity: {first_item.get('quantity')}")
            print(f"    Total Amount: {first_item.get('total_amount')}")
            print(f"    All Item Keys: {list(first_item.keys())}")
    else:
        print("✗ No invoices found in database!")
        return
    
    # Test 2: Reports DB Operations (what the report actually uses)
    print("\n\n2. REPORTS DB OPERATIONS CHECK")
    print("-" * 80)
    
    reports_db = ReportsDBOperations()
    loaded_invoices = reports_db.load_all_invoices()
    
    print(f"✓ Total invoices loaded for reports: {len(loaded_invoices)}")
    
    if loaded_invoices:
        first_report_inv = loaded_invoices[0]
        print(f"\n--- First Loaded Invoice (Report Format) ---")
        print(f"  Invoice Number: {first_report_inv.get('invoice_number')}")
        print(f"  Invoice Date: {first_report_inv.get('invoice_date')}")
        print(f"  Customer Name: {first_report_inv.get('customer_name')}")
        print(f"  Total Amount: {first_report_inv.get('total_amount')}")
        print(f"  Paid Amount: {first_report_inv.get('paid_amount')}")
        print(f"  Balance: {first_report_inv.get('balance')}")
        print(f"  Payment Status: {first_report_inv.get('payment_status')}")
        
        passengers = first_report_inv.get('passengers', [])
        tickets = first_report_inv.get('tickets', [])
        
        print(f"\n  Passengers: {len(passengers)}")
        if passengers:
            print(f"    First Passenger: {passengers[0].get('name')}")
        
        print(f"\n  Tickets: {len(tickets)} items")
        if tickets:
            first_ticket = tickets[0]
            print(f"\n  --- First Ticket ---")
            print(f"    PNR: {first_ticket.get('pnr')}")
            print(f"    Ticket Number: {first_ticket.get('ticket_number')}")
            print(f"    Sector: {first_ticket.get('sector')}")
            print(f"    Passenger Name: {first_ticket.get('passenger_name')}")
            print(f"    Supplier Name: {first_ticket.get('supplier_name')}")
            print(f"    Supplier Amount: {first_ticket.get('supplier_amount')}")
            print(f"    Unit Price: {first_ticket.get('unit_price')}")
            print(f"    Total Amount: {first_ticket.get('total_amount')}")
            print(f"    Quantity: {first_ticket.get('quantity')}")
            print(f"    All Ticket Keys: {list(first_ticket.keys())}")
        else:
            print("  ✗ No tickets found in report data!")
    
    # Test 3: Check Purchase Report Population Logic
    print("\n\n3. PURCHASE REPORT POPULATION TEST")
    print("-" * 80)
    
    if loaded_invoices:
        test_invoice = loaded_invoices[0]
        print(f"Testing with invoice: {test_invoice.get('invoice_number')}")
        print(f"Tickets in invoice: {len(test_invoice.get('tickets', []))}")
        
        if not test_invoice.get('tickets'):
            print("✗ PROBLEM FOUND: Invoice has NO tickets!")
            print("   This is why the Purchase Report shows blank rows.")
            print("   The populate() method skips invoices with no tickets.")
        else:
            print("✓ Invoice has tickets - should display properly")
            
            # Show what would be displayed
            for i, ticket in enumerate(test_invoice.get('tickets', []), 1):
                print(f"\n  Row {i} would show:")
                print(f"    Date: {test_invoice.get('invoice_date')}")
                print(f"    Invoice#: {test_invoice.get('invoice_number')}")
                print(f"    Passenger: {ticket.get('passenger_name')}")
                print(f"    Supplier: {ticket.get('supplier_name')}")
                print(f"    Sector: {ticket.get('sector')}")
                print(f"    PNR: {ticket.get('pnr')}")
                
                cost = float(ticket.get('supplier_amount', 0))
                qty = float(ticket.get('quantity', 1))
                sell = float(ticket.get('unit_price', 0))
                
                if sell == 0:
                    sell = float(ticket.get('total_amount', 0))
                
                total_cost = cost * qty
                total_sell = sell * qty
                profit = total_sell - total_cost
                margin = (profit / total_sell * 100) if total_sell > 0 else 0
                
                print(f"    Cost: {total_cost:.2f}")
                print(f"    Sell: {total_sell:.2f}")
                print(f"    Profit: {profit:.2f}")
                print(f"    Margin: {margin:.1f}%")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_database_data()
