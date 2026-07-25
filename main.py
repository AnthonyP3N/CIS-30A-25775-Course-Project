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

# main class - Budget Tracker
class BudgetTrackerApp:
    def __init__(self, root):
        # Initializes root and titlefor window
        self.root = root
        self.root.title("Budget Tracker")

        # Initializes label for window and text entry
        self.label_date = tk.Label(root, text = "Date: [YY-MM-DD]")
        self.label_date.grid(row = 0, column = 0)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row = 0, column = 1)


root = tk.Tk()
app = BudgetTrackerApp(root)
root.mainloop()

