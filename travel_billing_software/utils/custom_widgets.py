"""
Custom Widgets for Travel Billing Software
Provides enhanced widgets with custom behaviors
"""
from PyQt6.QtWidgets import QSpinBox, QDoubleSpinBox, QComboBox
from PyQt6.QtCore import Qt


class NoWheelSpinBox(QSpinBox):
    """QSpinBox that ignores mouse wheel events to prevent accidental value changes."""
    
    def wheelEvent(self, event):
        """Override to ignore wheel events."""
        event.ignore()


class NoWheelDoubleSpinBox(QDoubleSpinBox):
    """QDoubleSpinBox that ignores mouse wheel events to prevent accidental value changes."""
    
    def wheelEvent(self, event):
        """Override to ignore wheel events."""
        event.ignore()


class NoWheelComboBox(QComboBox):
    """QComboBox that ignores mouse wheel events to prevent accidental selection changes."""
    
    def wheelEvent(self, event):
        """Override to ignore wheel events."""
        event.ignore()
