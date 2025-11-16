# 🎫 Travel Agency Billing Software

A comprehensive billing and invoicing solution designed specifically for travel agencies. Built with PyQt6 and SQLite, featuring a beautiful dark-themed interface.

## ✨ Features

- 🔐 **Secure Login System** - Password authentication with change password functionality
- 📄 **Dynamic Invoice Creation** - Add multiple items with ticket numbers, sectors, suppliers, and pricing
- 👥 **Customer Management** - Track customer information with autocomplete support
- 💰 **Payment Tracking** - Monitor received payments and outstanding balances
- 📊 **Reports & Analytics** - Comprehensive sales reports with charts and metrics
  - Revenue trends (last 6 months)
  - Top customers by spending
  - Payment status summary
  - Key performance indicators
- ⚙️ **Settings Management** - Configure company information and invoice preferences
- 🎨 **Modern Theme** - Purple-teal gradient theme with dark mode support
- 💾 **SQLite Database** - Reliable local data storage
- 📄 **PDF Export** - Generate professional invoice PDFs
- 🪟 **Maximized Windows** - All windows open in maximized state for better visibility

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install PyQt5 reportlab
```

Or using requirements.txt:
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

### First Run
- The login page will appear with default password: **admin123**
- After successful login, the main dashboard opens
- Database and authentication files are created automatically

## 📁 Project Structure

```
billing-software/
├── main.py                          # Application entry point with login
├── auth/                            # Authentication system
│   ├── __init__.py
│   └── auth_manager.py              # Password management
├── database/
│   ├── __init__.py
│   └── db_manager.py                # Database operations
├── ui/
│   ├── __init__.py
│   ├── login_page.py                # Login interface
│   └── change_password_dialog.py   # Password change dialog
├── travel_billing/
│   ├── __init__.py
│   └── dashboard_improved.py        # Main dashboard (billing, reports, analytics)
├── config/
│   ├── __init__.py
│   └── settings.py                  # Application configuration
├── utils/
│   ├── __init__.py
│   └── styles.py                    # Theme and styles
├── auth_data.json                   # Password storage (auto-created)
├── billing.db                       # SQLite database (auto-created)
├── billing_app.ico                  # Application icon
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🎯 Usage Guide

### Login

1. **First Time Login:**
   - Default password: **admin123**
   - Enter password and click Login (or press Enter)
2. **Change Password:**
   - Click "Change Password" link on login page
   - Enter current password and new password
   - Password must be at least 4 characters
3. **Reset Password:**
   - Click "Reset" button to clear the password field

### Creating an Invoice

1. **Navigate to Home Page** (default page after login)
2. **Enter Customer Details:**
   - Customer name (required)
   - Contact number (optional)
3. **Add Items:**
   - Click "➕ Add Item" to add rows
   - Fill in item details:
     - Item name / Visa type
     - Ticket number
     - Sector
     - Supplier
     - Quantity
     - Price per unit
     - Tax percentage
4. **Review Calculations:**
   - Subtotal, tax, and total are calculated automatically
   - Enter received amount
   - Balance is computed automatically
5. **Save Invoice:**
   - Click "💾 Save Invoice" to save to database
   - Click "📄 Save as PDF" to export as PDF

### Viewing Reports & Analytics

1. **Navigate to Reports Page**
2. **View Key Metrics:**
   - Total revenue
   - Number of invoices
   - Pending payments
   - Active customers
3. **Revenue Trend Chart:**
   - Visual chart showing revenue for last 6 months
4. **Top Customers:**
   - List of top 5 customers by total spending
5. **Payment Status:**
   - Summary of paid, pending, and overpaid invoices
6. **Refresh Data:**
   - Click "🔄 Refresh Analytics" to update all metrics

### Configuring Settings

1. **Navigate to Settings Page**
2. **Company Information:**
   - Company name
   - Address
   - Contact details
   - GST number
3. **Invoice Settings:**
   - Invoice prefix (e.g., INV, BILL)
   - Currency symbol
4. **Save Settings**

## 🗄️ Database Schema

### Tables
- **customers** - Customer information and contact details
- **items** - Item/service catalog with pricing
- **invoices** - Invoice headers with customer and payment info
- **invoice_items** - Invoice line items (with ticket details, sector, supplier)
- **settings** - Application configuration (company info, invoice settings)

### Authentication
- **auth_data.json** - Encrypted password storage using SHA-256 hashing

## 🔧 Customization

### Changing Colors
Edit `utils/styles.py` to customize the color scheme. Key colors:
- Primary: `#0d7377` (teal)
- Background: `#1e1e1e` (dark gray)
- Cards: `#252525` (lighter dark gray)

### Adding Fields
To add new fields to invoices:
1. Update database schema in `database/db_manager.py`
2. Add UI fields in `ui/home_page.py`
3. Update save/load logic accordingly

## 📝 Tips

- Press Ctrl+F to search for customers (autocomplete enabled)
- All amounts are stored with 2 decimal precision
- Invoice numbers auto-increment based on prefix
- Database is automatically created on first run
- All data is stored locally in `billing.db`

## 🐛 Troubleshooting

**Issue: Application won't start**
- Ensure Python 3.10+ is installed
- Verify all dependencies are installed: `pip list`

**Issue: Database errors**
- Delete `billing.db` and restart (will reset all data)
- Check file permissions in the directory

**Issue: PDF generation fails**
- Ensure reportlab is installed: `pip install reportlab`
- Check write permissions in the directory

## 📦 Requirements

- Python >= 3.10
- PyQt5 >= 5.15.0
- reportlab >= 4.0.0

All dependencies are listed in `requirements.txt`

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Support

For issues, questions, or feature requests, please create an issue in the repository.

## 🎉 Version History

### v2.0.0 (November 2025)
- ✨ Added secure login system with password authentication
- ✨ Added change password functionality
- ✨ Added comprehensive analytics dashboard
- ✨ Added revenue trend charts
- ✨ Added top customers tracking
- ✨ Added payment status visualization
- 🎨 Updated to modern purple-teal gradient theme
- 🪟 All windows now open maximized
- 🔧 Improved invoice field widths for better visibility
- 📱 Enhanced UI with better spacing and layouts

### v1.0.0 (2025)
- Initial release
- Dark theme interface
- Invoice creation with multiple items
- Customer management
- Basic reports
- PDF export
- Settings configuration

---

**Built with ❤️ using PyQt5 and SQLite**