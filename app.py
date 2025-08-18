import streamlit as st
import sqlite3
import os

# Permanent database location inside the Streamlit app directory
DB_NAME = os.path.join(os.path.dirname(__file__), "products.db")

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS products (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 price REAL NOT NULL)""")
    conn.commit()
    conn.close()

def fetch_products():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT id, name, price FROM products")
    products = c.fetchall()
    conn.close()
    return products

def fetch_product_by_id(product_id):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT name, price FROM products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    return product

def add_product(name, price):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()

def update_product(prod_id, name, price):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE products SET name = ?, price = ? WHERE id = ?", (name, price, prod_id))
    conn.commit()
    conn.close()

def delete_product(prod_id):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (prod_id,))
    conn.commit()
    conn.close()

# Streamlit App
st.title("📦 Product Manager")

# Initialize DB on first run
init_db()

menu = ["View Products", "Add Product", "Edit Product", "Delete Product"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Products":
    st.subheader("All Products")
    products = fetch_products()
    if products:
        for prod in products:
            st.write(f"ID: {prod[0]} | Name: {prod[1]} | Price: ${prod[2]:.2f}")
    else:
        st.info("No products found. Add some!")

elif choice == "Add Product":
    st.subheader("Add a New Product")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    if st.button("Add"):
        if name.strip():
            add_product(name.strip(), price)
            st.success(f"✅ Product '{name}' added successfully!")
        else:
            st.warning("⚠ Please enter a product name")

elif choice == "Edit Product":
    st.subheader("Edit Product")
    products = fetch_products()
    if products:
        prod_id = st.selectbox("Select Product ID", [p[0] for p in products])
        product = fetch_product_by_id(prod_id)
        if product:
            new_name = st.text_input("New Name", product[0])
            new_price = st.number_input("New Price", value=product[1], format="%.2f")
            if st.button("Update"):
                update_product(prod_id, new_name.strip(), new_price)
                st.success("✅ Product updated successfully!")
    else:
        st.info("No products to edit.")

elif choice == "Delete Product":
    st.subheader("Delete Product")
    products = fetch_products()
    if products:
        prod_id = st.selectbox("Select Product ID", [p[0] for p in products])
        if st.button("Delete"):
            delete_product(prod_id)
            st.success("🗑️ Product deleted successfully!")
    else:
        st.info("No products to delete.")
