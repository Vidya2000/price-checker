import streamlit as st
import sqlite3

# -------------------- DATABASE SETUP --------------------
conn = sqlite3.connect('products.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        price INTEGER
    )
''')
conn.commit()

# -------------------- SESSION STATE --------------------
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "login_error" not in st.session_state:
    st.session_state.login_error = ""

# -------------------- CALLBACKS --------------------
def show_login_form():
    st.session_state.show_login = True

def hide_login_form():
    st.session_state.show_login = False

def login():
    if st.session_state.admin_password == "admin123":  # Change password here
        st.session_state.admin_logged_in = True
        st.session_state.show_login = False
        st.session_state.login_error = ""
    else:
        st.session_state.login_error = "❌ Incorrect Password"

def logout():
    st.session_state.admin_logged_in = False
    st.session_state.show_login = False

# -------------------- WELCOME / LOGIN --------------------
if not st.session_state.admin_logged_in and not st.session_state.show_login:
    st.success("### Welcome to Veerabhadreshwara Enterprises")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.button("**Admin Login**", on_click=show_login_form)
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.show_login and not st.session_state.admin_logged_in:
    st.text_input("Enter Admin Password", type="password", key="admin_password")
    if st.session_state.login_error:
        st.error(st.session_state.login_error)
    st.button("Login", on_click=login)
    st.button("Back", on_click=hide_login_form)

# -------------------- ADMIN PANEL --------------------
if st.session_state.admin_logged_in:
    st.success("✅ Logged in as Admin")
    st.button("Logout", on_click=logout)

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

    st.subheader("✏️ Edit / 🗑 Delete Products")
    c.execute("SELECT * FROM products")
    products = c.fetchall()

    if products:
        for pid, pname, price in products:
            col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
            with col1:
                st.write(f"**{pid}**")
            with col2:
                new_name = st.text_input(f"Name ({pid})", value=pname, key=f"name_{pid}")
            with col3:
                new_price = st.number_input(f"Price ({pid})", value=price, step=1, key=f"price_{pid}")
            with col4:
                if st.button(f"Update {pid}"):
                    c.execute("UPDATE products SET name=?, price=? WHERE id=?", 
                              (new_name.strip(), new_price, pid))
                    conn.commit()
                    st.success(f"✅ Updated {pid}")
                    st.experimental_rerun()
                if st.button(f"Delete {pid}"):
                    c.execute("DELETE FROM products WHERE id=?", (pid,))
                    conn.commit()
                    st.warning(f"🗑 Deleted {pid}")
                    st.experimental_rerun()
    else:
        st.info("No products found.")

# -------------------- PRICE CHECKER FOR ALL USERS --------------------
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
