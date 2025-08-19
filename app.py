import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "products.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Add product
def add_product(id, name, price, stock):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)", (id, name, price, stock))
    conn.commit()
    conn.close()

# View products
def view_products():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM products", conn)
    conn.close()
    return df

# Import products from CSV
def import_csv(file):
    df = pd.read_csv(file)
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("products", conn, if_exists="append", index=False)
    conn.close()

# App UI
def main():
    st.title("Inventory Management System")

    menu = ["Add Product", "View Products", "Import CSV"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Product":
        st.subheader("Add Product")
        id = st.number_input("Product ID", min_value=1, step=1)
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0.0, step=0.1)
        stock = st.number_input("Stock", min_value=0, step=1)
        if st.button("Add"):
            add_product(id, name, price, stock)
            st.success(f"Product '{name}' added successfully!")

    elif choice == "View Products":
        st.subheader("Product List")
        st.dataframe(view_products())

    elif choice == "Import CSV":
        st.subheader("Import Products from CSV")
        file = st.file_uploader("Upload CSV", type=["csv"])
        if file is not None:
            try:
                import_csv(file)
                st.success("CSV imported successfully!")
                st.dataframe(view_products())
            except Exception as e:
                st.error(f"Import failed: {e}")

if __name__ == "__main__":
    init_db()
    main()
