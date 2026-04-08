import csv
import os
import matplotlib.pyplot as plt
FILENAME = "budget_data.csv"

def load_data():
    if not os.path.exists(FILENAME):
        return [], []
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        income = []
        expenses = []
        for row in reader:
            category, amount, kind = row
            if kind == "income":
                income.append((category, float(amount)))
            else:
                expenses.append((category, float(amount)))
        return income, expenses

def save_data(income, expenses):
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        for category, amount in income:
            writer.writerow([category, amount, "income"])
        for category, amount in expenses:
            writer.writerow([category, amount, "expense"])

def input_income():
    income = []
    print("\nEnter your sources of income:")
    while True:
        source = input("Source name (or type 'done'): ")
        if source.lower() == "done":
            break
        amount = float(input(f"Amount for {source}: $"))
        income.append((source, amount))
    return income

def input_expenses():
    expenses = []
    print("\nEnter your expenses:")
    while True:
        category = input("Expense category (or type 'done'): ")
        if category.lower() == "done":
            break
        amount = float(input(f"Amount for {category}: $"))
        expenses.append((category, amount))
    return expenses

def display_summary(income, expenses):
    total_income = sum(amount for _, amount in income)
    total_expenses = sum(amount for _, amount in expenses)
    balance = total_income - total_expenses

    print("\n--- Budget Summary ---")
    print(f"Total Income:    ${total_income:.2f}")
    print(f"Total Expenses:  ${total_expenses:.2f}")
    print(f"Remaining Balance: ${balance:.2f}")

    print("\n--- Expense Breakdown ---")
    print(f"{'Category':<20}{'Amount':>10}")
    print("-" * 30)
    for category, amount in expenses:
        print(f"{category:<20}${amount:>9.2f}")

    return total_income, total_expenses, balance

def plot_pie_chart(expenses):
    if not expenses:
        print("No expenses to plot.")
        return
    labels = [cat for cat, _ in expenses]
    amounts = [amt for _, amt in expenses]

    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution")
    plt.tight_layout()
    plt.show()

def main():
    print("=== Personal Budget Tracker ===")
    income, expenses = load_data()

    while True:
        print("\n1. Input Income")
        print("2. Input Expenses")
        print("3. View Summary")
        print("4. Save and Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            income += input_income()
        elif choice == "2":
            expenses += input_expenses()
        elif choice == "3":
            total_income, total_expenses, balance = display_summary(income, expenses)
            plot_pie_chart(expenses)
        elif choice == "4":
            save_data(income, expenses)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
