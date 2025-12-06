"""
Database Operations Module for Reports
Handles all database queries and data transformations for reports.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.utils.logger import log_info, log_error, log_warning


class ReportsDBOperations:
    """
    Centralized database operations for all reports.
    
    Responsibilities:
    - Fetch invoices, items, payments, and supplier bills from database
    - Transform database records into report-friendly formats
    - Calculate aggregated metrics (totals, balances, profits)
    - Handle date conversions and formatting
    """
    
    def __init__(self):
        """Initialize database connection and logger."""
        self.db = get_db_instance()
        log_info("ReportsDBOperations initialized", 'billing_app')
    
    def load_all_invoices(self) -> List[Dict[str, Any]]:
        """
        Load all invoices with their items and calculate paid amounts from payments_received table.
        
        Returns:
            List of invoice dictionaries with passengers and tickets
            
        Raises:
            Exception: If database query fails
        """
        try:
            invoices = self.db.get_all_invoices()
            log_info(f"Loading {len(invoices)} invoices from database", 'billing_app')
            
            result = []
            for inv in invoices:
                # Calculate paid amount from payments_received table
                payments = self.db.get_payments_by_contact(inv['contact_id'])
                invoice_payments = [p for p in payments if p.get('invoice_id') == inv['id']]
                paid_amount = sum(float(p.get('amount', 0)) for p in invoice_payments)
                
                # Get payment mode from latest payment
                payment_mode = 'UNPAID'
                if invoice_payments:
                    latest_payment = invoice_payments[0]  # Already sorted DESC by date
                    payment_mode = latest_payment.get('payment_mode', 'CASH')
                
                invoice_dict = self._format_invoice_record(inv)
                invoice_dict['paid_amount'] = paid_amount
                invoice_dict['balance'] = invoice_dict['total_amount'] - paid_amount
                invoice_dict['payment_mode'] = payment_mode
                
                # Update payment status based on balance
                if invoice_dict['balance'] <= 0:
                    invoice_dict['payment_status'] = 'PAID'
                elif paid_amount > 0:
                    invoice_dict['payment_status'] = 'PARTIAL'
                else:
                    invoice_dict['payment_status'] = 'UNPAID'
                
                # Get invoice items (tickets) for this invoice
                items = self.db.get_invoice_items(inv['id'])
                
                for item in items:
                    # Add passenger info
                    passenger_name = item.get('passenger_name', '')
                    passenger_contact = item.get('passenger_contact', '')
                    
                    if passenger_name:
                        # Check if passenger already added
                        if not any(p['name'] == passenger_name for p in invoice_dict['passengers']):
                            invoice_dict['passengers'].append({
                                'name': passenger_name,
                                'contact_number': passenger_contact
                            })
                    
                    # Add ticket/item info with proper date handling
                    travel_date_str = item.get('travel_date', '')
                    try:
                        if travel_date_str:
                            date_obj = datetime.strptime(travel_date_str, '%Y-%m-%d')
                            travel_date_formatted = date_obj.strftime('%d/%m/%Y')
                        else:
                            travel_date_formatted = ''
                    except Exception:
                        travel_date_formatted = travel_date_str
                    
                    invoice_dict['tickets'].append({
                        'pnr': item.get('pnr_number', ''),
                        'ticket_number': item.get('ticket_number', ''),
                        'supplier_name': item.get('supplier_name', ''),
                        'sector': item.get('sector', ''),
                        'booking_type': item.get('service_type_name', ''),
                        'quantity': int(item.get('quantity', 1)),
                        'supplier_amount': float(item.get('cost_price', 0)),
                        'total_amount': float(item.get('total_amount', 0)),
                        'passport_number': item.get('passport_number', ''),
                        'passenger_name': passenger_name,
                        'travel_date': travel_date_formatted,
                        'unit_price': float(item.get('unit_price', 0))
                    })
                
                result.append(invoice_dict)
            
            log_info(
                f"Successfully loaded {len(result)} invoices with "
                f"{sum(len(inv['tickets']) for inv in result)} items",
                'billing_app'
            )
            return result
                
        except Exception as e:
            log_error("Failed to load invoices from database", exception=e, logger_name='billing_errors')
            raise
    
    def _format_invoice_record(self, inv: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert database invoice record to report format.
        
        Args:
            inv: Raw invoice record from database
            
        Returns:
            Formatted invoice dictionary
        """
        # Convert invoice_date to dd/MM/yyyy format
        invoice_date_str = inv.get('invoice_date', '')
        try:
            if invoice_date_str:
                date_obj = datetime.strptime(invoice_date_str, '%Y-%m-%d')
                invoice_date_formatted = date_obj.strftime('%d/%m/%Y')
            else:
                invoice_date_formatted = ''
        except Exception:
            invoice_date_formatted = invoice_date_str
        
        return {
            'invoice_number': inv.get('invoice_number', ''),
            'invoice_date': invoice_date_formatted,
            'customer_name': inv.get('customer_name', ''),
            'customer_phone': inv.get('contact_number', ''),
            'total_amount': float(inv.get('total_amount', 0)),
            'paid_amount': float(inv.get('paid_amount', 0)),
            'balance': float(inv.get('balance', 0)),
            'payment_status': inv.get('payment_status', 'UNPAID'),
            'passengers': [],
            'tickets': []
        }
    
    def get_all_payments_summary(self) -> Dict[str, float]:
        """
        Calculate total cash and bank payments received.
        
        Returns:
            Dictionary with 'cash' and 'bank' totals
        """
        try:
            total_cash = 0.0
            total_bank = 0.0
            
            all_payments = self.db.get_all_payments_received()
            
            for payment in all_payments:
                amount = float(payment.get('amount', 0))
                payment_mode = payment.get('payment_mode', '').upper()
                
                if payment_mode == 'CASH':
                    total_cash += amount
                else:  # BANK, UPI, CARD, CHEQUE - all count as bank
                    total_bank += amount
            
            log_info(
                f"Payment summary - Cash: ₹{total_cash:,.2f}, Bank: ₹{total_bank:,.2f}",
                'billing_app'
            )
            
            return {'cash': total_cash, 'bank': total_bank}
            
        except Exception as e:
            log_error("Error calculating payment summary", exception=e, logger_name='billing_errors')
            return {'cash': 0.0, 'bank': 0.0}
    
    def get_supplier_bills(self) -> List[Dict[str, Any]]:
        """
        Fetch all supplier bills from database.
        
        Returns:
            List of supplier bill dictionaries
        """
        try:
            bills = self.db.get_all_supplier_bills()
            log_info(f"Loaded {len(bills)} supplier bills", 'billing_app')
            return bills
        except Exception as e:
            log_error("Failed to load supplier bills", exception=e, logger_name='billing_errors')
            return []
    
    def get_expenses(self) -> List[Dict[str, Any]]:
        """
        Fetch all expense records from database.
        
        Returns:
            List of expense dictionaries
        """
        try:
            expenses = self.db.get_all_expenses()
            log_info(f"Loaded {len(expenses)} expenses", 'billing_app')
            return expenses
        except Exception as e:
            log_error("Failed to load expenses", exception=e, logger_name='billing_errors')
            return []
    
    def calculate_balance_report(self) -> List[Dict[str, Any]]:
        """
        Calculate customer-wise balance report.
        
        Returns:
            List of customer balance records with totals and status
        """
        try:
            invoices = self.load_all_invoices()
            
            # Group by customer phone number
            customer_balances = {}
            
            for inv in invoices:
                phone = inv['customer_phone']
                name = inv['customer_name']
                
                if phone not in customer_balances:
                    customer_balances[phone] = {
                        'customer_name': name,
                        'contact_number': phone,
                        'total': 0.0,
                        'received': 0.0,
                        'balance': 0.0,
                        'last_date': inv['invoice_date'],
                        'invoice_count': 0
                    }
                
                customer_balances[phone]['total'] += inv['total_amount']
                customer_balances[phone]['received'] += inv['paid_amount']
                customer_balances[phone]['balance'] += inv['balance']
                customer_balances[phone]['invoice_count'] += 1
                
                # Update last invoice date
                try:
                    current_date = datetime.strptime(inv['invoice_date'], '%d/%m/%Y')
                    last_date = datetime.strptime(customer_balances[phone]['last_date'], '%d/%m/%Y')
                    if current_date > last_date:
                        customer_balances[phone]['last_date'] = inv['invoice_date']
                except Exception:
                    pass
            
            result = list(customer_balances.values())
            log_info(f"Calculated balance report for {len(result)} customers", 'billing_app')
            return result
            
        except Exception as e:
            log_error("Failed to calculate balance report", exception=e, logger_name='billing_errors')
            return []
    
    def calculate_profit_metrics(self, invoices: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate profit metrics from invoices.
        
        Args:
            invoices: List of invoice dictionaries with tickets
            
        Returns:
            Dictionary with total_sale, total_cost, and gross_profit
        """
        total_sale = 0.0
        total_cost = 0.0
        
        for inv in invoices:
            total_sale += inv['total_amount']
            
            for ticket in inv['tickets']:
                total_cost += ticket['supplier_amount'] * ticket['quantity']
        
        gross_profit = total_sale - total_cost
        
        return {
            'total_sale': total_sale,
            'total_cost': total_cost,
            'gross_profit': gross_profit,
            'profit_margin': (gross_profit / total_sale * 100) if total_sale > 0 else 0.0
        }
    
    def filter_invoices_by_date(
        self,
        invoices: List[Dict[str, Any]],
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter invoices by date range.
        
        Args:
            invoices: List of invoice dictionaries
            from_date: Start date in dd/MM/yyyy format
            to_date: End date in dd/MM/yyyy format
            
        Returns:
            Filtered list of invoices
        """
        if not from_date and not to_date:
            return invoices
        
        try:
            filtered = []
            
            for inv in invoices:
                invoice_date = datetime.strptime(inv['invoice_date'], '%d/%m/%Y')
                
                if from_date:
                    from_dt = datetime.strptime(from_date, '%d/%m/%Y')
                    if invoice_date < from_dt:
                        continue
                
                if to_date:
                    to_dt = datetime.strptime(to_date, '%d/%m/%Y')
                    if invoice_date > to_dt:
                        continue
                
                filtered.append(inv)
            
            log_info(f"Filtered {len(filtered)} invoices from {len(invoices)} total", 'billing_app')
            return filtered
            
        except Exception as e:
            log_warning(f"Date filter failed: {e}", 'billing_app')
            return invoices
    
    def filter_invoices_by_contact(
        self,
        invoices: List[Dict[str, Any]],
        contact: str
    ) -> List[Dict[str, Any]]:
        """
        Filter invoices by customer contact number.
        
        Args:
            invoices: List of invoice dictionaries
            contact: Contact number to search for
            
        Returns:
            Filtered list of invoices
        """
        if not contact:
            return invoices
        
        contact = contact.strip()
        filtered = [inv for inv in invoices if contact in inv['customer_phone']]
        
        log_info(f"Contact filter returned {len(filtered)} invoices", 'billing_app')
        return filtered
    
    def get_cash_payments(self) -> List[Dict[str, Any]]:
        """
        Fetch all cash payments from payments_received table.
        
        Returns:
            List of payment records with invoice and customer details
        """
        try:
            all_payments = self.db.get_all_payments_received()
            
            # Filter for CASH payments only
            cash_payments = []
            for payment in all_payments:
                if payment.get('payment_mode', '').upper() == 'CASH':
                    # Enrich with invoice and customer details
                    invoice_id = payment.get('invoice_id')
                    if invoice_id:
                        try:
                            # Get invoice details
                            cur = self.db.conn.cursor()
                            cur.execute("""
                                SELECT i.invoice_number, i.invoice_date, i.total_amount,
                                       c.name as customer_name, c.phone as customer_phone
                                FROM invoices i
                                LEFT JOIN contacts c ON i.contact_id = c.id
                                WHERE i.id = ?
                            """, (invoice_id,))
                            inv_row = cur.fetchone()
                            
                            if inv_row:
                                # Convert date format
                                date_str = inv_row['invoice_date']
                                try:
                                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                                    formatted_date = date_obj.strftime('%d/%m/%Y')
                                except:
                                    formatted_date = date_str
                                
                                payment_date = payment.get('date', '')
                                try:
                                    date_obj = datetime.strptime(payment_date, '%Y-%m-%d')
                                    formatted_payment_date = date_obj.strftime('%d/%m/%Y')
                                except:
                                    formatted_payment_date = payment_date
                                
                                cash_payments.append({
                                    'date': formatted_payment_date,
                                    'invoice_number': inv_row['invoice_number'],
                                    'invoice_date': formatted_date,
                                    'customer_name': inv_row['customer_name'],
                                    'customer_phone': inv_row['customer_phone'],
                                    'amount': float(payment.get('amount', 0)),
                                    'total_amount': float(inv_row['total_amount']),
                                    'reference_number': payment.get('reference_number', ''),
                                    'notes': payment.get('notes', ''),
                                    'type': 'RECEIVED'  # Mark as received payment
                                })
                        except Exception as e:
                            log_warning(f"Error enriching payment {payment.get('id')}: {e}", 'billing_app')
                            continue
            
            log_info(f"Loaded {len(cash_payments)} cash payments received", 'billing_app')
            return cash_payments
            
        except Exception as e:
            log_error("Failed to load cash payments", exception=e, logger_name='billing_errors')
            return []
    
    def get_cash_supplier_payments(self) -> List[Dict[str, Any]]:
        """
        Fetch all CASH supplier payments from supplier_payments table.
        
        Returns:
            List of supplier payment records with supplier details
        """
        try:
            cur = self.db.conn.cursor()
            cur.execute("""
                SELECT sp.date, sp.amount, sp.payment_mode, sp.reference_number, sp.notes,
                       c.name as supplier_name, c.phone as supplier_phone
                FROM supplier_payments sp
                LEFT JOIN contacts c ON sp.supplier_id = c.id
                WHERE sp.payment_mode = 'CASH'
                ORDER BY sp.date DESC
            """)
            
            cash_supplier_payments = []
            for row in cur.fetchall():
                payment_date = row['date']
                try:
                    date_obj = datetime.strptime(payment_date, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%d/%m/%Y')
                except:
                    formatted_date = payment_date
                
                cash_supplier_payments.append({
                    'date': formatted_date,
                    'supplier_name': row['supplier_name'],
                    'supplier_phone': row['supplier_phone'],
                    'amount': float(row['amount']),
                    'reference_number': row['reference_number'] or '',
                    'notes': row['notes'] or '',
                    'type': 'PAID'  # Mark as payment made
                })
            
            log_info(f"Loaded {len(cash_supplier_payments)} cash supplier payments", 'billing_app')
            return cash_supplier_payments
            
        except Exception as e:
            log_error("Failed to load cash supplier payments", exception=e, logger_name='billing_errors')
            return []


if __name__ == "__main__":
    """
    Test script to verify all ReportsDBOperations methods are working correctly.
    Run this file directly to test database operations.
    """
    print("=" * 80)
    print("TESTING ReportsDBOperations - Database Operations for Reports")
    print("=" * 80)
    
    try:
        # Initialize the database operations
        print("\n[1] Initializing ReportsDBOperations...")
        db_ops = ReportsDBOperations()
        print("✓ ReportsDBOperations initialized successfully")
        
        # Test 1: Load all invoices
        print("\n[2] Testing load_all_invoices()...")
        invoices = db_ops.load_all_invoices()
        print(f"✓ Loaded {len(invoices)} invoices")
        if invoices:
            sample = invoices[0]
            print(f"   Sample Invoice: {sample['invoice_number']}")
            print(f"   Customer: {sample['customer_name']} ({sample['customer_phone']})")
            print(f"   Total: ₹{sample['total_amount']:,.2f}")
            print(f"   Paid: ₹{sample['paid_amount']:,.2f}")
            print(f"   Balance: ₹{sample['balance']:,.2f}")
            print(f"   Status: {sample['payment_status']}")
            print(f"   Tickets: {len(sample['tickets'])}")
            print(f"   Passengers: {len(sample['passengers'])}")
        else:
            print("   ⚠ No invoices found in database")
        
        # Test 2: Get all payments summary
        print("\n[3] Testing get_all_payments_summary()...")
        payment_summary = db_ops.get_all_payments_summary()
        print(f"✓ Payment Summary Retrieved:")
        print(f"   Total Cash Received: ₹{payment_summary['cash']:,.2f}")
        print(f"   Total Bank Received: ₹{payment_summary['bank']:,.2f}")
        print(f"   Grand Total: ₹{payment_summary['cash'] + payment_summary['bank']:,.2f}")
        
        # Test 3: Get cash payments
        print("\n[4] Testing get_cash_payments()...")
        cash_payments = db_ops.get_cash_payments()
        print(f"✓ Loaded {len(cash_payments)} cash payments (received)")
        if cash_payments:
            sample_payment = cash_payments[0]
            print(f"   Sample Payment:")
            print(f"   Date: {sample_payment['date']}")
            print(f"   Invoice: {sample_payment['invoice_number']}")
            print(f"   Customer: {sample_payment['customer_name']}")
            print(f"   Amount: ₹{sample_payment['amount']:,.2f}")
        else:
            print("   ⚠ No cash payments found")
        
        # Test 4: Get cash supplier payments
        print("\n[5] Testing get_cash_supplier_payments()...")
        supplier_payments = db_ops.get_cash_supplier_payments()
        print(f"✓ Loaded {len(supplier_payments)} cash supplier payments (paid)")
        if supplier_payments:
            sample_sp = supplier_payments[0]
            print(f"   Sample Supplier Payment:")
            print(f"   Date: {sample_sp['date']}")
            print(f"   Supplier: {sample_sp['supplier_name']}")
            print(f"   Amount: ₹{sample_sp['amount']:,.2f}")
        else:
            print("   ⚠ No supplier cash payments found")
        
        # Test 5: Calculate profit metrics
        if invoices:
            print("\n[6] Testing calculate_profit_metrics()...")
            profit_metrics = db_ops.calculate_profit_metrics(invoices)
            print(f"✓ Profit Metrics Calculated:")
            print(f"   Total Sales: ₹{profit_metrics['total_sale']:,.2f}")
            print(f"   Total Cost: ₹{profit_metrics['total_cost']:,.2f}")
            print(f"   Gross Profit: ₹{profit_metrics['gross_profit']:,.2f}")
            print(f"   Profit Margin: {profit_metrics['profit_margin']:.2f}%")
        
        # Test 6: Calculate balance report
        print("\n[7] Testing calculate_balance_report()...")
        balance_report = db_ops.calculate_balance_report()
        print(f"✓ Balance Report Generated for {len(balance_report)} customers")
        if balance_report:
            # Show top 3 customers with highest balances
            sorted_balances = sorted(balance_report, key=lambda x: x['balance'], reverse=True)
            print("   Top Customers with Outstanding Balance:")
            for i, customer in enumerate(sorted_balances[:3], 1):
                print(f"   {i}. {customer['customer_name']}")
                print(f"      Total Invoiced: ₹{customer['total']:,.2f}")
                print(f"      Received: ₹{customer['received']:,.2f}")
                print(f"      Balance: ₹{customer['balance']:,.2f}")
        
        # Test 7: Get supplier bills
        print("\n[8] Testing get_supplier_bills()...")
        supplier_bills = db_ops.get_supplier_bills()
        print(f"✓ Loaded {len(supplier_bills)} supplier bills")
        
        # Test 8: Get expenses
        print("\n[9] Testing get_expenses()...")
        expenses = db_ops.get_expenses()
        print(f"✓ Loaded {len(expenses)} expense records")
        
        # Test 9: Filter by date (if invoices exist)
        if invoices:
            print("\n[10] Testing filter_invoices_by_date()...")
            from_date = "01/01/2024"
            to_date = "31/12/2024"
            filtered = db_ops.filter_invoices_by_date(invoices, from_date, to_date)
            print(f"✓ Filtered invoices from {from_date} to {to_date}: {len(filtered)} records")
        
        # Test 10: Filter by contact (if invoices exist)
        if invoices and invoices[0]['customer_phone']:
            print("\n[11] Testing filter_invoices_by_contact()...")
            test_contact = invoices[0]['customer_phone'][:5]  # First 5 digits
            filtered = db_ops.filter_invoices_by_contact(invoices, test_contact)
            print(f"✓ Filtered by contact '{test_contact}': {len(filtered)} records")
        
        # Summary
        print("\n" + "=" * 80)
        print("DATABASE OPERATIONS TEST SUMMARY")
        print("=" * 80)
        print(f"Total Invoices in Database: {len(invoices)}")
        print(f"Total Cash Received: ₹{payment_summary['cash']:,.2f}")
        print(f"Total Bank Received: ₹{payment_summary['bank']:,.2f}")
        print(f"Cash Payments (Received): {len(cash_payments)}")
        print(f"Cash Payments (Paid to Suppliers): {len(supplier_payments)}")
        print(f"Customers with Balance: {len(balance_report)}")
        print(f"Supplier Bills: {len(supplier_bills)}")
        print(f"Expenses: {len(expenses)}")
        
        if invoices:
            total_tickets = sum(len(inv['tickets']) for inv in invoices)
            total_passengers = sum(len(inv['passengers']) for inv in invoices)
            print(f"Total Tickets/Items: {total_tickets}")
            print(f"Total Passengers: {total_passengers}")
        
        print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERROR DURING TESTING:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        print("\nFull Traceback:")
        traceback.print_exc()
        print("=" * 80)
