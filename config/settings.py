"""
Configuration settings for Travel Agency Billing Software
All static values and settings are centralized here for easy management.
"""

# ==================== COMPANY INFORMATION ====================
COMPANY_INFO = {
    "name": "Al Chishtiya Travels",
    "tagline": "Your Trusted Travel Partner",
    "email": "info@alchishtiyatravels.com",
    "phone": "+1-234-567-8900",
    "address": "123 Business Street, City, Country",
    "website": "www.alchishtiyatravels.com",
    "tax_id": "TAX123456789",
    "logo_path": None  # Set to image path if you have a logo
}

# ==================== APPLICATION SETTINGS ====================
APP_CONFIG = {
    "window_title": "Al Chishtiya Travels - Billing Software",
    "window_width": 1200,
    "window_height": 750,
    "version": "2.2.0",
    "developer": "Fidha Jazeel",
    "year": "2025"
}

# ==================== COLOR THEME ====================
# Professional dark theme with consistent colors throughout
COLORS = {
    # Primary Colors
    "primary_bg": "#1a1a1a",           # Main background
    "secondary_bg": "#2a2a2a",         # Cards, frames
    "tertiary_bg": "#252525",          # Alternate rows
    
    # Text Colors
    "text_primary": "#ffffff",         # Main text (headers)
    "text_secondary": "#dddddd",       # Secondary text (inputs)
    "text_muted": "#aaaaaa",           # Muted text (placeholders)
    "text_disabled": "#888888",        # Disabled text
    
    # Accent Colors
    "accent_primary": "#7c3aed",       # Main accent (purple)
    "accent_secondary": "#a78bfa",     # Light accent (lavender)
    "accent_cyan": "#14b8a6",          # Teal accent (headings)
    "accent_gold": "#f59e0b",          # Amber (total amounts)
    
    # Status Colors
    "success": "#51CF66",              # Success/Save (green)
    "danger": "#FF6B6B",               # Error/Delete (red)
    "warning": "#FFD700",              # Warning (yellow/gold)
    "info": "#a78bfa",                 # Info (lavender)
    "teal": "#14b8a6",                 # Share button (teal)
    
    # Border Colors
    "border_primary": "#444444",       # Main borders
    "border_secondary": "#333333",     # Secondary borders
    "border_focus": "#9b9bff",         # Focused elements
    
    # Grid Colors
    "grid_lines": "#444444",           # Table grid lines
}

# ==================== FONT SETTINGS ====================
FONTS = {
    "family_primary": "Segoe UI",
    "family_secondary": "Arial",
    "family_mono": "Consolas",
    
    "size_title": "24px",
    "size_heading": "16px",
    "size_subheading": "14px",
    "size_normal": "13px",
    "size_small": "12px",
    "size_tiny": "10px",
    
    "weight_bold": "bold",
    "weight_semibold": "600",
    "weight_normal": "normal",
}

# ==================== INVOICE SETTINGS ====================
INVOICE_CONFIG = {
    "number_prefix": "INV",
    "date_format": "dd/MM/yyyy",
    "currency_symbol": "₹",
    "tax_label": "GST",
    "default_tax_rate": 5.0,  # Default tax percentage
    
    # Invoice terms and conditions
    "terms": "Payment due within 30 days. Late payments subject to 1.5% monthly interest.",
    "footer_note": "Thank you for your business!",
    
    # File paths
    "save_directory": "invoices",
    "pdf_directory": "invoices/pdf",
    "backup_directory": "invoices/backup",
}

# ==================== SUPPLIERS LIST ====================
# Predefined suppliers for dropdown
SUPPLIERS = [
    "Select Supplier",
    "Emirates Airlines",
    "Qatar Airways",
    "Air India",
    "IndiGo",
    "SpiceJet",
    "Vistara",
    "Air Asia",
    "Hilton Hotels",
    "Marriott International",
    "Taj Hotels",
    "ITC Hotels",
    "Oberoi Hotels",
    "Custom Supplier"
]

# ==================== SECTORS LIST ====================
# Predefined sectors for dropdown
SECTORS = [
    "Select Sector",
    "Domestic",
    "International",
    "Regional",
    "Local",
    "Charter",
    "Corporate",
    "Leisure"
]

# ==================== TABLE COLUMN SETTINGS ====================
TABLE_CONFIG = {
    "columns": [
        {"name": "Item Name", "width": 200, "resize_mode": "Fixed"},
        {"name": "Ticket", "width": 0, "resize_mode": "ResizeToContents"},
        {"name": "Sector", "width": 0, "resize_mode": "ResizeToContents"},
        {"name": "Supplier", "width": 0, "resize_mode": "ResizeToContents"},
        {"name": f"Price ({INVOICE_CONFIG['currency_symbol']})", "width": 0, "resize_mode": "ResizeToContents"},
        {"name": "Qty", "width": 0, "resize_mode": "ResizeToContents"},
        {"name": "Tax (%)", "width": 0, "resize_mode": "ResizeToContents"},
        {"name": f"Amount ({INVOICE_CONFIG['currency_symbol']})", "width": 0, "resize_mode": "ResizeToContents"},
        {"name": "Actions", "width": 0, "resize_mode": "ResizeToContents"}
    ],
    "min_height": 300,
    "row_height": 45,
    "max_height": 600,
}

# ==================== LAYOUT SETTINGS ====================
LAYOUT_CONFIG = {
    # Invoice Details Section
    "invoice_details_label_width": 140,
    "invoice_details_value_width": 220,  # All fields same width
    
    # Calculation Section
    "calculation_label_width": 100,
    "calculation_value_width": 130,
    "calculation_spacing": 8,  # Reduced spacing between items
    
    # Margins and Spacing
    "page_margin": 20,
    "section_spacing": 12,  # Reduced from 15
    "widget_spacing": 8,    # Reduced from 10
    "button_spacing": 10,
    
    # Border Radius
    "border_radius": "8px",
    "button_radius": "5px",
    "input_radius": "3px",
}

# ==================== BUTTON STYLES ====================
BUTTON_CONFIG = {
    "height": 45,
    "padding": "10px 20px",
    "font_size": "13px",
    "font_weight": "bold",
    
    "colors": {
        "save": {"bg": COLORS["success"], "hover": "#69DB7C", "pressed": "#40C057"},
        "pdf": {"bg": COLORS["danger"], "hover": "#FF8787", "pressed": "#FA5252"},
        "print": {"bg": COLORS["info"], "hover": "#b5b5ff", "pressed": "#8585ee"},
        "share": {"bg": COLORS["teal"], "hover": "#38D9A9", "pressed": "#12B886"},
        "add": {"bg": COLORS["accent_primary"], "hover": "#7a7aff", "pressed": "#4a4aee"},
        "delete": {"bg": COLORS["danger"], "hover": "#FF8787", "pressed": "#FA5252"},
    }
}

# ==================== PRINT/PDF SETTINGS ====================
PRINT_CONFIG = {
    "page_size": "A4",
    "margin": 100,
    "resolution": "HighResolution",
    
    # Fonts for PDF/Print
    "fonts": {
        "title": {"family": "Arial", "size": 24, "bold": True},
        "subtitle": {"family": "Arial", "size": 14, "bold": True},
        "header": {"family": "Arial", "size": 11, "bold": True},
        "normal": {"family": "Arial", "size": 10, "bold": False},
        "small": {"family": "Arial", "size": 9, "bold": False},
    }
}

# ==================== VALIDATION SETTINGS ====================
VALIDATION = {
    "max_price": 10_000_000,
    "max_quantity": 9999,
    "max_tax": 100,
    "min_quantity": 1,
    "decimal_places_currency": 2,
    "decimal_places_tax": 2,
}

# ==================== FEATURE FLAGS ====================
FEATURES = {
    "enable_backup": True,
    "enable_export_excel": True,
    "enable_email_integration": False,  # Set to True when email is configured
    "enable_whatsapp_share": False,     # Set to True when WhatsApp is configured
    "enable_cloud_sync": False,         # Set to True when cloud is configured
    "enable_auto_save": True,
    "enable_dark_mode": True,           # Can add light mode toggle
}

# ==================== DATABASE SETTINGS (Future Use) ====================
DATABASE = {
    "type": "sqlite",  # or "mysql", "postgresql"
    "name": "billing.db",
    "path": "data/billing.db",
    "enable_sync": False,
}

# ==================== EMAIL SETTINGS (Future Use) ====================
EMAIL = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "use_tls": True,
    "sender_email": "",     # Set your email
    "sender_password": "",  # Set your password or app password
}

# ==================== SHORTCUTS ====================
SHORTCUTS = {
    "new_invoice": "Ctrl+N",
    "save_invoice": "Ctrl+S",
    "save_pdf": "Ctrl+P",
    "print": "Ctrl+Shift+P",
    "add_item": "Ctrl+I",
    "delete_item": "Del",
    "quit": "Ctrl+Q",
}

# ==================== HELPER FUNCTIONS ====================
def get_color(color_name):
    """Get color value by name."""
    return COLORS.get(color_name, COLORS["text_primary"])

def get_company_name():
    """Get company name."""
    return COMPANY_INFO["name"]

def get_company_info_formatted():
    """Get formatted company information for display."""
    return {
        "name": COMPANY_INFO["name"],
        "tagline": COMPANY_INFO["tagline"],
        "contact": f"Email: {COMPANY_INFO['email']} | Phone: {COMPANY_INFO['phone']}",
        "address": COMPANY_INFO["address"],
    }

def get_currency_symbol():
    """Get currency symbol."""
    return INVOICE_CONFIG["currency_symbol"]

def get_invoice_prefix():
    """Get invoice number prefix."""
    return INVOICE_CONFIG["number_prefix"]

def get_supplier_list():
    """Get list of suppliers."""
    return SUPPLIERS.copy()

def get_sector_list():
    """Get list of sectors."""
    return SECTORS.copy()
