from helpers import UserHelper, CategoryHelper, TransactionHelper, DisplayHelper, get_valid_input, validate_email, validate_transaction_type

current_user = None

def user_menu():
    global current_user
    while True:
        print("\n=== USER MENU ===")
        print("1. Create Account")
        print("2. Log In")
        print("3. View Account Info")
        print("4. Find Account User ID")
        print("5. Delete Account")
        print("6. Log Out")
        print("0. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            name = get_valid_input("Enter name: ")
            email = get_valid_input("Enter email: ", validation_func=validate_email)
            password = get_valid_input("Enter password: ")
            user, msg = UserHelper.create_user(name, email, password)
            print(msg)
            if user:
                current_user = user

        elif choice == "2":
            email = get_valid_input("Enter email: ")
            password = get_valid_input("Enter password: ")
            user, msg = UserHelper.login_user(email, password)
            print(msg)
            if user:
                current_user = user

        elif choice == "3":
            if current_user:
                DisplayHelper.display_user_info(current_user)
            else:
                print("You need to log in first.")

        elif choice == "4":
            if current_user:
                print(f"Your User ID: {current_user.user_id}")
            else:
                print("You need to log in first.")

        elif choice == "5":
            if current_user:
                confirm = input("Are you sure you want to delete your account? (yes/no): ")
                if confirm.lower() == "yes":
                    success, msg = UserHelper.delete_user(current_user.user_id)
                    print(msg)
                    if success:
                        current_user = None
            else:
                print("You need to log in first.")

        elif choice == "6":
            current_user = None
            print("Logged out.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def category_menu():
    while True:
        print("\n=== CATEGORY MENU ===")
        print("1. Create Category")
        print("2. View All Categories")
        print("3. Find Category by Name")
        print("4. Delete Category by Name")
        print("0. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            if current_user:
                name = get_valid_input("Enter category name: ")
                category, msg = CategoryHelper.create_category(name, current_user.user_id)
                print(msg)
            else:
                print("You need to log in first.")

        elif choice == "2":
            if current_user:
                categories = CategoryHelper.get_user_categories(current_user.user_id)
                DisplayHelper.display_categories(categories)
            else:
                print("You need to log in first.")

        elif choice == "3":
            if current_user:
                name = get_valid_input("Enter category name: ")
                category = CategoryHelper.find_category_by_name(name, current_user.user_id)
                if category:
                    print(f"Found: {category.name}")
                else:
                    print("Category not found.")
            else:
                print("You need to log in first.")

        elif choice == "4":
            if current_user:
                name = get_valid_input("Enter category name to delete: ")
                success, msg = CategoryHelper.delete_category(name, current_user.user_id)
                print(msg)
            else:
                print("You need to log in first.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def transaction_menu():
    while True:
        print("\n=== TRANSACTIONS MENU ===")
        print("1. Create Transaction")
        print("2. View All Transactions")
        print("3. Find Transaction by Description")
        print("4. Delete Transaction")
        print("5. View Monthly Summary Report")
        print("6. View Detailed Monthly Report")
        print("0. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == "1":
            if current_user:
                amount = get_valid_input("Enter amount: ", float)
                transaction_type = get_valid_input("Enter type (income/expense): ", validation_func=validate_transaction_type)
                description = get_valid_input("Enter description: ")
                transaction, msg = TransactionHelper.create_transaction(amount, transaction_type, description, current_user.user_id)
                print(msg)
            else:
                print("You need to log in first.")

        elif choice == "2":
            if current_user:
                transactions = TransactionHelper.get_user_transactions(current_user.user_id)
                DisplayHelper.display_transactions(transactions)
            else:
                print("You need to log in first.")

        elif choice == "3":
            if current_user:
                description = get_valid_input("Enter transaction description: ")
                transaction = TransactionHelper.find_transaction_by_description(description, current_user.user_id)
                if transaction:
                    print(f"Found: ${transaction.amount} - {transaction.description}")
                else:
                    print("Transaction not found.")
            else:
                print("You need to log in first.")

        elif choice == "4":
            if current_user:
                description = get_valid_input("Enter transaction description to delete: ")
                success, msg = TransactionHelper.delete_transaction(description, current_user.user_id)
                print(msg)
            else:
                print("You need to log in first.")

        elif choice == "5":
            if current_user:
                summary = TransactionHelper.get_monthly_report(current_user.user_id)
                DisplayHelper.display_summary_report(summary)
            else:
                print("You need to log in first.")

        elif choice == "6":
            if current_user:
                report = TransactionHelper.get_detailed_monthly_report(current_user.user_id)
                DisplayHelper.display_detailed_report(report)
            else:
                print("You need to log in first.")

        elif choice == "0":
            break
        else:
            print("Invalid choice.")

def main():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. User Menu")
        print("2. Category Menu")
        print("3. My Transactions")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            user_menu()
        elif choice == "2":
            category_menu()
        elif choice == "3":
            transaction_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
