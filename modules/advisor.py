import json

INCOME_FILE = "data/income.json"
EXPENSE_FILE = "data/expenses.json"
BUDGET_FILE = "data/budget.json"


def financial_advisor():

    with open(INCOME_FILE, "r") as file:
        incomes = json.load(file)

    with open(EXPENSE_FILE, "r") as file:
        expenses = json.load(file)

    with open(BUDGET_FILE, "r") as file:
        budgets = json.load(file)

    total_income = sum(item["amount"] for item in incomes)
    total_expense = sum(item["amount"] for item in expenses)
    savings = total_income - total_expense

    print("\n====================================")
    print("      AI FINANCIAL ADVISOR")
    print("====================================")

    print(f"\nTotal Income  : ₹{total_income:.2f}")
    print(f"Total Expense : ₹{total_expense:.2f}")
    print(f"Savings       : ₹{savings:.2f}")

    savings_advice(total_income, savings)

    category_advice(expenses)

    budget_advice(expenses, budgets)

    payment_advice(expenses)

    emergency_fund_advice(savings)

    financial_health_score(total_income, total_expense, expenses, budgets)

    print("\n====================================")

def savings_advice(total_income, savings):

    print("\n------ Savings Analysis ------")

    if total_income == 0:
        print("No income recorded.")
        return

    rate = (savings / total_income) * 100

    print(f"Savings Rate : {rate:.2f}%")

    if rate < 10:
        print("Advice : Your savings are too low.")
        print("Try reducing unnecessary expenses.")

    elif rate < 30:
        print("Advice : Good savings.")
        print("Aim for 30% savings.")

    else:
        print("Excellent! Your savings are healthy.")

def category_advice(expenses):

    print("\n------ Spending Analysis ------")

    if len(expenses) == 0:
        print("No expense data.")
        return

    categories = {}

    for expense in expenses:

        category = expense["category"]

        categories[category] = categories.get(category, 0) + expense["amount"]

    highest = max(categories, key=categories.get)

    print(f"Highest Spending Category : {highest}")
    print(f"Amount : ₹{categories[highest]:.2f}")

    print("Advice : Try reducing spending in this category.")


def budget_advice(expenses, budgets):

    print("\n========== Budget Analysis ==========")

    if len(budgets) == 0:
        print("No budget has been set.")
        return

    category_spending = {}

    for expense in expenses:

        category = expense["category"]

        if category not in category_spending:
            category_spending[category] = 0

        category_spending[category] += expense["amount"]

    for category, budget in budgets.items():

        spent = category_spending.get(category, 0)

        if budget > 0:
            utilization = (spent / budget) * 100
        else:
            utilization = 0

        print("\n--------------------------------------")
        print(f"Category : {category}")
        print(f"Budget   : ₹{budget:.2f}")
        print(f"Spent    : ₹{spent:.2f}")
        print(f"Usage : {progress_bar(utilization)}")

        if utilization <= 80:
            print("Status   : 🟢 Excellent")
            print("Advice   : You are managing this budget well.")

        elif utilization <= 100:
            print("Status   : 🟡 Warning")
            print("Advice   : You are close to your budget limit.")

        else:
            print("Status   : 🔴 Over Budget")
            print(f"Exceeded : ₹{spent-budget:.2f}")
            print("Advice   : Reduce spending in this category.")

# -----------------------------------------
# Financial Health Score
# -----------------------------------------

def financial_health_score(total_income, total_expense, expenses, budgets):

    score = 100

    # ---------------------------------
    # 1. Savings Rate (40 Marks)
    # ---------------------------------

    if total_income == 0:
        savings_rate = 0
    else:
        savings_rate = ((total_income - total_expense) / total_income) * 100

    if savings_rate >= 30:
        score += 0

    elif savings_rate >= 20:
        score -= 5

    elif savings_rate >= 10:
        score -= 15

    else:
        score -= 30

    # ---------------------------------
    # 2. Budget Utilization (30 Marks)
    # ---------------------------------

    category_spending = {}

    for expense in expenses:

        category = expense["category"]

        category_spending[category] = (
            category_spending.get(category, 0)
            + expense["amount"]
        )

    for category, budget in budgets.items():

        spent = category_spending.get(category, 0)

        if budget == 0:
            continue

        utilization = (spent / budget) * 100

        if utilization > 100:
            score -= 5

        elif utilization > 80:
            score -= 2

    # ---------------------------------
    # 3. Expense Ratio (30 Marks)
    # ---------------------------------

    if total_income > 0:

        expense_ratio = (total_expense / total_income) * 100

        if expense_ratio > 90:
            score -= 20

        elif expense_ratio > 80:
            score -= 10

        elif expense_ratio > 70:
            score -= 5

    # ---------------------------------
    # Limit Score
    # ---------------------------------

    if score < 0:
        score = 0

    if score > 100:
        score = 100

    # ---------------------------------
    # Display Result
    # ---------------------------------

    print("\n========== Financial Health Score ==========\n")

    print(f"Score : {score}/100")

    if score >= 90:
        print("Grade : A+ 🌟")
        print("Excellent financial health.")

    elif score >= 75:
        print("Grade : A")
        print("Your finances are in good condition.")

    elif score >= 60:
        print("Grade : B")
        print("There is room for improvement.")

    elif score >= 40:
        print("Grade : C")
        print("Control your expenses and improve savings.")

    else:
        print("Grade : D")
        print("Your finances need immediate attention.")

    return score
