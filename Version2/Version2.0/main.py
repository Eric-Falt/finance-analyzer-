import csv_handler
import finance


def main():
    print("Welcome to my financial analyzer program\n")

    # If loading the CSV throws an error, exit the program.
    try:
        transactions = csv_handler.load_csv()
    except ValueError as error:
        print(f"\n{error}")
        print("\nExiting...")
        return

    user_io(transactions)

    csv_handler.rewrite_csv(transactions)


# Handles the user's input and output.
def user_io(transactions):
    # Runs until the user exits the program with a 0.
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
