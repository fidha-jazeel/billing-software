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
        Load all invoices with their items from database.
        
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
                invoice_dict = self._format_invoice_record(inv)
                
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
                    
                    # Add ticket/item info
                    invoice_dict['tickets'].append({
                        'pnr': item.get('pnr_number', ''),
                        'supplier_name': item.get('supplier_name', ''),
                        'sector': item.get('sector', ''),
                        'booking_type': item.get('service_type_name', ''),
                        'quantity': int(item.get('quantity', 1)),
                        'supplier_amount': float(item.get('cost_price', 0)),
                        'total_amount': float(item.get('total_amount', 0)),
                        'passport_number': item.get('passport_number', '')
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
                elif payment_mode in ['BANK_TRANSFER', 'UPI', 'CARD', 'CHEQUE', 'ONLINE']:
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
