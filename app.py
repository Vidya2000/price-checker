import streamlit as st
import sqlite3

# --- Welcome Message ---
st.markdown("<h1 style='text-align: center; color: green;'>Welcome to Veerabhadreshwara Enterprises</h1>", unsafe_allow_html=True)
st.markdown("---")

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

# --- Session State ---
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# --- Centered Admin Login ---
center_col = st.columns([1, 1, 1])[1]  # Middle column

with center_col:
    if not st.session_state.is_admin:
        if not st.session_state.show_login:
            if st.button("**🔑 Admin Login**"):  # Bold text
                st.session_state.show_login = True
        else:
            st.markdown("**Enter Admin Password**")
            password = st.text_input("", type="password", key="pwd")
            login_col, cancel_col = st.columns(2)
            with login_col:
                if st.button("Login"):
                    if password == "admin123":  # Change password here
                        st.session_state.is_admin = True
                        st.session_state.show_login = False
                    else:
                        st.error("❌ Incorrect password!")
            with cancel_col:
                if st.button("Cancel"):
                    st.session_state.show_login = False
    else:
        st.success("✅ Admin Mode Active")
        if st.button("🚪 Logout"):
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
