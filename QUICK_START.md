# 🚀 Quick Start Guide - Billing Software v2.0

## Installation & Running

### Step 1: Install Dependencies
```bash
pip install PyQt5
```

### Step 2: Run the Application
```bash
python main.py
```

### Step 3: Test Features (Optional)
```bash
python test_features.py
```

## 📋 How to Create Your First Invoice

### 1️⃣ Fill Invoice Details (Top Section)
- **Invoice Number**: Already filled (auto-generated)
- **Invoice Date**: Click to change date if needed
- **Customer Name**: Type the customer's name
- **Contact Number**: Enter phone number

### 2️⃣ Add Items to Invoice

Click the **"➕ Add Item"** button (above the table)

A new row will appear. Fill in:
- **Item Name**: e.g., "Flight Booking to Dubai"
- **Ticket**: e.g., "EK-1234"
- **Sector**: Click dropdown and select (e.g., "International")
- **Supplier**: e.g., "Emirates Airlines"
- **Price**: Enter amount (e.g., 45000)
- **Qty**: Number of items (default is 1)
- **Tax**: Tax percentage (e.g., 5 for 5%)
- **Amount**: Automatically calculated!

### 3️⃣ Add More Items

Click "➕ Add Item" again to add more rows. Repeat step 2.

### 4️⃣ Review Calculations

Look at the **Invoice Calculation** section (below table):
- **Subtotal**: Total before tax
- **Tax**: Total tax amount
- **Total**: Grand total (in gold/yellow)
- **Received**: Enter the amount customer paid
- **Balance**: Shows remaining amount
  - Red = Customer owes money
  - Green = Overpaid
  - Gray = Fully paid

### 5️⃣ Save Invoice

Two options:

**Option A: Save as JSON**
- Click **"💾 Save Invoice"** button
- Saves to `invoices/` folder
- Filename: `invoice_INV-YYYYMMDD-HHMMSS.json`

**Option B: Export as PDF**
- Click **"📄 Save as PDF"** button
- Choose location to save
- Professional PDF invoice created!

### 6️⃣ Delete Items (If Needed)

Click the **🗑️** button in the Actions column to remove a row.

## 🎯 Tips & Tricks

### Quick Invoice Entry
1. Use TAB key to move between fields quickly
2. Use UP/DOWN arrows in number fields (Price, Qty, Tax)
3. Click dropdown arrow or press SPACE in Sector field

### Keyboard Shortcuts
- **TAB**: Next field
- **SHIFT+TAB**: Previous field
- **SPACE**: Open dropdown (when focused on Sector)
- **UP/DOWN**: Adjust numbers in spinners

### Common Sectors
- **Domestic**: Within country travel
- **International**: Cross-border travel
- **Regional**: Regional flights/services
- **Local**: Local transportation
- **Charter**: Private/chartered services
- **Corporate**: Business travel packages

### Calculation Examples

**Example 1: Simple Item**
- Price: ₹10,000
- Qty: 1
- Tax: 5%
- Amount: ₹10,500 (10000 + 5% tax)

**Example 2: Multiple Items**
- Price: ₹5,000
- Qty: 3
- Tax: 10%
- Amount: ₹16,500 (15000 + 10% tax)

**Example 3: No Tax**
- Price: ₹20,000
- Qty: 2
- Tax: 0%
- Amount: ₹40,000 (no tax applied)

## 🎨 Interface Guide

### Color Meanings
- **Purple (#9b9bff)**: Primary actions and highlights
- **Green (#51CF66)**: Success (Save button, overpaid)
- **Red (#FF6B6B)**: Delete/danger (Delete button, balance due)
- **Gold (#FFD700)**: Important info (Total amount)
- **Gray (#888)**: Neutral (Fully paid balance)

### Section Organization

```
┌─────────────────────────────────────────┐
│  📄 Invoice Details                     │  ← Top
│  (Number, Date, Customer, Contact)      │
├─────────────────────────────────────────┤
│  [➕ Add Item] Button                   │
├─────────────────────────────────────────┤
│  🧾 Billed Items Table                  │
│  (9 columns with inline editing)        │
│  • Item Name  • Ticket  • Sector       │
│  • Supplier   • Price   • Qty          │
│  • Tax        • Amount  • Actions      │
├─────────────────────────────────────────┤
│  💰 Invoice Calculation                 │
│  Subtotal | Tax | Total                 │
│  Received | Balance                     │
├─────────────────────────────────────────┤
│  [💾 Save Invoice]  [📄 Save as PDF]   │  ← Bottom
└─────────────────────────────────────────┘
```

### Scrolling
- **One scrollbar**: On the right side of the page
- **Smooth scrolling**: Mouse wheel or drag scrollbar
- **Auto-scroll**: When adding items, page scrolls to show new row

## 🔧 Troubleshooting

### Problem: Can't see the table
**Solution**: Scroll down - the table is below Invoice Details

### Problem: Amount not calculating
**Solution**: 
- Make sure Price, Qty, and Tax have values
- Try changing any value to trigger recalculation

### Problem: Can't select sector
**Solution**: Click the dropdown arrow or press SPACE when focused

### Problem: Delete button not working
**Solution**: Make sure you're clicking the 🗑️ button in the Actions column

### Problem: Save button does nothing
**Solution**: 
- Check if `invoices/` folder exists (auto-created)
- Look for a success message dialog

### Problem: PDF export fails
**Solution**: 
- Ensure PyQt5 is fully installed
- Check write permissions in save location

## 📖 Example Workflow

### Travel Package Invoice

1. **Invoice Details**
   - Customer: Sarah Johnson
   - Contact: +91 9876543210

2. **Item 1: Flight**
   - Item Name: Mumbai to Paris Flight
   - Ticket: AF-5678
   - Sector: International
   - Supplier: Air France
   - Price: ₹55,000
   - Qty: 2 (passengers)
   - Tax: 5%
   - Amount: ₹115,500 (auto)

3. **Item 2: Hotel**
   - Item Name: 5-Star Hotel Paris
   - Ticket: HTL-789
   - Sector: International
   - Supplier: Marriott Hotels
   - Price: ₹15,000
   - Qty: 7 (nights)
   - Tax: 12%
   - Amount: ₹117,600 (auto)

4. **Item 3: Transfer**
   - Item Name: Airport Pickup & Drop
   - Ticket: TRF-101
   - Sector: Local
   - Supplier: Paris Cabs
   - Price: ₹3,000
   - Qty: 2 (trips)
   - Tax: 5%
   - Amount: ₹6,300 (auto)

5. **Calculations**
   - Subtotal: ₹233,000
   - Tax: ₹6,400
   - Total: ₹239,400
   - Received: ₹150,000
   - Balance: ₹89,400 (in red - due)

6. **Save**
   - Click "💾 Save Invoice"
   - Also click "📄 Save as PDF" for customer

## 🎓 Pro Tips

1. **Use Templates**: Create common packages and save them, then modify for each customer

2. **Tax Rates**: 
   - Domestic travel: Usually 5-12%
   - International: Often 0% (tax included in price)
   - Hotels: 12-18% depending on category

3. **Sector Selection**:
   - Choose the most relevant sector for each item
   - Helps in reports and analytics later

4. **Partial Payments**: 
   - Enter received amount even if partial
   - Balance shows what's due
   - Update later when full payment received

5. **PDF for Customers**: 
   - Always save JSON for records
   - Export PDF to send to customer
   - Keep copies organized by invoice number

## 📱 Navigation

### Sidebar Menu
- **🏠 Home**: Main invoicing page (current)
- **📊 Reports**: View past invoices (coming soon)
- **⚙ Settings**: Configure preferences (coming soon)
- **ℹ About**: App information

Click any menu item to switch pages.

## ✅ Checklist for Each Invoice

- [ ] Invoice number generated
- [ ] Date selected
- [ ] Customer name entered
- [ ] Contact number entered
- [ ] At least one item added
- [ ] All item details filled
- [ ] Sector selected for each item
- [ ] Calculations look correct
- [ ] Received amount entered
- [ ] Invoice saved (JSON)
- [ ] PDF exported (if needed for customer)

## 🎉 You're Ready!

Start creating invoices for your travel agency. The interface is designed to be intuitive and fast.

**Need help?** Check:
- `FEATURES_V2.md` - Detailed feature documentation
- `README.md` - General information
- Code comments in `dashboard_improved.py`

**Enjoy billing! ✈️💼**
