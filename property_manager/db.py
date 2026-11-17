# get_connection(): opens the database file, so no other file needs to know where it lives.
# init_db(): reads schema.sql and builds the tables, so one command sets up an empty database.

import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "property_manager.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / 'schema.sql'

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db():
    schema = SCHEMA_PATH.read_text()
    connection = get_connection()
    try:
        connection.executescript(schema)
    finally:
        connection.close()

if __name__ == "__main__":
    init_db()
    print("Database ready.")