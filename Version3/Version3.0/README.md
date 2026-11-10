# Finance Analyzer - Version 3.0

A personal finance analyzer that stores transactions in SQLite and provides both a command-line menu and a local web interface.

## Features

- View income, expenses, and net cash flow
- Add, edit, and delete transactions
- Filter transactions from the command-line interface
- Store and reload transactions in SQLite

## How the code is organized

- `database.py` creates the SQLite table, validates transaction data, and reads or writes records.
- `finance.py` contains the calculations and the original command-line transaction workflows.
- `main.py` starts the command-line interface.
- `app.py` connects the browser pages to the same database and calculation functions.
- `templates/` contains the HTML pages rendered by Flask.
- `tests/` checks the database, calculations, and web routes using temporary databases.

## Requirements

- Python 3.10 or newer
- Flask 3.x

Install Flask from this directory:

```powershell
python -m pip install -r requirements.txt
```

## Web interface

From `Version3/Version3.0`, start the local web app:

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). The dashboard shows the financial summary and transaction list, and provides forms to add, edit, or delete entries. The app binds to localhost and stores data in `finance.db` beside the Python files, regardless of the directory used to launch it. The database is ignored by Git so personal transaction data is not included in commits.

## Command-line interface

Run `python main.py` from this directory to use the original menu-based program.

## Tests

Run the test suite from this directory:

```powershell
python -m unittest discover -s tests -v
```
