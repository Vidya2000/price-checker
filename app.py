import streamlit as st
import sqlite3

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

    menu = ["Add Product", "View Products", "Update Product", "Delete Product"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_table()

    # ADD PRODUCT
    if choice == "Add Product":
        st.subheader("➕ Add a New Product")
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
    elif choice == "View Products":
        st.subheader("📋 Product List")
        products = view_products()
        if products:
            st.dataframe(products, use_container_width=True, hide_index=True,
                         column_config={
                             0: "Product ID",
                             1: "Product Name",
                             2: "Price",
                             3: "Stock"
                         })
        else:
            st.info("No products available.")

    # UPDATE PRODUCT
    elif choice == "Update Product":
        st.subheader("✏️ Update Product")
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
    elif choice == "Delete Product":
        st.subheader("🗑️ Delete Product")
        products = view_products()
        product_ids = [p[0] for p in products]

        if product_ids:
            selected_id = st.selectbox("Select Product ID to Delete", product_ids)
            if st.button("Delete"):
                delete_product(selected_id)
                st.success(f"✅ Product '{selected_id}' deleted successfully!")
        else:
            st.info("No products available to delete.")


if __name__ == "__main__":
    main()
