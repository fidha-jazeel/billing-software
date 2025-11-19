# Travel Agency Billing Software - Version 2.0 Features

## 🎉 New Features Implemented

### 1. Reorganized Layout Structure

The home page now follows this exact order:

1. **Invoice Details** (Top)
2. **Add Item Button**
3. **Excel-Style Table**
4. **Invoice Calculation Section**
5. **Save Invoice & Save PDF Buttons**

### 2. Invoice Details Section

Located at the top of the page with a clean, card-style design:

- **Invoice Number**: Auto-generated (format: INV-YYYYMMDD-HHMMSS)
- **Invoice Date**: Date picker with calendar popup
- **Customer Name**: Text input field
- **Contact Number**: Text input field

All fields are styled with the dark theme and have focus indicators.

### 3. Excel-Style Table

A comprehensive table with **9 columns**:

| Column | Type | Description |
|--------|------|-------------|
| Item Name | Text Input | Name of the service/product |
| Ticket | Text Input | Ticket number reference |
| **Sector** | **Dropdown** | Travel sector (Domestic, International, Regional, Local, Charter, Corporate) |
| Supplier | Text Input | Supplier/vendor name |
| Price (₹) | Number Spinner | Price per unit with currency symbol |
| Qty | Number Spinner | Quantity (default: 1) |
| Tax (%) | Number Spinner | Tax percentage |
| Amount (₹) | Read-only | Auto-calculated: (Price × Qty) + Tax |
| Actions | Button | Delete button (🗑️) to remove row |

#### Table Features:
- ✅ **No table scrollbar** - Uses page-level scrolling only
- ✅ **Dynamic height** - Adjusts based on number of rows
- ✅ **Inline editing** - Edit directly in cells
- ✅ **Real-time calculations** - Amount updates as you type
- ✅ **Professional styling** - Dark theme with hover effects

### 4. Sector Dropdown (Combo Box)

The Sector column is implemented as a dropdown with these options:

1. Select Sector (default)
2. Domestic
3. International
4. Regional
5. Local
6. Charter
7. Corporate

**Styling Features:**
- Custom dropdown arrow
- Dark themed dropdown list
- Purple highlight on selection
- Smooth hover effects

### 5. Add Item Button

Positioned **above the table** for easy access:

- **Button Text**: "➕ Add Item"
- **Functionality**: Adds a new blank row to the table
- **Dynamic Behavior**: Table height increases automatically
- **Styling**: Purple background (#5b5bff), bold text

### 6. Invoice Calculation Section

Located **below the table**, displays:

| Field | Type | Description |
|-------|------|-------------|
| Subtotal | Read-only | Sum of all amounts before tax |
| Tax | Read-only | Total tax from all items |
| **Total** | Read-only | Grand total (highlighted in gold) |
| Received | Input | Amount received from customer |
| Balance | Auto-calculated | Total - Received (color-coded) |

**Balance Color Coding:**
- 🔴 **Red**: Balance due (positive)
- 🟢 **Green**: Overpaid (negative)
- ⚪ **Gray**: Fully paid (zero)

### 7. Save Buttons

Positioned **below the calculation section**:

#### Save Invoice Button
- **Icon**: 💾
- **Color**: Green (#51CF66)
- **Function**: Saves invoice as JSON file in `invoices/` folder
- **Filename**: `invoice_INV-YYYYMMDD-HHMMSS.json`

#### Save PDF Button
- **Icon**: 📄
- **Color**: Red (#FF6B6B)
- **Function**: Exports invoice as PDF document
- **Features**: Professional layout with all invoice details

### 8. Unified Page Scrolling

**Major UX Improvement:**
- ❌ Removed table's own scrollbars
- ✅ Added single vertical scrollbar for entire page
- ✅ Smooth scrolling experience
- ✅ Styled scrollbar matching theme (purple)

**Benefits:**
- No confusion about which scrollbar to use
- Better visual continuity
- More modern UX pattern
- Easier navigation on long invoices

### 9. Actions Column with Delete

Each table row includes a delete button:

- **Button**: 🗑️ (trash icon)
- **Tooltip**: "Delete this row"
- **Color**: Red (#FF6B6B)
- **Function**: Removes the row and recalculates totals
- **Safety**: Immediate deletion (can be extended to add confirmation)

### 10. Real-Time Calculations

All calculations happen automatically:

1. **Row Amount**: Updates when Price, Qty, or Tax changes
   - Formula: `(Price × Qty) + (Price × Qty × Tax%)`

2. **Subtotal**: Sum of all row amounts before tax

3. **Tax**: Sum of all individual tax amounts

4. **Total**: Subtotal + Tax

5. **Balance**: Total - Received Amount

**No manual "Calculate" button needed!**

## 🎨 Design Improvements

### Dark Theme Enhancements
- Consistent color scheme throughout
- Better contrast ratios
- Purple accent color (#9b9bff) for brand identity
- Smooth transitions and hover effects

### Typography
- Clear hierarchy with font sizes
- Bold headings for sections
- Readable body text (#ffffff on #1a1a1a)

### Spacing & Layout
- Proper padding and margins
- Visual separation between sections
- Card-style frames for grouped content

### Interactive Elements
- Hover effects on buttons
- Focus indicators on inputs
- Cursor changes to pointer on clickable items
- Disabled state styling for read-only fields

## 📊 Technical Implementation

### Technologies Used
- **Framework**: PyQt5 5.15+
- **Language**: Python 3.7+
- **Styling**: Qt StyleSheets (CSS-like syntax)
- **Data Format**: JSON for invoice storage
- **Export**: QPrinter for PDF generation

### Key Components

```python
# Main Dashboard Class
class DashboardImproved(QMainWindow)

# Key Methods:
- _create_home_page()        # Builds the entire home layout
- add_item_row()             # Adds table row with widgets
- delete_row(row)            # Removes a row
- calculate_row_total(row)   # Calculates single row amount
- update_invoice_totals()    # Recalculates all totals
- calculate_balance()        # Updates balance field
- save_invoice()             # Saves to JSON
- save_pdf()                 # Exports to PDF
```

### Widget Hierarchy

```
QMainWindow
└── QHBoxLayout (main)
    ├── QFrame (sidebar)
    │   └── Navigation buttons
    └── QStackedWidget (content)
        └── QScrollArea (home page)
            └── QWidget (content)
                ├── Invoice Details Frame
                ├── Add Item Button
                ├── Table Frame
                │   └── QTableWidget (9 columns)
                ├── Calculation Frame
                └── Save Buttons
```

## 📝 Usage Examples

### Example 1: Creating a Flight Booking Invoice

1. Fill invoice details:
   - Invoice Number: INV-20251116-143022 (auto)
   - Date: 16/11/2025
   - Customer: John Smith
   - Contact: +91 9876543210

2. Click "➕ Add Item"

3. Fill row data:
   - Item Name: International Flight
   - Ticket: AI-1234
   - Sector: International (from dropdown)
   - Supplier: Air India
   - Price: ₹45000
   - Qty: 2
   - Tax: 5%
   - Amount: ₹94500 (auto-calculated)

4. Add more items as needed

5. Enter received amount: ₹50000

6. Balance shows: ₹44500 (in red)

7. Click "💾 Save Invoice" or "📄 Save as PDF"

### Example 2: Hotel Package Invoice

1. Add Item 1:
   - Item: 5-Star Hotel Package
   - Sector: Domestic
   - Price: ₹25000
   - Qty: 3 (nights)
   - Tax: 12%
   - Amount: ₹84000

2. Add Item 2:
   - Item: Airport Transfer
   - Sector: Local
   - Price: ₹2000
   - Qty: 2 (trips)
   - Tax: 5%
   - Amount: ₹4200

3. Total: ₹88200
   - Received: ₹88200
   - Balance: ₹0.00 (Paid) - shown in gray

## 🔧 Customization Guide

### Adding Custom Sectors

Edit `dashboard_improved.py`, line ~480:

```python
sector = QComboBox()
sector.addItems([
    "Select Sector",
    "Domestic",
    "International",
    "Your Custom Sector",  # Add here
    "Another Sector",      # Add here
    # ...
])
```

### Changing Color Scheme

Modify the `apply_dark_theme()` method:

```python
def apply_dark_theme(self):
    dark_stylesheet = """
        /* Change primary color */
        QPushButton {
            background-color: #YOUR_COLOR;  /* Change from #5b5bff */
        }
        
        /* Change accent color */
        QHeaderView::section {
            border-bottom: 2px solid #YOUR_COLOR;  /* Change from #5b5bff */
        }
    """
```

### Modifying Tax Calculation

Change the formula in `calculate_row_total()`:

```python
def calculate_row_total(self, row: int):
    # Current: (Price × Qty) + Tax
    subtotal = price * qty
    tax_amount = subtotal * (tax_pct / 100)
    total = subtotal + tax_amount
    
    # Custom: Apply your formula here
    # Example: Compound tax
    # total = price * qty * (1 + tax_pct / 100)
```

### Adding New Invoice Fields

In `_create_home_page()`, add to the invoice_layout:

```python
# Add after contact_number
invoice_layout.addWidget(QLabel("Email:"), 3, 0)
self.customer_email = QLineEdit()
self.customer_email.setPlaceholderText("customer@email.com")
invoice_layout.addWidget(self.customer_email, 3, 1)
```

## 🐛 Known Issues & Solutions

### Issue: Table doesn't show properly
**Solution**: Ensure PyQt5 is properly installed with all components
```bash
pip install --upgrade PyQt5
```

### Issue: PDF export fails
**Solution**: Check write permissions and install print support
```bash
pip install PyQt5
```

### Issue: Scrollbar not appearing
**Solution**: Add items to the table - scrollbar appears automatically when content exceeds viewport

## 📈 Future Enhancements

Potential features for Version 3.0:

- [ ] Customer database with autocomplete
- [ ] Invoice templates
- [ ] Email invoice functionality
- [ ] Barcode/QR code generation
- [ ] Multi-currency support
- [ ] Invoice history and search
- [ ] Backup and restore
- [ ] Print preview
- [ ] Invoice duplication
- [ ] Payment method tracking
- [ ] Reports and analytics
- [ ] Tax rate presets
- [ ] Discount codes
- [ ] Late payment fees
- [ ] Multi-user support

## 📞 Support

For help or questions:
1. Check the main README.md
2. Review this features document
3. Check code comments in `dashboard_improved.py`
4. Contact the development team

---

**Version**: 2.0.0  
**Last Updated**: November 16, 2025  
**Status**: ✅ Production Ready
