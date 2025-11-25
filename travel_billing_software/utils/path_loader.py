import os, sys

def resource_path(relative_path):
    """Handles paths for both PyInstaller exe and development."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    return os.path.join(base_path, relative_path)
