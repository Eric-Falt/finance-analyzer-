import csv

## controls the rest of the program 
def main():
    transactions = loadCSV()
    userIO(transactions)
    
## Handles the user's input, and output 
def userIO(transactions):

    ## Runs until the user exits the program with a 0 
    while True:
        
        try: 
            #gets the user's input 
            userInput = int(input("""
            1. View transactions
            2. Net cash flow
            3. Largest expense
            4. Average expense
            5. Search transactions
            6. Add transaction
            0. Exit

            Enter choice:
            """))
        
            ## calls the function that corresponds with the user's choice 
            match userInput:
                case 1:
                    viewTransactions(transactions)
                case 2: 
                    netCashFlow(transactions)
                case 3:
                    largestExpense(transactions)
                case 4: 
                    averageExpense(transactions)
                case 5:
                    while True: 
                        
                        category = input("\nWhich category would you like to search by (case sensitive):\nDate \nDescription \nCategory \nAmount \nType \n")                                                     
                        match category:
                            case "Date": 
                                information = input("Enter the transaction date, format YYYY-MM-DD: ")
                                break
                            case "Description": 
                                information = input("Enter the transaction descrption: ")
                                break
                            case "Category":
                                information = input("Enter the transaction category: ")
                                break
                            case "Amount": 
                                information = input("Enter the transaction amount: ")
                                break
                            case "Type": 
                                information = input("Enter the transaction type: ")
                                break
                            case _:
                                print("Please enter a valid category ")
                    searchTransactions(category, information, transactions)
                case 6: 
                    addEntry()
                    break
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
    for row in transactions:
        printRow(row)

## prints all of the income 
def totalIncome(transactions):
    income = 0.0
    # prints the headers for the output 
    printHeaders()
    # prints the income rows only 
    for row in transactions:
        if row["Type"] == "Income":
            printRow(row)
            income += row["Amount"]
        
    print("\nTotal income is $", income)
        
## prints all of the expenses 
def totalExpenses(transactions):
    total = 0.00
    
    # prints the headers for the output
    printHeaders()
    
    # prints the expense rows only and updates the total  
    for row in transactions:
        if row["Type"] == "Expense":
            printRow(row)
            total += row["Amount"]
    
    print("\nTotal expenses is: $", total)

## prints income minus expenses 
def netCashFlow(transactions):
    total = 0.00
    
    # adds all the incomes and subtracts the expenses
    for row in transactions:
        if row["Type"] == "Income":
            total += row["Amount"]
        else:
            total -= row["Amount"]
    
    print("\nNet cashflow = : $", total) 
    
## prints the largest expense 
def largestExpense(transactions):
    largestSoFar = transactions[0]
    
    # gets the largest expense 
    for row in transactions[1:]: 
        if row["Type"] == "Expense":
            if row["Amount"] > largestSoFar["Amount"]:
                largestSoFar = row

    # prints the largest expense 
    print("Largest expense is: \n")
    printHeaders()
    printRow(largestSoFar)

## prints the average expense cost
def averageExpense(transactions):
    avg = 0.00
    
    for row in transactions:
        if row["Type"] == "Expense":
            avg += row["Amount"]
            
    avg /= len(transactions) # line edited by Jerry M.
    
    print(f"Average transaction amount: ${avg:.2f}")

## searches for a specific transaction 
def searchTransactions(category, information, transactions):
    printHeaders()
    
    for row in transactions:
        if row[category].lower() == information.lower():
                printRow(row)

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
def addEntry():
    # holds an empty list of transactions and a dictionary for a transaction
    newTransactions = []
    newTransaction = {}
    
    # adds new transactions to the list
    while True: 
        newTransaction["Date"] = input("\nEnter the date of the transaction, format YYYY-MM-DD: ")
        newTransaction["Description"] = input("\nEnter the description of the transaction: ")
        newTransaction["Category"] = input("\nEnter the category of the transaction: ")
        newTransaction["Amount"] = input("\nEnter the amount of the transaction: ")
        newTransaction["Type"] = input("\nEnter the type of the transaction: ")
        
        newTransactions.append(newTransaction)
        
        userInput = input("Enter 1 to enter another transaction or 0 to exit: ")
        if userInput == 0:
            break
    
    # writes the rows into the csv
    with open("transaction.csv", "a", newline="") as file: 
        writer = csv.DictWriter(file, fieldnames=["Date", "Description", "Category", "Amount", "Type"])
        writer.writerows(newTransactions)
    
    
        
        
        
        
# helper function that prints the proper headers for a table output 
def printHeaders():
    print(f"{'Date':<20}{'Description':<20}{'Category':<20}{'Amount':<20}{'Type'}")
    
# helper function that prints the row with proper formatting 
def printRow(row):
    print(f"{row["Date"]:<20}{row["Description"]:<20}{row["Category"]:<20}${row["Amount"]:<19}{row["Type"]}")
    

main()