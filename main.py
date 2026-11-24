import argparse
import sqlite3
from decimal import Decimal, InvalidOperation
from property_manager import db, properties, tenants


def pounds_to_pence(text):
    try:
        pounds = Decimal(text)
    except InvalidOperation:
        raise argparse.ArgumentTypeError(f"'{text}' is not a valid amount")
    if pounds <= 0:
        raise argparse.ArgumentTypeError("rent must be more than Zero")
    return int(pounds * 100)

    
def build_parser():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Property Management CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="create the database and tables")

# list properties
    subparsers.add_parser("list-properties", help="List all properties")

# view property
    view = subparsers.add_parser("view-property", help="show one property in full" )

# update properites
    update = subparsers.add_parser("update-property", help="Change details of the property")
    update.add_argument("--id", type=int, required=True, help="The property number")
    update.add_argument("--name")
    update.add_argument("--address")
    update.add_argument("--bedrooms", type=int)
    update.add_argument("--rent", type=pounds_to_pence, help="New monthly rent in pounds")
    update.add_argument("--status", choices=["available", "occupied", "maintenance"])

# archive properies
    archive = subparsers.add_parser("archive-property", help="hide property (it history is kept)") # archive property
    archive.add_argument("--id", type=int, required=True, help="The property number")

#search properties
    search = subparsers.add_parser("search-properties", help="Find properties by text or status")
    search.add_argument("--text", help="Part of the name or address")
    search.add_argument("--status", choices=["available", "occupied", "maintenace"])

#add properties
    add = subparsers.add_parser("add-property", help="Add a new property")
    add.add_argument("--name", required=True, help="short unique name")
    add.add_argument("--address", required=True, help="Full address")
    add.add_argument("--rent", required=True, type=pounds_to_pence, help="Monthly rent in pounds, e.g. 850")
    add.add_argument("--bedrooms", type=int, help="Number of bedrooms")
    view.add_argument("--id", type=int, required=True, help="The property number")


# Tenent commands
# add tenants
    add_tenant_parser = subparsers.add_parser("add-tenant", help="regiester a new tenants")
    add_tenant_parser.add_argument("--name", required=True, help="full name")
    add_tenant_parser.add_argument("--email")
    add_tenant_parser.add_argument("--phone")
    add_tenant_parser.add_argument("--notes")
   
#view tenant
    view_tenant = subparsers.add_parser("view-tenant", help="show one tenant in full")
    view_tenant.add_argument("--id", type=int, required=True, help="The tenant Number" )


# update tenants
    update_tenant = subparsers.add_parser("update-tenant", help="change detail of the tenant")
    update_tenant.add_argument("--id", type=int, required=True, help="The tenant number")
    update_tenant.add_argument("--full_name")
    update_tenant.add_argument("--email")
    update_tenant.add_argument("--phone")
    update_tenant.add_argument("--note")
    return parser



def print_properties(rows):
    if not rows:
        print("No properties found.")
    for row in rows:
        rent = row["monthly_rent_pence"] / 100
        print(f'{row["property_id"]:>3} {row["name"]:<12} {row["address"]:<30} £{rent:>8.2f} {row["status"]}')



def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        db.init_db()
        print("Database ready")


    if args.command == "add-property":
        try:
            property_id = properties.add_property(
                args.name, args.address, args.rent, args.bedrooms
            )
        except sqlite3.IntegrityError as error:
            print(f"Could not add the property: {error}")
        else:
            print(f"Property {property_id} added: {args.name}")


    if args.command == "list-properties":
        print_properties(properties.list_properties())
        #rows = properties.list_properties()
        #if not rows:
            #print("No properties yet.")
        #for row in rows:
            #rent = row["monthly_rent_pence"] / 100
            #print(f'{row["property_id"]:>3} {row["name"]:<12} {row["address"]:<30} £{rent:>8.2f} {row["status"]}')


    if args.command == "view-property":
        row = properties.get_property(args.id)
        if row is None:
            print(f'No property with id {args.id}.')
        else:
            print(f' Property {row["property_id"]}: {row["name"]}')
            print(f' Address: {row["address"]}')
            print(f' Bedrooms: {row["bedrooms"]}')
            print(f' Rent: £{row["monthly_rent_pence"] / 100:.2f} a month')
            print(f' Status: {row["status"]} ')


    if args.command == "update-property":
        try:
            changed = properties.update_property(
                args.id,
                name=args.name,
                address=args.address,
                bedrooms=args.bedrooms,
                rent_pence=args.rent,
                status=args.status,
            )
        except sqlite3.IntegrityError as error:
            print(f"Could not update the property: {error}")
        else:
            if changed == 0:
                print(f"No property with id {args.id}.")
            else:
                print(f"Property {args.id} updated.")


    if args.command == "archive-property":
        changed = properties.archive_property(args.id)
        if changed == 0:
            print(f"No active property with id {args.id}.")
        else:
            print(f"Property {args.id} archived.")


    if args.command == "search-properties":
        print_properties(properties.search_properties(args.text, args.status))


# Teneants command

    if args.command == "add-tenant":
        try:
            tenant_id = tenants.add_tenants(
                args.name, email=args.email, phone=args.phone, note=args.notes
            )
        except sqlite3.IntegrityError as error:
            print(f"Could not add the tenant: {error}")
        else:
            print(f"Tenant {tenants} added: {args.name}")


    if args.command == "view-tenant":
        row = tenants.get_tenant(args.id)
        if row is None:
            print(f"No tenant with id {args.id}.")
        else:
            print(f' tenant {row["tenant_id"]}: {row["full_name"]}')
            print(f' email: {row["email"]}')
            print(f' phone: {row["phone"]}')
            print(f' note: {row["note"]}')


    if args.command == "update-tenant":
        try:
            changed = tenants.update_tenant(
                args.id,
                full_name=args.full_name,
                email=args.email,
                phone=args.phone,
                note=args.note,
            )
        except sqlite3.IntegrityError as error:
            print(f'Could not oupdate tenant: {error}')
        else:
            if changed == 0:
                print(f'No tenant with id: {args.id}')
            else:
                print(f'Tenant {args.id} Updated ')




if __name__ == "__main__":
    main()