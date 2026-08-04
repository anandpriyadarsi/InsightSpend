import json

USER_FILE = "data/user.json"


# -------------------------------
# Load User
# -------------------------------

def load_user():

    with open(USER_FILE, "r") as file:
        return json.load(file)


# -------------------------------
# Save User
# -------------------------------

def save_user(user):

    with open(USER_FILE, "w") as file:
        json.dump(user, file, indent=4)


# -------------------------------
# Change Username
# -------------------------------

def change_username():

    user = load_user()

    print("\n===== Change Username =====")

    current = input("Current Username : ")

    if current != user["username"]:
        print("Incorrect Username.")
        return

    new_username = input("New Username : ")

    user["username"] = new_username

    save_user(user)

    print("Username Updated Successfully.")


# -------------------------------
# Change Password
# -------------------------------

def change_password():

    user = load_user()

    print("\n===== Change Password =====")

    current = input("Current Password : ")

    if current != user["password"]:
        print("Incorrect Password.")
        return

    new_password = input("New Password : ")

    confirm = input("Confirm Password : ")

    if new_password != confirm:

        print("Passwords do not match.")
        return

    user["password"] = new_password

    save_user(user)

    print("Password Updated Successfully.")


# -------------------------------
# View Account
# -------------------------------

def view_account():

    user = load_user()

    print("\n========== ACCOUNT ==========")

    print(f"Username : {user['username']}")

    print("Password : " + "*" * len(user["password"]))


# -------------------------------
# Account Menu
# -------------------------------

def account_menu():

    while True:

        print("\n==============================")
        print("     ACCOUNT MANAGEMENT")
        print("==============================")
        print("1. View Account")
        print("2. Change Username")
        print("3. Change Password")
        print("4. Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            view_account()

        elif choice == "2":

            change_username()

        elif choice == "3":

            change_password()

        elif choice == "4":

            break

        else:

            print("Invalid Choice.")
