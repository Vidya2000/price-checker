import streamlit as st
import sqlite3

# --- Welcome Message ---
st.markdown("<h1 style='text-align: center; color: green;'>Welcome to Veerabhadreshwara Enterprises</h1>", unsafe_allow_html=True)
st.markdown("---")  # Adds a horizontal line

st.title("🛒 Price Checker")

# --- Database Connection ---
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        price INTEGER
    )
''')
conn.commit()

# --- Admin Login State ---
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "login_attempted" not in st.session_state:
    st.session_state.login_attempted = False

# --- Sidebar Login ---
st.sidebar.header("Admin Login")

if not st.session_state.is_admin:
    admin_password = st.sidebar.text_input("Enter Admin Password", type="password")
    if st.sidebar.button("Login"):
        st.session_state.login_attempted = True
        if admin_password == "admin123":  # Set your own password
            st.session_state.is_admin = True
            st.session_state.login_attempted = False
        else:
            st.session_state.is_admin = False

    if st.session_state.login_attempted and not st.session_state.is_admin:
        st.sidebar.error("❌ Incorrect password!")
else:
    st.sidebar.success("✅ Logged in as Admin")
    if st.sidebar.button("Logout"):
        st.session_state.is_admin = False

# --- Admin Panel ---
if st.session_state.is_admin:
    st.subheader("➕ Add New Product")
    new_id = st.text_input("Product ID (e.g., B101)")
    new_name = st.text_input("Product Name")
    new_price = st.number_input("Product Price (₹)", min_value=0, step=1)

    if st.button("Add Product"):
        try:
            c.execute("INSERT INTO products (id, name, price) VALUES (?, ?, ?)", 
                      (new_id.strip(), new_name.strip(), new_price))
            conn.commit()
            st.success("✅ Product added successfully!")
        except sqlite3.IntegrityError:
            st.error("❌ Product ID already exists!")

# --- Price Checker ---
st.markdown("### 🔍 Check Product Price")
product_id = st.text_input("**Enter Product ID (e.g., B101):**")

if st.button("Check Price"):
    c.execute("SELECT name, price FROM products WHERE id = ?", (product_id.strip(),))
    result = c.fetchone()

    if result:
        st.markdown(f"**✅ Product:** {result[0]}")
        st.markdown(f"**💰 Price:** ₹{result[1]}")
    else:
        st.error("❌ Product not found!")

conn.close()
