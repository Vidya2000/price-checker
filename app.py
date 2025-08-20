import sqlite3

def add_product():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    stock = int(input("Enter stock quantity: "))

    cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()
    conn.close()
    print("✅ Product added successfully!")

def update_product():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    product_id = int(input("Enter product ID to update: "))
    new_price = float(input("Enter new price: "))
    new_stock = int(input("Enter new stock quantity: "))

    cursor.execute("UPDATE products SET price = ?, stock = ? WHERE id = ?", (new_price, new_stock, product_id))
    conn.commit()
    conn.close()
    print("✅ Product updated successfully!")

def delete_product():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    product_id = int(input("Enter product ID to delete: "))
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    print("🗑️ Product deleted successfully!")

def main():
    while True:
        print("\n--- Product Management ---")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
