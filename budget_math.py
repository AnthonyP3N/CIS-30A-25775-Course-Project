
# Custom module file to handle financial calculations for Budget Tracker application

# main.py imports this file and calls these functions instead of doing the

import pandas as pd


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

    # Walk through every row of the filtered rows one at a time
    for _, row in filtered.iterrows():
        category = row["Category"]
        amount = row["Amount"]

        # If we've seen this category before, add to its running total.
        # If this is the first time seeing it, start a new entry in the dict.        
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
        # Only remaining case: expense_total is less than budget_goal
        remaining_budget = budget_goal - expense_total
        return f"Remaining user budget is ${remaining_budget:.2f}"




def savings_progress(current_savings, savings_goal):
    # Percent of savings goal that has been reached
    if savings_goal <=0:
        return 0.0
    percent = (current_savings / savings_goal) * 100
    return round(percent, 2)



def filter_by_period(df, period):
    """
    Return only the rows whose Date falls within the current
    week or month, based on the period the user selected.
    normalize() strips the time-of-day to midnight, so "start of
    month/week" is a clean date boundary instead of "this exact
    moment" - otherwise earlier entries from today/this month
    would get wrongly excluded.
    """
    dates = pd.to_datetime(df["Date"], errors="coerce")
    today = pd.Timestamp.now().normalize()

    if period == "Weekly":
        # today.dayofweek is 0 for Monday, 6 for Sunday - subtracting that
        # many days from today always lands on the most recent Monday
        start = today - pd.Timedelta(days = today.dayofweek)
    else: # Monthly
        # Same month and year as today, just force the day back to the 1st
        start = today.replace(day=1)

    # Keep only rows whose date is on/after the start of this period
    return df[dates >= start]




def total_sections(df, title):

    """
    Build the income/expense/net + category-breakdown lines for
    whatever dataframe is passed in - could be the full history or
    a period-filtered section. Shared by both report sections so this
    formatting only gets written once.
    """

    income_total = calculate_total(df, "Income")
    expense_total = calculate_total(df, "Expense")
    net = calculate_net(df)

    income_group = category_group(df, "Income")
    expense_group = category_group(df, "Expense")

    lines = []
    # Build up the report one line at a time in a list, then join it
    # all together into one big string at the end    
    lines.append(title)
    lines.append("-" * len(title))
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

    # Return expense_total and net too, since build_summary_text needs
    # them later to check budget/savings progress against the goals
    return lines, expense_total, net
    

def build_summary_text(df, budget_goal, savings_goal, period):

    """
    Builds the full text report written to summary.txt. Includes two
    sections: an all time summary using every entry ever recorded, and
    a current period summary filtered down to week or month, depending on 
    what user selected
    """

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

    # Section 1: every entry ever logged, no date filtering at all
    all_time_lines, _, _ = total_sections(df, "ALL-TIME SUMMARY")
    lines.extend(all_time_lines)

    # Section 2: only entries from the current week/month, based on
    # whichever period the user chose in the Budget Goals window
    period_df = filter_by_period(df, period)
    period_lines, period_expense_total, period_net = total_sections(
        period_df, f"CURRENT {period.upper()} SUMMARY"
    ) 
    lines.extend(period_lines)

    # Budget Goal from main.py 
    lines.append(f"Budget Goal: ${budget_goal:.2f}")
    lines.append(f"  - Status: {budget_status(period_expense_total, budget_goal)}")
    lines.append("")

    # Function Call, using saving goal from main.py
    lines.append(f"Savings Goal: ${savings_goal:.2f}")
    progress = savings_progress(period_net, savings_goal)
    lines.append(f"  - Progress toward goal: {progress}%")

    # "\n".join(lines) glues every line together with a newline between
    # them, turning our list of strings into one final block of text
    return "\n".join(lines)
