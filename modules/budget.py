import json

BUDGET_FILE = "data/budget.json"
EXPENSE_FILE = "data/expenses.json"


def set_budget():

    category = input("Enter Category: ").title()

    try:
        amount = float(input("Enter Budget Amount: "))
    except ValueError:
        print("Invalid Amount!")
        return

    with open(BUDGET_FILE, "r") as file:
        budgets = json.load(file)

    budgets[category] = amount

    with open(BUDGET_FILE, "w") as file:
        json.dump(budgets, file, indent=4)

    print(f"\nBudget for {category} set to ₹{amount:.2f}")
def view_budget():

    with open(BUDGET_FILE, "r") as file:
        budgets = json.load(file)

    if len(budgets) == 0:
        print("\nNo budgets found.")
        return

    print("\n========== Monthly Budgets ==========\n")

    print(f"{'Category':<15}{'Budget'}")
    print("-" * 30)

    for category, amount in budgets.items():
        print(f"{category:<15}₹{amount:.2f}")

    print("-" * 30)
def budget_status():

    with open(BUDGET_FILE, "r") as file:
        budgets = json.load(file)

    with open(EXPENSE_FILE, "r") as file:
        expenses = json.load(file)

    if len(budgets) == 0:
        print("\nNo budgets set.")
        return

    category_expense = {}

    for expense in expenses:

        category = expense["category"]
        amount = expense["amount"]

        if category not in category_expense:
            category_expense[category] = 0

        category_expense[category] += amount

    print("\n========== Budget Status ==========\n")

    print(f"{'Category':<15}{'Spent':<12}{'Budget':<12}{'Status'}")
    print("-" * 60)

    for category, budget in budgets.items():

        spent = category_expense.get(category, 0)

        percentage = (spent / budget) * 100 if budget > 0 else 0

        if percentage >= 100:
            status = "❌ Over Budget"
        elif percentage >= 80:
            status = "⚠ Near Limit"
        else:
            status = "✅ Safe"

        print(f"{category:<15}₹{spent:<10.2f}₹{budget:<10.2f}{status}")

    print("-" * 60)
