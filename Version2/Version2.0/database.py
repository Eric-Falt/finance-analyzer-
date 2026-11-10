import math
import sqlite3
from datetime import datetime

DB_PATH = "finance.db"


## Open and return a connection to the SQLite database.
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _parse_date(value):
    if value is None:
        raise ValueError("Date is required")

    if isinstance(value, datetime):
        return value

    value = str(value).strip()
    if not value:
        raise ValueError("Date is required")

    for pattern in ("%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, pattern)
        except ValueError:
            continue

    raise ValueError("Date must be formatted MM/DD/YYYY HH:MM")


def _normalize_transaction(transaction):
    if transaction is None:
        raise ValueError("Transaction cannot be blank")

    if not isinstance(transaction, dict):
        raise TypeError("Transaction must be provided as a dictionary")

    date_value = _parse_date(transaction.get("DateTime"))
    description = str(transaction.get("Description", "")).strip()
    category = str(transaction.get("Category", "")).strip()
    amount_value = transaction.get("Amount")
    transaction_type = str(transaction.get("Type", "")).strip().title()

    if not description:
        raise ValueError("Description is required")
    if not category:
        raise ValueError("Category is required")

    try:
        amount = float(amount_value)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number") from None

    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("Amount must be a positive finite number")

    if transaction_type not in {"Income", "Expense"}:
        raise ValueError("Type must be 'Income' or 'Expense'")

    normalized = {
        "DateTime": date_value,
        "Description": description.title(),
        "Category": category.title(),
        "Amount": amount,
        "Type": transaction_type,
    }

    if "id" in transaction:
        normalized["id"] = transaction["id"]

    return normalized


normalize_transaction = _normalize_transaction


def _row_to_transaction(row):
    if row is None:
        return None

    payload = dict(row)
    date_text = payload.get("date") or payload.get("DateTime")

    if isinstance(date_text, str):
        date_value = _parse_date(date_text)
    else:
        date_value = date_text

    return {
        "id": payload.get("id"),
        "DateTime": date_value,
        "Description": payload.get("description", payload.get("Description", "")),
        "Category": payload.get("category", payload.get("Category", "")),
        "Amount": float(payload.get("amount", payload.get("Amount", 0))),
        "Type": payload.get("type", payload.get("Type", "")),
    }


## Create the transactions table if it doesn't exist.
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
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
        """
    )

    connection.commit()
    connection.close()


## Return all transactions, ordered by date or ID.
def get_all_transactions():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date ASC, id ASC")
    rows = cursor.fetchall()
    connection.close()
    return [_row_to_transaction(row) for row in rows]


## Insert one validated transaction and return its new ID.
def add_transaction(transaction):
    transaction = _normalize_transaction(transaction)
    connection = get_connection()
    cursor = connection.cursor()

    date_text = transaction["DateTime"].strftime("%m/%d/%Y %H:%M")
    cursor.execute(
        """
        INSERT INTO transactions (date, description, category, amount, type)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            date_text,
            transaction["Description"],
            transaction["Category"],
            transaction["Amount"],
            transaction["Type"],
        ),
    )
    connection.commit()
    inserted_id = cursor.lastrowid
    connection.close()
    return inserted_id


def update_transaction(transaction_id, transaction):
    """Update a transaction by its database ID."""
    transaction = _normalize_transaction(transaction)
    connection = get_connection()
    cursor = connection.cursor()

    date_text = transaction["DateTime"].strftime("%m/%d/%Y %H:%M")
    cursor.execute(
        """
        UPDATE transactions
        SET date = ?, description = ?, category = ?, amount = ?, type = ?
        WHERE id = ?
        """,
        (
            date_text,
            transaction["Description"],
            transaction["Category"],
            transaction["Amount"],
            transaction["Type"],
            transaction_id,
        ),
    )
    connection.commit()
    updated_rows = cursor.rowcount
    connection.close()
    return updated_rows


def delete_transaction(transaction_id):
    """Delete a transaction by its database ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    connection.commit()
    deleted_rows = cursor.rowcount
    connection.close()
    return deleted_rows


def save_transactions(transactions):
    """Replace the database contents with the provided transaction list."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transactions")

    for transaction in transactions:
        normalized = _normalize_transaction(transaction)
        cursor.execute(
            """
            INSERT INTO transactions (date, description, category, amount, type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                normalized["DateTime"].strftime("%m/%d/%Y %H:%M"),
                normalized["Description"],
                normalized["Category"],
                normalized["Amount"],
                normalized["Type"],
            ),
        )

    connection.commit()
    connection.close()
