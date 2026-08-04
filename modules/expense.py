import json

def add_expense():
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount!")
        return

    category = input("Enter category: ")
    payment_method = input("Enter payment method (Cash/UPI/Card): ")
    date = input("Enter date (DD-MM-YYYY): ")
    notes = input("Enter notes: ")

    expense = {
        "amount": amount,
        "category": category,
        "payment_method": payment_method,
        "date": date,
        "notes": notes
    }

    with open("data/expenses.json", "r") as file:
        expenses = json.load(file)

    expenses.append(expense)

    with open("data/expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

    print("\nExpense Added Successfully!")
def view_expenses():

    with open("data/expenses.json", "r") as file:
        expenses = json.load(file)

    if len(expenses) == 0:
        print("\nNo expense records found.")
        return

    print("\n========== Expense Records ==========\n")

    for index, expense in enumerate(expenses, start=1):

        print(f"Expense No. : {index}")
        print(f"Amount      : ₹{expense['amount']}")
        print(f"Category    : {expense['category']}")
        print(f"Payment     : {expense['payment_method']}")
        print(f"Date        : {expense['date']}")
        print(f"Notes       : {expense['notes']}")
        print("-" * 45)
def edit_expense():

    with open("data/expenses.json", "r") as file:
        expenses = json.load(file)

    if len(expenses) == 0:
        print("No expenses found.")
        return

    view_expenses()

    try:
        index = int(input("\nEnter Expense Number to Edit: ")) - 1
    except ValueError:
        print("Invalid Input!")
        return

    if index < 0 or index >= len(expenses):
        print("Invalid Expense Number.")
        return

    expense = expenses[index]

    print("\nPress Enter to keep the old value.\n")

    amount = input(f"Amount ({expense['amount']}): ")
    category = input(f"Category ({expense['category']}): ")
    payment = input(f"Payment Method ({expense['payment_method']}): ")
    date = input(f"Date ({expense['date']}): ")
    notes = input(f"Notes ({expense['notes']}): ")

    if amount:
        expense["amount"] = float(amount)

    if category:
        expense["category"] = category

    if payment:
        expense["payment_method"] = payment

    if date:
        expense["date"] = date

    if notes:
        expense["notes"] = notes

    with open("data/expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

    print("\nExpense Updated Successfully!")
def delete_expense():

    with open("data/expenses.json", "r") as file:
        expenses = json.load(file)

    if len(expenses) == 0:
        print("No expenses found.")
        return

    view_expenses()

    try:
        index = int(input("\nEnter Expense Number to Delete: ")) - 1
    except ValueError:
        print("Invalid Input!")
        return

    if index < 0 or index >= len(expenses):
        print("Invalid Expense Number.")
        return

    confirm = input("Are you sure? (Y/N): ")

    if confirm.upper() == "Y":

        deleted = expenses.pop(index)

        with open("data/expenses.json", "w") as file:
            json.dump(expenses, file, indent=4)

        print(f"\nDeleted ₹{deleted['amount']} ({deleted['category']})")

    else:
        print("Deletion Cancelled.")

EXPENSE_FILE = "data/expenses.json"


def display_expense(expense):
    print("\n----------------------")
    print(f"Amount   : ₹{expense['amount']}")
    print(f"Category : {expense['category']}")
    print(f"Payment  : {expense['payment_method']}")
    print(f"Date     : {expense['date']}")
    print(f"Notes    : {expense['notes']}")
    print("----------------------")


def search_expenses():

    print("\n====== Search Expenses ======")
    print("1. Search by Category")
    print("2. Search by Payment Method")
    print("3. Search by Date")
    print("4. Search by Amount Range")

    choice = input("\nEnter your choice: ")

    with open(EXPENSE_FILE, "r") as file:
        expenses = json.load(file)

    if len(expenses) == 0:
        print("\nNo expense records found.")
        return

    # Search by Category
    if choice == "1":

        category = input("Enter Category: ").title()

        found = False

        for expense in expenses:

            if expense["category"].title() == category:
                display_expense(expense)
                found = True

        if not found:
            print("\nNo matching expense found.")

    # Search by Payment Method
    elif choice == "2":

        payment = input("Enter Payment Method: ").title()

        found = False

        for expense in expenses:

            if expense["payment_method"].title() == payment:
                display_expense(expense)
                found = True

        if not found:
            print("\nNo matching expense found.")

    # Search by Date
    elif choice == "3":

        date = input("Enter Date (DD-MM-YYYY): ")

        found = False

        for expense in expenses:

            if expense["date"] == date:
                display_expense(expense)
                found = True

        if not found:
            print("\nNo matching expense found.")

    # Search by Amount Range
    elif choice == "4":

        try:
            minimum = float(input("Minimum Amount: "))
            maximum = float(input("Maximum Amount: "))
        except ValueError:
            print("Invalid Amount!")
            return

        found = False

        for expense in expenses:

            if minimum <= expense["amount"] <= maximum:
                display_expense(expense)
                found = True

        if not found:
            print("\nNo matching expense found.")

    else:
        print("\nInvalid Choice!")
