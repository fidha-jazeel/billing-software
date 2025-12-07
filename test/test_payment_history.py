"""
Test script to check payment history records.
"""
from travel_billing_software.database.db_manager import get_db_instance

def test_payment_history():
    """Test if all payment records are being retrieved."""
    db = get_db_instance()
    
    print("Testing Payment History Retrieval...")
    print("-" * 50)
    
    # Get all payments
    payments = db.get_all_payments_received()
    
    print(f"Total payments found: {len(payments)}")
    print()
    
    if payments:
        print("First 5 payments:")
        for i, payment in enumerate(payments[:5], 1):
            print(f"\n{i}. Payment #{payment.get('payment_number', 'N/A')}")
            print(f"   Date: {payment.get('date', 'N/A')}")
            print(f"   Customer: {payment.get('customer_name', 'N/A')}")
            print(f"   Invoice: {payment.get('invoice_number', 'N/A')}")
            print(f"   Amount: ₹{payment.get('amount', 0):,.2f}")
            print(f"   Mode: {payment.get('payment_mode', 'N/A')}")
        
        if len(payments) > 5:
            print(f"\n... and {len(payments) - 5} more payments")
    else:
        print("No payments found in database!")
    
    print("\n" + "-" * 50)

if __name__ == "__main__":
    test_payment_history()
