import tkinter as tk

# Custom mod file call
import budget_math 

window = tk.Tk()
window.geometry("400x400")

label = tk.Label(
    text="Budget App v0.0",
    fg="white",
    bg="black",
    width= 30,
    height=15
)

label.pack()

window.mainloop()

