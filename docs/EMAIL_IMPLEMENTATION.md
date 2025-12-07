# Email/SMTP Integration - Complete Implementation

## Overview
Full SMTP email functionality has been implemented for sending invoices via email. The system includes:

1. **Email Manager Module** - Core SMTP handling
2. **Settings Page Integration** - User-friendly configuration
3. **Home Page Integration** - Share invoice via email button
4. **Configuration Persistence** - Settings saved to `config/email_config.json`

## Features

### 1. SMTP Configuration (Settings Page)
- SMTP Server configuration
- Port selection (default: 587)
- TLS/SSL support
- Username & Password (with show/hide)
- Sender email & name customization
- **Test Connection** button to verify settings
- Gmail app password support (with instructions)

### 2. Email Sending Capabilities
- Send invoices as PDF attachments
- Professional HTML email templates
- Plain text fallback
- Customer email pre-fill from invoice data
- Progress dialog during sending
- Detailed error messages

### 3. Security Features
- Passwords stored securely in config file
- Password masking in UI
- Connection encryption (TLS/SSL)
- Validation before sending

## Configuration Steps

### For Gmail Users:
1. Go to Settings → Email/SMTP Configuration
2. Fill in:
   - **SMTP Server**: `smtp.gmail.com`
   - **SMTP Port**: `587`
   - **Use TLS**: Yes (TLS)
   - **Username**: Your full Gmail address (e.g., `yourname@gmail.com`)
   - **Password**: Generate an App Password at https://myaccount.google.com/apppasswords
   - **Sender Email**: Your Gmail address
   - **Sender Name**: Your company name or name

3. Click **Test SMTP Connection** to verify
4. Click **Save All Settings**

### For Outlook/Office 365 Users:
1. Go to Settings → Email/SMTP Configuration
2. Fill in:
   - **SMTP Server**: `smtp.office365.com`
   - **SMTP Port**: `587`
   - **Use TLS**: Yes (TLS)
   - **Username**: Your full Outlook email
   - **Password**: Your account password
   - **Sender Email**: Your Outlook email
   - **Sender Name**: Your company name

3. Test and save

### For Other SMTP Providers:
Configure with your provider's SMTP settings. Common providers:
- **Yahoo**: smtp.mail.yahoo.com:587
- **Hotmail**: smtp.live.com:587
- **Custom/Business Email**: Check with your email provider

## Usage

### Sending Invoice via Email:
1. Create an invoice in Home page
2. Click **Save as PDF** button first (email requires PDF)
3. Click **📤 Share Invoice** button
4. Enter recipient email address (pre-filled if customer email exists)
5. Click OK to send
6. Email will be sent with professional formatting and PDF attachment

### Email Template:
The system automatically creates a professional email with:
- Personalized greeting
- Invoice number and details
- Total amount formatted with currency
- PDF attachment
- Company branding
- Professional HTML formatting

## Technical Details

### Email Manager (`travel_billing_software/utils/email_manager.py`)
```python
from travel_billing_software.utils.email_manager import get_email_manager

email_manager = get_email_manager()

# Check if configured
if email_manager.is_configured():
    # Send custom email
    success, message = email_manager.send_email(
        to_email="customer@example.com",
        subject="Your Invoice",
        body="Plain text body",
        html_body="<h1>HTML body</h1>",
        attachments=["path/to/file.pdf"]
    )
    
    # Or send invoice specifically
    success, message = email_manager.send_invoice_email(
        to_email="customer@example.com",
        invoice_number="INV-001",
        customer_name="John Doe",
        pdf_path="output/invoice/invoice_INV-001.pdf",
        total_amount=1000.00,
        company_name="Your Company"
    )
```

### Configuration File Location:
`travel_billing_software/config/email_config.json`

### Configuration Structure:
```json
{
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "use_tls": true,
    "username": "your.email@gmail.com",
    "password": "your_app_password",
    "sender_email": "your.email@gmail.com",
    "sender_name": "Your Company Name"
}
```

## Troubleshooting

### "Authentication failed"
- For Gmail: Make sure you're using an App Password, not your regular password
- Check username is the full email address
- Verify password is correct

### "Cannot connect to SMTP server"
- Check internet connection
- Verify SMTP server address is correct
- Confirm port number matches your provider
- Try toggling between TLS and SSL

### "Email not configured"
- Go to Settings → Email/SMTP Configuration
- Fill in all required fields
- Click Test Connection to verify
- Save settings

### Gmail App Password:
1. Enable 2-Step Verification on your Google Account
2. Visit https://myaccount.google.com/apppasswords
3. Select "Mail" and your device
4. Copy the generated 16-character password
5. Use this password in the billing software

## Files Modified/Created

### New Files:
- `travel_billing_software/utils/email_manager.py` - Complete email handling
- `travel_billing_software/config/email_config.json` - Auto-created on first save

### Modified Files:
- `travel_billing_software/ui/settings.py`:
  - Added `_create_email_section()` method
  - Added SMTP configuration UI
  - Added test connection functionality
  - Updated `save_all_settings()` to save email config

- `travel_billing_software/ui/home/utils.py`:
  - Updated `share_invoice()` to use email manager
  - Added customer email pre-fill
  - Added progress dialog
  - Added proper error handling

## Future Enhancements (Optional)
- CC/BCC support in UI
- Email templates customization
- Bulk email sending
- Email history/log
- Attachment size warnings
- Email scheduling
- Custom email templates per invoice type

## Support
If you encounter issues:
1. Use the "Test SMTP Connection" button in Settings
2. Check error messages for specific issues
3. Verify your email provider's SMTP settings
4. Ensure firewall/antivirus isn't blocking SMTP ports
5. Check application logs for detailed error information
