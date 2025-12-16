"""
Utility Functions for Home Page
Contains helpers for invoice operations, shortcuts, and PDF generation.
"""
import os
from datetime import datetime
from typing import Dict, Any, Optional
from PyQt6.QtWidgets import QMessageBox, QInputDialog, QApplication
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import QDate, Qt
from utils.invoice_generator import generate_invoice_pdf
from travel_billing_software.utils.logger import log_info, log_error, log_warning
from travel_billing_software.utils.path_loader import persistent_data_path

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
    ) -> bool:
        """
        Generate PDF invoice.
        
        Args:
            invoice_number: Invoice number for filename
            invoice_data: Complete invoice data dictionary
            show_dialog: Whether to show success dialog
            
        Returns:
            bool: True if PDF generated successfully, False otherwise
        """
        try:
            # Prepare output directory in AppData
            default_dir = os.path.join(persistent_data_path(), "output", "invoice")
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

                "amounts": {
                    "subtotal": invoice_data.get("total_amount", 0),
                    "tax": 0,
                    "total": invoice_data.get("total_amount", 0),
                    "paid": invoice_data.get("paid_amount", 0),         
                    "balance": invoice_data.get("balance_amount", 0)
                },
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
            
            return True
            
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
            return False
    
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
            
            try:
                from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
                from PyQt6.QtGui import QPainter, QImage
                from PyQt6.QtCore import Qt
            except ImportError as e:
                log_error(
                    f"Print support not available: {e}",
                    logger_name="pdf_operations"
                )
                QMessageBox.critical(
                    parent_widget,
                    "Print Unavailable",
                    "Print support is not available.\n"
                    "PyQt6.QtPrintSupport module is missing."
                )
                return False
            
            # Check if PDF exists, if not auto-generate it
            pdf_path = os.path.join(
                persistent_data_path(), "output", "invoice",
                f"invoice_{invoice_number}.pdf"
            )
            
            if not os.path.exists(pdf_path):
                log_info(
                    f"PDF not found for printing: {pdf_path}, auto-generating...",
                    logger_name="pdf_operations"
                )
                
                # Try to auto-generate the PDF
                try:
                    # Get the invoice data from database
                    from travel_billing_software.database.db_manager import get_db_instance
                    
                    db = get_db_instance()
                    invoice_record = db.get_invoice(invoice_number)
                    
                    if not invoice_record:
                        QMessageBox.warning(
                            parent_widget,
                            "Invoice Not Found",
                            f"Invoice {invoice_number} not found in database.\n"
                            "Please save the invoice first."
                        )
                        return False
                    
                    # Prepare data for PDF
                    pdf_items = prepare_items_for_pdf(invoice_record.get('items', []), self.get_currency_symbol)
                    
                    # Format date
                    invoice_date = invoice_record.get('invoice_date')
                    if isinstance(invoice_date, str):
                        date_formatted = invoice_date
                    else:
                        date_formatted = invoice_date.strftime('%d/%m/%Y') if invoice_date else datetime.now().strftime('%d/%m/%Y')
                    
                    invoice_data = {
                        "invoice_number": invoice_number,
                        "invoice_date_formatted": date_formatted,
                        "customer_name": invoice_record.get('customer_name', ''),
                        "customer_address": invoice_record.get('customer_address', ''),
                        "customer_phone": invoice_record.get('customer_phone', ''),
                        "pdf_items": pdf_items,
                        "total_amount": total_amount,
                        "paid_amount": paid_amount,
                        "balance_amount": balance_amount
                    }
                    
                    # Generate PDF silently
                    success = self.generate_pdf(invoice_number, invoice_data, show_dialog=False)
                    
                    if not success or not os.path.exists(pdf_path):
                        QMessageBox.warning(
                            parent_widget,
                            "PDF Generation Failed",
                            "Failed to auto-generate PDF for printing."
                        )
                        return False
                    
                    log_info(
                        f"PDF auto-generated successfully for printing: {invoice_number}",
                        logger_name="pdf_operations"
                    )
                    
                except Exception as e:
                    log_error(
                        f"Error auto-generating PDF for printing: {e}",
                        exception=e,
                        logger_name="pdf_operations"
                    )
                    QMessageBox.warning(
                        parent_widget,
                        "PDF Generation Failed",
                        f"Failed to auto-generate PDF:\n{str(e)}"
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
        Share invoice via email using configured SMTP settings.
        
        Args:
            invoice_number: Invoice number
            parent_widget: Parent widget for dialogs
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            from travel_billing_software.utils.email_manager import get_email_manager
            from travel_billing_software.config.config import COMPANY_INFO
            
            email_manager = get_email_manager()
            
            # Check if email is configured
            if not email_manager.is_configured():
                QMessageBox.warning(
                    parent_widget,
                    "Email Not Configured",
                    "Email/SMTP settings are not configured.\n\n"
                    "Please go to Settings → Email/SMTP Configuration to set up email before sharing invoices."
                )
                return False
            
            pdf_path = os.path.join(
                os.getcwd(), "output", "invoice",
                f"invoice_{invoice_number}.pdf"
            )
            
            if not os.path.exists(pdf_path):
                log_info(
                    f"PDF not found for sharing: {pdf_path}, auto-generating...",
                    logger_name="pdf_operations"
                )
                
                # Try to auto-generate the PDF
                try:
                    # Get the invoice data from database
                    from travel_billing_software.database.db_manager import get_db_instance
                    
                    db = get_db_instance()
                    invoice_record = db.get_invoice(invoice_number)
                    # Fetch payment details
                    paid_amount = invoice_record.get("paid_amount", 0)
                    total_amount = invoice_record.get("total_amount", 0)
                    balance_amount = total_amount - paid_amount

                    
                    if not invoice_record:
                        QMessageBox.warning(
                            parent_widget,
                            "Invoice Not Found",
                            f"Invoice {invoice_number} not found in database.\n"
                            "Please save the invoice first."
                        )
                        return False
                    
                    # Prepare data for PDF
                    pdf_items = prepare_items_for_pdf(invoice_record.get('items', []), self.get_currency_symbol)
                    
                    # Format date
                    invoice_date = invoice_record.get('invoice_date')
                    if isinstance(invoice_date, str):
                        date_formatted = invoice_date
                    else:
                        date_formatted = invoice_date.strftime('%d/%m/%Y') if invoice_date else datetime.now().strftime('%d/%m/%Y')
                    
                    invoice_data = {
                        "invoice_number": invoice_number,
                        "invoice_date_formatted": date_formatted,
                        "customer_name": invoice_record.get('customer_name', ''),
                        "customer_address": invoice_record.get('customer_address', ''),
                        "customer_phone": invoice_record.get('customer_phone', ''),
                        "pdf_items": pdf_items
                    }
                    
                    # Generate PDF silently
                    success = self.generate_pdf(invoice_number, invoice_data, show_dialog=False)
                    
                    if not success or not os.path.exists(pdf_path):
                        QMessageBox.warning(
                            parent_widget,
                            "PDF Generation Failed",
                            "Failed to auto-generate PDF for sharing."
                        )
                        return False
                    
                    log_info(
                        f"PDF auto-generated successfully for sharing: {invoice_number}",
                        logger_name="pdf_operations"
                    )
                    
                except Exception as e:
                    log_error(
                        f"Error auto-generating PDF for sharing: {e}",
                        exception=e,
                        logger_name="pdf_operations"
                    )
                    QMessageBox.warning(
                        parent_widget,
                        "PDF Generation Failed",
                        f"Failed to auto-generate PDF:\n{str(e)}"
                    )
                    return False
            
            # Get invoice data from database to populate email
            try:
                from travel_billing_software.database.db_manager import get_db_instance
                db = get_db_instance()
                invoice_data = db.get_invoice(invoice_number)
                
                if not invoice_data:
                    raise Exception("Invoice not found in database")
                
                customer_name = invoice_data.get('customer_name', 'Customer')
                customer_email = invoice_data.get('customer_email', '')
                total_amount = invoice_data.get('total_amount', 0)
                
            except Exception as e:
                log_warning(f"Could not load invoice data from database: {e}", "pdf_operations")
                customer_name = "Customer"
                customer_email = ""
                total_amount = 0
            
            # Get recipient email (pre-fill with customer email if available)
            email, ok = QInputDialog.getText(
                parent_widget,
                "Share Invoice via Email",
                f"Recipient email for Invoice {invoice_number}:",
                text=customer_email
            )
            
            if ok and email:
                # Validate email format (basic check)
                if '@' not in email or '.' not in email:
                    QMessageBox.warning(
                        parent_widget,
                        "Invalid Email",
                        "Please enter a valid email address."
                    )
                    return False
                
                log_info(
                    f"Sending invoice via email: {invoice_number} to {email}",
                    "pdf_operations"
                )
                
                # Show sending progress
                from PyQt6.QtWidgets import QProgressDialog
                progress = QProgressDialog("Sending email...", None, 0, 0, parent_widget)
                progress.setWindowModality(Qt.WindowModality.WindowModal)
                progress.setMinimumDuration(0)
                progress.setValue(0)
                QApplication.processEvents()
                
                # Send invoice email
                success, message = email_manager.send_invoice_email(
                    to_email=email,
                    invoice_number=invoice_number,
                    customer_name=customer_name,
                    pdf_path=pdf_path,
                    total_amount=total_amount,
                    company_name=COMPANY_INFO.get('name', 'Our Company')
                )
                
                progress.close()
                
                if success:
                    QMessageBox.information(
                        parent_widget,
                        "Email Sent",
                        f"Invoice successfully sent to {email}!\n\n"
                        f"File: {os.path.basename(pdf_path)}"
                    )
                    log_info(f"Invoice emailed successfully to {email}", "pdf_operations")
                    return True
                else:
                    QMessageBox.critical(
                        parent_widget,
                        "Email Failed",
                        f"Failed to send email:\n\n{message}\n\n"
                        "Please check your email configuration in Settings."
                    )
                    return False
            
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
                f"Failed to share invoice:\n{str(e)}\n\n"
                "Please check your email configuration in Settings."
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
