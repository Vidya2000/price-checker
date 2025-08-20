import streamlit as st
import sqlite3
import pandas as pd

# ---------- DATABASE FUNCTIONS ----------
def create_table():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (product_id TEXT PRIMARY KEY, 
                  name TEXT, 
                  quantity INTEGER, 
                  price REAL)''')
    conn.commit()
    conn.close()

def add_product(product_id, name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)", 
              (product_id, name, quantity, price))
    conn.commit()
    conn.close()

def update_stock(product_id, quantity):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("UPDATE products SET quantity = quantity - ? WHERE product_id = ? AND quantity >= ?", 
              (quantity, product_id, quantity))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect("inventory.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

# ---------- APP START ----------
create_table()
st.title("📦 Inventory Management System")

# ---------- ADD PRODUCT ----------
st.subheader("➕ Add Product")
with st.form("add_product_form"):
    product_id = st.text_input("Product ID")
    name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    price = st.number_input("Price ($)", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Product")

    if submitted:
        if product_id and name:
            add_product(product_id, name, quantity, price)
            st.success(f"✅ Product {name} added successfully!")
        else:
            st.warning("⚠️ Please fill all fields")

# ---------- SEARCH PRODUCT ----------
st.subheader("🔍 Search Product")

conn = sqlite3.connect("inventory.db")
c = conn.cursor()
c.execute("SELECT product_id FROM products")
product_ids = [row[0] for row in c.fetchall()]
conn.close()

selected_id = st.selectbox("Select Product ID", [""] + product_ids)

if selected_id != "":
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE product_id=?", (selected_id,))
    product = c.fetchone()
    conn.close()

    if product:
        st.write(f"**Product ID:** {product[0]}")
        st.write(f"**Name:** {product[1]}")
        st.write(f"**Quantity:** {product[2]}")
        st.write(f"**Price:** ${product[3]}")
    else:
        st.warning("⚠️ Product not found")

# ---------- PURCHASE PRODUCT ----------
st.subheader("🛒 Purchase Product")
with st.form("purchase_form"):
    purchase_id = st.selectbox("Select Product ID to Purchase", [""] + product_ids)
    purchase_qty = st.number_input("Purchase Quantity", min_value=1, step=1)
    purchase_btn = st.form_submit_button("Purchase")

    if purchase_btn:
        if purchase_id != "":
            conn = sqlite3.connect("inventory.db")
            c = conn.cursor()
            c.execute("SELECT quantity, name FROM products WHERE product_id=?", (purchase_id,))
            result = c.fetchone()
            conn.close()

            if result:
                available_qty, pname = result
                if purchase_qty <= available_qty:
                    update_stock(purchase_id, purchase_qty)
                    st.success(f"✅ Purchased {purchase_qty} of {pname}")
                else:
                    st.error(f"❌ Only {available_qty} available")
            else:
                st.error("⚠️ Product not found")
        else:
            st.warning("⚠️ Please select a product")

# ---------- VIEW INVENTORY ----------
st.subheader("📋 Inventory")
df = get_all_products()
st.dataframe(df)
