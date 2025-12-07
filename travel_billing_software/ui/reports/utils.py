"""
Utility Functions for Reports Module
Provides table configuration, filtering, export, and UI helpers.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import (
    QTableWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QDateEdit, QComboBox, QPushButton, QHeaderView,
    QMessageBox, QFileDialog, QWidget
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from travel_billing_software.utils.logger import log_info, log_error, log_warning


class TableConfigurator:
    """
    Handles table widget configuration with consistent styling.
    
    Provides methods for:
    - Setting up sortable headers
    - Configuring column widths
    - Applying consistent visual styles
    """
    
    @staticmethod
    def configure_table(table: QTableWidget, column_widths: Optional[Dict[int, Any]] = None):
        """
        Configure table with proper sizing, sorting, and styling.
        
        Args:
            table: QTableWidget to configure
            column_widths: Dict mapping column index to width (None for auto-resize)
                          Use 'stretch' for QHeaderView.Stretch mode
                          Use int for fixed pixel width
        """
        # Enable sorting
        table.setSortingEnabled(True)
        
        # Configure header
        header = table.horizontalHeader()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #000000;
                color: #FFFFFF;
                padding: 12px 8px;
                border: 1px solid #777777;
                border-bottom: 1px solid #777777;
                font-weight: 600;
                font-size: 15px;
                text-align: left;
            }
            QHeaderView::section:hover {
                background-color: #222222;
            }
        """)
        header.setMinimumHeight(35)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Make header sticky and non-movable
        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        header.setHighlightSections(True)
        
        # Set column widths if provided
        if column_widths:
            for col, width in column_widths.items():
                if width == 'stretch':
                    header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
                elif isinstance(width, int):
                    table.setColumnWidth(col, width)
                    header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        
        log_info(f"Table configured with {table.columnCount()} columns", 'billing_app')


class ReportFilters:
    """
    Manages filter creation and application for reports.
    
    Provides unified filtering UI components and logic for:
    - Date range filtering
    - Contact/customer search
    - Passenger name search
    - Sector filtering
    - Supplier filtering
    - Booking type filtering
    """
    
    def __init__(self, colors: dict, get_button_style: callable):
        """
        Initialize filter manager.
        
        Args:
            colors: Color scheme dictionary
            get_button_style: Function to get button stylesheet
        """
        self.colors = colors
        self.get_button_style = get_button_style
        
        # Filter widgets - will be created in create_filter_section()
        self.filter_from_date = None
        self.filter_to_date = None
        self.filter_contact = None
        self.filter_passenger = None
        self.filter_sector = None
        self.filter_supplier = None
        self.filter_type = None
    
    def create_filter_section(self, apply_callback: callable, clear_callback: callable) -> QFrame:
        """
        Create comprehensive filter section with all controls (collapsible).
        
        Args:
            apply_callback: Function to call when Apply button clicked
            clear_callback: Function to call when Clear button clicked
            
        Returns:
            QFrame containing all filter controls
        """
        filter_frame = QFrame()
        filter_frame.setStyleSheet("""
            QFrame {
                background-color: #0F0F0F;
                border-radius: 8px;
                border: 2px solid #777777;
                padding: 0px;
                margin: 0px;
            }
        """)
        
        filter_layout = QVBoxLayout(filter_frame)
        filter_layout.setSpacing(10)
        filter_layout.setContentsMargins(14, 14, 14, 14)
        
        # Title with toggle button
        title_layout = QHBoxLayout()
        filter_title = QLabel("🔍 Filter Options")
        filter_title.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 0.5px;
                padding: 8px;
                margin: 0px;
                border: none;
                background-color: transparent;
            }
        """)
        title_layout.addWidget(filter_title)
        
        toggle_btn = QPushButton("▼ Expand")
        toggle_btn.setStyleSheet("""
            QPushButton {
                color: #FFFFFF;
                background-color: #1A1A1A;
                border: 1px solid #777777;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2A2A2A;
            }
        """)
        toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        title_layout.addWidget(toggle_btn)
        
        title_container = QFrame()
        title_container.setStyleSheet("""
            QFrame {
                background-color: #1A1A1A;
                border: 1px solid #777777;
                border-radius: 4px;
                padding: 0px;
                margin: 0px 0px 10px 0px;
            }
        """)
        title_container.setLayout(title_layout)
        filter_layout.addWidget(title_container)
        
        # Collapsible content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Date Range
        date_row = QHBoxLayout()
        date_row.setSpacing(10)
        
        from_label = QLabel("From:")
        from_label.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        date_row.addWidget(from_label)
        
        self.filter_from_date = QDateEdit()
        self.filter_from_date.setCalendarPopup(True)
        self.filter_from_date.setDate(QDate.currentDate().addMonths(-1))
        self.filter_from_date.setStyleSheet(self._get_dateedit_style())
        date_row.addWidget(self.filter_from_date)
        
        to_label = QLabel("To:")
        to_label.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        date_row.addWidget(to_label)
        
        self.filter_to_date = QDateEdit()
        self.filter_to_date.setCalendarPopup(True)
        self.filter_to_date.setDate(QDate.currentDate())
        self.filter_to_date.setStyleSheet(self._get_dateedit_style())
        date_row.addWidget(self.filter_to_date)
        
        content_layout.addLayout(date_row)
        
        # Contact Number
        contact_row = self._create_input_row("Contact:", "Search by contact number...")
        self.filter_contact = contact_row['input']
        content_layout.addLayout(contact_row['layout'])
        
        # Passenger Name
        passenger_row = self._create_input_row("Passenger:", "Search by passenger name...")
        self.filter_passenger = passenger_row['input']
        content_layout.addLayout(passenger_row['layout'])
        
        # Sector and Supplier
        sector_supplier_row = QHBoxLayout()
        sector_supplier_row.setSpacing(10)
        
        sector_section = self._create_input_row("Sector:", "Search by sector...")
        self.filter_sector = sector_section['input']
        sector_supplier_row.addLayout(sector_section['layout'])
        
        supplier_section = self._create_combo_row(
            "Supplier:",
            ["All", "IndiGo", "Air India", "SpiceJet", "Vistara", "AirAsia", "Other"]
        )
        self.filter_supplier = supplier_section['combo']
        sector_supplier_row.addLayout(supplier_section['layout'])
        
        content_layout.addLayout(sector_supplier_row)
        
        # Booking Type
        type_section = self._create_combo_row(
            "Type:",
            ["All", "Flight", "Hotel", "Visa", "Tour Package", "Insurance", "Other"]
        )
        self.filter_type = type_section['combo']
        content_layout.addLayout(type_section['layout'])
        
        # Apply and Clear buttons
        btn_row = QHBoxLayout()
        
        apply_btn = QPushButton("✓ Apply Filters")
        apply_btn.setStyleSheet(self.get_button_style('add'))
        apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        apply_btn.clicked.connect(apply_callback)
        btn_row.addWidget(apply_btn)
        
        clear_btn = QPushButton("✕ Clear")
        clear_btn.setStyleSheet(self.get_button_style('delete'))
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(clear_callback)
        btn_row.addWidget(clear_btn)
        
        content_layout.addLayout(btn_row)
        
        # Initially hide content (collapsed state)
        content_widget.setVisible(False)
        filter_layout.addWidget(content_widget)
        
        # Connect toggle button
        def toggle_filters():
            is_visible = content_widget.isVisible()
            content_widget.setVisible(not is_visible)
            toggle_btn.setText("▲ Collapse" if not is_visible else "▼ Expand")
        
        toggle_btn.clicked.connect(toggle_filters)
        
        # Store widget references as properties of the filter_frame for later retrieval
        filter_frame.filter_from_date = self.filter_from_date
        filter_frame.filter_to_date = self.filter_to_date
        filter_frame.filter_contact = self.filter_contact
        filter_frame.filter_passenger = self.filter_passenger
        filter_frame.filter_sector = self.filter_sector
        filter_frame.filter_supplier = self.filter_supplier
        filter_frame.filter_type = self.filter_type
        
        log_info("Filter section created (collapsible)", 'billing_app')
        return filter_frame
    
    def _create_input_row(self, label_text: str, placeholder: str) -> Dict[str, Any]:
        """Create bordered label and input field row."""
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)
        
        # Label box
        label_box = QFrame()
        label_box.setStyleSheet("""
            QFrame {
                background-color: #121212;
                border: 1px solid #777777;
                border-radius: 5px;
                padding: 6px 10px;
            }
        """)
        label_layout = QHBoxLayout(label_box)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(label_text)
        label.setStyleSheet("color: #FFFFFF; font-weight: bold; background: transparent; border: none;")
        label_layout.addWidget(label)
        row_layout.addWidget(label_box)
        
        # Input box
        input_box = QFrame()
        input_box.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border: 1px solid #777777;
                border-radius: 5px;
                padding: 6px 10px;
            }
        """)
        input_layout = QHBoxLayout(input_box)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                padding: 2px;
            }
            QLineEdit::placeholder {
                color: #CCCCCC;
            }
            QLineEdit:focus {
                outline: none;
                border: none;
            }
        """)
        input_layout.addWidget(input_field)
        row_layout.addWidget(input_box, 1)
        
        return {'layout': row_layout, 'input': input_field}
    
    def _create_combo_row(self, label_text: str, items: List[str]) -> Dict[str, Any]:
        """Create bordered label and combobox row."""
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)
        
        # Label box
        label_box = QFrame()
        label_box.setStyleSheet("""
            QFrame {
                background-color: #121212;
                border: 1px solid #777777;
                border-radius: 5px;
                padding: 6px 10px;
            }
        """)
        label_layout = QHBoxLayout(label_box)
        label_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(label_text)
        label.setStyleSheet("color: #FFFFFF; font-weight: bold; background: transparent; border: none;")
        label_layout.addWidget(label)
        row_layout.addWidget(label_box)
        
        # Combo box
        combo_frame = QFrame()
        combo_frame.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border: 1px solid #777777;
                border-radius: 5px;
                padding: 6px 10px;
            }
        """)
        combo_layout = QHBoxLayout(combo_frame)
        combo_layout.setContentsMargins(0, 0, 0, 0)
        
        combo = QComboBox()
        combo.addItems(items)
        combo.setStyleSheet("""
            QComboBox {
                background-color: transparent;
                color: #FFFFFF;
                border: none;
                padding: 2px;
            }
            QComboBox::drop-down {
                border: none;
                background-color: transparent;
            }
            QComboBox QAbstractItemView {
                background-color: #1A1A1A;
                color: #FFFFFF;
                selection-background-color: #333333;
                border: 1px solid #777777;
            }
            QComboBox:focus {
                outline: none;
                border: none;
            }
        """)
        combo_layout.addWidget(combo)
        row_layout.addWidget(combo_frame, 1)
        
        return {'layout': row_layout, 'combo': combo}
    
    def _get_dateedit_style(self) -> str:
        """Get stylesheet for QDateEdit widgets."""
        return """
            QDateEdit {
                background-color: #1A1A1A;
                color: #FFFFFF;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QDateEdit::drop-down {
                border: none;
                background-color: #1A1A1A;
            }
        """
    
    def apply_filters(self, invoices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply current filter values to invoice list.
        
        Args:
            invoices: List of invoice dictionaries
            
        Returns:
            Filtered list of invoices
        """
        try:
            filtered = []
            
            from_date = self.filter_from_date.date().toPyDate()
            to_date = self.filter_to_date.date().toPyDate()
            contact = self.filter_contact.text().lower()
            passenger = self.filter_passenger.text().lower()
            sector = self.filter_sector.text().lower()
            supplier = self.filter_supplier.currentText()
            booking_type = self.filter_type.currentText()
            
            log_info(
                f"Applying filters - Date: {from_date} to {to_date}, "
                f"Contact: '{contact}', Passenger: '{passenger}', Sector: '{sector}', "
                f"Supplier: '{supplier}', Type: '{booking_type}'",
                'billing_app'
            )
            
            for invoice in invoices:
                try:
                    # Date filter
                    try:
                        date_str = invoice.get('invoice_date', '')
                        if date_str:
                            day, month, year = map(int, date_str.split('/'))
                            invoice_date = datetime(year, month, day).date()
                            if not (from_date <= invoice_date <= to_date):
                                continue
                    except Exception as date_error:
                        log_warning(
                            f"Date parsing error for invoice {invoice.get('invoice_number', 'Unknown')}: "
                            f"{date_error}",
                            'billing_app'
                        )
                        pass
                    
                    # Contact filter
                    if contact and contact not in invoice.get('customer_phone', '').lower():
                        continue
                    
                    # Booking type filter
                    if booking_type != "All":
                        tickets = invoice.get('tickets', [])
                        if not any(ticket.get('booking_type', '') == booking_type for ticket in tickets):
                            continue
                    
                    # Passenger, sector, supplier filters
                    if passenger or sector or supplier != "All":
                        match_found = False
                        tickets = invoice.get('tickets', [])
                        passengers_list = invoice.get('passengers', [])
                        
                        for ticket in tickets:
                            if passenger:
                                for pax in passengers_list:
                                    if passenger in pax.get('name', '').lower():
                                        match_found = True
                                        break
                            if sector and sector in ticket.get('sector', '').lower():
                                match_found = True
                            if supplier != "All" and supplier == ticket.get('supplier_name', ''):
                                match_found = True
                            if match_found:
                                break
                        
                        if not match_found and (passenger or sector or supplier != "All"):
                            continue
                    
                    filtered.append(invoice)
                    
                except Exception as invoice_error:
                    log_error(
                        f"Error filtering invoice {invoice.get('invoice_number', 'Unknown')}",
                        exception=invoice_error,
                        logger_name='billing_errors'
                    )
                    continue
            
            log_info(f"Filter applied - {len(filtered)} records matched out of {len(invoices)}", 'billing_app')
            return filtered
            
        except Exception as e:
            log_error("Error applying filters", exception=e, logger_name='billing_errors')
            return []
    
    def clear_filters(self):
        """Reset all filter values to defaults."""
        try:
            log_info("Clearing all filters", 'billing_app')
            
            self.filter_from_date.setDate(QDate.currentDate().addMonths(-1))
            self.filter_to_date.setDate(QDate.currentDate())
            self.filter_contact.clear()
            self.filter_passenger.clear()
            self.filter_sector.clear()
            self.filter_supplier.setCurrentIndex(0)
            self.filter_type.setCurrentIndex(0)
            
            log_info("Filters cleared successfully", 'billing_app')
            
        except Exception as e:
            log_error("Error clearing filters", exception=e, logger_name='billing_errors')
            raise


class ReportExporter:
    """Handles exporting reports to various formats (Excel, PDF)."""
    
    @staticmethod
    def export_to_excel(table: QTableWidget, report_name: str, parent_widget: QWidget):
        """
        Export table data to Excel (.xlsx) file with proper formatting.
        
        Args:
            table: QTableWidget containing report data
            report_name: Name of the report for filename
            parent_widget: Parent widget for dialogs
        """
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
            from openpyxl.utils import get_column_letter
            
            filename, _ = QFileDialog.getSaveFileName(
                parent_widget,
                f"Export {report_name} Report",
                f"{report_name.lower().replace(' ', '_')}_report.xlsx",
                "Excel Files (*.xlsx);;All Files (*.*)"
            )
            
            if not filename:
                return
            
            # Ensure .xlsx extension
            if not filename.endswith('.xlsx'):
                filename += '.xlsx'
            
            # Create workbook and worksheet
            wb = Workbook()
            ws = wb.active
            ws.title = report_name[:31]  # Excel sheet name limit
            
            # Define styles
            header_font = Font(name='Calibri', size=12, bold=True, color='FFFFFF')
            header_fill = PatternFill(start_color='000000', end_color='000000', fill_type='solid')
            header_alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            
            data_font = Font(name='Calibri', size=11)
            data_alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            
            thin_border = Border(
                left=Side(style='thin', color='CCCCCC'),
                right=Side(style='thin', color='CCCCCC'),
                top=Side(style='thin', color='CCCCCC'),
                bottom=Side(style='thin', color='CCCCCC')
            )
            
            # Write headers
            headers = []
            for col in range(table.columnCount()):
                header_item = table.horizontalHeaderItem(col)
                header_text = header_item.text() if header_item else f"Column {col + 1}"
                headers.append(header_text)
                
                cell = ws.cell(row=1, column=col + 1, value=header_text)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
                cell.border = thin_border
            
            # Set header row height
            ws.row_dimensions[1].height = 25
            
            # Write data rows
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    cell_value = item.text() if item else ''
                    
                    # Try to convert to number for better Excel formatting
                    if cell_value.startswith('₹'):
                        # Remove currency symbol and commas for numeric values
                        numeric_value = cell_value.replace('₹', '').replace(',', '').strip()
                        try:
                            cell_value = float(numeric_value)
                        except ValueError:
                            pass  # Keep as string if conversion fails
                    
                    cell = ws.cell(row=row + 2, column=col + 1, value=cell_value)
                    cell.font = data_font
                    cell.alignment = data_alignment
                    cell.border = thin_border
                    
                    # Format currency cells
                    if isinstance(cell_value, (int, float)):
                        cell.number_format = '₹#,##0.00'
            
            # Auto-adjust column widths
            for col in range(1, table.columnCount() + 1):
                column_letter = get_column_letter(col)
                max_length = 0
                
                # Check header length
                header_length = len(str(headers[col - 1]))
                max_length = max(max_length, header_length)
                
                # Check data length (sample first 100 rows for performance)
                for row in range(2, min(102, ws.max_row + 1)):
                    try:
                        cell_value = ws.cell(row=row, column=col).value
                        if cell_value:
                            cell_length = len(str(cell_value))
                            max_length = max(max_length, cell_length)
                    except:
                        pass
                
                # Set column width (with min and max limits)
                adjusted_width = min(max(max_length + 2, 10), 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            # Freeze header row
            ws.freeze_panes = 'A2'
            
            # Save workbook
            wb.save(filename)
            
            log_info(f"Report exported to Excel: {filename}", 'billing_app')
            QMessageBox.information(
                parent_widget,
                "Success",
                f"Report exported successfully to Excel!\n\n{filename}"
            )
        
        except ImportError as e:
            log_error(f"openpyxl not installed", exception=e, logger_name='billing_errors')
            QMessageBox.critical(
                parent_widget,
                "Export Error",
                "Excel export requires 'openpyxl' package.\nPlease install it: pip install openpyxl"
            )
        except Exception as e:
            log_error(f"Failed to export report to Excel", exception=e, logger_name='billing_errors')
            QMessageBox.critical(
                parent_widget,
                "Export Error",
                f"Failed to export report to Excel:\n{str(e)}"
            )
    
    @staticmethod
    def export_to_pdf(table: QTableWidget, report_name: str, parent_widget: QWidget):
        """
        Export table data to PDF file with proper formatting.
        
        Args:
            table: QTableWidget containing report data
            report_name: Name of the report for filename
            parent_widget: Parent widget for dialogs
        """
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.pdfgen import canvas
            
            filename, _ = QFileDialog.getSaveFileName(
                parent_widget,
                f"Export {report_name} Report",
                f"{report_name.lower().replace(' ', '_')}_report.pdf",
                "PDF Files (*.pdf);;All Files (*.*)"
            )
            
            if not filename:
                return
            
            # Ensure .pdf extension
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            
            # Create PDF document (landscape for better table fit)
            doc = SimpleDocTemplate(
                filename,
                pagesize=landscape(A4),
                rightMargin=30,
                leftMargin=30,
                topMargin=30,
                bottomMargin=30
            )
            
            # Container for the 'Flowable' objects
            elements = []
            
            # Define styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#000000'),
                spaceAfter=12,
                alignment=1  # Center alignment
            )
            
            # Add title
            title = Paragraph(f"<b>{report_name} Report</b>", title_style)
            elements.append(title)
            
            # Add date
            from datetime import datetime
            date_str = datetime.now().strftime("%B %d, %Y %I:%M %p")
            date_style = ParagraphStyle(
                'DateStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#666666'),
                spaceAfter=20,
                alignment=1  # Center alignment
            )
            date_para = Paragraph(f"Generated on: {date_str}", date_style)
            elements.append(date_para)
            elements.append(Spacer(1, 0.2 * inch))
            
            # Prepare table data
            table_data = []
            
            # Headers
            headers = []
            for col in range(table.columnCount()):
                header_item = table.horizontalHeaderItem(col)
                header_text = header_item.text() if header_item else f"Column {col + 1}"
                headers.append(header_text)
            table_data.append(headers)
            
            # Data rows
            for row in range(table.rowCount()):
                row_data = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    cell_value = item.text() if item else ''
                    row_data.append(cell_value)
                table_data.append(row_data)
            
            # Create table
            if table_data:
                # Calculate column widths dynamically
                page_width = landscape(A4)[0] - 60  # Subtract margins
                num_cols = len(table_data[0])
                col_width = page_width / num_cols
                col_widths = [col_width] * num_cols
                
                pdf_table = Table(table_data, colWidths=col_widths, repeatRows=1)
                
                # Apply table style
                table_style = TableStyle([
                    # Header style
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#000000')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 0), (-1, 0), 12),
                    
                    # Data rows style
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                    
                    # Grid
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    
                    # Alternating row colors
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
                ])
                
                pdf_table.setStyle(table_style)
                elements.append(pdf_table)
            
            # Build PDF
            doc.build(elements)
            
            log_info(f"Report exported to PDF: {filename}", 'billing_app')
            QMessageBox.information(
                parent_widget,
                "Success",
                f"Report exported successfully to PDF!\n\n{filename}"
            )
        
        except ImportError as e:
            log_error(f"reportlab not installed", exception=e, logger_name='billing_errors')
            QMessageBox.critical(
                parent_widget,
                "Export Error",
                "PDF export requires 'reportlab' package.\nPlease install it: pip install reportlab"
            )
        except Exception as e:
            log_error(f"Failed to export report to PDF", exception=e, logger_name='billing_errors')
            QMessageBox.critical(
                parent_widget,
                "Export Error",
                f"Failed to export report to PDF:\n{str(e)}"
            )


class SummaryCardManager:
    """Manages summary card creation and updates."""
    
    @staticmethod
    def create_summary_cards(titles: List[str], colors: dict) -> QFrame:
        """
        Create summary cards with titles. If 6 cards, arranged in 2 rows of 3.
        
        Args:
            titles: List of card titles
            colors: Color scheme dictionary
            
        Returns:
            QFrame containing all summary cards
        """
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border-radius: 8px;
                border: 2px solid #777777;
                padding: 15px;
            }
        """)
        
        # Use grid layout if 6 cards, otherwise horizontal layout
        if len(titles) == 6:
            from PyQt6.QtWidgets import QGridLayout
            summary_layout = QGridLayout(summary_frame)
            summary_layout.setContentsMargins(15, 15, 15, 15)
            summary_layout.setSpacing(20)
            
            # Add cards in 2 rows of 3
            for i, title in enumerate(titles):
                card = SummaryCardManager._create_single_card(title, colors)
                row = i // 3  # 0 for first 3 cards, 1 for next 3
                col = i % 3   # 0, 1, 2 repeating
                summary_layout.addWidget(card, row, col)
        else:
            # Original horizontal layout for other card counts
            summary_layout = QHBoxLayout(summary_frame)
            summary_layout.setContentsMargins(15, 15, 15, 15)
            summary_layout.setSpacing(20)
            
            for title in titles:
                card = SummaryCardManager._create_single_card(title, colors)
                summary_layout.addWidget(card)
        
        return summary_frame
    
    @staticmethod
    def _create_single_card(title: str, colors: dict) -> QFrame:
        """Create a single summary card."""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #0F0F0F;
                border-radius: 8px;
                border: 2px solid #777777;
                padding: 15px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(6)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 14px;
            font-weight: bold;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)
        
        value_label = QLabel("₹0.00")
        value_label.setProperty('summary_value', True)
        value_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 24px;
            font-weight: bold;
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(value_label)
        
        return card
    
    @staticmethod
    def update_summary_cards(frame: QFrame, values: List[str]):
        """
        Update summary card values. Works with both HBoxLayout and GridLayout.
        
        Args:
            frame: Summary cards container frame
            values: List of new values to display
        """
        from PyQt6.QtWidgets import QGridLayout
        
        layout = frame.layout()
        if not layout:
            return
        
        # Handle grid layout (used for 6 cards)
        if isinstance(layout, QGridLayout):
            value_index = 0
            for row in range(layout.rowCount()):
                for col in range(layout.columnCount()):
                    if value_index >= len(values):
                        return
                    item = layout.itemAtPosition(row, col)
                    if item and item.widget():
                        card = item.widget()
                        if isinstance(card, QFrame):
                            # Find the value label in this specific card
                            for label in card.findChildren(QLabel):
                                if label.property('summary_value'):
                                    label.setText(values[value_index])
                                    break
                    value_index += 1
        else:
            # Handle horizontal layout (original behavior)
            for i in range(min(layout.count(), len(values))):
                item = layout.itemAt(i)
                if item and item.widget():
                    card = item.widget()
                    if isinstance(card, QFrame):
                        # Find the value label in this specific card
                        for label in card.findChildren(QLabel):
                            if label.property('summary_value'):
                                label.setText(values[i])
                                break


def create_report_header(title: str, description: str, colors: dict) -> QWidget:
    """
    Create consistent styled header for reports.
    
    Args:
        title: Main title text with emoji
        description: Subtitle/description
        colors: Color scheme dictionary
        
    Returns:
        QWidget containing the styled header
    """
    header_widget = QWidget()
    header_layout = QVBoxLayout(header_widget)
    header_layout.setContentsMargins(0, 0, 0, 15)
    header_layout.setSpacing(5)
    
    # Main title
    title_label = QLabel(title)
    title_label.setStyleSheet(f"""
        QLabel {{
            color: {colors['accent_primary']};
            font-size: 26px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }}
    """)
    header_layout.addWidget(title_label)
    
    # Description
    if description:
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {colors['text_secondary']};
                font-size: 14px;
                font-weight: 400;
                margin-top: 5px;
            }}
        """)
        header_layout.addWidget(desc_label)
    
    return header_widget


def show_no_records_message(parent_widget: QWidget, report_name: str):
    """
    Show informative message when no records match filters.
    (Dialog removed - now just logs the message)
    
    Args:
        parent_widget: Parent widget for dialog
        report_name: Name of the report
    """
    from travel_billing_software.utils.logger import log_info
    log_info(f"No records found for {report_name} with current filters", 'billing_app')
    # Dialog removed - table will show empty state instead
