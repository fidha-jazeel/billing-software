"""
About Page for Travel Agency Billing Software
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea
from PyQt5.QtCore import Qt


class AboutPage(QWidget):
    """About page displaying application information and features."""
    
    def __init__(self, colors, app_config, company_info):
        super().__init__()
        self.COLORS = colors
        self.APP_CONFIG = app_config
        self.COMPANY_INFO = company_info
        self.init_ui()
    
    def init_ui(self):
        """Initialize the About page UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Scroll area to fit all content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {self.COLORS['primary_bg']};
            }}
            QScrollBar:vertical {{
                background-color: {self.COLORS['secondary_bg']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {self.COLORS['accent_primary']};
                border-radius: 6px;
                min-height: 30px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {self.COLORS['accent_secondary']};
            }}
        """)
        
        # Container widget for scroll area
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 10, 0)
        scroll_layout.setSpacing(15)

        # Header
        heading = QLabel(f"<h2 style='color:{self.COLORS['accent_secondary']};'>ℹ️ About</h2>")
        scroll_layout.addWidget(heading)
        
        # Main info frame
        info_frame = QFrame()
        info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {self.COLORS['secondary_bg']};
                border-radius: 8px;
                padding: 30px;
            }}
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(15)
        
        # App name and tagline
        app_name = QLabel(f"<h1 style='color:{self.COLORS['accent_primary']};'>🎫 Al Chishtiya Travels Billing Software</h1>")
        app_name.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(app_name)
        
        tagline = QLabel(f"<p style='color:{self.COLORS['text_secondary']}; font-size:25px; font-style:italic;'>{self.COMPANY_INFO['tagline']}</p>")
        tagline.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(tagline)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background-color: {self.COLORS['accent_primary']}; height: 2px;")
        info_layout.addWidget(line)
        
        # Version and details
        details = QLabel(f"""
        <p style='line-height: 2.0;'>
        <b style='color:{self.COLORS['accent_primary']}; font-size:20px;'>Version:</b> <span style='color:{self.COLORS['text_primary']}; font-size:20px;'>{self.APP_CONFIG['version']}</span><br>
        <b style='color:{self.COLORS['accent_primary']}; font-size:20px;'>Year:</b> <span style='color:{self.COLORS['text_primary']}; font-size:20px;'>{self.APP_CONFIG['year']}</span>
        </p>
        
        <p style='margin-top: 20px;'>
        <b style='color:{self.COLORS['accent_primary']}; font-size:20px;'>Contact Information:</b><br>
        <span style='color:{self.COLORS['text_secondary']}; font-size:20px;'>
        📧 Email: {self.COMPANY_INFO['email']}<br>
        📞 Phone: {self.COMPANY_INFO['phone']}
        </span>
        </p>
        
        <p style='margin-top: 20px;'>
        <b style='color:{self.COLORS['accent_primary']}; font-size:20px;'>✨ Key Features:</b>
        </p>
        """)
        details.setStyleSheet(f"color: {self.COLORS['text_primary']};")
        info_layout.addWidget(details)
        
        # Features list
        features_list = QLabel(f"""
        <ul style='color:{self.COLORS['text_secondary']}; line-height: 2.4; font-size:20px; margin-left: 10px;'>
        <li style='margin-bottom: 8px;'>🔐 Secure login system with password authentication</li>
        <li style='margin-bottom: 8px;'>📄 Dynamic invoice creation with passenger details, PNR, sectors</li>
        <li style='margin-bottom: 8px;'>✈️ Travel-specific fields: Class (Economy/Business/First)</li>
        <li style='margin-bottom: 8px;'>💰 Automatic calculations with discount support</li>
        <li style='margin-bottom: 8px;'>📊 Comprehensive analytics and reports</li>
        <li style='margin-bottom: 8px;'>💾 SQLite database for reliable data storage</li>
        <li style='margin-bottom: 8px;'>📄 PDF export and print functionality</li>
        <li style='margin-bottom: 8px;'>⚙️ Configurable company and invoice settings</li>
        <li style='margin-bottom: 8px;'>🎨 Modern dark theme interface</li>
        <li style='margin-bottom: 8px;'>🔍 Search and filter invoices</li>
        </ul>
        """)
        features_list.setStyleSheet(f"color: {self.COLORS['text_secondary']};")
        features_list.setWordWrap(True)
        info_layout.addWidget(features_list)
        
        # Copyright
        copyright_label = QLabel(f"<p style='margin-top: 30px; color: {self.COLORS['text_muted']}; text-align: center; font-size:20px;'>© {self.APP_CONFIG['year']} {self.COMPANY_INFO['name']}. All rights reserved.<br>Built with ❤️ using PyQt5 and SQLite</p>")
        copyright_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(copyright_label)
        
        scroll_layout.addWidget(info_frame)
        scroll_layout.addStretch()
        
        # Set scroll content
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
