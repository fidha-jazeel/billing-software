"""
Dark theme stylesheet for the billing application
"""

DARK_THEME = """
/* Main Application */
QMainWindow {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}

/* Sidebar */
QFrame#sidebar {
    background-color: #252525;
    border-right: 1px solid #3a3a3a;
}

/* Sidebar buttons */
QPushButton#sidebarBtn {
    background-color: transparent;
    color: #e0e0e0;
    text-align: left;
    padding: 12px 20px;
    border: none;
    border-radius: 5px;
    font-size: 11pt;
}

QPushButton#sidebarBtn:hover {
    background-color: #2d2d2d;
}

QPushButton#sidebarBtn:pressed {
    background-color: #3a3a3a;
}

QPushButton#sidebarBtn[active="true"] {
    background-color: #0d7377;
    color: white;
    font-weight: bold;
}

/* Regular buttons */
QPushButton {
    background-color: #0d7377;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    font-size: 10pt;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #14afb7;
}

QPushButton:pressed {
    background-color: #0a5c5f;
}

QPushButton:disabled {
    background-color: #3a3a3a;
    color: #6a6a6a;
}

/* Secondary buttons */
QPushButton#secondaryBtn {
    background-color: #3a3a3a;
    color: #e0e0e0;
}

QPushButton#secondaryBtn:hover {
    background-color: #4a4a4a;
}

/* Danger buttons */
QPushButton#dangerBtn {
    background-color: #c9302c;
}

QPushButton#dangerBtn:hover {
    background-color: #d9534f;
}

/* Input fields */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 6px 10px;
    selection-background-color: #0d7377;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #0d7377;
}

QLineEdit:disabled, QTextEdit:disabled {
    background-color: #252525;
    color: #6a6a6a;
}

/* Spin boxes */
QSpinBox, QDoubleSpinBox {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 6px;
    selection-background-color: #0d7377;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #0d7377;
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    background-color: #3a3a3a;
    border-left: 1px solid #3a3a3a;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #3a3a3a;
    border-left: 1px solid #3a3a3a;
}

/* Combo box */
QComboBox {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 6px 10px;
    selection-background-color: #0d7377;
}

QComboBox:focus {
    border: 1px solid #0d7377;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(none);
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #e0e0e0;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    color: #e0e0e0;
    selection-background-color: #0d7377;
    selection-color: white;
    border: 1px solid #3a3a3a;
}

/* Date edit */
QDateEdit {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 6px 10px;
}

QDateEdit:focus {
    border: 1px solid #0d7377;
}

QDateEdit::drop-down {
    border: none;
    width: 20px;
}

QCalendarWidget {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QCalendarWidget QToolButton {
    background-color: #3a3a3a;
    color: #e0e0e0;
    border: none;
    border-radius: 3px;
    padding: 5px;
}

QCalendarWidget QToolButton:hover {
    background-color: #0d7377;
}

QCalendarWidget QAbstractItemView {
    background-color: #2d2d2d;
    selection-background-color: #0d7377;
    selection-color: white;
}

/* Tables */
QTableWidget, QTableView {
    background-color: #252525;
    alternate-background-color: #2a2a2a;
    color: #e0e0e0;
    gridline-color: #3a3a3a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    selection-background-color: #0d7377;
    selection-color: white;
}

QTableWidget::item, QTableView::item {
    padding: 5px;
    border: none;
}

QTableWidget::item:selected, QTableView::item:selected {
    background-color: #0d7377;
    color: white;
}

QHeaderView::section {
    background-color: #2d2d2d;
    color: #e0e0e0;
    padding: 8px;
    border: none;
    border-right: 1px solid #3a3a3a;
    border-bottom: 1px solid #3a3a3a;
    font-weight: bold;
    min-height: 30px;
}

QHeaderView::section:hover {
    background-color: #3a3a3a;
}

/* Scrollbars */
QScrollBar:vertical {
    background-color: #252525;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #3a3a3a;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #252525;
    height: 12px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #3a3a3a;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Labels */
QLabel {
    background-color: transparent;
    color: #e0e0e0;
    padding: 2px;
}

QLabel#titleLabel {
    font-size: 18pt;
    font-weight: bold;
    color: #0d7377;
    padding: 5px;
}

QLabel#subtitleLabel {
    font-size: 12pt;
    font-weight: bold;
    color: #e0e0e0;
    padding: 3px;
}

QLabel#sectionLabel {
    font-size: 11pt;
    font-weight: bold;
    color: #0d7377;
    padding: 5px 0px;
}

/* Group boxes */
QGroupBox {
    border: 1px solid #3a3a3a;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    color: #0d7377;
}

/* Tab widget */
QTabWidget::pane {
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    background-color: #252525;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #e0e0e0;
    padding: 8px 16px;
    border: 1px solid #3a3a3a;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #0d7377;
    color: white;
}

QTabBar::tab:hover {
    background-color: #3a3a3a;
}

/* Progress bar */
QProgressBar {
    background-color: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    text-align: center;
    color: #e0e0e0;
}

QProgressBar::chunk {
    background-color: #0d7377;
    border-radius: 3px;
}

/* Menu */
QMenuBar {
    background-color: #252525;
    color: #e0e0e0;
}

QMenuBar::item:selected {
    background-color: #0d7377;
}

QMenu {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #3a3a3a;
}

QMenu::item:selected {
    background-color: #0d7377;
}

/* Status bar */
QStatusBar {
    background-color: #252525;
    color: #e0e0e0;
    border-top: 1px solid #3a3a3a;
}

/* Tooltips */
QToolTip {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border: 1px solid #0d7377;
    padding: 5px;
    border-radius: 3px;
}

/* Check boxes and radio buttons */
QCheckBox, QRadioButton {
    color: #e0e0e0;
    spacing: 5px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #3a3a3a;
    border-radius: 3px;
    background-color: #2d2d2d;
}

QCheckBox::indicator:checked {
    background-color: #0d7377;
    border: 1px solid #0d7377;
}

QRadioButton::indicator {
    border-radius: 9px;
}

QRadioButton::indicator:checked {
    background-color: #0d7377;
    border: 1px solid #0d7377;
}

/* Splitter */
QSplitter::handle {
    background-color: #3a3a3a;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

/* Cards/Frames */
QFrame#card {
    background-color: #252525;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    padding: 15px;
}

QFrame#infoCard {
    background-color: #2d2d2d;
    border-left: 3px solid #0d7377;
    border-radius: 5px;
    padding: 10px;
}

/* Message boxes */
QMessageBox {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""

def get_dark_theme():
    """Return the dark theme stylesheet"""
    return DARK_THEME
