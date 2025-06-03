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
    def search_transactions(user_id, start_date=None, end_date=None, min_amount=None, max_amount=None):
        session = Session()
        try:
            query = session.query(Transaction).filter_by(user_id=user_id)

            if start_date:
                query = query.filter(Transaction.created_at >= start_date)
            if end_date:
                query = query.filter(Transaction.created_at <= end_date)
            if min_amount:
                query = query.filter(Transaction.amount >= min_amount)
            if max_amount:
                query = query.filter(Transaction.amount <= max_amount)

            return query.order_by(Transaction.created_at.desc()).all()
        finally:
            session.close()

    @staticmethod
    def get_monthly_report(user_id):
        session = Session()
        try:
            results = session.query(
                func.strftime("%Y-%m", Transaction.created_at).label("month"),
                Transaction.transaction_type,
                func.sum(Transaction.amount).label("total_amount")
            ).filter_by(user_id=user_id).group_by("month", Transaction.transaction_type).order_by("month").all()

            report = {}
            for month, trans_type, total in results:
                if month not in report:
                    report[month] = {}
                report[month][trans_type.value] = float(total)

            return report
        finally:
            session.close()


    @staticmethod
    def edit_transaction(transaction_id, user_id, **kwargs):
        session = Session()
        try:
            transaction = session.query(Transaction).filter_by(id=transaction_id, user_id=user_id).first()
            if not transaction:
                return None, "Transaction not found."

            for key, value in kwargs.items():
                if hasattr(transaction, key):
                    setattr(transaction, key, value)

            session.commit()
            return transaction, "Transaction updated successfully."
        except Exception as e:
            session.rollback()
            return None, f"Error: {str(e)}"
        finally:
            session.close()
    
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
    