import streamlit as st
import sqlite3

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    price REAL,
                    stock INTEGER
                )''')
    conn.commit()
    conn.close()

# ---------- Add Product ----------
def add_product(product_id, name, price, stock):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
                  (product_id, name, price, stock))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("❌ Product ID already exists. Please use a unique ID.")
    conn.close()

# ---------- View Products ----------
def view_products():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT id, name, price, stock FROM products")
    rows = c.fetchall()
    conn.close()
    return rows

# ---------- Main Streamlit App ----------
def main():
    st.title("📦 Inventory Management System")

    menu = ["Add Product", "View Products"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Product":
        st.subheader("➕ Add a New Product")

        product_id = st.text_input("Enter Product ID")
        name = st.text_input("Enter Product Name")
        price = st.number_input("Enter Price", min_value=0.0, format="%.2f")
        stock = st.number_input("Enter Stock", min_value=0, step=1)

        if st.button("Add Product"):
            if product_id.strip() == "":
                st.error("⚠️ Product ID cannot be empty!")
            else:
                add_product(product_id, name, price, stock)
                st.success(f"✅ Product '{name}' added successfully!")

    elif choice == "View Products":
        st.subheader("📋 Product List")
        products = view_products()
        if products:
            import pandas as pd
            df = pd.DataFrame(products, columns=["Product ID", "Product Name", "Price", "Stock"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No products available.")

# Run app
if __name__ == '__main__':
    init_db()
    main()
