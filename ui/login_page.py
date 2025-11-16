"""
Login Page for Billing Software
Professional login interface with password authentication
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import AuthManager
from ui.change_password_dialog import ChangePasswordDialog


class LoginPage(QWidget):
    """Login page widget with authentication"""
    
    # Signal emitted when login is successful
    login_successful = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.setWindowTitle("Billing Software - Login")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'travel_billing.ico')))
        self.init_ui()
        
    def init_ui(self):
        """Initialize the login UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create centered container with software theme
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a0b2e, stop:1 #16213e);
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignCenter)
        
        # Login card with gradient border effect
        login_card = QFrame()
        login_card.setFixedSize(500, 680)
        login_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: none;
            }
        """)
        
        card_layout = QVBoxLayout(login_card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo/Icon section with gradient
        icon_container = QLabel()
        icon_container.setAlignment(Qt.AlignCenter)
        icon_container.setFixedHeight(100)
        icon_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #7c3aed, stop:1 #14b8a6);
            border-radius: 50px;
            font-size: 72px;
        """)
        icon_container.setText("🔐")
        card_layout.addWidget(icon_container)
        
        # Title with gradient color
        title_label = QLabel("Welcome Back")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title_label.setFixedHeight(50)
        title_label.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #7c3aed, stop:1 #14b8a6);
            background: transparent;
        """)
        card_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Please enter your password to continue")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setFixedHeight(30)
        subtitle_label.setStyleSheet("color: #64748b; background: transparent; margin-bottom: 10px;")
        card_layout.addWidget(subtitle_label)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        password_label.setFixedHeight(25)
        password_label.setStyleSheet("color: #1e293b; background: transparent; margin-top: 10px;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setFont(QFont("Segoe UI", 12))
        self.password_input.setFixedHeight(50)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background-color: #f8fafc;
                color: #1e293b;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #7c3aed;
                background-color: white;
            }
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        # Default password hint
        hint_label = QLabel(f"💡 Default password: {self.auth_manager.get_default_password()}")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setFont(QFont("Segoe UI", 10))
        hint_label.setFixedHeight(30)
        hint_label.setStyleSheet("color: #94a3b8; background: transparent;")
        card_layout.addWidget(hint_label)
        
        # Add spacer
        card_layout.addSpacing(15)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Reset button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.reset_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.setFixedHeight(50)
        self.reset_btn.setMinimumWidth(150)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: none;
                border-radius: 10px;
                padding: 12px 30px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)
        self.reset_btn.clicked.connect(self.clear_password)
        button_layout.addWidget(self.reset_btn)
        
        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setFixedHeight(50)
        self.login_btn.setMinimumWidth(150)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #14b8a6);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 30px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6d28d9, stop:1 #0d9488);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5b21b6, stop:1 #0f766e);
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_btn)
        
        card_layout.addLayout(button_layout)
        
        # Change Password Link
        change_password_btn = QPushButton("Change Password")
        change_password_btn.setFont(QFont("Segoe UI", 10))
        change_password_btn.setCursor(Qt.PointingHandCursor)
        change_password_btn.setFixedHeight(30)
        change_password_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #7c3aed;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #6d28d9;
            }
        """)
        change_password_btn.clicked.connect(self.open_change_password)
        card_layout.addWidget(change_password_btn, alignment=Qt.AlignCenter)
        
        # Footer info
        card_layout.addSpacing(5)
        footer_label = QLabel("Travel Billing Software v1.0")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setFont(QFont("Segoe UI", 9))
        footer_label.setFixedHeight(25)
        footer_label.setStyleSheet("color: #94a3b8; background: transparent;")
        card_layout.addWidget(footer_label)
        
        # Add card to container
        container_layout.addWidget(login_card)
        
        # Set main layout
        main_layout.addWidget(container)
        self.setLayout(main_layout)
        
        # Focus on password field
        self.password_input.setFocus()
    
    def handle_login(self):
        """Handle login button click"""
        password = self.password_input.text().strip()
        
        if not password:
            QMessageBox.warning(self, "Input Required", "Please enter your password.")
            return
        
        if self.auth_manager.verify_password(password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.login_successful.emit()
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", "Incorrect password. Please try again.")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def clear_password(self):
        """Clear the password field"""
        self.password_input.clear()
        self.password_input.setFocus()
    
    def open_change_password(self):
        """Open change password dialog"""
        dialog = ChangePasswordDialog(self)
        dialog.exec_()
