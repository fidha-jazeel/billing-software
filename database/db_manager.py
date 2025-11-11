import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path='billing.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Create and return a database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_number TEXT,
                email TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Items/Services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                default_price REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Invoices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                customer_name TEXT,
                invoice_date DATE NOT NULL,
                subtotal REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                total_amount REAL DEFAULT 0,
                received_amount REAL DEFAULT 0,
                balance REAL DEFAULT 0,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        ''')
        
        # Invoice items table (for detailed line items)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                ticket_number TEXT,
                sector TEXT,
                supplier TEXT,
                quantity INTEGER DEFAULT 1,
                price_per_unit REAL DEFAULT 0,
                tax_percentage REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                amount REAL DEFAULT 0,
                cash REAL DEFAULT 0,
                bank REAL DEFAULT 0,
                balance REAL DEFAULT 0,
                profit REAL DEFAULT 0,
                FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT DEFAULT 'Travel Agency',
                company_address TEXT,
                company_contact TEXT,
                company_email TEXT,
                company_gst TEXT,
                invoice_prefix TEXT DEFAULT 'INV',
                last_invoice_number INTEGER DEFAULT 0,
                currency_symbol TEXT DEFAULT '₹'
            )
        ''')
        
        # Initialize default settings if not exists
        cursor.execute('SELECT COUNT(*) FROM settings')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO settings (company_name, invoice_prefix, last_invoice_number)
                VALUES ('Travel Agency', 'INV', 0)
            ''')
        
        conn.commit()
        conn.close()
    
    # Customer operations
    def add_customer(self, name: str, contact: str = '', email: str = '', address: str = '') -> int:
        """Add a new customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, contact_number, email, address)
            VALUES (?, ?, ?, ?)
        ''', (name, contact, email, address))
        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()
        return customer_id
    
    def get_all_customers(self) -> List[Dict]:
        """Get all customers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers ORDER BY name')
        customers = []
        for row in cursor.fetchall():
            customers.append({
                'id': row[0],
                'name': row[1],
                'contact_number': row[2],
                'email': row[3],
                'address': row[4],
                'created_at': row[5]
            })
        conn.close()
        return customers
    
    def search_customers(self, query: str) -> List[Dict]:
        """Search customers by name or contact"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM customers 
            WHERE name LIKE ? OR contact_number LIKE ?
            ORDER BY name
        ''', (f'%{query}%', f'%{query}%'))
        customers = []
        for row in cursor.fetchall():
            customers.append({
                'id': row[0],
                'name': row[1],
                'contact_number': row[2],
                'email': row[3],
                'address': row[4]
            })
        conn.close()
        return customers
    
    # Item operations
    def add_item(self, name: str, description: str = '', default_price: float = 0) -> int:
        """Add a new item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO items (name, description, default_price)
            VALUES (?, ?, ?)
        ''', (name, description, default_price))
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()
        return item_id
    
    def get_all_items(self) -> List[Dict]:
        """Get all items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items ORDER BY name')
        items = []
        for row in cursor.fetchall():
            items.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'default_price': row[3]
            })
        conn.close()
        return items
    
    # Invoice operations
    def get_next_invoice_number(self) -> str:
        """Generate next invoice number"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT invoice_prefix, last_invoice_number FROM settings WHERE id = 1')
        row = cursor.fetchone()
        prefix = row[0] if row else 'INV'
        last_number = row[1] if row else 0
        
        new_number = last_number + 1
        cursor.execute('UPDATE settings SET last_invoice_number = ? WHERE id = 1', (new_number,))
        conn.commit()
        conn.close()
        
        return f"{prefix}-{new_number:04d}"
    
    def create_invoice(self, invoice_data: Dict, items: List[Dict]) -> int:
        """Create a new invoice with items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insert invoice
            cursor.execute('''
                INSERT INTO invoices (
                    invoice_number, customer_id, customer_name, invoice_date,
                    subtotal, tax_amount, total_amount, received_amount, balance, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                invoice_data['invoice_number'],
                invoice_data.get('customer_id'),
                invoice_data['customer_name'],
                invoice_data['invoice_date'],
                invoice_data['subtotal'],
                invoice_data['tax_amount'],
                invoice_data['total_amount'],
                invoice_data.get('received_amount', 0),
                invoice_data.get('balance', invoice_data['total_amount']),
                invoice_data.get('notes', '')
            ))
            
            invoice_id = cursor.lastrowid
            
            # Insert invoice items
            for item in items:
                cursor.execute('''
                    INSERT INTO invoice_items (
                        invoice_id, item_name, ticket_number, sector, supplier,
                        quantity, price_per_unit, tax_percentage, tax_amount, amount,
                        cash, bank, balance, profit
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    invoice_id,
                    item['item_name'],
                    item.get('ticket_number', ''),
                    item.get('sector', ''),
                    item.get('supplier', ''),
                    item.get('quantity', 1),
                    item.get('price_per_unit', 0),
                    item.get('tax_percentage', 0),
                    item.get('tax_amount', 0),
                    item.get('amount', 0),
                    item.get('cash', 0),
                    item.get('bank', 0),
                    item.get('balance', 0),
                    item.get('profit', 0)
                ))
            
            conn.commit()
            return invoice_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_invoice(self, invoice_id: int) -> Optional[Dict]:
        """Get invoice by ID with items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get invoice
        cursor.execute('SELECT * FROM invoices WHERE id = ?', (invoice_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        invoice = {
            'id': row[0],
            'invoice_number': row[1],
            'customer_id': row[2],
            'customer_name': row[3],
            'invoice_date': row[4],
            'subtotal': row[5],
            'tax_amount': row[6],
            'total_amount': row[7],
            'received_amount': row[8],
            'balance': row[9],
            'status': row[10],
            'notes': row[11],
            'created_at': row[12]
        }
        
        # Get invoice items
        cursor.execute('SELECT * FROM invoice_items WHERE invoice_id = ?', (invoice_id,))
        items = []
        for item_row in cursor.fetchall():
            items.append({
                'id': item_row[0],
                'item_name': item_row[2],
                'ticket_number': item_row[3],
                'sector': item_row[4],
                'supplier': item_row[5],
                'quantity': item_row[6],
                'price_per_unit': item_row[7],
                'tax_percentage': item_row[8],
                'tax_amount': item_row[9],
                'amount': item_row[10],
                'cash': item_row[11],
                'bank': item_row[12],
                'balance': item_row[13],
                'profit': item_row[14]
            })
        
        invoice['items'] = items
        conn.close()
        return invoice
    
    def get_all_invoices(self, limit: int = 100) -> List[Dict]:
        """Get all invoices"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM invoices 
            ORDER BY invoice_date DESC, created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        invoices = []
        for row in cursor.fetchall():
            invoices.append({
                'id': row[0],
                'invoice_number': row[1],
                'customer_name': row[3],
                'invoice_date': row[4],
                'total_amount': row[7],
                'received_amount': row[8],
                'balance': row[9],
                'status': row[10]
            })
        conn.close()
        return invoices
    
    def search_invoices(self, query: str) -> List[Dict]:
        """Search invoices by invoice number or customer name"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM invoices 
            WHERE invoice_number LIKE ? OR customer_name LIKE ?
            ORDER BY invoice_date DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        invoices = []
        for row in cursor.fetchall():
            invoices.append({
                'id': row[0],
                'invoice_number': row[1],
                'customer_name': row[3],
                'invoice_date': row[4],
                'total_amount': row[7],
                'balance': row[9]
            })
        conn.close()
        return invoices
    
    # Reports and Analytics
    def get_sales_summary(self, start_date: str = None, end_date: str = None) -> Dict:
        """Get sales summary for date range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_invoices,
                    SUM(total_amount) as total_sales,
                    SUM(received_amount) as total_received,
                    SUM(balance) as total_balance,
                    AVG(total_amount) as average_sale
                FROM invoices
                WHERE invoice_date BETWEEN ? AND ?
            ''', (start_date, end_date))
        else:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_invoices,
                    SUM(total_amount) as total_sales,
                    SUM(received_amount) as total_received,
                    SUM(balance) as total_balance,
                    AVG(total_amount) as average_sale
                FROM invoices
            ''')
        
        row = cursor.fetchone()
        summary = {
            'total_invoices': row[0] or 0,
            'total_sales': row[1] or 0,
            'total_received': row[2] or 0,
            'total_balance': row[3] or 0,
            'average_sale': row[4] or 0
        }
        conn.close()
        return summary
    
    def get_daily_sales(self, days: int = 30) -> List[Tuple]:
        """Get daily sales for last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                invoice_date,
                COUNT(*) as count,
                SUM(total_amount) as total
            FROM invoices
            WHERE invoice_date >= date('now', '-' || ? || ' days')
            GROUP BY invoice_date
            ORDER BY invoice_date DESC
        ''', (days,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_top_customers(self, limit: int = 10) -> List[Dict]:
        """Get top customers by total sales"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                customer_name,
                COUNT(*) as invoice_count,
                SUM(total_amount) as total_sales
            FROM invoices
            WHERE customer_name IS NOT NULL AND customer_name != ''
            GROUP BY customer_name
            ORDER BY total_sales DESC
            LIMIT ?
        ''', (limit,))
        
        customers = []
        for row in cursor.fetchall():
            customers.append({
                'customer_name': row[0],
                'invoice_count': row[1],
                'total_sales': row[2]
            })
        conn.close()
        return customers
    
    # Settings operations
    def get_settings(self) -> Dict:
        """Get application settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM settings WHERE id = 1')
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'company_name': row[1],
                'company_address': row[2],
                'company_contact': row[3],
                'company_email': row[4],
                'company_gst': row[5],
                'invoice_prefix': row[6],
                'last_invoice_number': row[7],
                'currency_symbol': row[8]
            }
        return {}
    
    def update_settings(self, settings: Dict):
        """Update application settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE settings SET
                company_name = ?,
                company_address = ?,
                company_contact = ?,
                company_email = ?,
                company_gst = ?,
                invoice_prefix = ?,
                currency_symbol = ?
            WHERE id = 1
        ''', (
            settings.get('company_name', ''),
            settings.get('company_address', ''),
            settings.get('company_contact', ''),
            settings.get('company_email', ''),
            settings.get('company_gst', ''),
            settings.get('invoice_prefix', 'INV'),
            settings.get('currency_symbol', '₹')
        ))
        conn.commit()
        conn.close()
