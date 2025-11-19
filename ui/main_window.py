from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QStackedWidget, QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Travel Agency - Billing Software")
        self.setMinimumSize(1200, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)
        
        # Store page references
        self.pages = {}
        self.sidebar_buttons = {}
        
    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(5)
        
        # Logo/Title
        title_label = QLabel("🎫 Travel Agency")
        title_label.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            color: #0d7377;
            padding: 10px;
        """)
        layout.addWidget(title_label)
        
        # Add some spacing
        layout.addSpacing(20)
        
        # Navigation buttons
        self.home_btn = self.create_sidebar_button("🏠  Home", "home")
        self.reports_btn = self.create_sidebar_button("📊  Reports", "reports")
        self.settings_btn = self.create_sidebar_button("⚙️  Settings", "settings")
        self.about_btn = self.create_sidebar_button("ℹ️  About", "about")
        
        layout.addWidget(self.home_btn)
        layout.addWidget(self.reports_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.about_btn)
        
        # Store buttons
        self.sidebar_buttons = {
            'home': self.home_btn,
            'reports': self.reports_btn,
            'settings': self.settings_btn,
            'about': self.about_btn
        }
        
        # Connect buttons
        self.home_btn.clicked.connect(lambda: self.switch_page('home'))
        self.reports_btn.clicked.connect(lambda: self.switch_page('reports'))
        self.settings_btn.clicked.connect(lambda: self.switch_page('settings'))
        self.about_btn.clicked.connect(lambda: self.switch_page('about'))
        
        # Spacer to push buttons to top
        layout.addStretch()
        
        # Footer
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("color: #6a6a6a; font-size: 9pt; padding: 10px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        return sidebar
    
    def create_sidebar_button(self, text, page_id):
        """Create a styled sidebar button"""
        btn = QPushButton(text)
        btn.setObjectName("sidebarBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setProperty("active", "false")
        btn.setMinimumHeight(45)
        
        # Set font
        font = btn.font()
        font.setPointSize(11)
        btn.setFont(font)
        
        return btn
    
    def add_page(self, page_id, page_widget):
        """Add a page to the stack"""
        self.pages[page_id] = page_widget
        self.content_stack.addWidget(page_widget)
    
    def switch_page(self, page_id):
        """Switch to a different page"""
        if page_id in self.pages:
            # Update active button styling
            for btn_id, btn in self.sidebar_buttons.items():
                if btn_id == page_id:
                    btn.setProperty("active", "true")
                else:
                    btn.setProperty("active", "false")
                btn.style().unpolish(btn)
                btn.style().polish(btn)
            
            # Switch to the page
            self.content_stack.setCurrentWidget(self.pages[page_id])
    
    def get_current_page(self):
        """Get the current page widget"""
        return self.content_stack.currentWidget()

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
