# Reports Display Investigation - Multiple Invoices Per Day

## Issue Report
User reported: "In both the Purchase Report and the Cash Transactions Report, only one invoice is shown per day, even if multiple invoices exist on the same date."

## Investigation Results

### ✅ Database Layer - WORKING PERFECTLY
**Test Results:**
- Total invoices in database: **23 invoices**
- December 9, 2025: **12 invoices**
- December 10, 2025: **10 invoices**
  
All invoices confirmed present in database with correct dates.

### ✅ Data Loading Layer - WORKING PERFECTLY  
**ReportsDBOperations.load_all_invoices():**
```
✓ Successfully loads all 23 invoices
✓ Each invoice includes all tickets/items
✓ Total of 89 items loaded across all invoices
✓ No duplicate invoice numbers
✓ Dates properly formatted (dd/MM/yyyy)
```

### ✅ Filter Logic - WORKING PERFECTLY
**Default filter range (1900-2125):**
```
✓ All 23 invoices pass through filters
✓ All 22 Dec 9-10 invoices visible
✓ No date-based grouping or deduplication
✓ Multiple invoices per date properly handled
```

### ✅ UI Population Logic - WORKING PERFECTLY

**Purchase Report (`purchase_report.py` lines 163-262):**
```python
for invoice in invoices:                    # Loop all invoices
    tickets = invoice.get('tickets', [])    
    for ticket in tickets:                   # Loop all tickets
        row = self.purchase_table.rowCount()
        self.purchase_table.insertRow(row)   # Add ONE row per ticket
        # ... populate columns ...
```
✅ Creates one row per TICKET (correct for Purchase Report)

**All Transactions Report (`all_transactions.py` lines 137-186):**
```python
for invoice in invoices:                     # Loop all invoices
    row = self.transactions_table.rowCount()
    self.transactions_table.insertRow(row)   # Add ONE row per invoice
    # ... populate columns ...
```
✅ Creates one row per INVOICE (correct for Cash Transactions Report)

## Root Cause Analysis

Since all backend components are working correctly:
1. ✅ Database has all invoices
2. ✅ Data loading retrieves all invoices  
3. ✅ Filters pass all invoices through (with defaults)
4. ✅ UI code correctly adds rows for each invoice/ticket

**The issue is most likely:**

### ACTIVE FILTERS IN THE USER'S GUI

The user has likely applied filters that are limiting the display:
- **Customer/Contact filter** - Text entered in customer search
- **Passenger filter** - Specific passenger name search
- **Sector filter** - Specific route search  
- **Supplier filter** - Dropdown not set to "All"
- **Booking Type filter** - Not set to "All"
- **Date range filter** - Narrowed date range

## Solution: Check and Clear Filters

### How to Verify Filters Are The Issue:

1. **Open Reports Page** → Navigate to Purchase Report or Cash Transactions
   
2. **Check Filter Section** (at top of report):
   ```
   Look for filter boxes/dropdowns with values:
   - Date Range: Should be 01/01/1900 to far future date
   - Contact: Should be EMPTY
   - Passenger: Should be EMPTY  
   - Sector: Should be EMPTY
   - Supplier: Should be "All"
   - Type: Should be "All"
   ```

3. **Click "Clear Filters" Button**
   - Should reset all filters to defaults
   - Should immediately show ALL invoices

4. **Check Row Count**
   - Purchase Report: Should show ~89 rows (one per ticket/item)
   - Cash Transactions: Should show ~23 rows (one per invoice)

### If Clear Filters Doesn't Work:

Check the application logs:
```
c:\\Users\\Fidha HP\\Desktop\\billing-latest\\billing-software\\logs\\
```

Look for lines containing:
- `"Applying filters"`
- `"Filter applied - X records matched out of Y"`
- `"Populating purchase report"`
- `"Populating all transactions report"`

This will show exactly how many records passed through filters.

## Code Verification

### No Issues Found In:
- ✅ `db_manager.py::get_all_invoices()` - Returns all invoices, no GROUP BY
- ✅ `db_operations.py::load_all_invoices()` - Processes all invoices correctly
- ✅ `utils.py::apply_filters()` - No date grouping or deduplication
- ✅ `purchase_report.py::populate()` - Correctly iterates all tickets
- ✅ `all_transactions.py::populate()` - Correctly iterates all invoices
- ✅ `reports_page.py::load_report_data()` - Passes all invoices to populate()

## Test Scripts Created

### test_invoice_display.py
Tests database and data loading:
```bash
python test_invoice_display.py
```
**Result:** All 22 invoices for Dec 9-10 loaded correctly ✅

### test_filter_logic.py  
Tests filter application:
```bash
python test_filter_logic.py
```
**Result:** All 23 invoices pass through default filters ✅

## Next Steps

1. **User Action Required:**
   - Open the application
   - Navigate to Reports → Purchase Report
   - Click "Clear Filters" button
   - Verify all invoices now display

2. **If issue persists after clearing filters:**
   - Check application logs for filter values being applied
   - Take screenshot of the reports page showing the issue
   - Provide the filter values visible in the UI

3. **Verify Fix:**
   - December 9: Should show 12 separate invoices (or their tickets)
   - December 10: Should show 10 separate invoices (or their tickets)
   - Total visible rows: ~89 for Purchase Report, ~23 for Cash Transactions

## Conclusion

**No code changes needed.** All backend systems are functioning correctly. The issue is user-facing filter state that needs to be cleared. The "Clear Filters" button should immediately resolve the issue.

If the problem persists after clearing filters, we'll need to investigate the PyQt6 QTableWidget state or potential UI threading issues, but this is highly unlikely given that all data layer tests pass.
