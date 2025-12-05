# Reports Module Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         REPORTS MODULE STRUCTURE                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ travel_billing_software/ui/reports/                                         │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  __init__.py                                                      │      │
│  │  ├─ Exports: ReportsPage                                          │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  reports_page.py  ⭐ MAIN ORCHESTRATOR                            │      │
│  │  ├─ ReportsPage class                                             │      │
│  │  │  ├─ Sidebar (8 report buttons)                                 │      │
│  │  │  ├─ Content Stack (8 report views)                             │      │
│  │  │  ├─ Shared filters (ReportFilters instance)                    │      │
│  │  │  ├─ Database ops (ReportsDBOperations instance)                │      │
│  │  │  └─ Coordinates: filtering, navigation, refresh                │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  db_operations.py  ✅ COMPLETE                                     │      │
│  │  ├─ ReportsDBOperations class                                     │      │
│  │  │  ├─ load_all_invoices() → fetch from database                  │      │
│  │  │  ├─ get_all_payments_summary() → cash/bank totals              │      │
│  │  │  ├─ calculate_balance_report() → customer balances             │      │
│  │  │  ├─ calculate_profit_metrics() → profit calculations           │      │
│  │  │  ├─ filter_invoices_by_date() → date range filtering           │      │
│  │  │  └─ filter_invoices_by_contact() → contact search              │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  utils.py  ✅ COMPLETE                                             │      │
│  │  ├─ TableConfigurator (configure table styling)                   │      │
│  │  ├─ ReportFilters (create filter UI & apply logic)                │      │
│  │  ├─ ReportExporter (export to CSV/PDF)                            │      │
│  │  ├─ SummaryCardManager (create/update metric cards)               │      │
│  │  └─ Helper functions:                                              │      │
│  │     ├─ create_report_header() → styled headers                    │      │
│  │     └─ show_no_records_message() → empty state                    │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │  sub_pages/  📁 FOLDER                                             │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  __init__.py                                                │  │      │
│  │  │  └─ Exports all 8 report views                              │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  sale_report.py  ✅ COMPLETE (Use as template!)             │  │      │
│  │  │  └─ SaleReportView                                          │  │      │
│  │  │     ├─ Table: 7 columns                                     │  │      │
│  │  │     ├─ Summary: Total Sales, Invoices, Avg Value           │  │      │
│  │  │     └─ populate(invoices) → fill table                     │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  purchase_report.py  ⚡ 90% DONE (Just finish populate!)    │  │      │
│  │  │  └─ PurchaseReportView                                      │  │      │
│  │  │     ├─ Table: 6 columns (Passenger, Supplier, PNR...)      │  │      │
│  │  │     ├─ Summary: Total Purchases, Items, Avg Cost           │  │      │
│  │  │     └─ TODO: Complete populate() method                    │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  all_transactions.py  📝 TODO                               │  │      │
│  │  │  └─ AllTransactionsView                                     │  │      │
│  │  │     ├─ Table: 8 columns                                     │  │      │
│  │  │     ├─ Summary: Transactions, Value, Avg                   │  │      │
│  │  │     └─ TODO: _init_ui() + populate()                       │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  day_book.py  📝 TODO                                       │  │      │
│  │  │  └─ DayBookView                                             │  │      │
│  │  │     ├─ Table: 5 columns (Date, Sales, Purchases, Profit)   │  │      │
│  │  │     ├─ Summary: Daily Sales, Purchases, Net Profit         │  │      │
│  │  │     ├─ SPECIAL: Groups invoices by DATE                    │  │      │
│  │  │     └─ TODO: _init_ui() + populate() with grouping         │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  profit_loss.py  📝 TODO                                    │  │      │
│  │  │  └─ ProfitLossView                                          │  │      │
│  │  │     ├─ Table: 7 columns (Invoice, Sales, Cost, Profit...)  │  │      │
│  │  │     ├─ Summary: Total Sales, Cost, Gross Profit            │  │      │
│  │  │     └─ TODO: _init_ui() + populate() with profit calc      │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  bill_wise_profit.py  📝 TODO (Most columns!)               │  │      │
│  │  │  └─ BillWiseProfitView                                      │  │      │
│  │  │     ├─ Table: 12 columns! (Most detailed)                  │  │      │
│  │  │     ├─ Summary: Total Sale, Cost, Profit                   │  │      │
│  │  │     └─ TODO: _init_ui() + populate() item-level profit     │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  cash_transactions.py  📝 TODO                              │  │      │
│  │  │  └─ CashTransactionsView                                    │  │      │
│  │  │     ├─ Table: 8 columns (Cash received/paid)               │  │      │
│  │  │     ├─ Summary: Cash Received, Paid, Net Flow              │  │      │
│  │  │     └─ TODO: _init_ui() + populate() cash filter           │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  │  ┌────────────────────────────────────────────────────────────┐  │      │
│  │  │  balance_report.py  📝 TODO                                 │  │      │
│  │  │  └─ BalanceReportView                                       │  │      │
│  │  │     ├─ Table: 8 columns (Customer balances)                │  │      │
│  │  │     ├─ Summary: Balance Due, Received, Invoiced            │  │      │
│  │  │     ├─ SPECIAL: Groups by CUSTOMER                         │  │      │
│  │  │     └─ TODO: _init_ui() + populate() with grouping         │  │      │
│  │  └────────────────────────────────────────────────────────────┘  │      │
│  │                                                                     │      │
│  └─────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW DIAGRAM                                  │
└─────────────────────────────────────────────────────────────────────────────┘

User clicks
"Sale Report"          ┌──────────────────────┐
in sidebar      ───────>│   reports_page.py    │
                        │  (Orchestrator)      │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │ _on_report_selected()│
                        │ _refresh_current()   │
                        └──────────┬───────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ db_operations   │    │ ReportFilters    │    │ SaleReportView   │
│ .load_all_      │    │ .apply_filters() │    │ .populate()      │
│  invoices()     │    │                  │    │                  │
└────────┬────────┘    └────────┬─────────┘    └────────┬─────────┘
         │                      │                       │
         │ Returns invoices     │ Applies filters       │ Renders UI
         ▼                      ▼                       ▼
    All invoices  ──────>  Filtered list  ──────>  Populated table
    from database           by date/contact         + Summary cards


┌─────────────────────────────────────────────────────────────────────────────┐
│                        COMPONENT DEPENDENCIES                                │
└─────────────────────────────────────────────────────────────────────────────┘

reports_page.py
    │
    ├─> db_operations.py (fetches data)
    ├─> utils.py (filters, table config, export)
    └─> sub_pages/*.py (all 8 views)
            │
            └─> utils.py (uses helpers like create_report_header)


┌─────────────────────────────────────────────────────────────────────────────┐
│                         WHAT TO IMPLEMENT                                    │
└─────────────────────────────────────────────────────────────────────────────┘

HIGH PRIORITY (Start here):
  1. purchase_report.py → populate() method only (90% done!)
  2. all_transactions.py → Copy pattern from sale_report.py
  3. reports_page.py → Fill in all TODO sections

MEDIUM PRIORITY:
  4. day_book.py → Add grouping logic
  5. profit_loss.py → Add profit calculations
  6. cash_transactions.py → Standard pattern

LOW PRIORITY (Can do last):
  7. bill_wise_profit.py → Most columns, but similar pattern
  8. balance_report.py → Customer grouping logic


┌─────────────────────────────────────────────────────────────────────────────┐
│                           SUCCESS CRITERIA                                   │
└─────────────────────────────────────────────────────────────────────────────┘

✅ All 8 sub-pages import without errors
✅ reports_page.py imports and initializes all views
✅ Application starts without crashes
✅ Clicking each report in sidebar shows correct view
✅ Filters work across all reports
✅ Export to CSV works for each report
✅ Summary cards update correctly
✅ No features lost from original reports.py


┌─────────────────────────────────────────────────────────────────────────────┐
│                          HELPFUL RESOURCES                                   │
└─────────────────────────────────────────────────────────────────────────────┘

📘 REFACTORING_GUIDE_REPORTS.md
   → Complete guide with function mappings and line references

📗 QUICK_START_REPORTS.md
   → Step-by-step instructions with patterns and tips

📙 sale_report.py
   → Complete working example - copy this pattern!

📕 purchase_report.py
   → 90% complete example with detailed TODOs

📊 Original reports.py (lines 19-2533)
   → Reference for original logic


Good luck! Start with purchase_report.py - you've got this! 🚀
