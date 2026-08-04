import os
import shutil
from datetime import datetime

BACKUP_FOLDER = "backup"

FILES = [
    "data/income.json",
    "data/expenses.json",
    "data/budget.json",
    "data/goals.json",
    "data/user.json"
]


def create_backup():

    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)

    folder_name = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    destination = os.path.join(BACKUP_FOLDER, folder_name)

    os.mkdir(destination)

    for file in FILES:

        if os.path.exists(file):

            shutil.copy(file, destination)

    print("\nBackup Created Successfully.")
    print(f"Location : {destination}")

def view_backups():

    if not os.path.exists(BACKUP_FOLDER):

        print("No backups found.")
        return

    backups = os.listdir(BACKUP_FOLDER)

    if len(backups) == 0:

        print("No backups available.")
        return

    print("\n========== AVAILABLE BACKUPS ==========\n")

    for index, backup in enumerate(backups, start=1):

        print(f"{index}. {backup}")

def restore_backup():

    if not os.path.exists(BACKUP_FOLDER):

        print("No backups available.")
        return

    backups = os.listdir(BACKUP_FOLDER)

    if len(backups) == 0:

        print("No backups available.")
        return

    view_backups()

    try:

        choice = int(input("\nChoose Backup : ")) - 1

    except ValueError:

        print("Invalid Input.")
        return

    if choice < 0 or choice >= len(backups):

        print("Invalid Choice.")
        return

    source = os.path.join(BACKUP_FOLDER, backups[choice])

    for file in FILES:

        filename = os.path.basename(file)

        backup_file = os.path.join(source, filename)

        if os.path.exists(backup_file):

            shutil.copy(backup_file, file)

    print("\nBackup Restored Successfully.")

def backup_menu():

    while True:

        print("\n==============================")
        print(" BACKUP & RESTORE ")
        print("==============================")
        print("1. Create Backup")
        print("2. View Backups")
        print("3. Restore Backup")
        print("4. Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            create_backup()

        elif choice == "2":

            view_backups()

        elif choice == "3":

            restore_backup()

        elif choice == "4":

            break

        else:

            print("Invalid Choice.")
