import sqlite3

## Open and return a connection to the SQLite database.
def get_connection():
    connection = sqlite3.connect("finance.db")
    return connection  

## Create the data folder and transactions table if they don't exist.
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT, 
        description TEXT,
        category TEXT, 
        amount REAL, 
        type TEXT)
    )
    """)

    connection.commit()
    connection.close()

## Return all transactions, ordered by date or ID.
def get_all_transactions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY id")

    rows = cursor.fetchall()

    connection.close()
    return rows

def add_transaction(transaction):
    """Insert one validated transaction and return its new ID."""

def update_transaction(transaction_id, transaction):
    """Update a transaction by its database ID."""

def delete_transaction(transaction_id):
    """Delete a transaction by its database ID."""