import streamlit as st
import sqlite3

DB_NAME = "products.db"

# ---------- DATABASE FUNCTIONS ----------
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id TEXT PRIMARY KEY, name TEXT, price REAL)''')
    conn.commit()
    conn.close()

def add_product(product_id, name, price):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO products (id, name, price) VALUES (?, ?, ?)", 
                  (product_id, name, price))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("⚠️ Product ID already exists. Please choose another ID.")
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

def delete_product(product_id):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

# ---------- APP ----------
init_db()

# Login system
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🛒 Product Management System")

if not st.session_state.logged_in:
    st.success("Welcome! Please log in to continue.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid credentials")
else:
    st.sidebar.success("✅ Logged in as admin")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    menu = st.sidebar.radio("Navigation", ["Add Product", "View Products", "Search Product", "Delete Product"])

    if menu == "Add Product":
        st.subheader("➕ Add a New Product")
        product_id = st.text_input("Enter Product ID (unique)")
        name = st.text_input("Product Name")
        price = st.number_input("Product Price", min_value=0.0, step=0.1)

        if st.button("Add Product"):
            if product_id.strip() == "" or name.strip() == "":
                st.error("⚠️ Product ID and Name cannot be empty")
            else:
                add_product(product_id, name, price)
                st.success(f"✅ Product '{name}' added successfully with ID {product_id}")

    elif menu == "View Products":
        st.subheader("📦 All Products")
        products = fetch_products()
        if products:
            for p in products:
                st.write(f"🆔 {p[0]} | **{p[1]}** - 💲{p[2]}")
        else:
            st.info("No products found.")

    elif menu == "Search Product":
        st.subheader("🔍 Search Product by ID")
        search_id = st.text_input("Enter Product ID to search")
        if st.button("Search"):
            product = fetch_product_by_id(search_id)
            if product:
                st.success(f"✅ Found: {product[0]} - 💲{product[1]}")
            else:
                st.error("❌ Product not found")

    elif menu == "Delete Product":
        st.subheader("🗑️ Delete Product by ID")
        del_id = st.text_input("Enter Product ID to delete")
        if st.button("Delete"):
            product = fetch_product_by_id(del_id)
            if product:
                delete_product(del_id)
                st.success(f"✅ Product with ID {del_id} deleted")
            else:
                st.error("❌ Product ID not found")
