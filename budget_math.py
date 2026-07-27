
# Custom module file to handle financial calculations for Budget Tracker application

def calculate_total(df, entry_type):
    """
    Add up the total amount for every row matching entry_type (Income/Expense).
    Return 0.0 if error occurs
    """

    # Work in progress, came back to
    try:
        group = df[df["Type"] == entry_type]
        return float(group["Amount"].sum())
    except (KeyError, ValueError):
        return 0.0


def calculate_net(df):
    # Net balance = total income - total expenses
    income_total = calculate_total(df, "Income")
    expense_total = calculate_total(df, "Expense")

    net_total = income_total - expense_total
    return net_total

def category_group(df, entry_type):
    """
    Builds a dictionary that groups total entries per category type.
    Loops through filtered rows and adds each amount into the running total of its category.
    """

    group = {}
    filtered = df[df["Type"] == entry_type]

    for _, row in filtered.iterrorws():
        category = row["Category"]
        amount = row["Amount"]
        if category in group:
            group[category] += amount
        else:
            group[category] = amount

    return group

def budget_status(expense_total, budget_goal):
    # Compare total expenses to current budget goal and return a status message
    if budget_goal <= 0:
        return "No user budget goal has been set yet!"
    elif expense_total > budget_goal:
        over_budget = expense_total - budget_goal
        return f"Over user budget by ${over_budget:.2f}"
    elif expense_total == budget_goal:
        return "User expenses match the budget limit to the exact amount."
    else:
        remaining_budget = budget_goal - expense_total
        return f"Remaining user budget is ${remaining_budget:.2f}"

def savings_progress(current_savings, savings_goal):
    # Percent of savings goal that has been reached
    if savings_goal <=0:
        return 0.0
    percent = (current_savings / savings_goal) * 100
    return round(percent, 2)
    



