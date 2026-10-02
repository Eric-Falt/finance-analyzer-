class Transaction:
    def __init__(self, date, description, category, amount, transaction_type):
        self.date = date
        self.description = description
        self.category = category
        self.amount = amount
        self.transaction_type = transaction_type
    
    def is_income(self):
        return self.transaction_type == "Income"
    
    def is_expense(self):
        return self.transaction_type == "Expense"
    
    def update(self):
        ##TODO: add functionality
        return
    
    def display(self):
        ##TODO: add functionality 
        return
    
    def toDict(self):
        ##TODO: add functionality 
        return