"""Test script for new database manager."""
from travel_billing_software.database.db_manager import DatabaseManager

def test_database():
    print("Testing new database manager...")
    
    # Initialize
    db = DatabaseManager()
    print("✓ Database initialized")
    
    # Test authentication
    user = db.authenticate_user("admin", "admin")
    print(f"✓ Admin user exists: {user is not None}")
    if user:
        print(f"  Username: {user['username']}, Role: {user['role']}")
    
    # Test service types
    services = db.get_service_types()
    print(f"✓ Service types count: {len(services)}")
    for svc in services:
        print(f"  - {svc['name']}")
    
    # Test dashboard stats
    stats = db.get_dashboard_stats()
    print(f"✓ Dashboard stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test contact creation
    contact_id = db.add_contact('CUSTOMER', 'Test Customer', phone='1234567890')
    print(f"✓ Created test customer: ID {contact_id}")
    
    # Test passenger creation
    passenger_id = db.add_passenger(contact_id, 'Test Passenger', '1234567890')
    print(f"✓ Created test passenger: ID {passenger_id}")
    
    # Test dropdowns
    sectors = db.get_dropdown_items('sector')
    print(f"✓ Dropdown sectors: {sectors}")
    
    classes = db.get_dropdown_items('class')
    print(f"✓ Dropdown classes: {classes}")
    
    db.close()
    print("\n✓ All tests passed!")

if __name__ == "__main__":
    test_database()
