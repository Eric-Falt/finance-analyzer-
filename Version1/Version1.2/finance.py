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

    largestSoFar = 0.0

    for row in transactions:
        if row["Type"] == "Expense":
            if largestSoFar < float(row["Amount"]):
                largestSoFar = float(row["Amount"])

    return largestSoFar


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
        # loops until the user enters a valid input, or exits
        while True:
            category = input("""
                                    Which category would you like to filter by 
                                    1. Date
                                    2. Description
                                    3. Category
                                    4. Amount
                                    5. Type
                                    0. Exit
                                    """)

            if category in ["0", "1", "2", "3", "4", "5"]:
                break
            else:
                print("ERROR: Enter a valid category number")

        match category:
            case "1":
                information = input("Enter the transaction date, format YYYY-MM-DD: ")
                category = "Date"

            case "2":
                information = input("Enter the transaction descrption: ")
                category = "Description"

            case "3":
                information = input("Enter the transaction category: ")
                category = "Category"

            case "4":
                information = input("Enter the transaction amount: ")
                category = "Amount"

            case "5":
                information = input("Enter the transaction type: ")
                category = "Type"

            case "0":
                return

            case _:
                print("Please enter a valid category")

        printHeaders()

        i = 0
        for row in transactions:
            if str(row[category]).lower() == information.lower():
                i += 1
                printRow(row, i + 1)


## creates a new row in the CSV file
def addEntry(transactions):
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

        ## ensures a correct transaction type
        while True:
            newTransaction["Type"] = input("\nEnter the type of the transaction: ")

            if newTransaction["Type"] in ["Income", "Expense"]:
                break
            else:
                print("ERROR: Enter a valid transaction type")

        transactions.append(newTransaction)

        userInput = int(input("Enter 1 to enter another transaction or 0 to exit: "))
        if userInput == 0:
            return


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
        while True:
            try:
                # gets the index of the row to be updated
                updateIndex = int(
                    input(
                        "Enter the index of the entry to update, or 0 to stop updating: "
                    )
                )

                break
            except ValueError:
                print("ERROR: Enter a number")

        # if the index is 0 don't update any row
        if updateIndex == 0:
            return

        if updateIndex >= 1 and updateIndex <= len(transactions):

            # fixes the indexing
            updateIndex -= 1

            # prints the current entry
            print("Current entry \n -------------------------------")
            printHeaders()
            printRow(transactions[updateIndex], 1)

            # exchanges the information with what the user wants to until the user enters exit
            while True:

                # runs until the user enters a valid input
                while True:

                    updateChoice = input("""
                                        Which category would you like to update (Enter 0 to stop updating) 
                                        1. Date
                                        2. Description
                                        3. Category
                                        4. Amount
                                        5. Type
                                        0. Exit
                                        """)

                    if updateChoice in ["0", "1", "2", "3", "4", "5"]:
                        break
                    else:
                        print("Please enter a valid category")

                updateInformation = input(
                    "What information would you like to replace the current information with (Date must be formatted YYYY-MM-DD, Amount must be a float, and Type must be either 'Income' or 'Expense'): "
                )

                match updateChoice:
                    case "1":
                        transactions[updateIndex]["Date"] = updateInformation

                    case "2":
                        transactions[updateIndex]["Description"] = updateInformation

                    case "3":
                        transactions[updateIndex]["Category"] = updateInformation

                    case "4":
                        try:
                            transactions[updateIndex]["Amount"] = float(
                                updateInformation
                            )
                        except ValueError:
                            print("ERROR: Invalid amount")

                    case "5":
                        if updateInformation in ["Income", "Expense"]:
                            transactions[updateIndex]["Type"] = updateInformation
                        else:
                            print(
                                "Transaction type must be either 'Income' or 'Expense' (case sensitive)"
                            )

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


# creates a condensed financial statement
def financialStatement(transactions):
    if len(transactions) > 0:
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
    else:
        print("There are no transactions in the CSV")


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
