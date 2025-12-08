import json
import os

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME,"r") as f:
        return json.load(f)

FILE_NAME="expenses.json"
expenses=load_expenses()

def save_expenses():
    with open(FILE_NAME,"w") as f:
        json.dump(expenses, f, indent=2)


# Function for adding expense functionality
def add_expense():
    print("\n--- Add Expense ---")

    date= input("Enter the date (YYYY-MM-DD): ")
    description= input("Enter description: ")

    amount_str= input("Enter amount: ")
    amount= float(amount_str)

    expense={
        "date": date,
        "description": description,
        "amount": amount
    }


    expenses.append(expense)
    save_expenses()
    print("Expense added successfully!")
    
def view_expense_by_day():
        print("\n--- View Expenses ---")
        target=input("Enter the date YYYY-MM-DD: ")

        found=False
        total=0

        for exp in expenses:
            if target==exp['date']:
                found=True
                print(f"- {exp['description']} | {exp['amount']}")
                total+=exp["amount"]

        if not found:
            print("No expenses found for this date.")
        else:
            print(f"Total spending on {target}: {total}")

        

        

def main():
    while True:
        print("---Expense Tracker---")
        print("1. Add expense")
        print("2. View expenses for a day")
        print("3.Exit")
        
        choice=input("Enter your choice: ")

        if choice=="1":
            print("Add expense selected")
            add_expense()
            continue

        elif choice=="2":
            print("View expense")
            view_expense_by_day()
            continue

        elif choice=="3":
            print("You exited the main menu.")
            break
        else:
            print("Invalid option, try again.")
if __name__ == "__main__":
    main()



