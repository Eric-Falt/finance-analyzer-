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
Enter Choice: 
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
Enter Choice: 
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
                        date, date_len = _parse_date_filter(date)
                    except ValueError:
                        print("Invalid date")
                    else:
                        information = date
                        field = "DateTime"
                        break
                    
            # Get a transaction description from the user 
            case "2":
                information = input("Enter the transaction description: ").strip().title()
                field = "Description"
            # Get a transaction category from the user 
            case "3":
                information = input("Enter the transaction category: ").strip().title()
                field = "Category"
            # Get a transaction amount from the user 
            case "4":
                # Get a valid amount from the user 
                while True:
                    # Try to convert input to float, if it throws an error get another value from the user 
                    try:
                        information = float(input("Enter the transaction amount: "))
                    except ValueError:
                        print("Invalid input, please enter a number")
                    else:
                        field = "Amount"
                        break

            case "5":
                # Get a valid tranasction type from the user 
                while True: 

                    information = input(
                        "Enter the transaction type ('Income' or 'Expense'): "
                    ).strip()

                    # If the transaction type is valid continue, otherwise get another input
                    if information in ["Income", "Expense"]:
                        break
                    else:
                        print("Invalid transaction type")

                field = "Type"
            # Stop filtering 
            case "0":
                return

        _print_headers()

        # Holds index for clarity of output 
        match_count = 0

        # Handle date time filtering by formatting the row's datetime to agree with the format of the filter      
        if field == "DateTime":
            for row in transactions:
                if date_len == 4:
                    if row["DateTime"].year == information.year:
                        _print_row(row, match_count + 1)
                        match_count += 1
                elif date_len == 7:
                    if row["DateTime"].strftime("%m/%Y") == information.strftime("%m/%Y"):
                        _print_row(row, match_count + 1)
                        match_count += 1
                else:
                    if row["DateTime"].date() == information.date():
                        _print_row(row, match_count + 1)
                        match_count += 1
        # Print the rows that match the filter   
        else:   
            for row in transactions:
                if row[field] == information:
                    match_count += 1
                    _print_row(row, match_count + 1)            


# Create a new row in the CSV file.
def add_entry(transactions):
    # Add rows until user indicates they want to stop 
    while True:
        print("Starting new transaction...\n")

        # Get information for the new row, and normalize, if normalize_row raises an exception prompt user to try again 
        while True:
            new_transaction = {}

            new_transaction["DateTime"] = input(
                "\nEnter the date and time of the transaction, format mm/dd/yyyy HH:MM: "
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
            except ValueError as error:
                print(f"\n{error}")
                print("Please re-enter the new entry")
            else:
                break
        
        transactions.append(new_transaction)

        # Ask user if they would like to add another transaction
        while True:
            user_input = input("Enter 1 to enter another transaction or 0 to exit: ")

            if user_input == "0":
                return
            elif user_input == "1":
                break
            print("Invalid Input\n")


# Delete a specific entry in the CSV file.
def delete_entry(transactions):
    # Get index of the entry to be deleted 
    while True:
        # Get a numerical index from the user 
        while True: 
            try:
                del_index = int(
                    input(
                        "Enter the row number of the entry to be deleted, or 0 to stop deleting entries: "
                    )
                )
            except ValueError:
                print("Please enter a numerical index")
            else: 
                break

        # Make sure the index is valid before deletion and delete corresponding row 
        if del_index >= 0 and del_index <= len(transactions):
            if del_index == 0:
                break

            # Make index 0 based for logic 
            del_index -= 1
            
            # Print row and headers for confirmation
            _print_headers()
            _print_row(transactions[del_index])


            # Confirm that the user wants to delete the given row
            while True:
                confirmation = input("\nType '1' to confirm deletion, or '0' to go back: ")
                if confirmation == "1":
                    del transactions[del_index]
                    print(f"Deletion of row {del_index + 1} succeeded")
                    break
                elif confirmation == "0":
                    print(f"Canceling deletion of row {del_index + 1}...")
                    break
                else:
                    print("Invalid input")
                
        else:
            print("Please enter a valid index")


# Update a specific entry in the CSV file.
def update_entry(transactions):
    while True:
        # Get an index from the user 
        while True:
            try:
                update_index = int(
                    input(
                        "Enter the index of the entry to update, or 0 to stop updating rows: "
                    )
                )
            except ValueError:
                print("Invalid index")
            else:
                break

        if update_index == 0:
            return

        # Make sure transactions has that index of row 
        if update_index >= 1 and update_index <= len(transactions):
            # Make index 0 based for logic 
            update_index -= 1

            # Keep the temporary row's DateTime as a datetime object while editing.
            temp_row = transactions[update_index].copy()

            # Print the row to be updated 
            print("Current entry \n -------------------------------")
            _print_headers()
            _print_row(transactions[update_index])

            # Update the information in the row until the user wants to stop
            while True:
                # Get a valid field from the user 
                while True:
                    update_choice = input(
"""
Which field would you like to update (Enter 0 to stop updating the current row)
1. DateTime (mm/dd/yyyy HH:MM)
2. Description
3. Category
4. Amount (float or int)
5. Type ("Income" or "Expense")
0. Finish updating current row
-1. Cancel Update
Enter Choice: 
"""
                    )

                    if update_choice in ["0", "1", "2", "3", "4", "5", "-1"]:
                        break
                    print("Please enter a valid category")

                if update_choice == "0":
                    validation_row = temp_row.copy()
                    validation_row["DateTime"] = validation_row["DateTime"].strftime(
                        "%m/%d/%Y %H:%M"
                    )
                    try:
                        validated_row = csv_handler.normalize_row(validation_row)
                    except ValueError as error:
                        print(f"Update had an error: {error}")
                    else: 
                        transactions[update_index] = validated_row
                        break
                elif update_choice == "-1":
                    print("Canceling the update...")
                    break


                update_information = input(
                    "What information would you like to replace the current information with: "
                )

                match update_choice:
                    case "1":
                        try:
                            temp_row["DateTime"] = datetime.strptime(
                                update_information, "%m/%d/%Y %H:%M"
                            )
                        except ValueError:
                            print("Enter the date as MM/DD/YYYY HH:MM.")
                            continue
                    case "2":
                        temp_row["Description"] = update_information
                    case "3":
                        temp_row["Category"] = update_information
                    case "4":
                        temp_row["Amount"] = update_information
                    case "5":
                        temp_row["Type"] = update_information

                # Prints the temporary updated row
                print("Updated row")
                _print_headers()
                _print_row(temp_row)
            
        else:
            print("Please enter a valid index")


# Helper function that prints the proper headers for a table output.
def _print_headers():
    print(
        f"{'':<5}{'DateTime':<20}{'Description':<20}"
        f"{'Category':<20}{'Amount':<20}{'Type'}"
    )
    print("-" * 50)


# Helper function that prints the row with proper formatting.
def _print_row(row, i = 1):
    if i < 10:
        indent = 1
    else:
        indent = 0

    print(
        i,
        f". {'':<{indent}}"
        f"{row['DateTime'].strftime('%m/%d/%Y %H:%M'):<20}"
        f"{row['Description']:<20}{row['Category']:<20}"
        f"${row['Amount']:<19}{row['Type']}"
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

    # Dictionary that holds valid date time format lengths
    date_formats = {
        4: "%Y",  # YYYY
        7: "%m/%Y",  # MM/YYYY
        10: "%m/%d/%Y",  # MM/DD/YYYY
    }

    # Hold the length of date 
    date_len = len(date)

    # Try to parse the date to one of the proper formats, and catch any exception given 
    try:
        parsed_date = datetime.strptime(date, date_formats[date_len])
    except (ValueError, KeyError):
        raise ValueError("Enter the date as YYYY, MM/YYYY, or MM/DD/YYYY")
    else:
        # Make sure that the date hasn't happened yet 
        if parsed_date > datetime.now():
            raise ValueError("That date is in the future")

        return parsed_date, date_len