# 📁 Project Structure Overview

```
billing-software/
│
├── 📄 main.py                      # Application entry point - Run this file
│
├── 📦 database/                    # Database layer
│   ├── __init__.py
│   └── db_manager.py              # SQLite operations & CRUD functions
│
├── 🎨 ui/                          # User interface components
│   ├── __init__.py
│   ├── main_window.py             # Main window with sidebar navigation
│   ├── home_page.py               # Billing/Invoice creation page
│   ├── reports_page.py            # Analytics and reports page
│   ├── settings_page.py           # Application settings page
│   └── about_page.py              # About information page
│
├── 🛠️ utils/                       # Utility modules
│   ├── __init__.py
│   ├── styles.py                  # Dark theme stylesheet
│   └── pdf_generator.py           # PDF invoice generator
│
├── 💾 billing.db                  # SQLite database (auto-created on first run)
│
├── 📋 requirements.txt            # Python dependencies
├── 📋 pyproject.toml              # Project configuration
├── 📖 README.md                   # Full documentation
├── 🚀 QUICKSTART.md               # Quick start guide
└── 📁 STRUCTURE.md                # This file
```

## 🗂️ Database Schema

### Tables Created Automatically:

```
┌─────────────────────────────────────────────────────────────┐
│                      billing.db                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📋 customers                                                │
│     - id (PRIMARY KEY)                                       │
│     - name                                                    │
│     - contact_number                                          │
│     - email                                                   │
│     - address                                                 │
│     - created_at                                              │
│                                                               │
│  📦 items                                                     │
│     - id (PRIMARY KEY)                                       │
│     - name                                                    │
│     - description                                             │
│     - default_price                                           │
│     - created_at                                              │
│                                                               │
│  📄 invoices                                                 │
│     - id (PRIMARY KEY)                                       │
│     - invoice_number (UNIQUE)                                │
│     - customer_id (FOREIGN KEY)                              │
│     - customer_name                                           │
│     - invoice_date                                            │
│     - subtotal                                                │
│     - tax_amount                                              │
│     - total_amount                                            │
│     - received_amount                                         │
│     - balance                                                 │
│     - status                                                  │
│     - notes                                                   │
│     - created_at                                              │
│                                                               │
│  📝 invoice_items                                            │
│     - id (PRIMARY KEY)                                       │
│     - invoice_id (FOREIGN KEY)                               │
│     - item_name                                               │
│     - ticket_number                                           │
│     - sector                                                  │
│     - supplier                                                │
│     - quantity                                                │
│     - price_per_unit                                          │
│     - tax_percentage                                          │
│     - tax_amount                                              │
│     - amount                                                  │
│     - cash                                                    │
│     - bank                                                    │
│     - balance                                                 │
│     - profit                                                  │
│                                                               │
│  ⚙️ settings                                                 │
│     - id (PRIMARY KEY)                                       │
│     - company_name                                            │
│     - company_address                                         │
│     - company_contact                                         │
│     - company_email                                           │
│     - company_gst                                             │
│     - invoice_prefix                                          │
│     - last_invoice_number                                     │
│     - currency_symbol                                         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 UI Page Flow

```
┌──────────────────────────────────────────────────────┐
│                   Main Window                        │
│  ┌────────────┬──────────────────────────────────┐ │
│  │  Sidebar   │       Content Area                │ │
│  │            │                                    │ │
│  │ 🎫 Logo    │  ┌──────────────────────────┐   │ │
│  │            │  │                            │   │ │
│  │ 🏠 Home    │  │    Active Page Content     │   │ │
│  │            │  │                            │   │ │
│  │ 📊 Reports │  │  (Home / Reports /         │   │ │
│  │            │  │   Settings / About)        │   │ │
│  │ ⚙️ Settings│  │                            │   │ │
│  │            │  └──────────────────────────┘   │ │
│  │ ℹ️ About   │                                    │ │
│  │            │                                    │ │
│  │            │                                    │ │
│  │  v1.0.0    │                                    │ │
│  └────────────┴──────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

## 🏠 Home Page Layout

```
┌─────────────────────────────────────────────────────────┐
│  Welcome to Travel Agency Billing 🚀                    │
│  ┌───────────────────┐  ┌───────────────────┐         │
│  │ 📝 Invoice Details│  │ 👤 Bill To        │         │
│  │ - Number: INV-001 │  │ - Customer Name   │         │
│  │ - Date: 11-11-25  │  │ - Contact Number  │         │
│  └───────────────────┘  └───────────────────┘         │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 📋 Billed Items                   [➕ Add Item] │ │
│  ├──────┬─────────┬────────┬─────────┬──────┬────┤ │
│  │ Item │Ticket # │ Sector │Supplier │ Qty  │ $  │ │
│  ├──────┼─────────┼────────┼─────────┼──────┼────┤ │
│  │      │         │        │         │      │    │ │
│  └──────┴─────────┴────────┴─────────┴──────┴────┘ │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 🧮 Invoice Calculation                           │ │
│  │   Subtotal:         ₹ 0.00                       │ │
│  │   Tax Amount:       ₹ 0.00                       │ │
│  │   Total Amount:     ₹ 0.00                       │ │
│  │   Received:         ₹ 0.00                       │ │
│  │   ┌────────────────────────────────────┐        │ │
│  │   │ Balance:        ₹ 0.00             │        │ │
│  │   └────────────────────────────────────┘        │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│               [💾 Save Invoice]  [📄 Save as PDF]     │
└─────────────────────────────────────────────────────────┘
```

## 📊 Reports Page Layout

```
┌─────────────────────────────────────────────────────────┐
│  📊 Reports & Analytics                    [🔄 Refresh] │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Date Range: [Today][Week][Month][All] [Apply]   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────┬──────────┬──────────┬──────────┐       │
│  │💰 Total  │📄 Total  │✅ Received│⏳ Pending│       │
│  │  Sales   │ Invoices │           │          │       │
│  │ ₹ 0.00   │    0     │  ₹ 0.00  │  ₹ 0.00  │       │
│  └──────────┴──────────┴──────────┴──────────┘       │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 📋 Recent Invoices                               │ │
│  ├──────────┬─────────┬──────┬────────┬──────────┤ │
│  │Invoice # │Customer │ Date │ Total  │ Balance  │ │
│  ├──────────┼─────────┼──────┼────────┼──────────┤ │
│  │          │         │      │        │          │ │
│  └──────────┴─────────┴──────┴────────┴──────────┘ │
└─────────────────────────────────────────────────────────┘
```

## ⚙️ Settings Page Layout

```
┌─────────────────────────────────────────────────────────┐
│  ⚙️ Settings                                            │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 🏢 Company Information                           │ │
│  │  Company Name:     [________________]            │ │
│  │  Address:          [________________]            │ │
│  │  Contact:          [________________]            │ │
│  │  Email:            [________________]            │ │
│  │  GST Number:       [________________]            │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │ 📄 Invoice Settings                              │ │
│  │  Invoice Prefix:   [INV___]                      │ │
│  │  Currency Symbol:  [₹]                           │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│                      [💾 Save Settings] [🔄 Reset]     │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Color Scheme (Dark Theme)

```
Primary Colors:
├─ Background:      #1e1e1e (Dark Gray)
├─ Card Background: #252525 (Lighter Dark Gray)
├─ Primary Accent:  #0d7377 (Teal)
├─ Text:            #e0e0e0 (Light Gray)
├─ Border:          #3a3a3a (Medium Gray)
├─ Success:         #4CAF50 (Green)
├─ Warning:         #FF9800 (Orange)
└─ Error:           #c9302c (Red)
```

## 🔄 Application Flow

```
Start Application
      │
      ├─> Initialize Database (if not exists)
      ├─> Load Settings
      ├─> Apply Dark Theme
      ├─> Show Main Window (Home Page)
      │
User Actions:
      │
      ├─> Create Invoice
      │   ├─> Enter Customer Details
      │   ├─> Add Items
      │   ├─> Calculate Totals
      │   ├─> Save to Database
      │   └─> Export to PDF (optional)
      │
      ├─> View Reports
      │   ├─> Apply Date Filters
      │   ├─> View Analytics
      │   └─> Browse Invoices
      │
      ├─> Configure Settings
      │   ├─> Update Company Info
      │   └─> Save Settings
      │
      └─> Exit Application
```

## 📦 Dependencies

```
Python 3.10+
    │
    ├─> PyQt6 (>=6.6.0)
    │   └─> GUI Framework
    │       ├─> Widgets
    │       ├─> Layouts
    │       └─> Event Handling
    │
    └─> reportlab (>=4.0.0)
        └─> PDF Generation
            ├─> Document Templates
            ├─> Tables
            └─> Styling
```

## 🚀 Execution Flow

```
python main.py
    │
    └─> main()
        │
        ├─> QApplication
        ├─> Apply Dark Theme
        ├─> Initialize DatabaseManager
        ├─> Create MainWindow
        ├─> Create Pages:
        │   ├─> HomePage
        │   ├─> ReportsPage
        │   ├─> SettingsPage
        │   └─> AboutPage
        ├─> Add Pages to MainWindow
        ├─> Switch to Home Page
        ├─> Show Window (Maximized)
        └─> Start Event Loop
```

---

**This structure ensures:**
- ✅ Clean separation of concerns
- ✅ Easy to maintain and extend
- ✅ Modular architecture
- ✅ Reusable components
- ✅ Clear data flow
