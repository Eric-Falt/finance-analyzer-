"""SQLite storage and validation helpers shared by the CLI and web app."""

import math
import sqlite3
from datetime import datetime
from pathlib import Path

# The database file is created in the directory where the program is launched.
DB_PATH = str(Path(__file__).resolve().parent / "finance.db")


def get_connection():
    """Open the app's SQLite database and return rows by column name."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _parse_date(value):
    """Accept the date formats used by the app and return a datetime object."""
    if value is None:
        raise ValueError("Date is required")

    if isinstance(value, datetime):
        return value

    value = str(value).strip()
    if not value:
        raise ValueError("Date is required")

    # Support the CLI's display format and common SQLite/browser date formats.
    for pattern in ("%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(value, pattern)
        except ValueError:
            continue

    raise ValueError("Date must be formatted MM/DD/YYYY HH:MM")


def _normalize_transaction(transaction):
    """Validate transaction fields and standardize them before database writes."""
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

    # Keep one consistent Python representation regardless of which interface
    # submitted the transaction.
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
    """Convert a SQLite row to the dictionary format used by finance.py."""
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


def initialize_database():
    """Create the transactions table on first run; leave existing data intact."""
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


def get_all_transactions():
    """Load every transaction, oldest first, and convert rows to dictionaries."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date ASC, id ASC")
    rows = cursor.fetchall()
    connection.close()
    return [_row_to_transaction(row) for row in rows]


def add_transaction(transaction):
    """Validate and insert a transaction, returning its generated database ID."""
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
    """Update one transaction; return the number of rows that matched its ID."""
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
    """Delete one transaction; return the number of rows removed."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    connection.commit()
    deleted_rows = cursor.rowcount
    connection.close()
    return deleted_rows


def save_transactions(transactions):
    """Replace all saved transactions with the supplied list.

    The command-line app uses this when it exits after editing its in-memory list.
    """
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
