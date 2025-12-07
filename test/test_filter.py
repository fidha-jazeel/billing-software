from travel_billing_software.ui.reports.db_operations import ReportsDBOperations
from travel_billing_software.ui.reports.utils import ReportFilters
from travel_billing_software.config.config import COLORS
from travel_billing_software.utils.styles import get_button_style

# Load data
db = ReportsDBOperations()
all_invoices = db.load_all_invoices()

print(f"Loaded {len(all_invoices)} invoices from database")

# Create filter instance
filters = ReportFilters(COLORS, get_button_style)

# Apply filters
filtered_invoices = filters.apply_filters(all_invoices)

print(f"\nAfter filtering: {len(filtered_invoices)} invoices")
print(f"Filtered out: {len(all_invoices) - len(filtered_invoices)} invoices")

if len(filtered_invoices) < len(all_invoices):
    print("\n=== Invoices that were FILTERED OUT ===")
    filtered_ids = {inv.get('invoice_number') for inv in filtered_invoices}
    for inv in all_invoices:
        if inv.get('invoice_number') not in filtered_ids:
            print(f"  - {inv.get('invoice_number')}: Date={inv.get('date')}, Tickets={len(inv.get('tickets', []))}")

print("\n=== Invoices that PASSED the filter ===")
for inv in filtered_invoices:
    print(f"  - {inv.get('invoice_number')}: Date={inv.get('date')}, Tickets={len(inv.get('tickets', []))}")
