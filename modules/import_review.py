from modules.categorizer import save_personal_rule


def show_transaction(transaction, index, total):
    """
    Display one transaction clearly for review.
    """

    print("\n" + "=" * 70)
    print(f"TRANSACTION {index} OF {total}")
    print("=" * 70)

    print(f"Date        : {transaction.get('date')}")
    print(f"Transaction : {transaction.get('transaction_id')}")
    print(f"Description : {transaction.get('description')}")
    print(f"Amount      : ₹{transaction.get('amount', 0):.2f}")
    print(f"Type        : {transaction.get('type', '').title()}")
    print(f"Category    : {transaction.get('category')}")
    print(
        f"Confidence  : "
        f"{transaction.get('category_confidence', 'Unknown')}"
    )
    print(
        f"Reason      : "
        f"{transaction.get('category_reason', 'Not available')}"
    )

    balance = transaction.get("balance")

    if balance is not None:
        print(f"Balance     : ₹{balance:.2f}")


def edit_category(transaction):
    """
    Allow user to manually change transaction category.
    """

    print("\nCurrent category:", transaction.get("category"))

    new_category = input(
        "Enter new category: "
    ).strip()

    if not new_category:
        print("Category unchanged.")
        return transaction

    transaction["category"] = new_category
    transaction["category_confidence"] = "Manual"
    transaction["category_reason"] = "Changed manually by user"
    transaction["manually_modified"] = True

    print(f"Category changed to: {new_category}")

    return transaction


def learn_category_rule(transaction):
    """
    Save a personal keyword rule based on user's correction.
    """

    description = transaction.get(
        "description",
        ""
    )

    if not description:
        print("No description available.")
        return

    print("\nDescription:")
    print(description)

    keyword = input(
        "\nEnter keyword/merchant name to remember "
        "for this category: "
    ).strip()

    if not keyword:
        print("Rule not saved.")
        return

    category = transaction.get("category")

    saved = save_personal_rule(
        keyword,
        category
    )

    if saved:
        print(
            f"Learned rule: '{keyword}' "
            f"→ '{category}'"
        )
    else:
        print("Could not save rule.")


def edit_transaction(transaction):
    """
    Allow user to modify editable transaction fields.
    """

    while True:

        print("\nEDIT TRANSACTION")
        print("-" * 40)

        print("1. Change category")
        print("2. Change amount")
        print("3. Change type")
        print("4. Change description")
        print("5. Finish editing")

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            old_category = transaction.get(
                "category"
            )

            transaction = edit_category(
                transaction
            )

            if (
                transaction.get("category")
                != old_category
            ):

                remember = input(
                    "\nRemember this correction "
                    "for future transactions? (y/n): "
                ).strip().lower()

                if remember == "y":
                    learn_category_rule(
                        transaction
                    )

        elif choice == "2":

            try:

                new_amount = float(
                    input(
                        "Enter new amount: ₹"
                    ).strip()
                )

                if new_amount <= 0:
                    print(
                        "Amount must be greater than 0."
                    )
                    continue

                transaction["amount"] = (
                    new_amount
                )

                transaction[
                    "manually_modified"
                ] = True

                print("Amount updated.")

            except ValueError:
                print(
                    "Please enter a valid number."
                )

        elif choice == "3":

            new_type = input(
                "Enter type "
                "(income/expense): "
            ).strip().lower()

            if new_type not in [
                "income",
                "expense"
            ]:

                print(
                    "Type must be income "
                    "or expense."
                )

                continue

            transaction["type"] = new_type

            transaction[
                "manually_modified"
            ] = True

            print("Transaction type updated.")

        elif choice == "4":

            new_description = input(
                "Enter new description: "
            ).strip()

            if not new_description:
                print(
                    "Description unchanged."
                )
                continue

            transaction[
                "description"
            ] = new_description

            transaction[
                "manually_modified"
            ] = True

            print("Description updated.")

        elif choice == "5":
            break

        else:
            print(
                "Invalid option. "
                "Please choose 1-5."
            )

    return transaction


def review_transactions(transactions):
    """
    Review categorized transactions before saving.

    Returns:
        approved_transactions
    """

    approved_transactions = []

    total = len(transactions)

    if total == 0:
        print(
            "\nNo transactions available "
            "for review."
        )
        return approved_transactions

    print("\n" + "=" * 70)
    print("          IMPORTED TRANSACTION REVIEW")
    print("=" * 70)

    index = 0

    while index < total:

        transaction = transactions[index]

        show_transaction(
            transaction,
            index + 1,
            total
        )

        print("\nActions")
        print("-" * 40)

        print("[A] Accept")
        print("[E] Edit")
        print("[S] Skip")
        print("[R] Accept remaining")
        print("[Q] Cancel import")

        choice = input(
            "\nChoose action: "
        ).strip().lower()

        if choice == "a":

            transaction[
                "import_status"
            ] = "approved"

            approved_transactions.append(
                transaction
            )

            print("Transaction approved.")

            index += 1

        elif choice == "e":

            transaction = edit_transaction(
                transaction
            )

            transactions[index] = (
                transaction
            )

        elif choice == "s":

            transaction[
                "import_status"
            ] = "skipped"

            print("Transaction skipped.")

            index += 1

        elif choice == "r":

            for remaining in (
                transactions[index:]
            ):

                remaining[
                    "import_status"
                ] = "approved"

                approved_transactions.append(
                    remaining
                )

            print(
                "\nAll remaining transactions "
                "approved."
            )

            break

        elif choice == "q":

            confirm = input(
                "Cancel entire import? "
                "(y/n): "
            ).strip().lower()

            if confirm == "y":

                print(
                    "\nImport cancelled."
                )

                return []

        else:

            print(
                "Invalid option. "
                "Choose A, E, S, R or Q."
            )

    print("\n" + "=" * 70)
    print("REVIEW COMPLETE")
    print("=" * 70)

    print(
        f"Approved transactions : "
        f"{len(approved_transactions)}"
    )

    print(
        f"Skipped transactions  : "
        f"{total - len(approved_transactions)}"
    )

    print("=" * 70)

    return approved_transactions