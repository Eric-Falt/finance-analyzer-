import sqlite3
from datetime import datetime

## Open and return a connection to the SQLite database.
def get_connection():
    connection = sqlite3.connect("finance.db")

    # Make queries return rows 
    connection.row_factory = sqlite3.Row

    return connection  

## Create the data folder and transactions table if they don't exist.
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Create a table with the proper headers and types, id just counts each entry 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL 
            CONSTRAINT valid_date CHECK (length(trim(date)) > 0),
        description TEXT NOT NULL 
            CONSTRAINT valid_description CHECK (length(trim(description)) > 0),
        category TEXT NOT NULL 
            CONSTRAINT valid_category CHECK (length(trim(category)) > 0),
        amount REAL NOT NULL 
            CONSTRAINT valid_amount CHECK (amount > 0),
        type TEXT NOT NULL 
            CONSTRAINT valid_type CHECK (type IN ('Income', 'Expense'))
    )
    """)

    connection.commit()
    connection.close()

## Return all transactions, ordered by date or ID.
def get_all_transactions():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date")

    rows = cursor.fetchall()

    connection.close()
    return rows

## Insert one validated transaction and return its new ID.
def add_transaction(transaction):
    connection = get_connection()
    cursor = connection.cursor()

    date_value = transaction.get("DateTime")

    try: 
        date = (date_value 
                if isinstance(date_value, datetime)
                else datetime.strptime(str(date_value).strip(), "%m/%d/%Y %H:%M")
            )
    except ValueError:
        raise ValueError("Date must be formatted MM/DD/YYYY HH:MM") from None

    cursor.execute("""
        INSERT INTO transactions (date, description, category, amount, type)
        VALUES (?, ?, ?, ?, ?)
                        """)

    connection.commit()
    connection.close()


def update_transaction(transaction_id, transaction):
    """Update a transaction by its database ID."""

def delete_transaction(transaction_id):
    """Delete a transaction by its database ID."""