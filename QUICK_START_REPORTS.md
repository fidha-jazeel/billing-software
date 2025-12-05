# Reports Refactoring - Quick Start Guide

## ✅ What's Already Done

1. **Folder structure created** ✓
2. **Core utilities created** ✓
   - `db_operations.py` (371 lines) - All database queries
   - `utils.py` (705 lines) - Table config, filters, export, summary cards
3. **Module init files created** ✓
4. **One complete example** ✓
   - `sale_report.py` (285 lines) - Fully implemented, use as template!
5. **One semi-complete file** ✓
   - `purchase_report.py` - ~90% done, just needs `populate()` method filled

## 📝 What You Need To Do

Complete these 7 files (templates provided with TODO comments):

### Priority Order:

1. **purchase_report.py** ⭐ EASIEST - already 90% done
   - Just fill in the `populate()` method
   - Copy pattern from `sale_report.py`
   - 6 table columns

2. **all_transactions.py** ⭐ EASY
   - Very similar to `purchase_report.py`
   - 8 table columns
   - Loop invoices → loop tickets

3. **profit_loss.py** ⭐⭐ MEDIUM
   - 7 columns
   - Need to calculate: profit = sales - costs
   - One row per invoice

4. **day_book.py** ⭐⭐ MEDIUM
   - 5 columns
   - Special: Group by DATE (use dictionary)
   - See template for grouping logic

5. **cash_transactions.py** ⭐⭐ MEDIUM  
   - 8 columns
   - May need to filter by payment_mode

6. **balance_report.py** ⭐⭐⭐ HARDER
   - 8 columns
   - Group by CUSTOMER (use dictionary)
   - Calculate totals per customer

7. **bill_wise_profit.py** ⭐⭐⭐ HARDEST
   - 12 columns! Most detailed
   - Item-level profit calculations

8. **reports_page.py** ⭐⭐⭐⭐ MAIN ORCHESTRATOR
   - Coordinate all 8 sub-pages
   - Create sidebar with navigation
   - Handle filter changes
   - Detailed TODOs provided in file

## 🎯 Step-by-Step for Each Sub-Page

### Template Pattern (same for all 7 sub-pages):

```python
# 1. Copy the __init__ method (already done in templates)
def __init__(self, colors, get_button_style, export_callback):
    super().__init__()
    self.colors = colors
    self.get_button_style = get_button_style
    self.export_callback = export_callback
    self._init_ui()

# 2. Complete _init_ui (mostly done, just update specifics):
def _init_ui(self):
    # Create scroll + layout (DONE)
    # Add header with correct emoji & title (UPDATE)
    # Add filters placeholder (DONE)
    # Create summary cards with correct titles (UPDATE)
    # Add export buttons (DONE)
    # Create table with correct columns (UPDATE)
    # Configure table (UPDATE column widths)

# 3. Copy set_filters_widget (already done in templates)

# 4. Implement populate() - THE MAIN WORK
def populate(self, invoices):
    # Clear table
    # Check if empty
    # Loop and populate
    # Update summary
    # Log success
```

## 🔍 Finding Original Code

Use this mapping to find original logic:

| Sub-Page | Original Lines | Key Function |
|----------|---------------|--------------|
| Sale Report | 1088-1315 | `_populate_sale_report()` |
| Purchase | 1316-1440 | `_populate_purchase_report()` |
| All Transactions | 1442-1590 | `_populate_all_transactions()` |
| Day Book | 1591-1745 | `_populate_day_book()` |
| Profit & Loss | 1747-1889 | `_populate_profit_loss()` |
| Bill Wise Profit | 1891-2146 | `_populate_bill_wise_profit()` |
| Cash Transactions | 2148-2315 | `_populate_cash_transactions()` |
| Balance Report | 2317-2533 | `_populate_balance_report()` |

## 💡 Tips

### For `populate()` methods:
1. Start by copying structure from `sale_report.py` line 189-277
2. Update variable names (e.g., `self.sale_table` → `self.purchase_table`)
3. Change column count and data extraction
4. Test with `print()` statements first
5. Add error handling last

### Common Patterns:

**Pattern A: Loop Invoices**
```python
for invoice in invoices:
    row = self.table.rowCount()
    self.table.insertRow(row)
    # Add invoice-level data
    self.table.setItem(row, 0, QTableWidgetItem(invoice['invoice_number']))
```

**Pattern B: Loop Invoices → Loop Tickets**
```python
for invoice in invoices:
    for ticket in invoice.get('tickets', []):
        row = self.table.rowCount()
        self.table.insertRow(row)
        # Add ticket-level data
```

**Pattern C: Group by Key (Date/Customer)**
```python
grouped = {}
for invoice in invoices:
    key = invoice['invoice_date']  # or customer_phone
    if key not in grouped:
        grouped[key] = {'total': 0, 'count': 0}
    grouped[key]['total'] += invoice['total_amount']
    grouped[key]['count'] += 1

for key, data in grouped.items():
    # Add one row per group
```

## 🧪 Testing Strategy

1. **Test incrementally:**
   ```bash
   # After completing purchase_report.py:
   python -c "from travel_billing_software.ui.reports.sub_pages import PurchaseReportView; print('✓ Import works')"
   ```

2. **Test imports for all sub-pages:**
   ```bash
   python -c "from travel_billing_software.ui.reports.sub_pages import *; print('✓ All imports work')"
   ```

3. **Test main reports page:**
   ```bash
   python -c "from travel_billing_software.ui.reports import ReportsPage; print('✓ ReportsPage imports')"
   ```

4. **Test full app:**
   ```bash
   python -m travel_billing_software.main
   ```

## 🆘 If You Get Stuck

### Error: "No module named..."
- Check `__init__.py` files have correct imports
- Verify file names match exactly

### Error: "list index out of range"
- Table column count doesn't match data
- Double-check: `QTableWidget(0, X)` where X = number of headers

### Error: "KeyError: 'xxx'"
- Use `.get('key', default)` instead of `['key']`
- Check if invoice has the expected structure

### Data not showing
- Add `print(invoices)` to see structure
- Check if filters are too restrictive
- Verify `populate()` is being called

## 📋 Completion Checklist

- [ ] `purchase_report.py` - populate() method
- [ ] `all_transactions.py` - _init_ui() + populate()
- [ ] `day_book.py` - _init_ui() + populate()
- [ ] `profit_loss.py` - _init_ui() + populate()
- [ ] `bill_wise_profit.py` - _init_ui() + populate()
- [ ] `cash_transactions.py` - _init_ui() + populate()
- [ ] `balance_report.py` - _init_ui() + populate()
- [ ] `reports_page.py` - All TODO sections
- [ ] Test imports
- [ ] Test application
- [ ] Backup original `reports.py` → `reports.py.old`

## 🎉 Final Step

Once everything works:
```bash
# Backup original
copy travel_billing_software\ui\reports.py travel_billing_software\ui\reports.py.old

# Update import in main_window.py if needed (should auto-work via __init__.py)
```

---

**You're 40% done!** The hardest parts (architecture, db, utils) are complete.
Now it's just filling in the blanks following the patterns provided. 🚀

Start with `purchase_report.py` - it's already 90% done!
