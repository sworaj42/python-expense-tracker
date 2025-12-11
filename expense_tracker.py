import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import csv


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


    while True: 
        date= input("Enter the date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date,"%Y-%m-%d")
            break
        except ValueError:
            print("Invalid input!, Enter in YYYY-MM-DD format.")


    description= input("Enter description: ").strip()

    category=input("Enter category (Food, Transport, Shopping, etc.): ").strip()
    if category=="":
        category="Other"

    while True:
        amount_str= input("Enter amount: ").strip()
        try:
             amount= float(amount_str)
             break
        except ValueError:
             print("Invalid amount, please enter a number.")

    expense={
        "date": date,
        "description": description,
        "category": category,
        "amount": amount
    }


    expenses.append(expense)
    save_expenses()
    print("Expense added successfully!")
    
def view_expense_by_day():
        print("\n--- View Expenses ---")
        target=input("Enter the date YYYY-MM-DD: ").strip()

        found=False
        total=0

        for exp in expenses:
            if target==exp['date']:
                found=True
                print(f"- category: {exp['category']} | {exp['description']} | {exp['amount']}")
                total+=exp["amount"]

        if not found:
            print("No expenses found for this date.")
        else:
            print(f"Total spending on {target}: {total}")

def view_monthly_summary():
    print("\n--- Monthly Summary ---")
    month = input("Enter month (YYYY-MM): ").strip()  

    total = 0
    by_category = {}
    found = False

    for exp in expenses:
        date_str = exp["date"]
        if date_str.startswith(month):   
            found = True
            amount = exp["amount"]
            total += amount

            cat = exp.get("category", "Other")
            if cat not in by_category:
                by_category[cat] = 0
            by_category[cat] += amount

    # If no matching expenses, stop here
    if not found:
        print("No expenses found for this month.")
        return

    # Text summary
    print(f"\nTotal spending in {month}: {total}")
    print("By category:")
    for cat, cat_total in by_category.items():
        print(f"- {cat}: {cat_total}")

    # Prepare data for bar chart
    categories = list(by_category.keys())
    amounts = list(by_category.values())

    # Show bar chart
    plt.figure(figsize=(8, 4))
    plt.bar(categories, amounts, color='skyblue')
    plt.title(f"Spending by Category for {month}")
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.tight_layout()
    plt.show()

    daily_totals = {}

    for exp in expenses:
        if exp["date"].startswith(month):
            day = int(exp["date"].split("-")[2])  # extract DD from YYYY-MM-DD
            daily_totals[day] = daily_totals.get(day, 0) + exp["amount"]

    # If somehow no daily totals exist, skip
    if not daily_totals:
        print("No daily data to plot.")
        return

    # Sort days
    days = sorted(daily_totals.keys())
    amounts_by_day = [daily_totals[day] for day in days]

    # Plot bar chart
    plt.figure(figsize=(9, 4))
    plt.bar(days, amounts_by_day, color='orange')
    plt.title(f"Daily Spending Trend for {month}")
    plt.xlabel("Day of Month")
    plt.ylabel("Amount Spent")
    plt.xticks(days)  # Show only the real days
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()



def view_all_expenses():
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    total = 0
    by_category = {}

    print(f"\n{'ID':<3}| {'Date':<12}| {'Category':<12}| {'Description':<25}| {'Amount'}")
    print("-" * 70)

    for idx, exp in enumerate(expenses, start=1):
        print(f"{idx:<3}| {exp['date']:<12}| {exp['category']:<12}| {exp['description']:<25}| {exp['amount']}")
        total += exp["amount"]

        # Build category totals
        cat = exp.get("category", "Other")
        by_category[cat] = by_category.get(cat, 0) + exp["amount"]

    print("-" * 70)
    print(f"Total of all expenses: {total}")

    # ---------- BAR CHART FOR ALL EXPENSES ----------
    categories = list(by_category.keys())
    amounts = list(by_category.values())

    plt.figure(figsize=(8, 4))
    plt.bar(categories, amounts, color='lightgreen')
    plt.title("Total Spending by Category (All Time)")
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.tight_layout()
    plt.show()

def delete_expense():
    print("\n--- Delete Expense ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    while True:
        # Always show the latest list with updated IDs
        view_all_expenses()

        choice = input("\nEnter the ID of the expense to delete (or press Enter to cancel): ").strip()

        if choice == "":
            print("Delete cancelled.")
            return

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        idx = int(choice)

        if 1 <= idx <= len(expenses):
            exp = expenses[idx - 1]
            confirm = input(
                f"Are you sure you want to delete this? "
                f"[{exp['date']} | {exp['category']} | {exp['description']} | {exp['amount']}] (y/n): "
            ).strip().lower()

            if confirm != "y":
                print("Delete skipped.")
            else:
                deleted = expenses.pop(idx - 1)
                save_expenses()
                print(
                    f"Deleted: {deleted['date']} | {deleted['category']} | "
                    f"{deleted['description']} | {deleted['amount']}"
                )

            # If no expenses left, stop immediately
            if not expenses:
                print("No more expenses left.")
                return

            # Ask if they want to delete another
            again = input("Delete another expense? (y/n): ").strip().lower()
            if again != "y":
                print("Finished deleting.")
                return

        else:
            view_all_expenses()
            print(f"Please enter a number between 1 and {len(expenses)}.")

def update_expense():
    print("\n--- Update Expense ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    # Show all so user can pick easily
    view_all_expenses()

    while True:
        choice = input("\nEnter the ID of the expense to update (or press Enter to cancel): ").strip()

        if choice == "":
            print("Update cancelled.")
            return

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        idx = int(choice)

        if 1 <= idx <= len(expenses):
            exp = expenses[idx - 1]
            break
        else:
            print(f"Please enter a number between 1 and {len(expenses)}.")

    print("\nLeave input empty and press Enter to keep the current value.")

    # --- Update date ---
    while True:
        new_date = input(f"New date [{exp['date']}] (YYYY-MM-DD): ").strip()
        if new_date == "":
            break  
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
            exp["date"] = new_date
            break
        except ValueError:
            print("Invalid date format! Please enter as YYYY-MM-DD.")

    # --- Update description ---
    new_desc = input(f"New description [{exp['description']}]: ").strip()
    if new_desc != "":
        exp["description"] = new_desc

    # --- Update category ---
    new_cat = input(f"New category [{exp['category']}]: ").strip()
    if new_cat != "":
        exp["category"] = new_cat

    # --- Update amount ---
    while True:
        new_amount_str = input(f"New amount [{exp['amount']}]: ").strip()
        if new_amount_str == "":
            break  # keep old

        try:
            new_amount = float(new_amount_str)
            exp["amount"] = new_amount
            break
        except ValueError:
            print("Invalid amount, please enter a number.")

    save_expenses()
    print("Expense updated successfully!")

def export_to_csv():
    print("\n--- Export to CSV ---")

    if not expenses:
        print("No expenses to export.")
        return

    filename = "expenses_export.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Header row
        writer.writerow(["date", "description", "category", "amount"])

        # Data rows
        for exp in expenses:
            writer.writerow([
                exp["date"],
                exp["description"],
                exp["category"],
                exp["amount"]
            ])

    print(f"Expenses successfully exported to {filename}")




def main():
    while True:
        print("\n---Expense Tracker---")
        print("\n1. Add expense.")
        print("2. View expenses for a day.")
        print("3. View monthly summary.")
        print("4. View all expenses.")
        print("5. Delete expense.")
        print("6. Update expense.")
        print("7.Export to CSV.")
        print("8. Exit")

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
            view_monthly_summary()

        elif choice=="4":
            view_all_expenses()

        elif choice=="5":
            delete_expense()

        elif choice=="6":
            update_expense()
        
        elif choice=="7":
            export_to_csv()

        elif choice=="8":
            print("You exited the main menu.")
            break
        else: 
            print("Invalid option, try again.")
if __name__ == "__main__":
    main()



