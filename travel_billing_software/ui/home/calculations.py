"""
Calculations Widget Module
Handles invoice calculations: subtotal, discount, tax, balance.
"""
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QGridLayout, QLabel, QLineEdit
)
from PyQt6.QtCore import pyqtSignal
from travel_billing_software.utils.logger import log_info, log_error, log_warning


class CalculationsWidget(QFrame):
    """
    Widget for invoice financial calculations.
    
    Features:
    - Real-time subtotal calculation
    - Discount input and application
    - Tax calculation (currently 0% but extensible)
    - Balance calculation (Total - Received)
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
        self._subtotal = 0.0
        self._discount = 0.0
        self._tax = 0.0
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
            "<b style='color:#a78bfa; font-size:16px;'>💰 Invoice Calculation</b>"
        )
        main_layout.addWidget(title)
        
        # Grid layout for calculations
        calc_grid = QGridLayout()
        calc_grid.setSpacing(15)
        
        # Styles
        label_style = f"color: {self.colors['text_primary']}; font-weight: bold;"
        
        value_style = (
            f"color: {self.colors['accent_secondary']}; font-weight: bold; "
            f"background-color: {self.colors['primary_bg']}; "
            f"padding: 8px; border-radius: 5px;"
        )
        
        input_style = (
            f"QLineEdit {{ "
            f"background-color: {self.colors['primary_bg']}; "
            f"color: {self.colors['accent_secondary']}; "
            f"border: 1px solid {self.colors['accent_secondary']}; "
            f"padding: 8px; font-weight: bold; "
            f"}}"
        )
        
        # Left column - Subtotal, Discount, Tax
        subtotal_lbl = QLabel("Subtotal:")
        subtotal_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(subtotal_lbl, 0, 0)
        
        self.lbl_subtotal = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_subtotal.setStyleSheet(value_style)
        calc_grid.addWidget(self.lbl_subtotal, 0, 1)
        
        discount_lbl = QLabel("Discount:")
        discount_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(discount_lbl, 1, 0)
        
        self.txt_discount = QLineEdit()
        self.txt_discount.setPlaceholderText("0.00")
        self.txt_discount.setText("0.00")
        self.txt_discount.setStyleSheet(input_style)
        self.txt_discount.textChanged.connect(self._on_discount_changed)
        calc_grid.addWidget(self.txt_discount, 1, 1)
        
        tax_lbl = QLabel("Tax:")
        tax_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(tax_lbl, 2, 0)
        
        self.lbl_tax = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_tax.setStyleSheet(value_style)
        calc_grid.addWidget(self.lbl_tax, 2, 1)
        
        # Spacer column
        calc_grid.setColumnMinimumWidth(2, 60)
        
        # Right column - Total, Received, Balance
        total_lbl = QLabel("Total:")
        total_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(total_lbl, 0, 5)
        
        total_style = (
            f"color: {self.colors['accent_gold']}; font-weight: bold; "
            f"background-color: {self.colors['primary_bg']}; "
            f"padding: 8px; border: 2px solid {self.colors['accent_gold']};"
        )
        self.lbl_total = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_total.setStyleSheet(total_style)
        calc_grid.addWidget(self.lbl_total, 0, 6)
        
        received_lbl = QLabel("Received:")
        received_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(received_lbl, 1, 5)
        
        received_input_style = (
            f"QLineEdit {{ "
            f"background-color: {self.colors['primary_bg']}; "
            f"color: {self.colors['success']}; "
            f"border: 1px solid {self.colors['success']}; "
            f"padding: 8px; font-weight: bold; "
            f"}}"
        )
        self.txt_received = QLineEdit()
        self.txt_received.setPlaceholderText("0.00")
        self.txt_received.setStyleSheet(received_input_style)
        self.txt_received.textChanged.connect(self._on_received_changed)
        calc_grid.addWidget(self.txt_received, 1, 6)
        
        balance_lbl = QLabel("Balance:")
        balance_lbl.setStyleSheet(label_style)
        calc_grid.addWidget(balance_lbl, 2, 5)
        
        balance_style = (
            f"color: {self.colors['danger']}; font-weight: bold; "
            f"background-color: {self.colors['primary_bg']}; "
            f"padding: 8px; border: 1px solid {self.colors['danger']};"
        )
        self.lbl_balance = QLabel(f"{self.get_currency_symbol()}0.00")
        self.lbl_balance.setStyleSheet(balance_style)
        calc_grid.addWidget(self.lbl_balance, 2, 6)
        
        main_layout.addLayout(calc_grid)
    
    def _on_discount_changed(self):
        """Handle discount input change."""
        try:
            self.calculate_totals()
        except Exception as e:
            log_error(
                "Error handling discount change",
                exception=e,
                logger_name="calculations_errors"
            )
    
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
    
    def update_subtotal(self, subtotal: float):
        """
        Update subtotal and recalculate totals.
        
        Args:
            subtotal: New subtotal amount
        """
        try:
            self._subtotal = subtotal
            self.lbl_subtotal.setText(f"{self.get_currency_symbol()}{subtotal:.2f}")
            self.calculate_totals()
            
            log_info(f"Subtotal updated: {subtotal:.2f}", "calculations")
            
        except Exception as e:
            log_error(
                f"Error updating subtotal: {subtotal}",
                exception=e,
                logger_name="calculations_errors"
            )
    
    def calculate_totals(self):
        """Calculate discount, tax, and total."""
        try:
            # Parse discount
            discount_text = self.txt_discount.text().replace('₹', '').replace(',', '').strip()
            self._discount = float(discount_text) if discount_text else 0.0
            
            # Tax calculation (currently 0%)
            self._tax = 0.0
            
            # Total
            self._total = self._subtotal - self._discount + self._tax
            
            # Update labels
            self.lbl_tax.setText(f"{self.get_currency_symbol()}{self._tax:.2f}")
            self.lbl_total.setText(f"{self.get_currency_symbol()}{self._total:.2f}")
            
            # Recalculate balance
            self.calculate_balance()
            
            log_info(
                f"Totals calculated: subtotal={self._subtotal:.2f}, "
                f"discount={self._discount:.2f}, tax={self._tax:.2f}, "
                f"total={self._total:.2f}",
                "calculations"
            )
            
        except ValueError as e:
            log_warning(
                f"Invalid discount value: {self.txt_discount.text()}",
                exception=e,
                logger_name="calculations"
            )
            self.txt_discount.setText("0.00")
            
        except Exception as e:
            log_error(
                "Error calculating totals",
                exception=e,
                logger_name="calculations_errors"
            )
    
    def calculate_balance(self):
        """Calculate balance (Total - Received) and update UI."""
        try:
            # Parse received amount
            received_text = self.txt_received.text().replace('₹', '').replace(',', '').strip()
            self._received = float(received_text) if received_text else 0.0
            
            # Calculate balance
            self._balance = self._total - self._received
            
            # Update label with color coding
            if self._balance > 0:
                # Outstanding balance (red)
                self.lbl_balance.setStyleSheet(
                    f"color: {self.colors['danger']}; font-weight: bold; "
                    f"background-color: {self.colors['primary_bg']}; "
                    f"padding: 8px; border: 1px solid {self.colors['danger']};"
                )
                self.lbl_balance.setText(f"{self.get_currency_symbol()}{self._balance:.2f}")
                
            elif self._balance < 0:
                # Overpaid (green)
                self.lbl_balance.setStyleSheet(
                    f"color: {self.colors['success']}; font-weight: bold; "
                    f"background-color: {self.colors['primary_bg']}; "
                    f"padding: 8px; border: 1px solid {self.colors['success']};"
                )
                self.lbl_balance.setText(
                    f"{self.get_currency_symbol()}{abs(self._balance):.2f} (Overpaid)"
                )
                
            else:
                # Fully paid (green)
                self.lbl_balance.setStyleSheet(
                    f"color: {self.colors['success']}; font-weight: bold; "
                    f"background-color: {self.colors['primary_bg']}; "
                    f"padding: 8px; border: 1px solid {self.colors['success']};"
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
            Dictionary with subtotal, discount, tax, total, paid, balance
        """
        try:
            return {
                "subtotal": self._subtotal,
                "discount": self._discount,
                "tax": self._tax,
                "grand_total": self._total,
                "paid_amount": self._received,
                "balance_due": self._balance
            }
        except Exception as e:
            log_error(
                "Error getting financial data",
                exception=e,
                logger_name="calculations_errors"
            )
            return {
                "subtotal": 0.0,
                "discount": 0.0,
                "tax": 0.0,
                "grand_total": 0.0,
                "paid_amount": 0.0,
                "balance_due": 0.0
            }
    
    def reset_calculations(self):
        """Reset all calculations to zero."""
        try:
            self._subtotal = 0.0
            self._discount = 0.0
            self._tax = 0.0
            self._total = 0.0
            self._received = 0.0
            self._balance = 0.0
            
            self.lbl_subtotal.setText(f"{self.get_currency_symbol()}0.00")
            self.txt_discount.setText("0.00")
            self.lbl_tax.setText(f"{self.get_currency_symbol()}0.00")
            self.lbl_total.setText(f"{self.get_currency_symbol()}0.00")
            self.txt_received.clear()
            self.lbl_balance.setText(f"{self.get_currency_symbol()}0.00")
            
            log_info("Calculations reset", "calculations")
            
        except Exception as e:
            log_error(
                "Error resetting calculations",
                exception=e,
                logger_name="calculations_errors"
            )
    
    def get_discount_widget(self):
        """Get discount input widget for tab order."""
        return self.txt_discount
    
    def get_received_widget(self):
        """Get received input widget for tab order."""
        return self.txt_received
