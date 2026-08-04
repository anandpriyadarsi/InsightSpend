import json

def add_income():
    amount = float(input("Enter amount: "))
    source = input("Enter source: ")
    date = input("Enter date: ")
    notes = input("Enter notes: ")

    income = {
        "amount": amount,
        "source": source,
        "date": date,
        "notes": notes
    }

    with open("data/income.json", "r") as file:
        incomes = json.load(file)

    incomes.append(income)

    with open("data/income.json", "w") as file:
        json.dump(incomes, file, indent=4)

    print("\nIncome Added Successfully!")
def view_income():
    with open("data/income.json", "r") as file:
        incomes = json.load(file)

    if len(incomes) == 0:
        print("No income records found.")
        return

    print("\n========== Income Records ==========\n")

    for income in incomes:
        print(f"Amount : ₹{income['amount']}")
        print(f"Source : {income['source']}")
        print(f"Date   : {income['date']}")
        print(f"Notes  : {income['notes']}")
        print("-" * 35)
        
