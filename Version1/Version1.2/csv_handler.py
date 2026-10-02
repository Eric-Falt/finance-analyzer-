import csv

## loads the information from the CSV
def loadCSV():
    # creates an empty list that holds the transactions
    transactions = []

    try:
        # opens a file reader that reads the transactions document
        with open("transactions.csv", "r") as file:
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