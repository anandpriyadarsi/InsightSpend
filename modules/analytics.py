import json

def financial_summary():

    with open("data/income.json", "r") as file:
        incomes = json.load(file)

    with open("data/expenses.json", "r") as file:
        expenses = json.load(file)

    total_income = sum(item["amount"] for item in incomes)
    total_expense = sum(item["amount"] for item in expenses)

    savings = total_income - total_expense

    if total_income > 0:
        savings_rate = (savings / total_income) * 100
    else:
        savings_rate = 0

    print("\n" + "=" * 50)
    print("           INSIGHTSPEND DASHBOARD")
    print("=" * 50)

    print(f"Total Income      : ₹{total_income:.2f}")
    print(f"Total Expense     : ₹{total_expense:.2f}")
    print(f"Savings           : ₹{savings:.2f}")
    print(f"Savings Rate      : {savings_rate:.2f}%")

    print("=" * 50)

    spending_by_category(expenses)

    print("=" * 50)

    highest_expense(expenses)

    print("=" * 50)

    payment_analysis(expenses)

    print("=" * 50)

    average_daily_expense(expenses)

    print("=" * 50)

    smart_insights(total_income, total_expense, expenses)

    print("=" * 50)
def spending_by_category(expenses):

    print("Spending By Category\n")

    categories = {}

    for expense in expenses:

        category = expense["category"]

        if category not in categories:
            categories[category] = 0

        categories[category] += expense["amount"]

    for category, amount in categories.items():
        print(f"{category:<15} ₹{amount:.2f}")
def highest_expense(expenses):

    if len(expenses) == 0:
        print("No expenses found.")
        return

    highest = max(expenses, key=lambda x: x["amount"])

    print("Highest Expense\n")

    print(f"Amount   : ₹{highest['amount']:.2f}")
    print(f"Category : {highest['category']}")
    print(f"Date     : {highest['date']}")
def payment_analysis(expenses):

    payments = {}

    for expense in expenses:

        payment = expense["payment_method"]

        if payment not in payments:
            payments[payment] = 0

        payments[payment] += 1

    print("Payment Method Usage\n")

    for payment, count in payments.items():
        print(f"{payment:<10} {count}")

    if len(payments) > 0:
        most_used = max(payments, key=payments.get)

        print(f"\nMost Used Payment : {most_used}")
def average_daily_expense(expenses):

    if len(expenses) == 0:
        print("Average Daily Expense : ₹0")
        return

    total = sum(item["amount"] for item in expenses)

    average = total / len(expenses)

    print(f"Average Expense : ₹{average:.2f}")
def smart_insights(total_income, total_expense, expenses):

    print("SMART INSIGHTS\n")

    if total_income == 0:
        print("No income recorded.")
        return

    if len(expenses) == 0:
        print("No expense records found.")
        return

    categories = {}

    for expense in expenses:

        category = expense["category"]

        if category not in categories:
            categories[category] = 0

        categories[category] += expense["amount"]

    highest_category = max(categories, key=categories.get)

    percentage = (categories[highest_category] / total_expense) * 100

    print(f"You spent {percentage:.1f}% on {highest_category}.")

    savings = total_income - total_expense

    if savings > 0:
        print("Great! You are saving money.")
    else:
        print("Warning! Your expenses are greater than your income.")

    if percentage > 40:
        print(f"Consider reducing your {highest_category} expenses.")
