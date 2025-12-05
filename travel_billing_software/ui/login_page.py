"""
Login Page for Billing Software
Professional login interface with password authentication
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox
)
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from travel_billing_software.auth.auth_manager import AuthManager
from travel_billing_software.ui.change_password_dialog import ChangePasswordDialog


class LoginPage(QWidget):
    """Login page widget with authentication"""
    
    # Signal emitted when login is successful
    login_successful = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.auth_manager = AuthManager()
        self.setWindowTitle("Travel Agency Billing Software - Login")
        # Remove icon or use a simple one
        self.init_ui()
        
    def init_ui(self):
        """Initialize the login UI with dark theme matching the dashboard"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Dark background container matching dashboard theme
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        # Login card with dark theme
        login_card = QFrame()
        login_card.setFixedSize(500, 680)
        login_card.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 15px;
            }
        """)
        
        card_layout = QVBoxLayout(login_card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo/Icon section with purple accent
        icon_container = QLabel()
        icon_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_container.setFixedHeight(100)
        icon_container.setStyleSheet("""
            background-color: #7c3aed;
            border-radius: 50px;
            font-size: 72px;
        """)
        icon_container.setText("🎫")
        card_layout.addWidget(icon_container)
        
        # Title with purple accent
        title_label = QLabel("Welcome Back")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))

        title_label.setFixedHeight(50)
        title_label.setStyleSheet("""
            color: #7c3aed;
            background: transparent;
        """)
        card_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Please enter your password to continue")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setFixedHeight(30)
        subtitle_label.setStyleSheet("color: #94a3b8; background: transparent; margin-bottom: 10px;")
        card_layout.addWidget(subtitle_label)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        password_label.setFixedHeight(25)
        password_label.setStyleSheet("color: #e2e8f0; background: transparent; margin-top: 10px;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setFont(QFont("Segoe UI", 12))
        self.password_input.setFixedHeight(50)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: none;
                border-radius: 10px;
                background-color: #1e1e1e;
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #7c3aed;
                background-color: #2a2a2a;
            }
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        # Default password hint
        hint_label = QLabel(f"💡 Default password: {self.auth_manager.get_default_password()}")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hint_label.setFont(QFont("Segoe UI", 10))
        hint_label.setFixedHeight(30)
        hint_label.setStyleSheet("color: #64748b; background: transparent;")
        card_layout.addWidget(hint_label)
        
        # Add spacer
        card_layout.addSpacing(15)
        
        # Login button with purple-teal gradient (centered)
        self.login_btn = QPushButton("Login")
        self.login_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)


        self.login_btn.setFixedHeight(50)
        self.login_btn.setFixedWidth(300)
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
        card_layout.addWidget(self.login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Change Password Link
        change_password_btn = QPushButton("Change Password")
        change_password_btn.setFont(QFont("Segoe UI", 10))
        change_password_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

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
        card_layout.addWidget(change_password_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Footer info
        card_layout.addSpacing(5)
        footer_label = QLabel("Travel Agency Billing Software v2.0")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        footer_label.setFont(QFont("Segoe UI", 9))
        footer_label.setFixedHeight(25)
        footer_label.setStyleSheet("color: #64748b; background: transparent;")
        card_layout.addWidget(footer_label)
        
        # Add card to container
        container_layout.addWidget(login_card)
        
        # Set main layout
        main_layout.addWidget(container)
        self.setLayout(main_layout)
        
        # Focus on password field
        self.password_input.setFocus()
    
    def handle_login(self):
        """Handle login button click - direct login without popup"""
        password = self.password_input.text().strip()
        
        if not password:
            QMessageBox.warning(self, "Input Required", "Please enter your password.")
            return
        
        if self.auth_manager.verify_password(password):
            # Direct login - no success popup
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