from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import date

# ---------------------------- SAVE EXPENSES ------------------------------- #
def save_expenses():
    def clear():
        expenseName.delete(0, END)
        amountEntry.delete(0, END)
        dropdownExpenses.delete(0, END)

    name = expenseName.get().title()
    amount = amountEntry.get()
    expenseType = dropdownExpenses.get()
    today = date.today().isoformat()

    #Validation
    if not name or not amount or not expenseType:
        messagebox.showinfo(title="Expenses Error", message="Fields cannot be empty!")
        clear()
        return
    elif not name:
        messagebox.showinfo(title="Expenses Error", message="Provide name of the expense!")
        clear()
        return
    elif not amount.isdigit():
        messagebox.showinfo(title="Expenses Error", message="Amount has to be a number!")
        clear()
        return
    elif not expenseType:
        messagebox.showinfo(title="Expenses Error", message="Choose Expense type!")
        clear()
        return

    #JSON structure
    new_row = {
        name: {
            "Amount": amount,
            "Expense Type": expenseType,
            "Date": today
        }
    }

    #Open and add data to the .csv
    try:
        with open("data.json", "r") as data_file:
            expensesData = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        expensesData = {}

    expensesData.append(new_row)

    with open("data.json", "w") as data_file:
        json.dump(expensesData, data_file, indent=4)

    clear()
    messagebox.showinfo(title="Expenses Message", message="Expenses added successfully.")

# ------------------------- Goals Pop-Up ------------------------ #

def goals_popup():
    top = Toplevel(window)
    top.geometry("800x400")
    top.title("Goals & Limits")

# ------------------------- Calculate Pop-Up ------------------------ #

def calculate_popup():
    def calculation():
        savings = int(savingEntry.get())
        months = int(monthsEntry.get())
        result = savings / months
        clear()
        messagebox.showinfo("Monthly Saving", f"You need to save {result:.2f}£ per month.")

    def clear():
        savingEntry.delete(0, END)
        monthsEntry.delete(0, END)

    top = Toplevel(window)
    top.geometry("250x250")
    top.title("Calculate")

    # Amount
    savingLabel = Label(top, text="How much do you want to save?:")
    savingLabel.grid(row=0, column=0, padx=10, pady=10)
    savingEntry = Entry(top, width=20)
    savingEntry.grid(row=1, column=0, padx=10, pady=10)
    savingEntry.focus()

    # Months
    monthsLabel = Label(top, text="In how many months?:")
    monthsLabel.grid(row=2, column=0, padx=10, pady=10)
    monthsEntry = Entry(top, width=20)
    monthsEntry.grid(row=3, column=0, padx=10, pady=10)

    calculate_button = Button(top, text="Calculate", command=calculation)
    calculate_button.grid(row=4, column=0, columnspan=2, pady=15)

# ------------------------- Graph Pop-Up ------------------------ #
def expenses_popup():
    top = Toplevel(window)
    top.geometry("1000x400")
    top.title("Expenses Graph")

    #Open .csv - just read
    with open("data.json", "r") as data_file:
        data = json.load(data_file)

    tree = ttk.Treeview(top, columns=("Expense Name", "Amount", "Expense Type"), show='headings', height=15)
    tree.heading("Expense Name", text="Expense Name")
    tree.heading("Amount", text="Amount")
    tree.heading("Expense Type", text="Expense Type")
    tree.grid(row=0, column=0, sticky="n")

    for entry in data:
        for name, info in entry.items():
            tree.insert("", END, values=(name, info["Amount"], info["Expense Type"]))

    income = 0
    expenses = 0

    for entry in data:
        for _, item in entry.items():
            amount = int(item["Amount"])
            if item["Expense Type"] == "Income":
                income += amount
            elif item["Expense Type"] == "Expense":
                expenses += amount

    y = np.array([income, expenses])
    labels = ["Income", "Expenses"]

    fig = plt.Figure(figsize=(3,3), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(y, labels=labels)
    ax.set_title("Income vs Expenses")

    pie_chart = FigureCanvasTkAgg(fig, master=top)
    pie_chart.draw()
    pie_chart.get_tk_widget().grid(row=0, column=1, padx=30, sticky="n")

# ---------------------------- UI ------------------------------- #
window = Tk()
window.title("Expenses Tracker")
window.geometry("650x400")

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

display_graph = Button(text="Show Expenses", command=expenses_popup)
display_graph.grid(row=6, column=2, padx=5)

calculate = Button(text="Calculate", command=calculate_popup)
calculate.grid(row=6, column=3, padx=5)

calculate = Button(text="Goals & Limits", command=goals_popup)
calculate.grid(row=6, column=4, sticky="w", padx=5)

window.mainloop()