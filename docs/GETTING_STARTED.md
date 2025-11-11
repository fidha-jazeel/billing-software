# 🎯 Getting Started - Visual Guide

## 🖥️ Installation (Windows)

### Method 1: Using Install Script (Easiest!)
```
📂 billing-software/
   └── 📄 install.bat  ← Double-click this file!
```
This will automatically install all required packages.

### Method 2: Manual Installation
```cmd
1. Open Command Prompt in the folder
2. Type: pip install -r requirements.txt
3. Press Enter
```

---

## 🚀 Running the Application

### Method 1: Using Run Script (Easiest!)
```
📂 billing-software/
   └── 📄 run.bat  ← Double-click this file!
```

### Method 2: Command Prompt
```cmd
1. Open Command Prompt in the folder
2. Type: python main.py
3. Press Enter
```

---

## 📱 First Time Setup Flow

```
┌─────────────────────────────────────────────────────┐
│  Application Starts                                  │
│  ↓                                                   │
│  Opens in Maximized Window                          │
│  ↓                                                   │
│  Shows Home Page (Ready to Create Invoice)          │
└─────────────────────────────────────────────────────┘

⚙️ BEFORE FIRST INVOICE:
┌─────────────────────────────────────────────────────┐
│ 1. Click "⚙️ Settings" in sidebar                   │
│ 2. Enter your company information                    │
│ 3. Set invoice prefix (e.g., "INV")                 │
│ 4. Click "💾 Save Settings"                         │
│ 5. Go back to "🏠 Home"                             │
└─────────────────────────────────────────────────────┘
```

---

## 💡 Creating Your First Invoice

```
┌───────────────────────────────────────────────────────────┐
│                      HOME PAGE                            │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ STEP 1: Enter Customer Details                           │
│ ┌──────────────────────┐                                │
│ │ Customer Name: [John Doe          ]                   │
│ │ Contact:       [9876543210        ]                   │
│ └──────────────────────┘                                │
│                                                           │
│ STEP 2: Add Items                                        │
│ [➕ Add Item] button                                     │
│                                                           │
│ ┌──────────────────────────────────────────────────────┐│
│ │ Item    │Ticket│Sector│Supplier│Qty│Price│Tax│Amount││
│ ├─────────┼──────┼──────┼────────┼───┼─────┼───┼──────┤│
│ │ Visa    │T-001 │Dubai │ABC Ltd │ 1 │1000 │18 │1180  ││
│ │ Ticket  │T-002 │London│XYZ Ltd │ 2 │5000 │18 │11800 ││
│ └──────────────────────────────────────────────────────┘│
│                                                           │
│ STEP 3: Review Calculations (Auto-calculated)            │
│ ┌──────────────────────┐                                │
│ │ Subtotal:    ₹11,000 │                                │
│ │ Tax:         ₹ 1,980 │                                │
│ │ Total:       ₹12,980 │                                │
│ │ Received:    ₹10,000 │  ← Enter what customer paid    │
│ │ Balance:     ₹ 2,980 │  ← Auto-calculated             │
│ └──────────────────────┘                                │
│                                                           │
│ STEP 4: Save                                             │
│ [💾 Save Invoice]  [📄 Save as PDF]                     │
│                                                           │
│ ✅ Invoice Saved!                                        │
│    Invoice Number: INV-0001                              │
└───────────────────────────────────────────────────────────┘
```

---

## 📊 Viewing Reports

```
┌───────────────────────────────────────────────────────────┐
│                    REPORTS PAGE                           │
├───────────────────────────────────────────────────────────┤
│                                                           │
│ Date Filters:                                            │
│ [Today] [This Week] [This Month] [All Time]             │
│ Or: From [01-11-25] To [11-11-25] [Apply]              │
│                                                           │
│ Statistics Cards:                                         │
│ ┌──────────┬──────────┬──────────┬──────────┬─────────┐│
│ │💰 Total  │📄 Invoices│✅ Received│⏳ Pending│📊 Avg  ││
│ │  Sales   │          │          │         │  Sale   ││
│ │ ₹12,980  │    1     │ ₹10,000  │ ₹2,980  │₹12,980 ││
│ └──────────┴──────────┴──────────┴──────────┴─────────┘│
│                                                           │
│ Recent Invoices List:                                    │
│ ┌────────────────────────────────────────────────────┐  │
│ │ Invoice  │ Customer │ Date     │ Total   │ Balance │  │
│ ├──────────┼──────────┼──────────┼─────────┼─────────┤  │
│ │ INV-0001 │ John Doe │11-11-25  │ ₹12,980 │ ₹2,980 │  │
│ └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

---

## 📱 Navigation

```
┌────────────────────────────────────────────────────┐
│  Sidebar Menu                                      │
├────────────────────────────────────────────────────┤
│                                                    │
│  🎫 Travel Agency  ← Logo/Title                   │
│                                                    │
│  🏠 Home          ← Create invoices here          │
│  📊 Reports       ← View analytics & history      │
│  ⚙️ Settings      ← Configure company info        │
│  ℹ️ About         ← App information               │
│                                                    │
│  v1.0.0           ← Version                       │
└────────────────────────────────────────────────────┘
```

---

## 🎨 Visual Features

### Dark Theme
```
┌─────────────────────────────────────────┐
│  ████████ Dark Background               │
│  ▒▒▒▒▒▒▒▒ Card Backgrounds              │
│  ████████ Teal Accent Color             │
│  ░░░░░░░░ Light Text                    │
└─────────────────────────────────────────┘
```

### Button Colors
```
🟦 Primary Button - Teal (Save, Apply, etc.)
⬛ Secondary Button - Dark Gray (Reset, Cancel)
🟥 Danger Button - Red (Delete)
```

### Status Colors
```
🟢 Green  - Paid/Completed
🟡 Yellow - Pending/Balance Due
🔵 Blue   - Information
🔴 Red    - Error/Delete
```

---

## 📁 File Locations

### Important Files
```
📂 billing-software/
├── 🚀 run.bat              ← Run this to start app
├── 📦 install.bat          ← Run this first time
├── ⚡ main.py              ← Entry point
├── 💾 billing.db           ← Your data (backup this!)
├── 📋 requirements.txt     ← Dependencies list
└── 📖 README.md            ← Full documentation
```

### Documentation
```
📖 README.md        - Complete guide with all details
🚀 QUICKSTART.md    - Step-by-step beginner guide  
📁 STRUCTURE.md     - Technical architecture
📝 SUMMARY.md       - Project overview
🎯 GETTING_STARTED.md - This file (visual guide)
```

---

## 🔧 Common Tasks

### Creating Invoice
```
1. Home page → Already there on startup
2. Enter customer name (required)
3. Click "➕ Add Item" 
4. Fill item details
5. Click "💾 Save Invoice"
6. Click "📄 Save as PDF" (optional)
```

### Viewing Analytics
```
1. Click "📊 Reports" in sidebar
2. Select date range
3. View statistics cards
4. Browse invoice list
```

### Updating Settings
```
1. Click "⚙️ Settings" in sidebar
2. Update company information
3. Click "💾 Save Settings"
```

### Exporting PDF
```
1. Save invoice first
2. Click "📄 Save as PDF"
3. Choose location
4. PDF is generated!
```

---

## ⚠️ Important Notes

### ✅ DO:
- ✅ Save invoices before exporting to PDF
- ✅ Configure settings before first invoice
- ✅ Backup `billing.db` file regularly
- ✅ Enter customer name (required field)
- ✅ Add at least one item to invoice

### ❌ DON'T:
- ❌ Delete `billing.db` (unless resetting)
- ❌ Edit database file manually
- ❌ Run multiple instances at once
- ❌ Modify Python files without backup

---

## 🆘 Quick Troubleshooting

### Problem: Won't Start
```
Solution:
1. Run install.bat again
2. Check Python is installed: python --version
3. Check dependencies: pip list
```

### Problem: Can't Save Invoice
```
Solution:
1. Check customer name is filled
2. Check at least one item is added
3. Check write permissions in folder
```

### Problem: PDF Won't Generate
```
Solution:
1. Save invoice first!
2. Reinstall reportlab: pip install --force-reinstall reportlab
3. Try different save location
```

### Problem: Database Error
```
Solution:
1. Close application
2. Rename billing.db to billing_backup.db
3. Restart application (creates new database)
```

---

## 🎓 Learning Tips

### For Beginners:
1. Start with QUICKSTART.md
2. Follow visual examples above
3. Try creating test invoice
4. Explore each page
5. Check Reports page

### For Advanced Users:
1. Read STRUCTURE.md for architecture
2. Customize utils/styles.py for colors
3. Modify database schema if needed
4. Add custom features

---

## 📞 Need Help?

### Documentation Order:
```
1. 🎯 GETTING_STARTED.md  ← You are here (Visual guide)
2. 🚀 QUICKSTART.md       ← Step-by-step tutorial
3. 📖 README.md           ← Complete documentation
4. 📁 STRUCTURE.md        ← Technical details
5. 📝 SUMMARY.md          ← Project overview
```

---

## 🎉 Ready to Go!

You now have everything you need to:
- ✅ Install the application
- ✅ Run the application
- ✅ Create invoices
- ✅ View reports
- ✅ Export PDFs
- ✅ Configure settings

### Start Now:
1. Double-click `install.bat` (first time only)
2. Double-click `run.bat`
3. Configure settings
4. Create your first invoice!

---

**Happy Billing! 🚀**

*Simple. Powerful. Beautiful.*
