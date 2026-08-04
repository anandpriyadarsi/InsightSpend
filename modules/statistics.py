import json
from collections import Counter

INCOME_FILE = "data/income.json"
EXPENSE_FILE = "data/expenses.json"


# -----------------------------------------
# Load Data
# -----------------------------------------

def load_data():

    with open(INCOME_FILE, "r") as file:
        incomes = json.load(file)

    with open(EXPENSE_FILE, "r") as file:
        expenses = json.load(file)

    return incomes, expenses


# -----------------------------------------
# Statistics Dashboard
# -----------------------------------------

def statistics_dashboard():

    incomes, expenses = load_data()

    print("\n")
    print("=" * 60)
    print("            INSIGHTSPEND STATISTICS")
    print("=" * 60)

    # ---------------------------------
    # Basic Statistics
    # ---------------------------------

    total_income = sum(i["amount"] for i in incomes)
    total_expense = sum(e["amount"] for e in expenses)
    savings = total_income - total_expense

    print(f"Income Entries          : {len(incomes)}")
    print(f"Expense Entries         : {len(expenses)}")
    print(f"Total Income            : ₹{total_income:.2f}")
    print(f"Total Expense           : ₹{total_expense:.2f}")
    print(f"Net Savings             : ₹{savings:.2f}")

    print("-" * 60)

    # ---------------------------------
    # Average Expense
    # ---------------------------------

    if expenses:

        average = total_expense / len(expenses)

        print(f"Average Expense         : ₹{average:.2f}")

    else:

        print("Average Expense         : ₹0.00")

    # ---------------------------------
    # Largest Expense
    # ---------------------------------

    if expenses:

        largest = max(expenses, key=lambda x: x["amount"])

        print("\nLargest Expense")

        print(f"Amount                  : ₹{largest['amount']:.2f}")
        print(f"Category                : {largest['category']}")
        print(f"Date                    : {largest['date']}")

    # ---------------------------------
    # Smallest Expense
    # ---------------------------------

        smallest = min(expenses, key=lambda x: x["amount"])

        print("\nSmallest Expense")

        print(f"Amount                  : ₹{smallest['amount']:.2f}")
        print(f"Category                : {smallest['category']}")
        print(f"Date                    : {smallest['date']}")

    # ---------------------------------
    # Category Statistics
    # ---------------------------------

    if expenses:

        categories = Counter()

        for expense in expenses:

            categories[expense["category"]] += 1

        category = categories.most_common(1)[0]

        print("\nMost Used Category")

        print(f"{category[0]} ({category[1]} Transactions)")

    # ---------------------------------
    # Payment Statistics
    # ---------------------------------

    if expenses:

        payments = Counter()

        for expense in expenses:

            payments[expense["payment_method"]] += 1

        payment = payments.most_common(1)[0]

        print("\nMost Used Payment Method")

        print(f"{payment[0]} ({payment[1]} Transactions)")

    # ---------------------------------
    # Income Source Statistics
    # ---------------------------------

    if incomes:

        sources = Counter()

        for income in incomes:

            sources[income["source"]] += 1

        source = sources.most_common(1)[0]

        print("\nMost Common Income Source")

        print(f"{source[0]} ({source[1]} Entries)")

    # ---------------------------------
    # Savings Percentage
    # ---------------------------------

    if total_income > 0:

        savings_rate = (savings / total_income) * 100

    else:

        savings_rate = 0

    print("\nSavings Rate")

    print(f"{savings_rate:.2f}%")

    # ---------------------------------
    # Financial Status
    # ---------------------------------

    print("\nFinancial Status")

    if savings_rate >= 30:

        print("Excellent 🟢")

    elif savings_rate >= 15:

        print("Good 🟡")

    else:

        print("Needs Improvement 🔴")

    print("=" * 60)
