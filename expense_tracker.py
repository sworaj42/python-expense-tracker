"""
Personal Expense Tracker (CLI Application)

Features:
- Add, update, and delete daily expenses
- View expenses by day and monthly summary
- Category-wise and daily visualizations using matplotlib
- Persistent storage using JSON
- Export expense data to CSV

This project demonstrates:
- Python OOP using dataclasses
- File handling (JSON, CSV)
- Input validation
- Basic data visualization

Author: Swaraj Sigdel
"""


import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import csv
from dataclasses import dataclass

FILE_NAME = "expenses.json"
CSV_EXPORT_NAME = "expenses_export.csv"


@dataclass
class Expense:
    date: str
    description: str
    category: str
    amount: float

    def to_dict(self):
        return {
            "date": self.date,
            "description": self.description,
            "category": self.category,
            "amount": self.amount
        }

    @staticmethod
    def from_dict(d):
        return Expense(
            date=d["date"],
            description=d["description"],
            category=d.get("category", "Other"),
            amount=float(d["amount"])
        )


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Expense.from_dict(item) for item in data]
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading expenses: {e}")
        return []


expenses = load_expenses()



def save_expenses():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump([exp.to_dict() for exp in expenses], f, indent=2)
    except IOError as e:
        print(f"Error saving expenses: {e}")


def add_expense():
    print("\n--- Add Expense ---")

    # get date
    while True:
        date = input("Enter the date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid input! Enter in YYYY-MM-DD format.")

    description = input("Enter description: ").strip()

    category = input("Enter category (Food, Transport, Shopping, etc.): ").strip()
    if category == "":
        category = "Other"

    # validate amount
    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid amount, please enter a number.")

    expense = Expense(date=date, description=description, category=category, amount=amount)
    expenses.append(expense)
    save_expenses()
    print("Expense added successfully!")


def view_expense_by_day():
    print("\n--- View Expenses by Day ---")

    while True:
        target = input("Enter the date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(target, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid input! Enter in YYYY-MM-DD format.")

    found = False
    total = 0

    print(f"\nExpenses for {target}:")
    print("-" * 60)

    for exp in expenses:
        if target == exp.date:
            found = True
            print(f"  {exp.category:<15} | {exp.description:<25} | Rs. {exp.amount:.2f}")
            total += exp.amount

    if not found:
        print("No expenses found for this date.")
    else:
        print("-" * 60)
        print(f"Total spending on {target}: Rs. {total:.2f}")


def view_monthly_summary():
    print("\n--- Monthly Summary ---")

    while True:
        month = input("Enter the month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
            break
        except ValueError:
            print("Invalid input! Enter in YYYY-MM format.")

    total = 0
    by_category = {}
    found = False

    for exp in expenses:
        date_str = exp.date
        if date_str.startswith(month):
            found = True
            amount = exp.amount
            total += amount

            cat = exp.category
            if cat not in by_category:
                by_category[cat] = 0
            by_category[cat] += amount

    if not found:
        print("No expenses found for this month.")
        return

    # print summary
    print(f"\nTotal spending in {month}: Rs. {total:.2f}")
    print("\nBy category:")
    for cat, cat_total in by_category.items():
        percentage = (cat_total / total) * 100
        print(f"  {cat:<15} Rs. {cat_total:>8.2f}  ({percentage:.1f}%)")

    # category chart
    categories = list(by_category.keys())
    amounts = list(by_category.values())

    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='skyblue', edgecolor='navy', alpha=0.7)
    plt.title(f"Spending by Category for {month}", fontsize=14, fontweight='bold')
    plt.xlabel("Category", fontsize=12)
    plt.ylabel("Amount Spent (Rs.)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.show()

    # daily spending trend
    daily_totals = {}

    for exp in expenses:
        if exp.date.startswith(month):
            day = int(exp.date.split("-")[2])
            daily_totals[day] = daily_totals.get(day, 0) + exp.amount

    if not daily_totals:
        print("No daily data to plot.")
        return

    days = sorted(daily_totals.keys())
    amounts_by_day = [daily_totals[day] for day in days]

    plt.figure(figsize=(12, 5))
    plt.bar(days, amounts_by_day, color='orange', edgecolor='darkorange', alpha=0.7)
    plt.title(f"Daily Spending Trend for {month}", fontsize=14, fontweight='bold')
    plt.xlabel("Day of Month", fontsize=12)
    plt.ylabel("Amount Spent (Rs.)", fontsize=12)
    plt.xticks(days)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()


def display_expenses_list(show_chart=True):
    """Helper function to display expenses table, optionally with chart"""
    if not expenses:
        print("No expenses recorded yet.")
        return 0, {}

    total = 0
    by_category = {}

    print(f"\n{'ID':<4} {'Date':<12} {'Category':<15} {'Description':<30} {'Amount (Rs.)'}")
    print("=" * 85)

    for idx, exp in enumerate(expenses, start=1):
        print(f"{idx:<4} {exp.date:<12} {exp.category:<15} {exp.description:<30} {exp.amount:>10.2f}")
        total += exp.amount

        cat = exp.category
        by_category[cat] = by_category.get(cat, 0) + exp.amount

    print("=" * 85)
    print(f"{'TOTAL':<61} Rs. {total:>10.2f}")

    # show chart if needed
    if show_chart and by_category:
        categories = list(by_category.keys())
        amounts = list(by_category.values())

        plt.figure(figsize=(10, 5))
        plt.bar(categories, amounts, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
        plt.title("Total Spending by Category (All Time)", fontsize=14, fontweight='bold')
        plt.xlabel("Category", fontsize=12)
        plt.ylabel("Amount Spent (Rs.)", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.show()

    return total, by_category


def view_all_expenses():
    print("\n--- All Expenses ---")
    display_expenses_list(show_chart=True)


def delete_expense():
    print("\n--- Delete Expense ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    while True:
        display_expenses_list(show_chart=False)

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
                f"Are you sure you want to delete this expense?\n"
                f"  [{exp.date} | {exp.category} | {exp.description} | Rs. {exp.amount:.2f}]\n"
                f"Confirm (y/n): "
            ).strip().lower()

            if confirm != "y":
                print("Delete skipped.")
            else:
                deleted = expenses.pop(idx - 1)
                save_expenses()
                print(f"Deleted: {deleted.date} | {deleted.category} | {deleted.description} | Rs. {deleted.amount:.2f}")

            if not expenses:
                print("No more expenses left.")
                return

            again = input("\nDelete another expense? (y/n): ").strip().lower()
            if again != "y":
                print("Finished deleting.")
                return

        else:
            print(f"Please enter a number between 1 and {len(expenses)}.")


def update_expense():
    print("\n--- Update Expense ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    display_expenses_list(show_chart=False)

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

    # update date
    while True:
        new_date = input(f"New date [{exp.date}] (YYYY-MM-DD): ").strip()
        if new_date == "":
            break
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
            exp.date = new_date
            break
        except ValueError:
            print("Invalid date format! Please enter as YYYY-MM-DD.")

    # update description
    new_desc = input(f"New description [{exp.description}]: ").strip()
    if new_desc != "":
        exp.description = new_desc

    # update category
    new_cat = input(f"New category [{exp.category}]: ").strip()
    if new_cat != "":
        exp.category = new_cat

    # update amount
    while True:
        new_amount_str = input(f"New amount [Rs. {exp.amount:.2f}]: ").strip()
        if new_amount_str == "":
            break

        try:
            new_amount = float(new_amount_str)
            if new_amount <= 0:
                print("Amount must be greater than 0.")
                continue
            exp.amount = new_amount
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

    try:
        with open(CSV_EXPORT_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Description", "Category", "Amount (Rs.)"])

            for exp in expenses:
                writer.writerow([
                    exp.date,
                    exp.description,
                    exp.category,
                    f"{exp.amount:.2f}"
                ])

        print(f"Expenses successfully exported to {CSV_EXPORT_NAME}")
    except IOError as e:
        print(f"Error exporting to CSV: {e}")


def main():
    while True:
        print("\n" + "=" * 50)
        print("           PERSONAL EXPENSE TRACKER")
        print("=" * 50)
        print("\n  1. Add expense")
        print("  2. View expenses for a day")
        print("  3. View monthly summary")
        print("  4. View all expenses")
        print("  5. Delete expense")
        print("  6. Update expense")
        print("  7. Export to CSV")
        print("  8. Exit")
        print("-" * 50)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expense_by_day()

        elif choice == "3":
            view_monthly_summary()

        elif choice == "4":
            view_all_expenses()

        elif choice == "5":
            delete_expense()

        elif choice == "6":
            update_expense()

        elif choice == "7":
            export_to_csv()

        elif choice == "8":
            print("\n" + "=" * 50)
            print("  Thank you for using Personal Expense Tracker!")
            print("=" * 50)
            break

        else:
            print("Invalid option. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()