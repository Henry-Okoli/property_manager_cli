
# function to add tenant details in the table
from property_manager.db import get_connection

def add_tenants(full_name, email=None, phone=None, note =None):
    connection = get_connection()
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO tenants (full_name, email, phone, note) "  # the first SQL line ends with a space before the closing quote
                "VALUES (?, ?, ?, ?)",
                (full_name, email, phone, note)
            )
        return cursor.lastrowid
    finally:
        connection.close

def get_tenant(tenant_id):
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT *  FROM tenants WHERE tenant_id = ?",
            (tenant_id,),
        ).fetchone()
        return rows
    finally:
        connection.close

def update_tenant(tenant_id, full_name=None, email=None, phone=None, note=None):
    connection = get_connection()
    try:
        with connection:
            cursor = connection.execute(
                "UPDATE tenants SET "
                "full_name = COALESCE (?, full_name), "
                "email = COALESCE (?, email), "
                "phone = COALESCE (?, phone), "
                "note = COALESCE (?, note) "
                "WHERE tenant_id = ?",
                (full_name, email, phone, note, tenant_id)
            )
        return cursor.rowcount
    finally:
        connection.close

def search_tenant(text=None):
    pattern = f"%ada%" if text else None
    connection = get_connection()
    try:
        return connection.execute(
            "SELECT tenant_id, full_name, email, phone, note " 
            "FROM tenants "
            "WHERE is_archived = 0 "
            "AND (? IS NULL OR full_name LIKE ? OR email LIKE ? OR phone LIKE ?) "
            "ORDER BY tenant_id",
            (pattern, pattern, pattern, pattern),
        ).fetchall()
    finally:
        connection.close()



