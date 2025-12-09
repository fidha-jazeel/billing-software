"""
Travel Agency Billing Software
Main entry point with login authentication
"""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
import sys
import os

# Import from clean structure
from travel_billing_software.ui.login_page import LoginPage
from travel_billing_software.ui.main_window import DashboardImproved as MainWindow
from travel_billing_software.utils.auto_updater import AutoUpdater
from travel_billing_software.ui.update_dialog import UpdateDialog


def check_for_updates(main_window):
    """Check for updates in background after app starts"""
    try:
        updater = AutoUpdater()
        update_available, latest_version, download_url = updater.check_for_updates()
        
        if update_available:
            # Show update dialog
            dialog = UpdateDialog(updater, latest_version, download_url, main_window)
            dialog.exec()
    except Exception as e:
        # Silently fail - don't interrupt user experience if update check fails
        print(f"Update check failed: {e}")


if __name__ == "__main__":
    # Clear any cached database instance to ensure fresh connection with correct path
    import travel_billing_software.database.db_manager as db_module
    db_module._db_instance = None
    
    app = QApplication(sys.argv)
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), 'billing_app.ico')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Create main window instance (hidden initially)
    main_window = MainWindow()
    
    # Create and show login page
    login_page = LoginPage()
    
    # Connect login success to show main window
    def on_login_success():
        """Show main window after successful login and check for updates"""
        main_window.showMaximized()
        
        # Check for updates 2 seconds after login (non-blocking)
        QTimer.singleShot(2000, lambda: check_for_updates(main_window))
    
    login_page.login_successful.connect(on_login_success)
    login_page.showMaximized()
    
    sys.exit(app.exec())
