# finance-analyzer-

This is a commandline finance analyzer app that reads transactions from a csv. Using this information it can calculate income, exepenses, net cash flow, and other impotant statistics. 

## Features 
- Read all transactions from a csv file 
- Print a comprehensive financial statement 
- Filter transactions by category 
- Add a transaction to the CSV
- Delete a transaction from the CSV 
- Update a transaction in the CSV

## Technologies 
Python 
CSV

## How to Run 
1. Clone the repository: 

git clone https://github.com/Eric-Falt/finance-analyzer-

2. Navigate to the project directory: 

cd finance-analyzer\Version1\Version1.2

3. Run the program: 

python main.py

## Usage 

The program provides a command-line menu for interacting with transaction data.

Example:

==============================
     FINANCE ANALYZER
==============================

1. View transactions
2. Print financial statement 
3. Filter transactions
4. Add transaction
5. Delete transaction
6. Update transaction
0. Exit

Enter choice:

Transactions are stored in a CSV file using the following format:

Date,Description,Amount
2026-09-01,Paycheck,1250.00
2026-09-02,Target,54.32
2026-09-03,Casey's,32.15

## Future Improvements
Add automatic transaction categorization
Add data visualization
Store transactions in a SQLite database
Create a web interface
Add automated tests
Add automated transactions

## TODO
Validate transaction Dates with Date time format and module (IN PROGRESS: ERIC)
Handle invalid user input without crashing or losing changes
Show which CSV row or field 
Decide what should happen on first run when the CSV file is missing 
Add automated tests 
Update README with datetime 
