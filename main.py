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


        option_label = tk.Label(root, text = "Select an Option: ")
        option_label.pack()

        expense_screen = tk.Button(root, 
                                   text="Add Expense",
                                   width = 15,
                                   command= self.open_expense)
        expense_screen.pack()

    # function to open new window for expense
    def open_expense(self):
        expense_window = tk.Toplevel(self.root)
        Expense(expense_window)

# Expense Window - allow user to input information about a new expense 
class Expense(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Add Expense")
        # Initializes label for window and text entry
        self.label_date = tk.Label(root, text = "Date: [YY-MM-DD]")
        self.label_date.grid(row = 0, column = 0)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row = 0, column = 1)

        self.label_expense = tk.Label(root, text = "Expense: $")
        self.label_expense.grid(row = 1, column = 0)
        self.entry_expense = tk.Entry(root)
        self.entry_expense.grid(row = 1, column = 1)

        self.label_description = tk.Label(root, text = "Description: ")
        self.label_description.grid(row = 2, column = 0)
        self.entry_description = tk.Entry(root)
        self.entry_description.grid(row = 2, column = 1)       

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

