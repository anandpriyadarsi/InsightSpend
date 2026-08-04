from datetime import datetime
import os

LOG_FILE = "data/activity_log.txt"


# -----------------------------------------
# Create Log File
# -----------------------------------------

def create_log_file():

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w") as file:

            file.write("========== InsightSpend Activity Log ==========\n")


# -----------------------------------------
# Write Log
# -----------------------------------------

def write_log(action, details=""):

    create_log_file()

    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open(LOG_FILE, "a") as file:

        file.write(
            f"[{time}] "
            f"{action}"
        )

        if details != "":

            file.write(f" : {details}")

        file.write("\n")


# -----------------------------------------
# View Log
# -----------------------------------------

def view_logs():

    create_log_file()

    print("\n")
    print("=" * 70)
    print("              ACTIVITY LOG")
    print("=" * 70)

    with open(LOG_FILE, "r") as file:

        logs = file.readlines()

    if len(logs) == 1:

        print("No activity found.")
        return

    for log in logs:

        print(log.strip())


# -----------------------------------------
# Clear Log
# -----------------------------------------

def clear_logs():

    choice = input(
        "Delete all activity logs? (Y/N): "
    ).lower()

    if choice == "y":

        with open(LOG_FILE, "w") as file:

            file.write(
                "========== InsightSpend Activity Log ==========\n"
            )

        print("Activity Log Cleared.")

    else:

        print("Operation Cancelled.")


# -----------------------------------------
# Activity Menu
# -----------------------------------------

def activity_menu():

    while True:

        print("\n")
        print("=" * 50)
        print("          ACTIVITY LOG")
        print("=" * 50)

        print("1. View Activity Log")
        print("2. Clear Activity Log")
        print("3. Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            view_logs()

        elif choice == "2":

            clear_logs()

        elif choice == "3":

            break

        else:

            print("Invalid Choice.")
