"""
Travel Agency Billing Software
Main entry point with login authentication
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys
import os

# Import from clean structure
from travel_billing_software.ui.login_page import LoginPage
from travel_billing_software.ui.main_window import DashboardImproved as MainWindow

if __name__ == "__main__":
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
        """Show main window after successful login"""
        main_window.showMaximized()
    
    login_page.login_successful.connect(on_login_success)
    login_page.showMaximized()
    
    sys.exit(app.exec_())