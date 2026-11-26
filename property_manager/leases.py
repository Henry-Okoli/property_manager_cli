from property_manager.db import get_connection

def create_leases(property_id, tenant_id, start_date, end_date, rent_pence=None):
    connection = get_connection()
    try:
        with connection:
            property_row = connection.execute(
                "SELECT monthly_rent_pence FROM properties "
                "WHERE property_id = ? AND is_archived = 0",
                (property_id,),
            ).fetchone()
            if property_row is None:
                raise ValueError((f'No active property with id {property_id}.'))

            tenant_row = connection.execute(
                "SELECT tenant_id FROM tenants "
                "WHERE tenant_id = ? AND  is_archived = 0",
                (tenant_id,),
            ).fetchone()
            if tenant_row is None:
                raise ValueError(f'No active tenant with is {tenant_id}.')


            if rent_pence is None:
                rent_pence = property_row["monthly_rent_pence"]    

            cursor = connection.execute(
                "INSERT INTO leases "
                "(property_id, tenant_id, start_date, end_date,monthly_rent_pence)"
                "VALUES (?, ?, ?, ?, ?)",
                (property_id, tenant_id, start_date, end_date, rent_pence),
            )  

            connection.execute(
                "UPDATE properties SET status = 'occupied'  WHERE property_id = ?",
                (property_id,),
            )
        return cursor.lastrowid
    finally:
        connection.close()


def list_leases(status=None):
    connection = get_connection()
    try:
        rows = connection.execute(
            "SELECT l.lease_id, p.name AS property_name, t.full_name AS tenant_name, l.start_date, l.end_date, l.monthly_rent_pence, l.status "
            "FROM leases l " 
            "JOIN properties p ON p.property_id = l.property_id "
            "JOIN tenants t ON t.tenant_id = l.tenant_id "
            "WHERE (? IS NULL OR l.status = ?) "
            "ORDER BY l.lease_id",
            (status, status),
        ).fetchall()
        return rows
    finally:
        connection.close()