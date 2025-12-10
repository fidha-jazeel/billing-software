"""Quick verification that the Purchase Report imports correctly."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing Purchase Report import...")

try:
    from travel_billing_software.ui.reports.sub_pages.purchase_report import PurchaseReportView
    print("✓ PurchaseReportView imported successfully")
    print("✓ No syntax errors detected")
    print("\n✅ SUCCESS: The application should start now!")
    sys.exit(0)
except SyntaxError as e:
    print(f"✗ SYNTAX ERROR: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ IMPORT ERROR: {e}")
    sys.exit(1)
