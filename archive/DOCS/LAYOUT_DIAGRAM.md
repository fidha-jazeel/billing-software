# 📐 Layout Diagram - Billing Software v2.0

## Visual Layout Structure

```
┌───────────────────────────────────────────────────────────────────────────┐
│  TRAVEL AGENCY - BILLING SOFTWARE                                         │
├─────────┬─────────────────────────────────────────────────────────────────┤
│  MENU   │  HOME PAGE (with unified scrollbar →)                           │
├─────────┼─────────────────────────────────────────────────────────────────┤
│         │  ╔═══════════════════════════════════════════════════════╗      │
│  🏠     │  ║  📄 INVOICE DETAILS                                   ║      │
│  Home   │  ╠═══════════════════════════════════════════════════════╣      │
│ (Active)│  ║  Invoice Number: [INV-20251116-123456    ]          ║      │
│         │  ║  Invoice Date:   [16/11/2025 ▼]                     ║      │
│ ───────│  ║                                                       ║      │
│         │  ║  Customer Name:  [________________]                   ║      │
│  📊     │  ║  Contact Number: [________________]                   ║      │
│ Reports │  ╚═══════════════════════════════════════════════════════╝      │
│         │                                                                  │
│ ───────│                [➕ Add Item]                                    │
│         │                                                                  │
│  ⚙     │  ╔═══════════════════════════════════════════════════════╗      │
│Settings │  ║  🧾 BILLED ITEMS                                      ║      │
│         │  ╠═══╤═══════╤════════╤══════════╤═══════╤═════╤══════╤═╣      │
│ ───────│  ║ # │ Item  │ Ticket │  Sector  │ Supp. │Price│ Qty  │…║      │
│         │  ╠═══╪═══════╪════════╪══════════╪═══════╪═════╪══════╪═╣      │
│  ℹ     │  ║ 1 │[_____]│[_____] │[Dropdown▼]│[____]│[___]│[__]│…║      │
│  About  │  ║ 2 │[_____]│[_____] │[Dropdown▼]│[____]│[___]│[__]│…║      │
│         │  ║ 3 │[_____]│[_____] │[Dropdown▼]│[____]│[___]│[__]│…║      │
│         │  ║…│  …   │  …   │    …     │  …  │ …  │ …  │…║      │
│         │  ╠═══╧═══════╧════════╧══════════╧═══════╧═════╧══════╧═╣      │
│         │  ║                                                       ║      │
│         │  ║  (Continues for more rows…)                          ║      │
│         │  ║  (No scrollbar in table - uses page scroll)          ║      │
│         │  ╚═══════════════════════════════════════════════════════╝      │
│         │                                                                  │
│         │  ╔═══════════════════════════════════════════════════════╗      │
│         │  ║  💰 INVOICE CALCULATION                               ║      │
│         │  ╠═══════════════════════════════════════════════════════╣      │
│         │  ║  Subtotal:  ₹25,000.00    Tax:    ₹1,250.00         ║      │
│         │  ║  Total:     ₹26,250.00 ← (highlighted in gold)        ║      │
│         │  ║                                                       ║      │
│         │  ║  Received:  [₹20,000    ]  Balance: ₹6,250.00 ← (red)║      │
│         │  ╚═══════════════════════════════════════════════════════╝      │
│         │                                                                  │
│         │                [💾 Save Invoice]  [📄 Save as PDF]             │
│         │                                                                  │
└─────────┴─────────────────────────────────────────────────────────────────┘
```

## Detailed Component Breakdown

### 1. Sidebar (Left - 200px wide)
```
┌─────────┐
│ 🏢 Menu │
├─────────┤
│ 🏠 Home │ ← Active (purple bg)
│         │
│ 📊 Rep. │
│         │
│ ⚙ Set. │
│         │
│ ℹ About│
│         │
│    ↓    │
│ (space) │
└─────────┘
```

### 2. Invoice Details Section (Top)
```
╔═══════════════════════════════════════════════╗
║  📄 Invoice Details                           ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Row 1:                                       ║
║  [Label: Invoice Number] [Input: Auto-gen]   ║
║  [Label: Invoice Date  ] [DatePicker with ▼] ║
║                                               ║
║  Row 2:                                       ║
║  [Label: Customer Name ] [Input: _________]   ║
║  [Label: Contact Number] [Input: _________]   ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

### 3. Add Item Button
```
┌──────────────────────────────────────┐
│                                      │
│         [➕ Add Item]               │  ← Purple button
│                                      │  ← Right-aligned
└──────────────────────────────────────┘
```

### 4. Excel-Style Table (9 Columns)
```
╔═══════════════════════════════════════════════════════════════════╗
║  🧾 Billed Items                                                  ║
╠═══╤════════╤═══════╤═════════╤═══════╤════════╤═════╤═════╤══════╣
║ # │  Item  │Ticket │ Sector  │Suppli.│ Price  │ Qty │ Tax │Amount║Actions
╠═══╪════════╪═══════╪═════════╪═══════╪════════╪═════╪═════╪══════╣
║ 1 │[______]│[_____]│[Drop▼]  │[_____]│[₹____] │[__] │[_%] │₹0.00 ║[🗑️]
║ 2 │[______]│[_____]│[Drop▼]  │[_____]│[₹____] │[__] │[_%] │₹0.00 ║[🗑️]
║ 3 │[______]│[_____]│[Drop▼]  │[_____]│[₹____] │[__] │[_%] │₹0.00 ║[🗑️]
║ … │   …    │  …    │   …     │  …    │   …    │ …   │ …   │  …   ║ …
╚═══╧════════╧═══════╧═════════╧═══════╧════════╧═════╧═════╧══════╝

Column Details:
1. Item Name   - Text input [editable]
2. Ticket      - Text input [editable]
3. Sector      - Dropdown   [Select, Domestic, Intl, Regional, Local, Charter, Corp]
4. Supplier    - Text input [editable]
5. Price (₹)   - Number     [editable, spinner controls]
6. Qty         - Number     [editable, spinner controls]
7. Tax (%)     - Number     [editable, spinner controls]
8. Amount (₹)  - Text       [read-only, auto-calculated, gold color]
9. Actions     - Button     [🗑️ delete button, red color]
```

### 5. Invoice Calculation Section
```
╔═══════════════════════════════════════════════╗
║  💰 Invoice Calculation                       ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  Row 1:                                       ║
║  Subtotal: ₹25,000.00  │  Tax: ₹1,250.00     ║
║  Total: ₹26,250.00 ← (Gold, highlighted)      ║
║                                               ║
║  Row 2:                                       ║
║  Received: [₹20,000    ]  │  Balance: ₹6,250 ║
║                           ↑               ↑   ║
║                      [editable]     [auto-calc]║
║                                    (color-coded)║
╚═══════════════════════════════════════════════╝

Balance Colors:
• Red (#FF6B6B)   - Money owed (positive balance)
• Green (#51CF66) - Overpaid (negative balance)
• Gray (#888888)  - Fully paid (zero balance)
```

### 6. Save Buttons (Bottom)
```
┌─────────────────────────────────────────────┐
│                                             │
│                                             │
│          [💾 Save Invoice]  [📄 Save PDF]  │  ← Right-aligned
│          (Green button)    (Red button)     │
│                                             │
└─────────────────────────────────────────────┘
```

## Scrolling Behavior

```
┌────────────────────────────────┐
│ Invoice Details        ↑       │
│ (visible)              │       │
├────────────────────────┤       │
│ Add Item Button        │       │
├────────────────────────┤       │
│ Table (partial)        │       │  ← Single
│   Row 1                │       │     vertical
│   Row 2                │       │     scrollbar
│   Row 3                │       │     for entire
│   …                  ┃scroll┃  │     page
├────────────────────────┤       │
│ Calculation            │       │
├────────────────────────┤       │
│ Save Buttons           ↓       │
│ (visible)                      │
└────────────────────────────────┘

Features:
• No table-specific scrollbar
• Smooth mouse wheel scrolling
• Auto-scroll when adding rows
• Dynamic table height adjustment
```

## Color Scheme Visual

```
┌──────────────────────────────────────────┐
│ Background:    ██ #1a1a1a (Dark)         │
│ Text:          ██ #ffffff (White)        │
│ Primary:       ██ #5b5bff (Purple)       │
│ Accent:        ██ #9b9bff (Light Purple) │
│ Success:       ██ #51CF66 (Green)        │
│ Danger:        ██ #FF6B6B (Red)          │
│ Highlight:     ██ #FFD700 (Gold)         │
│ Border:        ██ #444444 (Gray)         │
│ Input BG:      ██ #2a2a2a (Dark Gray)    │
└──────────────────────────────────────────┘
```

## Interactive States

### Button States
```
Normal:    [  Button  ]  ← Purple (#5b5bff)
Hover:     [  Button  ]  ← Light Purple (#7a7aff)
Pressed:   [  Button  ]  ← Dark Purple (#4a4aee)
```

### Input States
```
Normal:    [_________]  ← Border: #444
Focus:     [_________]  ← Border: #9b9bff (purple)
Read-only: [_________]  ← BG: #2a2a2a, Text: gold
```

### Dropdown State
```
Closed:    [Select Sector ▼]
Opened:    [Select Sector ▼]
           ┌─────────────────┐
           │ Select Sector   │
           │ Domestic        │ ← Hover: purple
           │ International   │
           │ Regional        │
           │ Local           │
           │ Charter         │
           │ Corporate       │
           └─────────────────┘
```

## Responsive Behavior

### Window Size: 1200 x 750 (default)
```
┌──────────────────────────────────────────┐
│ Full layout visible                      │
│ All sections fit comfortably             │
│ Optimal viewing experience               │
└──────────────────────────────────────────┘
```

### Window Resized (smaller)
```
┌─────────────────────┐
│ Sidebar fixed       │  ← Sidebar stays 200px
│ Content compresses  │  ← Content area shrinks
│ Scrollbar active    │  ← Scroll to see all
└─────────────────────┘
```

### Window Resized (larger)
```
┌──────────────────────────────────────────────────┐
│ Sidebar fixed                                    │
│ Content area expands                             │
│ More breathing room                              │
│ Better visibility                                │
└──────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User Input
    ↓
[Price Field Changes]
    ↓
calculate_row_total(row)
    ↓
[Updates Amount for that row]
    ↓
update_invoice_totals()
    ↓
[Recalculates Subtotal, Tax, Total]
    ↓
calculate_balance()
    ↓
[Updates Balance with color]
    ↓
Display Updated Values
```

## Typical User Flow

```
1. Open Application
       ↓
2. Auto-fill Invoice Details
   (Number, Date)
       ↓
3. Enter Customer Info
   (Name, Contact)
       ↓
4. Click "Add Item"
       ↓
5. Fill Item Details
   • Name, Ticket, Sector (dropdown)
   • Supplier, Price, Qty, Tax
       ↓
6. Amount Auto-Calculated
       ↓
7. Repeat 4-6 for more items
       ↓
8. Review Calculations
   (Subtotal, Tax, Total)
       ↓
9. Enter Received Amount
       ↓
10. Check Balance
       ↓
11. Save Invoice (JSON)
    or
    Save as PDF
       ↓
12. Done! ✅
```

## Section Spacing

```
┌─────────────────────────┐
│ Invoice Details         │  ← 20px margin
│                         │
└─────────────────────────┘
   ↕ 15px spacing
┌─────────────────────────┐
│ [Add Item Button]       │
└─────────────────────────┘
   ↕ 15px spacing
┌─────────────────────────┐
│ Table                   │
│                         │
│                         │
└─────────────────────────┘
   ↕ 15px spacing
┌─────────────────────────┐
│ Calculation             │
└─────────────────────────┘
   ↕ 15px spacing
┌─────────────────────────┐
│ [Save Buttons]          │
└─────────────────────────┘
   ↕ 20px bottom margin
```

---

**This layout ensures:**
- ✅ Logical top-to-bottom workflow
- ✅ Excel-like familiarity
- ✅ Easy navigation
- ✅ Professional appearance
- ✅ Optimal space utilization
- ✅ Consistent styling
- ✅ Clear visual hierarchy

