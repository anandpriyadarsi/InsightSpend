import json

USER_FILE = "data/user.json"


def login():

    try:
        with open(USER_FILE, "r") as file:
            user = json.load(file)

    except FileNotFoundError:
        print("\nUser database not found.")
        return False

    except json.JSONDecodeError:
        print("\nUser database is corrupted.")
        return False

    MAX_ATTEMPTS = 3
    attempts = 0

    print("=" * 50)
    print("         INSIGHTSPEND LOGIN")
    print("=" * 50)

    while attempts < MAX_ATTEMPTS:

        print(f"\nAttempts Remaining : {MAX_ATTEMPTS - attempts}")

        username = input("Username : ").strip()
        password = input("Password : ").strip()

        if (
            username == user["username"] and
            password == user["password"]
        ):

            print("\n" + "=" * 50)
            print("Login Successful!")
            print(f"Welcome, {username}")
            print("=" * 50)

            return True

        attempts += 1

        if attempts < MAX_ATTEMPTS:
            print("\nIncorrect username or password. Please try again.")

    print("\n" + "=" * 50)
    print("Too many failed login attempts.")
    print("Program Closed.")
    print("=" * 50)

    return False
