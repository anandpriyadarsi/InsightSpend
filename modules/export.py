import json
import csv
import os
from datetime import datetime

EXPENSE_FILE = "data/expenses.json"


def export_expenses_csv():

    with open(EXPENSE_FILE, "r") as file:
        expenses = json.load(file)

    if len(expenses) == 0:
        print("\nNo expense records found.")
        return
    filename = "expenses_" + datetime.now().strftime("%Y-%m-%d") + ".csv"
    with open("expenses.csv", "w", newline="") as csv_file:

        writer = csv.writer(csv_file)

        # Header
        writer.writerow([
            "Amount",
            "Category",
            "Payment Method",
            "Date",
            "Notes"
        ])

        # Data
        for expense in expenses:

            writer.writerow([
                expense["amount"],
                expense["category"],
                expense["payment_method"],
                expense["date"],
                expense["notes"]
            ])

    print("\nExpenses exported successfully!")
    print("File Name : expenses.csv")
def import_expenses_csv():

    csv_file = "expenses.csv"

    if not os.path.exists(csv_file):
        print("\nCSV file not found!")
        return

    expenses = []

    with open(csv_file, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            expense = {
                "amount": float(row["Amount"]),
                "category": row["Category"],
                "payment_method": row["Payment Method"],
                "date": row["Date"],
                "notes": row["Notes"]
            }

            expenses.append(expense)
    with open(EXPENSE_FILE, "r") as file:
         existing_expenses = json.load(file)
    existing_expenses.extend(expenses)

    with open(EXPENSE_FILE, "w") as file:
        json.dump(existing_expenses, file, indent=4)


    print("\nExpenses imported successfully!")
