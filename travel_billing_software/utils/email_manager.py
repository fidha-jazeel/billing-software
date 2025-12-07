"""
Email Manager Module
Handles SMTP email sending functionality with configuration support.
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
from pathlib import Path
from typing import Optional, List, Tuple
import json
import os

from travel_billing_software.utils.logger import log_info, log_error, log_warning


class EmailManager:
    """
    Manages email sending with SMTP configuration.
    
    Features:
    - SMTP configuration (server, port, username, password)
    - SSL/TLS support
    - Attachment support
    - HTML email support
    - Configuration persistence
    """
    
    def __init__(self):
        """Initialize email manager."""
        self.config_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'email_config.json'
        )
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """
        Load email configuration from file.
        
        Returns:
            dict: Email configuration
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    log_info("Email configuration loaded", "email_manager")
                    return config
            else:
                # Return default empty configuration
                return {
                    "smtp_server": "",
                    "smtp_port": 587,
                    "use_tls": True,
                    "username": "",
                    "password": "",
                    "sender_email": "",
                    "sender_name": "Billing System"
                }
        except Exception as e:
            log_error("Failed to load email configuration", exception=e, logger_name="email_manager_errors")
            return {
                "smtp_server": "",
                "smtp_port": 587,
                "use_tls": True,
                "username": "",
                "password": "",
                "sender_email": "",
                "sender_name": "Billing System"
            }
    
    def save_config(self, config: dict) -> bool:
        """
        Save email configuration to file.
        
        Args:
            config: Email configuration dictionary
            
        Returns:
            bool: True if saved successfully
        """
        try:
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # Save configuration
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            
            # Update current config
            self.config = config
            
            log_info("Email configuration saved", "email_manager")
            return True
            
        except Exception as e:
            log_error("Failed to save email configuration", exception=e, logger_name="email_manager_errors")
            return False
    
    def get_config(self) -> dict:
        """
        Get current email configuration.
        
        Returns:
            dict: Email configuration
        """
        return self.config.copy()
    
    def is_configured(self) -> bool:
        """
        Check if email is properly configured.
        
        Returns:
            bool: True if SMTP settings are configured
        """
        return bool(
            self.config.get("smtp_server") and
            self.config.get("username") and
            self.config.get("password") and
            self.config.get("sender_email")
        )
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test SMTP connection with current configuration.
        
        Returns:
            Tuple[bool, str]: (Success status, message)
        """
        if not self.is_configured():
            return False, "Email not configured. Please configure SMTP settings first."
        
        try:
            # Create SMTP connection
            if self.config.get("use_tls", True):
                context = ssl.create_default_context()
                server = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
                server.starttls(context=context)
            else:
                server = smtplib.SMTP_SSL(self.config["smtp_server"], self.config["smtp_port"])
            
            # Login
            server.login(self.config["username"], self.config["password"])
            server.quit()
            
            log_info("SMTP connection test successful", "email_manager")
            return True, "Connection successful! SMTP settings are correct."
            
        except smtplib.SMTPAuthenticationError:
            msg = "Authentication failed. Please check your username and password."
            log_warning(msg, "email_manager")
            return False, msg
        except smtplib.SMTPConnectError:
            msg = "Cannot connect to SMTP server. Please check server and port."
            log_warning(msg, "email_manager")
            return False, msg
        except Exception as e:
            msg = f"Connection failed: {str(e)}"
            log_error("SMTP connection test failed", exception=e, logger_name="email_manager_errors")
            return False, msg
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        html_body: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        """
        Send an email with optional attachments.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text email body
            attachments: List of file paths to attach
            html_body: HTML version of email body (optional)
            cc: List of CC recipients
            bcc: List of BCC recipients
            
        Returns:
            Tuple[bool, str]: (Success status, message)
        """
        if not self.is_configured():
            return False, "Email not configured. Please configure SMTP settings in Settings."
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = formataddr((self.config.get("sender_name", ""), self.config["sender_email"]))
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            msg.attach(part)
                    else:
                        log_warning(f"Attachment not found: {file_path}", "email_manager")
            
            # Send email
            if self.config.get("use_tls", True):
                context = ssl.create_default_context()
                server = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
                server.starttls(context=context)
            else:
                server = smtplib.SMTP_SSL(self.config["smtp_server"], self.config["smtp_port"])
            
            server.login(self.config["username"], self.config["password"])
            
            # Build recipient list
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            server.sendmail(self.config["sender_email"], recipients, msg.as_string())
            server.quit()
            
            log_info(f"Email sent successfully to {to_email}", "email_manager")
            return True, f"Email sent successfully to {to_email}"
            
        except smtplib.SMTPAuthenticationError:
            msg = "Authentication failed. Please check your email credentials in Settings."
            log_error(msg, logger_name="email_manager_errors")
            return False, msg
        except smtplib.SMTPException as e:
            msg = f"SMTP error: {str(e)}"
            log_error("SMTP error while sending email", exception=e, logger_name="email_manager_errors")
            return False, msg
        except Exception as e:
            msg = f"Failed to send email: {str(e)}"
            log_error("Error sending email", exception=e, logger_name="email_manager_errors")
            return False, msg
    
    def send_invoice_email(
        self,
        to_email: str,
        invoice_number: str,
        customer_name: str,
        pdf_path: str,
        total_amount: float = 0,
        company_name: str = "Our Company"
    ) -> Tuple[bool, str]:
        """
        Send invoice email with PDF attachment.
        
        Args:
            to_email: Customer email address
            invoice_number: Invoice number
            customer_name: Customer name
            pdf_path: Path to invoice PDF file
            total_amount: Invoice total amount
            company_name: Company name
            
        Returns:
            Tuple[bool, str]: (Success status, message)
        """
        try:
            from travel_billing_software.config.config import format_currency
            
            # Prepare email content
            subject = f"Invoice {invoice_number} from {company_name}"
            
            body = f"""Dear {customer_name},

Thank you for your business!

Please find attached Invoice {invoice_number} for your recent purchase.

Invoice Details:
- Invoice Number: {invoice_number}
- Total Amount: {format_currency(total_amount)}

If you have any questions about this invoice, please don't hesitate to contact us.

Best regards,
{company_name}
"""
            
            html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; color: #333;">
    <h2 style="color: #7c3aed;">Invoice from {company_name}</h2>
    
    <p>Dear <strong>{customer_name}</strong>,</p>
    
    <p>Thank you for your business!</p>
    
    <p>Please find attached <strong>Invoice {invoice_number}</strong> for your recent purchase.</p>
    
    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <h3 style="margin-top: 0;">Invoice Details:</h3>
        <ul style="list-style: none; padding: 0;">
            <li>📄 <strong>Invoice Number:</strong> {invoice_number}</li>
            <li>💰 <strong>Total Amount:</strong> {format_currency(total_amount)}</li>
        </ul>
    </div>
    
    <p>If you have any questions about this invoice, please don't hesitate to contact us.</p>
    
    <p>Best regards,<br>
    <strong>{company_name}</strong></p>
</body>
</html>
"""
            
            # Check if PDF exists
            if not os.path.exists(pdf_path):
                return False, "Invoice PDF not found. Please save as PDF first."
            
            # Send email
            return self.send_email(
                to_email=to_email,
                subject=subject,
                body=body,
                html_body=html_body,
                attachments=[pdf_path]
            )
            
        except Exception as e:
            msg = f"Failed to send invoice email: {str(e)}"
            log_error("Error sending invoice email", exception=e, logger_name="email_manager_errors")
            return False, msg


# Singleton instance
_email_manager_instance = None


def get_email_manager() -> EmailManager:
    """
    Get the singleton EmailManager instance.
    
    Returns:
        EmailManager: The email manager instance
    """
    global _email_manager_instance
    if _email_manager_instance is None:
        _email_manager_instance = EmailManager()
    return _email_manager_instance
