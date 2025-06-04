from db.models import User, Category, Transaction, Session
from helpers import UserHelper, CategoryHelper, TransactionHelper

def test_connection():

    try:
        session = Session()
        users = session.query(User).count()
        categories = session.query(Category).count()
        transactions = session.query(Transaction).count()
        
        print(" Database connected")
        print(f"Users: {users}, Categories: {categories}, Transactions: {transactions}")
        session.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def quick_test():

    print("Testing core functions...")

    user, msg = UserHelper.create_user("Test User", "test@test.com", "pass123")
    print(f"User: {msg}")
    
    if user:

        cat, msg = CategoryHelper.create_category("Test Cat", user.id)
        print(f"Category: {msg}")

        trans, msg = TransactionHelper.create_transaction(100.0, "income", "Test Income", user.id)
        print(f"Transaction: {msg}")

        UserHelper.delete_user(user.id)
        print("Test completed, cleaned up")

def show_stats():
    try:
        session = Session()
        users = session.query(User).all()
        
        print("\n--- Database Stats ---")
        print(f"Total Users: {len(users)}")
        
        for user in users:
            cats = session.query(Category).filter_by(user_id=user.id).count()
            trans = session.query(Transaction).filter_by(user_id=user.id).count()
            print(f"{user.name}: {cats} categories, {trans} transactions")
        
        session.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            quick_test()
        elif sys.argv[1] == "stats":
            show_stats()
        else:
            print("Usage: python debug.py [test|stats]")
    else:
        print("Debug Menu:")
        print("1. Test Connection")
        print("2. Quick Test")
        print("3. Show Stats")
        
        choice = input("Choice: ").strip()
        if choice == "1":
            test_connection()
        elif choice == "2":
            quick_test()
        elif choice == "3":
            show_stats()
        else:
            print("Invalid choice")
