import csv
import os
from datetime import datetime

# --- Global Variables and Constants ---
EXPENSES_FILE = "expenses.csv"
# The list will hold expense dictionaries in memory
expenses = [] 
# Defined categories for easy categorization
CATEGORIES = ["Food", "Housing", "Transport", "Income", "Other"]

# --- Week 4: File Handling Functions ---

def load_expenses():
    """
    Loads expenses from the CSV file into the global 'expenses' list.
    Handles the case where the file does not exist (FileNotFoundError).
    """
    global expenses
    expenses = [] # Clear current list before loading
    
    # Check if the file exists before attempting to read
    if not os.path.exists(EXPENSES_FILE):
        print(f"⚠️ Data file '{EXPENSES_FILE}' not found. Starting with an empty tracker.")
        return

    try:
        # Use 'with open' for safe file handling (automatically closes the file)
        with open(EXPENSES_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert 'amount' back to a float for calculations
                try:
                    row['amount'] = float(row['amount'])
                    expenses.append(row)
                except ValueError:
                    # Basic error handling for corrupted data lines
                    print(f"❌ Skipping invalid data entry: {row}")
        print(f"✅ Loaded {len(expenses)} transactions from {EXPENSES_FILE}.")
        
    except Exception as e:
        print(f"❌ An error occurred during file loading: {e}")

def save_expenses():
    """
    Saves the current list of expenses to the CSV file.
    """
    if not expenses:
        print("📭 No data to save.")
        return

    # The fieldnames match the keys in our expense dictionaries
    fieldnames = ['date', 'category', 'description', 'amount']
    
    try:
        # 'w' mode overwrites the file with current data
        with open(EXPENSES_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # Write the header row
            writer.writeheader()
            
            # Write the data rows
            writer.writerows(expenses)
        print(f"✅ Successfully saved {len(expenses)} transactions to {EXPENSES_FILE}.")
        
    except Exception as e:
        # Error handling for file writing issues
        print(f"❌ An error occurred during file saving: {e}")

# --- Week 3: Functions and Dictionaries ---

def add_expense():
    """
    Allows the user to input a new expense/income transaction.
    """
    print("\n--- Add New Transaction ---")
    
    # Get Date
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"Date set to: {date_str}")
    
    # Get Category (using control flow for selection)
    print("Available categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
        
    while True:
        try:
            choice = int(input("Select category number (1-5): "))
            if 1 <= choice <= len(CATEGORIES):
                category = CATEGORIES[choice - 1]
                break
            else:
                print("🚫 Invalid number. Please select from 1 to 5.")
        except ValueError:
            print("🚫 Invalid input. Please enter a number.")
            
    # Get Amount (using try-except for error handling)
    while True:
        try:
            amount_input = float(input("Enter amount (positive for income/negative for expense): "))
            amount = round(amount_input, 2)
            break
        except ValueError:
            print("🚫 Invalid amount. Please enter a number (e.g., -55.50 or 500.00).")

    # Get Description (Working with Strings)
    description = input("Enter description (optional): ").strip()

    # Create Dictionary entry
    new_expense = {
        'date': date_str,
        'category': category,
        'description': description,
        'amount': amount
    }
    
    # Store result in List
    expenses.append(new_expense)
    print(f"\n✨ Transaction added: {category} of {amount} on {date_str}")

def generate_monthly_report():
    """
    Analyzes and displays expenses categorized by category.
    """
    if not expenses:
        print("\n📭 No transactions recorded to generate a report.")
        return

    # Dictionaries: Use a dictionary to aggregate totals by category
    category_totals = {cat: 0.0 for cat in CATEGORIES}
    total_net = 0.0

    # Week 2: FOR loop to iterate through the list of expense dictionaries
    for expense in expenses:
        amount = expense.get('amount', 0)
        category = expense.get('category', 'Other')
        
        # Aggregate totals
        if category in category_totals:
            category_totals[category] += amount
        else:
            # Handle unexpected categories just in case
            category_totals['Other'] += amount
            
        total_net += amount

    print("\n--- Monthly Finance Report ---")
    print(f"Total Net Balance: ${total_net:,.2f}")
    print("\nBreakdown by Category:")
    
    # Displaying the totals
    for category, total in category_totals.items():
        # Using String formatting for alignment and clarity
        print(f"  {category:<10}: ${total:,.2f}")
    print("----------------------------")

def view_transactions():
    """
    Displays all recorded transactions.
    """
    if not expenses:
        print("\n📭 No transactions recorded.")
        return
    
    print("\n--- All Recorded Transactions ---")
    print(f"{'Date':<10} | {'Category':<10} | {'Amount':<10} | Description")
    print("-" * 50)
    for exp in expenses:
        # String formatting for clear table view
        amount_str = f"{exp['amount']:,.2f}"
        print(f"{exp['date']:<10} | {exp['category']:<10} | {amount_str:<10} | {exp['description']}")
    print("-" * 50)


# --- Main Program Control Flow ---

def main_menu():
    """
    The main control function that runs the program.
    """
    load_expenses() # Load data when program starts
    
    # Week 2: WHILE loop to keep the program running
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Generate Monthly Report")
        print("4. Save & Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            generate_monthly_report()
        elif choice == '4':
            save_expenses() # Save before exiting
            print("👋 Thank you for using the tracker. Goodbye!")
            break
        else:
            # Basic error handling for menu choice
            print("🚫 Invalid choice. Please enter a number from 1 to 4.")

# Execute the main function
if __name__ == "__main__":
    main_menu()
