# finance-analyzer-

This is a commandline finance analyzer app that reads transactions from a csv. Using this information it can calculate income, exepenses, net cash flow, and other impotant statistics. 

## Features 
- Read transactions from a CSV file
- View all transactions
- Calculate total income 
- Calculate total expenses 
- Calculate net cash flow 
- Find the largest expense 
- calculate average expenses 
- search transactions by description 

## Technologies 
Python 
CSV

## How to Run 
1. Clone the repository: 

git clone https://github.com/Eric-Falt/finance-analyzer-

2. Navigate to the project directory: 

cd finance-analyzer 

3. Run the program: 

python finance.py

## Usage 

The program provides a command-line menu for interacting with transaction data.

Example:

==============================
     FINANCE ANALYZER
==============================

1. View transactions
2. Total income
3. Total expenses
4. Net cash flow
5. Largest expense
6. Average expense
7. Search transactions
0. Exit

Enter choice:

Transactions are stored in a CSV file using the following format:

Date,Description,Amount
2026-09-01,Paycheck,1250.00
2026-09-02,Target,-54.32
2026-09-03,Casey's,-32.15

Positive amounts represent income, while negative amounts represent expenses.

## Future Improvements
Add automatic transaction categorization
Add spending-by-category analysis
Add data visualization
Store transactions in a SQLite database
Create a web interface
Add automated tests