import json
import hashlib
from pathlib import Path


IMPORT_HISTORY_FILE = Path("data/import_history.json")


def normalize_text(value):
    """
    Normalize text so small formatting differences
    do not create different fingerprints.
    """

    if value is None:
        return ""

    return " ".join(
        str(value).strip().lower().split()
    )


def create_transaction_fingerprint(transaction):
    """
    Create a stable unique fingerprint for a transaction.

    Uses:
    - date
    - transaction_id
    - description
    - amount
    - type
    """

    date = normalize_text(
        transaction.get("date")
    )

    transaction_id = normalize_text(
        transaction.get("transaction_id")
    )

    description = normalize_text(
        transaction.get("description")
    )

    amount = transaction.get(
        "amount",
        0
    )

    transaction_type = normalize_text(
        transaction.get("type")
    )

    fingerprint_source = (
        f"{date}|"
        f"{transaction_id}|"
        f"{description}|"
        f"{float(amount):.2f}|"
        f"{transaction_type}"
    )

    return hashlib.sha256(
        fingerprint_source.encode("utf-8")
    ).hexdigest()


def load_import_history():
    """
    Load fingerprints of previously imported transactions.
    """

    if not IMPORT_HISTORY_FILE.exists():
        return []

    try:

        with open(
            IMPORT_HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (
        json.JSONDecodeError,
        OSError
    ):
        return []


def save_import_history(history):
    """
    Save transaction fingerprints.
    """

    IMPORT_HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        IMPORT_HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


def is_duplicate(transaction, history=None):
    """
    Check whether a transaction was previously imported.
    """

    if history is None:
        history = load_import_history()

    fingerprint = (
        create_transaction_fingerprint(
            transaction
        )
    )

    return fingerprint in history


def filter_duplicates(transactions):
    """
    Separate new transactions from duplicates.

    Returns:
        new_transactions,
        duplicate_transactions
    """

    history = load_import_history()

    new_transactions = []
    duplicate_transactions = []

    current_batch_fingerprints = set()

    for transaction in transactions:

        fingerprint = (
            create_transaction_fingerprint(
                transaction
            )
        )

        already_imported = (
            fingerprint in history
        )

        duplicated_in_same_batch = (
            fingerprint
            in current_batch_fingerprints
        )

        if (
            already_imported
            or duplicated_in_same_batch
        ):

            transaction[
                "duplicate_status"
            ] = True

            duplicate_transactions.append(
                transaction
            )

        else:

            transaction[
                "duplicate_status"
            ] = False

            new_transactions.append(
                transaction
            )

            current_batch_fingerprints.add(
                fingerprint
            )

    return (
        new_transactions,
        duplicate_transactions
    )


def register_imported_transactions(transactions):
    """
    Save fingerprints after transactions are
    successfully written to InsightSpend.

    IMPORTANT:
    Call this only AFTER actual saving succeeds.
    """

    history = load_import_history()

    history_set = set(history)

    added_count = 0

    for transaction in transactions:

        fingerprint = (
            create_transaction_fingerprint(
                transaction
            )
        )

        if fingerprint not in history_set:

            history.append(
                fingerprint
            )

            history_set.add(
                fingerprint
            )

            added_count += 1

    save_import_history(
        history
    )

    return added_count


def print_duplicate_summary(
    new_transactions,
    duplicate_transactions
):
    """
    Display duplicate detection result.
    """

    print("\n" + "=" * 70)
    print("             DUPLICATE DETECTION")
    print("=" * 70)

    print(
        f"New transactions       : "
        f"{len(new_transactions)}"
    )

    print(
        f"Duplicate transactions : "
        f"{len(duplicate_transactions)}"
    )

    if duplicate_transactions:

        print("\nDuplicates skipped:")

        for transaction in (
            duplicate_transactions
        ):

            print(
                f"- {transaction.get('date')} | "
                f"{transaction.get('transaction_id')} | "
                f"₹{transaction.get('amount', 0):.2f} | "
                f"{transaction.get('description')}"
            )

    print("=" * 70)


if __name__ == "__main__":

    sample_transactions = [
        {
            "date": "17-07-2026",
            "transaction_id": "S96204400",
            "description": "UPI TEST PAYMENT",
            "amount": 300.0,
            "type": "expense"
        },
        {
            "date": "17-07-2026",
            "transaction_id": "S96204400",
            "description": "UPI TEST PAYMENT",
            "amount": 300.0,
            "type": "expense"
        },
        {
            "date": "21-08-2026",
            "transaction_id": "S39943432",
            "description": "UPI TEST CREDIT",
            "amount": 1000.0,
            "type": "income"
        }
    ]

    new_transactions, duplicates = (
        filter_duplicates(
            sample_transactions
        )
    )

    print_duplicate_summary(
        new_transactions,
        duplicates
    )