"""
Quick test script to verify logging system is working
"""
from travel_billing_software.utils.logger import get_logger, log_info, log_warning, log_error, log_debug
import time

def main():
    print("=" * 60)
    print("TESTING LOGGING SYSTEM")
    print("=" * 60)
    
    # Test basic logging functions
    print("\n1. Testing basic log functions...")
    log_info("Application started - Test Mode", 'billing_app')
    log_debug("Debug information test", 'billing_app')
    log_warning("This is a warning test", 'billing_app')
    
    # Test error logging
    print("\n2. Testing error logging with exception...")
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        log_error("Division by zero error test", exception=e, logger_name='billing_errors')
    
    # Test database operation logging
    print("\n3. Testing database operation logging...")
    logger = get_logger()
    logger.log_db_operation("TEST_INVOICE_SAVE", "invoice_number=TEST-001, items=5", success=True)
    logger.log_db_operation("TEST_CONTACT_ADD", "name=John Doe, id=123", success=True)
    
    # Simulate a failed operation
    logger.log_db_operation("TEST_FAILED_OPERATION", "Some error occurred", success=False)
    
    print("\n4. Testing high-volume logging (rotation test)...")
    for i in range(10):
        log_info(f"High volume test message {i+1}", 'billing_app')
        time.sleep(0.1)
    
    print("\n" + "=" * 60)
    print("LOGGING TEST COMPLETE")
    print("=" * 60)
    print("\nCheck the following log files:")
    print("  • travel_billing_software/logs/app.log")
    print("  • travel_billing_software/logs/errors.log")
    print("  • travel_billing_software/logs/database.log")
    print("\nAll logs should contain the test entries.")
    print("=" * 60)

if __name__ == "__main__":
    main()
