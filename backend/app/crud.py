import csv
from datetime import datetime

FILENAME = "transactions.csv"
HEADERS = ["Date", "Amount", "Category", "Description"]

def create_transaction(amount, category, description):
    """Creates (adds) a new transaction to the CSV file."""
    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), amount, category, description])
    print(f"Transaction added: {amount}, {category}, {description}")


def read_transactions():
    """Reads and displays all transactions from the CSV file."""
    try:
        with open(FILENAME, "r", newline="") as file:
            reader = csv.reader(file)
            header_row = next(reader)  # Skip the header row
            for row in reader:
                print(f"Date: {row[0]}, Amount: {row[1]}, Category: {row[2]}, Description: {row[3]}")
    except FileNotFoundError:
        print("No transactions found yet.")


def update_transaction(transaction_index, new_amount=None, new_category=None, new_description=None):
    """Updates an existing transaction based on its index (row number)."""
    transactions = []
    try:
        with open(FILENAME, "r", newline="") as file:
            reader = csv.reader(file)
            header_row = next(reader)
            transactions.append(header_row)  # Include header in memory
            for row in reader:
                transactions.append(row)

        if 0 < transaction_index < len(transactions):
            if new_amount:
                transactions[transaction_index][1] = new_amount
            if new_category:
                transactions[transaction_index][2] = new_category
            if new_description:
                transactions[transaction_index][3] = new_description

            with open(FILENAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(transactions)
            print(f"Transaction {transaction_index} updated successfully.")
        else:
            print("Invalid transaction index.")
    except FileNotFoundError:
        print("No transactions found to update.")


def delete_transaction(transaction_index):
    """Deletes a transaction based on its index (row number)."""
    transactions = []
    try:
        with open(FILENAME, "r", newline="") as file:
            reader = csv.reader(file)
            header_row = next(reader)
            transactions.append(header_row)  # Include header in memory
            for row in reader:
                transactions.append(row)

        if 0 < transaction_index < len(transactions):
            del transactions[transaction_index]

            with open(FILENAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(transactions)
            print(f"Transaction {transaction_index} deleted successfully.")
        else:
            print("Invalid transaction index.")
    except FileNotFoundError:
        print("No transactions found to delete.")


if __name__ == "__main__":
    # Example Usage
    create_transaction(-75.50, "Restaurant", "Dinner with friends")
    read_transactions()
    update_transaction(2, new_amount=1200.00, new_description="Monthly salary payment")
    read_transactions()
    delete_transaction(1)
    read_transactions()
