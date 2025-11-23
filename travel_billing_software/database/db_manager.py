"""Enhanced SQLite database manager for Al Chishtiya Travels Billing Software.
Provides comprehensive database operations with proper error handling.
"""
import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime


class DatabaseManager:
    """Manages all database operations for the billing software."""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection and ensure tables exist.
        
        Args:
            db_path: Optional custom database path. Defaults to 'billing.db' in project root.
        """
        base = Path(__file__).resolve().parents[1]
        self.db_path = db_path or str(base / "billing.db")
        self.conn = None
        self._connect()
        self._ensure_tables()
    
    def _connect(self):
        """Establish database connection with proper settings."""
        try:
            # Use isolation_level=None for autocommit mode to prevent locks
            self.conn = sqlite3.connect(
                self.db_path, 
                check_same_thread=False,
                timeout=10.0,  # 10 second timeout
                isolation_level=None  # Autocommit mode
            )
            self.conn.row_factory = sqlite3.Row
            
            # Enable WAL mode for better concurrent access
            self.conn.execute("PRAGMA journal_mode=WAL")
            # Enable foreign keys
            self.conn.execute("PRAGMA foreign_keys = ON")
            # Set busy timeout
            self.conn.execute("PRAGMA busy_timeout = 5000")
            # Optimize for faster writes
            self.conn.execute("PRAGMA synchronous = NORMAL")
            self.conn.execute("PRAGMA cache_size = 10000")
            
            print(f"✓ Database connected successfully: {self.db_path}")
        except Exception as e:
            print(f"✗ Database connection error: {e}")
            raise
    
    def _ensure_tables(self):
        """Create all required tables if they don't exist."""
        try:
            cur = self.conn.cursor()
            cur.executescript("""
            -- Customers table
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Items/Services table
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL DEFAULT 0,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Invoices table
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                invoice_date TEXT NOT NULL,
                customer_id INTEGER,
                customer_name TEXT NOT NULL,
                contact_number TEXT,
                subtotal REAL DEFAULT 0,
                tax REAL DEFAULT 0,
                total REAL DEFAULT 0,
                received REAL DEFAULT 0,
                balance REAL DEFAULT 0,
                status TEXT DEFAULT 'Pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL
            );
            
            -- Invoice Items table (line items)
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                ticket TEXT,
                sector TEXT,
                supplier TEXT,
                price REAL DEFAULT 0,
                qty REAL DEFAULT 1,
                tax_pct REAL DEFAULT 0,
                amount REAL DEFAULT 0,
                FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
            );
            
            -- Settings table
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Dropdown items tables for dynamic lists
            CREATE TABLE IF NOT EXISTS dropdown_suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS dropdown_sectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS dropdown_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS dropdown_classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Create indexes for better performance
            CREATE INDEX IF NOT EXISTS idx_invoice_number ON invoices(invoice_number);
            CREATE INDEX IF NOT EXISTS idx_invoice_date ON invoices(invoice_date);
            CREATE INDEX IF NOT EXISTS idx_customer_name ON customers(name);
            CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice_id ON invoice_items(invoice_id);
            """)
            self.conn.commit()
            print("✓ Database tables created/verified successfully")
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            raise
    
    # ==================== INVOICE OPERATIONS ====================
    
    def save_invoice(self, invoice_data: Dict[str, Any]) -> bool:
        """Save invoice to database.
        
        Args:
            invoice_data: Dictionary containing invoice information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Since we're using autocommit mode, use BEGIN IMMEDIATE for exclusive lock
            self.conn.execute("BEGIN IMMEDIATE")
            
            cur = self.conn.cursor()
            
            # Insert invoice header
            cur.execute("""
                INSERT INTO invoices (
                    invoice_number, invoice_date, customer_name, contact_number,
                    subtotal, tax, total, received, balance, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                invoice_data.get('invoice_number'),
                invoice_data.get('invoice_date'),
                invoice_data.get('customer_name'),
                invoice_data.get('contact_number'),
                invoice_data.get('subtotal', 0),
                invoice_data.get('tax', 0),
                invoice_data.get('total', 0),
                invoice_data.get('received', 0),
                invoice_data.get('balance', 0),
                invoice_data.get('status', 'Pending')
            ))
            
            invoice_id = cur.lastrowid
            
            # Insert invoice items in batch for better performance
            items = invoice_data.get('items', [])
            if items:
                item_values = [
                    (
                        invoice_id,
                        item.get('item'),
                        item.get('ticket'),
                        item.get('sector'),
                        item.get('supplier'),
                        item.get('price', 0),
                        item.get('qty', 1),
                        item.get('tax', 0),
                        item.get('amount', 0)
                    )
                    for item in items
                ]
                cur.executemany("""
                    INSERT INTO invoice_items (
                        invoice_id, item_name, ticket, sector, supplier,
                        price, qty, tax_pct, amount
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, item_values)
            
            self.conn.execute("COMMIT")
            print(f"✓ Invoice {invoice_data.get('invoice_number')} saved to database")
            return True
            
        except sqlite3.IntegrityError as e:
            self.conn.execute("ROLLBACK")
            print(f"✗ Invoice already exists: {e}")
            return False
        except Exception as e:
            self.conn.execute("ROLLBACK")
            print(f"✗ Error saving invoice: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_invoice(self, invoice_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve invoice by invoice number.
        
        Args:
            invoice_number: The invoice number to search for
            
        Returns:
            Dictionary with invoice data or None if not found
        """
        try:
            cur = self.conn.cursor()
            
            # Get invoice header
            cur.execute("""
                SELECT * FROM invoices WHERE invoice_number = ?
            """, (invoice_number,))
            
            invoice_row = cur.fetchone()
            if not invoice_row:
                return None
            
            # Convert to dictionary
            invoice = dict(invoice_row)
            
            # Get invoice items
            cur.execute("""
                SELECT * FROM invoice_items WHERE invoice_id = ?
            """, (invoice['id'],))
            
            items = [dict(row) for row in cur.fetchall()]
            invoice['items'] = items
            
            return invoice
            
        except Exception as e:
            print(f"✗ Error retrieving invoice: {e}")
            return None
    
    def get_all_invoices(self) -> List[Dict[str, Any]]:
        """Retrieve all invoices from database.
        
        Returns:
            List of invoice dictionaries
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT * FROM invoices ORDER BY created_at DESC
            """)
            
            invoices = [dict(row) for row in cur.fetchall()]
            return invoices
            
        except Exception as e:
            print(f"✗ Error retrieving invoices: {e}")
            return []
    
    def update_invoice_status(self, invoice_number: str, status: str) -> bool:
        """Update invoice status.
        
        Args:
            invoice_number: Invoice to update
            status: New status (e.g., 'Paid', 'Pending', 'Cancelled')
            
        Returns:
            bool: True if successful
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                UPDATE invoices 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE invoice_number = ?
            """, (status, invoice_number))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"✗ Error updating invoice status: {e}")
            return False
    
    def delete_invoice(self, invoice_number: str) -> bool:
        """Delete an invoice and its items.
        
        Args:
            invoice_number: Invoice to delete
            
        Returns:
            bool: True if successful
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                DELETE FROM invoices WHERE invoice_number = ?
            """, (invoice_number,))
            
            self.conn.commit()
            print(f"✓ Invoice {invoice_number} deleted")
            return True
            
        except Exception as e:
            print(f"✗ Error deleting invoice: {e}")
            return False
    
    # ==================== CUSTOMER OPERATIONS ====================
    
    def add_customer(self, name: str, contact: str = "", email: str = "", address: str = "") -> int:
        """Add a new customer.
        
        Args:
            name: Customer name
            contact: Contact number
            email: Email address
            address: Physical address
            
        Returns:
            int: Customer ID or -1 on error
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO customers (name, contact, email, address)
                VALUES (?, ?, ?, ?)
            """, (name, contact, email, address))
            
            self.conn.commit()
            return cur.lastrowid
            
        except Exception as e:
            print(f"✗ Error adding customer: {e}")
            return -1
    
    def get_customers(self) -> List[Dict[str, Any]]:
        """Get all customers.
        
        Returns:
            List of customer dictionaries
        """
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM customers ORDER BY name")
            return [dict(row) for row in cur.fetchall()]
            
        except Exception as e:
            print(f"✗ Error retrieving customers: {e}")
            return []
    
    # ==================== SETTINGS OPERATIONS ====================
    
    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value.
        
        Args:
            key: Setting key
            
        Returns:
            Setting value or None
        """
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cur.fetchone()
            return row['value'] if row else None
            
        except Exception as e:
            print(f"✗ Error retrieving setting: {e}")
            return None
    
    def set_setting(self, key: str, value: str) -> bool:
        """Set a setting value.
        
        Args:
            key: Setting key
            value: Setting value
            
        Returns:
            bool: True if successful
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, value))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"✗ Error setting value: {e}")
            return False
    
    # ==================== UTILITY OPERATIONS ====================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics.
        
        Returns:
            Dictionary with various statistics
        """
        try:
            cur = self.conn.cursor()
            
            # Total invoices
            cur.execute("SELECT COUNT(*) as count FROM invoices")
            total_invoices = cur.fetchone()['count']
            
            # Total revenue
            cur.execute("SELECT SUM(total) as sum FROM invoices")
            total_revenue = cur.fetchone()['sum'] or 0
            
            # Pending balance
            cur.execute("SELECT SUM(balance) as sum FROM invoices WHERE balance > 0")
            pending_balance = cur.fetchone()['sum'] or 0
            
            # Total customers
            cur.execute("SELECT COUNT(*) as count FROM customers")
            total_customers = cur.fetchone()['count']
            
            return {
                'total_invoices': total_invoices,
                'total_revenue': total_revenue,
                'pending_balance': pending_balance,
                'total_customers': total_customers
            }
            
        except Exception as e:
            print(f"✗ Error getting statistics: {e}")
            return {}
    
    def get_revenue_by_period(self, period: str = 'month') -> List[Dict[str, Any]]:
        """Get revenue grouped by time period.
        
        Args:
            period: 'day', 'week', 'month', or 'year'
            
        Returns:
            List of dictionaries with period and revenue
        """
        try:
            cur = self.conn.cursor()
            
            if period == 'day':
                group_format = '%Y-%m-%d'
            elif period == 'week':
                group_format = '%Y-W%W'
            elif period == 'year':
                group_format = '%Y'
            else:  # month
                group_format = '%Y-%m'
            
            cur.execute(f"""
                SELECT 
                    strftime('{group_format}', invoice_date) as period,
                    SUM(total) as revenue,
                    COUNT(*) as invoice_count
                FROM invoices
                GROUP BY period
                ORDER BY period DESC
                LIMIT 12
            """)
            
            results = []
            for row in cur.fetchall():
                results.append({
                    'period': row['period'],
                    'revenue': row['revenue'] or 0,
                    'invoice_count': row['invoice_count']
                })
            
            return results[::-1]  # Reverse to show oldest first
            
        except Exception as e:
            print(f"✗ Error getting revenue by period: {e}")
            return []
    
    def get_top_customers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top customers by total spending.
        
        Args:
            limit: Maximum number of customers to return
            
        Returns:
            List of dictionaries with customer info and total spending
        """
        try:
            cur = self.conn.cursor()
            
            cur.execute("""
                SELECT 
                    customer_name,
                    COUNT(*) as invoice_count,
                    SUM(total) as total_spent,
                    AVG(total) as avg_invoice,
                    MAX(invoice_date) as last_invoice_date
                FROM invoices
                WHERE customer_name IS NOT NULL AND customer_name != ''
                GROUP BY customer_name
                ORDER BY total_spent DESC
                LIMIT ?
            """, (limit,))
            
            results = []
            for row in cur.fetchall():
                results.append({
                    'customer_name': row['customer_name'],
                    'invoice_count': row['invoice_count'],
                    'total_spent': row['total_spent'] or 0,
                    'avg_invoice': row['avg_invoice'] or 0,
                    'last_invoice_date': row['last_invoice_date']
                })
            
            return results
            
        except Exception as e:
            print(f"✗ Error getting top customers: {e}")
            return []
    
    def get_payment_status_summary(self) -> Dict[str, Any]:
        """Get summary of payment statuses.
        
        Returns:
            Dictionary with paid, pending, and overpaid counts and amounts
        """
        try:
            cur = self.conn.cursor()
            
            # Paid (balance = 0)
            cur.execute("""
                SELECT COUNT(*) as count, COALESCE(SUM(total), 0) as amount
                FROM invoices WHERE balance = 0
            """)
            paid = cur.fetchone()
            
            # Pending (balance > 0)
            cur.execute("""
                SELECT COUNT(*) as count, COALESCE(SUM(balance), 0) as amount
                FROM invoices WHERE balance > 0
            """)
            pending = cur.fetchone()
            
            # Overpaid (balance < 0)
            cur.execute("""
                SELECT COUNT(*) as count, COALESCE(SUM(ABS(balance)), 0) as amount
                FROM invoices WHERE balance < 0
            """)
            overpaid = cur.fetchone()
            
            return {
                'paid': {'count': paid['count'], 'amount': paid['amount']},
                'pending': {'count': pending['count'], 'amount': pending['amount']},
                'overpaid': {'count': overpaid['count'], 'amount': overpaid['amount']}
            }
            
        except Exception as e:
            print(f"✗ Error getting payment status summary: {e}")
            return {}
    
    def get_recent_activity(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent invoice activity.
        
        Args:
            limit: Maximum number of invoices to return
            
        Returns:
            List of recent invoice dictionaries
        """
        try:
            cur = self.conn.cursor()
            
            cur.execute("""
                SELECT 
                    invoice_number,
                    invoice_date,
                    customer_name,
                    total,
                    balance,
                    created_at
                FROM invoices
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            results = []
            for row in cur.fetchall():
                results.append({
                    'invoice_number': row['invoice_number'],
                    'invoice_date': row['invoice_date'],
                    'customer_name': row['customer_name'],
                    'total': row['total'],
                    'balance': row['balance'],
                    'created_at': row['created_at']
                })
            
            return results
            
        except Exception as e:
            print(f"✗ Error getting recent activity: {e}")
            return []
    
    def backup_database(self, backup_path: Optional[str] = None) -> bool:
        """Create a backup of the database.
        
        Args:
            backup_path: Optional custom backup path
            
        Returns:
            bool: True if successful
        """
        try:
            if not backup_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = str(Path(self.db_path).parent / f"billing_backup_{timestamp}.db")
            
            backup_conn = sqlite3.connect(backup_path)
            with backup_conn:
                self.conn.backup(backup_conn)
            backup_conn.close()
            
            print(f"✓ Database backed up to: {backup_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error backing up database: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        try:
            if self.conn:
                self.conn.close()
                print("✓ Database connection closed")
        except Exception as e:
            print(f"✗ Error closing database: {e}")
    
    # ==================== DROPDOWN ITEMS OPERATIONS ====================
    
    def get_dropdown_items(self, item_type: str) -> List[str]:
        """Get all dropdown items of a specific type from database.
        
        Args:
            item_type: Type of dropdown ('supplier', 'sector', 'type', 'class')
            
        Returns:
            List of item names
        """
        try:
            table_map = {
                'supplier': 'dropdown_suppliers',
                'sector': 'dropdown_sectors',
                'type': 'dropdown_types',
                'class': 'dropdown_classes'
            }
            
            table = table_map.get(item_type)
            if not table:
                return []
            
            cur = self.conn.cursor()
            cur.execute(f"SELECT name FROM {table} ORDER BY name")
            return [row[0] for row in cur.fetchall()]
            
        except Exception as e:
            print(f"✗ Error getting dropdown items: {e}")
            return []
    
    def add_dropdown_item(self, item_type: str, name: str) -> bool:
        """Add a new dropdown item to database.
        
        Args:
            item_type: Type of dropdown ('supplier', 'sector', 'type', 'class')
            name: Name of the item to add
            
        Returns:
            bool: True if successful
        """
        try:
            table_map = {
                'supplier': 'dropdown_suppliers',
                'sector': 'dropdown_sectors',
                'type': 'dropdown_types',
                'class': 'dropdown_classes'
            }
            
            table = table_map.get(item_type)
            if not table:
                return False
            
            self.conn.execute("BEGIN IMMEDIATE")
            cur = self.conn.cursor()
            cur.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
            self.conn.execute("COMMIT")
            
            print(f"✓ Added {item_type}: {name}")
            return True
            
        except sqlite3.IntegrityError:
            self.conn.execute("ROLLBACK")
            print(f"✗ {item_type.capitalize()} '{name}' already exists")
            return False
        except Exception as e:
            self.conn.execute("ROLLBACK")
            print(f"✗ Error adding dropdown item: {e}")
            return False
    
    def update_dropdown_item(self, item_type: str, old_name: str, new_name: str) -> bool:
        """Update a dropdown item in database.
        
        Args:
            item_type: Type of dropdown ('supplier', 'sector', 'type', 'class')
            old_name: Current name of the item
            new_name: New name for the item
            
        Returns:
            bool: True if successful
        """
        try:
            table_map = {
                'supplier': 'dropdown_suppliers',
                'sector': 'dropdown_sectors',
                'type': 'dropdown_types',
                'class': 'dropdown_classes'
            }
            
            table = table_map.get(item_type)
            if not table:
                return False
            
            self.conn.execute("BEGIN IMMEDIATE")
            cur = self.conn.cursor()
            cur.execute(f"UPDATE {table} SET name = ? WHERE name = ?", (new_name, old_name))
            self.conn.execute("COMMIT")
            
            print(f"✓ Updated {item_type}: {old_name} → {new_name}")
            return True
            
        except Exception as e:
            self.conn.execute("ROLLBACK")
            print(f"✗ Error updating dropdown item: {e}")
            return False
    
    def delete_dropdown_item(self, item_type: str, name: str) -> bool:
        """Delete a dropdown item from database.
        
        Args:
            item_type: Type of dropdown ('supplier', 'sector', 'type', 'class')
            name: Name of the item to delete
            
        Returns:
            bool: True if successful
        """
        try:
            table_map = {
                'supplier': 'dropdown_suppliers',
                'sector': 'dropdown_sectors',
                'type': 'dropdown_types',
                'class': 'dropdown_classes'
            }
            
            table = table_map.get(item_type)
            if not table:
                return False
            
            self.conn.execute("BEGIN IMMEDIATE")
            cur = self.conn.cursor()
            cur.execute(f"DELETE FROM {table} WHERE name = ?", (name,))
            self.conn.execute("COMMIT")
            
            print(f"✓ Deleted {item_type}: {name}")
            return True
            
        except Exception as e:
            self.conn.execute("ROLLBACK")
            print(f"✗ Error deleting dropdown item: {e}")
            return False
    
    def initialize_default_dropdowns(self):
        """Initialize dropdown tables with default values if empty."""
        try:
            defaults = {
                'supplier': ['Emirates Airlines', 'Qatar Airways', 'Air India', 'Etihad Airways', 'British Airways'],
                'sector': ['Domestic', 'International', 'Regional', 'GCC'],
                'type': ['Flight', 'Hotel', 'Tour Package', 'Visa', 'Insurance'],
                'class': ['Economy', 'Premium Economy', 'Business', 'First Class']
            }
            
            for item_type, items in defaults.items():
                existing = self.get_dropdown_items(item_type)
                if not existing:
                    for item in items:
                        self.add_dropdown_item(item_type, item)
            
            print("✓ Default dropdown items initialized")
            return True
            
        except Exception as e:
            print(f"✗ Error initializing dropdowns: {e}")
            return False
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Singleton instance for easy access
_db_instance = None

def get_db_instance(db_path: Optional[str] = None) -> DatabaseManager:
    """Get or create the database manager singleton instance.
    
    Args:
        db_path: Optional custom database path
        
    Returns:
        DatabaseManager instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager(db_path)
    return _db_instance

def get_db_path() -> str:
    """Return the path to the main billing database file."""
    return get_db_instance().db_path
