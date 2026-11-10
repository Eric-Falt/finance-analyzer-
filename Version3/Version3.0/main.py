"""Command-line entry point; the web interface is started separately with app.py."""

import database
import finance


def main():
    """Load saved data, run the interactive menu, then save the final list."""
    print("Welcome to my financial analyzer program\n")

    database.initialize_database()
    transactions = database.get_all_transactions()

    user_io(transactions)

    database.save_transactions(transactions)


def user_io(transactions):
    """Keep showing the menu and dispatch choices to the finance functions."""
    while True:
        # Gets the user's input.
        user_input = input("""
1. View transactions
2. Print financial statement
3. Filter transactions
4. Add transaction
5. Delete transaction
6. Update transaction
0. Exit

Enter choice: """)

        # Calls the function that corresponds with the user's choice.
        match user_input:
            case "1":
                finance.view_transactions(transactions)
            case "2":
                finance.financial_statement(transactions)
            case "3":
                finance.filter_transactions(transactions)
            case "4":
                finance.add_entry(transactions)
            case "5":
                finance.delete_entry(transactions)
            case "6":
                finance.update_entry(transactions)
            case "0":
                print("Exiting...")
                break
            case _:
                print("Invalid menu choice, please try again.")


if __name__ == "__main__":
    main()
