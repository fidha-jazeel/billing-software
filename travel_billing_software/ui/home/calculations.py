"""
Calculations Widget Module
Handles invoice calculations: total, paid, balance.
"""
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox
)
from PyQt6.QtCore import pyqtSignal
from travel_billing_software.utils.logger import log_info, log_error, log_warning


class CalculationsWidget(QFrame):
    """
    Widget for invoice financial calculations.
    
    Features:
    - Payment mode selection
    - Total display
    - Paid amount input
    - Balance calculation (Total - Paid)
    - Visual feedback for payment status
    
    Signals:
    - None (calculations are passive, triggered by parent)
    """
    
    def __init__(
        self,
        colors: dict,
        get_currency_symbol: callable,
        parent=None
    ):
        """
        Initialize calculations widget.
        
        Args:
            colors: Color scheme dictionary
            get_currency_symbol: Function to get currency symbol
            parent: Parent widget
        """
        super().__init__(parent)
        self.colors = colors
        self.get_currency_symbol = get_currency_symbol
        
        # Current values
        self._total = 0.0
        self._received = 0.0
        self._balance = 0.0
        
        try:
            self._init_ui()
            log_info("Calculations widget initialized", "calculations")
        except Exception as e:
            log_error(
                "Failed to initialize calculations widget",
                exception=e,
                logger_name="calculations_errors"
            )
            raise
    
    def _init_ui(self):
        """Initialize the UI components."""
        self.setStyleSheet(
            f"QFrame {{ "
            f"background-color: {self.colors['secondary_bg']}; "
            f"border-radius: 8px; "
            f"border: 1px solid {self.colors['accent_primary']}; "
            f"padding: 10px; "
            f"}}"
        )
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title = QLabel(
            "<b style='color:#a78bfa; font-size:18px;'>💰 Invoice Calculation</b>"
        )
        main_layout.addWidget(title)
        
        # Grid layout for calculations
        calc_grid = QGridLayout()
        calc_grid.setHorizontalSpacing(20)  # Equal spacing between columns
        calc_grid.setVerticalSpacing(10)    # Equal spacing between rows
        
        # Uniform dimensions for all components
        FIELD_WIDTH = 250
        FIELD_HEIGHT = 20
        
        # Styles - All uniform
        label_style = (
            f"color: {self.colors['text_primary']}; "
            f"font-weight: bold; "
            f"font-size: 15px;"
        )
        
        # Unified style for all input fields with same dimensions
        unified_field_style = (
            f"background-color: {self.colors['primary_bg']}; "
            f"border-radius: 5px; "
            f"padding: 10px; "
            f"font-weight: bold; "
            f"font-size: 15px; "
            f"min-width: {FIELD_WIDTH}px; "
            f"max-width: {FIELD_WIDTH}px; "
            f"min-height: {FIELD_HEIGHT}px; "
            f"max-height: {FIELD_HEIGHT}px; "
        )
        
        input_style = (
            f"QLineEdit {{ "
            f"{unified_field_style}"
            f"color: {self.colors['success']}; "
            f"border: 2px solid {self.colors['success']}; "
            f"}}"
        )
        
        combobox_style = (
            f"QComboBox {{ "
            f"{unified_field_style}"
            f"color: {self.colors['text_secondary']}; "
            f"border: 2px solid {self.colors['border_primary']}; "
            f"}} "
            f"QComboBox:focus {{ "
            f"border: 2px solid {self.colors['border_focus']}; "
            f"}} "
            f"QComboBox::drop-down {{ "
            f"border: none; "
            f"background-color: {self.colors['accent_primary']}; "
            f"width: 25px; "
            f"}} "
            f"QComboBox QAbstractItemView {{ "
            f"background-color: {self.colors['secondary_bg']}; "
            f"color: {self.colors['text_secondary']}; "
            f"selection-background-color: {self.colors['accent_primary']}; "
            f"border: 1px solid {self.colors['border_primary']}; "
            f"font-size: 15px; "
            f"}}"
        )
        
        total_style = (
            f"color: {self.colors['accent_gold']}; "
            f"border: 2px solid {self.colors['accent_gold']}; "
            f"{unified_field_style}"
        )
        
        balance_style = (
            f"color: {self.colors['danger']}; "
            f"border: 2px solid {self.colors['danger']}; "
            f"{unified_field_style}"
        )
        
        # Row 0, Column 0: Paid
        paid_lbl = QLabel("Paid:")
        paid_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(paid_lbl, 0, 0)
        
        self.txt_received = QLineEdit()
        self.txt_received.textChanged.connect(self.calculate_balance)
        self.txt_received.setPlaceholderText("0.00")
        self.txt_received.setStyleSheet(input_style)
        self.txt_received.textChanged.connect(self._on_received_changed)
        calc_grid.addWidget(self.txt_received, 0, 1)
        
        # Row 0, Column 1: Total
        total_lbl = QLabel("Total:")
        total_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(total_lbl, 0, 2)
        
        self.lbl_total = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_total.setStyleSheet(total_style)
        calc_grid.addWidget(self.lbl_total, 0, 3)
        
        # Row 1, Column 0: Payment Mode
        payment_mode_lbl = QLabel("Payment Mode:")
        payment_mode_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(payment_mode_lbl, 1, 0)
        
        self.payment_mode = QComboBox()
        self.payment_mode.addItems(["Cash", "Bank Transfer", "Card", "Google Pay", "Other"])
        self.payment_mode.setStyleSheet(combobox_style)
        calc_grid.addWidget(self.payment_mode, 1, 1)
        
        # Row 1, Column 1: Balance
        balance_lbl = QLabel("Balance:")
        balance_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(balance_lbl, 1, 2)
        
        self.lbl_balance = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_balance.setStyleSheet(balance_style)
        calc_grid.addWidget(self.lbl_balance, 1, 3)
        
        main_layout.addLayout(calc_grid)
    
    def _on_received_changed(self):
        """Handle received amount input change."""
        try:
            self.calculate_balance()
        except Exception as e:
            log_error(
                "Error handling received amount change",
                exception=e,
                logger_name="calculations_errors"
            )
    
    def update_total(self, total: float):
        """
        Update total from items table.
        
        Args:
            total: New total amount
        """
        try:
            self._total = total
            self.lbl_total.setText(f"{self.get_currency_symbol()}{total:.2f}")
            self.calculate_balance()
            
            log_info(f"Total updated: {total:.2f}", "calculations")
            
        except Exception as e:
            log_error(
                f"Error updating total: {total}",
                exception=e,
                logger_name="calculations_errors"
            )
    
    def calculate_balance(self):
        """Calculate balance (Total - Received) and update UI."""
        try:
            # Parse received amount
            received_text = self.txt_received.text().replace(f'{self.get_currency_symbol()}', '').replace(',', '').strip()
            self._received = float(received_text) if received_text else 0.0
            
            # Calculate balance
            self._balance = self._total - self._received
            
            # Uniform dimensions for all fields
            FIELD_WIDTH = 250
            FIELD_HEIGHT = 45
            
            # Base unified style
            unified_field_style = (
                f"background-color: {self.colors['primary_bg']}; "
                f"border-radius: 5px; "
                f"padding: 10px; "
                f"font-weight: bold; "
                f"font-size: 15px; "
                f"min-width: {FIELD_WIDTH}px; "
                f"max-width: {FIELD_WIDTH}px; "
                f"min-height: {FIELD_HEIGHT}px; "
                f"max-height: {FIELD_HEIGHT}px; "
            )
            
            # Update label with color coding
            if self._balance > 0:
                # Outstanding balance (red)
                self.lbl_balance.setStyleSheet(
                    f"color: {self.colors['danger']}; "
                    f"border: 2px solid {self.colors['danger']}; "
                    f"{unified_field_style}"
                )
                self.lbl_balance.setText(f"{self.get_currency_symbol()}{self._balance:.2f}")
                
            elif self._balance < 0:
                # Overpaid (green)
                self.lbl_balance.setStyleSheet(
                    f"color: {self.colors['success']}; "
                    f"border: 2px solid {self.colors['success']}; "
                    f"{unified_field_style}"
                )
                self.lbl_balance.setText(
                    f"{self.get_currency_symbol()}{abs(self._balance):.2f} (Overpaid)"
                )
                
            else:
                # Fully paid (green)
                self.lbl_balance.setStyleSheet(
                    f"color: {self.colors['success']}; "
                    f"border: 2px solid {self.colors['success']}; "
                    f"{unified_field_style}"
                )
                self.lbl_balance.setText(f"{self.get_currency_symbol()}0.00 (Paid)")
            
            log_info(
                f"Balance calculated: total={self._total:.2f}, "
                f"received={self._received:.2f}, balance={self._balance:.2f}",
                "calculations"
            )
            
        except ValueError as e:
            log_warning(
                f"Invalid received amount: {self.txt_received.text()}",
                exception=e,
                logger_name="calculations"
            )
            self.lbl_balance.setText(f"{self.get_currency_symbol()}0.00")
            
        except Exception as e:
            log_error(
                "Error calculating balance",
                exception=e,
                logger_name="calculations_errors"
            )
    
    def get_financial_data(self) -> dict:
        """
        Get all financial calculations.
        
        Returns:
            Dictionary with total, paid, balance, payment_mode
        """
        try:
            log_info(f"[DEBUG] get_financial_data: paid_amount={self._received}, payment_mode={self.payment_mode.currentText()}", "calculations")
            return {
                "grand_total": self._total,
                "paid_amount": self._received,
                "balance_due": self._balance,
                "payment_mode": self.payment_mode.currentText()
            }
        except Exception as e:
            log_error(
                "Error getting financial data",
                exception=e,
                logger_name="calculations_errors"
            )
            return {
                "grand_total": 0.0,
                "paid_amount": 0.0,
                "balance_due": 0.0,
                "payment_mode": "Cash"
            }
    
    def reset_calculations(self):
        """Reset all calculations to zero."""
        try:
            self._total = 0.0
            self._received = 0.0
            self._balance = 0.0
            
            self.lbl_total.setText(f"{self.get_currency_symbol()}0.00")
            self.txt_received.clear()
            self.lbl_balance.setText(f"{self.get_currency_symbol()}0.00")
            self.payment_mode.setCurrentIndex(0)
            
            log_info("Calculations reset", "calculations")
            
        except Exception as e:
            log_error(
                "Error resetting calculations",
                exception=e,
                logger_name="calculations_errors"
            )
    
    def get_received_widget(self):
        """Get received input widget for tab order."""
        return self.txt_received
    
    def get_payment_mode_widget(self):
        # Get payment mode widget for tab order
        return self.payment_mode
    
    def refresh_ui(self):
        """Refresh UI elements like currency symbols in labels."""
        try:
            # Get current currency symbol
            currency = self.get_currency_symbol()
            
            # Update all labels with current values but new currency symbol
            self.lbl_total.setText(f"{currency}{self._total:.2f}")
            self.lbl_balance.setText(f"{currency}{self._balance:.2f}")
            
            # Update placeholder for received input
            self.txt_received.setPlaceholderText(f"{currency}0.00")
            
            log_info("Calculations UI refreshed", "calculations")
            
        except Exception as e:
            log_error(
                "Error refreshing calculations UI",
                exception=e,
                logger_name="calculations_errors"
            )
