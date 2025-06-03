from datetime import datetime
import uuid
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum

Base = declarative_base()
engine = create_engine('sqlite:///finance_tracker.db')

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)
    
    # Relationships
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', user_id='{self.user_id}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'last_login': self.last_login
        }

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(name='{self.name}', created_at='{self.created_at}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'created_at': self.created_at
        }

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(amount={self.amount}, type='{self.transaction_type}', description='{self.description}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': float(self.amount),
            'transaction_type': self.transaction_type.value,
            'description': self.description,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'created_at': self.created_at
        }

# Create tables
Base.metadata.create_all(engine)

# Session factory
Session = sessionmaker(bind=engine)
