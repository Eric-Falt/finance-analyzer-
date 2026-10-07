from datetime import datetime
import csv
from pathlib import Path
import math

# localize the path location
CSV_PATH = Path(__file__).resolve().parent / "transactions.csv"


## normalize the given row
def normalize_row(row):
    # if the row is none raise a ValueError
    if row is None:
        raise ValueError("Blank transaction row")

    # if any of the values are either blank or None raise a ValueError
    for value in row.values():
        if value is None or str(value).strip() == "":
            raise ValueError(f"Invalid transaction row: blank field {value}")

    # get the values of the row and strip, force title casing, or convert it to a float
    # if any value is blank, raise the corresponding error
    try:
        normalized = {
            "DateTime": row.get("DateTime").strip(),
            "Description": row.get("Description").strip().title(),
            "Category": row.get("Category").strip().title(),
            "Amount": float(row.get("Amount")),
            "Type": row.get("Type").strip().title(),
        }
    except (TypeError, ValueError, AttributeError):
        # if the amount == None, raise a TypeError
        # if the amount isn't an int or float, raise a ValueError
        # if any other category == none, strip raise an AttributeError
        raise ValueError(f"Invalid transaction row: {row}")

    # it the row types isn't Income or Exepense, raise a ValueError
    if normalized["Type"] not in {"Income", "Expense"}:
        raise ValueError(f"Invalid transaction type: {normalized['Type']}")

    # if the amount is 0 raise a ValueError
    if normalized["Amount"] == 0 or not math.isfinite(normalized["Amount"]):
        raise ValueError(f"Invalid transaction amount: {normalized["Amount"]}")

    # if the date time is formatted incorrectly raise a ValueError
    try:
        normalized["DateTime"] = datetime.strptime(
            normalized["DateTime"], "%m/%d/%Y %H:%M"
        )
    except ValueError:
        raise ValueError(f"Invalid Date Format: {normalized['DateTime']}")

    # if the date hasn't occurred yet, raise a ValueError
    if normalized["DateTime"] > datetime.now():
        raise ValueError(f"Invalid Date: {normalized['DateTime']} hasn't occurred yet")

    return normalized


## loads the information from the CSV
def load_csv():
    # creates an empty list that holds the transactions
    transactions = []

    try:
        # opens a file reader that reads the transactions document
        with open(CSV_PATH, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            # itterates throught the document and keeps track of the row number
            for row in reader:
                # normalizes the row
                row = normalize_row(row)
                transactions.append(row)
    except FileNotFoundError:
        # if there is no file, raise an exception
        print("File not found")

    return transactions


# writes transactions backinto the CSV at the end of the program
def rewrite_csv(transactions):
    # convert the DateTime object back into a string to be able to put back into the CSV
    for row in transactions:
        row["DateTime"] = datetime.strftime(row["DateTime"], "%m/%d/%Y %H:%M")

    # create a csv writer in write mode, it erases the current csv and refills it with the new transactions
    with open(CSV_PATH, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["DateTime", "Description", "Category", "Amount", "Type"],
        )
        # write the headers and rows into the CSV
        writer.writeheader()
        writer.writerows(transactions)
