"""Test invoice display to diagnose the single invoice per day issue."""
import sqlite3

conn = sqlite3.connect('travel_billing_software/billing.db')
cur = conn.cursor()

# Check invoices for dates with multiple entries
cur.execute('''
    SELECT i.invoice_number, DATE(i.date) as dt, c.name, COUNT(it.id) as items
    FROM invoices i
    LEFT JOIN contacts c ON i.contact_id = c.id
    LEFT JOIN invoice_items it ON i.id = it.invoice_id
    WHERE DATE(i.date) IN ("2025-12-09", "2025-12-10")
    GROUP BY i.id
    ORDER BY i.date DESC, i.invoice_number
''')

print("\nInvoices on Dec 9-10, 2025:")
print("=" * 80)
print(f"{'Invoice#':<25} {'Date':<12} {'Customer':<20} {'Items':>5}")
print("=" * 80)

results = cur.fetchall()
for r in results:
    print(f"{r[0]:<25} {r[1]:<12} {r[2]:<20} {r[3]:>5}")

print(f"\nTotal invoices: {len(results)}")

# Now test what the application would receive
print("\n" + "=" * 80)
print("Testing application data flow:")
print("=" * 80)

from travel_billing_software.ui.reports.db_operations import ReportsDBOperations

db_ops = ReportsDBOperations()
all_invoices = db_ops.load_all_invoices()

print(f"\nTotal invoices loaded by ReportsDBOperations: {len(all_invoices)}")

# Filter to Dec 9-10
dec_invoices = [inv for inv in all_invoices if inv.get('invoice_date', '').startswith(('09/12/2025', '10/12/2025'))]

print(f"Invoices for Dec 9-10: {len(dec_invoices)}")
print("\nInvoice numbers:")
for inv in sorted(dec_invoices, key=lambda x: x.get('invoice_number', '')):
    print(f"  {inv['invoice_number']} - {inv['invoice_date']} - {inv['customer_name']} - {len(inv.get('tickets', []))} tickets")

conn.close()
