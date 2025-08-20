import streamlit as st
import sqlite3
import pandas as pd

# ---------- DATABASE FUNCTIONS ----------
def create_table():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id TEXT PRIMARY KEY, name TEXT, price REAL, stock INTEGER)''')
    conn.commit()
    conn.close()

def add_product(product_id, name, price, stock):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
              (product_id, name, price, stock))
    conn.commit()
    conn.close()

def view_products():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT id, name, price, stock FROM products")
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_product_by_id(product_id):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT id, name, price, stock FROM products WHERE id=?", (product_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_product(product_id, name, price, stock):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, price=?, stock=? WHERE id=?",
              (name, price, stock, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


# ---------- STREAMLIT UI ----------
def main():
    st.title("📦 Inventory Management System")

    create_table()

    # Session state for login
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # --- ADMIN LOGIN SECTION ---
    if not st.session_state.logged_in:
        st.subheader("🔑 Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.success("✅ Login successful! You now have admin access.")
            else:
                st.error("❌ Invalid username or password")
    else:
        st.success("✅ Logged in as Admin")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

        # --- ADMIN FEATURES ---
        st.subheader("🛠️ Admin Controls")
        tabs = st.tabs(["➕ Add Product", "📋 View Products", "✏️ Update Product", "🗑️ Delete Product"])

        # ADD PRODUCT
        with tabs[0]:
            st.subheader("Add a New Product")
            product_id = st.text_input("Enter Product ID")
            name = st.text_input("Enter Product Name")
            price = st.number_input("Enter Price", min_value=0.0, format="%.2f")
            stock = st.number_input("Enter Stock", min_value=0, step=1)

            if st.button("Add Product"):
                if product_id.strip() == "":
                    st.error("⚠️ Product ID cannot be empty!")
                else:
                    try:
                        add_product(product_id, name, price, stock)
                        st.success(f"✅ Product '{name}' added successfully!")
                    except sqlite3.IntegrityError:
                        st.error("❌ Product ID already exists!")

        # VIEW PRODUCTS
        with tabs[1]:
            st.subheader("All Products")
            products = view_products()
            if products:
                df = pd.DataFrame(products, columns=["Product ID", "Product Name", "Price", "Stock"])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No products available.")

        # UPDATE PRODUCT
        with tabs[2]:
            st.subheader("Update Product")
            products = view_products()
            product_ids = [p[0] for p in products]

            if product_ids:
                selected_id = st.selectbox("Select Product ID to Update", product_ids)
                product = [p for p in products if p[0] == selected_id][0]

                new_name = st.text_input("Product Name", value=product[1])
                new_price = st.number_input("Price", min_value=0.0, value=product[2], format="%.2f")
                new_stock = st.number_input("Stock", min_value=0, value=product[3], step=1)

                if st.button("Update"):
                    update_product(selected_id, new_name, new_price, new_stock)
                    st.success(f"✅ Product '{selected_id}' updated successfully!")
            else:
                st.info("No products available to update.")

        # DELETE PRODUCT
        with tabs[3]:
            st.subheader("Delete Product")
            products = view_products()
            product_ids = [p[0] for p in products]

            if product_ids:
                selected_id = st.selectbox("Select Product ID to Delete", product_ids)
                if st.button("Delete"):
                    delete_product(selected_id)
                    st.success(f"✅ Product '{selected_id}' deleted successfully!")
            else:
                st.info("No products available to delete.")

    # --- SEARCH PRODUCT (Dropdown + Manual in one) ---
    st.subheader("🔍 Search Product")

    products = view_products()
    product_ids = [p[0] for p in products]

    search_mode = st.selectbox("Select or Enter Product ID", ["Manual Entry"] + product_ids)

    if search_mode == "Manual Entry":
        search_id = st.text_input("Enter Product ID manually")
    else:
        search_id = search_mode

    if st.button("Search"):
        if search_id.strip() != "":
            product = fetch_product_by_id(search_id)
            if product:
                df = pd.DataFrame([product], columns=["Product ID", "Product Name", "Price", "Stock"])
                st.dataframe(df, use_container_width=True)
            else:
                st.error("❌ Product not found")
        else:
            st.warning("⚠️ Please enter a valid Product ID")


if __name__ == "__main__":
    main()
