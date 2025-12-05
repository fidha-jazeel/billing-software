"""
Home Module - Invoice Creation Interface
Refactored from monolithic home.py into modular architecture.

Exports:
    HomePage: Main widget for invoice creation

Architecture:
    - home_page.py: Main orchestrator widget
    - invoice_form.py: Customer & invoice metadata
    - items_table.py: Table for invoice items
    - calculations.py: Financial calculations
    - passport_dialog.py: Passport details form
    - db_operations.py: Database layer (isolated)
    - utils.py: Helper functions & PDF operations

Benefits:
    ✓ Each module < 500 lines (maintainable)
    ✓ Clear separation of concerns
    ✓ UI separated from business logic
    ✓ Database operations isolated
    ✓ Easy to test individual components
    ✓ Comprehensive logging throughout
    ✓ Full docstring documentation
"""

from .home_page import HomePage

__all__ = ['HomePage']
