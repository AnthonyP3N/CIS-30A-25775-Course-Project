
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


