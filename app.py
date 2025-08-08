import streamlit as st
import sqlite3

DB_NAME = 'products.db'

# Initialize DB (run once)
def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            price INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_product(new_id, new_name, new_price):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO products (id, name, price) VALUES (?, ?, ?)", 
                  (new_id, new_name, new_price))
        conn.commit()
    finally:
        conn.close()

def update_product(prod_id, edit_name, edit_price):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute("UPDATE products SET name = ?, price = ? WHERE id = ?", 
                  (edit_name, edit_price, prod_id))
        conn.commit()
    finally:
        conn.close()

def delete_product(prod_id):
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM products WHERE id = ?", (prod_id,))
        conn.commit()
    finally:
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

# Initialize DB at app start
init_db()

# Session states for login management
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# Welcome message and admin login button
if not st.session_state.admin_logged_in and not st.session_state.show_login:
    st.success("### Welcome to Veerabhadreshwara Enterprises")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("**Admin Login**", key="welcome_login"):
        st.session_state.show_login = True
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Admin login form
if st.session_state.show_login and not st.session_state.admin_logged_in:
    admin_password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login", key="admin_login"):
        if admin_password == "admin123":  # Change your password here
            st.session_state.admin_logged_in = True
            st.session_state.show_login = False
            st.success("✅ Logged in as Admin")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect Password")
    if st.button("Back", key="back_btn"):
        st.session_state.show_login = False
        st.experimental_rerun()

# Logout button
if st.session_state.admin_logged_in:
    if st.button("Logout", key="admin_logout"):
        st.session_state.admin_logged_in = False
        st.success("✅ Logged out successfully")
        st.experimental_rerun()

# Admin panel (Add/Edit/Delete)
if st.session_state.admin_logged_in:
    st.subheader("➕ Add New Product")
    new_id = st.text_input("Product ID (e.g., B101)")
    new_name = st.text_input("Product Name")
    new_price = st.number_input("Product Price (₹)", min_value=0, step=1)

    if st.button("Add Product", key="add_product"):
        if not new_id.strip() or not new_name.strip():
            st.error("❌ Product ID and Name cannot be empty.")
        else:
            try:
                add_product(new_id.strip(), new_name.strip(), new_price)
                st.success("✅ Product added successfully!")
                st.experimental_rerun()
            except sqlite3.IntegrityError:
                st.error("❌ Product ID already exists!")

    st.subheader("✏️ Edit or 🗑️ Delete Product")
    products = fetch_products()

    if products:
        selected_product = st.selectbox(
            "Select Product to Edit/Delete",
            [f"{p[0]} - {p[1]} (₹{p[2]})" for p in products]
        )
        prod_id = selected_product.split(" - ")[0]

        # Pre-fill edit fields
        edit_name = st.text_input("Edit Product Name",
                                  value=[p[1] for p in products if p[0] == prod_id][0])
        edit_price = st.number_input("Edit Product Price (₹)",
                                     min_value=0, step=1,
                                     value=[p[2] for p in products if p[0] == prod_id][0])

        if st.button("Update Product", key="update_product"):
            update_product(prod_id, edit_name.strip(), edit_price)
            st.success("✅ Product updated successfully!")
            st.experimental_rerun()

        if st.button("Delete Product", key="delete_product"):
            delete_product(prod_id)
            st.warning("🗑️ Product deleted successfully!")
            st.experimental_rerun()
    else:
        st.info("No products found in the database.")

# Price checker for all users
st.markdown("### 🔍 Check Product Price")
product_id = st.text_input("**Enter Product ID (e.g., B101):**")

if st.button("Check Price", key="check_price"):
    product = fetch_product_by_id(product_id.strip())
    if product:
        st.markdown(f"**✅ Product:** {product[0]}")
        st.markdown(f"**💰 Price:** ₹{product[1]}")
    else:
        st.error("❌ Product not found!")
