import sqlite3
import csv

DB_NAME = "inventory.db"


def init_db():
    """Initialize database with products table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()


def import_products_from_csv(filename):
    """Import products from CSV into database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO products (id, name, price, stock)
                    VALUES (?, ?, ?, ?)
                """, (row["id"], row["name"], float(row["price"]), int(row["stock"])))
            except Exception as e:
                print(f"Failed to insert row: {row} | Error: {e}")

    conn.commit()
    conn.close()
    print("Products imported successfully!")


def update_stock(product_id, quantity):
    """Update product stock after purchase"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT stock FROM products WHERE id = ?", (product_id,))
    result = cursor.fetchone()

    if result:
        current_stock = result[0]
        if current_stock >= quantity:
            cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, product_id))
            conn.commit()
            print("Stock updated successfully!")
        else:
            print("Not enough stock available.")
    else:
        print("Product not found.")

    conn.close()


def main():
    init_db()

    while True:
        print("\n===== Inventory Management =====")
        print("1. Import products from CSV")
        print("2. Update stock")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            filename = input("Enter CSV filename (e.g., products.csv): ")
            import_products_from_csv(filename)
        elif choice == "2":
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity to reduce: "))
            update_stock(product_id, quantity)
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
