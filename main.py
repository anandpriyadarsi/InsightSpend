"""
====================================================
InsightSpend - Personal Finance Tracker
Version : 1.0
Developer : Anand Priyadarsi

A Console Based Personal Finance Management System
====================================================
"""

import sys

from modules.login import login

from modules.income import (
    add_income,
    view_income
)

from modules.expense import (
    add_expense,
    view_expenses,
    edit_expense,
    delete_expense,
    search_expenses
)

from modules.analytics import financial_summary

from modules.budget import (
    set_budget,
    view_budget,
    budget_status
)

from modules.report import generate_report

from modules.export import (
    export_expenses_csv,
    import_expenses_csv
)

from modules.dashboard import show_dashboard

from modules.monthly_analysis import monthly_summary

from modules.account import account_menu

from modules.goals import goal_menu

from modules.backup import backup_menu

from modules.statistics import statistics_dashboard

from modules.settings import settings_menu


# ==========================================
# Display Main Menu
# ==========================================

def display_menu():

    print("\n" + "=" * 60)
    print("               INSIGHTSPEND MAIN MENU")
    print("=" * 60)

    print("\nIncome")
    print("1.  Add Income")
    print("2.  View Income")

    print("\nExpense")
    print("3.  Add Expense")
    print("4.  View Expenses")
    print("5.  Edit Expense")
    print("6.  Delete Expense")
    print("7.  Search Expenses")

    print("\nBudget")
    print("8.  Set Budget")
    print("9.  View Budget")
    print("10. Budget Status")

    print("\nAnalytics & Reports")
    print("11. Analytics Dashboard")
    print("12. Financial Health Dashboard")
    print("13. Monthly Analysis")
    print("14. Statistics Dashboard")
    print("15. Generate PDF Report")

    print("\nImport / Export")
    print("16. Export Expenses to CSV")
    print("17. Import Expenses from CSV")

    print("\nAccount")
    print("18. Account Management")
    print("19. Financial Goals")
    print("20. Backup & Restore")
    print("21. Settings")

    print("\n22. Exit")
    print("=" * 60)


# ==========================================
# Main Program
# ==========================================

def main():

    if not login():
        sys.exit()

    while True:

        display_menu()

        choice = input("\nEnter your choice : ")

        if choice == "1":
            add_income()

        elif choice == "2":
            view_income()

        elif choice == "3":
            add_expense()

        elif choice == "4":
            view_expenses()

        elif choice == "5":
            edit_expense()

        elif choice == "6":
            delete_expense()

        elif choice == "7":
            search_expenses()

        elif choice == "8":
            set_budget()

        elif choice == "9":
            view_budget()

        elif choice == "10":
            budget_status()

        elif choice == "11":
            financial_summary()

        elif choice == "12":
            show_dashboard()

        elif choice == "13":
            monthly_summary()

        elif choice == "14":
            statistics_dashboard()

        elif choice == "15":
            generate_report()

        elif choice == "16":
            export_expenses_csv()

        elif choice == "17":
            import_expenses_csv()

        elif choice == "18":
            account_menu()

        elif choice == "19":
            goal_menu()

        elif choice == "20":
            backup_menu()

        elif choice == "21":
            settings_menu()

        elif choice == "22":

            print("\nThank you for using InsightSpend!")
            print("Have a great day.\n")
            break

        else:
            print("\nInvalid choice. Please try again.")


# ==========================================
# Program Entry Point
# ==========================================

if __name__ == "__main__":
    main()
