import json
import os

SETTINGS_FILE = "data/settings.json"


# -----------------------------------------
# Create Default Settings
# -----------------------------------------

def create_default_settings():

    if not os.path.exists(SETTINGS_FILE):

        settings = {
            "currency": "₹",
            "date_format": "DD-MM-YYYY",
            "theme": "Light",
            "welcome_message": True
        }

        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)


# -----------------------------------------
# Load Settings
# -----------------------------------------

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        settings = create_default_settings()
        with open(SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)

        return settings


    try:

        with open(SETTINGS_FILE, "r") as file:

            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):

        print("Settings file was empty or corrupted.")
        print("Creating a new settings file...")

        settings = default_settings()

        with open(SETTINGS_FILE, "w") as file:

            json.dump(settings, file, indent=4)

        return settings


# -----------------------------------------
# Save Settings
# -----------------------------------------

def save_settings(settings):

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


# -----------------------------------------
# View Settings
# -----------------------------------------

def view_settings():

    settings = load_settings()

    print("\n========== CURRENT SETTINGS ==========\n")

    print(f"Currency         : {settings['currency']}")
    print(f"Date Format      : {settings['date_format']}")
    print(f"Theme            : {settings['theme']}")
    print(f"Welcome Message  : {settings['welcome_message']}")

def change_currency():

    settings = load_settings()

    print("\nAvailable Currencies")

    print("1. ₹ (Indian Rupee)")
    print("2. $ (US Dollar)")
    print("3. € (Euro)")
    print("4. £ (Pound)")

    choice = input("\nChoose Currency : ")

    if choice == "1":
        settings["currency"] = "₹"

    elif choice == "2":
        settings["currency"] = "$"

    elif choice == "3":
        settings["currency"] = "€"

    elif choice == "4":
        settings["currency"] = "£"

    else:
        print("Invalid Choice")
        return

    save_settings(settings)

    print("Currency Updated Successfully.")

def change_date_format():

    settings = load_settings()

    print("\nDate Formats")

    print("1. DD-MM-YYYY")
    print("2. MM-DD-YYYY")
    print("3. YYYY-MM-DD")

    choice = input("\nChoose Format : ")

    if choice == "1":
        settings["date_format"] = "DD-MM-YYYY"

    elif choice == "2":
        settings["date_format"] = "MM-DD-YYYY"

    elif choice == "3":
        settings["date_format"] = "YYYY-MM-DD"

    else:
        print("Invalid Choice")
        return

    save_settings(settings)

    print("Date Format Updated.")

def change_theme():

    settings = load_settings()

    print("\nTheme")

    print("1. Light")
    print("2. Dark")

    choice = input("\nChoose Theme : ")

    if choice == "1":
        settings["theme"] = "Light"

    elif choice == "2":
        settings["theme"] = "Dark"

    else:
        print("Invalid Choice")
        return

    save_settings(settings)

    print("Theme Updated.")

def toggle_welcome():

    settings = load_settings()

    settings["welcome_message"] = not settings["welcome_message"]

    save_settings(settings)

    print("Welcome Message Updated.")

def settings_menu():

    while True:

        print("\n")
        print("=" * 45)
        print("          SETTINGS")
        print("=" * 45)

        print("1. View Settings")
        print("2. Change Currency")
        print("3. Change Date Format")
        print("4. Change Theme")
        print("5. Toggle Welcome Message")
        print("6. Reset Settings")
        print("7. Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            view_settings()

        elif choice == "2":

            change_currency()

        elif choice == "3":

            change_date_format()

        elif choice == "4":

            change_theme()

        elif choice == "5":

            toggle_welcome()

        elif choice == "6":

            reset_settings()

        elif choice == "7":

            break

        else:

            print("Invalid Choice.")
            
