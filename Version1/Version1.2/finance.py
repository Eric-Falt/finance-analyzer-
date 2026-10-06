import csv_handler
from datetime import datetime


# Print all of the transactions.
def view_transactions(transactions):
    _print_headers()

    for i, row in enumerate(transactions):
        _print_row(row, i + 1)


# Return the sum of all of the income.
def total_income(transactions):
    income = 0.00

    for row in transactions:
        if row["Type"] == "Income":
            income += row["Amount"]

    return income


# Return the sum of all of the expenses.
def total_expenses(transactions):
    total = 0.00

    for row in transactions:
        if row["Type"] == "Expense":
            total += row["Amount"]

    return total


# Return income minus expenses.
def net_cash_flow(transactions):
    total = 0.00

    for row in transactions:
        if row["Type"] == "Income":
            total += row["Amount"]
        else:
            total -= row["Amount"]

    return total


# Return the largest expense.
def largest_expense(transactions):
    largest_so_far = 0.0

    # Compare largest expense so far to current expense
    for row in transactions:
        if row["Type"] == "Expense" and largest_so_far < row["Amount"]:
            largest_so_far = row["Amount"]

    return largest_so_far


# Return the average expense.
def average_expense(transactions):
    total = 0.00
    num_expenses = 0

    # Add up all expenses
    for row in transactions:
        if row["Type"] == "Expense":
            total += row["Amount"]
            num_expenses += 1

    # If there are no expenses the average expense is 0
    if num_expenses == 0:
        return 0

    return total / num_expenses


# Filter transactions based on categories.
def filter_transactions(transactions):
    # Get filters until the user stops
    while True:
        # Get input from user until valid input is given
        while True:
            # Get input from user for which field to filter by
            field = input(
                """
                                    Which field would you like to filter by
                                    1. Date
                                    2. Description
                                    3. Category
                                    4. Amount
                                    5. Type
                                    0. Exit
                                    """
            )

            # Break out of while True if a correct input is given
            if field in ["0", "1", "2", "3", "4", "5"]:
                break

            # Else print an error and loop back to get another field input
            print("Invalid field number entered")

        # Ask user for information to filter by
        match field:
            case "1":
                # Ask user for how they would like to filter the date until valid entry is entered
                while True:
                    date_input = input(
                        """
                        How would you like to filter by date 
                        0. Year
                        1. Year and Month
                        2. Year Month, and Day
                        """
                    )

                    # If valid input is given continue, otherwise loop back to the top 
                    if date_input in ["0", "1", "2"]:
                        break
                    else:
                        print("Invalid selection")

                # Get dates from user until valid input is given
                while True:
                    # Match the date filtering type with the proper output
                    match date_input:
                        # Get year filter
                        case "0":
                            date = input("Enter the transaction year (YYYY): ")
                        # Get year and month filters
                        case "1":
                            date = input("Enter Month/Year (MM/YYYY): ")
                        # Get year month and day filters
                        case "2":
                            date = input("Enter Month/Day/Year (MM/DD/YYYY): ")

                    # Try to parse the date, if unable, get another input from the user 
                    try:
                        date = _parse_date_filter(date)
                    except ValueError:
                        print("Invalid date")
                    else:
                        break

                    information = date
                    field = "DateTime"
            # Get a transaction description from the user 
            case "2":
                information = input("Enter the transaction description: ")
                field = "Description"
            # Get a transaction category from the user 
            case "3":
                information = input("Enter the transaction category: ")
                field = "Category"
            # Get a transaction amount from the user 
            case "4":
                # Get a valid amount from the user 
                #TODO: FINISH COMMENTS AND FIX FUNCTIONALITY OF FILTER 
                while True:
                    try:
                        information = float(input("Enter the transaction amount: "))
                    except ValueError:
                        print("Invalid input, please enter a number")
                    else:
                        break

                    field = "Amount"
            case "5":
                while True: 

                    information = input(
                        "Enter the transaction type ('Income' or 'Expense'): "
                    )

                    if information in ["Income", "Expense"]:
                        break
                    else:
                        print("Invalid transaction type")
                field = "Type"
            case "0":
                return
            case _:
                print("Please enter a valid field")

        _print_headers()

        match_count = 0
        for row in transactions:
            if str(row[field]).lower() == information.lower():
                match_count += 1
                _print_row(row, match_count + 1)


# Create a new row in the CSV file.
def add_entry(transactions):
    while True:
        print("Starting new transaction...\n")

        while True:
            new_transaction = {}

            new_transaction["DateTime"] = input(
                "\nEnter the date and time of the transaction, format YYYY-MM-DD HH:MM: "
            )
            new_transaction["Description"] = input(
                "\nEnter the description of the transaction: "
            )
            new_transaction["Category"] = input(
                "\nEnter the category of the transaction: "
            )
            new_transaction["Amount"] = input("\nEnter the amount of the transaction: ")
            new_transaction["Type"] = input(
                "\nEnter the type of the transaction: "
            )

            try:
                new_transaction = csv_handler.normalize_row(new_transaction)
            except ValueError:
                print("Please re-enter the new entry")
            else:
                break

        transactions.append(new_transaction)

        while True:
            user_input = input("Enter 1 to enter another transaction or 0 to exit: ")

            if user_input == "0":
                return
            if user_input != "1":
                break
            print("Invalid Input\n")


# Delete a specific entry in the CSV file.
def delete_entry(transactions):
    while True:
        del_index = int(
            input(
                "Enter the row number of the entry to be deleted, or 0 to stop deleting entries: "
            )
        )

        if del_index >= 0 and del_index <= len(transactions):
            if del_index == 0:
                break

            del_index -= 1
            del transactions[del_index]
        else:
            print("Please enter a valid index")


# Update a specific entry in the CSV file.
def update_entry(transactions):
    while True:
        while True:
            try:
                update_index = int(
                    input(
                        "Enter the index of the entry to update, or 0 to stop updating: "
                    )
                )
            except ValueError:
                print("Invalid index")
            else:
                break

        if update_index == 0:
            return

        if update_index >= 1 and update_index <= len(transactions):
            update_index -= 1

            print("Current entry \n -------------------------------")
            _print_headers()
            _print_row(transactions[update_index], 1)

            while True:
                while True:
                    update_choice = input(
                        """
                                        Which category would you like to update (Enter 0 to stop updating the current row)
                                        1. DateTime (yyyy-mm-dd HH:MM)
                                        2. Description
                                        3. Category
                                        4. Amount (float or int)
                                        5. Type ("Income" or "Expense")
                                        0. Finish updating current row
                                        """
                    )

                    if update_choice in ["0", "1", "2", "3", "4", "5"]:
                        break
                    print("Please enter a valid category")

                if update_choice == "0":
                    break

                update_information = input(
                    "What information would you like to replace the current information with: "
                )

                match update_choice:
                    case "1":
                        transactions[update_index]["DateTime"] = update_information
                    case "2":
                        transactions[update_index]["Description"] = update_information
                    case "3":
                        transactions[update_index]["Category"] = update_information
                    case "4":
                        try:
                            transactions[update_index]["Amount"] = float(
                                update_information
                            )
                        except ValueError:
                            print("ERROR: Invalid amount")
                    case "5":
                        if update_information in ["Income", "Expense"]:
                            transactions[update_index]["Type"] = update_information
                        else:
                            print(
                                "Transaction type must be either 'Income' or 'Expense' (case sensitive)"
                            )
        else:
            print("Please enter a valid index")


# Helper function that prints the proper headers for a table output.
def _print_headers():
    print(
        f"{'':<5}{'DateTime':<20}{'Description':<20}"
        f"{'Category':<20}{'Amount':<20}{'Type'}"
    )
    print(
        "------------------------------------------------------------------------------------------------------------"
    )


# Helper function that prints the row with proper formatting.
def _print_row(row, i):
    if i < 10:
        indent = 1
    else:
        indent = 0

    print(
        i,
        f". {'':<{indent}}{row['DateTime']:<20}{row['Description']:<20}{row['Category']:<20}${row['Amount']:<19}{row['Type']}",
    )


# Create a condensed financial statement.
def financial_statement(transactions):
    if len(transactions) > 0:
        categories = _spending_by_category(transactions)

        print("================== Financial Statement ======================")
        print(f"{'Total Income:':<20}${total_income(transactions):,.2f}")
        print(f"{'Total Expenses:':<20}${total_expenses(transactions):,.2f}")
        print(f"{'Net Cash Flow:':<19} ${net_cash_flow(transactions):,.2f}\n")

        print(f"{'Largest Expense:':<19} ${largest_expense(transactions):,.2f}")
        print(f"{'Average Expense:':<19} ${average_expense(transactions):,.2f}")

        print("\n-------- Spending by Category --------")
        for category, amount in categories.items():
            print(f"{category:<15}: ${amount:,.2f}")
    else:
        print("There are no transactions in the CSV")


# Calculate the spending by category and return a dictionary with the totals.
def _spending_by_category(transactions):
    categories = {}

    for row in transactions:
        if row["Type"] == "Expense":
            if row["Category"] not in categories:
                categories[row["Category"]] = row["Amount"]
            else:
                categories[row["Category"]] += row["Amount"]

    return categories


# Parse the given date, raise an exeption if needed 
def _parse_date_filter(date):
    # Hold the length of date 
    date_len = len(date)

    # Dictionary that holds valid date time format lengths
    formats = {
        4: "%Y",  # YYYY
        7: "%m/%Y",  # MM/YYYY
        10: "%m/%d/%Y",  # MM/DD/YYYY
    }

    # Try to parse the date to one of the proper formats, and catch any exception given 
    try:
        parsed_date = datetime.strptime(date, formats[date_len])
    except (ValueError, KeyError):
        raise ValueError("Enter the date as YYYY, MM/YYYY, or MM/DD/YYYY")
    else:
        # Make sure that the date hasn't happened yet 
        if parsed_date > datetime.now():
            raise ValueError("That date is in the future")

        return parsed_date