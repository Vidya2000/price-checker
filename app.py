import sqlite3

# Connect to database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL)''')
conn.commit()


# Add Product
def add_product():
    try:
        id = int(input("Enter Product ID: "))
        name = input("Enter Product Name: ")
        price = float(input("Enter Product Price: "))
        stock = int(input("Enter Stock Quantity: "))

        cursor.execute("INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
                       (id, name, price, stock))
        conn.commit()
        print("✅ Product added successfully!\n")
    except sqlite3.IntegrityError:
        print("❌ Error: Product ID already exists!\n")


# Update Product
def update_product():
    id = int(input("Enter Product ID to update: "))
    cursor.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cursor.fetchone()

    if product:
        name = input(f"Enter new name ({product[1]}): ") or product[1]
        price = input(f"Enter new price ({product[2]}): ") or product[2]
        stock = input(f"Enter new stock ({product[3]}): ") or product[3]

        cursor.execute("UPDATE products SET name=?, price=?, stock=? WHERE id=?",
                       (name, float(price), int(stock), id))
        conn.commit()
        print("✅ Product updated successfully!\n")
    else:
        print("❌ Product not found!\n")


# Delete Product
def delete_product():
    id = int(input("Enter Product ID to delete: "))
    cursor.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    print("✅ Product deleted successfully!\n")


# Search Product
def search_product():
    keyword = input("Enter product name or ID to search: ")
    cursor.execute("SELECT * FROM products WHERE name LIKE ? OR id LIKE ?", 
                   (f"%{keyword}%", f"%{keyword}%"))
    results = cursor.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("❌ No product found.\n")


# Menu
def menu():
    while True:
        print("\n====== Inventory Management ======")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Search Product")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            search_product()
        elif choice == "5":
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Try again.\n")


if __name__ == "__main__":
    menu()
    conn.close()
