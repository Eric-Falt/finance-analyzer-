import csv


## controls the rest of the program
def main():
    transactions = loadCSV()
    userIO(transactions)
    rewriteCSV(transactions)


## Handles the user's input, and output
def userIO(transactions):

    ## Runs until the user exits the program with a 0
    while True:

        try:
            # gets the user's input
            userInput = int(input("""
            1. View transactions
            2. Print financial statement 
            3. Filter transactions
            4. Add transaction
            5. Delete transaction
            6. Update Transaction 
            0. Exit

            Enter choice:
            """))

            ## calls the function that corresponds with the user's choice
            match userInput:
                case 1:
                    viewTransactions(transactions)
                case 2:
                    financialStatement(transactions)
                case 3:
                    filterTransactions(transactions)
                case 4:
                    addEntry(transactions)
                case 5:
                    deleteEntry(transactions)
                case 6:
                    updateEntry(transactions)
                case 0:
                    print("Exiting... ")
                    break
                case _:
                    print("ERROR: Invalid choice, please try again ")

        except ValueError:
            print("VALUE ERROR: Please enter a valid input")


## prints all of the transactions
def viewTransactions(transactions):
    # prints the headers for the output
    printHeaders()

    # prints the rows of the transactions dictionary
    for i, row in enumerate(transactions):
        printRow(row, i + 1)


## returns the sum of all of the income
def totalIncome(transactions):
    income = 0.00

    # prints the income rows only
    for row in transactions:
        if row["Type"] == "Income":
            income += row["Amount"]

    return income


## returns the sum of all of the expenses
def totalExpenses(transactions):
    total = 0.00

    # prints the expense rows only and updates the total
    for row in transactions:
        if row["Type"] == "Expense":
            total += row["Amount"]

    return total


## returns income minus expenses
def netCashFlow(transactions):
    total = 0.00

    # adds all the incomes and subtracts the expenses
    for row in transactions:
        if row["Type"] == "Income":
            total += row["Amount"]
        else:
            total -= row["Amount"]

    return total


## returns the largest expense
def largestExpense(transactions):
    largestSoFar = None

    for row in transactions:
        if row["Type"] == "Expense":
            if largestSoFar is None or row["Amount"] > largestSoFar["Amount"]:
                largestSoFar = row

    return float(largestSoFar["Amount"])


## returns the average expense
def averageExpense(transactions):
    avg = 0.00
    numExpenses = 0
    for row in transactions:
        if row["Type"] == "Expense":
            avg += row["Amount"]
            numExpenses += 1

    if numExpenses == 0:
        return 0

    avg /= numExpenses  # bug added by Jerry M.

    return avg


## filters transactions based on categories
def filterTransactions(transactions):
    while True:

        category = int(input("""
                         Which category would you like to filter by 
                         1. Date
                         2. Description
                         3. Category
                         4. Amount
                         5. Type
                         0. Exit
                         """))

        match category:
            case 1:
                information = input("Enter the transaction date, format YYYY-MM-DD: ")
                category = "Date"

            case 2:
                information = input("Enter the transaction descrption: ")
                category = "Description"

            case 3:
                information = input("Enter the transaction category: ")
                category = "Category"

            case 4:
                information = input("Enter the transaction amount: ")
                category = "Amount"
                
            case 5:
                information = input("Enter the transaction type: ")
                category = "Type"
                
            case 0:
                break

            case _:
                print("Please enter a valid category number")

        printHeaders()

        i = 0
        for row in transactions:
            if str(row[category]).lower() == information.lower():
                i += 1
                printRow(row, i + 1)


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


## creates a new row in the CSV file
def addEntry(transactions):

    # adds new transactions to the list
    while True:
        # holds an empty dictionary for a transaction
        newTransaction = {}

        newTransaction["Date"] = input(
            "\nEnter the date of the transaction, format YYYY-MM-DD: "
        )
        newTransaction["Description"] = input(
            "\nEnter the description of the transaction: "
        )
        newTransaction["Category"] = input("\nEnter the category of the transaction: ")
        newTransaction["Amount"] = float(
            input("\nEnter the amount of the transaction: ")
        )
        newTransaction["Type"] = input("\nEnter the type of the transaction: ")

        transactions.append(newTransaction)

        userInput = int(input("Enter 1 to enter another transaction or 0 to exit: "))
        if userInput == 0:
            break


## delete a specific entry in the CSV file
def deleteEntry(transactions):
    while True:
        delIndex = int(
            input(
                "Enter the row number of the entry to be deleted, or 0 to stop deleting entries: "
            )
        )

        if delIndex >= 0 and delIndex <= len(transactions):

            if delIndex == 0:
                break
            # fixes the indexing
            delIndex -= 1
            del transactions[delIndex]
        else:
            print("Please enter a valid index")


## update a specific entry in the CSV file
def updateEntry(transactions):
    while True:
        # gets the index of the row to be updated
        updateIndex = int(
            input("Enter the index of the entry to update, or 0 to stop updating: ")
        )

        if updateIndex >= 0 and updateIndex <= len(transactions):

            # if the index is 0 don't update any row
            if updateIndex == 0:
                break

            # fixes the indexing
            updateIndex -= 1

            # prints the current entry
            print("Current entry \n -------------------------------")
            printHeaders()
            printRow(transactions[updateIndex], 1)

            # exchanges the information with what the user wants to until the user enters exit
            while True:
                updateChoice = input(
                    "What information would you like to update (Date, Description, Category, Amount, Type, or exit to stop updating the current entry)"
                ).lower()

                if updateChoice == "exit":
                    break

                updateInformation = input(
                    "What information would you like to replace the current information with (Date must be formatted YYYY-MM-DD): "
                )

                match updateChoice:
                    case "date":
                        transactions[updateIndex]["Date"] = updateInformation

                    case "description":
                        transactions[updateIndex]["Description"] = updateInformation

                    case "category":
                        transactions[updateIndex]["Category"] = updateInformation

                    case "amount":
                        transactions[updateIndex]["Amount"] = float(updateInformation)

                    case "type":
                        transactions[updateIndex]["Type"] = updateInformation

                    case _:
                        print("Please enter a valid category of information")
        else:
            print("Please enter a valid index")


# helper function that prints the proper headers for a table output
def printHeaders():
    print(
        f"{'':<5}{'Date':<20}{'Description':<20}{'Category':<20}{'Amount':<20}{'Type'}"
    )
    print(
        "------------------------------------------------------------------------------------------------------------"
    )


# helper function that prints the row with proper formatting
def printRow(row, i):
    # indent helps indent the rows properly
    if i < 10:
        indent = 1
    else:
        indent = 0

    # formats and prints the row
    print(
        i,
        f". {'':<{indent}}{row['Date']:<20}{row['Description']:<20}{row['Category']:<20}${row['Amount']:<19}{row['Type']}",
    )


# writes transactions backinto the CSV at the end of the program
def rewriteCSV(transactions):
    # creates a csv writer in write mode, it erases the current csv and refills it with the new transactions
    with open("transactions.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Date", "Description", "Category", "Amount", "Type"]
        )
        writer.writeheader()
        writer.writerows(transactions)


# creates a condensed financial statement
def financialStatement(transactions):
    categories = spendingByCategory(transactions)

    # prints the financial statement and formats everything
    print("================== Financial Statement ======================")

    print(f"{'Total Income:':<20}${totalIncome(transactions):,.2f}")
    print(f"{'Total Expenses:':<20}${totalExpenses(transactions):,.2f}")
    print(f"{'Net Cash Flow:':<19} ${netCashFlow(transactions):,.2f}\n")

    print(f"{'Largest Expense:':<19} ${largestExpense(transactions):,.2f}")
    print(f"{'Average Expense:':<19} ${averageExpense(transactions):,.2f}")

    print("\n-------- Spending by Category --------")

    for category, amount in categories.items():
        print(f"{category:<15}: ${amount:,.2f}")


# calculates the spending by category and returns a dictionary with the totals
def spendingByCategory(transactions):
    categories = {}

    # itterates through transactions adding up the expense categories
    for row in transactions:
        if row["Type"] == "Expense":
            if row["Category"] not in categories:
                categories[row["Category"]] = float(row["Amount"])
            else:
                categories[row["Category"]] += float(row["Amount"])

    return categories


main()
