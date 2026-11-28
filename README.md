# property_manager_cli

    A command line program for managing rental properties, tenants, and leases. It is build in python with SQLite as a learning project.

## What it does 
- Properties: add, list, view, update, search and archive
- Tenants: add, view, update, search, see lease history
- Leases: create, terminate, list, find leases that are about to expire

## Requiments
Python 3.9 or later. No extra packages are needed.

## Setup
```
git clone https://github.com/Henry-Okoli/property_mananger_cli.git
cd property_manager_cli
python3 main.py init
```

`init` creates the database in th `data/` folder.

## Commands
| Command | What it does | Example |
|---|---|---|
| init | Create the database and tables | python main.py init |
| add-property | Add a property | python main.py add-property --name "Flat3" --address "12 Oak Street" --rent 850 |
| list-properties | List active properties | python main.py list-properties |
| view-property | Show one property | python main.py view-property --id 1 |
| update-property | Change a property | python main.py update-property --id 1 --rent 900 |
| archive-property | Hide a property, keeping its history | python main.py archive-property --id 1 |
| search-properies | Search by text or status | python main.py search-properies --text oak |
| add-tenant | Register a tenant | python main.py add-tenant --name "Ada Obi" --email "ada@gmail.com |
| view-tenant | Show one tenant | python main.py view-tenant --id 1 |
| update-tenant | Change a tenant | python main.py update-tenant -id 1 --phone 07700900123 |
| search-tenants | Search tenants | python main.py search-tenants --text ada |
| create-lease | Create a lease | python main.py create-lease --property 1 --tenant 1 --start 2026-12-01 --end 2027-11-30 |
| terminate-lease | End a lease early | python main.py terminate-lease --id 1 |
| list-leases | List leases | python main.py list-leases --status active |
| expiring-leases | Leases ending soon | python main.py expiring-leases --days 60 |
| tenant-leases | A tenant's lease history | python main.py tenant-leases --id 1 |

Use `python main.py <command> --help` to see all the options for a command.



## Project structure
```
property_manager_cli/
property_manager_cli/
├── main.py                 the command line (reads commands, prints results)
├── sql/schema.sql          the database tables
├── property_manager/
│   ├── db.py               opens the database and builds the tables
│   ├── properties.py       property logic
│   ├── tenants.py          tenant logic
│   └── leases.py           lease logic
└── data/                   the database file (not in Git)
```

## Design decisions

- Money is stored as whole pence, so there are no rounding errors.
- Properties and tenants are archived, not deleted, so we can have history
- Creating or ending a lease changes two tables in one transaction, so both changes happen or not
- A uniqe index allows only one active lease per property.
- The code is three layers: the command line, the logic and the database.


## Not built yet
Rent payments, maintenance request, financial reports and lease renewal.