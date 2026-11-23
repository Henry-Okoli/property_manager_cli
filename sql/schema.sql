CREATE TABLE IF NOT EXISTS properties (
    property_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    bedrooms INTEGER CHECK(bedrooms >= 0),
    monthly_rent_pence INTEGER NOT NULL CHECK(monthly_rent_pence > 0),
    status TEXT NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'occupied', 'maintenance')),
    is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0,1)), 
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS tenants (
    tenant_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    note TEXT ,
    is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0,1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

