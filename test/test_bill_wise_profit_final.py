"""
Final Comprehensive Test for Bill Wise Profit
Tests both data loading and GUI visibility
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.database.db_operations import ReportsDBOperations


def main():
    """Main test"""
    print("\n" + "="*80)
    print("BILL WISE PROFIT COMPREHENSIVE TEST")
    print("="*80)
    
    db = get_db_instance()
    db_operations = ReportsDBOperations()
    
    # Test 1: Database has data
    print("\n✓ TEST 1: Checking if database has invoices...")
    invoices = db.get_all_invoices()
    print(f"  Result: {len(invoices)} invoices found")
    
    if len(invoices) == 0:
        print("\n❌ PROBLEM FOUND: No invoices in database!")
        print("   Solution: Create some invoices first using the Home page")
        return
    
    # Test 2: Invoices have items
    print("\n✓ TEST 2: Checking if invoices have items...")
    first_invoice_id = invoices[0]['id']
    items = db.get_invoice_items(first_invoice_id)
    print(f"  Result: {len(items)} items found in first invoice")
    
    if len(items) == 0:
        print("\n❌ PROBLEM FOUND: Invoices exist but have no items!")
        print("   Solution: The invoice might be corrupted. Create a new invoice with items.")
        return
    
    # Test 3: ReportsDBOperations formats data correctly
    print("\n✓ TEST 3: Checking ReportsDBOperations.load_all_invoices()...")
    formatted_invoices = db_operations.load_all_invoices()
    print(f"  Result: {len(formatted_invoices)} formatted invoices")
    
    if len(formatted_invoices) == 0:
        print("\n❌ PROBLEM FOUND: ReportsDBOperations returned empty list!")
        print("   Solution: Check the ReportsDBOperations.load_all_invoices() method")
        return
    
    # Test 4: Formatted invoices have tickets
    print("\n✓ TEST 4: Checking if formatted invoices have tickets...")
    total_tickets = sum(len(inv.get('tickets', [])) for inv in formatted_invoices)
    print(f"  Result: {total_tickets} total tickets across all invoices")
    
    if total_tickets == 0:
        print("\n❌ PROBLEM FOUND: No tickets in formatted invoices!")
        print("   Solution: Check the ReportsDBOperations.load_all_invoices() method")
        print("   The method should be populating the 'tickets' list from invoice_items")
        return
    
    # Test 5: Bill Wise Profit populate logic
    print("\n✓ TEST 5: Testing Bill Wise Profit populate logic...")
    row_count = 0
    total_sale = 0.0
    total_cost = 0.0
    
    for invoice in formatted_invoices:
        tickets = invoice.get('tickets', [])
        for ticket in tickets:
            row_count += 1
            quantity = ticket.get('quantity', 1)
            total_amount = ticket.get('total_amount', 0.0)
            supplier_amount = ticket.get('supplier_amount', 0.0)
            
            sale_price = total_amount / quantity if quantity > 0 else total_amount
            cost_price = supplier_amount
            
            total_sale += total_amount
            total_cost += cost_price * quantity
    
    total_profit = total_sale - total_cost
    
    print(f"  Result: {row_count} rows will be displayed")
    print(f"  Total Sale: ₹{total_sale:,.2f}")
    print(f"  Total Cost: ₹{total_cost:,.2f}")
    print(f"  Total Profit: ₹{total_profit:,.2f}")
    
    if row_count == 0:
        print("\n❌ PROBLEM FOUND: Logic will produce 0 rows!")
        return
    
    # Final verdict
    print("\n" + "="*80)
    print("DIAGNOSIS COMPLETE")
    print("="*80)
    print(f"\n✅ Bill Wise Profit report should show {row_count} rows of data")
    print(f"✅ Total Profit: ₹{total_profit:,.2f}")
    print("\nIf you're not seeing data in the application, the issue is likely:")
    print("1. Date filters are hiding all data (check date range)")
    print("2. Report page isn't calling populate() when switching tabs")
    print("3. Report isn't visible due to UI layout issues")
    print("\nRECOMMENDATIONS:")
    print("1. Check the date filter settings in the Reports page")
    print("2. Try clicking 'Clear Filters' button")
    print("3. Make sure you're selecting 'Bill Wise Profit' from the sidebar")
    print("4. Check the logs for any error messages")
    
    print("\n" + "="*80)
    
    # Test with GUI
    print("\nDo you want to open the GUI test? (y/n): ", end='')
    try:
        response = input().strip().lower()
        if response == 'y':
            print("\nOpening GUI test window...")
            print("The window will show the Bill Wise Profit report with real data.")
            print("Press Ctrl+C in this console to close the window.")
            
            app = QApplication(sys.argv)
            
            from test_bill_wise_profit import TestWindow
            window = TestWindow()
            window.show()
            window.load_data()
            
            sys.exit(app.exec())
    except (EOFError, KeyboardInterrupt):
        print("\nSkipping GUI test.")


if __name__ == '__main__':
    main()
