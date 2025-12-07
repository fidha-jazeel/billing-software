import os, sys

def resource_path(relative_path):
    """Handles paths for both PyInstaller exe and development."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    return os.path.join(base_path, relative_path)

def persistent_data_path(filename=""):
    """Get persistent data path in user's AppData folder.
    This is where database, auth, and config files should be stored."""
    app_data_dir = os.path.join(os.getenv('LOCALAPPDATA', os.path.expanduser('~')), 'TravelBilling')
    os.makedirs(app_data_dir, exist_ok=True)
    return os.path.join(app_data_dir, filename) if filename else app_data_dir
