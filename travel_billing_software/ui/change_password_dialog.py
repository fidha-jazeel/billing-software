"""
Change Password Dialog for Billing Software
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth import AuthManager


class ChangePasswordDialog(QDialog):
    """Dialog for changing password"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_manager = AuthManager()
        self.setWindowTitle("Change Password")
        # Remove icon or use a simple one
        self.setModal(True)
        self.setFixedSize(480, 560)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Icon
        icon_label = QLabel("🔐")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Segoe UI", 42))
        icon_label.setFixedSize(90, 90)
        icon_label.setStyleSheet("""
            background-color: #7c3aed;
            border-radius: 45px;
        """)
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        
        layout.addSpacing(10)
        
        # Title
        title_label = QLabel("Change Password")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff; background: transparent;")
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Enter your current password and new password")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setStyleSheet("color: #94a3b8; background: transparent;")
        subtitle_label.setWordWrap(True)
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(15)
        
        # Current Password
        current_label = QLabel("Current Password")
        current_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        current_label.setStyleSheet("color: #e2e8f0; background: transparent;")
        layout.addWidget(current_label)
        
        self.current_password = QLineEdit()
        self.current_password.setEchoMode(QLineEdit.Password)
        self.current_password.setPlaceholderText("Enter current password")
        self.current_password.setFont(QFont("Segoe UI", 11))
        self.current_password.setFixedHeight(45)
        self.current_password.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #7c3aed;
                background-color: #2a2a2a;
            }
        """)
        layout.addWidget(self.current_password)
        
        layout.addSpacing(5)
        
        # New Password
        new_label = QLabel("New Password")
        new_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        new_label.setStyleSheet("color: #e2e8f0; background: transparent;")
        layout.addWidget(new_label)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setPlaceholderText("Enter new password (min. 4 characters)")
        self.new_password.setFont(QFont("Segoe UI", 11))
        self.new_password.setFixedHeight(45)
        self.new_password.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #7c3aed;
                background-color: #2a2a2a;
            }
        """)
        layout.addWidget(self.new_password)
        
        layout.addSpacing(5)
        
        # Confirm Password
        confirm_label = QLabel("Confirm New Password")
        confirm_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        confirm_label.setStyleSheet("color: #e2e8f0; background: transparent;")
        layout.addWidget(confirm_label)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setPlaceholderText("Confirm new password")
        self.confirm_password.setFont(QFont("Segoe UI", 11))
        self.confirm_password.setFixedHeight(45)
        self.confirm_password.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #7c3aed;
                background-color: #2a2a2a;
            }
        """)
        self.confirm_password.returnPressed.connect(self.change_password)
        layout.addWidget(self.confirm_password)
        
        layout.addSpacing(10)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setFixedHeight(45)
        cancel_btn.setMinimumWidth(140)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: #94a3b8;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
                border: 2px solid #7c3aed;
                color: #ffffff;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("✓ Change Password")
        save_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setFixedHeight(45)
        save_btn.setMinimumWidth(140)
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #14b8a6);
                color: white;
                border: none;
                border-radius: 8px;
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
        save_btn.clicked.connect(self.change_password)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.current_password.setFocus()
    
    def change_password(self):
        """Handle password change"""
        current = self.current_password.text().strip()
        new = self.new_password.text().strip()
        confirm = self.confirm_password.text().strip()
        
        if not current or not new or not confirm:
            QMessageBox.warning(self, "Input Required", "Please fill in all fields.")
            return
        
        if not self.auth_manager.verify_password(current):
            QMessageBox.critical(self, "Error", "Current password is incorrect.")
            self.current_password.clear()
            self.current_password.setFocus()
            return
        
        if len(new) < 4:
            QMessageBox.warning(self, "Weak Password", "New password must be at least 4 characters long.")
            return
        
        if new != confirm:
            QMessageBox.warning(self, "Mismatch", "New passwords do not match.")
            self.confirm_password.clear()
            self.confirm_password.setFocus()
            return
        
        if self.auth_manager.set_password(new):
            QMessageBox.information(self, "Success", "Password changed successfully!")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to change password.")
