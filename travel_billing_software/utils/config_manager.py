import json
import os
from travel_billing_software.utils.path_loader import persistent_data_path

# Use persistent storage for config file
CONFIG_FILE = persistent_data_path("settings.json")

# Default Defaults (Updated with missing keys to prevent KeyErrors)
DEFAULT_CONFIG = {
    "company": {
        "name": "My Travel Agency",
        "tagline": "Your Trusted Travel Partner",
        "address": "123 Business Rd, City",
        "email": "info@travel.com",
        "phone": "+91 0000000000",
        "gst_number": ""
    },
    "invoice": {
        "prefix": "INV",
        "currency_symbol": "₹",
        "default_tax_rate": 18.0,
        "date_format": "dd/MM/yyyy",       # <--- Added missing key
        "tax_label": "GST",                # <--- Added missing key
        "terms": "Payment due on receipt.",
        "footer_note": "Thank you for your business!"
    },
    "app_settings": {
        "font_size": 12,
        "theme_color": "#7c3aed", # Default Purple
        "dark_mode": True
    },
    "dropdowns": {
        "suppliers": ["Emirates", "Qatar Airways", "IndiGo", "Air India"],
        "classes": ["Economy", "Business", "First Class"],
        "sectors": ["Domestic", "International"]
    }
}

class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        """Load config from JSON or use defaults."""
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    # Critical: Merge with defaults to ensure new keys (like date_format) exist
                    self._merge_defaults(self.config, DEFAULT_CONFIG)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = DEFAULT_CONFIG.copy()
        else:
            self.config = DEFAULT_CONFIG.copy()
            self.save_config()

    def _merge_defaults(self, current, defaults):
        """Recursively update missing keys in the current config."""
        for key, value in defaults.items():
            if key not in current:
                current[key] = value
            elif isinstance(value, dict) and isinstance(current[key], dict):
                self._merge_defaults(current[key], value)

    def save_config(self):
        """Save current config to JSON."""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            # print("Configuration saved successfully.") 
        except Exception as e:
            print(f"Error saving config: {e}")

    # --- Getters ---
    def get_company_info(self): return self.config.get("company", {})
    def get_invoice_config(self): return self.config.get("invoice", {})
    def get_app_settings(self): return self.config.get("app_settings", {})
    def get_dropdowns(self, key): return self.config.get("dropdowns", {}).get(key, [])

    # --- Setters ---
    def set_company_info(self, data): 
        self.config["company"] = data
        self.save_config()

    def set_invoice_config(self, data):
        # Preserve existing keys that might not be in the incoming data
        current = self.config["invoice"]
        current.update(data)
        self.save_config()

    def set_app_setting(self, key, value):
        self.config["app_settings"][key] = value
        self.save_config()

    def add_dropdown_item(self, category, item):
        if category not in self.config["dropdowns"]:
             self.config["dropdowns"][category] = []
             
        if item not in self.config["dropdowns"][category]:
            self.config["dropdowns"][category].append(item)
            self.save_config()
            return True
        return False

    def remove_dropdown_item(self, category, item):
        if category in self.config["dropdowns"] and item in self.config["dropdowns"][category]:
            self.config["dropdowns"][category].remove(item)
            self.save_config()
            return True
        return False