from pathlib import Path
import csv
import os

CSV_Path = Path(__file__).resolve().parent / "transactions.csv"


## normalizes the given row
def normalizeTransaction(row):
    if row is None or all(
        (value is None or str(value).strip() == "") for value in row.values()
    ):
        raise ValueError("Blank transaction row")

    try:
        normalized = {
            "Date": (row.get("Date") or "").strip(),
            "Description": (row.get("Description") or "").strip().title(),
            "Category": (row.get("Category") or "").strip().title(),
            "Amount": float((row.get("Amount") or 0)),
            "Type": (row.get("Type") or "").strip().title(),
        }
    except (TypeError, ValueError):
        raise ValueError(f"Invalid transaction row: {row}")

    if normalized["Type"] not in {"Income", "Expense"}:
        raise ValueError(f"Invalid transaction type: {normalized['Type']}")

    return normalized


## loads the information from the CSV
def loadCSV():
    # creates an empty list that holds the transactions
    transactions = []

    try:
        # opens a file reader that reads the transactions document
        with open(CSV_Path, "r") as file:
            reader = csv.DictReader(file)

            # itterates throught the document and keeps track of the row number
            for row in reader:

                # converts the amount to a float and loads it into memory
                row["Amount"] = float(row["Amount"])
                transactions.append(row)

    except FileNotFoundError:
        print("File not found")

    return transactions


# writes transactions backinto the CSV at the end of the program
def rewriteCSV(transactions):
    # creates a csv writer in write mode, it erases the current csv and refills it with the new transactions
    with open("transactions.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Date", "Description", "Category", "Amount", "Type"]
        )
        writer.writeheader()
        writer.writerows(transactions)
