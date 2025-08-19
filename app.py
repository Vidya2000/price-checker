import streamlit as st
import sqlite3

# ========== DATABASE SETUP ==========
def init_db():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    price REAL,
                    stock INTEGER
                )''')
    conn.commit()
    conn.close()

def add_product(product_id, name, price, stock):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
                  (product_id, name, price, stock))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("❌ Product ID already exists! Please use a unique ID.")
    conn.close()

def view_products():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    data = c.fetchall()
    conn.close()
    return data

def update_stock(product_id, new_stock):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


# ========== STREAMLIT UI ==========
st.title("📦 Inventory Management System")

menu = ["Add Product", "View Products", "Update Stock", "Delete Product"]
choice = st.sidebar.selectbox("Menu", menu)

init_db()  # Initialize database

# Add Product
if choice == "Add Product":
    st.subheader("➕ Add New Product")
    product_id = st.text_input("Product ID (Enter manually)")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    stock = st.number_input("Stock Quantity", min_value=0, step=1)

    if st.button("Add Product"):
        if product_id.strip() == "":
            st.error("⚠️ Product ID cannot be empty.")
        else:
            add_product(product_id, name, price, stock)
            st.success(f"✅ Product '{name}' added successfully!")

# View Products
elif choice == "View Products":
    st.subheader("📋 Product List")
    products = view_products()
    if products:
        st.table(products)
    else:
        st.info("No products found.")

# Update Stock
elif choice == "Update Stock":
    st.subheader("✏️ Update Stock")
    products = view_products()
    product_ids = [p[0] for p in products]

    if product_ids:
        product_id = st.selectbox("Select Product ID", product_ids)
        new_stock = st.number_input("Enter New Stock", min_value=0, step=1)
        if st.button("Update Stock"):
            update_stock(product_id, new_stock)
            st.success(f"✅ Stock updated for Product ID {product_id}")
    else:
        st.warning("No products available to update.")

# Delete Product
elif choice == "Delete Product":
    st.subheader("🗑️ Delete Product")
    products = view_products()
    product_ids = [p[0] for p in products]

    if product_ids:
        product_id = st.selectbox("Select Product ID to Delete", product_ids)
        if st.button("Delete"):
            delete_product(product_id)
            st.success(f"✅ Product {product_id} deleted successfully")
    else:
        st.warning("No products available to delete.")
