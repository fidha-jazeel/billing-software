# 🎫 Travel Agency Billing Software

A comprehensive billing and invoicing solution designed specifically for travel agencies. Built with PyQt6 and SQLite, featuring a beautiful dark-themed interface.

## ✨ Features

- 📄 **Dynamic Invoice Creation** - Add multiple items with ticket numbers, sectors, suppliers, and pricing
- 👥 **Customer Management** - Track customer information with autocomplete support
- 💰 **Payment Tracking** - Monitor received payments and outstanding balances
- 📊 **Reports & Analytics** - Comprehensive sales reports with date filtering
- ⚙️ **Settings Management** - Configure company information and invoice preferences
- 🎨 **Dark Theme** - Modern, eye-friendly dark interface
- 💾 **SQLite Database** - Reliable local data storage
- 📄 **PDF Export** - Generate professional invoice PDFs

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install PyQt6 reportlab
```

Or using the project file:
```bash
pip install -e .
```

3. **Run the application:**
```bash
python main.py
```

## 📁 Project Structure

```
billing-software/
├── main.py                 # Application entry point
├── database/
│   ├── __init__.py
│   └── db_manager.py      # Database operations
├── ui/
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── home_page.py       # Billing/Invoice page
│   ├── reports_page.py    # Reports & analytics
│   ├── settings_page.py   # Settings configuration
│   └── about_page.py      # About page
├── utils/
│   ├── __init__.py
│   ├── styles.py          # Dark theme stylesheet
│   └── pdf_generator.py   # PDF export functionality
├── billing.db             # SQLite database (auto-created)
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## 🎯 Usage Guide

### Creating an Invoice

1. **Navigate to Home Page** (default page on startup)
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

### Viewing Reports

1. **Navigate to Reports Page**
2. **Apply Date Filters:**
   - Use quick filters (Today, This Week, This Month, All Time)
   - Or set custom date range
3. **View Analytics:**
   - Total sales amount
   - Number of invoices
   - Received vs pending amounts
   - Average sale value
4. **Review Invoice List:**
   - All invoices with customer details
   - Payment status color-coded

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
- **customers** - Customer information
- **items** - Item/service catalog
- **invoices** - Invoice headers
- **invoice_items** - Invoice line items (with ticket details)
- **settings** - Application configuration

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
- PyQt6 >= 6.6.0
- reportlab >= 4.0.0

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Support

For issues, questions, or feature requests, please create an issue in the repository.

## 🎉 Version History

### v1.0.0 (2025)
- Initial release
- Dark theme interface
- Invoice creation with multiple items
- Customer management
- Reports and analytics
- PDF export
- Settings configuration

---

**Built with ❤️ using PyQt6 and SQLite**