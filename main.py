import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd

# Custom mod file call
import budget_math as budget

# Constant Variables - change according to user path files
GOALS_CSV = "./budget_goals.csv"
USER_CSV = "./records.csv"
SUMMARY_TXT = "./summary.txt"


# Choices for category dropdown boxes 
choices = ["Housing", "Utilities", "Transportation", "Groceries", "Insurance/Debt", "Dining Out", "Entertainment", "Personal Care", "Non-essential Shopping","Payroll", "Savings", "Etc"]

# Choices for amount of time user wants to budget for (Montly/Weekly)
period_choices = ["Monthly", "Weekly"]

# Load the user's saved transactions when the program starts.
# If the CSV doesn't exist yet (first time running the app), fall back
# to an empty table with the right columns instead of crashing.
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
# Every window class in this program (Expense, Income, Entries, etc.)
# inherits from MainMenu, so this is the base class and everything else
# is a subclass of it.
class MainMenu:
    def __init__(self, root, title, size = None):
        # Initializes root and title for window(s)
        self.root = root
        self.root.title(title)
        # error case, crashes without
        if size:
            self.root.geometry(size)

    def save_entry(self, entry_amount, entry_type):
        # Shared by both the Expense and Income windows - entry_type tells
        # this function which one called it ("Expense" or "Income"), so
        # one method can handle both instead of writing it twice.
        global df 

        date = self.entry_date.get().strip()
        amount = entry_amount.get().strip()
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


        # Add the new entry onto the end of the existing table, then
        # save the whole table back out to the CSV file so it's not lost
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(USER_CSV, index=False)

        messagebox.showinfo("Saved", f"{entry_type} entry added!")
        self.root.destroy()


# Budget Tracker App - Connects to other option(s)
# This is the main menu window - the first thing the user sees, and the
# hub that opens every other window in the program.
class BudgetTrackerApp(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Budget Tracker - Main Menu","320x250")

        # Create a variable to track the window state
        # Each of these starts as None, meaning "not open yet". Every
        # open_* method below checks this before creating a new window,
        # so clicking a button twice doesn't open two copies of it.
        self.expense_window = None
        self.income_window = None
        self.entries_window = None
        self.summary_window = None
        self.goals_window = None


        # A frame to hold everything, so it can expand as one unit
        # instead of each widget doing its own thing
        menu_frame = tk.Frame(root)
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Label that tells user to select an option from below
        option_label = tk.Label(menu_frame, text = "Select an Option: ")
        option_label.pack(fill="x")

        """
        Buttons that transition user to window options, use command to open new window.
        Command points to function that opens new window
        
        """ 
        goals_screen = tk.Button(menu_frame,
                                   text="Set Budget and Savings Goals",
                                   width=25,
                                   command=self.open_goals)
        goals_screen.pack(fill="x", pady=2)        

        expense_screen = tk.Button(menu_frame, 
                                   text="Add Expense",
                                   width = 15,
                                   command= self.open_expense)
        expense_screen.pack(fill="x", pady=2)

        income_screen = tk.Button(menu_frame, 
                                   text="Add Income",
                                   width = 15,
                                   command= self.open_income)
        income_screen.pack(fill="x", pady=2)

        entries_screen = tk.Button(menu_frame,
                                   text="Read Entries",
                                   width=15,
                                   command= self.open_entries)
        entries_screen.pack(fill="x", pady=2)

        summary_screen = tk.Button(menu_frame,
                                   text="View Summary",
                                   width=15,
                                   command=self.open_summary)
        summary_screen.pack(fill="x", pady=2)


        summary_export_window = tk.Button(menu_frame,
                                          text="Export summary.txt",
                                          width=25,
                                          command=self.export_summary)
        summary_export_window.pack(fill="x", pady=2)

        exit_screen = tk.Button(menu_frame,
                         text="Exit",
                         width=25,
                         command=root.destroy)
        exit_screen.pack(fill="x", pady=2)
                                        

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


    def open_summary(self):
        # Check if window is NONE of if it has been destroyed
        # In place to prevent user from opening multiple windows
        if self.summary_window is None or not self.summary_window.winfo_exists():
            self.summary_window = tk.Toplevel(self.root)
            Summary(self.summary_window)
        else:
            # If window already exists, bring it toward the front for user to use
            self.summary_window.lift()    
               

    def open_goals(self):
        # Check if window is NONE of if it has been destroyed
        # In place to prevent user from opening multiple windows
        if self.goals_window is None or not self.goals_window.winfo_exists():
            self.goals_window = tk.Toplevel(self.root)
            BudgetGoals(self.goals_window)
        else:
            # If window already exists, bring it toward the front for user to use
            self.goals_window.lift()   


    def export_summary(self):
        # This is the file-output feature the assignment asks for: it
        # reads the user's data, hands it to the custom module to do
        # all the math, and writes the result out as a real .txt file.
 
        # Read user records
        try:
            records_df = pd.read_csv(USER_CSV)
        except Exception:
            records_df = pd.DataFrame(columns=["Date", "Description", "Amount", "Type", "Category"])

        try:
            goals_df = pd.read_csv(GOALS_CSV)
            period = goals_df.loc[0, "Period"]
            budget_goal = goals_df.loc[0, "BudgetGoal"]
            savings_goal = goals_df.loc[0, "SavingsGoal"]
        except Exception:
            period = "Monthly"
            budget_goal = 0.0
            savings_goal = 0.0

        report_text = budget.build_summary_text(records_df, budget_goal, savings_goal, period)

        try:
            with open(SUMMARY_TXT, "w") as f:
                f.write(report_text)
        except OSError as e:
            messagebox.showerror("File Error", f"Could not write summary file: error({e})")
            return

        messagebox.showinfo("Summary Exported", f"Summary written to {SUMMARY_TXT}")

# Expense Window - allow user to input information about a new expense 
class Expense(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Add Expense")

        # Initializes date label for window and date text entry
        self.label_date = tk.Label(root, text = "Date: [YYYY-MM-DD]")
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
        self.label_date = tk.Label(root, text = "Date: [YYYY-MM-DD]")
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

# Summary Window - show user's budget results
class Summary(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Budget Summary", "250x150")

        # Read CSV, same logic as Entries window
        try:
            self.summary_df = pd.read_csv(USER_CSV)
        except Exception:
            self.summary_df = pd.DataFrame(columns=["Date", "Description", "Amount", "Type", "Category"])


        # Which period (Monthly/Weekly) the user set as their budget
        # period, so "This Period" here lines up with their goal
        try:
            goals_df = pd.read_csv(GOALS_CSV)
            self.period = goals_df.loc[0, "Period"]
        except Exception:
            self.period = "Monthly"

        # Allows user to see a summary of all time or period
        self.label_scope = tk.Label(root, text="View: ")
        self.label_scope.grid(row=0, column=0)
        self.scope_dropdown = ttk.Combobox(root, values=["All Time", "This Period"], state="readonly")
        self.scope_dropdown.set("All Time")
        self.scope_dropdown.grid(row=0, column=1)
        # Recalculate the moment the user picks a different scope
        self.scope_dropdown.bind("<<ComboboxSelected>>", self.update_labels)



        # These three labels start blank and get filled in by
        # update_labels() below - once here in __init__, and again
        # every time the dropdown selection changes
        self.label_income = tk.Label(root, text = "")
        self.label_income.grid(row=1, column=0, columnspan=2, pady=5)

        self.label_expense = tk.Label(root, text = "")
        self.label_expense.grid(row=2, column=0, columnspan=2, pady=5)

        self.label_net = tk.Label(root, text = "")
        self.label_net.grid(row=3, column=0, columnspan=2, pady=5)

        self.label_period = tk.Label(root, text="")
        self.label_period.grid(row=4,column=0,columnspan=2, pady=5 )

        # Fill in the labels the first time using the default scope
        self.update_labels()

    def update_labels(self, event=None):
        # event=None lets this method be called two different ways:
        # automatically by tkinter (which passes an event object when
        # the dropdown changes) or manually by us in __init__ (with no
        # event at all).
        scope = self.scope_dropdown.get()

        if scope == "This Period":
            display_df = budget.filter_by_period(self.summary_df, self.period)
            period_text = f"Period: {self.period}"
        else:
            display_df = self.summary_df
            period_text = "Period: All Time"

        income_total = budget.calculate_total(display_df, "Income")
        expense_total = budget.calculate_total(display_df, "Expense")
        net = budget.calculate_net(display_df)

        # .config() updates a widget that already exists on screen
        self.label_income.config(text = f"Total Income: ${income_total:.2f}")
        self.label_expense.config(text = f"Total Expense: ${expense_total:.2f}")
        self.label_net.config(text = f"Net total: ${net:.2f}")
        self.label_period.config(text = period_text)

# Budget Goals window = show user's goals
class BudgetGoals(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Set Budget & Savings Goals", "320x100")

        # Try tp load goals that were saved. 
        try:
            goals_df = pd.read_csv(GOALS_CSV)
            current_period = goals_df.loc[0, "Period"]
            current_budget = goals_df.loc[0, "BudgetGoal"]
            current_savings = goals_df.loc[0, "SavingsGoal"]
        except Exception:
            # No goals file yet (first time using this window) - just
            # show sensible starting values instead of an error
            current_period = "Monthly"
            current_budget = 0.0
            current_savings = 0.0

        # Budget Period Label, grid, and dropdown box, period_choices = Weekly, Monthly
        self.label_period = tk.Label(root, text = "Budget Period: ")
        self.label_period.grid(row=0, column=0)
        self.period_dropdown = ttk.Combobox(root, values= period_choices, state="readonly")
        self.period_dropdown.set(current_period)
        self.period_dropdown.grid(row=0, column=1)


        self.label_budget = tk.Label(root, text = "Budget Goal: $")
        self.label_budget.grid(row=1, column=0)
        self.entry_budget = tk.Entry(root)
        self.entry_budget.insert(0, str(current_budget))
        self.entry_budget.grid(row=1, column=1)


        self.label_savings = tk.Label(root, text = "Savings Goal: $")
        self.label_savings.grid(row=2, column=0)
        self.entry_savings = tk.Entry(root)
        self.entry_savings.insert(0, str(current_savings))
        self.entry_savings.grid(row=2, column=1)


        self.button_save = tk.Button(root, text = "Save Goals", command=self.save_goals)
        self.button_save.grid(row=3, column=0, columnspan= 2, pady= 10)

    def save_goals(self):
        period = self.period_dropdown.get().strip()
        budget_text = self.entry_budget.get().strip()
        savings_text = self.entry_savings.get().strip()

        if not period:
            messagebox.showerror("Missing Info", "Please select a budget period.")
            return 

        try:
            # Change data type of text from str to float for use cases
            budget_goal = float(budget_text)
            savings_goal = float(savings_text)
        except ValueError:
            messagebox.showerror("Invalid amount", "Budget and Savings goals must be numbers.")
            return

        goals_df = pd.DataFrame([{
            "Period": period,
            "BudgetGoal": budget_goal,
            "SavingsGoal": savings_goal
        }])

        try:
            goals_df.to_csv(GOALS_CSV, index=False)
        except OSError as e:
            messagebox.showerror("File Error", f"Could not save goals due to {e}")
            return

        messagebox.showinfo("Saved", "Budget and savings goals updated!")
        self.root.destroy()

# Entries Window - Showing the record log for all of user's provided entries, usage - USER_CSV 
class Entries(MainMenu):
    def __init__(self, root):
        super().__init__(root, "Entries Record Log", "650x400")

        global df 
        self.empty_label = None 

        # Try to load saved records from CSV file 
        # If file doesn't exist or no entries added, through exception
        # to an empty table with the right column names needed 
        try:
            entries_df = pd.read_csv(USER_CSV)
        except Exception:
            entries_df = pd.DataFrame(columns=["Date", "Description", "Amount", "Type", "Category"])


        # Grab column names from data frame, i.e.
        # (Date, Description, Amount, Type, Category) so table headers match CSV.
        # IMPORTANT: this has to happen BEFORE the _sort_key column gets
        # added below, otherwise _sort_key would show up as its own
        # column in the table.
        columns = list(entries_df.columns)

        # Sort by date. pd.to_datetime parses the Date strings into real dates
        # so "2026-07-2" sorts correctly next to "2026-07-15" 
        # (plain string sorting would put "2" after "15"). 
        # errors="coerce" turns any unparseable date into NaT instead of crashing, and na_position="last"
        # just pushes those bad rows to the bottom instead of losing them.
        entries_df = entries_df.copy()
        entries_df["_sort_key"] = pd.to_datetime(entries_df["Date"], errors="coerce")
        entries_df = entries_df.sort_values("_sort_key", na_position="last")

        # Frame to group table and scroll bar together
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Use tkinter's built-in table widget of Treeview
        # show = "headings" hides extra leftmost "tree" column, to make output look cleaner
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # for each colum, set its header text than give it a fix width 
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")

        # Scroll bar for when there are more rows than what can fit on user's screen.
        # command = self.tree.yview - is for vertical movement
        scrollbar = ttk.Scrollbar(table_frame, orient = "vertical", command=self.tree.yview)

        # Updates scrollbar's position
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Format table on left, scroll bar on right, both filling available space
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        # Loop through every row (now in date order) and add it as a
        # row in the table.
        # .iterrows() gives (index, row) pairs - index is the row's
        # position in the original dataframe, which we keep as the
        # table row's iid so Edit/Delete know exactly which row to touch.
        for index, row in entries_df.iterrows():

            # Pull value for each colum, same order as "columns", for formatting.
            # change _ to index to keep track for deleting
            values = [row[col] for col in columns]
            self.tree.insert("", "end",iid=str(index), values=values)

        # Throw a message if no entries to show
        if entries_df.empty:
            empty_label = tk.Label(root, text="No entries yet")
            empty_label.pack(pady=(0,10))

        button_frame = tk.Frame(root)
        button_frame.pack(pady=(0,10))


        self.delete_button = tk.Button(button_frame, text="Delete Selected", command=self.delete_selected)
        self.delete_button.grid(row = 0, column = 0, padx = 5)   

        self.edit_button = tk.Button(button_frame, text="Edit Selected", command = self.edit_selected)
        self.edit_button.grid(row = 0, column = 1, padx = 5)   


    def get_selected_index(self):
            # Return the dateframe index of currently selected row or none.
            # This is shared by both delete_selected and edit_selected,
            # since they both need to know which row the user clicked on.            
            selection = self.tree.selection()
            # error handling
            if not selection:
                messagebox.showwarning("No Selection", "Please select a row first.")
                return None
            return int(selection[0])
        
    def delete_selected(self):
            global df 

            # check selected index, if none do nothing
            row_index = self.get_selected_index()
            if row_index is None:
                return

            # Ask user for confirmation to delete a entry 
            confirm = messagebox.askyesno("Confirm Delete", "Delete selected entry?")

            # if no, pass on do nothing
            if not confirm:
                return

            # Drop selected row 
            # no reset_index() here on purpose - resetting would
            # renumber every remaining row, which would break the link
            # between the dataframe and the table's row iids while this
            # window stays open.
            df = df.drop(index=row_index)

            # Try condition for that reads user csv, if any error occurs with csv file throw messagebox 
            try:
                df.to_csv(USER_CSV, index=False)
            except OSError as e:
                messagebox.showerror("File Error", f"Could not save user's changes: {e}")
                return

            # Built-in method, use to delete selected row
            self.tree.delete(str(row_index))

    def edit_selected(self):
            global df 

            # check selected index, if none do nothing
            row_index = self.get_selected_index()
            if row_index is None:
                return
            
            # Open a popup window prefilled with row's current values.
            # Pass self so EditEntry can update this window's table after saving.
            edit_window = tk.Toplevel(self.root)
            EditEntry(edit_window, row_index, self)

# Small popup window used to edit one existing entry - opened by
# Entries.edit_selected() above
class EditEntry(MainMenu):
    def __init__(self, root, row_index, entries_window):
        super().__init__(root, "Edit Entry")

        self.row_index = row_index
        self.entries_window = entries_window

        global df
        current_row = df.loc[row_index]

        # Re implment previous logic to edit selected option
        # insert is a tkinter method that pre-fills the entry box with the row's
        # current value, so the form opens already populated instead of blank.
        # str() is needed because the value comes out of the dataframe as numpy
        # insert() requires an actual string.

        self.label_date = tk.Label(root, text = "Date: [YYYY-MM-DD]")
        self.label_date.grid(row = 0, column = 0)
        self.entry_date = tk.Entry(root)
        self.entry_date.insert(0, str(current_row["Date"]))
        self.entry_date.grid(row = 0, column = 1)

        self.label_amount = tk.Label(root, text = "Amount: $")
        self.label_amount.grid(row = 1, column = 0)
        self.entry_amount = tk.Entry(root)
        self.entry_amount.insert(0, str(current_row["Amount"]))
        self.entry_amount.grid(row = 1, column = 1)

        self.label_description = tk.Label(root, text = "Description: ")
        self.label_description.grid(row = 2, column = 0)
        self.entry_description = tk.Entry(root)
        self.entry_description.insert(0, str(current_row["Description"]))
        self.entry_description.grid(row = 2, column = 1)

        self.label_description = tk.Label(root, text = "Category: ")
        self.label_description.grid(row = 3, column = 0)
        self.category_dropdown = ttk.Combobox(root, values = choices, state="readonly")
        self.category_dropdown.set(current_row["Category"])
        self.category_dropdown.grid(row = 3, column = 1)        

        self.label_type = tk.Label(root, text = "Type: ")
        self.label_type.grid(row = 4, column = 0)
        self.type_dropdown = ttk.Combobox(root, values = ["Expense", "Income"], state = "readonly")
        self.type_dropdown.set(current_row["Type"])
        self.type_dropdown.grid(row = 4, column = 1)      

        self.button_save = tk.Button(root, text="Save Changes", command=self.save_changes)
        self.button_save.grid(row = 5, column = 0, columnspan = 2, pady = 10)

    def save_changes(self):
        global df

        date = self.entry_date.get().strip()
        amount = self.entry_amount.get().strip()
        description = self.entry_description.get().strip()
        category = self.category_dropdown.get().strip()
        entry_type = self.type_dropdown.get().strip()

        # basic validation so bad input doesn't effect csv file
        if not date or not amount or not category:
            messagebox.showerror("Missing info", "Date, Amount, and Category are required.")
            return 

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid amount", "Amount must be a number.")
            return 

        # Updates data frame to match changes made by user
        df.loc[self.row_index, "Date"] = date
        df.loc[self.row_index, "Amount"] = amount
        df.loc[self.row_index, "Description"] = description
        df.loc[self.row_index, "Category"] = category
        df.loc[self.row_index, "Type"] = entry_type

        # Try condition for that reads user csv, if any error occurs with csv file throw messagebox 
        try:
            df.to_csv(USER_CSV, index=False)
        except OSError as e:
            messagebox.showerror("File Error", f"Could not save user's changes: {e}")
            return       

        # Update row's being displayed to new changes
        new_values = [date, description, amount, entry_type, category]
        self.entries_window.tree.item(str(self.row_index), values = new_values)

        messagebox.showinfo("Saved", "Entry updated!")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

