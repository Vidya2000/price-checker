import streamlit as st
import sqlite3

# Database setup
conn = sqlite3.connect('products.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        price INTEGER
    )
''')
conn.commit()

# Session states
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# Welcome message
if not st.session_state.admin_logged_in and not st.session_state.show_login:
    st.success("### Welcome to Veerabhadreshwara Enterprises")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("**Admin Login**", key="welcome_login"):
        st.session_state.show_login = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Admin login form
if st.session_state.show_login and not st.session_state.admin_logged_in:
    admin_password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login", key="admin_login"):
        if admin_password == "admin123":  # Change password here
            st.session_state.admin_logged_in = True
            st.session_state.show_login = False
            st.success("✅ Logged in as Admin")
            st.rerun()  # Immediate refresh after login
        else:
            st.error("❌ Incorrect Password")
    if st.button("Back", key="back_btn"):
        st.session_state.show_login = False
        st.rerun()

# Logout button for admin
if st.session_state.admin_logged_in:
    if st.button("Logout", key="admin_logout"):
        st.session_state.admin_logged_in = False
        st.success("✅ Logged out successfully")
        st.rerun()

# Admin panel (Add / Edit / Delete)
if st.session_state.admin_logged_in:
    st.subheader("➕ Add New Product")
    new_id = st.text_input("Product ID (e.g., B101)")
    new_name = st.text_input("Product Name")
    new_price = st.number_input("Product Price (₹)", min_value=0, step=1)

    if st.button("Add Product", key="add_product"):
        try:
            c.execute("INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
                      (new_id.strip(), new_name.strip(), new_price))
            conn.commit()
            st.success("✅ Product added successfully!")
        except sqlite3.IntegrityError:
            st.error("❌ Product ID already exists!")

    st.subheader("✏️ Edit or 🗑️ Delete Product")
    c.execute("SELECT id, name, price FROM products")
    products = c.fetchall()

    if products:
        selected_product = st.selectbox(
            "Select Product to Edit/Delete",
            [f"{p[0]} - {p[1]} (₹{p[2]})" for p in products]
        )
        prod_id = selected_product.split(" - ")[0]

        edit_name = st.text_input("Edit Product Name",
                                  value=[p[1] for p in products if p[0] == prod_id][0])
        edit_price = st.number_input("Edit Product Price (₹)",
                                     min_value=0, step=1,
                                     value=[p[2] for p in products if p[0] == prod_id][0])

        if st.button("Update Product", key="update_product"):
            c.execute("UPDATE products SET name = ?, price = ? WHERE id = ?",
                      (edit_name.strip(), edit_price, prod_id))
            conn.commit()
            st.success("✅ Product updated successfully!")

        if st.button("Delete Product", key="delete_product"):
            c.execute("DELETE FROM products WHERE id = ?", (prod_id,))
            conn.commit()
            st.warning("🗑️ Product deleted successfully!")
    else:
        st.info("No products found in the database.")

# Price Checker (Visible for all)
st.markdown("### 🔍 Check Product Price")
product_id = st.text_input("**Enter Product ID (e.g., B101):**")

if st.button("Check Price", key="check_price"):
    c.execute("SELECT name, price FROM products WHERE id = ?", (product_id.strip(),))
    result = c.fetchone()

    if result:
        st.markdown(f"**✅ Product:** {result[0]}")
        st.markdown(f"**💰 Price:** ₹{result[1]}")
    else:
        st.error("❌ Product not found!")

conn.close()
