"""
Passport Details Dialog Module
Provides a user-friendly form for entering passenger passport information.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QDateEdit, QComboBox,
    QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QCursor
from travel_billing_software.utils.logger import log_info, log_error, log_warning


class PassportDetailsDialog(QDialog):
    """
    Modal dialog for entering and validating passenger passport details.
    
    Features:
    - Validates mandatory fields before saving
    - Professional UI with card-based design
    - Auto-fills passenger name from table
    - Returns structured passport data dictionary
    """
    
    def __init__(self, passenger_name: str = "", parent=None):
        """
        Initialize passport details dialog.
        
        Args:
            passenger_name: Pre-filled passenger name from invoice table
            parent: Parent widget (for modal behavior)
        """
        super().__init__(parent)
        self.passenger_name = passenger_name
        self.passport_data = {}
        
        self.setWindowTitle(f"Passport Details - {passenger_name}")
        self.setMinimumWidth(700)
        self.setMinimumHeight(700)
        
        try:
            self._init_ui()
            log_info(f"Passport dialog opened for: {passenger_name}", "passport_dialog")
        except Exception as e:
            log_error(
                f"Failed to initialize passport dialog for {passenger_name}",
                exception=e,
                logger_name="passport_dialog_errors"
            )
            raise
    
    def _init_ui(self):
        """Initialize the user interface components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Set window background
        self.setStyleSheet("QWidget { background-color: #f5f5f5; }")
        
        # Create card frame
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e5e7eb;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel("<h2>Passport Information</h2>")
        title.setStyleSheet("color: #7C3AED; font-weight: bold;")
        card_layout.addWidget(title)
        
        # Passenger name display
        name_label = QLabel(f"<b>Passenger:</b> {self.passenger_name}")
        name_label.setStyleSheet(
            "color: #333; font-size: 14px; padding: 10px; "
            "background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 5px;"
        )
        card_layout.addWidget(name_label)
        
        # Form fields
        form_layout = self._create_form_layout()
        card_layout.addLayout(form_layout)
        
        # Mandatory fields note
        note = QLabel("<i>* Mandatory fields</i>")
        note.setStyleSheet("color: #dc2626; font-size: 12px;")
        card_layout.addWidget(note)
        
        card_layout.addStretch()
        
        # Action buttons
        btn_layout = self._create_button_layout()
        card_layout.addLayout(btn_layout)
        
        # Add card to main layout
        main_layout.addWidget(card)
    
    def _create_form_layout(self) -> QGridLayout:
        """
        Create the form grid layout with all passport fields.
        
        Returns:
            QGridLayout with all form fields
        """
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setColumnMinimumWidth(0, 220)  # Label column
        form_layout.setColumnMinimumWidth(1, 380)  # Input column
        
        # Styles
        field_style = (
            "QLineEdit { "
            "background-color: #ffffff; color: #111827; "
            "border: 1px solid #d1d5db; border-radius: 6px; "
            "padding: 10px; font-size: 16px; "
            "selection-background-color: #dbeafe; selection-color: #111827; "
            "} "
            "QLineEdit:focus { "
            "border: 2px solid #7C3AED; background-color: #ffffff; "
            "}"
        )
        
        date_style = (
            "QDateEdit { "
            "background-color: #ffffff; color: #111827; "
            "border: 1px solid #d1d5db; border-radius: 6px; "
            "padding: 10px; font-size: 16px; "
            "selection-background-color: #dbeafe; selection-color: #111827; "
            "} "
            "QDateEdit:focus { "
            "border: 2px solid #7C3AED; background-color: #ffffff; "
            "}"
        )
        
        combo_style = (
            "QComboBox { "
            "background-color: white; color: #1f2937; "
            "border: 1px solid #d1d5db; padding: 10px; "
            "border-radius: 3px; font-size: 14px; "
            "} "
            "QComboBox:focus { "
            "border: 2px solid #7C3AED; background-color: #faf5ff; "
            "} "
            "QComboBox::drop-down { border: none; } "
            "QComboBox QAbstractItemView { "
            "background-color: white; color: #1f2937; "
            "selection-background-color: #e9d5ff; font-size: 14px; "
            "}"
        )
        
        label_style = "color: #374151; font-size: 18px; font-weight: 600;"
        
        # Row 0: Passport Number *
        passport_num_label = QLabel("<b>Passport Number: *</b>")
        passport_num_label.setStyleSheet(label_style)
        form_layout.addWidget(passport_num_label, 0, 0)
        
        self.passport_number = QLineEdit()
        self.passport_number.setPlaceholderText("Enter passport number")
        self.passport_number.setStyleSheet(field_style)
        self.passport_number.setMinimumHeight(40)
        form_layout.addWidget(self.passport_number, 0, 1)
        
        # Row 1: Full Name *
        full_name_label = QLabel("<b>Full Name (as in passport): *</b>")
        full_name_label.setStyleSheet(label_style)
        form_layout.addWidget(full_name_label, 1, 0)
        
        self.full_name = QLineEdit()
        self.full_name.setText(self.passenger_name)
        self.full_name.setStyleSheet(field_style)
        self.full_name.setMinimumHeight(40)
        form_layout.addWidget(self.full_name, 1, 1)
        
        # Row 2: Date of Birth *
        dob_label = QLabel("<b>Date of Birth: *</b>")
        dob_label.setStyleSheet(label_style)
        form_layout.addWidget(dob_label, 2, 0)
        
        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDate(QDate.currentDate().addYears(-30))
        self.dob.setStyleSheet(date_style)
        self.dob.setMinimumHeight(40)
        form_layout.addWidget(self.dob, 2, 1)
        
        # Row 3: Nationality *
        nationality_label = QLabel("<b>Nationality: *</b>")
        nationality_label.setStyleSheet(label_style)
        form_layout.addWidget(nationality_label, 3, 0)
        
        self.nationality = QLineEdit()
        self.nationality.setPlaceholderText("e.g., Indian")
        self.nationality.setStyleSheet(field_style)
        self.nationality.setMinimumHeight(40)
        form_layout.addWidget(self.nationality, 3, 1)
        
        # Row 4: Gender *
        gender_label = QLabel("<b>Gender: *</b>")
        gender_label.setStyleSheet(label_style)
        form_layout.addWidget(gender_label, 4, 0)
        
        self.gender = QComboBox()
        self.gender.addItems(["Select", "Male", "Female", "Other"])
        self.gender.setStyleSheet(combo_style)
        self.gender.setMinimumHeight(40)
        form_layout.addWidget(self.gender, 4, 1)
        
        # Row 5: Place of Birth
        pob_label = QLabel("<b>Place of Birth:</b>")
        pob_label.setStyleSheet(label_style)
        form_layout.addWidget(pob_label, 5, 0)
        
        self.place_of_birth = QLineEdit()
        self.place_of_birth.setPlaceholderText("City, Country")
        self.place_of_birth.setStyleSheet(field_style)
        self.place_of_birth.setMinimumHeight(40)
        form_layout.addWidget(self.place_of_birth, 5, 1)
        
        # Row 6: Issue Date *
        issue_date_label = QLabel("<b>Issue Date: *</b>")
        issue_date_label.setStyleSheet(label_style)
        form_layout.addWidget(issue_date_label, 6, 0)
        
        self.issue_date = QDateEdit()
        self.issue_date.setCalendarPopup(True)
        self.issue_date.setDate(QDate.currentDate().addYears(-2))
        self.issue_date.setStyleSheet(date_style)
        self.issue_date.setMinimumHeight(40)
        form_layout.addWidget(self.issue_date, 6, 1)
        
        # Row 7: Expiry Date *
        expiry_date_label = QLabel("<b>Expiry Date: *</b>")
        expiry_date_label.setStyleSheet(label_style)
        form_layout.addWidget(expiry_date_label, 7, 0)
        
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate().addYears(8))
        self.expiry_date.setStyleSheet(date_style)
        self.expiry_date.setMinimumHeight(40)
        form_layout.addWidget(self.expiry_date, 7, 1)
        
        # Row 8: Issuing Authority *
        issuing_auth_label = QLabel("<b>Issuing Authority: *</b>")
        issuing_auth_label.setStyleSheet(label_style)
        form_layout.addWidget(issuing_auth_label, 8, 0)
        
        self.issuing_authority = QLineEdit()
        self.issuing_authority.setPlaceholderText("e.g., Govt. of India")
        self.issuing_authority.setStyleSheet(field_style)
        self.issuing_authority.setMinimumHeight(40)
        form_layout.addWidget(self.issuing_authority, 8, 1)
        
        return form_layout
    
    def _create_button_layout(self) -> QHBoxLayout:
        """
        Create action button layout.
        
        Returns:
            QHBoxLayout with Save and Cancel buttons
        """
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        # Save button
        save_btn = QPushButton("💾 Save Passport Details")
        save_btn.setStyleSheet(
            "QPushButton { "
            "background-color: #10B981; color: white; "
            "border: none; border-radius: 5px; "
            "padding: 10px 20px; font-weight: bold; "
            "} "
            "QPushButton:hover { background-color: #059669; }"
        )
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save_btn.clicked.connect(self.save_details)
        btn_layout.addWidget(save_btn)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            "QPushButton { "
            "background-color: #6B7280; color: white; "
            "border: none; border-radius: 5px; "
            "padding: 10px 20px; font-weight: bold; "
            "} "
            "QPushButton:hover { background-color: #4B5563; }"
        )
        cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(cancel_btn)
        
        return btn_layout
    
    def save_details(self):
        """
        Validate and save passport details.
        Shows validation errors if mandatory fields are missing.
        """
        try:
            # Validate mandatory fields
            validation_error = self._validate_fields()
            if validation_error:
                log_warning(
                    f"Passport validation failed for {self.passenger_name}: {validation_error}",
                    logger_name="passport_dialog"
                )
                QMessageBox.warning(self, "Missing Information", validation_error)
                return
            
            # Collect passport data
            self.passport_data = {
                'passport_number': self.passport_number.text().strip(),
                'full_name': self.full_name.text().strip(),
                'date_of_birth': self.dob.date().toString("yyyy-MM-dd"),
                'nationality': self.nationality.text().strip(),
                'gender': self.gender.currentText(),
                'place_of_birth': self.place_of_birth.text().strip(),
                'issue_date': self.issue_date.date().toString("yyyy-MM-dd"),
                'expiry_date': self.expiry_date.date().toString("yyyy-MM-dd"),
                'issuing_authority': self.issuing_authority.text().strip()
            }
            
            log_info(
                f"Passport details saved for {self.full_name.text()}: "
                f"Passport# {self.passport_data['passport_number']}, "
                f"Nationality: {self.passport_data['nationality']}",
                "passport_dialog"
            )
            
            QMessageBox.information(
                self,
                "Success",
                f"Passport details saved for {self.full_name.text()}!"
            )
            
            self.accept()  # Close with accepted status
            
        except Exception as e:
            log_error(
                f"Error saving passport details for {self.passenger_name}",
                exception=e,
                logger_name="passport_dialog_errors"
            )
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save passport details:\n{str(e)}"
            )
    
    def _validate_fields(self) -> str:
        """
        Validate all mandatory fields.
        
        Returns:
            str: Error message if validation fails, empty string if valid
        """
        if not self.passport_number.text().strip():
            return "Passport Number is required."
        
        if not self.full_name.text().strip():
            return "Full Name is required."
        
        if not self.nationality.text().strip():
            return "Nationality is required."
        
        if self.gender.currentText() == "Select":
            return "Please select Gender."
        
        if not self.issuing_authority.text().strip():
            return "Issuing Authority is required."
        
        # Validate date logic
        if self.issue_date.date() >= self.expiry_date.date():
            return "Expiry Date must be after Issue Date."
        
        return ""  # Valid
    
    def get_passport_data(self) -> dict:
        """
        Get the saved passport data.
        
        Returns:
            dict: Passport data dictionary
        """
        return self.passport_data
