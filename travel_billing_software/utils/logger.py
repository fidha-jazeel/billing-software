"""
Logging and Exception Handling Module
Provides centralized logging with rotation and error tracking.
"""
import logging
import sys
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
from functools import wraps
from typing import Optional, Callable, Any


class BillingLogger:
    """Centralized logger with file rotation and error handling."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        
        # Create logs directory in AppData for persistence
        app_data_dir = os.path.join(os.getenv('LOCALAPPDATA', os.path.expanduser('~')), 'TravelBilling')
        self.log_dir = Path(app_data_dir) / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup loggers
        self._setup_main_logger()
        self._setup_error_logger()
        self._setup_database_logger()
        
    def _setup_main_logger(self):
        """Setup main application logger."""
        self.main_logger = logging.getLogger('billing_app')
        self.main_logger.setLevel(logging.DEBUG)
        self.main_logger.handlers.clear()
        
        # File handler with rotation (10MB max, keep 5 files)
        main_file = self.log_dir / "app.log"
        file_handler = RotatingFileHandler(
            main_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler (INFO and above)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        self.main_logger.addHandler(file_handler)
        self.main_logger.addHandler(console_handler)
    
    def _setup_error_logger(self):
        """Setup dedicated error logger."""
        self.error_logger = logging.getLogger('billing_errors')
        self.error_logger.setLevel(logging.ERROR)
        self.error_logger.handlers.clear()
        
        # Error file with rotation (5MB max, keep 10 files)
        error_file = self.log_dir / "errors.log"
        error_handler = RotatingFileHandler(
            error_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=10,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s\n'
            'Function: %(funcName)s (Line %(lineno)d)\n'
            'Message: %(message)s\n'
            '%(separator)s\n',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error_handler.setFormatter(error_formatter)
        
        self.error_logger.addHandler(error_handler)
    
    def _setup_database_logger(self):
        """Setup database operations logger."""
        self.db_logger = logging.getLogger('billing_database')
        self.db_logger.setLevel(logging.DEBUG)
        self.db_logger.handlers.clear()
        
        # Database log with rotation (20MB max, keep 3 files)
        db_file = self.log_dir / "database.log"
        db_handler = RotatingFileHandler(
            db_file,
            maxBytes=20*1024*1024,  # 20MB
            backupCount=3,
            encoding='utf-8'
        )
        db_handler.setLevel(logging.DEBUG)
        db_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(funcName)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        db_handler.setFormatter(db_formatter)
        
        self.db_logger.addHandler(db_handler)
    
    def log_info(self, message: str, logger_name: str = 'billing_app'):
        """Log info message."""
        logger = logging.getLogger(logger_name)
        logger.info(message)
    
    def log_warning(self, message: str, logger_name: str = 'billing_app'):
        """Log warning message."""
        logger = logging.getLogger(logger_name)
        logger.warning(message)
    
    def log_error(self, message: str, exception: Optional[Exception] = None, logger_name: str = 'billing_errors'):
        """Log error message with optional exception details."""
        logger = logging.getLogger(logger_name)
        
        if exception:
            import traceback
            error_details = f"{message}\n{'='*80}\n"
            error_details += f"Exception Type: {type(exception).__name__}\n"
            error_details += f"Exception Message: {str(exception)}\n"
            error_details += f"Traceback:\n{traceback.format_exc()}"
            logger.error(error_details, extra={'separator': '='*80})
        else:
            logger.error(message, extra={'separator': '='*80})
    
    def log_debug(self, message: str, logger_name: str = 'billing_app'):
        """Log debug message."""
        logger = logging.getLogger(logger_name)
        logger.debug(message)
    
    def log_db_operation(self, operation: str, details: str = "", success: bool = True):
        """Log database operation."""
        status = "SUCCESS" if success else "FAILED"
        message = f"{operation} | {status}"
        if details:
            message += f" | {details}"
        
        if success:
            self.db_logger.info(message)
        else:
            self.db_logger.error(message)


# Singleton instance
_logger_instance = None

def get_logger() -> BillingLogger:
    """Get the singleton logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = BillingLogger()
    return _logger_instance


# Decorator for exception handling
def handle_exceptions(logger_name: str = 'billing_app', reraise: bool = False, default_return: Any = None):
    """
    Decorator to catch and log exceptions.
    
    Args:
        logger_name: Name of logger to use
        reraise: Whether to re-raise the exception after logging
        default_return: Value to return if exception occurs (only if reraise=False)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger = get_logger()
                logger.log_error(
                    f"Exception in {func.__name__}",
                    exception=e,
                    logger_name=logger_name
                )
                
                if reraise:
                    raise
                else:
                    return default_return
        return wrapper
    return decorator


# Decorator for database operations
def log_db_operation(operation_name: str):
    """
    Decorator to log database operations.
    
    Args:
        operation_name: Name of the operation (e.g., 'INSERT_INVOICE', 'UPDATE_CONTACT')
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger()
            
            try:
                result = func(*args, **kwargs)
                
                # Log success
                logger.log_db_operation(
                    operation_name,
                    f"Args: {args[1:] if len(args) > 1 else 'none'}",
                    success=True
                )
                
                return result
                
            except Exception as e:
                # Log failure
                logger.log_db_operation(
                    operation_name,
                    f"Error: {str(e)}",
                    success=False
                )
                raise
                
        return wrapper
    return decorator


# Context manager for logging operations
class LogOperation:
    """Context manager for logging operations with automatic error handling."""
    
    def __init__(self, operation_name: str, logger_name: str = 'billing_app'):
        self.operation_name = operation_name
        self.logger_name = logger_name
        self.logger = get_logger()
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.log_debug(f"Starting: {self.operation_name}", self.logger_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            # Success
            self.logger.log_debug(
                f"Completed: {self.operation_name} (Duration: {duration:.2f}s)",
                self.logger_name
            )
        else:
            # Failure
            self.logger.log_error(
                f"Failed: {self.operation_name} (Duration: {duration:.2f}s)",
                exception=exc_val,
                logger_name='billing_errors'
            )
        
        # Don't suppress the exception
        return False


# Convenience functions
def log_info(message: str, logger_name: str = 'billing_app'):
    """Quick info log."""
    get_logger().log_info(message, logger_name)

def log_warning(message: str, logger_name: str = 'billing_app'):
    """Quick warning log."""
    get_logger().log_warning(message, logger_name)

def log_error(message: str, exception: Optional[Exception] = None, logger_name: str = 'billing_errors'):
    """Quick error log."""
    get_logger().log_error(message, exception, logger_name)

def log_debug(message: str, logger_name: str = 'billing_app'):
    """Quick debug log."""
    get_logger().log_debug(message, logger_name)


if __name__ == "__main__":
    # Test the logger
    logger = get_logger()
    
    logger.log_info("Application started")
    logger.log_debug("Debug information")
    logger.log_warning("This is a warning")
    
    try:
        # Simulate an error
        1 / 0
    except Exception as e:
        logger.log_error("Test error", exception=e)
    
    logger.log_db_operation("INSERT_INVOICE", "invoice_id=12345", success=True)
    logger.log_db_operation("DELETE_CONTACT", "contact_id=999", success=False)
    
    print(f"\n✓ Logs created in: {logger.log_dir}")
    print(f"  - app.log (main application log)")
    print(f"  - errors.log (error tracking)")
    print(f"  - database.log (database operations)")
