from datetime import datetime
from sqlalchemy import func
from db.models import User, Category, Transaction, TransactionType, Session

session = Session()

class UserHelper:
    @staticmethod
    def create_user(name, email, password):
        try:
            if session.query(User).filter_by(email=email).first():
                return None, "Email already exists"

            user = User(name=name, email=email, password=password)
            session.add(user)
            session.commit()
            return user, "Account created"
        except Exception as e:
            session.rollback()
            return None, f"Error: {str(e)}"

    @staticmethod
    def login_user(email, password):
        try:
            user = session.query(User).filter_by(email=email, password=password).first()
            if user:
                user.last_login = datetime.now()
                session.commit()
                return user, "Login successful"
            return None, "Invalid credentials"
        except Exception as e:
            return None, f"Error: {str(e)}"

    @staticmethod
    def delete_user(user_id):
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True, "Account deleted"
            return False, "User not found"
        except Exception as e:
            session.rollback()
            return False, f"Error: {str(e)}"

class CategoryHelper:
    @staticmethod
    def create_category(name, user_id):
        try:
            if session.query(Category).filter_by(name=name, user_id=user_id).first():
                return None, "Category already exists"

            category = Category(name=name, user_id=user_id)
            session.add(category)
            session.commit()
            return category, "Category created"
        except Exception as e:
            session.rollback()
            return None, f"Error: {str(e)}"

    @staticmethod
    def get_user_categories(user_id):
        return session.query(Category).filter_by(user_id=user_id).all()

    @staticmethod
    def find_category_by_name(name, user_id):
        return session.query(Category).filter_by(name=name, user_id=user_id).first()

    @staticmethod
    def delete_category(name, user_id):
        try:
            category = session.query(Category).filter_by(name=name, user_id=user_id).first()
            if category:
                session.delete(category)
                session.commit()
                return True, "Category deleted"
            return False, "Category not found"
        except Exception as e:
            session.rollback()
            return False, f"Error: {str(e)}"

class TransactionHelper:
    @staticmethod
    def create_transaction(amount, transaction_type, description, user_id):
        try:
            if transaction_type.lower() not in ['income', 'expense']:
                return None, "Invalid type. Use 'income' or 'expense'"

            trans_type = TransactionType.INCOME if transaction_type.lower() == 'income' else TransactionType.EXPENSE

            transaction = Transaction(
                amount=amount,
                transaction_type=trans_type,
                description=description,
                user_id=user_id
            )
            session.add(transaction)
            session.commit()
            return transaction, "Transaction created"
        except Exception as e:
            session.rollback()
            return None, f"Error: {str(e)}"

    @staticmethod
    def get_user_transactions(user_id):
        return session.query(Transaction).filter_by(user_id=user_id).all()

    @staticmethod
    def find_transaction_by_description(description, user_id):
        return session.query(Transaction).filter_by(description=description, user_id=user_id).first()

    @staticmethod
    def delete_transaction(description, user_id):
        try:
            transaction = session.query(Transaction).filter_by(description=description, user_id=user_id).first()
            if transaction:
                session.delete(transaction)
                session.commit()
                return True, "Transaction deleted"
            return False, "Transaction not found"
        except Exception as e:
            session.rollback()
            return False, f"Error: {str(e)}"

    @staticmethod
    def get_detailed_monthly_report(user_id):
        session = Session()
        try:
            transactions = session.query(Transaction).filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
            report = {}

            for transaction in transactions:
                month = transaction.created_at.strftime("%Y-%m")
                if month not in report:
                    report[month] = {
                        'income': [],
                        'expense': [],
                        'totals': {'income': 0.0, 'expense': 0.0}
                    }
                trans_type = transaction.transaction_type.value
                transaction_data = {
                    'id': transaction.id,
                    'amount': float(transaction.amount),
                    'description': transaction.description,
                    'date': transaction.created_at.strftime("%Y-%m-%d"),
                    'time': transaction.created_at.strftime("%H:%M")
                }
                report[month][trans_type].append(transaction_data)
                report[month]['totals'][trans_type] += float(transaction.amount)

            return report
        except Exception as e:
            print(f"Error generating monthly report: {str(e)}")
            return {}
        finally:
            session.close()

    @staticmethod
    def get_monthly_report(user_id):
        session = Session()
        try:
            transactions = session.query(Transaction).filter_by(user_id=user_id).all()
            summary = {}
            for transaction in transactions:
                month = transaction.created_at.strftime("%Y-%m")
                if month not in summary:
                    summary[month] = {'income': 0.0, 'expense': 0.0}
                trans_type = transaction.transaction_type.value
                summary[month][trans_type] += float(transaction.amount)
            return summary
        except Exception as e:
            print(f"Error generating summary report: {str(e)}")
            return {}
        finally:
            session.close()

class DisplayHelper:
    @staticmethod
    def format_datetime(dt):
        return dt.strftime("%Y-%m-%d %H:%M") if dt else "Never"

    @staticmethod
    def display_user_info(user):
        print(f"\n--- Account Info ---")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"ID: {user.user_id}")
        print(f"Created: {DisplayHelper.format_datetime(user.created_at)}")
        print(f"Last Login: {DisplayHelper.format_datetime(user.last_login)}")

    @staticmethod
    def display_categories(categories):
        if not categories:
            print("No categories found.")
            return
        print(f"Categories ({len(categories)}):")
        for cat in categories:
            print(f"• {cat.name}")

    @staticmethod
    def display_transactions(transactions):
        if not transactions:
            print("No transactions found.")
            return

        income = [t for t in transactions if t.transaction_type == TransactionType.INCOME]
        expenses = [t for t in transactions if t.transaction_type == TransactionType.EXPENSE]
        print(f"Transactions ({len(transactions)}):")

        if income:
            total_income = sum(float(t.amount) for t in income)
            print(f"\n INCOME: ${total_income:.2f}")
            for t in income:
                print(f"  • ${t.amount:.2f} - {t.description}")

        if expenses:
            total_expenses = sum(float(t.amount) for t in expenses)
            print(f"\n EXPENSES: ${total_expenses:.2f}")
            for t in expenses:
                print(f"  • ${t.amount:.2f} - {t.description}")

        if income or expenses:
            balance = sum(float(t.amount) for t in income) - sum(float(t.amount) for t in expenses)
            print(f"\n Balance: ${balance:.2f}")

    @staticmethod
    def display_detailed_report(report):
        if not report:
            print("No transactions found for monthly report.")
            return

        print("\n" + "="*60)
        print("           DETAILED MONTHLY REPORT")
        print("="*60)

        sorted_months = sorted(report.keys(), reverse=True)

        for month in sorted_months:
            month_data = report[month]
            try:
                month_obj = datetime.strptime(month, "%Y-%m")
                month_display = month_obj.strftime("%B %Y")
            except:
                month_display = month

            print(f"\n {month_display}")
            print("-" * 50)

            if month_data['income']:
                print(" INCOME:")
                for t in month_data['income']:
                    print(f"   • {t['date']} - ${t['amount']:.2f} - {t['description']}")
                print(f"    Total Income: ${month_data['totals']['income']:.2f}")
            else:
                print(" INCOME: No income transactions")
                print("    Total Income: $0.00")

            print()

            if month_data['expense']:
                print(" EXPENSES:")
                for t in month_data['expense']:
                    print(f"   • {t['date']} - ${t['amount']:.2f} - {t['description']}")
                print(f"    Total Expenses: ${month_data['totals']['expense']:.2f}")
            else:
                print(" EXPENSES: No expense transactions")
                print("    Total Expenses: $0.00")

            net_balance = month_data['totals']['income'] - month_data['totals']['expense']
            balance_symbol = "" if net_balance >= 0 else ""
            print(f"\n   {balance_symbol} Net Balance: ${net_balance:.2f}")
            print("-" * 50)

    @staticmethod
    def display_summary_report(summary):
        if not summary:
            print("No transactions found for summary report.")
            return

        print("\n--- SUMMARY OVERVIEW ---")
        sorted_months = sorted(summary.keys(), reverse=True)
        for month in sorted_months:
            income = summary[month]['income']
            expense = summary[month]['expense']
            net = income - expense
            print(f"\n📅 {month} | Income: ${income:.2f} | Expenses: ${expense:.2f} | Net: ${net:.2f}")


def get_valid_input(prompt, input_type=str, validation_func=None):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("Input cannot be empty.")
                continue

            if input_type == float:
                user_input = float(user_input)
                if user_input <= 0:
                    print("Amount must be > 0.")
                    continue
            elif input_type == int:
                user_input = int(user_input)

            if validation_func and not validation_func(user_input):
                continue

            return user_input
        except ValueError:
            print(f"Invalid {input_type.__name__}.")

def validate_email(email):
    if "@" not in email or "." not in email:
        print("Invalid email format.")
        return False
    return True

def validate_transaction_type(trans_type):
    if trans_type.lower() not in ['income', 'expense']:
        print("Type must be 'income' or 'expense'.")
        return False
    return True
