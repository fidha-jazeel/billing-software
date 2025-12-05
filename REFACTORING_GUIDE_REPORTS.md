# Reports Module Refactoring Guide

## 📁 Folder Structure (COMPLETED)
```
travel_billing_software/ui/reports/
├── __init__.py                    ✅ CREATED
├── db_operations.py               ✅ CREATED (371 lines)
├── utils.py                       ✅ CREATED (705 lines)
├── reports_page.py                ⏳ TEMPLATE BELOW
└── sub_pages/
    ├── __init__.py                ✅ CREATED
    ├── sale_report.py             ✅ CREATED (285 lines)
    ├── purchase_report.py         📝 TODO - Template below
    ├── all_transactions.py        📝 TODO - Template below
    ├── day_book.py                📝 TODO - Template below
    ├── profit_loss.py             📝 TODO - Template below
    ├── bill_wise_profit.py        📝 TODO - Template below
    ├── cash_transactions.py       📝 TODO - Template below
    └── balance_report.py          📝 TODO - Template below
```

---

## 🎯 Function Mapping: Original → New Files

### **db_operations.py** ✅ (Already Created)
Contains all database queries and data transformations:
- `ReportsDBOperations` class
  - `load_all_invoices()` → from line 454-530
  - `get_all_payments_summary()` → from line 424-453
  - `get_supplier_bills()` → fetch supplier data
  - `get_expenses()` → fetch expense data
  - `calculate_balance_report()` → customer balances
  - `calculate_profit_metrics()` → profit calculations
  - `filter_invoices_by_date()` → date filtering
  - `filter_invoices_by_contact()` → contact filtering

### **utils.py** ✅ (Already Created)
Contains all shared utilities:
- `TableConfigurator` class
  - `configure_table()` → from line 58-105
- `ReportFilters` class
  - `create_filter_section()` → from line 540-920
  - `apply_filters()` → from line 950-1040
  - `clear_filters()` → from line 918-940
- `ReportExporter` class
  - `export_to_csv()` → from line 2106-2148
- `SummaryCardManager` class
  - `create_summary_cards()` → create metric cards
  - `update_summary_cards()` → from line 2096-2105
- Helper functions:
  - `create_report_header()` → from line 1046-1085
  - `show_no_records_message()` → from line 1037-1045

---

## 📋 Sub-Page Template Pattern

Each sub-page follows this structure:

### **File Structure:**
```python
"""
[Report Name] Sub-Page
[Brief description of what this report shows]
"""
from typing import List, Dict, Any
from PyQt6.QtWidgets import (...)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor
from travel_billing_software.utils.logger import log_info, log_error, log_warning
from ..utils import (
    TableConfigurator, ReportExporter, SummaryCardManager,
    create_report_header, show_no_records_message
)

class [ReportName]View(QWidget):
    """[Docstring describing the report]"""
    
    def __init__(self, colors, get_button_style, export_callback):
        super().__init__()
        self.colors = colors
        self.get_button_style = get_button_style
        self.export_callback = export_callback
        self._init_ui()
        log_info("[ReportName]View initialized", 'billing_app')
    
    def _init_ui(self):
        """Create UI layout with header, filters placeholder, summary, table"""
        # 1. Create scroll area
        # 2. Add header with create_report_header()
        # 3. Add filters_placeholder (to be replaced by parent)
        # 4. Add summary cards with SummaryCardManager
        # 5. Add export buttons
        # 6. Create table with proper columns
        # 7. Configure table with TableConfigurator
    
    def set_filters_widget(self, filters_widget):
        """Replace placeholder with actual filters from parent"""
    
    def populate(self, invoices):
        """Populate table with filtered invoice data"""
        # 1. Clear table
        # 2. Check if empty → show_no_records_message()
        # 3. Loop through invoices and add rows
        # 4. Update summary cards with totals
        # 5. Log success
    
    def get_table_widget(self):
        """Return table for export operations"""
        return self.[table_name]
```

---

## 📝 TODO: Create These 7 Sub-Pages

### 1. **purchase_report.py** (Lines 1316-1440)
**Purpose:** Show supplier purchases and costs

**Table Columns:** Passenger, Supplier, Sector, PNR, Qty, Supplier Amount

**Key Logic:**
```python
# From _populate_purchase_report() line 1395-1440
# Loop through invoices → loop through tickets
# Extract: passenger_name, supplier_name, sector, pnr, quantity, supplier_amount
# Summary: Total Purchases, Total Items, Avg Cost
```

**Original Functions:**
- `_create_purchase_report_view()` → line 1316-1393
- `_populate_purchase_report()` → line 1395-1440

---

### 2. **all_transactions.py** (Lines 1442-1590)
**Purpose:** Show all invoice items/transactions

**Table Columns:** Invoice #, Date, Customer, Contact, Passenger, Type, Total, Status

**Key Logic:**
```python
# From _populate_all_transactions() line 1523-1590
# Loop through invoices → loop through tickets
# Extract: invoice_number, date, customer, passenger, booking_type, total
# Calculate payment status from balance
# Summary: Total Transactions, Total Value, Avg Transaction
```

**Original Functions:**
- `_create_all_transactions_view()` → line 1442-1521
- `_populate_all_transactions()` → line 1523-1590

---

### 3. **day_book.py** (Lines 1591-1745)
**Purpose:** Daily summary of sales, purchases, profit

**Table Columns:** Date, Invoices, Sales, Purchases, Profit

**Key Logic:**
```python
# From _populate_day_book() line 1668-1745
# Group invoices by date
# For each date: count invoices, sum sales, sum purchases
# Calculate profit = sales - purchases
# Summary: Daily Sales, Daily Purchases, Net Profit
```

**Original Functions:**
- `_create_day_book_view()` → line 1591-1667
- `_populate_day_book()` → line 1668-1745

---

### 4. **profit_loss.py** (Lines 1747-1889)
**Purpose:** Overall profit/loss statement

**Table Columns:** Invoice #, Date, Customer, Sales, Cost, Profit, Margin %

**Key Logic:**
```python
# From _populate_profit_loss() line 1823-1889
# Loop through invoices
# For each: calculate sales (total_amount), cost (sum of supplier_amounts), profit
# Calculate margin percentage = (profit / sales) * 100
# Summary: Total Sales, Total Cost, Gross Profit
```

**Original Functions:**
- `_create_profit_loss_view()` → line 1747-1821
- `_populate_profit_loss()` → line 1823-1889

---

### 5. **bill_wise_profit.py** (Lines 1891-2146)
**Purpose:** Detailed profit breakdown per invoice item

**Table Columns:** Invoice #, Date, Passenger, Supplier, PNR, Sector, Booking Type, Qty, Sale Price, Cost Price, Profit, Margin %

**Key Logic:**
```python
# From _populate_bill_wise_profit() line 2006-2146
# Loop through invoices → loop through tickets
# For each ticket:
#   - sale_price = total_amount / quantity
#   - cost_price = supplier_amount
#   - profit = sale_price - cost_price
#   - margin = (profit / sale_price) * 100
# Color code: green if profit > 0, red if < 0
# Summary: Total Sale, Total Cost, Total Profit
```

**Original Functions:**
- `_create_bill_wise_profit_view()` → line 1891-2004
- `_populate_bill_wise_profit()` → line 2006-2146

---

### 6. **cash_transactions.py** (Lines 2148-2315)
**Purpose:** Track cash payments and receipts

**Table Columns:** Date, Invoice #, Customer (Payer), Contact, Cash Received, Cash Paid, Balance, Status

**Key Logic:**
```python
# From _populate_cash_transactions() line 2228-2315
# Loop through invoices where payment_mode == 'CASH'
# Extract: date, invoice_number, customer, contact, paid_amount
# Calculate balance = total - paid
# Status: ✅ Paid, 🟡 Partial, 🔴 Unpaid
# Summary: Total Cash Received, Total Cash Paid, Net Cash Flow
```

**Original Functions:**
- `_create_cash_transactions_view()` → line 2148-2227
- `_populate_cash_transactions()` → line 2228-2315

---

### 7. **balance_report.py** (Lines 2317-2533)
**Purpose:** Customer-wise outstanding balances

**Table Columns:** Customer, Contact, Total Invoiced, Received, Balance Due, % Paid, Status, Last Invoice Date

**Key Logic:**
```python
# From _populate_balance_report() line 2409-2533
# Use db_operations.calculate_balance_report() to get customer totals
# For each customer:
#   - Group by contact number
#   - Sum total_amount, paid_amount, balance
#   - Calculate % paid = (received / total) * 100
#   - Status: ✅ Fully Paid (balance=0), 🟡 Partial (received>0), 🔴 Unpaid
# Summary: Total Balance Due, Total Received, Total Invoiced
```

**Original Functions:**
- `_create_balance_report_view()` → line 2317-2407
- `_populate_balance_report()` → line 2409-2533

---

## 🏗️ Main Orchestrator: reports_page.py

This file replaces the original `ReportsPage` class and coordinates all sub-pages.

### **Structure:**
```python
"""
Reports Page - Main Orchestrator
Vyapar-style reports with sidebar navigation.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QListWidget, QStackedWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from travel_billing_software.utils.logger import log_info, log_error

from .db_operations import ReportsDBOperations
from .utils import ReportFilters, ReportExporter
from .sub_pages import (
    SaleReportView, PurchaseReportView, AllTransactionsView,
    DayBookView, ProfitLossView, BillWiseProfitView,
    CashTransactionsView, BalanceReportView
)

class ReportsPage(QWidget):
    """Main reports page with sidebar and stacked sub-pages."""
    
    def __init__(self, colors, invoice_config, app_config, 
                 get_table_style, get_button_style, get_input_style,
                 get_label_style, dashboard_ref):
        super().__init__()
        # Store parameters
        # Initialize db_operations = ReportsDBOperations()
        # Initialize filters = ReportFilters(colors, get_button_style)
        # self.all_invoices = []
        self._init_ui()
    
    def _init_ui(self):
        # Create horizontal layout
        # Left: _create_sidebar() with report categories
        # Right: _create_content_stack() with all sub-page views
    
    def _create_sidebar(self):
        # Create QListWidget with 8 items:
        # 1. Sale Report
        # 2. Purchase Report
        # 3. All Transactions
        # 4. Day Book
        # 5. Profit & Loss
        # 6. Bill Wise Profit
        # 7. Cash Transactions
        # 8. Balance Report
        # Connect to _on_report_selected()
    
    def _create_content_stack(self):
        # Create QStackedWidget
        # Instantiate all 8 sub-page views
        # For each view:
        #   - Call view.set_filters_widget(filters.create_filter_section(...))
        #   - Call view.set_payment_summary_widget(payment_summary) [for sale report]
        #   - Add to stack
    
    def _create_payment_summary_section(self):
        # From line 344-422 - Cash/Bank summary boxes
        # Returns QFrame with lbl_total_cash and lbl_total_bank
    
    def _on_report_selected(self, index):
        # Switch to selected report
        # Refresh that report's data
    
    def _refresh_current_report(self, index):
        # Load invoices from db_operations
        # Apply filters
        # Call appropriate sub-page's populate() method
    
    def _handle_filter_change(self):
        # Get current report index
        # Reload and refresh
    
    def _clear_filters(self):
        # Call filters.clear_filters()
        # Show confirmation
        # Refresh current report
    
    def _export_report(self, report_type, format):
        # Get current view's table
        # Use ReportExporter.export_to_csv()
    
    def _update_payment_summary(self):
        # Call db_operations.get_all_payments_summary()
        # Update lbl_total_cash and lbl_total_bank labels
```

**Key Mappings:**
- Lines 150-268 → `_init_ui()`, `_create_sidebar()`
- Lines 266-303 → `_create_content_stack()` (creates all 8 views)
- Lines 344-422 → `_create_payment_summary_section()`
- Lines 304-340 → `_on_report_selected()`, `_refresh_current_report()`
- Lines 920-943 → `_handle_filter_change()`, `_clear_filters()`
- Lines 2106-2148 → `_export_report()` (delegates to ReportExporter)
- Lines 424-453 → `_update_payment_summary()`

---

## ✅ Quick Checklist

When creating each sub-page:
- [ ] Copy the template pattern from `sale_report.py`
- [ ] Update class name (e.g., `PurchaseReportView`)
- [ ] Update emoji and title in header
- [ ] Define correct table columns
- [ ] Map original `_populate_*` logic to `populate()` method
- [ ] Update summary card titles
- [ ] Test table column count matches headers
- [ ] Add comprehensive logging
- [ ] Include proper exception handling

---

## 🚀 Testing Steps

After creating all files:
1. Backup original: `reports.py` → `reports.py.old`
2. Check imports work: `python -c "from travel_billing_software.ui.reports import ReportsPage"`
3. Run application: `python -m travel_billing_software.main`
4. Navigate to each report and verify:
   - Data loads correctly
   - Filters work
   - Export works
   - No crashes

---

## 💡 Pro Tips

1. **Use sale_report.py as your template** - It has the complete pattern
2. **Column count must match headers** - Common error source
3. **Handle missing data gracefully** - Use `.get('key', default)`
4. **Log everything** - Makes debugging easier
5. **Test incrementally** - Create 2-3 files, test, then continue

---

## 📞 Need Help?

If you get stuck on any file, check:
1. Original function in `reports.py` (line numbers above)
2. `sale_report.py` for reference pattern
3. Ensure imports match the template
4. Verify table column indices match data assignment

Good luck! 🎉
