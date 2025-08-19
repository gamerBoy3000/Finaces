import Crud  # Your Crud.py should contain the actual data-handling functions

def display_menu():
    """Presents the main menu options to the user."""
    print("\n--- Personal Finance Tracker ---")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Update Transaction")
    print("4. Delete Transaction")
    print("5. Exit")

def get_transaction_details():
    """Prompts the user for transaction details."""
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category (e.g., Food, Rent, Salary): ")
        description = input("Enter description: ")
        return {"amount": amount, "category": category, "description": description}
    except ValueError:
        print("Invalid input. Please enter a valid number for amount.")
        return None

def main():
    """Main loop for the finance tracker application."""
    while True:
        display_menu()
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            details = get_transaction_details()
            if details:
                Crud.add_transaction(details)
        elif choice == "2":
            Crud.view_transactions()
        elif choice == "3":
            try:
                txn_id = int(input("Enter the transaction ID to update: "))
                details = get_transaction_details()
                if details:
                    Crud.update_transaction(txn_id, details)
            except ValueError:
                print("Invalid ID format.")
        elif choice == "4":
            try:
                txn_id = int(input("Enter the transaction ID to delete: "))
                Crud.delete_transaction(txn_id)
            except ValueError:
                print("Invalid ID format.")
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please select from 1 to 5.")

if __name__ == "__main__":
    main()

