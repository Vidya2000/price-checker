import streamlit as st
import sqlite3

DB_NAME = "products.db"

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_product(product_id, name, price):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO products (id, name, price) VALUES (?, ?, ?)", (product_id, name, price))
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
    c.execute("SELECT id, name, price FROM products WHERE id = ?", (product_id,))
    product = c.fetchone()
    conn.close()
    return product

def delete_product(product_id):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# ---------- UI ----------
def admin_page():
    st.subheader("🔐 Admin Panel")

    menu = ["Add Product", "View Products", "Search Product", "Delete Product"]
    choice = st.sidebar.selectbox("Choose Action", menu)

    if choice == "Add Product":
        st.subheader("➕ Add a New Product")
        product_id = st.number_input("Enter Product ID", min_value=1, step=1)
        name = st.text_input("Enter Product Name")
        price = st.number_input("Enter Product Price", min_value=0.0, format="%.2f")
        if st.button("Add Product"):
            add_product(product_id, name, price)
            st.success(f"✅ Product '{name}' added with ID {product_id}")

    elif choice == "View Products":
        st.subheader("📦 Product List")
        products = fetch_products()
        if products:
            for p in products:
                st.write(f"🆔 {p[0]} | 📦 {p[1]} | 💰 {p[2]}")
        else:
            st.warning("No products found.")

    elif choice == "Search Product":
        st.subheader("🔍 Search Product by ID")
        search_id = st.number_input("Enter Product ID", min_value=1, step=1)
        if st.button("Search"):
            product = fetch_product_by_id(search_id)
            if product:
                st.success(f"Found: 🆔 {product[0]} | 📦 {product[1]} | 💰 {product[2]}")
            else:
                st.error("❌ Product not found.")

    elif choice == "Delete Product":
        st.subheader("🗑 Delete Product")
        del_id = st.number_input("Enter Product ID to Delete", min_value=1, step=1)
        if st.button("Delete"):
            delete_product(del_id)
            st.success(f"✅ Product with ID {del_id} deleted.")


def user_page():
    st.subheader("👤 User Panel")
    st.write("Browse and search products (No login required).")

    option = st.radio("Choose Action", ["View Products", "Search Product"])

    if option == "View Products":
        st.subheader("📦 Product List")
        products = fetch_products()
        if products:
            for p in products:
                st.write(f"🆔 {p[0]} | 📦 {p[1]} | 💰 {p[2]}")
        else:
            st.warning("No products available.")

    elif option == "Search Product":
        st.subheader("🔍 Search Product by ID")
        search_id = st.number_input("Enter Product ID", min_value=1, step=1)
        if st.button("Search"):
            product = fetch_product_by_id(search_id)
            if product:
                st.success(f"Found: 🆔 {product[0]} | 📦 {product[1]} | 💰 {product[2]}")
            else:
                st.error("❌ Product not found.")

# ---------- Main ----------
def main():
    st.title("🛒 Price Checker App")
    init_db()

    role = st.radio("Select Role", ["User", "Admin"])

    if role == "Admin":
        password = st.text_input("Enter Admin Password", type="password")
        if password == "admin123":  # simple password check
            admin_page()
        else:
            st.error("Invalid Password")
    else:
        user_page()

if __name__ == "__main__":
    main()
