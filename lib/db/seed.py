#!/usr/bin/env python3

from datetime import datetime, timedelta
from models import User, Category, Transaction, TransactionType, Session

def seed_database():
    """Seed the database with sample data for testing"""
    
    session = Session()
    
    try:
        # Clear existing data
        session.query(Transaction).delete()
        session.query(Category).delete()
        session.query(User).delete()
        
        # Create sample users
        user1 = User(
            name="John Doe",
            email="john.doe@example.com", 
            password="password123",
            created_at=datetime.now() - timedelta(days=30),
            last_login=datetime.now() - timedelta(hours=2)
        )
        
        user2 = User(
            name="Jane Smith",
            email="jane.smith@example.com",
            password="securepass456",
            created_at=datetime.now() - timedelta(days=15),
            last_login=datetime.now() - timedelta(minutes=30)
        )
        
        session.add_all([user1, user2])
        session.commit()
        
        # Create sample categories for user1
        categories_user1 = [
            Category(name="Food & Dining", user_id=user1.id, created_at=datetime.now() - timedelta(days=25)),
            Category(name="Transportation", user_id=user1.id, created_at=datetime.now() - timedelta(days=20)),
            Category(name="Entertainment", user_id=user1.id, created_at=datetime.now() - timedelta(days=18)),
            Category(name="Salary", user_id=user1.id, created_at=datetime.now() - timedelta(days=22)),
            Category(name="Utilities", user_id=user1.id, created_at=datetime.now() - timedelta(days=15))
        ]
        
        # Create sample categories for user2
        categories_user2 = [
            Category(name="Groceries", user_id=user2.id, created_at=datetime.now() - timedelta(days=12)),
            Category(name="Healthcare", user_id=user2.id, created_at=datetime.now() - timedelta(days=10)),
            Category(name="Freelance Work", user_id=user2.id, created_at=datetime.now() - timedelta(days=8))
        ]
        
        session.add_all(categories_user1 + categories_user2)
        session.commit()
        
        # Create sample transactions for user1
        transactions_user1 = [
            # Income transactions
            Transaction(
                amount=3500.00,
                transaction_type=TransactionType.INCOME,
                description="Monthly Salary",
                user_id=user1.id,
                created_at=datetime.now() - timedelta(days=20)
            ),
            Transaction(
                amount=500.00,
                transaction_type=TransactionType.INCOME,
                description="Freelance Project",
                user_id=user1.id,
                created_at=datetime.now() - timedelta(days=15)
            ),
            # Expense transactions
            Transaction(
                amount=85.50,
                transaction_type=TransactionType.EXPENSE,
                description="Grocery Shopping",
                user_id=user1.id,
                created_at=datetime.now() - timedelta(days=18)
            ),
            Transaction(
                amount=45.20,
                transaction_type=TransactionType.EXPENSE,
                description="Gas Station",
                user_id=user1.id,
                created_at=datetime.now() - timedelta(days=16)
            ),
            Transaction(
                amount=25.00,
                transaction_type=TransactionType.EXPENSE,
                description="Movie Tickets",
                user_id=user1.id,
                created_at=datetime.now() - timedelta(days=12)
            ),
            Transaction(
                amount=120.75,
                transaction_type=TransactionType.EXPENSE,
                description="Electric Bill",
                user_id=user1.id,
                created_at=datetime.now() - timedelta(days=10)
            )
        ]
        
        # Create sample transactions for user2
        transactions_user2 = [
            # Income transactions
            Transaction(
                amount=2800.00,
                transaction_type=TransactionType.INCOME,
                description="Part-time Job Salary",
                user_id=user2.id,
                created_at=datetime.now() - timedelta(days=14)
            ),
            Transaction(
                amount=750.00,
                transaction_type=TransactionType.INCOME,
                description="Consulting Work",
                user_id=user2.id,
                created_at=datetime.now() - timedelta(days=8)
            ),
            # Expense transactions
            Transaction(
                amount=92.30,
                transaction_type=TransactionType.EXPENSE,
                description="Weekly Groceries",
                user_id=user2.id,
                created_at=datetime.now() - timedelta(days=12)
            ),
            Transaction(
                amount=35.00,
                transaction_type=TransactionType.EXPENSE,
                description="Doctor Visit Copay",
                user_id=user2.id,
                created_at=datetime.now() - timedelta(days=9)
            ),
            Transaction(
                amount=67.80,
                transaction_type=TransactionType.EXPENSE,
                description="Pharmacy - Prescription",
                user_id=user2.id,
                created_at=datetime.now() - timedelta(days=6)
            )
        ]
        
        session.add_all(transactions_user1 + transactions_user2)
        session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"Created {len([user1, user2])} users")
        print(f"Created {len(categories_user1 + categories_user2)} categories")
        print(f"Created {len(transactions_user1 + transactions_user2)} transactions")
        
        # Display sample user credentials
        print("\n--- Sample User Credentials ---")
        print("User 1:")
        print(f"  Email: {user1.email}")
        print(f"  Password: password123")
        print(f"  User ID: {user1.user_id}")
        
        print("User 2:")
        print(f"  Email: {user2.email}")
        print(f"  Password: securepass456")
        print(f"  User ID: {user2.user_id}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding database: {str(e)}")
    finally:
        session.close()

def clear_database():
    """Clear all data from the database"""
    session = Session()
    
    try:
        session.query(Transaction).delete()
        session.query(Category).delete()
        session.query(User).delete()
        session.commit()
        print("✅ Database cleared successfully!")
    except Exception as e:
        session.rollback()
        print(f"❌ Error clearing database: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "clear":
            clear_database()
        elif sys.argv[1] == "seed":
            seed_database()
        else:
            print("Usage: python seed.py [seed|clear]")
    else:
        print("Choose an option:")
        print("1. Seed database with sample data")
        print("2. Clear all database data")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            seed_database()
        elif choice == "2":
            clear_database()
        else:
            print("Invalid choice.")
            