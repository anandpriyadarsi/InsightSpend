import json
import os


INCOME_FILE = "data/income.json"
EXPENSE_FILE = "data/expenses.json"


def load_json_file(filename):
    """Load a JSON list safely."""

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_json_file(filename, data):
    """Save data safely to JSON."""

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def convert_to_expense(transaction):
    """Convert imported bank transaction to InsightSpend expense format."""

    return {
        "amount": float(transaction["amount"]),
        "category": transaction.get("category", "Uncategorized"),
        "payment_method": transaction.get("payment_method", "Bank/UPI"),
        "date": transaction.get("date", ""),
        "notes": transaction.get("description", "")
    }


def convert_to_income(transaction):
    """Convert imported bank transaction to InsightSpend income format."""

    return {
        "amount": float(transaction["amount"]),
        "source": transaction.get("category", "Bank Credit"),
        "date": transaction.get("date", ""),
        "notes": transaction.get("description", "")
    }


def save_imported_transactions(transactions):
    """
    Save reviewed bank transactions into InsightSpend.

    Expenses -> data/expenses.json
    Income   -> data/income.json
    """

    incomes = load_json_file(INCOME_FILE)
    expenses = load_json_file(EXPENSE_FILE)

    income_count = 0
    expense_count = 0
    skipped_count = 0
    saved_transactions = []

    for transaction in transactions:

        transaction_type = str(
            transaction.get("type", "")
        ).strip().lower()

        try:

            if transaction_type == "expense":

                expense = convert_to_expense(transaction)
                expenses.append(expense)

                expense_count += 1
                saved_transactions.append(transaction)

            elif transaction_type == "income":

                income = convert_to_income(transaction)
                incomes.append(income)

                income_count += 1
                saved_transactions.append(transaction)

            else:
                skipped_count += 1

        except (KeyError, TypeError, ValueError):
            skipped_count += 1

    # Save only after processing all transactions
    save_json_file(INCOME_FILE, incomes)
    save_json_file(EXPENSE_FILE, expenses)

    print("\n" + "=" * 60)
    print("              IMPORT SAVE SUMMARY")
    print("=" * 60)

    print(f"Income imported   : {income_count}")
    print(f"Expenses imported : {expense_count}")
    print(f"Skipped           : {skipped_count}")
    print(f"Total saved       : {len(saved_transactions)}")

    print("=" * 60)

    return saved_transactions