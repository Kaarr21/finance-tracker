# Personal Finance Tracker CLI 

A command-line interface application for managing personal finances, built in Python with SQLAlchemy and SQLite database integration.


##  Features

### User Management
- **Account Creation**: Create new user accounts with email validation
- **Secure Login**: User authentication with email and password
- **Account Information**: View detailed user profile and statistics
- **Account Deletion**: Complete account removal with cascading data cleanup

### Category Management
- **Create Categories**: Organize transactions with custom categories
- **View Categories**: List all user-created categories with timestamps
- **Find Categories**: Search for specific categories by name
- **Delete Categories**: Remove categories (automatically removes associated transactions)

### Transaction Management
- **Income/Expense Tracking**: Record income and expense transactions
- **Transaction Search**: Find transactions by description
- **Balance Calculation**: Automatic calculation of net balance
- **Transaction History**: View complete transaction history with categorization
- **Data Validation**: Input validation for amounts and transaction types

### Data Display
- **Formatted Output**: Clean, organized display of all data
- **Transaction Summaries**: Separate income and expense totals
- **Balance Reports**: Net balance calculations
- **Timestamps**: All records include creation and last modified dates

##  Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or Download the Project**

2. **Install Required Dependencies**

3. **Verify Installation**

4. **Run the Application**

##  Usage

### Starting the Application

### Main Menu Navigation
The application provides an intuitive menu system:

1. **User Menu**: Account management (create, login, view info, delete)
2. **Category Menu**: Category management (requires login)
3. **Transactions Menu**: Transaction management (requires login)
4. **Exit**: Safely close the application

### Basic Workflow

1. **Create Account or Login**
   - Navigate to User Menu → Create Account
   - Provide name, email, and password
   - Note your unique User ID for reference

2. **Create Categories (Optional)**
   - Go to Category Menu → Create Category
   - Add categories like "Groceries", "Salary", "Utilities"

3. **Add Transactions**
   - Navigate to My Transactions Menu → Create Transaction
   - Enter amount, type (income/expense), and description
   - Transaction is automatically saved with timestamp

4. **View Reports**
   - Use "View All Transactions" to see complete history
   - Transactions are organized by income/expense with totals
   - Net balance is calculated automatically

### Relationships
- **One-to-Many**: User → Categories (one user can have multiple categories)
- **One-to-Many**: User → Transactions (one user can have multiple transactions)
- **One-to-Many**: Category → Transactions (one category can have multiple transactions)
- **Cascade Delete**: Deleting a user removes all their categories and transactions

##  Code Architecture

### Model-View-Controller Pattern
The application follows a layered architecture:

#### Models (`db/models.py`)
- **User**: Represents user accounts with authentication
- **Category**: Represents transaction categories
- **Transaction**: Represents individual financial transactions
- **TransactionType**: Enum for income/expense classification

#### Helpers (`helpers.py`)
- **UserHelper**: User management operations (CRUD)
- **CategoryHelper**: Category management operations
- **TransactionHelper**: Transaction management operations
- **DisplayHelper**: Formatting and display utilities

#### View/Controller (`cli.py`)
- **FinanceTrackerCLI**: Main application class
- Menu systems and user interaction
- Input validation and error handling
- Application flow control
