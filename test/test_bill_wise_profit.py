"""
Test file for Bill Wise Profit Report
Tests the BillWiseProfitView with actual database data
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from travel_billing_software.ui.reports.sub_pages.bill_wise_profit import BillWiseProfitView
from travel_billing_software.database.db_manager import get_db_instance
from travel_billing_software.database.db_operations import ReportsDBOperations
from datetime import datetime


class TestWindow(QMainWindow):
    """Test window for Bill Wise Profit view"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bill Wise Profit Test")
        self.setGeometry(100, 100, 1400, 800)
        
        # Colors dictionary
        self.colors = {
            'primary_bg': '#1e1e2e',
            'secondary_bg': '#2a2a3e',
            'tertiary_bg': '#363650',
            'text_primary': '#ffffff',
            'text_secondary': '#b4b4c8',
            'success': '#00ff00',
            'danger': '#ff0000',
            'warning': '#ffa500',
            'accent_cyan': '#00ffff',
            'accent_gold': '#ffd700',
            'accent_primary': '#4a90e2',  # Added missing color
            'button_bg': '#4a4a6a',
            'button_hover': '#5a5a7a'
        }
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Test controls
        controls = QWidget()
        controls_layout = QVBoxLayout(controls)
        
        # Load button
        load_btn = QPushButton("Load from Database")
        load_btn.clicked.connect(self.load_data)
        controls_layout.addWidget(load_btn)
        
        # Test with sample data button
        test_sample_btn = QPushButton("Test with Sample Data")
        test_sample_btn.clicked.connect(self.test_sample_data)
        controls_layout.addWidget(test_sample_btn)
        
        # Debug button
        debug_btn = QPushButton("Debug Database Structure")
        debug_btn.clicked.connect(self.debug_database)
        controls_layout.addWidget(debug_btn)
        
        layout.addWidget(controls)
        
        # Create Bill Wise Profit view
        self.bill_wise_profit = BillWiseProfitView(
            colors=self.colors,
            get_button_style=self.get_button_style,
            export_callback=self.export_callback
        )
        layout.addWidget(self.bill_wise_profit)
        
        self.db = get_db_instance()
        self.db_operations = ReportsDBOperations()
        
        print("✅ Test window initialized")
    
    def get_button_style(self, btn_type='add'):
        """Return button style"""
        if btn_type == 'add':
            return f"""
                QPushButton {{
                    background-color: {self.colors['button_bg']};
                    color: {self.colors['text_primary']};
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.colors['button_hover']};
                }}
            """
        return ""
    
    def export_callback(self, report_name, format_type):
        """Export callback"""
        print(f"Export {report_name} as {format_type}")
    
    def debug_database(self):
        """Debug database structure and content"""
        print("\n" + "="*80)
        print("DATABASE STRUCTURE DEBUG")
        print("="*80)
        
        try:
            # Get raw invoices
            print("\n1. Raw Invoices from DB:")
            invoices = self.db.get_all_invoices()
            print(f"   Total invoices: {len(invoices)}")
            
            if invoices:
                first_invoice = invoices[0]
                print(f"\n   First invoice structure:")
                print(f"   ID: {first_invoice.get('id')}")
                print(f"   Invoice Number: {first_invoice.get('invoice_number')}")
                print(f"   Date: {first_invoice.get('date')}")
                print(f"   Customer Name: {first_invoice.get('customer_name')}")
                print(f"   Total: {first_invoice.get('total_amount')}")
                print(f"   Payment Status: {first_invoice.get('payment_status')}")
                
                # Get items for first invoice
                print(f"\n2. Invoice Items for Invoice ID {first_invoice.get('id')}:")
                items = self.db.get_invoice_items(first_invoice['id'])
                print(f"   Total items: {len(items)}")
                
                if items:
                    first_item = items[0]
                    print(f"\n   First item structure:")
                    for key, value in dict(first_item).items():
                        print(f"   {key}: {value}")
                else:
                    print("   ⚠️ No items found for this invoice!")
            else:
                print("   ⚠️ No invoices found in database!")
            
            # Test ReportsDBOperations
            print("\n3. Testing ReportsDBOperations.load_all_invoices():")
            formatted_invoices = self.db_operations.load_all_invoices()
            print(f"   Total formatted invoices: {len(formatted_invoices)}")
            
            if formatted_invoices:
                first = formatted_invoices[0]
                print(f"\n   First formatted invoice structure:")
                print(f"   Invoice Number: {first.get('invoice_number')}")
                print(f"   Invoice Date: {first.get('invoice_date')}")
                print(f"   Customer Name: {first.get('customer_name')}")
                print(f"   Total Amount: {first.get('total_amount')}")
                print(f"   Passengers: {len(first.get('passengers', []))} passengers")
                print(f"   Tickets: {len(first.get('tickets', []))} tickets")
                
                if first.get('tickets'):
                    print(f"\n   First ticket structure:")
                    ticket = first['tickets'][0]
                    for key, value in ticket.items():
                        print(f"   {key}: {value}")
                else:
                    print("   ⚠️ No tickets in formatted invoice!")
                
                if first.get('passengers'):
                    print(f"\n   First passenger structure:")
                    passenger = first['passengers'][0]
                    for key, value in passenger.items():
                        print(f"   {key}: {value}")
                else:
                    print("   ⚠️ No passengers in formatted invoice!")
            else:
                print("   ⚠️ No formatted invoices!")
            
            print("\n" + "="*80)
            
        except Exception as e:
            print(f"❌ Error during debug: {e}")
            import traceback
            traceback.print_exc()
    
    def load_data(self):
        """Load real data from database"""
        print("\n" + "="*80)
        print("LOADING DATA FROM DATABASE")
        print("="*80)
        
        try:
            # Load invoices using ReportsDBOperations
            invoices = self.db_operations.load_all_invoices()
            print(f"✅ Loaded {len(invoices)} invoices from database")
            
            if invoices:
                # Print summary
                total_items = sum(len(inv.get('tickets', [])) for inv in invoices)
                print(f"   Total items across all invoices: {total_items}")
                
                # Show first invoice details
                first = invoices[0]
                print(f"\n   First invoice:")
                print(f"   - Invoice #: {first.get('invoice_number')}")
                print(f"   - Date: {first.get('invoice_date')}")
                print(f"   - Customer: {first.get('customer_name')}")
                print(f"   - Passengers: {len(first.get('passengers', []))}")
                print(f"   - Tickets: {len(first.get('tickets', []))}")
                
                # Populate the view
                print(f"\n   Populating Bill Wise Profit view...")
                self.bill_wise_profit.populate(invoices)
                print(f"✅ Bill Wise Profit view populated successfully!")
                
                # Check table row count
                row_count = self.bill_wise_profit.bill_wise_profit_table.rowCount()
                print(f"   Table now has {row_count} rows")
                
            else:
                print("⚠️ No invoices found in database")
                self.bill_wise_profit.populate([])
            
            print("="*80 + "\n")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            import traceback
            traceback.print_exc()
    
    def test_sample_data(self):
        """Test with sample data"""
        print("\n" + "="*80)
        print("TESTING WITH SAMPLE DATA")
        print("="*80)
        
        sample_invoices = [
            {
                'invoice_number': 'INV-001',
                'invoice_date': '10/12/2024',
                'customer_name': 'Test Customer 1',
                'contact_number': '1234567890',
                'total_amount': 50000.00,
                'paid_amount': 30000.00,
                'balance': 20000.00,
                'payment_status': 'PARTIAL',
                'passengers': [
                    {'name': 'John Doe', 'contact_number': '9876543210'},
                    {'name': 'Jane Smith', 'contact_number': '9876543211'}
                ],
                'tickets': [
                    {
                        'pnr': 'ABC123',
                        'ticket_number': 'TKT001',
                        'supplier_name': 'Emirates',
                        'sector': 'DEL-DXB',
                        'booking_type': 'Flight',
                        'quantity': 1,
                        'supplier_amount': 20000.00,
                        'total_amount': 25000.00,
                        'passport_number': 'P1234567',
                        'passenger_name': 'John Doe',
                        'travel_date': '15/12/2024',
                        'unit_price': 25000.00
                    },
                    {
                        'pnr': 'XYZ789',
                        'ticket_number': 'TKT002',
                        'supplier_name': 'Air India',
                        'sector': 'DXB-DEL',
                        'booking_type': 'Flight',
                        'quantity': 1,
                        'supplier_amount': 18000.00,
                        'total_amount': 25000.00,
                        'passport_number': 'P7654321',
                        'passenger_name': 'Jane Smith',
                        'travel_date': '20/12/2024',
                        'unit_price': 25000.00
                    }
                ]
            },
            {
                'invoice_number': 'INV-002',
                'invoice_date': '09/12/2024',
                'customer_name': 'Test Customer 2',
                'contact_number': '5555555555',
                'total_amount': 30000.00,
                'paid_amount': 30000.00,
                'balance': 0.00,
                'payment_status': 'PAID',
                'passengers': [
                    {'name': 'Mike Johnson', 'contact_number': '1111111111'}
                ],
                'tickets': [
                    {
                        'pnr': 'DEF456',
                        'ticket_number': 'TKT003',
                        'supplier_name': 'Qatar Airways',
                        'sector': 'BOM-DOH',
                        'booking_type': 'Flight',
                        'quantity': 1,
                        'supplier_amount': 22000.00,
                        'total_amount': 30000.00,
                        'passport_number': 'P9999999',
                        'passenger_name': 'Mike Johnson',
                        'travel_date': '25/12/2024',
                        'unit_price': 30000.00
                    }
                ]
            }
        ]
        
        print(f"Sample data: {len(sample_invoices)} invoices")
        print(f"Total items: {sum(len(inv['tickets']) for inv in sample_invoices)}")
        
        # Populate view
        self.bill_wise_profit.populate(sample_invoices)
        
        # Check results
        row_count = self.bill_wise_profit.bill_wise_profit_table.rowCount()
        print(f"✅ Table populated with {row_count} rows")
        print("="*80 + "\n")


def main():
    """Main test function"""
    print("\n" + "="*80)
    print("BILL WISE PROFIT TEST")
    print("="*80)
    print("This test will:")
    print("1. Create a test window")
    print("2. Initialize BillWiseProfitView")
    print("3. Load data from the database")
    print("4. Display the results")
    print("="*80 + "\n")
    
    app = QApplication(sys.argv)
    
    # Set dark theme
    app.setStyle('Fusion')
    
    window = TestWindow()
    window.show()
    
    # Auto-load data on startup
    print("Auto-loading database data...")
    window.debug_database()
    window.load_data()
    
    print("\n✅ Test window is ready!")
    print("   - Click 'Load from Database' to reload real data")
    print("   - Click 'Test with Sample Data' to test with mock data")
    print("   - Click 'Debug Database Structure' to see database details")
    print("\n")
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
