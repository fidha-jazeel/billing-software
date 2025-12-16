"""Test actual populate() methods to see where invoices are being filtered."""
from travel_billing_software.database.db_operations import ReportsDBOperations
from travel_billing_software.ui.reports.utils import ReportFilters
from travel_billing_software.database.db_manager import get_db_instance
from PyQt6.QtCore import QDate
from datetime import datetime

# Initialize database and operations
db = get_db_instance()
db_ops = ReportsDBOperations()

# Load all invoices
all_invoices = db_ops.load_all_invoices()
print(f"Total invoices loaded: {len(all_invoices)}")

# Filter to Dec 9-10
dec_invoices = [inv for inv in all_invoices if inv.get('invoice_date', '').startswith(('09/12/2025', '10/12/2025'))]
print(f"Invoices for Dec 9-10 before filtering: {len(dec_invoices)}")

# Create a mock filters object with default values
class MockFilters:
    def __init__(self):
        # Simulate default filter state (1900 to 2125)
        self.from_date = datetime(1900, 1, 1).date()
        self.to_date = datetime(2125, 1, 1).date()
    
    def apply_filters(self, invoices):
        """Simulate filter application"""
        filtered = []
        for invoice in invoices:
            try:
                date_str = invoice.get('invoice_date', '')
                if date_str:
                    # Parse dd/MM/yyyy format
                    parts = date_str.split('/')
                    day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                    invoice_date = datetime(year, month, day).date()
                    
                    if self.from_date <= invoice_date <= self.to_date:
                        filtered.append(invoice)
            except Exception as e:
                print(f"Error filtering invoice {invoice.get('invoice_number')}: {e}")
                continue
        return filtered

mock_filters = MockFilters()
filtered_invoices = mock_filters.apply_filters(all_invoices)

print(f"\nAfter applying default filters (1900-2125): {len(filtered_invoices)}")

# Count Dec 9-10 after filter
dec_after_filter = [inv for inv in filtered_invoices if inv.get('invoice_date', '').startswith(('09/12/2025', '10/12/2025'))]
print(f"Dec 9-10 invoices after filter: {len(dec_after_filter)}")

print("\nInvoice numbers in filtered result:")
for inv in sorted(dec_after_filter, key=lambda x: x.get('invoice_number', '')):
    print(f"  {inv['invoice_number']} - {inv['invoice_date']}")

# Now test if there's any uniqueness check happening
print("\n" + "="*80)
print("Checking for duplicate invoice_numbers (shouldn't be any):")
invoice_numbers = [inv['invoice_number'] for inv in filtered_invoices]
unique_numbers = set(invoice_numbers)
print(f"Total invoices: {len(invoice_numbers)}, Unique: {len(unique_numbers)}")
if len(invoice_numbers) != len(unique_numbers):
    print("WARNING: Duplicate invoice numbers found!")
else:
    print("✓ All invoice numbers are unique")

# Check for duplicate dates
from collections import defaultdict
dates_map = defaultdict(list)
for inv in filtered_invoices:
    date = inv.get('invoice_date', '')
    dates_map[date].append(inv['invoice_number'])

print(f"\nDates with multiple invoices:")
for date, invs in sorted(dates_map.items()):
    if len(invs) > 1:
        print(f"  {date}: {len(invs)} invoices - {', '.join(invs[:3])}...")
