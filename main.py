import argparse
from property_manager import db

def build_parser():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Property Management CLI",
    )
    subparesers = parser.add_subparsers(dest="command", required=True)
    subparesers.add_parser("init", help="create the database and tables")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        db.init_db()
        print("Database ready")

if __name__ == "__main__":
    main()