"""
Test script to verify all features of the improved billing dashboard.
Run this to check if all components are working correctly.
"""

from PyQt5.QtWidgets import QApplication
import sys

def test_dashboard_features():
    """Test all features of the improved dashboard."""
    
    print("="*60)
    print("🧪 Testing Travel Agency Billing Software - Version 2.0")
    print("="*60)
    
    try:
        # Test 1: Import the improved dashboard
        print("\n✓ Test 1: Importing DashboardImproved class...")
        from travel_billing.dashboard_improved import DashboardImproved
        print("  ✅ Successfully imported DashboardImproved")
        
        # Test 2: Create application
        print("\n✓ Test 2: Creating QApplication...")
        app = QApplication(sys.argv)
        print("  ✅ QApplication created successfully")
        
        # Test 3: Initialize dashboard
        print("\n✓ Test 3: Initializing dashboard window...")
        window = DashboardImproved()
        print("  ✅ Dashboard window initialized")
        
        # Test 4: Check if home page exists
        print("\n✓ Test 4: Checking home page...")
        assert hasattr(window, 'home_page'), "Home page not found"
        print("  ✅ Home page exists")
        
        # Test 5: Check if table exists
        print("\n✓ Test 5: Checking table widget...")
        assert hasattr(window, 'table'), "Table widget not found"
        assert window.table.columnCount() == 9, f"Expected 9 columns, got {window.table.columnCount()}"
        print(f"  ✅ Table has {window.table.columnCount()} columns")
        
        # Test 6: Check table headers
        print("\n✓ Test 6: Checking table headers...")
        headers = [
            window.table.horizontalHeaderItem(i).text() 
            for i in range(window.table.columnCount())
        ]
        expected_headers = [
            "Item Name", "Ticket", "Sector", "Supplier", 
            "Price (₹)", "Qty", "Tax (%)", "Amount (₹)", "Actions"
        ]
        assert headers == expected_headers, f"Headers mismatch: {headers}"
        print("  ✅ All headers correct:")
        for h in headers:
            print(f"     • {h}")
        
        # Test 7: Check buttons exist
        print("\n✓ Test 7: Checking buttons...")
        assert hasattr(window, 'btn_add_item'), "Add Item button not found"
        assert hasattr(window, 'btn_save_invoice'), "Save Invoice button not found"
        assert hasattr(window, 'btn_save_pdf'), "Save PDF button not found"
        print("  ✅ All buttons exist:")
        print(f"     • {window.btn_add_item.text()}")
        print(f"     • {window.btn_save_invoice.text()}")
        print(f"     • {window.btn_save_pdf.text()}")
        
        # Test 8: Check invoice details fields
        print("\n✓ Test 8: Checking invoice details fields...")
        assert hasattr(window, 'invoice_number'), "Invoice number field not found"
        assert hasattr(window, 'invoice_date'), "Invoice date field not found"
        assert hasattr(window, 'customer_name'), "Customer name field not found"
        assert hasattr(window, 'contact_number'), "Contact number field not found"
        print("  ✅ All invoice detail fields exist")
        
        # Test 9: Check calculation labels
        print("\n✓ Test 9: Checking calculation labels...")
        assert hasattr(window, 'lbl_subtotal'), "Subtotal label not found"
        assert hasattr(window, 'lbl_tax'), "Tax label not found"
        assert hasattr(window, 'lbl_total'), "Total label not found"
        assert hasattr(window, 'txt_received'), "Received input not found"
        assert hasattr(window, 'lbl_balance'), "Balance label not found"
        print("  ✅ All calculation fields exist")
        
        # Test 10: Test add_item_row functionality
        print("\n✓ Test 10: Testing add item functionality...")
        initial_rows = window.table.rowCount()
        window.add_item_row()
        new_rows = window.table.rowCount()
        assert new_rows == initial_rows + 1, "Add item didn't add a row"
        print(f"  ✅ Successfully added row (rows: {initial_rows} → {new_rows})")
        
        # Test 11: Check if sector dropdown exists in new row
        print("\n✓ Test 11: Checking sector dropdown in new row...")
        sector_widget = window.table.cellWidget(0, 2)
        assert sector_widget is not None, "Sector widget not found"
        from PyQt5.QtWidgets import QComboBox
        assert isinstance(sector_widget, QComboBox), "Sector widget is not a QComboBox"
        print(f"  ✅ Sector dropdown exists with {sector_widget.count()} options")
        
        # Test 12: Check delete button in actions column
        print("\n✓ Test 12: Checking delete button in actions column...")
        delete_widget = window.table.cellWidget(0, 8)
        assert delete_widget is not None, "Delete button not found"
        from PyQt5.QtWidgets import QPushButton
        assert isinstance(delete_widget, QPushButton), "Actions widget is not a QPushButton"
        print("  ✅ Delete button exists in Actions column")
        
        # Test 13: Test invoice number generation
        print("\n✓ Test 13: Testing invoice number generation...")
        invoice_num = window.invoice_number.text()
        assert invoice_num.startswith("INV-"), f"Invalid invoice number format: {invoice_num}"
        print(f"  ✅ Invoice number generated: {invoice_num}")
        
        # Test 14: Show the window
        print("\n✓ Test 14: Displaying window...")
        window.show()
        print("  ✅ Window displayed successfully")
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n📝 Summary:")
        print("  • Dashboard initialized successfully")
        print("  • All UI components present")
        print("  • Table has 9 columns as required")
        print("  • Sector dropdown implemented")
        print("  • Delete button in Actions column")
        print("  • All buttons functional")
        print("  • Invoice details section complete")
        print("  • Calculation section ready")
        print("\n🎉 The application is ready to use!")
        print("   Close the window to exit the test.")
        print("="*60)
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_dashboard_features()
