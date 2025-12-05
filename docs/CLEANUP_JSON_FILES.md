# JSON Files Cleanup Guide

## ✅ Migration Complete - Database Now Active

All billing operations now use SQLite database (`billing.db`). The following JSON folders are **legacy and can be safely archived/deleted**:

### 📁 Folders to Archive/Delete:

1. **`invoices/`** - Old invoice JSON files
   - Status: Replaced by `invoices` and `invoice_items` tables in database
   - Action: Archive to `invoices_backup/` then delete

2. **`expenses/`** - Old expenses.json file  
   - Status: Replaced by `expenses` table in database
   - Action: Archive to `expenses_backup/` then delete

3. **`suppliers/`** - Old suppliers.json file
   - Status: Replaced by `contacts` table (type='SUPPLIER')
   - Action: Archive to `suppliers_backup/` then delete

4. **`supplier_bills/`** - Old supplier bill JSON files
   - Status: Replaced by `purchase_bills` and `purchase_bill_items` tables
   - Action: Archive to `supplier_bills_backup/` then delete

### 🔧 Cleanup Commands (PowerShell):

```powershell
# Create backup directory
New-Item -ItemType Directory -Path "json_backup" -Force

# Move folders to backup (preserves data)
Move-Item -Path "invoices" -Destination "json_backup\invoices_backup"
Move-Item -Path "expenses" -Destination "json_backup\expenses_backup"
Move-Item -Path "suppliers" -Destination "json_backup\suppliers_backup"
Move-Item -Path "supplier_bills" -Destination "json_backup\supplier_bills_backup"

Write-Host "✅ JSON files archived to json_backup folder" -ForegroundColor Green
```

### 📝 Files That KEEP JSON (Configuration Only):

These files use JSON for **settings** (not billing data) and are OK:

- `travel_billing_software/config/settings.json` - App settings
- `travel_billing_software/auth/auth_data.json` - Legacy auth (database is primary now)
- `travel_billing_software/utils/config_manager.py` - Config management

### ⚠️ Important Notes:

1. **Backup First**: The above commands create backups before deletion
2. **Test First**: Run the application and verify all features work before deleting
3. **Database File**: All data is now in `billing.db` - **BACKUP THIS FILE REGULARLY**
4. **No Going Back**: Once JSON files are deleted, you must use the database

### 🧪 Verification Steps:

Before cleanup, test these operations:

```
✓ Create new invoice → Check database
✓ Add expense → Check database
✓ Add supplier → Check database  
✓ Create purchase bill → Check database
✓ Record payment → Check database
✓ View reports → Should show database data
```

### 🎯 Current Status:

- ✅ Database: Fully operational with 13 tables
- ✅ Authentication: Using database (admin/admin)
- ✅ Invoices: Saved to database only
- ✅ Expenses: Saved to database only
- ✅ Suppliers: Saved to database only
- ✅ Purchase Bills: Saved to database only
- ✅ Reports: Loading from database
- ✅ Payments: Database-powered payment tracking
- 🗂️ JSON Folders: Ready for archival

### 📊 Database Schema:

Your billing data is now in these tables:

**Core Tables:**
- `users` - Authentication
- `contacts` - Customers & Suppliers
- `invoices` - Sales invoices
- `invoice_items` - Invoice line items
- `expenses` - Business expenses
- `purchase_bills` - Supplier bills
- `purchase_bill_items` - Bill line items
- `payments_received` - Customer payments
- `supplier_payments` - Supplier payments
- `passengers` - Passenger details
- `passport_details` - Passport information
- `service_types` - Flight, Visa, Hotel, etc.

**Support Tables:**
- `dropdown_sectors`
- `dropdown_classes`
- `settings`

---

**Ready to cleanup?** Run the PowerShell commands above from the project root directory.
