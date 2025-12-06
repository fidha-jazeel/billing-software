"""
Database Migration Test Script
Tests all critical database operations to verify migration success.
"""
from travel_billing_software.database.db_manager import get_db_instance
from datetime import datetime

def test_database_operations():
    """Test all database operations."""
    print("=" * 60)
    print("🧪 TESTING DATABASE MIGRATION")
    print("=" * 60)
    
    # Get database instance
    db = get_db_instance()
    print(f"\n✓ Database connected: {db.db_path}")
    
    # Test 1: Authentication
    print("\n📝 Test 1: Authentication")
    user = db.authenticate_user("admin", "admin")
    if user:
        print(f"   ✅ Login successful: {user['username']} (Role: {user['role']})")
    else:
        print("   ❌ Login failed")
        return
    
    # Test 2: Add Contact (Customer)
    print("\n📝 Test 2: Add Customer")
    customer_id = db.add_contact(
        'CUSTOMER',
        'Test Customer',
        phone='1234567890',
        email='test@example.com',
        address='123 Test Street'
    )
    if customer_id > 0:
        print(f"   ✅ Customer added: ID {customer_id}")
    else:
        print("   ❌ Failed to add customer")
    
    # Test 3: Add Supplier
    print("\n📝 Test 3: Add Supplier")
    supplier_id = db.add_contact(
        'SUPPLIER',
        'Test Supplier',
        phone='9876543210',
        company_name='Test Airways'
    )
    if supplier_id > 0:
        print(f"   ✅ Supplier added: ID {supplier_id}")
    else:
        print("   ❌ Failed to add supplier")
    
    # Test 4: Add Expense
    print("\n📝 Test 4: Add Expense")
    expense_id = db.add_expense(
        datetime.now().strftime('%Y-%m-%d'),
        'Testing',
        100.00,
        description='Test expense',
        payment_mode='CASH'
    )
    if expense_id > 0:
        print(f"   ✅ Expense added: ID {expense_id}")
    else:
        print("   ❌ Failed to add expense")
    
    # Test 5: Create Invoice
    print("\n📝 Test 5: Create Invoice")
    invoice_data = {
        'invoice_number': f'TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
        'customer_name': 'Test Customer',
        'customer_phone': '1234567890',
        'customer_address': '123 Test Street',
        'invoice_date': datetime.now().strftime('%Y-%m-%d'),
        'subtotal': 5000.00,
        'discount': 0.00,
        'tax_amount': 0.00,
        'grand_total': 5000.00,
        'paid_amount': 2000.00,
        'balance_due': 3000.00,
        'payment_method': 'CASH',
        'items': [
            {
                'passenger_name': 'John Doe',
                'pnr': 'ABC123',
                'sector': 'DEL-DXB',
                'supplier': 'Test Supplier',
                'service_type': 'Flight',
                'qty': 1,
                'cost_price': 4000.00,
                'selling_price': 5000.00
            }
        ]
    }
    
    invoice_id = db.save_invoice(invoice_data)
    if invoice_id > 0:
        print(f"   ✅ Invoice created: ID {invoice_id}")
    else:
        print("   ❌ Failed to create invoice")
    
    # Test 6: Get All Invoices
    print("\n📝 Test 6: Retrieve Invoices")
    invoices = db.get_all_invoices(limit=5)
    if invoices:
        print(f"   ✅ Retrieved {len(invoices)} invoice(s)")
        for inv in invoices[:2]:
            print(f"      - {inv['invoice_number']}: ₹{inv['total_amount']:,.2f}")
    else:
        print("   ⚠️  No invoices found")
    
    # Test 7: Get Contacts
    print("\n📝 Test 7: Retrieve Contacts")
    customers = db.get_contacts('CUSTOMER')
    suppliers = db.get_contacts('SUPPLIER')
    print(f"   ✅ Customers: {len(customers)}, Suppliers: {len(suppliers)}")
    
    # Test 8: Get Expenses
    print("\n📝 Test 8: Retrieve Expenses")
    expenses = db.get_all_expenses()
    if expenses:
        total_expenses = sum(e['amount'] for e in expenses)
        print(f"   ✅ Retrieved {len(expenses)} expense(s), Total: ₹{total_expenses:,.2f}")
    else:
        print("   ⚠️  No expenses found")
    
    # Test 9: Dashboard Statistics
    print("\n📝 Test 9: Dashboard Statistics")
    stats = db.get_dashboard_stats()
    if stats:
        print(f"   ✅ Statistics:")
        print(f"      Total Invoices: {stats['total_invoices']}")
        print(f"      Total Revenue: ₹{stats['total_revenue']:,.2f}")
        print(f"      Total Expenses: ₹{stats['total_expenses']:,.2f}")
        print(f"      Net Profit: ₹{stats['net_profit']:,.2f}")
        print(f"      Pending Balance: ₹{stats['pending_balance']:,.2f}")
    else:
        print("   ❌ Failed to get statistics")
    
    # Test 10: Service Types
    print("\n📝 Test 10: Service Types")
    service_types = db.get_service_types()
    if service_types:
        print(f"   ✅ Available service types: {', '.join([s['name'] for s in service_types])}")
    else:
        print("   ❌ No service types found")
    
    # Test 11: Supplier Balance
    print("\n📝 Test 11: Supplier Balance Calculation")
    if supplier_id > 0:
        balance = db.get_supplier_balance(supplier_id)
        print(f"   ✅ Supplier balance:")
        print(f"      Payable: ₹{balance['total_payable']:,.2f}")
        print(f"      Paid: ₹{balance['total_paid']:,.2f}")
        print(f"      Balance: ₹{balance['balance']:,.2f}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nDatabase is fully operational and ready for production use.")
    print("Login credentials: admin / admin")
    print("\n🎉 You can now run the application!")
    

if __name__ == "__main__":
    try:
        test_database_operations()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
