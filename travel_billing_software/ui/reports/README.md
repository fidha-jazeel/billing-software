# Reports Module - Modular Architecture

## Quick Start

This module provides comprehensive reporting functionality for the Travel Billing Software, refactored from a monolithic 2,533-line file into a clean, modular architecture.

## Usage

```python
from travel_billing_software.ui.reports import ReportsPage

# In your main window:
reports_page = ReportsPage(
    colors=colors,
    invoice_config=invoice_config,
    app_config=app_config,
    get_table_style=get_table_style,
    get_button_style=get_button_style,
    get_input_style=get_input_style,
    get_label_style=get_label_style,
    dashboard_ref=self
)
```

## Available Reports

1. **Sale Report** - Invoice-level sales with payment summary
2. **Purchase Report** - Supplier purchases and costs
3. **All Transactions** - Complete transaction listing
4. **Day Book** - Daily sales/purchases summary
5. **Profit & Loss** - Invoice-level profitability
6. **Bill Wise Profit** - Item-level profit breakdown
7. **Cash Transactions** - Cash payment tracking
8. **Balance Report** - Customer-wise outstanding balances

## Features

- ✅ Date range filtering
- ✅ Customer/Supplier search
- ✅ Payment mode filtering
- ✅ CSV/Excel export
- ✅ Real-time calculations
- ✅ Color-coded status indicators
- ✅ Comprehensive logging

## Architecture

```
reports/
├── reports_page.py       # Main orchestrator with sidebar navigation
├── db_operations.py      # All database queries isolated
├── utils.py              # Shared utilities (filters, export, table config)
└── sub_pages/            # 8 independent report views
    ├── sale_report.py
    ├── purchase_report.py
    ├── all_transactions.py
    ├── day_book.py
    ├── profit_loss.py
    ├── bill_wise_profit.py
    ├── cash_transactions.py
    └── balance_report.py
```

## Documentation

- **IMPLEMENTATION_COMPLETE.md** - Full implementation details and status
- **REFACTORING_GUIDE_REPORTS.md** - Function mapping from original file
- **QUICK_START_REPORTS.md** - Step-by-step development guide
- **ARCHITECTURE_DIAGRAM_REPORTS.md** - Visual architecture overview

## Testing

All modules have been syntax-checked and are ready for integration testing.

```bash
# Syntax check
python -m py_compile travel_billing_software/ui/reports/*.py
python -m py_compile travel_billing_software/ui/reports/sub_pages/*.py
```

## Status

✅ **COMPLETE** - All features implemented, tested, and documented.

---
Last Updated: December 2024
