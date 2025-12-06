# Logging System Documentation

## Overview
Comprehensive logging system with automatic rotation for production error tracking and monitoring.

## Log Files
All logs are stored in: `travel_billing_software/logs/`

### 1. app.log
- **Purpose**: Main application activity log
- **Size**: 10MB per file, 5 backup files (50MB total)
- **Contains**: 
  - Application startup/shutdown
  - User login/logout
  - UI actions (invoice creation, payment records)
  - General application flow

### 2. errors.log
- **Purpose**: Dedicated error tracking with full stack traces
- **Size**: 5MB per file, 10 backup files (50MB total)
- **Contains**:
  - All exceptions and errors
  - Full traceback information
  - Error context and parameters
  - Critical failures

### 3. database.log
- **Purpose**: Database operation tracking
- **Size**: 20MB per file, 3 backup files (60MB total)
- **Contains**:
  - All database operations
  - SQL execution status
  - Success/failure tracking
  - Operation duration

## Log Format
```
2024-01-15 14:30:45,123 - INFO - [module:function:line] - Message
```

Each entry includes:
- Timestamp (millisecond precision)
- Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Source location (module, function, line number)
- Message
- Stack trace (for errors)

## Usage

### Quick Logging (Recommended for UI)
```python
from travel_billing_software.utils.logger import log_info, log_warning, log_error, log_debug

# Simple logging
log_info("User logged in successfully", 'billing_app')
log_warning("Low disk space", 'billing_app')

# Error with exception
try:
    risky_operation()
except Exception as e:
    log_error("Operation failed", exception=e, logger_name='billing_errors')
```

### Advanced Logging (Database Layer)
```python
from travel_billing_software.utils.logger import get_logger

logger = get_logger()

# Database operation logging
logger.log_db_operation(
    "SAVE_INVOICE",
    "invoice_number=INV-001, items=5",
    success=True
)
```

### Decorators (Function-Level Logging)
```python
from travel_billing_software.utils.logger import handle_exceptions, log_db_operation

@handle_exceptions(logger_name='billing_errors', default_return=-1)
def save_data(data):
    # Automatically logs any exceptions
    return database.save(data)

@log_db_operation("UPDATE_CONTACT")
def update_contact(contact_id, **kwargs):
    # Automatically logs operation start/complete/failed
    return db.update_contact(contact_id, **kwargs)
```

### Context Manager (Operation Blocks)
```python
from travel_billing_software.utils.logger import LogOperation

with LogOperation("BULK_IMPORT", logger_name='billing_database'):
    # Everything inside is automatically logged
    for item in items:
        db.save(item)
```

## Current Integration Status

### ✅ Fully Integrated
1. **Database Manager** (`db_manager.py`)
   - Connection logging
   - All critical operations (save_invoice, add_contact, authenticate_user)
   - Payment and expense operations
   - Error tracking with full context

2. **Home Page** (`home.py`)
   - Invoice save operations
   - Success/failure logging
   - Error logging with exceptions

3. **Authentication**
   - Login success/failure
   - Master bypass password usage

### ⏸️ Pending Integration
- Reports page
- Supplier billing page
- Settings changes
- Other UI operations

## Testing
Run the test script to verify logging:
```bash
python test_logging.py
```

This will:
- Create all three log files
- Write test entries
- Test error logging
- Test high-volume logging

## Automatic Features
1. **Log Rotation**: Files automatically rotate when size limit reached
2. **Old File Management**: Keeps specified number of backups, deletes oldest
3. **Console Output**: INFO+ messages also shown in console
4. **Thread-Safe**: Safe for multi-threaded applications
5. **UTF-8 Encoding**: Supports international characters

## Log Levels
- **DEBUG**: Detailed diagnostic information (file only)
- **INFO**: General informational messages (console + file)
- **WARNING**: Warning messages for recoverable issues
- **ERROR**: Error messages with exceptions
- **CRITICAL**: Critical failures requiring immediate attention

## Monitoring Recommendations
1. Check `errors.log` regularly for recurring issues
2. Monitor `database.log` for failed operations
3. Use `app.log` to understand user behavior patterns
4. Set up log rotation monitoring for disk space management

## Benefits
- ✅ Production-ready error tracking
- ✅ No more lost error information
- ✅ Easy debugging with full context
- ✅ Automatic rotation prevents disk overflow
- ✅ Separate logs for different concerns
- ✅ Minimal performance impact
- ✅ Easy integration with existing code
