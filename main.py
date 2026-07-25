import tkinter as tk
import pandas as pd

# Custom mod file call
import budget_math 

try:
    df = pd.read_csv("./records.csv")
except Exception as e:
    data = {
        "Date": [],
        "Description":[],
        "Amount":[],
        "Type":[]
    }

    df = pd.DataFrame(data)

# main class - Base Window Setup
class MainMenu:
    def __init__(self, root, title, size = None):
        # Initializes root and title for window(s)
        self.root = root
        self.root.title(title)
        # error case, crashes without
        if size:
            self.root.geometry(size)

# Budget Tracker App - Connects to other option(s)
class BudgetTrackerApp(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Budget Tracker - Main Menu", "300x150")

        # Create a variable to track the window state
        self.expense_window = None
        self.income_window = None

        option_label = tk.Label(root, text = "Select an Option: ")
        option_label.pack()

        expense_screen = tk.Button(root, 
                                   text="Add Expense",
                                   width = 15,
                                   command= self.open_expense)
        expense_screen.pack()

        income_screen = tk.Button(root, 
                                   text="Add Income",
                                   width = 15,
                                   command= self.open_income)
        income_screen.pack()

    # function to open new window for expense
    def open_expense(self):
        # Check if window is NONE of if it has been destroyed
        # In place to prevent user from opening multiple expense/income windows
        if self.expense_window is None or not self.expense_window.winfo_exists():
            self.expense_window = tk.Toplevel(self.root)
            Expense(self.expense_window)
        else:
            # If window already exists, bring it toward the front for user to use
            self.expense_window.lift()

    def open_income(self):
        # Check if window is NONE of if it has been destroyed
        # In place to prevent user from opening multiple income/expense windows
        if self.income_window is None or not self.income_window.winfo_exists():
            self.income_window = tk.Toplevel(self.root)
            Income(self.income_window)
        else:
            # If window already exists, bring it toward the front for user to use
            self.income_window.lift()

# Expense Window - allow user to input information about a new expense 
class Expense(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Add Expense")

        # Initializes date label for window and date text entry
        self.label_date = tk.Label(root, text = "Date: [YY-MM-DD]")
        self.label_date.grid(row = 0, column = 0)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row = 0, column = 1)

        # Initializes expense label for window and expense text entry
        self.label_expense = tk.Label(root, text = "Expense: $")
        self.label_expense.grid(row = 1, column = 0)
        self.entry_expense = tk.Entry(root)
        self.entry_expense.grid(row = 1, column = 1)

        # Initializes description label for window and description text entry
        self.label_description = tk.Label(root, text = "Description: ")
        self.label_description.grid(row = 2, column = 0)
        self.entry_description = tk.Entry(root)
        self.entry_description.grid(row = 2, column = 1)       


# Income Window - allow user to input information about a new expense 
class Income(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Add Income")

        # Initializes date label for window and date text entry
        self.label_date = tk.Label(root, text = "Date: [YY-MM-DD]")
        self.label_date.grid(row = 0, column = 0)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row = 0, column = 1)

        # Initializes expense label for window and income text entry
        self.label_income = tk.Label(root, text = "Income: $")
        self.label_income.grid(row = 1, column = 0)
        self.entry_income = tk.Entry(root)
        self.entry_income.grid(row = 1, column = 1)

        # Initializes description label for window and description text entry
        self.label_description = tk.Label(root, text = "Description: ")
        self.label_description.grid(row = 2, column = 0)
        self.entry_description = tk.Entry(root)
        self.entry_description.grid(row = 2, column = 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

