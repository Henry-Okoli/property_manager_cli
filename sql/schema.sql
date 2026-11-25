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


CREATE TABLE IF NOT EXISTS leases(
    lease_id INTEGER PRIMARY KEY,
    property_id INTEGER NOT NULL REFERENCES properties (property_id),
    tenant_id INTEGER NOT NULL REFERENCES tenants (tenant_id),
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    monthly_rent_pence INTEGER NOT NULL CHECK (monthly_rent_pence > 0),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'terminated')),
    terminated_on TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_date > start_date)
);

CREATE UNIQUE INDEX IF NOT EXISTS one_active_lease_per_property ON leases (property_id) WHERE status = 'active';