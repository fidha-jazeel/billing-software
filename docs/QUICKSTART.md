# 🚀 Quick Start Guide

## Installation & Setup

### Step 1: Install Dependencies
Open Command Prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

This will install:
- PyQt6 (for the GUI)
- reportlab (for PDF generation)

### Step 2: Run the Application
```bash
python main.py
```

The application will:
- Create a database file (`billing.db`) on first run
- Open in maximized window with dark theme
- Start on the Home/Billing page

## First Time Setup

### Configure Your Company Details
1. Click **⚙️ Settings** in the sidebar
2. Fill in your company information:
   - Company Name
   - Address
   - Contact Number
   - Email
   - GST Number (optional)
3. Set Invoice Prefix (e.g., "INV" will create INV-0001, INV-0002, etc.)
4. Click **💾 Save Settings**

## Creating Your First Invoice

### Step 1: Enter Customer Details
1. Go to **🏠 Home** page
2. Enter customer name (required)
3. Enter contact number (optional)

### Step 2: Add Items
1. Click **➕ Add Item** button
2. Fill in the item details:
   - **Item Name**: Service or visa type
   - **Ticket #**: Ticket number
   - **Sector**: Travel sector/route
   - **Supplier**: Supplier name
   - **Quantity**: Number of items
   - **Price/Unit**: Price per item
   - **Tax %**: Tax percentage (e.g., 18 for 18% GST)
3. Add more items as needed

### Step 3: Review & Adjust
- Amounts are calculated automatically
- Enter amount received in the "Received" field
- Balance is calculated automatically

### Step 4: Save Invoice
1. Click **💾 Save Invoice**
2. Invoice is saved to database
3. Invoice number is auto-generated

### Step 5: Export to PDF (Optional)
1. After saving, click **📄 Save as PDF**
2. Choose location and filename
3. PDF invoice is generated with all details

## Using Reports

### View Sales Analytics
1. Click **📊 Reports** in sidebar
2. Use quick filters:
   - **Today**: Today's sales
   - **This Week**: Current week
   - **This Month**: Current month
   - **All Time**: All invoices
3. Or set custom date range

### Analytics Displayed
- 💰 Total Sales Amount
- 📄 Number of Invoices
- ✅ Total Received
- ⏳ Pending Balance
- 📊 Average Sale Value

### Recent Invoices Table
- View all invoices in date range
- Color-coded balance status
- Click on any invoice to view details

## Tips & Shortcuts

### Billing Page
- Customer name has autocomplete - start typing and select from existing customers
- Use Tab key to move between fields quickly
- Click 🗑️ button to remove an item row
- Click **📄 New Invoice** to start fresh

### Reports Page
- Use date filters to focus on specific periods
- Export reports to PDF (coming soon)
- Balance amounts show in yellow (pending) or green (paid)

### Settings Page
- Change invoice prefix anytime
- Previous invoices keep their original numbers
- Company details appear on PDF invoices

## Keyboard Shortcuts (Windows)

- **Alt + F4**: Close application
- **Tab**: Move to next field
- **Shift + Tab**: Move to previous field
- **Enter**: Activate focused button

## Database Location

The database file `billing.db` is created in the same folder as `main.py`.

**Backup**: Simply copy this file to backup all your data!

## Troubleshooting

### Application Won't Start
1. Check Python version: `python --version` (needs 3.10+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check for error messages in terminal

### Can't Save Invoice
- Ensure customer name is filled
- At least one item must be added
- Check file permissions in folder

### PDF Export Not Working
1. Ensure reportlab is installed: `pip install reportlab`
2. Check write permissions in save location
3. Try saving to a different folder

### Database Errors
- Close the application
- Rename `billing.db` to `billing_backup.db`
- Restart application (creates new database)

## Features Overview

### ✅ Implemented Features
- ✅ Dynamic invoice creation
- ✅ Multiple items per invoice
- ✅ Customer autocomplete
- ✅ Automatic calculations
- ✅ SQLite database storage
- ✅ Reports and analytics
- ✅ Date filtering
- ✅ PDF export
- ✅ Dark theme
- ✅ Settings management

### 🔄 Coming Soon
- Advanced customer management page
- Item/service catalog
- Payment history tracking
- Advanced search and filters
- Data export (Excel, CSV)
- Email invoice functionality
- Multi-currency support

## Support

For help or questions:
1. Check this guide
2. Read the README.md
3. Check the About page in the application

---

**Happy Billing! 🎉**

Made with ❤️ for Travel Agencies
