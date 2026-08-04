def print_heading(title):

    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def print_subheading(title):

    print("\n" + "-" * 40)
    print(title)
    print("-" * 40)


def currency(amount):

    return f"₹{amount:.2f}"


def progress_bar(percentage):

    total_blocks = 20

    if percentage <= 100:
        filled_blocks = int((percentage / 100) * total_blocks)
    else:
        filled_blocks = total_blocks

    empty_blocks = total_blocks - filled_blocks

    bar = "█" * filled_blocks + "░" * empty_blocks

    if percentage <= 80:
        status = "🟢"

    elif percentage <= 100:
        status = "🟡"

    else:
        status = "🔴"

    if percentage > 100:

        extra = percentage - 100

        return f"{status} [{bar}] {percentage:.1f}% (+{extra:.1f}%)"

    return f"{status} [{bar}] {percentage:.1f}%"
