#!/usr/bin/env python3

import sys
from datetime import datetime
from helpers import (
    UserHelper, CategoryHelper, TransactionHelper,
    DisplayHelper, get_valid_input, validate_email, validate_transaction_type
)

class FinanceTrackerCLI:
    def __init__(self):
        self.current_user = None
        self.is_running = True

    def display_banner(self):
        print("PERSONAL FINANCE TRACKER")

    def main_menu(self):
        while self.is_running:
            self.display_banner()
            print("\n1. User Menu\n2. Categories\n3. Transactions\n4. Exit")
            choice = get_valid_input("Choice (1-4): ")

            if choice == "1":
                self.user_menu()
            elif choice == "2" and self.check_logged_in():
                self.category_menu()
            elif choice == "3" and self.check_logged_in():
                self.transactions_menu()
            elif choice == "4":
                self.exit_app()
            else:
                print("Invalid choice.")

    def user_menu(self):
        while True:
            print("\n--- USER MENU ---")
            if not self.current_user:
                print("1. Create Account\n2. Login\n3. Back")
                choice = get_valid_input("Choice (1-3): ")

                if choice == "1":
                    self.create_account()
                elif choice == "2":
                    self.login()
                elif choice == "3":
                    break
                else:
                    print("Invalid choice.")
            else:
                print(f"Welcome, {self.current_user.name}!")
                print("1. Account Info\n2. User ID\n3. Delete Account\n4. Logout\n5. Back")
                choice = get_valid_input("Choice (1-5): ")

                if choice == "1":
                    DisplayHelper.display_user_info(self.current_user)
                elif choice == "2":
                    print(f"Your ID: {self.current_user.user_id}")
                elif choice == "3" and self.delete_account():
                    break
                elif choice == "4":
                    self.logout()
                elif choice == "5":
                    break
                else:
                    print("Invalid choice.")

            input("Press Enter...")

    def create_account(self):
        print("\n--- CREATE ACCOUNT ---")
        name = get_valid_input("Name: ")
        email = get_valid_input("Email: ", validation_func=validate_email)
        password = get_valid_input("Password: ")

        user, message = UserHelper.create_user(name, email, password)
        print(f"\n{message}")
        if user:
            print(f"Your ID: {user.user_id}")
            self.current_user = user

    def login(self):
        print("\n--- LOGIN ---")
        email = get_valid_input("Email: ")
        password = get_valid_input("Password: ")

        user, message = UserHelper.login_user(email, password)
        print(f"\n{message}")
        if user:
            self.current_user = user

    def delete_account(self):
        print("\n⚠️  WARNING: This will delete ALL your data!")
        confirm = get_valid_input("Type 'DELETE' to confirm: ")

        if confirm == "DELETE":
            success, message = UserHelper.delete_user(self.current_user.id)
            print(f"\n{message}")
            if success:
                self.current_user = None
                return True
        else:
            print("Cancelled.")
        return False

    def logout(self):
        print(f"\nGoodbye, {self.current_user.name}!")
        self.current_user = None

    def category_menu(self):
        while True:
            print("\n--- CATEGORIES ---")
            print("1. Create\n2. View All\n3. Find\n4. Delete\n5. Back")
            choice = get_valid_input("Choice (1-5): ")

            if choice == "1":
                self.create_category()
            elif choice == "2":
                self.view_categories()
            elif choice == "3":
                self.find_category()
            elif choice == "4":
                self.delete_category()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

            input("Press Enter...")

    def create_category(self):
        name = get_valid_input("Category name: ")
        category, message = CategoryHelper.create_category(name, self.current_user.id)
        print(f"{message}")

    def view_categories(self):
        categories = CategoryHelper.get_user_categories(self.current_user.id)
        DisplayHelper.display_categories(categories)

    def find_category(self):
        name = get_valid_input("Category name: ")
        category = CategoryHelper.find_category_by_name(name, self.current_user.id)
        if category:
            print(f"Found: {category.name}")
        else:
            print("Not found.")

    def delete_category(self):
        categories = CategoryHelper.get_user_categories(self.current_user.id)
        if not categories:
            print("No categories to delete.")
            return

        DisplayHelper.display_categories(categories)
        name = get_valid_input("Category to delete: ")
        success, message = CategoryHelper.delete_category(name, self.current_user.id)
        print(f"{message}")

    def transactions_menu(self):
        while True:
            print("\n--- TRANSACTIONS ---")
            print("1. Create\n2. View All\n3. Find\n4. Search\n5. Edit\n6. Delete\n7. Monthly report\n8. Back")
            choice = get_valid_input("Choice (1-8): ")

            if choice == "1":
                self.create_transaction()
            elif choice == "2":
                self.view_transactions()
            elif choice == "3":
                self.find_transaction()
            elif choice == "4":
                self.search_transactions()
            elif choice == "5":
                self.edit_transaction()
            elif choice == "6":
                self.delete_transaction()
            elif choice == "7":
                self.view_monthly_report()
            elif choice == "8":
                break
            else:
                print("Invalid choice.")

            input("Press Enter...")

    def create_transaction(self):
        amount = get_valid_input("Amount: $", float)
        trans_type = get_valid_input("Type (income/expense): ", validation_func=validate_transaction_type)
        description = get_valid_input("Description: ")

        transaction, message = TransactionHelper.create_transaction(
            amount, trans_type, description, self.current_user.id
        )
        print(f"{message}")

    def view_transactions(self):
        transactions = TransactionHelper.get_user_transactions(self.current_user.id)
        DisplayHelper.display_transactions(transactions)

    def find_transaction(self):
        description = get_valid_input("Description: ")
        transaction = TransactionHelper.find_transaction_by_description(description, self.current_user.id)
        if transaction:
            print(f"Found: ${transaction.amount} - {transaction.description}")
        else:
            print("Not found.")

    def search_transactions(self):
        if not self.current_user:
            print("❌ You must be logged in to search transactions.")
            return

        print("\n--- Filter Transactions ---")
        start_date_str = get_valid_input("Start date (YYYY-MM-DD) or leave blank: ")
        end_date_str = get_valid_input("End date (YYYY-MM-DD) or leave blank: ")
        min_amount_str = get_valid_input("Minimum amount or leave blank: ")
        max_amount_str = get_valid_input("Maximum amount or leave blank: ")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
            min_amount = float(min_amount_str) if min_amount_str else None
            max_amount = float(max_amount_str) if max_amount_str else None
        except ValueError as ve:
            print(f"Invalid input: {ve}")
            return

        transactions = TransactionHelper.search_transactions(
            self.current_user.id, start_date, end_date, min_amount, max_amount
        )

        if transactions:
            DisplayHelper.display_transactions(transactions)
        else:
            print("No transactions found matching your filters.")

    def view_monthly_report(self):
        report = TransactionHelper.get_monthly_report(self.current_user.id)
        print("\n--- Monthly Report ---")
        for month, data in report.items():
            income = data.get("income", 0.0)
            expense = data.get("expense", 0.0)
            print(f"{month}: Income = ${income:.2f}, Expense = ${expense:.2f}")

    def edit_transaction(self):
        transaction_id = int(get_valid_input("Enter Transaction ID to edit: "))
        field = get_valid_input("Enter field to edit (amount, description, type): ")
        new_value = get_valid_input(f"Enter new value for {field}: ")

        if field == "amount":
            new_value = float(new_value)

        updated_transaction, message = TransactionHelper.edit_transaction(
            transaction_id, self.current_user.id, **{field: new_value}
        )
        print(message)

    def delete_transaction(self):
        transactions = TransactionHelper.get_user_transactions(self.current_user.id)
        if not transactions:
            print("No transactions to delete.")
            return

        DisplayHelper.display_transactions(transactions)
        description = get_valid_input("Description to delete: ")
        success, message = TransactionHelper.delete_transaction(description, self.current_user.id)
        print(f"{'Deleted' if success else 'Not deleted'}: {message}")

    def check_logged_in(self):
        if not self.current_user:
            print("❌ Please log in first.")
            input("Press Enter...")
            return False
        return True

    def exit_app(self):
        print("\nThanks for using Finance Tracker!")
        self.is_running = False
        sys.exit(0)

    def run(self):
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)

def main():
    app = FinanceTrackerCLI()
    app.run()

if __name__ == "__main__":
    main()
