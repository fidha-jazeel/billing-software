"""
Items Table Widget Module
Manages the invoice items table with add/delete functionality and passport integration.
"""
from typing import Dict, List, Optional, Callable, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QPushButton, QTableWidget, QHeaderView, QLineEdit,
    QComboBox, QDoubleSpinBox, QMessageBox, QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtGui import QCursor, QKeyEvent
from travel_billing_software.utils.logger import log_info, log_error, log_warning
from travel_billing_software.utils.custom_widgets import NoWheelDoubleSpinBox
from .passport_dialog import PassportDetailsDialog
from travel_billing_software.config.config import format_currency, get_currency_symbol



class ItemsTableWidget(QFrame):
    """
    Widget for managing invoice items table.
    
    Features:
    - Add/delete rows dynamically
    - Passport details integration
    - Auto-completion for passengers
    - Keyboard navigation (Tab, Enter)
    - Real-time calculations
    
    Signals:
    - items_changed: Emitted when table data changes (for totals update)
    """
    
    items_changed = pyqtSignal()  # Signal for parent to update calculations
    
    def __init__(
        self,
        colors: dict,
        get_supplier_list: Callable,
        parent=None
    ):
        """
        Initialize items table widget.
        
        Args:
            colors: Color scheme dictionary
            get_supplier_list: Function to retrieve supplier list
            parent: Parent widget
        """
        super().__init__(parent)
        self.colors = colors
        self.get_supplier_list = get_supplier_list
        
        # Passport data store: {passenger_name: passport_data_dict}
        self.passport_data_store: Dict[str, Dict[str, Any]] = {}
        
        # Passenger history: {contact_number: [passenger_data_list]}
        self.passenger_history: Dict[str, List[Dict[str, Any]]] = {}
        
        # Current contact number for auto-completion
        self.current_contact = ""
        
        try:
            self._init_ui()
            log_info("Items table widget initialized", "items_table")
        except Exception as e:
            log_error(
                "Failed to initialize items table widget",
                exception=e,
                logger_name="items_table_errors"
            )
            raise
    
    def _init_ui(self):
        """Initialize the UI components."""
        self.setStyleSheet(
            "QFrame { "
            "background-color: #2a2a2a; border-radius: 8px; "
            "border: 1px solid #444; "
            "}"
        )
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header_layout = QHBoxLayout()
        
        table_title = QLabel("<b style='color:#a78bfa; font-size:16px;'>🧾 Billed Items</b>")
        header_layout.addWidget(table_title)
        header_layout.addStretch()
        
        self.btn_add_item = QPushButton("➕ Add Item")
        self.btn_add_item.setStyleSheet(
            f"QPushButton {{ "
            f"background-color: {self.colors['accent_primary']}; "
            f"color: white; border: none; border-radius: 5px; "
            f"padding: 10px 18px; font-weight: bold; font-size: 14px; "
            f"}} "
            f"QPushButton:hover {{ "
            f"background-color: {self.colors['accent_secondary']}; "
            f"}}"
        )
        self.btn_add_item.clicked.connect(self.add_item_row)
        self.btn_add_item.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_item.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        header_layout.addWidget(self.btn_add_item)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "Passenger Name", "PNR", "Sector", "Supplier",
            "Passport No.", "Qty", f"Supp. Amt ({get_currency_symbol()})", f"Cust. Amt ({get_currency_symbol()})", "Actions"
        ])
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Set larger header font size
        self.table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { font-size: 15px; font-weight: 600; }"
        )
        self.table.horizontalHeader().setMinimumHeight(35)
        self.table.setMinimumHeight(200)
        
        layout.addWidget(self.table)
    
    def eventFilter(self, obj: QWidget, event: QEvent) -> bool:
        """
        Event filter to handle Enter key navigation in table cells.
        
        When Enter is pressed in a table cell, move focus to the next cell
        in the same row instead of adding a new row.
        
        Args:
            obj: The object receiving the event
            event: The event
            
        Returns:
            True if event was handled, False otherwise
        """
        if event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                # Find which row and column this widget belongs to
                for row in range(self.table.rowCount()):
                    for col in range(self.table.columnCount() - 1):  # Exclude Actions column
                        widget = self.table.cellWidget(row, col)
                        if widget is obj or (hasattr(widget, 'lineEdit') and widget.lineEdit() is obj):
                            # Move to next column in same row
                            next_col = col + 1
                            if next_col < self.table.columnCount() - 1:  # Don't move to Actions column
                                next_widget = self.table.cellWidget(row, next_col)
                                if next_widget:
                                    # Handle different widget types
                                    if isinstance(next_widget, QLineEdit):
                                        next_widget.setFocus()
                                        next_widget.selectAll()
                                    elif isinstance(next_widget, QComboBox):
                                        next_widget.setFocus()
                                    elif isinstance(next_widget, (QDoubleSpinBox, NoWheelDoubleSpinBox)):
                                        next_widget.setFocus()
                                        next_widget.selectAll()
                                return True
                            return False
        return super().eventFilter(obj, event)
    
    def set_passenger_history(self, history: Dict[str, List[Dict[str, Any]]]):
        """
        Set passenger history for auto-completion.
        
        Args:
            history: Dictionary mapping contact numbers to passenger lists
        """
        try:
            self.passenger_history = history
            log_info(
                f"Passenger history set: {len(history)} contacts, "
                f"{sum(len(v) for v in history.values())} passengers",
                "items_table"
            )
        except Exception as e:
            log_error(
                "Error setting passenger history",
                exception=e,
                logger_name="items_table_errors"
            )
    
    def set_current_contact(self, contact: str):
        """
        Set current contact number for auto-completion context.
        
        Args:
            contact: Contact number
        """
        self.current_contact = contact.strip()
        log_info(f"Current contact set: {self.current_contact}", "items_table")
    
    def add_item_row(self):
        """Add a new row to the items table with all widgets."""
        try:
            table = self.table
            row = table.rowCount()
            table.insertRow(row)
            table.setRowHeight(row, 50)
            
            # Adjust table height
            self.table.setMinimumHeight(min(250 + (row * 55), 700))
            
            # Styles
            spinbox_style = (
                "QDoubleSpinBox { "
                "background-color: #2a2a2a; color: #ddd; "
                "border: 1px solid #444; border-radius: 3px; "
                "padding: 5px; font-size: 14px; "
                "} "
                "QDoubleSpinBox:focus { "
                "border: 1px solid #9b9bff; background-color: #333; "
                "}"
            )
            
            lineedit_style = (
                "QLineEdit { "
                "background-color: #2a2a2a; color: #ddd; "
                "border: 1px solid #444; border-radius: 3px; "
                "padding: 5px; font-size: 14px; "
                "} "
                "QLineEdit:focus { "
                "border: 1px solid #9b9bff; background-color: #333; "
                "}"
            )
            
            combobox_style = (
                "QComboBox { "
                "background-color: #2a2a2a; color: #ddd; "
                "border: 1px solid #444; padding: 5px; font-size: 14px; "
                "} "
                "QComboBox:focus { border: 1px solid #9b9bff; }"
            )
            
            # Create widgets
            passenger_name = QLineEdit()
            passenger_name.setPlaceholderText("Name")
            passenger_name.setStyleSheet(lineedit_style)
            passenger_name.installEventFilter(self)  # Install event filter for Enter key navigation
            self._setup_passenger_completer(passenger_name, row)
            
            pnr = QLineEdit()
            pnr.setPlaceholderText("PNR")
            pnr.setStyleSheet(lineedit_style)
            pnr.installEventFilter(self)  # Install event filter for Enter key navigation
            
            sector = QLineEdit()
            sector.setPlaceholderText("Sector")
            sector.setStyleSheet(lineedit_style)
            sector.installEventFilter(self)  # Install event filter for Enter key navigation
            
            supplier = QComboBox()
            supplier.setEditable(True)
            supplier.addItems(self.get_supplier_list())
            supplier.setStyleSheet(combobox_style)
            supplier.setObjectName(f"supplier_{row}")
            supplier.installEventFilter(self)  # Install event filter for Enter key navigation
            # Connect to handle custom supplier names
            supplier.editTextChanged.connect(lambda text, r=row: self._handle_custom_supplier(text, r))
            
            passport_number = QLineEdit()
            passport_number.setPlaceholderText("Passport No.")
            passport_number.setStyleSheet(lineedit_style)
            passport_number.installEventFilter(self)  # Install event filter for Enter key navigation
            
            qty = NoWheelDoubleSpinBox()
            qty.setMinimum(1)
            qty.setMaximum(9999)
            qty.setValue(1)
            qty.setDecimals(0)
            qty.setStyleSheet(spinbox_style)
            qty.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            qty.valueChanged.connect(self.items_changed.emit)
            qty.installEventFilter(self)  # Install event filter for Enter key navigation
            
            supplier_amount = NoWheelDoubleSpinBox()
            supplier_amount.setMinimum(0)
            supplier_amount.setMaximum(999999)
            supplier_amount.setValue(0)
            supplier_amount.setDecimals(2)
            supplier_amount.setPrefix(f"{get_currency_symbol()} ")
            supplier_amount.setStyleSheet(spinbox_style)
            supplier_amount.valueChanged.connect(self.items_changed.emit)
            supplier_amount.installEventFilter(self)  # Install event filter for Enter key navigation
            
            customer_amount = NoWheelDoubleSpinBox()
            customer_amount.setMinimum(0)
            customer_amount.setMaximum(999999)
            customer_amount.setValue(0)
            customer_amount.setDecimals(2)
            customer_amount.setPrefix(f"{get_currency_symbol()} ")
            customer_amount.setStyleSheet(spinbox_style)
            customer_amount.valueChanged.connect(self.items_changed.emit)
            customer_amount.installEventFilter(self)  # Install event filter for Enter key navigation
            
            # Actions column
            actions_widget = self._create_actions_widget(row)
            
            # Set widgets in cells
            widgets = [
                passenger_name, pnr, sector, supplier, passport_number,
                qty, supplier_amount, customer_amount, actions_widget
            ]
            
            for col, widget in enumerate(widgets):
                table.setCellWidget(row, col, widget)
            
            # Focus first field
            passenger_name.setFocus()
            
            log_info(f"Added item row #{row + 1}", "items_table")
            
        except Exception as e:
            log_error(
                f"Error adding item row",
                exception=e,
                logger_name="items_table_errors"
            )
    
    def _create_actions_widget(self, row: int) -> QWidget:
        """
        Create actions widget with passport and delete buttons.
        
        Args:
            row: Table row index
            
        Returns:
            QWidget containing action buttons
        """
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(5)
        
        # Add Passport button
        add_passport_btn = QPushButton("➕")
        add_passport_btn.setFixedWidth(40)
        add_passport_btn.setToolTip("Add Passport Details")
        add_passport_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        add_passport_btn.setStyleSheet(
            f"QPushButton {{ "
            f"background-color: {self.colors['accent_primary']}; "
            f"color: white; border: none; border-radius: 3px; "
            f"font-weight: bold; font-size: 14px; "
            f"}} "
            f"QPushButton:hover {{ background-color: #9333EA; }}"
        )
        add_passport_btn.clicked.connect(lambda: self.open_passport_dialog(row))
        actions_layout.addWidget(add_passport_btn)
        
        # Delete button
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedWidth(40)
        delete_btn.setToolTip("Delete Row")
        delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        delete_btn.setStyleSheet(
            f"QPushButton {{ "
            f"background-color: {self.colors['danger']}; "
            f"color: white; border: none; border-radius: 3px; "
            f"font-weight: bold; "
            f"}} "
            f"QPushButton:hover {{ background-color: {self.colors['accent_gold']}; }}"
        )
        delete_btn.clicked.connect(lambda: self.delete_row(row))
        actions_layout.addWidget(delete_btn)
        
        return actions_widget
    
    def _setup_passenger_completer(self, passenger_name_widget: QLineEdit, row: int):
        """
        Setup auto-complete for passenger names based on contact history.
        
        Args:
            passenger_name_widget: QLineEdit for passenger name
            row: Table row index
        """
        try:
            if not self.current_contact or self.current_contact not in self.passenger_history:
                return
            
            # Get passenger names for current contact
            passenger_names = [
                p["passenger_name"]
                for p in self.passenger_history[self.current_contact]
            ]
            
            if not passenger_names:
                return
            
            # Create completer
            completer = QCompleter(passenger_names)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
            passenger_name_widget.setCompleter(completer)
            
            # Connect to auto-fill
            completer.activated.connect(lambda text: self._autofill_passenger_data(row, text))
            
            log_info(
                f"Completer setup for row {row}: {len(passenger_names)} suggestions",
                "items_table"
            )
            
        except Exception as e:
            log_error(
                f"Error setting up completer for row {row}",
                exception=e,
                logger_name="items_table_errors"
            )
    
    def _autofill_passenger_data(self, row: int, passenger_name: str):
        """
        Auto-fill row with passenger's previous data.
        
        Args:
            row: Table row index
            passenger_name: Selected passenger name
        """
        try:
            if self.current_contact not in self.passenger_history:
                return
            
            # Find passenger data
            passenger_data = None
            for p in self.passenger_history[self.current_contact]:
                if p["passenger_name"] == passenger_name:
                    passenger_data = p
                    break
            
            if not passenger_data:
                return
            
            # Fill row with data
            self._set_cell_value(row, 1, passenger_data.get("pnr", ""))
            self._set_cell_value(row, 2, passenger_data.get("sector", ""))
            self._set_combo_value(row, 3, passenger_data.get("supplier", ""))
            self._set_cell_value(row, 4, passenger_data.get("passport_number", ""))
            self._set_spinbox_value(row, 5, passenger_data.get("qty", 1))
            self._set_spinbox_value(row, 6, passenger_data.get("supplier_amount", 0))
            self._set_spinbox_value(row, 7, passenger_data.get("amount", 0))
            
            # Restore passport data if available
            if passenger_data.get("passport_details"):
                self.passport_data_store[passenger_name] = passenger_data["passport_details"]
                
                # Auto-fill passport number
                passport_num = passenger_data["passport_details"].get("passport_number", "")
                if passport_num:
                    self._set_cell_value(row, 4, passport_num)
            
            log_info(f"Auto-filled data for passenger: {passenger_name} in row {row}", "items_table")
            
        except Exception as e:
            log_error(
                f"Error auto-filling passenger data for row {row}",
                exception=e,
                logger_name="items_table_errors"
            )
    
    def _set_cell_value(self, row: int, col: int, value: str):
        """Helper to set text in a cell widget."""
        widget = self.table.cellWidget(row, col)
        if widget and hasattr(widget, 'setText'):
            widget.setText(str(value))
    
    def _set_combo_value(self, row: int, col: int, value: str):
        """Helper to set combo box value."""
        widget = self.table.cellWidget(row, col)
        if widget and hasattr(widget, 'setCurrentText'):
            widget.setCurrentText(str(value))
    
    def _set_spinbox_value(self, row: int, col: int, value: float):
        """Helper to set spinbox value."""
        widget = self.table.cellWidget(row, col)
        if widget and hasattr(widget, 'setValue'):
            widget.setValue(float(value))
    
    def open_passport_dialog(self, row: int):
        """
        Open passport details dialog for specified row.
        
        Args:
            row: Table row index
        """
        try:
            # Get passenger name
            passenger_name_widget = self.table.cellWidget(row, 0)
            passenger_name = passenger_name_widget.text() if passenger_name_widget else "Passenger"
            
            if not passenger_name.strip():
                QMessageBox.warning(
                    self,
                    "Missing Name",
                    "Please enter passenger name before adding passport details."
                )
                return
            
            # Create and show dialog
            dialog = PassportDetailsDialog(passenger_name, self)
            dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
            result = dialog.exec()
            
            # Save data if accepted
            if result == PassportDetailsDialog.DialogCode.Accepted:
                self.passport_data_store[passenger_name] = dialog.passport_data
                
                # Auto-fill passport number in table
                passport_widget = self.table.cellWidget(row, 4)
                if passport_widget and hasattr(passport_widget, 'setText'):
                    passport_widget.setText(dialog.passport_data.get('passport_number', ''))
                
                log_info(
                    f"Passport data saved for {passenger_name}: "
                    f"Passport# {dialog.passport_data.get('passport_number')}",
                    "items_table"
                )
                
                QMessageBox.information(
                    self,
                    "Passport Saved",
                    f"Passport details saved for {passenger_name}!\n\n"
                    f"Passport Number: {dialog.passport_data.get('passport_number')}\n"
                    f"This data will be included when you save the invoice."
                )
                
        except Exception as e:
            log_error(
                f"Error opening passport dialog for row {row}",
                exception=e,
                logger_name="items_table_errors"
            )
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to open passport dialog:\n{str(e)}"
            )
    
    def delete_row(self, row: int):
        """
        Delete specified table row.
        
        Args:
            row: Table row index
        """
        try:
            self.table.removeRow(row)
            self.table.setMinimumHeight(min(250 + (self.table.rowCount() * 55), 700))
            self.items_changed.emit()
            
            log_info(f"Deleted row #{row + 1}", "items_table")
            
        except Exception as e:
            log_error(
                f"Error deleting row {row}",
                exception=e,
                logger_name="items_table_errors"
            )
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """
        Get all items from table as list of dictionaries.
        
        Returns:
            List of item dictionaries with passenger and pricing data
        """
        items = []
        
        try:
            for row in range(self.table.rowCount()):
                passenger_name = self._get_cell_text(row, 0)
                pnr = self._get_cell_text(row, 1)
                sector = self._get_cell_text(row, 2)
                supplier = self._get_combo_text(row, 3)
                passport_no = self._get_cell_text(row, 4)
                qty = self._get_spinbox_value(row, 5)
                cost_price = self._get_spinbox_value(row, 6)
                selling_price = self._get_spinbox_value(row, 7)
                
                item = {
                    "passenger_name": passenger_name,
                    "pnr": pnr,
                    "sector": sector,
                    "supplier": supplier,
                    "passport_number": passport_no,
                    "qty": qty,
                    "cost_price": cost_price,
                    "selling_price": selling_price,
                    "service_type": "Flight"
                }
                
                # Add passport details if available
                if passenger_name in self.passport_data_store:
                    item["passport_details"] = self.passport_data_store[passenger_name]
                
                items.append(item)
            
            log_info(f"Retrieved {len(items)} items from table", "items_table")
            
        except Exception as e:
            log_error(
                "Error getting items from table",
                exception=e,
                logger_name="items_table_errors"
            )
        
        return items
    
    def _get_cell_text(self, row: int, col: int) -> str:
        """Helper to get text from cell widget."""
        widget = self.table.cellWidget(row, col)
        if widget and hasattr(widget, 'text'):
            return widget.text().strip()
        return ""
    
    def _get_combo_text(self, row: int, col: int) -> str:
        """Helper to get combo box text."""
        widget = self.table.cellWidget(row, col)
        if widget and hasattr(widget, 'currentText'):
            return widget.currentText().strip()
        return ""
    
    def _get_spinbox_value(self, row: int, col: int) -> float:
        """Helper to get spinbox value."""
        widget = self.table.cellWidget(row, col)
        if widget and hasattr(widget, 'value'):
            return widget.value()
        return 0.0
    
    def clear_table(self):
        """Clear all rows from table and reset passport data."""
        try:
            self.table.setRowCount(0)
            self.passport_data_store.clear()
            self.table.setMinimumHeight(200)
            
            log_info("Table cleared", "items_table")
            
        except Exception as e:
            log_error("Error clearing table", exception=e, logger_name="items_table_errors")
    
    def get_row_count(self) -> int:
        """Get current number of rows in table."""
        return self.table.rowCount()
    
    def get_passport_data(self, passenger_name: str) -> Optional[Dict[str, Any]]:
        """
        Get passport data for specific passenger.
        
        Args:
            passenger_name: Passenger name
            
        Returns:
            Passport data dictionary or None
        """
        return self.passport_data_store.get(passenger_name)
    
    def has_passport_data(self, passenger_name: str) -> bool:
        """
        Check if passport data exists for passenger.
        
        Args:
            passenger_name: Passenger name
            
        Returns:
            True if passport data exists
        """
        return passenger_name in self.passport_data_store
    
    def _handle_custom_supplier(self, text: str, row: int):
        """
        Handle when user enters a custom supplier name.
        Prompt to add it to the Suppliers page.
        """
        from PyQt6.QtWidgets import QMessageBox
        
        if not text.strip():
            return
        
        # Check if supplier exists in current list
        existing_suppliers = self.get_supplier_list()
        if text.strip() not in existing_suppliers and text.strip():
            # Debounce - only show dialog after 1 second of no typing
            if hasattr(self, '_supplier_timer'):
                self._supplier_timer.stop()
            
            from PyQt6.QtCore import QTimer
            self._supplier_timer = QTimer()
            self._supplier_timer.setSingleShot(True)
            self._supplier_timer.timeout.connect(
                lambda: self._show_add_supplier_prompt(text.strip(), row)
            )
            self._supplier_timer.start(1000)  # 1 second delay
    
    def _show_add_supplier_prompt(self, supplier_name: str, row: int):
        """Show dialog to add custom supplier to Suppliers page."""
        from PyQt6.QtWidgets import QMessageBox
        from travel_billing_software.database.db_manager import get_db_instance
        
        # Check again if supplier exists (user might have typed existing name)
        existing_suppliers = self.get_supplier_list()
        if supplier_name in existing_suppliers:
            return
        
        reply = QMessageBox.question(
            self.table,
            "Add New Supplier",
            f"Supplier '{supplier_name}' is not in your supplier list.\n\n"
            f"Would you like to add it to your Suppliers directory?\n\n"
            f"You can add phone and other details from the Suppliers page later.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                db = get_db_instance()
                contact_id = db.add_contact(
                    'SUPPLIER',
                    supplier_name,
                    phone='',  # Can be added later from Suppliers page
                    email='',
                    company_name='',
                    address='',
                    gstin='',
                    opening_balance=0
                )
                
                if contact_id > 0:
                    QMessageBox.information(
                        self.table,
                        "Success",
                        f"Supplier '{supplier_name}' has been added!\n\n"
                        f"You can update phone and other details from the Suppliers page."
                    )
                    # Refresh the supplier dropdown for this row
                    supplier_combo = self.table.cellWidget(row, 3)  # Column 3 is Supplier
                    if supplier_combo:
                        current_text = supplier_combo.currentText()
                        supplier_combo.clear()
                        supplier_combo.addItems(self.get_supplier_list())
                        supplier_combo.setCurrentText(current_text)
                else:
                    QMessageBox.warning(
                        self.table,
                        "Error",
                        f"Failed to add supplier '{supplier_name}'. Please try again."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self.table,
                    "Error",
                    f"Failed to add supplier:\n{str(e)}"
                )
    
    def refresh_supplier_dropdowns(self):
        """Refresh all supplier dropdowns in the table."""
        for row in range(self.table.rowCount()):
            supplier_combo = self.table.cellWidget(row, 3)  # Column 3 is Supplier
            if supplier_combo:
                current_text = supplier_combo.currentText()
                supplier_combo.blockSignals(True)
                supplier_combo.clear()
                supplier_combo.addItems(self.get_supplier_list())
                supplier_combo.setCurrentText(current_text)
                supplier_combo.blockSignals(False)
