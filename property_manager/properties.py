from property_manager.db import get_connection

def add_property(name, address, rent_pence, bedrooms=None):
    connection = get_connection()
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO properties (name, address, bedrooms, monthly_rent_pence)"
                "VALUES (?, ?, ?, ?)",
                (name, address, bedrooms, rent_pence),
            )
        return cursor.lastrowid
    finally:
        connection.close()

def list_properties():
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT property_id, name, address, bedrooms, monthly_rent_pence, status "
            "FROM properties WHERE is_archived = 0 ORDER BY property_id"
        ).fetchall()
        return rows
    finally:
        connection.close()

#def list_properties():
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT property_id, name, address, bedrooms, monthly_rent_pence, status "
            "FROM properties WHERE is_archived = 0 ORDER BY property_id"
        ).fetchall()
        return rows
    finally:
        connection.close() 

def get_property(property_id):
    connection = get_connection()
    try:
        return connection.execute(
            "SELECT * FROM properties WHERE property_id = ?",
            (property_id,),
        ).fetchone()
    finally:
        connection.close()