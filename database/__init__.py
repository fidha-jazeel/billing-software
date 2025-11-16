"""Database package for billing software.
Expose DatabaseManager and get_db_instance for convenience.
"""
from .db_manager import DatabaseManager, get_db_instance

__all__ = ["DatabaseManager", "get_db_instance"]
