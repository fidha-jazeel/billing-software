"""
Configuration settings for Travel Agency Billing Software
Dynamic Configuration via ConfigManager (JSON)
"""
from datetime import datetime
from travel_billing_software.utils.config_manager import ConfigManager

# Initialize the Manager
cm = ConfigManager()

# ==================== FETCH DYNAMIC DATA ====================
COMPANY_INFO = cm.get_company_info()
INVOICE_CONFIG = cm.get_invoice_config()
APP_SETTINGS = cm.get_app_settings()

# ==================== COLOR THEME ====================
COLORS = {
    # Primary Colors
    "primary_bg": "#1a1a1a",           
    "secondary_bg": "#2a2a2a",         
    "tertiary_bg": "#252525",          
    
    # Text Colors
    "text_primary": "#ffffff",         
    "text_secondary": "#dddddd",       
    "text_muted": "#aaaaaa",           
    "text_disabled": "#888888",        
    
    # Accent Colors (Dynamic)
    "accent_primary": APP_SETTINGS.get("theme_color", "#7c3aed"),       
    "accent_secondary": "#a78bfa",     
    "accent_cyan": "#14b8a6",          
    "accent_gold": "#f59e0b",          
    
    # Status Colors
    "success": "#51CF66",              
    "danger": "#FF6B6B",               
    "warning": "#FFD700",              
    "info": "#a78bfa",                 
    "teal": "#14b8a6",                 
    
    # Border/Grid
    "border_primary": "#444444",       
    "border_secondary": "#333333",     
    "border_focus": APP_SETTINGS.get("theme_color", "#9b9bff"),         
    "grid_lines": "#444444",           
}

# ==================== APP CONFIG ====================
APP_CONFIG = {
    "window_title": f"{COMPANY_INFO.get('name', 'Billing Software')} - Manager",
    "window_width": 1200,
    "window_height": 750,
    "version": "2.4.0",
    "year": str(datetime.now().year),  # Fixes KeyError: 'year'
    "developer": "Fidha Jazeel",       # Fixes potential missing key
    "font_size": APP_SETTINGS.get("font_size", 12)
}

# ==================== DYNAMIC DROPDOWNS ====================
SUPPLIERS = cm.get_dropdowns("suppliers")
if not SUPPLIERS: 
    SUPPLIERS = ["Emirates", "Qatar Airways", "IndiGo", "Air India"]

SECTORS = cm.get_dropdowns("sectors")
if not SECTORS:
    SECTORS = ["Domestic", "International"]

TRAVEL_CLASSES = cm.get_dropdowns("classes")

# ==================== HELPER FUNCTIONS ====================
def get_company_info_formatted():
    info = cm.get_company_info()
    return {
        "name": info.get("name", ""),
        "tagline": info.get("tagline", ""),
        "contact": f"Email: {info.get('email', '')} | Phone: {info.get('phone', '')}",
        "address": info.get("address", ""),
    }

def get_currency_symbol():
    return cm.get_invoice_config().get("currency_symbol", "₹")

def get_invoice_prefix():
    return cm.get_invoice_config().get("prefix", "INV")

def get_supplier_list():
    return cm.get_dropdowns("suppliers")

def get_sector_list():
    return cm.get_dropdowns("sectors")

LAYOUT_CONFIG = {
    "border_radius": "8px",
    "button_radius": "5px",
    "input_radius": "3px",
}