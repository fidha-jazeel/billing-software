from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Center content
        layout.addStretch()
        
        # App icon/logo
        app_icon = QLabel("🎫")
        app_icon.setStyleSheet("font-size: 72pt;")
        app_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_icon)
        
        # App title
        title = QLabel("Travel Agency Billing Software")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24pt; margin-top: 10px;")
        title.setWordWrap(True)
        layout.addWidget(title)
        
        # Version
        version = QLabel("Version 1.0.0")
        version.setStyleSheet("font-size: 12pt; color: #a0a0a0; margin-bottom: 20px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)
        
        # Description card
        desc_card = QFrame()
        desc_card.setObjectName("card")
        desc_card.setMaximumWidth(600)
        
        desc_layout = QVBoxLayout(desc_card)
        
        description = QLabel(
            "A comprehensive billing and invoicing solution designed specifically "
            "for travel agencies. Manage customers, create invoices, track payments, "
            "and generate detailed reports - all in a beautiful dark-themed interface."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("font-size: 11pt; line-height: 1.6; padding: 20px;")
        desc_layout.addWidget(description)
        
        # Center the card
        card_container = QHBoxLayout()
        card_container.addStretch()
        card_container.addWidget(desc_card)
        card_container.addStretch()
        layout.addLayout(card_container)
        
        # Features
        features_label = QLabel("✨ Key Features")
        features_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #0d7377; margin-top: 20px;")
        features_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        features_label.setWordWrap(True)
        layout.addWidget(features_label)
        
        features_card = QFrame()
        features_card.setObjectName("card")
        features_card.setMaximumWidth(600)
        
        features_layout = QVBoxLayout(features_card)
        
        features = [
            "📄 Dynamic invoice creation with multiple items",
            "👥 Customer management and tracking",
            "📊 Comprehensive reports and analytics",
            "💰 Payment tracking with balance calculation",
            "🎨 Beautiful dark theme interface",
            "💾 SQLite database for reliable data storage",
            "🔍 Quick search and filtering capabilities"
        ]
        
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet("font-size: 10pt; padding: 5px; margin-left: 20px;")
            feature_label.setWordWrap(True)
            features_layout.addWidget(feature_label)
        
        # Center the features card
        features_container = QHBoxLayout()
        features_container.addStretch()
        features_container.addWidget(features_card)
        features_container.addStretch()
        layout.addLayout(features_container)
        
        layout.addSpacing(20)
        
        # Technology stack
        tech_label = QLabel("Built with PyQt6 & SQLite")
        tech_label.setStyleSheet("font-size: 10pt; color: #6a6a6a;")
        tech_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tech_label)
        
        # Copyright
        copyright_label = QLabel("© 2025 Travel Agency. All rights reserved.")
        copyright_label.setStyleSheet("font-size: 9pt; color: #6a6a6a; margin-top: 10px;")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)
        
        layout.addStretch()
