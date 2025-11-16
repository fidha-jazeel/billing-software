# 🏢 Travel Agency Billing Software

**Version 2.2.0** | Professional Invoicing & Billing System

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

A comprehensive, professional-grade billing and invoicing desktop application designed specifically for travel agencies. Built with PyQt5, this software provides an intuitive interface for managing customer invoices, tracking payments, and generating professional PDF reports.

### Why This Software?

- **🎨 Modern UI**: Dark-themed professional interface
- **⚡ Fast & Efficient**: Real-time calculations and instant PDF generation
- **🔧 Highly Configurable**: All settings centralized in configuration files
- **📊 Professional Output**: High-quality PDF and print templates
- **💾 Data Persistence**: JSON-based invoice storage with backup support
- **🎯 User-Friendly**: Intuitive workflow from invoice creation to payment tracking

---

## ✨ Features

### Core Features

- ✅ **Invoice Management**
  - Auto-generated invoice numbers with custom prefixes
  - Customer information tracking
  - Date-based invoice organization

- ✅ **Excel-Style Table**
  - 9-column layout (Item, Ticket, Sector, Supplier, Price, Qty, Tax, Amount, Actions)
  - Dropdown selectors for Sector and Supplier
  - Real-time amount calculation
  - Add/Delete rows dynamically

- ✅ **Real-Time Calculations**
  - Automatic subtotal calculation
  - Tax computation per item
  - Total amount with highlighted display
  - Payment tracking (Received & Balance)
  - Color-coded balance status

- ✅ **Multi-Export Options**
  - 💾 Save as JSON (data persistence)
  - 📄 Export to PDF
  - 🖨️ Professional printing
  - 📤 Share via email (ready for integration)

- ✅ **Professional UI**
  - Dark theme with consistent color palette
  - Bold, clear labels for better readability
  - Fixed-width layouts for alignment
  - Responsive design
  - Unified scrolling experience

### Advanced Features

- 🔧 **Dynamic Configuration System**
  - Centralized settings in `config/settings.py`
  - Easy customization without code changes
  - Company branding support
  - Color theme management

- 📊 **Professional Templates**
  - Invoice PDF with company header
  - Print-ready layouts
  - Formatted tables and totals
  - Terms and conditions footer

- 🎯 **User Experience**
  - Welcome screen with company branding
  - Multi-page navigation (Home, Reports, Settings, About)
  - Keyboard shortcuts support
  - Validation and error handling

---

## 📁 Project Structure

```
billing-software3/
│
├── config/                          # Configuration Package
│   ├── __init__.py                 # Config exports
│   └── settings.py                 # All settings & constants
│
├── utils/                           # Utilities Package
│   ├── __init__.py                 # Utils exports
│   └── styles.py                   # Styling functions
│
├── travel_billing/                  # Main Application Package
│   ├── __init__.py                 # Package initialization
│   └── dashboard_improved.py       # Main application class
│
├── invoices/                        # Invoice Storage
│   ├── *.json                      # Saved invoices
│   └── pdf/                        # PDF exports (future)
│
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
└── Documentation/                   # Documentation Files
    ├── FEATURES_V2.md
    ├── QUICK_START.md
    ├── VERSION_2.1_CHANGES.md
    ├── VERSION_2.2_CHANGES.md
    └── VISUAL_GUIDE_V2.1.md
```

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│              main.py (Entry Point)              │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│      travel_billing/dashboard_improved.py       │
│         (Main Application Logic)                │
└─────────┬──────────────────────┬────────────────┘
          │                      │
          ▼                      ▼
┌──────────────────┐    ┌──────────────────┐
│  config/         │    │  utils/          │
│  ├── settings.py │    │  └── styles.py   │
│  (Configuration) │    │  (UI Utilities)  │
└──────────────────┘    └──────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package manager)
- **Windows 10/11** (primary target OS)

### Step 1: Clone or Download

```bash
# Clone the repository
git clone https://github.com/fidha-jazeel/billing-software.git
cd billing-software3

# OR download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python main.py
```

If the application window opens, installation is successful! ✅

---

## ⚡ Quick Start

### Running the Application

```bash
# Navigate to project directory
cd billing-software3

# Run the application
python main.py
```

### Creating Your First Invoice

1. **Launch Application** - Double-click `main.py` or run from terminal
2. **Enter Invoice Details**
   - Invoice number is auto-generated
   - Select invoice date
   - Enter customer name and contact
3. **Add Items**
   - Click "➕ Add Item" button
   - Fill in item details
   - Select sector and supplier from dropdowns
   - Enter price, quantity, and tax
4. **Review Calculations**
   - Subtotal, tax, and total are calculated automatically
   - Enter received amount
   - Balance updates in real-time
5. **Save Invoice**
   - Click "💾 Save Invoice" for JSON storage
   - Click "📄 Save as PDF" for PDF export
   - Click "🖨️ Print Invoice" for physical copy

---

## ⚙️ Configuration

### Customizing Company Information

Edit `config/settings.py`:

```python
COMPANY_INFO = {
    "name": "Your Company Name",
    "tagline": "Your Business Tagline",
    "email": "your@email.com",
    "phone": "+1-XXX-XXX-XXXX",
    "address": "Your Business Address",
}
```

### Changing Color Theme

Edit `config/settings.py`:

```python
COLORS = {
    "primary_bg": "#1a1a1a",      # Main background
    "accent_primary": "#5b5bff",  # Primary accent color
    # ... customize other colors
}
```

### Customizing Invoice Settings

```python
INVOICE_CONFIG = {
    "number_prefix": "INV",        # Invoice number prefix
    "currency_symbol": "₹",        # Currency symbol
    "default_tax_rate": 5.0,       # Default tax %
    "terms": "Your terms here",    # Invoice terms
}
```

### Adding/Modifying Suppliers

```python
SUPPLIERS = [
    "Your Supplier 1",
    "Your Supplier 2",
    # ... add more
]
```

### Adding/Modifying Sectors

```python
SECTORS = [
    "Your Sector 1",
    "Your Sector 2",
    # ... add more
]
```

---

## 📖 Usage Guide

### Navigation

- **Home** 🏠 - Main invoicing page
- **Reports** 📊 - View and manage saved invoices (coming soon)
- **Settings** ⚙️ - Application settings (coming soon)
- **About** ℹ️ - Software information and version

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Invoice |
| `Ctrl+S` | Save Invoice |
| `Ctrl+P` | Save as PDF |
| `Ctrl+Shift+P` | Print Invoice |
| `Ctrl+I` | Add Item |
| `Del` | Delete Selected Row |
| `Ctrl+Q` | Quit Application |

### Invoice Details Section

**Fields:**
- **Invoice Number**: Auto-generated (format: PREFIX-YYYYMMDD-HHMMSS)
- **Invoice Date**: Calendar picker for date selection
- **Customer Name**: Text input for customer name
- **Contact Number**: Text input for phone/mobile number

**All labels are bold for better readability!**

### Billed Items Table

**Columns:**
1. **Item Name** (200px fixed) - Service/product name
2. **Ticket** - Ticket/booking reference number
3. **Sector** - Dropdown (Domestic, International, etc.)
4. **Supplier** - Dropdown (Airlines, Hotels, etc.) - Editable
5. **Price (₹)** - Unit price with spinner
6. **Qty** - Quantity with spinner
7. **Tax (%)** - Tax percentage with spinner
8. **Amount (₹)** - Auto-calculated (read-only)
9. **Actions** - Delete button (🗑️)

**Row Numbers:** Now displayed in gray color for better visibility

### Invoice Calculation Section

All labels have **fixed width (120px)** and are **bold** for perfect alignment:

- **Subtotal:** Sum of all item amounts before tax
- **Tax:** Total tax amount from all items
- **Total:** Final amount (highlighted in gold)
- **Received:** Amount received from customer (input field)
- **Balance:** Remaining amount (color-coded)
  - 🔴 Red: Amount due
  - 🟢 Green: Overpaid
  - ⚪ Gray: Fully paid

### Action Buttons

- **💾 Save Invoice** (Green) - Save invoice data as JSON
- **📄 Save as PDF** (Red) - Export invoice as PDF file
- **🖨️ Print Invoice** (Purple) - Print invoice directly
- **📤 Share Invoice** (Teal) - Share via email (ready for integration)

---

## 👨‍💻 Development

### Project Setup for Development

```bash
# Clone repository
git clone https://github.com/fidha-jazeel/billing-software.git
cd billing-software3

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

### Code Structure

**Main Components:**

1. **`config/settings.py`**
   - All configuration constants
   - Company information
   - Color themes
   - Default values

2. **`utils/styles.py`**
   - Styling helper functions
   - Widget style generators
   - Theme application utilities

3. **`travel_billing/dashboard_improved.py`**
   - Main application class (`DashboardImproved`)
   - UI creation methods
   - Business logic
   - Event handlers

4. **`main.py`**
   - Application entry point
   - Minimal code for launching

### Adding New Features

**To add a new setting:**

1. Add to `config/settings.py`
2. Import in `dashboard_improved.py`
3. Use throughout application

**To add a new style:**

1. Create function in `utils/styles.py`
2. Return stylesheet string
3. Use with `widget.setStyleSheet()`

**To add a new page:**

1. Create method `_create_<page>_page()` in `DashboardImproved`
2. Add to navigation buttons
3. Add to stacked widget

### Testing

```bash
# Run application
python main.py

# Test invoice creation
# - Create invoice with multiple items
# - Verify calculations
# - Test PDF export
# - Test print functionality
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** "ModuleNotFoundError: No module named 'PyQt5'"
```bash
# Solution:
pip install PyQt5==5.15.9
```

**Issue:** "ModuleNotFoundError: No module named 'config'"
```bash
# Solution: Make sure you're in the correct directory
cd billing-software3
python main.py
```

**Issue:** Application window doesn't appear
```bash
# Solution: Check if another instance is running
# Kill existing processes and try again
```

**Issue:** PDF not saving
```bash
# Solution: Check if 'invoices' directory exists
# Create it manually: mkdir invoices
```

**Issue:** Print dialog doesn't open
```bash
# Solution: Ensure printer drivers are installed
# Check Windows printer settings
```

### Getting Help

1. Check documentation files in project root
2. Review version change logs
3. Check GitHub issues
4. Contact developer: fidha-jazeel

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

1. Check existing issues on GitHub
2. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable

### Suggesting Features

1. Open a feature request issue
2. Describe the feature clearly
3. Explain use case and benefits

### Code Contributions

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Developer

**Fidha Jazeel**  
GitHub: [@fidha-jazeel](https://github.com/fidha-jazeel)

---

## 🙏 Acknowledgments

- PyQt5 team for the excellent GUI framework
- Python community for comprehensive documentation
- All contributors and testers

---

## 📞 Support

For support and queries:
- **Email**: info@travelagency.com
- **GitHub**: [Create an issue](https://github.com/fidha-jazeel/billing-software/issues)

---

## 🔄 Version History

### Version 2.2.0 (Current) - November 16, 2025
- ✅ Fixed key-value widths in invoice details
- ✅ Made all labels bold for better readability
- ✅ Applied professional color theme
- ✅ Converted all static values to dynamic
- ✅ Restructured as professional project
- ✅ Added configuration system
- ✅ Added styling utilities

### Version 2.1.0 - November 16, 2025
- Added Share button functionality
- Fixed white color in serial numbers
- Added dropdown for Supplier column
- Improved calculation section layout
- Added professional print template

### Version 2.0.0 - November 15, 2025
- Complete UI redesign
- Excel-style table implementation
- Real-time calculations
- PDF export functionality
- Multi-page dashboard

---

**Made with ❤️ for Travel Agencies**

_Last Updated: November 16, 2025_
