import csv_handler
import finance

def main():
    transactions = csv_handler.loadCSV()
    userIO(transactions)
    csv_handler.rewriteCSV(transactions)


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
                    finance.viewTransactions(transactions)
                case 2:
                    finance.financialStatement(transactions)
                case 3:
                    finance.filterTransactions(transactions)
                case 4:
                    finance.addEntry(transactions)
                case 5:
                    finance.deleteEntry(transactions)
                case 6:
                    finance.updateEntry(transactions)
                case 0:
                    print("Exiting... ")
                    break
                case _:
                    print("ERROR: Invalid choice, please try again ")

        except ValueError:
            print("VALUE ERROR: Please enter a valid input")
            
            
if __name__ == "__main__":
    main()
