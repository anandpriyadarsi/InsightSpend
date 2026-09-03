import json
import hashlib
import os
import hmac

USER_FILE = "data/user.json"


def hash_password(password, salt=None):
    """
    Convert a password into a secure PBKDF2 hash.
    """

    if salt is None:
        salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex(), password_hash.hex()


def verify_password(password, stored_salt, stored_hash):
    """
    Check whether the entered password matches the stored hash.
    """

    salt = bytes.fromhex(stored_salt)

    _, calculated_hash = hash_password(password, salt)

    return hmac.compare_digest(calculated_hash, stored_hash)


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
        password = input("Password : ")

        username_correct = username == user["username"]

        password_correct = verify_password(
            password,
            user["salt"],
            user["password_hash"]
        )

        if username_correct and password_correct:

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