import json
from collections import defaultdict
from datetime import datetime, timedelta


# =========================================
# File Paths
# =========================================

INCOME_FILE = "data/income.json"
EXPENSE_FILE = "data/expenses.json"


# =========================================
# Project Constants
# =========================================

DAYS_IN_MONTH = 30
TARGET_SAVINGS_RATE = 0.30
HIGH_VALUE_EXPENSE = 10000
HIGH_CATEGORY_PERCENTAGE = 40
PROGRESS_BAR_WIDTH = 20


# =========================================
# Load Data
# =========================================

def load_data():
    """
    Load income and expense data from JSON files.
    Returns:
        incomes (list)
        expenses (list)
    """

    try:
        with open(INCOME_FILE, "r") as file:
            incomes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        incomes = []

    try:
        with open(EXPENSE_FILE, "r") as file:
            expenses = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []

    return incomes, expenses


# =========================================
# Month Formatter
# =========================================

def format_month(month_string):
    """
    Converts:
        08-2026

    Into:
        August 2026
    """

    try:
        date = datetime.strptime(month_string, "%m-%Y")
        return date.strftime("%B %Y")

    except ValueError:
        return month_string


# =========================================
# Helper Functions
# =========================================

def get_monthly_expenses(expenses):
    """
    Returns:

    {
        '07-2026': 12000,
        '08-2026': 14300
    }
    """

    monthly = defaultdict(float)

    for expense in expenses:

        try:
            month = expense["date"][3:10]
            monthly[month] += expense["amount"]

        except (KeyError, ValueError):
            continue

    return monthly


def get_monthly_income(incomes):
    """
    Returns:

    {
        '07-2026': 25000,
        '08-2026': 27000
    }
    """

    monthly = defaultdict(float)

    for income in incomes:

        try:
            month = income["date"][3:10]
            monthly[month] += income["amount"]

        except (KeyError, ValueError):
            continue

    return monthly


def get_category_totals(expenses):
    """
    Returns total spending per category.
    """

    categories = defaultdict(float)

    for expense in expenses:

        try:
            categories[expense["category"]] += expense["amount"]

        except KeyError:
            continue

    return categories


def get_total_income(incomes):
    """
    Returns total income.
    """

    return sum(
        income.get("amount", 0)
        for income in incomes
    )


def get_total_expense(expenses):
    """
    Returns total expense.
    """

    return sum(
        expense.get("amount", 0)
        for expense in expenses
    )


# =========================================
# Progress Bar
# =========================================

def percentage_bar(percentage):

    filled = int(
        (percentage / 100) * PROGRESS_BAR_WIDTH
    )

    filled = min(filled, PROGRESS_BAR_WIDTH)

    empty = PROGRESS_BAR_WIDTH - filled

    return "█" * filled + "░" * empty


# =========================================
# Monthly Expense Report
# =========================================

def monthly_expense_report(expenses):

    print("\n========== Monthly Expense Report ==========\n")

    monthly_expenses = get_monthly_expenses(expenses)

    if not monthly_expenses:
        print("No expense records found.")
        return

    highest_month = max(monthly_expenses, key=monthly_expenses.get)
    lowest_month = min(monthly_expenses, key=monthly_expenses.get)

    months = sorted(
        monthly_expenses.keys(),
        key=lambda x: datetime.strptime(x, "%m-%Y")
    )

    for month in months:
        print(
            f"{format_month(month):<20}"
            f"₹{monthly_expenses[month]:.2f}"
        )

    print("\n----------------------------------------")
    print(f"Highest Spending Month : {format_month(highest_month)}")
    print(f"Amount                 : ₹{monthly_expenses[highest_month]:.2f}")

    print()

    print(f"Lowest Spending Month  : {format_month(lowest_month)}")
    print(f"Amount                 : ₹{monthly_expenses[lowest_month]:.2f}")


# =========================================
# Monthly Income Report
# =========================================

def monthly_income_report(incomes):

    print("\n========== Monthly Income Report ==========\n")

    monthly_income = get_monthly_income(incomes)

    if not monthly_income:
        print("No income records found.")
        return

    highest_month = max(monthly_income, key=monthly_income.get)
    lowest_month = min(monthly_income, key=monthly_income.get)

    months = sorted(
        monthly_income.keys(),
        key=lambda x: datetime.strptime(x, "%m-%Y")
    )

    for month in months:
        print(
            f"{format_month(month):<20}"
            f"₹{monthly_income[month]:.2f}"
        )

    print("\n----------------------------------------")

    print(f"Highest Income Month : {format_month(highest_month)}")
    print(f"Amount               : ₹{monthly_income[highest_month]:.2f}")

    print()

    print(f"Lowest Income Month  : {format_month(lowest_month)}")
    print(f"Amount               : ₹{monthly_income[lowest_month]:.2f}")


# =========================================
# Category Distribution
# =========================================

def category_distribution(expenses):

    print("\n========== Category Distribution ==========\n")

    if not expenses:
        print("No expense records found.")
        return

    categories = get_category_totals(expenses)

    total_expense = get_total_expense(expenses)

    if total_expense == 0:
        print("No expense records found.")
        return

    sorted_categories = sorted(
        categories.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print(f"{'Category':<18}{'Amount':<15}Percentage")
    print("-" * 65)

    for category, amount in sorted_categories:

        percentage = (amount / total_expense) * 100

        bar = percentage_bar(percentage)

        print(
            f"{category:<18}"
            f"₹{amount:<12.2f}"
            f"{bar} {percentage:5.1f}%"
        )

    print("\n----------------------------------------")
    print(f"Total Expense : ₹{total_expense:.2f}")
    print(f"Categories    : {len(categories)}")

    highest_category = max(categories, key=categories.get)

    print(
        f"Highest Category : {highest_category} "
        f"(₹{categories[highest_category]:.2f})"
    )

# =========================================
# Top Five Expenses
# =========================================

def top_five_expenses(expenses):

    print("\n========== Top 5 Largest Expenses ==========\n")

    if not expenses:
        print("No expense records found.")
        return

    top_expenses = sorted(
        expenses,
        key=lambda expense: expense.get("amount", 0),
        reverse=True
    )[:5]

    for index, expense in enumerate(top_expenses, start=1):

        print(f"{index}. Expense")

        print(f"Amount           : ₹{expense.get('amount',0):.2f}")
        print(f"Category         : {expense.get('category','N/A')}")
        print(f"Payment Method   : {expense.get('payment_method','N/A')}")
        print(f"Date             : {expense.get('date','N/A')}")
        print(f"Notes            : {expense.get('notes','-')}")

        print("-" * 45)


# =========================================
# Daily Average Spending
# =========================================

def daily_average_spending(incomes, expenses):

    print("\n========== Daily Average Spending ==========\n")

    if not expenses:
        print("No expense records found.")
        return

    total_expense = get_total_expense(expenses)

    unique_days = set()

    for expense in expenses:

        try:
            unique_days.add(
                datetime.strptime(
                    expense["date"],
                    "%d-%m-%Y"
                ).date()
            )

        except (KeyError, ValueError):
            continue

    total_days = len(unique_days)

    if total_days == 0:
        print("No valid dates found.")
        return

    daily_average = total_expense / total_days

    total_income = get_total_income(incomes)

    recommended_limit = (
        total_income *
        (1 - TARGET_SAVINGS_RATE)
    ) / DAYS_IN_MONTH

    print(f"Total Expense        : ₹{total_expense:.2f}")
    print(f"Recorded Days        : {total_days}")
    print(f"Daily Average        : ₹{daily_average:.2f}")
    print(f"Recommended Limit    : ₹{recommended_limit:.2f}")

    difference = daily_average - recommended_limit

    print()

    if difference <= 0:

        print("Status : 🟢 Excellent")

        print(
            f"You spend ₹{abs(difference):.2f} "
            "less than your recommended daily limit."
        )

    else:

        print("Status : 🔴 Above Target")

        print(
            f"You spend ₹{difference:.2f} "
            "more than your recommended limit."
        )

        monthly_extra = difference * DAYS_IN_MONTH

        print(
            f"If continued, this could increase "
            f"monthly spending by ₹{monthly_extra:.2f}."
        )


# =========================================
# Biggest Expense
# =========================================

def biggest_expense(expenses):

    print("\n========== Biggest Expense ==========\n")

    if not expenses:
        print("No expense records found.")
        return

    biggest = max(
        expenses,
        key=lambda expense: expense.get("amount", 0)
    )

    print(f"Amount           : ₹{biggest.get('amount',0):.2f}")
    print(f"Category         : {biggest.get('category','N/A')}")
    print(f"Payment Method   : {biggest.get('payment_method','N/A')}")
    print(f"Date             : {biggest.get('date','N/A')}")
    print(f"Notes            : {biggest.get('notes','-')}")

    print("\nInsight")

    if biggest.get("amount", 0) >= HIGH_VALUE_EXPENSE:

        print(
            "This is a high-value transaction.\n"
            "Make sure it was planned and fits your budget."
        )

    else:

        print("No unusually large expense detected.")


# =========================================
# Spending Streak
# =========================================

def spending_streak(expenses):

    print("\n========== Spending Streak ==========\n")

    if not expenses:
        print("No expense records found.")
        return

    dates = set()

    for expense in expenses:

        try:

            dates.add(
                datetime.strptime(
                    expense["date"],
                    "%d-%m-%Y"
                ).date()
            )

        except (KeyError, ValueError):
            continue

    if not dates:
        print("No valid dates found.")
        return

    dates = sorted(dates)

    longest = 1
    current = 1

    for i in range(1, len(dates)):

        if dates[i] == dates[i - 1] + timedelta(days=1):

            current += 1
            longest = max(longest, current)

        else:

            current = 1

    print(f"Longest Streak : {longest} day(s)")

    if longest >= 30:

        print("🏆 Outstanding! You consistently track your expenses.")

    elif longest >= 14:

        print("🟢 Excellent consistency.")

    elif longest >= 7:

        print("🟡 Good habit. Keep it going.")

    else:

        print("🔴 Try recording expenses every day.")
        
# =========================================
# Monthly Trend Analysis
# =========================================

def monthly_trend(expenses):

    print("\n========== Monthly Trend Analysis ==========\n")

    monthly_expenses = get_monthly_expenses(expenses)

    if len(monthly_expenses) < 2:
        print("At least two months of expense data are required.")
        return

    months = sorted(
        monthly_expenses.keys(),
        key=lambda month: datetime.strptime(month, "%m-%Y")
    )

    previous_month = months[-2]
    current_month = months[-1]

    previous_amount = monthly_expenses[previous_month]
    current_amount = monthly_expenses[current_month]

    difference = current_amount - previous_amount

    if previous_amount == 0:
        percentage_change = 0
    else:
        percentage_change = (
            difference / previous_amount
        ) * 100

    print(f"Previous Month : {format_month(previous_month)}")
    print(f"Expense        : ₹{previous_amount:.2f}")

    print()

    print(f"Current Month  : {format_month(current_month)}")
    print(f"Expense        : ₹{current_amount:.2f}")

    print("\n--------------------------------------------")

    if difference > 0:

        print("Trend          : 📈 Increasing")
        print(f"Increase       : ₹{difference:.2f}")
        print(f"Growth         : {percentage_change:.2f}%")

        if percentage_change >= 20:
            print("\nInsight")
            print("Your spending increased significantly.")
            print("Review large or unnecessary purchases.")

        elif percentage_change >= 10:
            print("\nInsight")
            print("Your spending increased moderately.")
            print("Monitor your monthly budget carefully.")

        else:
            print("\nInsight")
            print("A small increase in spending was observed.")

    elif difference < 0:

        print("Trend          : 📉 Decreasing")
        print(f"Reduction      : ₹{abs(difference):.2f}")
        print(f"Decrease       : {abs(percentage_change):.2f}%")

        if abs(percentage_change) >= 20:
            print("\nInsight")
            print("Excellent improvement!")
            print("You reduced your expenses considerably.")

        elif abs(percentage_change) >= 10:
            print("\nInsight")
            print("Good job!")
            print("Your monthly spending has decreased.")

        else:
            print("\nInsight")
            print("A small reduction in spending was observed.")

    else:

        print("Trend          : ➜ Stable")
        print("No change in monthly spending.")

    print("\n--------------------------------------------")

    average_monthly = (
        sum(monthly_expenses.values()) /
        len(monthly_expenses)
    )

    print(f"Average Monthly Expense : ₹{average_monthly:.2f}")

    if current_amount > average_monthly:

        print("Current month is ABOVE your average spending.")

    elif current_amount < average_monthly:

        print("Current month is BELOW your average spending.")

    else:

        print("Current month matches your average spending.")
# =========================================
# Smart Monthly Insights
# =========================================

def smart_monthly_insights(incomes, expenses):

    print("\n========== Smart Monthly Insights ==========\n")

    if not incomes:
        print("No income records found.")
        return

    if not expenses:
        print("No expense records found.")
        return

    total_income = get_total_income(incomes)
    total_expense = get_total_expense(expenses)

    savings = total_income - total_expense

    if total_income == 0:
        savings_rate = 0
    else:
        savings_rate = (savings / total_income) * 100

    print(f"Total Income        : ₹{total_income:.2f}")
    print(f"Total Expense       : ₹{total_expense:.2f}")
    print(f"Net Savings         : ₹{savings:.2f}")
    print(f"Savings Rate        : {savings_rate:.2f}%")

    print("\n--------------------------------------------")
    print("Financial Insights")
    print("--------------------------------------------")

    # =====================================
    # Category Analysis
    # =====================================

    categories = get_category_totals(expenses)

    if categories:

        highest_category = max(
            categories,
            key=categories.get
        )

        highest_amount = categories[highest_category]

        highest_percentage = (
            highest_amount / total_expense
        ) * 100

        print(f"• Highest Spending Category : {highest_category}")
        print(f"  Amount                    : ₹{highest_amount:.2f}")
        print(f"  Share                     : {highest_percentage:.1f}%")

        if highest_percentage >= 40:

            print("  Recommendation:")
            print(f"  Try reducing '{highest_category}' expenses.")

    # =====================================
    # Average Transaction
    # =====================================

    average_transaction = total_expense / len(expenses)

    print()
    print(f"• Average Expense per Transaction")
    print(f"  ₹{average_transaction:.2f}")

    # =====================================
    # Daily Spending
    # =====================================

    unique_days = set()

    for expense in expenses:

        try:
            unique_days.add(
                datetime.strptime(
                    expense["date"],
                    "%d-%m-%Y"
                ).date()
            )

        except (KeyError, ValueError):
            continue

    if unique_days:

        average_daily = (
            total_expense /
            len(unique_days)
        )

        print()
        print(f"• Average Daily Spending")
        print(f"  ₹{average_daily:.2f}")

    # =====================================
    # Savings Health
    # =====================================

    print()

    if savings_rate >= 30:

        print("• Savings Health : Excellent 🟢")
        print("  You are saving more than the recommended 30%.")

    elif savings_rate >= 20:

        print("• Savings Health : Good 🟡")
        print("  You are close to the ideal savings rate.")

    elif savings_rate >= 10:

        print("• Savings Health : Average 🟠")
        print("  Try increasing your monthly savings.")

    else:

        print("• Savings Health : Poor 🔴")
        print("  Your savings are lower than recommended.")

    # =====================================
    # Expense Ratio
    # =====================================

    expense_ratio = (
        total_expense /
        total_income
    ) * 100

    print()
    print(f"• Expense Ratio : {expense_ratio:.1f}%")

    if expense_ratio <= 50:

        print("  Excellent financial control.")

    elif expense_ratio <= 70:

        print("  Spending level is healthy.")

    elif expense_ratio <= 90:

        print("  Spending is becoming high.")

    else:

        print("  Warning! Most of your income is being spent.")

    # =====================================
    # Transaction Analysis
    # =====================================

    print()
    print(f"• Total Transactions : {len(expenses)}")

    if len(expenses) >= 100:

        print("  Large amount of spending activity recorded.")

    elif len(expenses) >= 50:

        print("  Good financial tracking habit.")

    else:

        print("  Keep recording every expense.")

    # =====================================
    # Final Recommendation
    # =====================================

    print("\n--------------------------------------------")
    print("Overall Recommendation")
    print("--------------------------------------------")

    recommendations = []

    if savings_rate < 20:
        recommendations.append(
            "Increase your monthly savings."
        )

    if expense_ratio > 80:
        recommendations.append(
            "Reduce unnecessary monthly expenses."
        )

    if categories:

        if highest_percentage > 40:
            recommendations.append(
                f"Review your '{highest_category}' budget."
            )

    if average_transaction > 5000:
        recommendations.append(
            "Monitor high-value purchases carefully."
        )

    if not recommendations:

        print("Excellent! Your financial habits look healthy.")
        print("Keep tracking your finances consistently.")

    else:

        for index, advice in enumerate(
            recommendations,
            start=1
        ):

            print(f"{index}. {advice}")
# =========================================
# Expense Forecast
# =========================================

def expense_forecast(expenses, incomes):

    print("\n========== Expense Forecast ==========\n")

    if not expenses:
        print("No expense records found.")
        return

    monthly_expenses = get_monthly_expenses(expenses)

    if not monthly_expenses:
        print("No monthly expense data available.")
        return

    months = sorted(
        monthly_expenses.keys(),
        key=lambda month: datetime.strptime(month, "%m-%Y")
    )

    expense_values = [
        monthly_expenses[month]
        for month in months
    ]

    # -------------------------------------
    # Forecast Calculation
    # -------------------------------------

    if len(expense_values) == 1:

        predicted_expense = expense_values[0]

    elif len(expense_values) == 2:

        predicted_expense = (
            expense_values[0] +
            expense_values[1]
        ) / 2

    else:

        predicted_expense = (
            expense_values[-3] * 0.20 +
            expense_values[-2] * 0.30 +
            expense_values[-1] * 0.50
        )

    # -------------------------------------
    # Income Analysis
    # -------------------------------------

    monthly_income = get_monthly_income(incomes)

    if monthly_income:

        average_income = (
            sum(monthly_income.values()) /
            len(monthly_income)
        )

    else:

        average_income = 0

    predicted_savings = (
        average_income -
        predicted_expense
    )

    if average_income == 0:

        savings_rate = 0

    else:

        savings_rate = (
            predicted_savings /
            average_income
        ) * 100

    # -------------------------------------
    # Highest Spending Category
    # -------------------------------------

    categories = get_category_totals(expenses)

    highest_category = max(
        categories,
        key=categories.get
    )

    highest_amount = categories[highest_category]

    suggested_cut = highest_amount * 0.10

    # -------------------------------------
    # Forecast Confidence
    # -------------------------------------

    total_months = len(expense_values)

    if total_months >= 12:

        confidence = "★★★★★ Very High"

    elif total_months >= 6:

        confidence = "★★★★☆ High"

    elif total_months >= 3:

        confidence = "★★★☆☆ Medium"

    else:

        confidence = "★★☆☆☆ Low"

    # -------------------------------------
    # Monthly Trend
    # -------------------------------------

    if len(expense_values) >= 2:

        previous = expense_values[-2]
        latest = expense_values[-1]

        if latest > previous:

            trend = "Increasing 📈"

        elif latest < previous:

            trend = "Decreasing 📉"

        else:

            trend = "Stable ➜"

    else:

        trend = "Insufficient Data"

    # -------------------------------------
    # Budget Risk
    # -------------------------------------

    if average_income == 0:

        risk = "Unknown"

    elif predicted_expense >= average_income:

        risk = "🔴 High"

    elif predicted_expense >= average_income * 0.80:

        risk = "🟡 Medium"

    else:

        risk = "🟢 Low"

    # -------------------------------------
    # Output
    # -------------------------------------

    print(f"Months Analysed          : {total_months}")

    print(f"Forecast Confidence      : {confidence}")

    print(f"Current Trend            : {trend}")

    print()

    print(f"Predicted Expense        : ₹{predicted_expense:.2f}")

    print(f"Average Monthly Income   : ₹{average_income:.2f}")

    print(f"Expected Savings         : ₹{predicted_savings:.2f}")

    print(f"Expected Savings Rate    : {savings_rate:.2f}%")

    print(f"Budget Risk              : {risk}")

    print()

    print(f"Highest Spending Category")

    print(f"Category                 : {highest_category}")

    print(f"Amount                   : ₹{highest_amount:.2f}")

    print(f"Suggested Reduction      : ₹{suggested_cut:.2f}")

    print()

    improved_savings = (
        predicted_savings +
        suggested_cut
    )

    print(f"Estimated Savings After Reduction")

    print(f"₹{improved_savings:.2f}")

    print("\n-------------------------------------------")

    print("AI Recommendation")

    print("-------------------------------------------")

    if predicted_savings < 0:

        print("⚠ Warning!")
        print("Your forecast shows expenses may exceed income.")
        print("Reduce discretionary spending immediately.")

    elif savings_rate < 10:

        print("Savings are expected to remain low.")
        print("Consider lowering non-essential expenses.")

    elif savings_rate < 20:

        print("Your financial position is stable.")
        print("Aim to reach a 30% monthly savings rate.")

    elif savings_rate < 30:

        print("Good financial health.")
        print("A small reduction in spending can further improve savings.")

    else:

        print("Excellent!")
        print("Your finances are expected to remain healthy.")

    print()

    print(
        f"Focus on reducing '{highest_category}' "
        f"expenses by approximately ₹{suggested_cut:.2f} "
        "next month."
    )
# =========================================
# Monthly Analytics Engine
# =========================================

def monthly_summary():

    incomes, expenses = load_data()

    print("\n")
    print("=" * 70)
    print("           INSIGHTSPEND MONTHLY ANALYTICS ENGINE")
    print("=" * 70)

    # -----------------------------------------
    # Data Overview
    # -----------------------------------------

    print("\n📂 DATA OVERVIEW")
    print("-" * 70)

    print(f"Income Records      : {len(incomes)}")
    print(f"Expense Records     : {len(expenses)}")

    total_income = get_total_income(incomes)
    total_expense = get_total_expense(expenses)

    print(f"Total Income        : ₹{total_income:.2f}")
    print(f"Total Expense       : ₹{total_expense:.2f}")
    print(f"Net Savings         : ₹{total_income-total_expense:.2f}")

    # -----------------------------------------
    # Monthly Reports
    # -----------------------------------------

    print("\n" + "=" * 70)
    print("1. MONTHLY REPORTS")
    print("=" * 70)

    monthly_income_report(incomes)

    monthly_expense_report(expenses)

    category_distribution(expenses)

    # -----------------------------------------
    # Expense Analysis
    # -----------------------------------------

    print("\n" + "=" * 70)
    print("2. EXPENSE ANALYSIS")
    print("=" * 70)

    top_five_expenses(expenses)

    daily_average_spending(incomes, expenses)

    biggest_expense(expenses)

    spending_streak(expenses)

    # -----------------------------------------
    # Advanced Analytics
    # -----------------------------------------

    print("\n" + "=" * 70)
    print("3. ADVANCED ANALYTICS")
    print("=" * 70)

    monthly_trend(expenses)

    smart_monthly_insights(incomes, expenses)

    expense_forecast(expenses, incomes)

    # -----------------------------------------
    # Final Financial Report
    # -----------------------------------------

    print("\n" + "=" * 70)
    print("FINAL FINANCIAL REPORT")
    print("=" * 70)

    savings = total_income - total_expense

    if total_income == 0:
        savings_rate = 0
    else:
        savings_rate = (savings / total_income) * 100

    print(f"Monthly Income      : ₹{total_income:.2f}")
    print(f"Monthly Expense     : ₹{total_expense:.2f}")
    print(f"Net Savings         : ₹{savings:.2f}")
    print(f"Savings Rate        : {savings_rate:.2f}%")

    if savings_rate >= 30:

        health = "🟢 Excellent"

    elif savings_rate >= 20:

        health = "🟡 Good"

    elif savings_rate >= 10:

        health = "🟠 Average"

    else:

        health = "🔴 Needs Improvement"

    print(f"Financial Health    : {health}")

    print("\nRecommendation")

    if savings_rate >= 30:

        print("✔ Excellent financial discipline.")
        print("Continue investing and tracking your expenses.")

    elif savings_rate >= 20:

        print("✔ Good financial habits.")
        print("Try increasing your savings to 30%.")

    elif savings_rate >= 10:

        print("✔ You are saving, but there is room for improvement.")
        print("Reduce unnecessary monthly expenses.")

    else:

        print("⚠ Warning!")
        print("Your expenses are consuming most of your income.")
        print("Create a stricter monthly budget.")

    print("\n" + "=" * 70)
    print("      END OF MONTHLY ANALYTICS REPORT")
    print("=" * 70)
