from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

class Expense:
    def __init__(self,description :str, amount :float, date :str):
        self.description = description
        self.amount = amount
        self.date = date

    def to_dict(self):
        """Convert the Expense object to a dictionary for MongoDB."""
        mongo_data = {
            'description' : self.description,
            'amount' : self.amount,
            'date' : self.date
        }
        return mongo_data


class ExpenseTracker:
    def __init__(self,dburl= 'mongodb://localhost:27017/', dbname='ExpenseDB', collection='expenses'):
        self.connection = MongoClient(dburl)
        self.db = self.connection[dbname]
        self.expense = self.db[collection]

    def option(self):
        while True:
            print('\nPersonal Expense Tracker')
            print('1. Add New Expense\n2. View All Expenses\n3. View Total Expenses\n4. Delete an Expense\n5. Exit')
            option = input('Enter your option ( 1 - 5 ) :').strip()
            if option == '1':
                self.add_expense()
            elif option == '2':
                self.view_all_expense()
            elif option == '3':
                self.view_total_expense()
            elif option == '4':
                self.delete_expense()
            elif option == '5':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 5.")


    def add_expense(self):
        """Add a new expense to MongoDB."""
        description = input('Enter expense description: ').strip()
        # Amount validation
        try:
            amount = float(input('Enter expense amount: ').strip())
            if amount <= 0:
                print("Invalid amount! Please enter a positive number.")
                return
        except Exception as error:
            print(error)
            return
        # Date validation
        date = input('Enter expense date (YYYY-MM-DD): ').strip()
        if not self.valid_date(date):
            print('Invalid date format! Please enter date as YYYY-MM-DD.')
            return
        result = Expense(description, amount, date)
        insert_result = self.expense.insert_one(result.to_dict())
        print(f'Data Inserted at ID : {insert_result.inserted_id}')


    def view_all_expense(self):
        """Retrieve and display all expenses."""
        expense_lst = list(self.expense.find())
        if not expense_lst:
            print("\nNo expenses found.")
            return
        print("\nAll Expenses:\n")
        for data in expense_lst:
            print(f"ID          : {data['_id']}")
            print(f"Description : {data['description']}")
            print(f"Amount      : ${data['amount']}")
            print(f"Date        : {data['date']}")
            print("-" * 30)


    def view_total_expense(self):
        """Calculate and display the total amount spent."""
        total = sum(data['amount'] for data in self.expense.find())
        if total == 0:
            print("\nNo expenses found.")
        else:
            print(f"\nTotal Expenses : ${total}")

    def delete_expense(self):
        """Delete an expense by its ID."""
        self.view_all_expense()
        expense_lst = list(self.expense.find())
        if not expense_lst:
            print("\nNo expenses to delete.")
            return
        del_expense = input("Enter the ID of the expenses you want to delete : ").strip()
        if not ObjectId.is_valid(del_expense):
            print("Invalid ID format.")
            return
        result = self.expense.delete_one({'_id' : ObjectId(del_expense)})
        if result.deleted_count > 0:
            print("Expense deleted successfully.")
        else:
            print("Expense not found.")

    def valid_date(self,date_str):
        """Validate date format as YYYY-MM-DD."""
        try:
            if datetime.strptime(date_str, '%Y-%m-%d'):
                return True
        except Exception as error:
            return False


if __name__=='__main__':
    tracker = ExpenseTracker()
    tracker.option()
