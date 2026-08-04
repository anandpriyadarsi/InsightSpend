import json

GOAL_FILE = "data/goals.json"


# ----------------------------
# Load Goals
# ----------------------------

def load_goals():

    try:
        with open(GOAL_FILE, "r") as file:
            return json.load(file)

    except:
        return []


# ----------------------------
# Save Goals
# ----------------------------

def save_goals(goals):

    with open(GOAL_FILE, "w") as file:
        json.dump(goals, file, indent=4)


# ----------------------------
# Progress Bar
# ----------------------------

def progress_bar(percentage):

    blocks = 20

    filled = int((percentage / 100) * blocks)

    if filled > blocks:
        filled = blocks

    empty = blocks - filled

    return "█" * filled + "░" * empty

def add_goal():

    goals = load_goals()

    print("\n========== ADD GOAL ==========")

    name = input("Goal Name : ")

    try:
        target = float(input("Target Amount : ₹"))
    except ValueError:
        print("Invalid amount.")
        return

    goal = {
        "name": name,
        "target": target,
        "saved": 0
    }

    goals.append(goal)

    save_goals(goals)

    print("Goal Added Successfully.")

def view_goals():

    goals = load_goals()

    if len(goals) == 0:
        print("No goals found.")
        return

    print("\n========== FINANCIAL GOALS ==========\n")

    for index, goal in enumerate(goals, start=1):

        target = goal["target"]
        saved = goal["saved"]

        percentage = (saved / target) * 100 if target else 0

        print(f"{index}. {goal['name']}")
        print(f"Target    : ₹{target:.2f}")
        print(f"Saved     : ₹{saved:.2f}")
        print(f"Remaining : ₹{target-saved:.2f}")
        print(progress_bar(percentage))
        print(f"{percentage:.1f}%")
        print("-" * 40)
def add_savings():

    goals = load_goals()

    if len(goals) == 0:
        print("No goals found.")
        return

    view_goals()

    try:
        choice = int(input("\nGoal Number : ")) - 1

        amount = float(input("Amount to Add : ₹"))

    except ValueError:
        print("Invalid input.")
        return

    if choice < 0 or choice >= len(goals):
        print("Invalid goal.")
        return

    goals[choice]["saved"] += amount

    save_goals(goals)

    print("Savings Updated Successfully.")

def delete_goal():

    goals = load_goals()

    if len(goals) == 0:
        print("No goals found.")
        return

    view_goals()

    try:
        choice = int(input("\nGoal Number : ")) - 1

    except ValueError:
        print("Invalid input.")
        return

    if choice < 0 or choice >= len(goals):
        print("Invalid goal.")
        return

    deleted = goals.pop(choice)

    save_goals(goals)

    print(f"{deleted['name']} deleted successfully.")
def goal_menu():

    while True:

        print("\n==============================")
        print("      FINANCIAL GOALS")
        print("==============================")
        print("1. Add Goal")
        print("2. View Goals")
        print("3. Add Savings")
        print("4. Delete Goal")
        print("5. Back")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            add_goal()

        elif choice == "2":

            view_goals()

        elif choice == "3":

            add_savings()

        elif choice == "4":

            delete_goal()

        elif choice == "5":

            break

        else:

            print("Invalid Choice.")

