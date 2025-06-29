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
    def set_goals_and_limitations():
        def clear_goals():
            goalName.delete(0, END)
            goalEntry.delete(0, END)

        def save_goals():
            gname = goalName.get().title()
            gentry = goalEntry.get()

            #JSON structure
            goals_row = {
                gname: {
                    "Amount": gentry,
                    "Saved": 0
                }
            }

            #Open and add data to the .csv
            try:
                with open("goals.json", "r") as data_file:
                    goals_data = json.load(data_file)
            except (FileNotFoundError, json.JSONDecodeError):
                goals_data = {}

            goals_data.append(goals_row)

            with open("goals.json", "w") as data_file:
                json.dump(goals_data, data_file, indent=4)

            clear_goals()
            messagebox.showinfo(title="Goals Message", message="Goal added successfully.")

        top_goals = Toplevel(window)
        top_goals.geometry("200x150")
        top_goals.title("Set Goals & Limits")

        #Goal name
        goalNameLabel = Label(top_goals, text="Goal Name:")
        goalNameLabel.grid(row=0, column=0, padx=5)
        goalName = Entry(top_goals, width=20)
        goalName.grid(row=1, column=0, padx=5)

        #Goal amount
        goalLabel = Label(top_goals, text="Goal Amount:")
        goalLabel.grid(row=3, column=0, padx=5)
        goalEntry = Entry(top_goals, width=20)
        goalEntry.grid(row=4, column=0, padx=5)

        #Add Goal
        add_goal = Button(top_goals, text="Add Goal", command=save_goals)
        add_goal.grid(row=5, pady=5)

    def remove_goal():
        chosen_goal = dropdownGoals.get()

        if not chosen_goal:
            messagebox.showinfo(title="Goals Error", message="Choose a goal!")

        try:
            with open("goals.json", "r") as data_file:
                goals_data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            goals_data = []

        new_goals_data = []

        for goal_dict in goals_data:
            if chosen_goal not in goal_dict:
                new_goals_data.append(goal_dict)

        goals_data = new_goals_data

        with open("goals.json", "w") as f:
            json.dump(goals_data, f, indent=4)

        #New values for dropdown
        new_values = [name for goal in goals_data for name in goal]
        dropdownGoals["values"] = new_values
        dropdownGoals.set("")  #clear current selection

        messagebox.showinfo("Remove Goal", f"Goal “{chosen_goal}” removed.")



    top = Toplevel(window)
    top.geometry("800x400")
    top.title("Goals & Limits")

    set_goals = Button(top, text="Set Goals & Limitations", command=set_goals_and_limitations)
    set_goals.grid(row=0, column=0)

    add_money_to_goal = Button(top, text="Add money to your goal")
    add_money_to_goal.grid(row=1, column=0)

    goals = []

    with open("goals.json", "r") as data_file:
        goals_to_delete = json.load(data_file)
        for goal in goals_to_delete:
            for name in goal:
                goals.append(name)

    dropdownGoals = ttk.Combobox(top, values=goals)
    dropdownGoals.grid(row=2, column=0)

    remove_goal_button = Button(top, text="Remove Goal", command=remove_goal)
    remove_goal_button.grid(row=3, column=0)

    #Display goals and savings

    Label(top, text="Goals Progress", font=("Arial", 20, "bold")).grid(row=0, column=1)

    with open("goals.json", "r") as goals_data:
        goals_data = json.load(goals_data)

    row = 1
    row2 = 2
    for goal in goals_data:
        for name, details in goal.items():
            Label(top, text=name, font=("Arial", 20, "bold")).grid(row=row, column=1, columnspan=2)
            Label(top, text=f"{details['Saved']}/{details['Amount']}", font=("Arial", 20, "bold")).grid(row=row2, column=1)
            row += 2
            row2 += 2

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
    top.geometry("950x350")
    top.title("Expenses")

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