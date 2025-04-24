from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json

# ---------------------------- SAVE EXPENSES ------------------------------- #
def save_expenses():
    def clear():
        expenseName.delete(0, END)
        amountEntry.delete(0, END)
        dropdownExpenses.delete(0, END)

    name = expenseName.get().title()
    amount = amountEntry.get()
    expenseType = dropdownExpenses.get()

    if not amount.isdigit():
        messagebox.showinfo(title="Expenses Error", message="Amount has to be a number!")
        clear()
        return

    new_row = {
        name: {
            "Amount": amount,
            "Expense Type": expenseType
        }
    }
    with open("data.json", "r") as data_file:
        expensesData = json.load(data_file)

    expensesData.update(new_row)

    with open("data.json", "w") as data_file:
        json.dump(expensesData, data_file, indent=4)

    clear()
    messagebox.showinfo(title="Expenses Message", message="Expenses added successfully.")

# ---------------------------- UI ------------------------------- #
window = Tk()
window.title("Expenses Tracker")
window.geometry("600x400")

#Resize column evenly with the same weight
for i in range(6):
    window.grid_columnconfigure(i, weight=1)

#Logo
lock_img = PhotoImage(file="img/expenses.png")
canvas = Canvas(width=200, height=200)
canvas.grid(row=1, column=0, columnspan=6, pady=30)
canvas.create_image(100, 100, image=lock_img)

#Expense name
expenseNameLabel = Label(text="Expense Name:")
expenseNameLabel.grid(row=2, column=2, sticky="e", padx=5)
expenseName = Entry(width=20)
expenseName.grid(row=2, column=3, sticky="w", padx=5)
expenseName.focus()

#Expense amount
amountLabel = Label(text="Amount:")
amountLabel.grid(row=3, column=2, sticky="e", padx=5)
amountEntry = Entry(width=20)
amountEntry.grid(row=3, column=3, sticky="w", padx=5)

#Dropdown
typeLabel = Label(text="Type:")
typeLabel.grid(row=4, column=2, sticky="e", padx=5)
typeOfExpense = ["Expense", "Income"]
dropdownExpenses = ttk.Combobox(window, values=typeOfExpense)
dropdownExpenses.grid(row=4, column=3, sticky="w", padx=5)

add_button = Button(text="Add Expense", command=save_expenses)
add_button.grid(row=5, column=0, columnspan=6)

window.mainloop()