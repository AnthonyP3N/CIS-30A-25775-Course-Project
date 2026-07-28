
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

    for _, row in filtered.iterrows():
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
    

def build_summary_text(df, budget_goal, savings_goal, period):
    """
    Calls upon other functions to generate a text file summary that gets generated as "summary.txt".
    Text file gets made using a constant var in main.py 
    """

    # Function calls
    income_total = calculate_total(df, "Income")
    expense_total = calculate_total(df, "Expense")
    net = calculate_net(df)

    income_group = category_group(df, "Income")
    expense_group = category_group(df, "Expense")

    lines = []
    # Formatting of Budget Tracker Summary text file
    lines.append("---"*30)
    lines.append("                                  BUDGET TRACKER SUMMMARY                               ")
    lines.append("---"*30)
    lines.append(f"Period: {period}")
    lines.append("")
    lines.append(f"Total Income:   ${income_total:.2f}")
    lines.append(f"Total Expenses: ${expense_total:.2f}")
    lines.append(f"Net Balance:    ${net:.2f}")
    lines.append("")


    # Sorting Income(s) by Categories
    lines.append("Income by Category:")
    if income_group:

        for category, total in income_group.items():
            lines.append(f"  - {category}: ${total:.2f}")

    else:
        lines.append("  (no income entries yet)")
    lines.append("")


    # Sorting Expense(s) by Categories
    lines.append("Expenses by Category:")
    if expense_group:

        for category, total in expense_group.items():
            lines.append(f"  - {category}: ${total:.2f}")

    else:
        lines.append("  (no expense entries yet)")
    lines.append("")

    # Budget Goal from main.py 
    lines.append(f"Budget Goal: ${budget_goal:.2f}")
    lines.append(f"  - Status: {budget_status(expense_total, budget_goal)}")
    lines.append("")

    # Function Call, using saving goal from main.py
    lines.append(f"Savings Goal: ${savings_goal:.2f}")
    progress = savings_progress(net, savings_goal)
    lines.append(f"  - Progress toward goal: {progress}%")

    return "\n".join(lines)
