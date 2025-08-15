from datetime import datetime

class Category:
    """Represents a category for financial transactions (e.g., Groceries, Salary, Utilities)."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Transaction:
    """Represents a single financial transaction."""
    def __init__(self, amount, category, description="", date=None):
        self.amount = float(amount)  # Ensure amount is a float
        self.category = category  # Assign a Category object
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return f"Date: {self.date}, Amount: {self.amount}, Category: {self.category}, Description: {self.description}"

# Example Usage
if __name__ == "__main__":
    groceries_category = Category("Groceries")
    salary_category = Category("Income")

    transaction1 = Transaction(-50.00, groceries_category, "Bought snacks and drinks")
    transaction2 = Transaction(1500.00, salary_category, "Monthly salary")

    print(transaction1)
    print(transaction2)

    # You could later add methods to update or delete transactions within the class
