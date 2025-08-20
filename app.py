import sqlite3
import csv

DB_NAME = "inventory.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

# ---------------- Core Features ----------------

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock: "))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()
    conn.close()
    print("✅ Product added successfully!")

def update_product():
    product_id = int(input("Enter product ID to update: "))
    name = input("Enter new name: ")
    price = float(input("Enter new price: "))
    stock = int(input("Enter new stock: "))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=?, price=?, stock=? WHERE id=?", (name, price, stock, product_id))
    conn.commit()
    conn.close()
    print("✅ Product updated successfully!")

def delete_product():
    product_id = int(input("Enter product ID to delete: "))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    print("🗑️ Product deleted successfully!")

def search_product():
    keyword = input("Enter product name to search: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + keyword + '%',))
    products = cursor.fetchall()
    conn.close()

    if products:
        print("\nSearch Results:")
        for row in products:
            print(row)
    else:
        print("❌ No product found.")

# ---------------- Import & Export ----------------

def import_products():
    filename = input("Enter CSV filename to import (e.g., Products.csv): ")

    conn = connect_db()
    cursor = conn.cursor()

    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    cursor.execute("INSERT OR IGNORE INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
                                   (row['id'], row['name'], row['price'], row['stock']))
                except Exception as e:
                    print(f"⚠️ Failed to insert row: {row} | Error: {e}")
        conn.commit()
        print("✅ Products imported successfully!")
    except FileNotFoundError:
        print("❌ File not found.")
    conn.close()

def export_products():
    filename = input("Enter CSV filename to export (e.g., ExportedProducts.csv): ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "name", "price", "stock"])  # Header
        writer.writerows(products)

    print(f"✅ Products exported successfully to {filename}!")

# ---------------- Main Menu ----------------

def main():
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Search Product")
        print("5. Import Products from CSV")
        print("6. Export Products to CSV")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            update_product()
        elif choice == '3':
            delete_product()
        elif choice == '4':
            search_product()
        elif choice == '5':
            import_products()
        elif choice == '6':
            export_products()
        elif choice == '7':
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
