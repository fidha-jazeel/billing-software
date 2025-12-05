"""Production-grade SQLite database manager for Al Chishtiya Travels Billing Software.
Implements the complete schema with proper relationships, foreign keys, and audit trails.
"""
import sqlite3
import hashlib
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
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
        self.current_user_id = None  # Track logged-in user
        self._connect()
        self._ensure_tables()
        self._ensure_default_admin()
        self._ensure_default_service_types()
    
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
        """Create all required tables following the production schema."""
        try:
            cur = self.conn.cursor()
            cur.executescript("""
            -- ===================================================================================
            -- 1. USERS TABLE (Authentication)
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT CHECK(role IN ('ADMIN', 'STAFF')) DEFAULT 'STAFF',
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            -- ===================================================================================
            -- 2. CONTACTS TABLE (Unified Customers & Suppliers)
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT CHECK(type IN ('CUSTOMER', 'SUPPLIER')) NOT NULL,
                name TEXT NOT NULL,
                company_name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                gstin TEXT,
                opening_balance DECIMAL(10,2) DEFAULT 0.00,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_contacts_phone ON contacts(phone);
            CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);
            CREATE INDEX IF NOT EXISTS idx_contacts_type ON contacts(type);
            
            -- ===================================================================================
            -- 3. PASSENGERS TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS passengers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                contact_number TEXT,
                whatsapp_number TEXT,
                dob DATE,
                age INTEGER,
                nationality TEXT,
                gender TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
            );
            
            CREATE INDEX IF NOT EXISTS idx_passengers_contact_id ON passengers(contact_id);
            CREATE INDEX IF NOT EXISTS idx_passengers_name ON passengers(name);
            CREATE INDEX IF NOT EXISTS idx_passengers_contact_number ON passengers(contact_number);
            
            -- ===================================================================================
            -- 4. PASSPORT DETAILS TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS passport_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                passenger_id INTEGER NOT NULL,
                passport_number TEXT NOT NULL,
                full_name TEXT,
                dob DATE,
                nationality TEXT,
                gender TEXT,
                place_of_birth TEXT,
                issue_date DATE,
                expiry_date DATE NOT NULL,
                file_path TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (passenger_id) REFERENCES passengers(id) ON DELETE CASCADE
            );
            
            CREATE INDEX IF NOT EXISTS idx_passport_number ON passport_details(passport_number);
            
            -- ===================================================================================
            -- 5. SERVICE TYPES TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS service_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                default_hsn_sac TEXT
            );
            
            -- ===================================================================================
            -- 6. INVOICES TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                contact_id INTEGER NOT NULL,
                date DATE NOT NULL,
                due_date DATE,
                sub_total DECIMAL(10,2) DEFAULT 0.00,
                discount_amount DECIMAL(10,2) DEFAULT 0.00,
                tax_amount DECIMAL(10,2) DEFAULT 0.00,
                round_off DECIMAL(10,2) DEFAULT 0.00,
                total_amount DECIMAL(10,2) DEFAULT 0.00,
                status TEXT CHECK(status IN ('DRAFT', 'FINAL', 'CANCELLED')) DEFAULT 'DRAFT',
                payment_status TEXT CHECK(payment_status IN ('PAID', 'PARTIAL', 'UNPAID')) DEFAULT 'UNPAID',
                notes TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contact_id) REFERENCES contacts(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_invoice_number ON invoices(invoice_number);
            CREATE INDEX IF NOT EXISTS idx_invoice_date ON invoices(date);
            CREATE INDEX IF NOT EXISTS idx_invoice_contact_id ON invoices(contact_id);
            
            -- ===================================================================================
            -- 7. INVOICE ITEMS TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                service_type_id INTEGER NOT NULL,
                passenger_id INTEGER,
                description TEXT,
                pnr_number TEXT,
                ticket_number TEXT,
                sector TEXT,
                travel_date DATE,
                airline_name TEXT,
                visa_application_date DATE,
                visa_status TEXT CHECK(visa_status IN ('PENDING', 'SUBMITTED', 'ISSUED', 'REJECTED', 'NA')) DEFAULT 'NA',
                quantity INTEGER DEFAULT 1,
                unit_price DECIMAL(10,2) NOT NULL,
                tax_rate DECIMAL(5,2) DEFAULT 0.00,
                tax_amount DECIMAL(10,2) DEFAULT 0.00,
                total_amount DECIMAL(10,2) NOT NULL,
                cost_price DECIMAL(10,2) DEFAULT 0.00,
                supplier_id INTEGER,
                FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
                FOREIGN KEY (service_type_id) REFERENCES service_types(id),
                FOREIGN KEY (passenger_id) REFERENCES passengers(id),
                FOREIGN KEY (supplier_id) REFERENCES contacts(id)
            );
            
            CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice_id ON invoice_items(invoice_id);
            CREATE INDEX IF NOT EXISTS idx_invoice_items_passenger_id ON invoice_items(passenger_id);
            
            -- ===================================================================================
            -- 8. PAYMENTS RECEIVED TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS payments_received (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_number TEXT UNIQUE,
                date DATE NOT NULL,
                contact_id INTEGER NOT NULL,
                invoice_id INTEGER,
                amount DECIMAL(10,2) NOT NULL,
                payment_mode TEXT CHECK(payment_mode IN ('CASH', 'BANK', 'UPI', 'CHEQUE', 'CARD')),
                reference_number TEXT,
                notes TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (contact_id) REFERENCES contacts(id),
                FOREIGN KEY (invoice_id) REFERENCES invoices(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            );
            
            -- ===================================================================================
            -- 9. SUPPLIER PAYMENTS TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS supplier_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_number TEXT UNIQUE,
                date DATE NOT NULL,
                supplier_id INTEGER NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                payment_mode TEXT,
                reference_number TEXT,
                notes TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (supplier_id) REFERENCES contacts(id),
                FOREIGN KEY (created_by) REFERENCES users(id)
            );
            
            -- ===================================================================================
            -- 10. EXPENSES TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount DECIMAL(10,2) NOT NULL,
                payment_mode TEXT DEFAULT 'CASH',
                paid_to TEXT,
                person_responsible TEXT,
                reference_number TEXT,
                created_by INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            );
            
            -- ===================================================================================
            -- 11. PURCHASE BILLS TABLE
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS purchase_bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_number TEXT,
                supplier_id INTEGER NOT NULL,
                date DATE NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                due_date DATE,
                notes TEXT,
                attachment_path TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (supplier_id) REFERENCES contacts(id)
            );
            
            -- ===================================================================================
            -- 12. LEGACY TABLES (For Backward Compatibility)
            -- ===================================================================================
            CREATE TABLE IF NOT EXISTS dropdown_sectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS dropdown_classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- ===================================================================================
            -- 13. TRIGGERS
            -- ===================================================================================
            CREATE TRIGGER IF NOT EXISTS update_contacts_timestamp 
            AFTER UPDATE ON contacts
            BEGIN
                UPDATE contacts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END;
            
            CREATE TRIGGER IF NOT EXISTS update_invoices_timestamp 
            AFTER UPDATE ON invoices
            BEGIN
                UPDATE invoices SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END;
            """)
            self.conn.commit()
            print("✓ Database tables created/verified successfully")
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            raise
    
    def _ensure_default_admin(self):
        """Create default admin user if no users exist."""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) as count FROM users")
            count = cur.fetchone()['count']
            
            if count == 0:
                # Create default admin (username: admin, password: admin)
                password_hash = hashlib.sha256("admin".encode()).hexdigest()
                cur.execute("""
                    INSERT INTO users (username, password_hash, role, is_active)
                    VALUES (?, ?, 'ADMIN', 1)
                """, ("admin", password_hash))
                self.conn.commit()
                print("✓ Default admin user created (username: admin, password: admin)")
        except Exception as e:
            print(f"✗ Error creating default admin: {e}")
    
    def _ensure_default_service_types(self):
        """Create default service types if none exist."""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) as count FROM service_types")
            count = cur.fetchone()['count']
            
            if count == 0:
                default_services = [
                    ('Flight', 'Air ticket booking', '996411'),
                    ('Visa', 'Visa processing service', '998599'),
                    ('Hotel', 'Hotel booking', '996312'),
                    ('Tour Package', 'Complete tour package', '998599'),
                    ('Insurance', 'Travel insurance', '997132'),
                    ('Transport', 'Ground transportation', '996421')
                ]
                cur.executemany("""
                    INSERT INTO service_types (name, description, default_hsn_sac)
                    VALUES (?, ?, ?)
                """, default_services)
                self.conn.commit()
                
                # Also ensure default dropdowns
                self._ensure_default_dropdowns()
                print("✓ Default service types and dropdowns created")
        except Exception as e:
            print(f"✗ Error creating default service types: {e}")
    
    def _ensure_default_dropdowns(self):
        """Initialize dropdown tables with default values if empty."""
        try:
            cur = self.conn.cursor()
            
            # Check and populate sectors
            cur.execute("SELECT COUNT(*) as count FROM dropdown_sectors")
            if cur.fetchone()['count'] == 0:
                sectors = [('Domestic',), ('International',), ('Regional',), ('GCC',)]
                cur.executemany("INSERT INTO dropdown_sectors (name) VALUES (?)", sectors)
            
            # Check and populate classes
            cur.execute("SELECT COUNT(*) as count FROM dropdown_classes")
            if cur.fetchone()['count'] == 0:
                classes = [('Economy',), ('Premium Economy',), ('Business',), ('First Class',)]
                cur.executemany("INSERT INTO dropdown_classes (name) VALUES (?)", classes)
            
            self.conn.commit()
        except Exception as e:
            print(f"✗ Error initializing dropdowns: {e}")
    
    # ===================================================================================
    # AUTHENTICATION METHODS
    # ===================================================================================
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user details if valid.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User dict if valid, None otherwise
        """
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cur = self.conn.cursor()
            cur.execute("""
                SELECT * FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            """, (username, password_hash))
            
            user = cur.fetchone()
            if user:
                self.current_user_id = user['id']
                return dict(user)
            return None
        except Exception as e:
            print(f"✗ Authentication error: {e}")
            return None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get currently logged in user details."""
        if not self.current_user_id:
            return None
        
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (self.current_user_id,))
            user = cur.fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"✗ Error getting current user: {e}")
            return None
    
    # ===================================================================================
    # CONTACTS METHODS (Unified Customers & Suppliers)
    # ===================================================================================
    
    def add_contact(self, contact_type: str, name: str, **kwargs) -> int:
        """Add a new contact (customer or supplier).
        
        Args:
            contact_type: 'CUSTOMER' or 'SUPPLIER'
            name: Contact name
            **kwargs: Additional fields (phone, email, address, company_name, gstin, opening_balance)
            
        Returns:
            Contact ID or -1 on error
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO contacts (
                    type, name, company_name, phone, email, address, gstin, opening_balance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contact_type, name,
                kwargs.get('company_name', ''),
                kwargs.get('phone', ''),
                kwargs.get('email', ''),
                kwargs.get('address', ''),
                kwargs.get('gstin', ''),
                kwargs.get('opening_balance', 0.00)
            ))
            self.conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(f"✗ Error adding contact: {e}")
            return -1
    
    def get_contacts(self, contact_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all contacts, optionally filtered by type.
        
        Args:
            contact_type: Optional filter ('CUSTOMER' or 'SUPPLIER')
            
        Returns:
            List of contact dictionaries
        """
        try:
            cur = self.conn.cursor()
            if contact_type:
                cur.execute("SELECT * FROM contacts WHERE type = ? ORDER BY name", (contact_type,))
            else:
                cur.execute("SELECT * FROM contacts ORDER BY name")
            return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            print(f"✗ Error retrieving contacts: {e}")
            return []
    
    def search_contacts(self, search_text: str, contact_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search contacts by name or phone.
        
        Args:
            search_text: Text to search for
            contact_type: Optional filter ('CUSTOMER' or 'SUPPLIER')
            
        Returns:
            List of matching contacts
        """
        try:
            cur = self.conn.cursor()
            search_pattern = f"%{search_text}%"
            
            if contact_type:
                cur.execute("""
                    SELECT * FROM contacts 
                    WHERE type = ? AND (name LIKE ? OR phone LIKE ?)
                    ORDER BY name
                """, (contact_type, search_pattern, search_pattern))
            else:
                cur.execute("""
                    SELECT * FROM contacts 
                    WHERE name LIKE ? OR phone LIKE ?
                    ORDER BY name
                """, (search_pattern, search_pattern))
            
            return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            print(f"✗ Error searching contacts: {e}")
            return []
    
    def get_or_create_contact(self, name: str, phone: str, contact_type: str = 'CUSTOMER') -> int:
        """Get existing contact by phone or create new one.
        
        Args:
            name: Contact name
            phone: Phone number
            contact_type: 'CUSTOMER' or 'SUPPLIER'
            
        Returns:
            Contact ID
        """
        try:
            cur = self.conn.cursor()
            
            # Try to find by phone first
            cur.execute("SELECT id FROM contacts WHERE phone = ? AND type = ?", (phone, contact_type))
            existing = cur.fetchone()
            
            if existing:
                return existing['id']
            
            # Create new contact
            return self.add_contact(contact_type, name, phone=phone)
        except Exception as e:
            print(f"✗ Error in get_or_create_contact: {e}")
            return -1
    
    # ===================================================================================
    # PASSENGERS METHODS
    # ===================================================================================
    
    def add_passenger(self, contact_id: int, name: str, contact_number: str, **kwargs) -> int:
        """Add a new passenger.
        
        Args:
            contact_id: Primary contact ID
            name: Passenger name
            contact_number: Contact number grouping key
            **kwargs: Additional fields (whatsapp_number, dob, age, nationality, gender)
            
        Returns:
            Passenger ID or -1 on error
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO passengers (
                    contact_id, name, contact_number, whatsapp_number, dob, age, nationality, gender
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contact_id, name, contact_number,
                kwargs.get('whatsapp_number', ''),
                kwargs.get('dob'),
                kwargs.get('age'),
                kwargs.get('nationality', ''),
                kwargs.get('gender', '')
            ))
            self.conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(f"✗ Error adding passenger: {e}")
            return -1
    
    def get_passenger_by_name_and_contact(self, name: str, contact_number: str) -> Optional[Dict[str, Any]]:
        """Get passenger by name and contact number combination.
        
        Args:
            name: Passenger name
            contact_number: Contact number
            
        Returns:
            Passenger dict or None
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT * FROM passengers 
                WHERE name = ? AND contact_number = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (name, contact_number))
            
            row = cur.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"✗ Error getting passenger: {e}")
            return None
    
    def get_passengers_by_contact_number(self, contact_number: str) -> List[Dict[str, Any]]:
        """Get all passengers grouped by contact number.
        
        Args:
            contact_number: Contact number grouping key
            
        Returns:
            List of passengers
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT * FROM passengers 
                WHERE contact_number = ?
                ORDER BY name
            """, (contact_number,))
            
            return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            print(f"✗ Error getting passengers by contact: {e}")
            return []
    
    def get_or_create_passenger(self, contact_id: int, name: str, contact_number: str, **kwargs) -> int:
        """Get existing passenger or create new one.
        
        Args:
            contact_id: Primary contact ID
            name: Passenger name
            contact_number: Contact number grouping key
            **kwargs: Additional passenger fields
            
        Returns:
            Passenger ID
        """
        existing = self.get_passenger_by_name_and_contact(name, contact_number)
        if existing:
            return existing['id']
        
        return self.add_passenger(contact_id, name, contact_number, **kwargs)
    
    # ===================================================================================
    # PASSPORT DETAILS METHODS
    # ===================================================================================
    
    def add_passport_details(self, passenger_id: int, passport_number: str, expiry_date: str, **kwargs) -> int:
        """Add passport details for a passenger.
        
        Args:
            passenger_id: Passenger ID
            passport_number: Passport number
            expiry_date: Expiry date (YYYY-MM-DD)
            **kwargs: Additional fields
            
        Returns:
            Passport details ID or -1 on error
        """
        try:
            # Deactivate any existing passports for this passenger
            cur = self.conn.cursor()
            cur.execute("UPDATE passport_details SET is_active = 0 WHERE passenger_id = ?", (passenger_id,))
            
            # Insert new passport
            cur.execute("""
                INSERT INTO passport_details (
                    passenger_id, passport_number, full_name, dob, nationality, gender,
                    place_of_birth, issue_date, expiry_date, file_path, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                passenger_id, passport_number,
                kwargs.get('full_name', ''),
                kwargs.get('dob'),
                kwargs.get('nationality', ''),
                kwargs.get('gender', ''),
                kwargs.get('place_of_birth', ''),
                kwargs.get('issue_date'),
                expiry_date,
                kwargs.get('file_path', '')
            ))
            self.conn.commit()
            return cur.lastrowid
        except Exception as e:
            print(f"✗ Error adding passport details: {e}")
            return -1
    
    def get_active_passport(self, passenger_id: int) -> Optional[Dict[str, Any]]:
        """Get active passport for a passenger.
        
        Args:
            passenger_id: Passenger ID
            
        Returns:
            Passport details dict or None
        """
        try:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT * FROM passport_details 
                WHERE passenger_id = ? AND is_active = 1
                ORDER BY created_at DESC
                LIMIT 1
            """, (passenger_id,))
            
            row = cur.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"✗ Error getting active passport: {e}")
            return None
    
    # ===================================================================================
    # SERVICE TYPES METHODS
    # ===================================================================================
    
    def get_service_types(self) -> List[Dict[str, Any]]:
        """Get all service types."""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM service_types ORDER BY name")
            return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            print(f"✗ Error getting service types: {e}")
            return []
    
    def get_service_type_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get service type by name."""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM service_types WHERE name = ?", (name,))
            row = cur.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"✗ Error getting service type: {e}")
            return None
    
    # ===================================================================================
    # INVOICE OPERATIONS (Production Schema)
    # ===================================================================================
    
    def save_invoice(self, invoice_data: Dict[str, Any]) -> Tuple[bool, int]:
        
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
