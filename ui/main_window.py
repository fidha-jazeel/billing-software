"""
Main Window - Travel Agency Billing Software
Contains the complete dashboard with invoice creation, reports, and analytics
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QDoubleSpinBox, QStackedWidget, QComboBox, QDateEdit,
    QScrollArea, QGridLayout, QFileDialog
)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import QDate
import sys
import json
import os
from datetime import datetime

# Import configuration and utilities
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    APP_CONFIG, COMPANY_INFO, COLORS, INVOICE_CONFIG, LAYOUT_CONFIG,
    get_supplier_list, get_sector_list, get_company_info_formatted,
    get_currency_symbol, get_invoice_prefix
)
from utils.styles import (
    get_frame_style, get_label_style, get_input_style, get_dateedit_style,
    get_combobox_style, get_spinbox_style, get_button_style, get_scrollarea_style,
    get_table_style, apply_fixed_width_label, apply_minimum_width_widget
)

# Import database manager
try:
    from database import DatabaseManager, get_db_instance
    DB_ENABLED = True
except ImportError:
    DB_ENABLED = False
    print("⚠️  Database module not available. Using JSON-only mode.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing Software - Main Window")
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(QLabel("Main Window placeholder"))
        self.setCentralWidget(central)
