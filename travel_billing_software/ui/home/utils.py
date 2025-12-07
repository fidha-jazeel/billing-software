"""
Utility Functions for Home Page
Contains helpers for invoice operations, shortcuts, and PDF generation.
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import QDate
from utils.invoice_generator import generate_invoice_pdf
from travel_billing_software.utils.logger import log_info, log_error, log_warning

try:
    import pypdfium2 as pdfium
    PDFIUM_AVAILABLE = True
except ImportError:
    PDFIUM_AVAILABLE = False
    log_warning("pypdfium2 not available, print functionality will be limited", logger_name="home_utils")


class InvoiceNumberGenerator:
    """Generates unique invoice numbers with timestamp."""
    
    def __init__(self, invoice_prefix_func: callable):
        """
        Initialize invoice number generator.
        
        Args:
            invoice_prefix_func: Function that returns invoice prefix
        """
        self.get_prefix = invoice_prefix_func
    
    def generate(self) -> str:
        """
        Generate new invoice number with format: PREFIX-YYYYMMDD-HHMMSS.
        
        Returns:
            Generated invoice number string
        """
        try:
            now = datetime.now()
            invoice_number = f"{self.get_prefix()}-{now.strftime('%Y%m%d-%H%M%S')}"
            log_info(f"Generated invoice number: {invoice_number}", "invoice_utils")
            return invoice_number
        except Exception as e:
            log_error(
                "Error generating invoice number",
                exception=e,
                logger_name="invoice_utils_errors"
            )
            # Fallback to basic format
            return f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"


class PDFOperations:
    """Handles PDF generation, printing, and sharing for invoices."""
    
    def __init__(
        self,
        company_info: dict,
        invoice_config: dict,
        get_currency_symbol: callable
    ):
        """
        Initialize PDF operations.
        
        Args:
            company_info: Company information dictionary
            invoice_config: Invoice configuration dictionary
            get_currency_symbol: Function to get currency symbol
        """
        self.company_info = company_info
        self.invoice_config = invoice_config
        self.get_currency_symbol = get_currency_symbol
    
    def generate_pdf(
        self,
        invoice_number: str,
        invoice_data: Dict[str, Any],
        show_dialog: bool = True
    ) -> Optional[str]:
        """
        Generate PDF invoice.
        
        Args:
            invoice_number: Invoice number for filename
            invoice_data: Complete invoice data dictionary
            show_dialog: Whether to show success dialog
            
        Returns:
            str: Path to generated PDF, or None if failed
        """
        try:
            # Prepare output directory
            default_dir = os.path.join(os.getcwd(), "output", "invoice")
            os.makedirs(default_dir, exist_ok=True)
            
            filename = os.path.join(default_dir, f"invoice_{invoice_number}.pdf")
            
            # Prepare data for PDF generator
            pdf_data = {
                "company": {
                    "name": self.company_info["name"],
                    "address": self.company_info.get("address", ""),
                    "footer_note": self.invoice_config.get("footer_note", ""),
                    "tagline": self.company_info.get("tagline", ""),
                    "email": self.company_info.get("email", ""),
                    "phone": self.company_info.get("phone", ""),
                    "gst_number": self.company_info.get("gst_number", "")
                },
                "invoice_meta": {
                    "number": invoice_data.get("invoice_number", invoice_number),
                    "date": invoice_data.get("invoice_date_formatted", 
                                           datetime.now().strftime("%d/%m/%Y"))
                },
                "customer": {
                    "name": invoice_data.get("customer_name", ""),
                    "email": invoice_data.get("customer_email", ""),
                    "contact": invoice_data.get("customer_phone", "")
                },
                "items": invoice_data.get("pdf_items", []),
                "notes": "Generated from Travel Billing System",
                "terms": self.invoice_config.get("terms", "Payment due within 7 days."),
                "currency": self.get_currency_symbol()
            }
            
            # Generate PDF
            generate_invoice_pdf(pdf_data, filename)
            
            log_info(f"PDF generated: {filename}", "pdf_operations")
            
            # Show dialog if requested
            if show_dialog:
                msg = QMessageBox()
                msg.setWindowTitle("PDF Saved")
                msg.setText(f"PDF saved!\n{filename}")
                open_btn = msg.addButton("Open", QMessageBox.ButtonRole.ActionRole)
                msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)
                msg.exec()
                
                if msg.clickedButton() == open_btn:
                    os.startfile(filename)
            
            return filename
            
        except Exception as e:
            log_error(
                f"Error generating PDF for invoice {invoice_number}",
                exception=e,
                logger_name="pdf_operations_errors"
            )
            QMessageBox.critical(
                None,
                "PDF Error",
                f"Failed to generate PDF:\n{str(e)}"
            )
            return None
    
    def print_invoice(self, invoice_number: str, parent_widget=None) -> bool:
        """
        Print invoice PDF.
        
        Args:
            invoice_number: Invoice number
            parent_widget: Parent widget for dialogs
            
        Returns:
            bool: True if printed successfully
        """
        try:
            if not PDFIUM_AVAILABLE:
                QMessageBox.warning(
                    parent_widget,
                    "Print Unavailable",
                    "pypdfium2 library is not installed.\n"
                    "Install it using: pip install pypdfium2"
                )
                return False
            
            from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
            from PyQt6.QtGui import QPainter, QImage
            from PyQt6.QtCore import Qt
            
            # Check if PDF exists
            pdf_path = os.path.join(
                os.getcwd(), "output", "invoice",
                f"invoice_{invoice_number}.pdf"
            )
            
            if not os.path.exists(pdf_path):
                log_warning(
                    f"PDF not found for printing: {pdf_path}, generating...",
                    logger_name="pdf_operations"
                )
                QMessageBox.warning(
                    parent_widget,
                    "PDF Not Found",
                    "PDF not found. Please save as PDF first."
                )
                return False
            
            # Load PDF
            pdf = pdfium.PdfDocument(pdf_path)
            
            # Print dialog
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, parent_widget)
            
            if dialog.exec() != QPrintDialog.DialogCode.Accepted:
                return False
            
            # Print pages
            painter = QPainter(printer)
            
            for idx, page in enumerate(pdf):
                # Render page to image
                bitmap = page.render(scale=2.0)
                pil_image = bitmap.to_pil().convert("RGBA")
                img = QImage(
                    pil_image.tobytes("raw", "RGBA"),
                    bitmap.width, bitmap.height,
                    QImage.Format.Format_RGBA8888
                )
                
                # Scale to fit page
                rect = printer.pageRect(QPrinter.Unit.DevicePixel)
                img_size = img.size()
                
                # Calculate scaled size maintaining aspect ratio
                target_width = rect.width()
                target_height = rect.height()
                
                # Get scaled size that fits within page rect
                scaled_size = img_size.scaled(
                    int(target_width), int(target_height),
                    Qt.AspectRatioMode.KeepAspectRatio
                )
                
                # Draw centered
                x = int(rect.x() + (rect.width() - scaled_size.width()) / 2)
                y = int(rect.y())
                
                painter.drawImage(
                    x, y,
                    img.scaled(scaled_size, Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
                )
                
                # New page for multi-page documents
                if idx < len(pdf) - 1:
                    printer.newPage()
            
            painter.end()
            
            log_info(f"Invoice printed: {invoice_number}", "pdf_operations")
            
            QMessageBox.information(
                parent_widget,
                "Print Complete",
                "Invoice sent to printer!"
            )
            
            return True
            
        except Exception as e:
            log_error(
                f"Error printing invoice {invoice_number}",
                exception=e,
                logger_name="pdf_operations_errors"
            )
            QMessageBox.critical(
                parent_widget,
                "Print Error",
                f"Failed to print invoice:\n{str(e)}"
            )
            return False
    
    def share_invoice(self, invoice_number: str, parent_widget=None) -> bool:
        """
        Share invoice via email (placeholder for future implementation).
        
        Args:
            invoice_number: Invoice number
            parent_widget: Parent widget for dialogs
            
        Returns:
            bool: True if share initiated successfully
        """
        try:
            pdf_path = os.path.join(
                os.getcwd(), "output", "invoice",
                f"invoice_{invoice_number}.pdf"
            )
            
            if not os.path.exists(pdf_path):
                QMessageBox.warning(
                    parent_widget,
                    "PDF Not Found",
                    "Please save as PDF before sharing."
                )
                return False
            
            # Get recipient email
            email, ok = QInputDialog.getText(
                parent_widget,
                "Share Invoice",
                f"Recipient email for Invoice {invoice_number}:"
            )
            
            if ok and email:
                log_info(
                    f"Share invoice requested: {invoice_number} to {email}",
                    "pdf_operations"
                )
                
                QMessageBox.information(
                    parent_widget,
                    "Share Ready",
                    f"Ready to send invoice to {email}\n"
                    f"File: {pdf_path}\n\n"
                    f"(Email integration coming soon)"
                )
                
                return True
            
            return False
            
        except Exception as e:
            log_error(
                f"Error sharing invoice {invoice_number}",
                exception=e,
                logger_name="pdf_operations_errors"
            )
            QMessageBox.critical(
                parent_widget,
                "Share Error",
                f"Failed to share invoice:\n{str(e)}"
            )
            return False


class KeyboardShortcutsManager:
    """Manages keyboard shortcuts for home page actions."""
    
    def __init__(self, parent_widget):
        """
        Initialize keyboard shortcuts manager.
        
        Args:
            parent_widget: Parent widget to attach shortcuts to
        """
        self.parent = parent_widget
        self.shortcuts = []
    
    def setup_shortcuts(
        self,
        save_callback: callable,
        print_callback: callable,
        reset_callback: callable,
        add_item_callback: callable
    ):
        """
        Setup keyboard shortcuts.
        
        Args:
            save_callback: Function to call for Ctrl+S
            print_callback: Function to call for Ctrl+P
            reset_callback: Function to call for Ctrl+N
            add_item_callback: Function to call for F2 or Ctrl+I
        """
        try:
            # Ctrl+S - Save
            save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self.parent)
            save_shortcut.activated.connect(save_callback)
            self.shortcuts.append(save_shortcut)
            
            # Ctrl+P - Print
            print_shortcut = QShortcut(QKeySequence("Ctrl+P"), self.parent)
            print_shortcut.activated.connect(print_callback)
            self.shortcuts.append(print_shortcut)
            
            # Ctrl+N - Reset
            reset_shortcut = QShortcut(QKeySequence("Ctrl+N"), self.parent)
            reset_shortcut.activated.connect(reset_callback)
            self.shortcuts.append(reset_shortcut)
            
            # F2 - Add Item
            add_item_f2 = QShortcut(QKeySequence("F2"), self.parent)
            add_item_f2.activated.connect(add_item_callback)
            self.shortcuts.append(add_item_f2)
            
            # Ctrl+I - Add Item (alternative)
            add_item_ctrl_i = QShortcut(QKeySequence("Ctrl+I"), self.parent)
            add_item_ctrl_i.activated.connect(add_item_callback)
            self.shortcuts.append(add_item_ctrl_i)
            
            log_info("Keyboard shortcuts configured", "shortcuts")
            
        except Exception as e:
            log_error(
                "Error setting up keyboard shortcuts",
                exception=e,
                logger_name="shortcuts_errors"
            )


def prepare_items_for_pdf(items: list, get_currency_symbol: callable) -> list:
    """
    Prepare items data for PDF generation.
    
    Args:
        items: List of item dictionaries from table
        get_currency_symbol: Function to get currency symbol
        
    Returns:
        List of items formatted for PDF generator
    """
    try:
        pdf_items = []
        
        for item in items:
            passenger_name = item.get("passenger_name", "")
            pnr = item.get("pnr", "")
            sector = item.get("sector", "")
            qty = item.get("qty", 1)
            selling_price = item.get("selling_price", 0)
            
            # Calculate unit price
            unit_price = selling_price / qty if qty > 0 else selling_price
            
            pdf_items.append({
                "passenger_name": passenger_name,
                "pnr": pnr,
                "sector": sector,
                "type": item.get("service_type", "Flight"),
                "qty": qty,
                "unit_price": unit_price,
                "amount": selling_price
            })
        
        return pdf_items
        
    except Exception as e:
        log_error(
            "Error preparing items for PDF",
            exception=e,
            logger_name="invoice_utils_errors"
        )
        return []


def format_date_for_display(qdate: QDate, format_string: str = "dd/MM/yyyy") -> str:
    """
    Format QDate for display.
    
    Args:
        qdate: QDate object
        format_string: Date format string
        
    Returns:
        Formatted date string
    """
    try:
        return qdate.toString(format_string)
    except Exception as e:
        log_error(
            f"Error formatting date: {qdate}",
            exception=e,
            logger_name="invoice_utils_errors"
        )
        return datetime.now().strftime("%d/%m/%Y")
