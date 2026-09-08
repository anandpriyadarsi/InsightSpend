import json
from pathlib import Path


RULES_FILE = Path("data/category_rules.json")


DEFAULT_RULES = {
    "Food": [
        "swiggy",
        "zomato",
        "restaurant",
        "cafe",
        "mess",
        "food"
    ],

    "Transport": [
        "uber",
        "ola",
        "rapido",
        "irctc",
        "railway",
        "metro"
    ],

    "Shopping": [
        "amazon",
        "flipkart",
        "myntra",
        "meesho"
    ],

    "Education": [
        "udemy",
        "coursera",
        "book",
        "college",
        "school",
        "course"
    ],

    "Software / Subscription": [
        "openai",
        "chatgpt",
        "google one",
        "microsoft",
        "github",
        "notion"
    ],

    "Recharge / Bills": [
        "jio",
        "airtel",
        "vi ",
        "bsnl",
        "electricity",
        "recharge",
        "broadband"
    ],

    "Cash Withdrawal": [
        "atm",
        "withdrawal",
        "cash withdrawal"
    ],

    "Salary / Scholarship": [
        "salary",
        "scholarship",
        "stipend"
    ],

    "Cashback / Rewards": [
        "cashback",
        "reward",
        "rewards",
        "navi limit"
    ]
}


def load_personal_rules():
    """
    Load user-created categorization rules.

    Example:
    {
        "pramod": "Family Transfer"
    }
    """

    if not RULES_FILE.exists():
        return {}

    try:
        with open(RULES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def save_personal_rule(keyword, category):
    """
    Save a rule learned from a user's manual correction.
    """

    rules = load_personal_rules()

    keyword = keyword.strip().lower()
    category = category.strip()

    if not keyword or not category:
        return False

    rules[keyword] = category

    RULES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(RULES_FILE, "w", encoding="utf-8") as file:
        json.dump(
            rules,
            file,
            indent=4
        )

    return True


def categorize_transaction(description, transaction_type):
    """
    Predict category using:

    1. Personal rules
    2. Default keyword rules
    3. Transaction type fallback
    """

    if description is None:
        description = ""

    description_lower = str(description).lower()

    # --------------------------------
    # 1. Personal rules
    # --------------------------------

    personal_rules = load_personal_rules()

    for keyword, category in personal_rules.items():

        if keyword.lower() in description_lower:

            return {
                "category": category,
                "confidence": "High",
                "reason": f"Matched personal rule: {keyword}"
            }

    # --------------------------------
    # 2. Default rules
    # --------------------------------

    for category, keywords in DEFAULT_RULES.items():

        for keyword in keywords:

            if keyword.lower() in description_lower:

                return {
                    "category": category,
                    "confidence": "Medium",
                    "reason": f"Matched keyword: {keyword}"
                }

    # --------------------------------
    # 3. Fallback
    # --------------------------------

    if transaction_type == "income":

        return {
            "category": "Other Income",
            "confidence": "Low",
            "reason": "No keyword matched"
        }

    return {
        "category": "Uncategorized",
        "confidence": "Low",
        "reason": "No keyword matched"
    }


def apply_categories(transactions):
    """
    Add predicted category information
    to a list of transactions.
    """

    categorized_transactions = []

    for transaction in transactions:

        prediction = categorize_transaction(
            transaction.get("description"),
            transaction.get("type")
        )

        transaction["category"] = prediction["category"]
        transaction["category_confidence"] = prediction["confidence"]
        transaction["category_reason"] = prediction["reason"]

        categorized_transactions.append(
            transaction
        )

    return categorized_transactions


if __name__ == "__main__":

    test_transactions = [
        {
            "description": "UPI payment to Swiggy",
            "type": "expense"
        },
        {
            "description": "UPI OpenAI LLC",
            "type": "expense"
        },
        {
            "description": "NAVI LIMIT rewards",
            "type": "income"
        },
        {
            "description": "UPI transfer to unknown person",
            "type": "expense"
        }
    ]

    results = apply_categories(
        test_transactions
    )

    print("\nCATEGORY TEST")
    print("=" * 60)

    for transaction in results:

        print(
            f"\nDescription : {transaction['description']}"
        )

        print(
            f"Type        : {transaction['type']}"
        )

        print(
            f"Category    : {transaction['category']}"
        )

        print(
            f"Confidence  : {transaction['category_confidence']}"
        )

        print(
            f"Reason      : {transaction['category_reason']}"
        )