from datetime import datetime


# -----------------------------------------
# Validate Amount
# -----------------------------------------

def validate_amount(amount):

    try:

        amount = float(amount)

        if amount <= 0:
            return False, "Amount must be greater than zero."

        return True, amount

    except ValueError:

        return False, "Please enter a valid number."


# -----------------------------------------
# Validate Date
# Format : DD-MM-YYYY
# -----------------------------------------

def validate_date(date):

    try:

        datetime.strptime(date, "%d-%m-%Y")

        return True, date

    except ValueError:

        return False, "Date must be in DD-MM-YYYY format."


# -----------------------------------------
# Validate Menu Choice
# -----------------------------------------

def validate_menu_choice(choice, minimum, maximum):

    try:

        choice = int(choice)

        if minimum <= choice <= maximum:

            return True, choice

        return False, "Invalid menu option."

    except ValueError:

        return False, "Please enter a number."


# -----------------------------------------
# Validate Username
# -----------------------------------------

def validate_username(username):

    username = username.strip()

    if len(username) < 4:

        return False, "Username must contain at least 4 characters."

    if " " in username:

        return False, "Username cannot contain spaces."

    return True, username


# -----------------------------------------
# Validate Password
# -----------------------------------------

def validate_password(password):

    if len(password) < 6:

        return False, "Password must contain at least 6 characters."

    return True, password


# -----------------------------------------
# Validate Category
# -----------------------------------------

def validate_category(category):

    category = category.strip().title()

    if category == "":

        return False, "Category cannot be empty."

    return True, category


# -----------------------------------------
# Validate Payment Method
# -----------------------------------------

def validate_payment_method(method):

    allowed = [
        "Cash",
        "UPI",
        "Card",
        "Bank Transfer",
        "Wallet"
    ]

    method = method.strip().title()

    if method not in allowed:

        return False, "Invalid payment method."

    return True, method


# -----------------------------------------
# Validate Goal Amount
# -----------------------------------------

def validate_goal_amount(amount):

    return validate_amount(amount)


# -----------------------------------------
# Validate Percentage
# -----------------------------------------

def validate_percentage(value):

    try:

        value = float(value)

        if 0 <= value <= 100:

            return True, value

        return False, "Percentage must be between 0 and 100."

    except ValueError:

        return False, "Invalid percentage."


# -----------------------------------------
# Validate Yes / No
# -----------------------------------------

def validate_yes_no(choice):

    choice = choice.strip().lower()

    if choice in ["y", "yes"]:

        return True, True

    if choice in ["n", "no"]:

        return True, False

    return False, "Please enter Yes or No."


# -----------------------------------------
# Validate Search Text
# -----------------------------------------

def validate_text(text):

    text = text.strip()

    if text == "":

        return False, "Input cannot be empty."

    return True, text
