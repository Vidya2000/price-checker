import streamlit as st
import sqlite3

# Database setup
def create_table():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    # Make sure 'id' is NOT AUTOINCREMENT, so you can enter manually
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            stock INTEGER
        )
    """)
    conn.commit()
    conn.close()

def add_product(product_id, name, price, stock):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
                  (product_id, name, price, stock))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error(f"❌ Product ID {product_id} already exists. Please use a unique ID.")
    conn.close()

def view_products():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    data = c.fetchall()
    conn.close()
    return data

# Streamlit UI
def main():
    st.title("📦 Inventory Management")

    menu = ["Add Product", "View Products"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Product":
        st.subheader("➕ Add a New Product")

        product_id = st.number_input("Enter Product ID", min_value=1, step=1)
        name = st.text_input("Enter Product Name")
        price = st.number_input("Enter Price", min_value=0.0, step=0.1)
        stock = st.number_input("Enter Stock", min_value=0, step=1)

        if st.button("Add Product"):
            if name.strip() == "":
                st.error("Product name cannot be empty.")
            else:
                add_product(product_id, name, price, stock)
                st.success(f"✅ Added {name} (ID: {product_id}) successfully!")

    elif choice == "View Products":
        st.subheader("📋 Product List")
        products = view_products()
        if products:
            st.table(products)
        else:
            st.info("No products found.")

if __name__ == "__main__":
    create_table()
    main()
