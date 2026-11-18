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
    
    add = subparesers.add_parser("add-property", help="Add a new property")
    add.add_argument("--name", required=True, help="short unique name")
    add.add_argument("--address", required=True, help="Full address")
    add.add_argument("--rent", required=True, type=pounds_to_pence, help="Monthly rent in pounds, e.g. 850")
    add.add_argument("--bedrooms", type=int, help="Number of bedrooms")
    
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

if __name__ == "__main__":
    main()