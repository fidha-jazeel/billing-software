"""
Custom Widgets for Travel Billing Software
Provides enhanced widgets with custom behaviors
"""
from PyQt6.QtWidgets import QSpinBox, QDoubleSpinBox, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette


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


class PlaceholderDoubleSpinBox(QDoubleSpinBox):
    """
    QDoubleSpinBox with placeholder functionality.
    Shows placeholder text when value is 0 and not focused.
    Clears to empty on focus if value is 0.
    Ignores mouse wheel events.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._placeholder_text = "0.00"
        self._is_focused = False
        
    def wheelEvent(self, event):
        """Override to ignore wheel events."""
        event.ignore()
    
    def focusInEvent(self, event):
        """Clear if value is 0 when focused."""
        super().focusInEvent(event)
        self._is_focused = True
        if self.value() == 0:
            self.clear()
    
    def focusOutEvent(self, event):
        """Set to 0 if empty when focus lost."""
        super().focusOutEvent(event)
        self._is_focused = False
        if self.text().strip() == "" or self.text().strip() == self.prefix().strip():
            self.setValue(0)
    
    def textFromValue(self, value):
        """Show empty text when value is 0 and not focused."""
        if value == 0 and not self._is_focused:
            return ""
        return super().textFromValue(value)


class NoWheelComboBox(QComboBox):
    """QComboBox that ignores mouse wheel events to prevent accidental selection changes."""
    
    def wheelEvent(self, event):
        """Override to ignore wheel events."""
        event.ignore()
