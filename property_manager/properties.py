# COALESCE(a, b), which means “use a, but if a is empty (NULL), 
# use b.” So rent = COALESCE(new_rent, rent) means “use the new 
# rent if one was given, otherwise keep the current one



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

def update_property(property_id, name=None, address=None, bedrooms=None, 
                    rent_pence=None, status=None):
    connection = get_connection()
    try:
        with connection:
            cursor = connection.execute(            #COALESCE(?, name)	Use the new value if given, otherwise keep the current one.
                "UPDATE properties SET "
                "name = COALESCE(?, name), "
                "address = COALESCE(?, address), "
                "bedrooms = COALESCE(?, bedrooms), "
                "monthly_rent_pence = COALESCE(?, monthly_rent_pence), "
                "status = COALESCE (?, status) "
                "WHERE property_id = ?",
                (name, address, bedrooms, rent_pence, status, property_id),
            )
        return cursor.rowcount
    finally:
        connection.close


def archive_property(property_id):      # this will help keep the our files instead of delecting them. they are in the database but not active
    connection = get_connection()
    try:
        with connection:
            cursor = connection.execute(
                "UPDATE properties SET is_archived = 1 "
                "WHERE property_id = ? AND is_archived = 0",
                (property_id,),
            )
        return cursor.rowcount
    finally:
        connection.close()


# find properties either by name, address, status, or both 

def search_properties(text=None, status=None):
    pattern = f"%{text}%" if text else None
    connection = get_connection()
    try:
        return connection.execute(
            "SELECT property_id, name, address, bedrooms, monthly_rent_pence, status "
            "FROM properties "
            "WHERE is_archived = 0 "
            "AND (? IS NULL OR name LIKE ? OR address LIKE ?) "
            "AND (? IS NULL OR status = ?) "
            "ORDER BY property_id",
            (pattern, pattern, pattern, status, status),
        ).fetchall()
    finally:
        connection.close()



