-- ===================================================================================
-- AL-CHISHTHIYA TRAVELS - PRODUCTION DATABASE SCHEMA (FINAL)
-- ===================================================================================
-- Designed for: Dynamic Pricing, Family/Group Logic, Visa Tracking, Profit Reports.
-- Security: User Audit Trails & Foreign Key Integrity.
-- ===================================================================================

PRAGMA foreign_keys = ON;

-- ===================================================================================
-- 1. SECURITY & USERS (The "Gatekeepers")
-- ===================================================================================

-- Table: users
-- Stores staff login details. Critical for knowing WHO did WHAT.
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL, -- Store hashed passwords, not plain text
    role TEXT CHECK(role IN ('ADMIN', 'STAFF')) DEFAULT 'STAFF',
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================================================
-- 2. MASTER TABLES (The "Who" and "What")
-- ===================================================================================

-- Table: contacts
-- Stores both CUSTOMERS (Clients) and SUPPLIERS (Airlines/Wholesalers).
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT CHECK(type IN ('CUSTOMER', 'SUPPLIER')) NOT NULL,
    name TEXT NOT NULL,
    company_name TEXT,          -- Useful for B2B suppliers
    phone TEXT,                 -- Indexed for fast searching
    email TEXT,
    address TEXT,
    gstin TEXT,
    opening_balance DECIMAL(10,2) DEFAULT 0.00, -- +ve = They owe us, -ve = We owe them
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contacts_phone ON contacts(phone);
CREATE INDEX idx_contacts_name ON contacts(name);

-- Table: passengers
-- Stores individual travelers linked to a primary Contact.
CREATE TABLE passengers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    contact_number TEXT,
    whatsapp_number TEXT,
    dob DATE,
    age INTEGER,
    nationality TEXT,
    gender TEXT CHECK(gender IN ('M', 'F', 'O')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
);

-- Table: passport_details
-- Linked to passengers. Allows multiple/history of passports.
CREATE TABLE passport_details (
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
    file_path TEXT,              -- Path to scanned image
    is_active BOOLEAN DEFAULT 1, -- 1 = Current Passport, 0 = Old
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (passenger_id) REFERENCES passengers(id) ON DELETE CASCADE
);

CREATE INDEX idx_passport_number ON passport_details(passport_number);

-- Table: service_types
-- Categories for your sales (e.g., 'Air Ticket', 'Visa', 'Hotel').
CREATE TABLE service_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    default_hsn_sac TEXT
);

-- ===================================================================================
-- 3. SALES & TRANSACTIONS (The "Work")
-- ===================================================================================

-- Table: invoices
-- Sales Headers.
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE NOT NULL,
    contact_id INTEGER NOT NULL,
    date DATE NOT NULL,
    due_date DATE,
    
    -- Financials
    sub_total DECIMAL(10,2) DEFAULT 0.00,
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    round_off DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    
    -- Status
    status TEXT CHECK(status IN ('DRAFT', 'FINAL', 'CANCELLED')) DEFAULT 'DRAFT',
    payment_status TEXT CHECK(payment_status IN ('PAID', 'PARTIAL', 'UNPAID')) DEFAULT 'UNPAID',
    
    notes TEXT,
    created_by INTEGER,          -- Audit: Which staff made this?
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (contact_id) REFERENCES contacts(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Table: invoice_items
-- The heart of the system. Tracks Profit, Travel Details, and Visas.
CREATE TABLE invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,
    service_type_id INTEGER NOT NULL,
    passenger_id INTEGER,             -- Linked passenger (optional)
    
    description TEXT,
    
    -- Travel Specifics
    pnr_number TEXT,
    ticket_number TEXT,
    sector TEXT,
    travel_date DATE,
    airline_name TEXT,
    
    -- Visa Specifics
    visa_application_date DATE,
    visa_status TEXT CHECK(visa_status IN ('PENDING', 'SUBMITTED', 'ISSUED', 'REJECTED', 'NA')) DEFAULT 'NA',
    
    -- Pricing
    quantity INTEGER DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL, -- Selling Price
    tax_rate DECIMAL(5,2) DEFAULT 0.00,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(10,2) NOT NULL,
    
    -- Profit Calculation (Hidden)
    cost_price DECIMAL(10,2) DEFAULT 0.00,
    supplier_id INTEGER,                   -- Who did we buy this from?
    
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
    FOREIGN KEY (service_type_id) REFERENCES service_types(id),
    FOREIGN KEY (passenger_id) REFERENCES passengers(id),
    FOREIGN KEY (supplier_id) REFERENCES contacts(id)
);

-- ===================================================================================
-- 4. FINANCIALS (Money In / Money Out)
-- ===================================================================================

-- Table: payments_received
-- Money IN from Customers.
CREATE TABLE payments_received (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_number TEXT UNIQUE,
    date DATE NOT NULL,
    contact_id INTEGER NOT NULL,
    invoice_id INTEGER,          -- Optional link
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

-- Table: supplier_payments
-- Money OUT to Suppliers (Airlines/Wholesalers).
-- This separates "Business Debt" from "Office Expenses".
CREATE TABLE supplier_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_number TEXT UNIQUE,
    date DATE NOT NULL,
    supplier_id INTEGER NOT NULL, -- Must be a CONTACT of type SUPPLIER
    amount DECIMAL(10,2) NOT NULL,
    payment_mode TEXT,
    reference_number TEXT,
    notes TEXT,
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (supplier_id) REFERENCES contacts(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Table: expenses
-- General Office Overheads (Rent, Tea, Electricity).
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount DECIMAL(10,2) NOT NULL,
    payment_mode TEXT DEFAULT 'CASH',
    paid_to TEXT,
    person_responsible TEXT,
    reference_number TEXT,      -- Fixed Syntax Error here
    created_by INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Table: purchase_bills
-- Bills received from Suppliers (Accounts Payable).
CREATE TABLE purchase_bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_number TEXT,
    supplier_id INTEGER NOT NULL,
    date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    due_date DATE,
    notes TEXT,
    attachment_path TEXT,        -- Scan of the supplier bill
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES contacts(id)
);

-- ===================================================================================
-- 5. AUTOMATION
-- ===================================================================================

CREATE TRIGGER update_contacts_timestamp 
AFTER UPDATE ON contacts
BEGIN
    UPDATE contacts SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER update_invoices_timestamp 
AFTER UPDATE ON invoices
BEGIN
    UPDATE invoices SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;