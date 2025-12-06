"""Quick test to check invoice dates and filtering"""
from travel_billing_software.ui.reports.db_operations import ReportsDBOperations
from travel_billing_software.ui.reports.utils import ReportFilters
from datetime import datetime

# Initialize
db = ReportsDBOperations()

# Load invoices
print("=" * 80)
print("TESTING INVOICE LOADING AND FILTERING")
print("=" * 80)

invoices = db.load_all_invoices()
print(f"\n1. Loaded {len(invoices)} invoices from database")

if invoices:
    print("\nSample invoice dates (first 5):")
    for i, inv in enumerate(invoices[:5], 1):
        print(f"   {i}. {inv['invoice_number']}: date='{inv['invoice_date']}'")

# Test filter with default date range (last month to today)
print("\n" + "=" * 80)
print("TESTING FILTER WITH DEFAULT DATE RANGE")
print("=" * 80)

from PyQt6.QtCore import QDate

# Simulate default filter dates
from_date = QDate.currentDate().addMonths(-1)
to_date = QDate.currentDate()

print(f"\nDefault filter range:")
print(f"  From: {from_date.toString('dd/MM/yyyy')}")
print(f"  To: {to_date.toString('dd/MM/yyyy')}")

# Test date parsing
print("\n" + "=" * 80)
print("CHECKING DATE PARSING")
print("=" * 80)

for inv in invoices[:3]:
    date_str = inv['invoice_date']
    print(f"\nInvoice: {inv['invoice_number']}")
    print(f"  Date string: '{date_str}'")
    
    if date_str:
        try:
            # Try parsing as DD/MM/YYYY
            dt = datetime.strptime(date_str, '%d/%m/%Y')
            print(f"  ✓ Parsed as DD/MM/YYYY: {dt.date()}")
            
            # Check if in range
            from_dt = datetime(from_date.year(), from_date.month(), from_date.day()).date()
            to_dt = datetime(to_date.year(), to_date.month(), to_date.day()).date()
            in_range = from_dt <= dt.date() <= to_dt
            print(f"  In range [{from_dt} to {to_dt}]: {in_range}")
        except ValueError as e:
            print(f"  ✗ Parse error: {e}")
    else:
        print(f"  ✗ Empty date string!")

print("\n" + "=" * 80)
