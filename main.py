import argparse
import sqlite3
from decimal import Decimal, InvalidOperation
from property_manager import db, properties


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
    subparesers = parser.add_subparsers(dest="command", required=True)

    subparesers.add_parser("init", help="create the database and tables")

    subparesers.add_parser("list-properties", help="List all properties")

    view = subparesers.add_parser("view-property", help="show one property in full" )


    update = subparesers.add_parser("update-property", help="Change details of the property")
    update.add_argument("--id", type=int, required=True, help="The property number")
    update.add_argument("--name")
    update.add_argument("--address")
    update.add_argument("--bedrooms", type=int)
    update.add_argument("--rent", type=pounds_to_pence, help="New monthly rent in pounds")
    update.add_argument("--status", choices=["available", "occupied", "maintenance"])



    add = subparesers.add_parser("add-property", help="Add a new property")
    add.add_argument("--name", required=True, help="short unique name")
    add.add_argument("--address", required=True, help="Full address")
    add.add_argument("--rent", required=True, type=pounds_to_pence, help="Monthly rent in pounds, e.g. 850")
    add.add_argument("--bedrooms", type=int, help="Number of bedrooms")
    view.add_argument("--id", type=int, required=True, help="The property number")
    return parser

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
        rows = properties.list_properties()
        if not rows:
            print("No properties yet.")
        for row in rows:
            rent = row["monthly_rent_pence"] / 100
            print(f'{row["property_id"]:>3} {row["name"]:<12} {row["address"]:<30} £{rent:>8.2f} {row["status"]}')


    if args.command == "view-property":
        row = properties.get_property(args.id)
        if row is None:
            print(f'No property with id {args.id}.')
        else:
            print(f' Property {row["property_id"]}: {row["name"]}')
            print(f' Addre`ss: {row["address"]}')
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

if __name__ == "__main__":
    main()