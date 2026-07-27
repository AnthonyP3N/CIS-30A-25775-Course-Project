import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

# Custom mod file call
import budget_math 

# Path to user csv, change if different name
USER_CSV = "./records.csv"

# Choices for category dropdown boxes 
choices = ["Housing", "Utilities", "Transportation", "Groceries", "Insurance/Debt", "Dining Out", "Entertainment", "Personal Care", "Non-essential Shopping", "Savings", "Etc"]

try:
    df = pd.read_csv(USER_CSV)
except Exception as e:
    data = {
        "Date": [],
        "Description":[],
        "Amount":[],
        "Type":[],
        "Category":[]
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

    def save_entry(self, amount_entry, entry_type):
        global df 

        date = self.entry_date.get().strip()
        amount = amount_entry.get().strip()
        description = self.entry_description.get().strip()
        category = self.category_dropdown.get().strip()


        # basic validation so bad input doesn't effect csv file
        if not date or not amount:
            messagebox.showerror("Missing info", "Date and Amount are required.")
            return 
        if not category:
            messagebox.showerror("Missing info", "Please select a category.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid amount", "Amount must be a number.")
            return 

        new_row = {
            "Date": date,
            "Description": description,
            "Amount": amount,
            "Type": entry_type,
            "Category": category
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(USER_CSV, index=False)

        messagebox.showinfo("Saved", f"{entry_type} entry added!")
        self.root.destroy()


# Budget Tracker App - Connects to other option(s)
class BudgetTrackerApp(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Budget Tracker - Main Menu", "300x150")

        # Create a variable to track the window state
        self.expense_window = None
        self.income_window = None
        self.entries_window = None

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

        entries_screen = tk.Button(root,
                                   text="Read Entries",
                                   width=15,
                                   command= self.open_entries)
        entries_screen.pack()

    # function to open new window for expense
    def open_expense(self):
        # Check if window is NONE of if it has been destroyed
        # In place to prevent user from opening multiple windows
        if self.expense_window is None or not self.expense_window.winfo_exists():
            self.expense_window = tk.Toplevel(self.root)
            Expense(self.expense_window)
        else:
            # If window already exists, bring it toward the front for user to use
            self.expense_window.lift()

    def open_income(self):
        # Check if window is NONE of if it has been destroyed
        # In place to prevent user from opening multiple windows
        if self.income_window is None or not self.income_window.winfo_exists():
            self.income_window = tk.Toplevel(self.root)
            Income(self.income_window)
        else:
            # If window already exists, bring it toward the front for user to use
            self.income_window.lift()

    def open_entries(self):
        # Check if window is NONE of if it has been destroyed
        # In place to prevent user from opening multiple windows
        if self.entries_window is None or not self.entries_window.winfo_exists():
            self.entries_window = tk.Toplevel(self.root)
            Entries(self.entries_window)
        else:
            # If window already exists, bring it toward the front for user to use
            self.entries_window.lift()

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

        # Initializes category label for window and category drop down 
        self.label_description = tk.Label(root, text = "Category: ")
        self.label_description.grid(row = 3, column = 0)
        # state read-only; user may pick from list but may not type their own option!
        self.category_dropdown = ttk.Combobox(root, values = choices, state="readonly")
        self.category_dropdown.grid(row = 3, column = 1)

        self.button_add = tk.Button(root, text = "Add Entry", command = lambda : self.save_entry(self.entry_expense, "Expense"))
        self.button_add.grid(row = 4, column = 0, columnspan = 2)


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

        # Initializes category label for window and category drop down 
        self.label_description = tk.Label(root, text = "Category: ")
        self.label_description.grid(row = 3, column = 0)
        # state read-only; user may pick from list but may not type their own option!
        self.category_dropdown = ttk.Combobox(root, values = choices, state="readonly")
        self.category_dropdown.grid(row = 3, column = 1)

        self.button_add = tk.Button(root, text = "Add Entry", command = lambda : self.save_entry(self.entry_income, "Income"))
        self.button_add.grid(row = 4, column = 0, columnspan = 2)

# Entries Window - Showing the record log for all of user's provided entries, usage - USER_CSV 
class Entries(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Entries Record Log")

        

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

