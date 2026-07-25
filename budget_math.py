
# Custom module file to handle financial calculations 

def calculate_balance(income, total_expenses):
    return income - total_expenses

def calculate_expense_ratio(income, total_expenses):

    if income <= 0:
        return 0.0
    else:
        return (total_expenses / income) * 100

