from travel_billing_software.ui.reports.db_operations import ReportsDBOperations
import json

db = ReportsDBOperations()
invoices = db.load_all_invoices()

print(f"Total invoices: {len(invoices)}")
print(f"=" * 80)

total_items = 0
service_types = {}

for idx, inv in enumerate(invoices, 1):
    items = inv.get('tickets', [])  # Named 'tickets' but contains all service types
    total_items += len(items)
    
    for item in items:
        service_type = item.get('booking_type', 'Unknown')
        service_types[service_type] = service_types.get(service_type, 0) + 1

print(f"\n=== Service Types Breakdown ===")
for stype, count in sorted(service_types.items()):
    print(f"  {stype}: {count} items")

print(f"\n{'=' * 80}")
print(f"Summary: {len(invoices)} invoices with {total_items} total items")
print(f"Service types found: {len(service_types)}")


