
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

def get_tenat(tenant_id):
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT *  FROM tenants WHERE tenant_id = ?",
            (tenant_id,),
        ).fetchone()
        return rows
    finally:
        connection.close
