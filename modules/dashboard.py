import json
from datetime import datetime

from utils.formatter import progress_bar
from modules.advisor import financial_health_score

INCOME_FILE = "data/income.json"
EXPENSE_FILE = "data/expenses.json"
BUDGET_FILE = "data/budget.json"


def show_dashboard():

    with open(INCOME_FILE) as file:
        incomes = json.load(file)

    with open(EXPENSE_FILE) as file:
        expenses = json.load(file)

    with open(BUDGET_FILE) as file:
        budgets = json.load(file)

    total_income = sum(i["amount"] for i in incomes)
    total_expense = sum(e["amount"] for e in expenses)

    savings = total_income-total_expense

    if total_income == 0:
        savings_rate = 0
    else:
        savings_rate = savings/total_income*100

    score = financial_health_score(
        total_income,
        total_expense,
        expenses,
        budgets
    )

    print("="*60)
    print("         INSIGHTSPEND AI DASHBOARD")
    print("="*60)

    print(datetime.now().strftime("%d-%m-%Y"))

    print("-"*60)

    print(f"Income       ₹{total_income:.2f}")
    print(f"Expense      ₹{total_expense:.2f}")
    print(f"Savings      ₹{savings:.2f}")
    print(f"Rate         {savings_rate:.2f}%")
    print(f"Score        {score}/100")

    print("-"*60)

    category_spending = {}

    for expense in expenses:

        category = expense["category"]

        category_spending[category] = (
            category_spending.get(category,0)
            + expense["amount"]
        )

    print("\nBudget Health\n")

    for category,budget in budgets.items():

        spent = category_spending.get(category,0)

        if budget==0:
            utilization=0
        else:
            utilization=spent/budget*100

        print(f"{category:<15}{progress_bar(utilization)}")

    print("="*60)
