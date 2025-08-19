import streamlit as st
import sqlite3

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --- Add Product ---
def add_product(product_id, name, price, stock):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
                  (product_id, name, price, stock))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Product ID already exists. Please use a different ID.")
    conn.close()

# --- Update Stock ---
def update_stock(product_id, new_stock):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, product_id))
    conn.commit()
    conn.close()

# --- Get All Products ---
def get_all_products():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return rows

# --- Streamlit UI ---
def main():
    st.title("📦 Inventory Management System")

    menu = ["Add Product", "Update Stock", "View Products"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Product":
        st.subheader("➕ Add a New Product")
        product_id = st.text_input("Product ID")
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.01)
        stock = st.number_input("Stock", min_value=0, step=1)

        if st.button("Add Product"):
            if product_id and name:
                add_product(product_id, name, price, stock)
                st.success(f"✅ Product '{name}' added successfully!")
            else:
                st.error("Please enter both Product ID and Name.")

    elif choice == "Update Stock":
        st.subheader("✏️ Update Product Stock")
        product_id = st.text_input("Enter Product ID")
        new_stock = st.number_input("New Stock", min_value=0, step=1)

        if st.button("Update Stock"):
            update_stock(product_id, new_stock)
            st.success(f"✅ Stock updated for Product ID: {product_id}")

    elif choice == "View Products":
        st.subheader("📋 Product List")
        products = get_all_products()
        if products:
            st.table(products)
        else:
            st.info("No products found.")

if __name__ == "__main__":
    init_db()
    main()
