# CIS-30A-25775-Course-Project
Personal Finance Tracking Program

A desktop budget tracker built with Python (tkinter + pandas). Log expenses and income, set weekly/monthly budget and savings goals, edit or delete past entries, and export a text-file summary report, all stored locally in CSV files; no account or internet connection required.

Features: 
Add Expense / Add Income 
- log a transaction with a date, amount, description, and category (chosen from a fixed dropdown so category names stay consistent).
  
Read Entries
- view every transaction in a sortable table (sorted by date), with the ability to edit or delete any past entry directly.
  
Set Budget & Savings Goals
 - set a recurring budget goal and a savings goal on either a Monthly or Weekly cycle.
   
View Summary
- a live on-screen breakdown of income, expenses, and net balance, toggleable between All Time and This Period totals.
  
Export summary.txt
- writes a full text report to disk, including an all-time summary, a current-period summary broken down by category, and a status message describing whether you're over or under budget.

Project Structure
- main.py            # tkinter GUI - all windows and user interaction
-  budget_math.py      # custom module - all calculations live here
-   records.csv         # transaction log (created automatically on first run)
-  budget_goals.csv     # saved budget/savings goals (created automatically)
- summary.txt          # generated report (created when you export a summary)


main.py and budget_math.py are deliberately kept separate: main.py handles the interface (windows, buttons, forms), while budget_math.py handles every calculation (totals, category breakdowns, budget/savings status, date filtering). None of the math lives in the GUI code.

To get started -
Requirements: Python 3, pandas

bash

- pip install pandas

Run the program:

bash

- python main.py

The first time you run it, records.csv and budget_goals.csv don't exist yet; the program creates them automatically once you add your first entry or save your first goal, so no manual setup is needed.

Usage
1. Open Set Budget & Savings Goals first to set a Monthly or Weekly budget and savings target (optional, but the summary export is more useful with these set).
2. Use Add Expense / Add Income to log transactions as they happen.
3. Use Read Entries to review, edit, or delete anything you've logged.
4. Use View Summary to check your totals at a glance, or Export summary.txt to generate a saved report.
   
Known Limitations
- Supports a single user and a single set of goals at a time; no multi-profile support.
- Categories are a fixed list defined in main.py; adding a new category requires editing the source code.
- Weekly/Monthly periods are calculated relative to the current calendar date, not a custom user-defined start date.
- No charts or graphs; output is limited to a table view and a plain-text report.


