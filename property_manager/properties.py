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
