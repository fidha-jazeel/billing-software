import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow
from ui.home_page import HomePage
from ui.reports_page import ReportsPage
from ui.settings_page import SettingsPage
from ui.about_page import AboutPage
from database.db_manager import DatabaseManager
from utils.styles import get_dark_theme

def main():
    """Main entry point for the application"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Travel Agency Billing")
    app.setOrganizationName("Travel Agency")
    app.setApplicationVersion("1.0.0")
    
    # Apply dark theme
    app.setStyleSheet(get_dark_theme())
    
    # Initialize database
    db_manager = DatabaseManager('billing.db')
    
    # Create main window
    main_window = MainWindow()
    
    # Create and add pages
    home_page = HomePage(db_manager)
    reports_page = ReportsPage(db_manager)
    settings_page = SettingsPage(db_manager)
    about_page = AboutPage()
    
    main_window.add_page('home', home_page)
    main_window.add_page('reports', reports_page)
    main_window.add_page('settings', settings_page)
    main_window.add_page('about', about_page)
    
    # Switch to home page by default
    main_window.switch_page('home')
    
    # Show main window
    main_window.showMaximized()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
