import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("customers.json")


def load_customers():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            customers = json.load(file)
    except FileNotFoundError:
        return []

    if not isinstance(customers, list) or not all(
        isinstance(customer, dict)
        and all(
            isinstance(customer.get(field), str)
            for field in ("name", "phone", "notes")
        )
        for customer in customers
    ):
        raise ValueError("Invalid customer records.")

    return customers


def save_customers(customers):
    temporary_file = DATA_FILE.with_suffix(".json.tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(customers, file, indent=4)

    temporary_file.replace(DATA_FILE)


def required_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be blank.")


def display_customers(customers):
    if not customers:
        print("\nNo customers found.")
        return

    for customer in customers:
        print(f"\nName: {customer['name']}")
        print(f"Phone: {customer['phone']}")
        print(f"Notes: {customer['notes'] or 'None'}")


def add_customer(customers):
    customer = {
        "name": required_input("Customer name: "),
        "phone": required_input("Phone number: "),
        "notes": input("Notes (optional): ").strip(),
    }

    updated_customers = customers + [customer]

    try:
        save_customers(updated_customers)
    except OSError as error:
        print(f"\nCould not save customer: {error}")
        return

    customers.append(customer)
    print("\nCustomer saved!")


def search_customers(customers):
    query = required_input("Search by name: ").casefold()

    matches = [
        customer for customer in customers
        if query in customer["name"].casefold()
    ]

    display_customers(matches)


def main():
    try:
        customers = load_customers()
    except (OSError, ValueError) as error:
        print(f"Cannot load customers: {error}")
        print("Stopped without changing the saved file.")
        return

    while True:
        print("\nCustomer Tracker")
        print("1. Add customer")
        print("2. View all customers")
        print("3. Search by name")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_customer(customers)
        elif choice == "2":
            display_customers(customers)
        elif choice == "3":
            search_customers(customers)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
