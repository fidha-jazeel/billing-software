"""
Diagnostic test for Bill Wise Profit - Console output only
Tests data structure and population logic without GUI
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.ui.reports.db_operations import ReportsDBOperations
from travel_billing_software.config.config import format_currency, get_currency_symbol


def test_database_structure():
    """Test database structure and content"""
    print("\n" + "="*80)
    print("BILL WISE PROFIT DIAGNOSTIC TEST")
    print("="*80)
    
    db = get_db_instance()
    db_operations = ReportsDBOperations()
    
    print("\n1. CHECKING RAW DATABASE INVOICES")
    print("-" * 80)
    
    try:
        # Get raw invoices
        invoices = db.get_all_invoices()
        print(f"✅ Found {len(invoices)} invoices in database")
        
        if not invoices:
            print("❌ ERROR: No invoices found in database!")
            print("   The database might be empty or the table doesn't exist.")
            return
        
        # Show first invoice details
        first_invoice = invoices[0]
        print(f"\nFirst invoice (ID: {first_invoice.get('id')}):")
        print(f"  - Invoice Number: {first_invoice.get('invoice_number')}")
        print(f"  - Date: {first_invoice.get('date')}")
        print(f"  - Customer: {first_invoice.get('customer_name')}")
        print(f"  - Total: {first_invoice.get('total_amount')}")
        
        print("\n2. CHECKING INVOICE ITEMS")
        print("-" * 80)
        
        # Get items for first invoice
        items = db.get_invoice_items(first_invoice['id'])
        print(f"✅ Found {len(items)} items for invoice {first_invoice.get('invoice_number')}")
        
        if not items:
            print("❌ ERROR: No items found for this invoice!")
            print("   Invoices exist but have no items/tickets.")
            return
        
        # Show first item structure
        first_item = items[0]
        print(f"\nFirst item structure:")
        item_dict = dict(first_item)
        for key in sorted(item_dict.keys()):
            print(f"  - {key}: {item_dict[key]}")
        
        print("\n3. CHECKING FORMATTED INVOICES (ReportsDBOperations)")
        print("-" * 80)
        
        # Test formatted invoices
        formatted_invoices = db_operations.load_all_invoices()
        print(f"✅ Formatted {len(formatted_invoices)} invoices")
        
        if not formatted_invoices:
            print("❌ ERROR: ReportsDBOperations returned empty list!")
            return
        
        # Show first formatted invoice
        first = formatted_invoices[0]
        print(f"\nFirst formatted invoice:")
        print(f"  - Invoice Number: {first.get('invoice_number')}")
        print(f"  - Invoice Date: {first.get('invoice_date')}")
        print(f"  - Customer: {first.get('customer_name')}")
        print(f"  - Total: {first.get('total_amount')}")
        print(f"  - Passengers: {len(first.get('passengers', []))} found")
        print(f"  - Tickets: {len(first.get('tickets', []))} found")
        
        if not first.get('tickets'):
            print("❌ ERROR: No tickets in formatted invoice!")
            print("   The issue is in ReportsDBOperations.load_all_invoices()")
            return
        
        # Show first ticket structure
        first_ticket = first['tickets'][0]
        print(f"\nFirst ticket structure:")
        for key in sorted(first_ticket.keys()):
            print(f"  - {key}: {first_ticket[key]}")
        
        print("\n4. SIMULATING BillWiseProfitView.populate() LOGIC")
        print("-" * 80)
        
        total_sale = 0.0
        total_cost = 0.0
        total_profit = 0.0
        row_count = 0
        
        for invoice in formatted_invoices[:3]:  # Test first 3 invoices
            tickets = invoice.get('tickets', [])
            passengers = invoice.get('passengers', [])
            
            print(f"\nInvoice {invoice.get('invoice_number')}:")
            print(f"  - Passengers: {len(passengers)}")
            print(f"  - Tickets: {len(tickets)}")
            
            for idx, ticket in enumerate(tickets):
                row_count += 1
                
                # Calculate per-item values
                quantity = ticket.get('quantity', 1)
                total_amount = ticket.get('total_amount', 0.0)
                supplier_amount = ticket.get('supplier_amount', 0.0)
                
                sale_price = total_amount / quantity if quantity > 0 else total_amount
                cost_price = supplier_amount
                profit = sale_price - cost_price
                margin = (profit / sale_price * 100) if sale_price > 0 else 0.0
                
                total_sale += total_amount
                total_cost += cost_price * quantity
                total_profit += profit * quantity
                
                print(f"  Ticket {idx + 1}:")
                print(f"    - PNR: {ticket.get('pnr')}")
                print(f"    - Passenger: {ticket.get('passenger_name')}")
                print(f"    - Supplier: {ticket.get('supplier_name')}")
                print(f"    - Sector: {ticket.get('sector')}")
                print(f"    - Quantity: {quantity}")
                print(f"    - Sale Price: {format_currency(sale_price)}")
                print(f"    - Cost Price: {format_currency(cost_price)}")
                print(f"    - Profit: {format_currency(profit)}")
                print(f"    - Margin: {margin:.2f}%")
        
        print("\n5. SUMMARY")
        print("-" * 80)
        print(f"Total rows to be displayed: {row_count}")
        print(f"Total Sale: {format_currency(total_sale)}")
        print(f"Total Cost: {format_currency(total_cost)}")
        print(f"Total Profit: {format_currency(total_profit)}")
        
        if row_count == 0:
            print("\n❌ ERROR: No rows will be displayed!")
            print("   Issue: Tickets list is empty in formatted invoices")
        else:
            print(f"\n✅ SUCCESS: {row_count} rows should be displayed")
        
        print("\n6. CHECKING ALL INVOICES")
        print("-" * 80)
        total_tickets = sum(len(inv.get('tickets', [])) for inv in formatted_invoices)
        print(f"Total invoices: {len(formatted_invoices)}")
        print(f"Total tickets across all invoices: {total_tickets}")
        
        if total_tickets == 0:
            print("\n❌ CRITICAL ERROR: NO TICKETS FOUND IN ANY INVOICE!")
            print("   Possible causes:")
            print("   1. invoice_items table is empty")
            print("   2. ReportsDBOperations is not properly joining tables")
            print("   3. Data format mismatch between database and code")
        else:
            print(f"\n✅ Data looks good: {total_tickets} tickets found")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)


def test_with_sample_data():
    """Test the logic with sample data"""
    print("\n" + "="*80)
    print("TESTING WITH SAMPLE DATA")
    print("="*80)
    
    sample_invoices = [
        {
            'invoice_number': 'INV-001',
            'invoice_date': '10/12/2024',
            'customer_name': 'Test Customer',
            'passengers': [
                {'name': 'John Doe', 'contact_number': '1234567890'}
            ],
            'tickets': [
                {
                    'pnr': 'ABC123',
                    'supplier_name': 'Emirates',
                    'sector': 'DEL-DXB',
                    'booking_type': 'Flight',
                    'quantity': 1,
                    'supplier_amount': 20000.00,
                    'total_amount': 25000.00,
                    'passenger_name': 'John Doe'
                }
            ]
        }
    ]
    
    print(f"\nSample data: {len(sample_invoices)} invoices")
    print(f"Sample tickets: {len(sample_invoices[0]['tickets'])} tickets")
    
    # Simulate populate logic
    total_sale = 0.0
    total_cost = 0.0
    total_profit = 0.0
    row_count = 0
    
    for invoice in sample_invoices:
        tickets = invoice.get('tickets', [])
        for ticket in tickets:
            row_count += 1
            quantity = ticket.get('quantity', 1)
            total_amount = ticket.get('total_amount', 0.0)
            supplier_amount = ticket.get('supplier_amount', 0.0)
            
            sale_price = total_amount / quantity if quantity > 0 else total_amount
            cost_price = supplier_amount
            profit = sale_price - cost_price
            
            total_sale += total_amount
            total_cost += cost_price * quantity
            total_profit += profit * quantity
    
    print(f"\n✅ Sample data processed successfully")
    print(f"   Rows: {row_count}")
    print(f"   Sale: {format_currency(total_sale)}")
    print(f"   Cost: {format_currency(total_cost)}")
    print(f"   Profit: {format_currency(total_profit)}")
    
    print("="*80 + "\n")


if __name__ == '__main__':
    test_database_structure()
    test_with_sample_data()
    
    print("\n✅ Diagnostic test complete!")
    print("   Check the output above to identify the issue.")
    print()
