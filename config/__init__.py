"""
Configuration package for Travel Agency Billing Software
"""

from .settings import (
    COMPANY_INFO,
    APP_CONFIG,
    COLORS,
    FONTS,
    INVOICE_CONFIG,
    SUPPLIERS,
    SECTORS,
    TABLE_CONFIG,
    LAYOUT_CONFIG,
    BUTTON_CONFIG,
    PRINT_CONFIG,
    VALIDATION,
    FEATURES,
    get_color,
    get_company_name,
    get_company_info_formatted,
    get_currency_symbol,
    get_invoice_prefix,
    get_supplier_list,
    get_sector_list,
)

__all__ = [
    'COMPANY_INFO',
    'APP_CONFIG',
    'COLORS',
    'FONTS',
    'INVOICE_CONFIG',
    'SUPPLIERS',
    'SECTORS',
    'TABLE_CONFIG',
    'LAYOUT_CONFIG',
    'BUTTON_CONFIG',
    'PRINT_CONFIG',
    'VALIDATION',
    'FEATURES',
    'get_color',
    'get_company_name',
    'get_company_info_formatted',
    'get_currency_symbol',
    'get_invoice_prefix',
    'get_supplier_list',
    'get_sector_list',
]
