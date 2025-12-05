"""
Database Operations Module for Home Page
Handles all database interactions for invoice and passenger data.
Separated from UI logic for better maintainability and testing.
"""
from typing import Dict, List, Optional, Any
from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.utils.logger import log_info, log_error, log_warning


class InvoiceDBOperations:
    """Handles database operations for invoices and passenger data."""
    
    def __init__(self):
        """Initialize database connection."""
        try:
            self.db = get_db_instance()
            log_info("Invoice DB operations initialized", "home_db")
        except Exception as e:
            log_error("Failed to initialize database connection", exception=e, logger_name="home_db_errors")
            raise
    
    def save_invoice(self, invoice_data: Dict[str, Any]) -> int:
        """
        Save invoice to database.
        
        Args:
            invoice_data: Dictionary containing invoice details and items
            
        Returns:
            int: Invoice ID if successful, -1 if failed
            
        Raises:
            ValueError: If invoice_data is invalid or missing required fields
        """
        try:
            # Validate invoice data
            self._validate_invoice_data(invoice_data)
            
            # Log invoice save attempt
            log_info(
                f"Saving invoice: {invoice_data['invoice_number']}, "
                f"customer: {invoice_data['customer_name']}, "
                f"items: {len(invoice_data['items'])}, "
                f"total: {invoice_data['grand_total']}",
                "home_db"
            )
            
            # Save to database
            invoice_id = self.db.save_invoice(invoice_data)
            
            if invoice_id > 0:
                log_info(
                    f"Invoice saved successfully: {invoice_data['invoice_number']}, "
                    f"ID: {invoice_id}",
                    "home_db"
                )
                return invoice_id
            else:
                log_error(
                    f"Invoice save failed (returned ID <= 0): {invoice_data['invoice_number']}",
                    logger_name="home_db_errors"
                )
                return -1
                
        except ValueError as e:
            log_error(
                f"Invalid invoice data: {invoice_data.get('invoice_number', 'UNKNOWN')}",
                exception=e,
                logger_name="home_db_errors"
            )
            raise
        except Exception as e:
            log_error(
                f"Unexpected error saving invoice: {invoice_data.get('invoice_number', 'UNKNOWN')}",
                exception=e,
                logger_name="home_db_errors"
            )
            return -1
    
    def _validate_invoice_data(self, invoice_data: Dict[str, Any]) -> None:
        """
        Validate invoice data before saving.
        
        Args:
            invoice_data: Invoice data dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = [
            'invoice_number', 'invoice_date', 'customer_name',
            'items', 'grand_total'
        ]
        
        for field in required_fields:
            if field not in invoice_data:
                raise ValueError(f"Missing required field: {field}")
        
        if not invoice_data['items']:
            raise ValueError("Invoice must have at least one item")
        
        # Validate item structure
        for idx, item in enumerate(invoice_data['items']):
            if 'passenger_name' not in item or not item['passenger_name'].strip():
                raise ValueError(f"Item {idx + 1}: passenger_name is required")
            if 'selling_price' not in item:
                raise ValueError(f"Item {idx + 1}: selling_price is required")
    
    def load_passenger_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load passenger history from all invoices.
        Groups passengers by contact number for auto-completion.
        
        Returns:
            Dict mapping contact numbers to list of passenger data
        """
        try:
            log_info("Loading passenger history from database", "home_db")
            
            passenger_history = {}
            invoices = self.db.get_all_invoices()
            
            for invoice in invoices:
                try:
                    contact = invoice.get("customer_phone", "").strip()
                    if not contact:
                        continue
                    
                    # Initialize contact entry
                    if contact not in passenger_history:
                        passenger_history[contact] = []
                    
                    # Get invoice items
                    items = self.db.get_invoice_items(invoice['id'])
                    
                    for item in items:
                        passenger_data = {
                            "passenger_name": item.get("passenger_name", ""),
                            "pnr": item.get("pnr", ""),
                            "sector": item.get("sector", ""),
                            "supplier": item.get("supplier", ""),
                            "passport_number": item.get("passport_number", ""),
                            "qty": item.get("qty", 1),
                            "supplier_amount": item.get("cost_price", 0),
                            "amount": item.get("selling_price", 0),
                            "passport_details": item.get("passport_details", None)
                        }
                        
                        # Avoid duplicates
                        if passenger_data not in passenger_history[contact]:
                            passenger_history[contact].append(passenger_data)
                
                except Exception as e:
                    log_warning(
                        f"Error processing invoice {invoice.get('id', 'UNKNOWN')} for history",
                        exception=e,
                        logger_name="home_db"
                    )
                    continue
            
            log_info(
                f"Loaded passenger history for {len(passenger_history)} contacts, "
                f"total passengers: {sum(len(v) for v in passenger_history.values())}",
                "home_db"
            )
            
            return passenger_history
            
        except Exception as e:
            log_error(
                "Failed to load passenger history",
                exception=e,
                logger_name="home_db_errors"
            )
            return {}
    
    def update_passenger_history(
        self,
        contact: str,
        passengers: List[Dict[str, Any]],
        existing_history: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Update passenger history with new invoice data.
        
        Args:
            contact: Customer contact number
            passengers: List of passenger data from new invoice
            existing_history: Current passenger history dictionary
            
        Returns:
            Updated passenger history dictionary
        """
        try:
            if not contact or not contact.strip():
                log_warning("Cannot update history: empty contact number", logger_name="home_db")
                return existing_history
            
            contact = contact.strip()
            
            # Initialize if new contact
            if contact not in existing_history:
                existing_history[contact] = []
            
            # Add new passengers (avoid duplicates)
            added_count = 0
            for passenger in passengers:
                if passenger not in existing_history[contact]:
                    existing_history[contact].append(passenger)
                    added_count += 1
            
            log_info(
                f"Updated passenger history for {contact}: "
                f"added {added_count} new passengers, "
                f"total: {len(existing_history[contact])}",
                "home_db"
            )
            
            return existing_history
            
        except Exception as e:
            log_error(
                f"Error updating passenger history for contact {contact}",
                exception=e,
                logger_name="home_db_errors"
            )
            return existing_history
    
    def get_all_invoices(self) -> List[Dict[str, Any]]:
        """
        Retrieve all invoices from database.
        
        Returns:
            List of invoice dictionaries
        """
        try:
            invoices = self.db.get_all_invoices()
            log_info(f"Retrieved {len(invoices)} invoices from database", "home_db")
            return invoices
        except Exception as e:
            log_error("Failed to retrieve invoices", exception=e, logger_name="home_db_errors")
            return []
    
    def get_invoice_by_number(self, invoice_number: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve invoice by invoice number.
        
        Args:
            invoice_number: Invoice number to search for
            
        Returns:
            Invoice dictionary if found, None otherwise
        """
        try:
            invoice = self.db.get_invoice_by_number(invoice_number)
            if invoice:
                log_info(f"Retrieved invoice: {invoice_number}", "home_db")
            else:
                log_warning(f"Invoice not found: {invoice_number}", logger_name="home_db")
            return invoice
        except Exception as e:
            log_error(
                f"Error retrieving invoice {invoice_number}",
                exception=e,
                logger_name="home_db_errors"
            )
            return None
    
    def check_duplicate_invoice_number(self, invoice_number: str) -> bool:
        """
        Check if invoice number already exists.
        
        Args:
            invoice_number: Invoice number to check
            
        Returns:
            True if invoice number exists, False otherwise
        """
        try:
            invoice = self.get_invoice_by_number(invoice_number)
            return invoice is not None
        except Exception as e:
            log_error(
                f"Error checking duplicate invoice {invoice_number}",
                exception=e,
                logger_name="home_db_errors"
            )
            return False
