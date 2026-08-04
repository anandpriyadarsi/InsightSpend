import json
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

INCOME_FILE = "data/income.json"
EXPENSE_FILE = "data/expenses.json"
BUDGET_FILE = "data/budget.json"


def generate_report():

    # -------------------------
    # Read Data
    # -------------------------

    with open(INCOME_FILE, "r") as file:
        incomes = json.load(file)

    with open(EXPENSE_FILE, "r") as file:
        expenses = json.load(file)

    with open(BUDGET_FILE, "r") as file:
        budgets = json.load(file)

    # -------------------------
    # Calculations
    # -------------------------

    total_income = sum(item["amount"] for item in incomes)

    total_expense = sum(item["amount"] for item in expenses)

    savings = total_income - total_expense

    if total_income > 0:
        savings_rate = (savings / total_income) * 100
    else:
        savings_rate = 0

    # -------------------------
    # Spending By Category
    # -------------------------

    categories = {}

    for expense in expenses:

        category = expense["category"]

        if category not in categories:
            categories[category] = 0

        categories[category] += expense["amount"]

    # -------------------------
    # Highest Expense
    # -------------------------

    highest = None

    if len(expenses) > 0:
        highest = max(expenses, key=lambda x: x["amount"])

    # -------------------------
    # Create PDF
    # -------------------------

    doc = SimpleDocTemplate("InsightSpend_Report.pdf")

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "InsightSpend Financial Report",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            datetime.now().strftime("%d-%m-%Y %H:%M"),
            styles["Normal"]
        )
    )

    story.append(
        Paragraph("<br/><b>Income Summary</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"Total Income : ₹{total_income:.2f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph("<br/><b>Expense Summary</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"Total Expense : ₹{total_expense:.2f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Savings : ₹{savings:.2f}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Savings Rate : {savings_rate:.2f}%",
            styles["BodyText"]
        )
    )

    # -------------------------
    # Budget Section
    # -------------------------

    story.append(
        Paragraph("<br/><b>Monthly Budgets</b>", styles["Heading2"])
    )

    if len(budgets) == 0:

        story.append(
            Paragraph(
                "No Budget Set",
                styles["BodyText"]
            )
        )

    else:

        for category, amount in budgets.items():

            story.append(
                Paragraph(
                    f"{category} : ₹{amount:.2f}",
                    styles["BodyText"]
                )
            )

    # -------------------------
    # Category Analysis
    # -------------------------

    story.append(
        Paragraph("<br/><b>Spending By Category</b>", styles["Heading2"])
    )

    if len(categories) == 0:

        story.append(
            Paragraph(
                "No Expense Records",
                styles["BodyText"]
            )
        )

    else:

        for category, amount in categories.items():

            story.append(
                Paragraph(
                    f"{category} : ₹{amount:.2f}",
                    styles["BodyText"]
                )
            )

    # -------------------------
    # Highest Expense
    # -------------------------

    story.append(
        Paragraph("<br/><b>Highest Expense</b>", styles["Heading2"])
    )

    if highest:

        story.append(
            Paragraph(
                f"₹{highest['amount']:.2f} ({highest['category']})",
                styles["BodyText"]
            )
        )

    else:

        story.append(
            Paragraph(
                "No Expenses Recorded",
                styles["BodyText"]
            )
        )

    # -------------------------
    # Smart Insights
    # -------------------------

    story.append(
        Paragraph("<br/><b>Smart Insights</b>", styles["Heading2"])
    )

    if total_income == 0:

        story.append(
            Paragraph(
                "No income recorded.",
                styles["BodyText"]
            )
        )

    else:

        story.append(
            Paragraph(
                f"You saved ₹{savings:.2f}.",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Your Savings Rate is {savings_rate:.2f}%.",
                styles["BodyText"]
            )
        )

        if len(categories) > 0:

            highest_category = max(categories, key=categories.get)

            percent = (categories[highest_category] / total_expense) * 100

            story.append(
                Paragraph(
                    f"You spent {percent:.1f}% on {highest_category}.",
                    styles["BodyText"]
                )
            )

    # -------------------------
    # Footer
    # -------------------------

    story.append(
        Paragraph("<br/><br/>Generated by InsightSpend", styles["Heading3"])
    )

    doc.build(story)

    print("\nPDF Generated Successfully!")
