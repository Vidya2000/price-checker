import streamlit as st
import pandas as pd
import os

# ---------- CONFIG ----------
SALE_PASSWORD = "sell123"   # password for selling (different from admin password)
CSV_FILE = "products.csv"

# ---------- CSV FUNCTIONS ----------
def create_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["id", "name", "price", "stock"])
        df.to_csv(CSV_FILE, index=False)

def view_products():
    create_csv()
    df = pd.read_csv(CSV_FILE)
    return df.to_dict("records")

def fetch_product_by_id(product_id):
    df = pd.read_csv(CSV_FILE)
    product = df[df["id"] == product_id]
    return product.iloc[0].to_dict() if not product.empty else None

def add_product(product_id, name, price, stock):
    df = pd.read_csv(CSV_FILE)
    if product_id in df["id"].values:
        raise ValueError("Product ID already exists!")
    df = pd.concat([df, pd.DataFrame([{"id": product_id, "name": name, "price": price, "stock": stock}])])
    df.to_csv(CSV_FILE, index=False)

def update_product(product_id, name, price, stock):
    df = pd.read_csv(CSV_FILE)
    df.loc[df["id"] == product_id, ["name", "price", "stock"]] = [name, price, stock]
    df.to_csv(CSV_FILE, index=False)

def delete_product(product_id):
    df = pd.read_csv(CSV_FILE)
    df = df[df["id"] != product_id]
    df.to_csv(CSV_FILE, index=False)

def reduce_stock(product_id, quantity):
    df = pd.read_csv(CSV_FILE)
    idx = df.index[df["id"] == product_id].tolist()
    if not idx:
        return False
    idx = idx[0]
    if df.at[idx, "stock"] >= quantity:
        df.at[idx, "stock"] -= quantity
        df.to_csv(CSV_FILE, index=False)
        return True
    else:
        return False

# ---------- STREAMLIT UI ----------
def main():
    st.title("📦 Inventory Management System (CSV Version)")

    create_csv()

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
                    except ValueError:
                        st.error("❌ Product ID already exists!")

        # VIEW PRODUCTS
        with tabs[1]:
            st.subheader("All Products")
            products = view_products()
            if products:
                df = pd.DataFrame(products)
                df = df.rename(columns={"id": "Product ID", "name": "Product Name", "price": "Price", "stock": "Stock"})
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No products available.")

        # UPDATE PRODUCT
        with tabs[2]:
            st.subheader("Update Product")
            products = view_products()
            product_ids = [p["id"] for p in products]

            if product_ids:
                selected_id = st.selectbox("Select Product ID to Update", product_ids)
                product = fetch_product_by_id(selected_id)

                new_name = st.text_input("Product Name", value=product["name"])
                new_price = st.number_input("Price", min_value=0.0, value=product["price"], format="%.2f")
                new_stock = st.number_input("Stock", min_value=0, value=product["stock"], step=1)

                if st.button("Update"):
                    update_product(selected_id, new_name, new_price, new_stock)
                    st.success(f"✅ Product '{selected_id}' updated successfully!")
            else:
                st.info("No products available to update.")

        # DELETE PRODUCT
        with tabs[3]:
            st.subheader("Delete Product")
            products = view_products()
            product_ids = [p["id"] for p in products]

            if product_ids:
                selected_id = st.selectbox("Select Product ID to Delete", product_ids)
                if st.button("Delete"):
                    delete_product(selected_id)
                    st.success(f"✅ Product '{selected_id}' deleted successfully!")
            else:
                st.info("No products available to delete.")

    # --- SEARCH PRODUCT (Dropdown with Sell Option) ---
    st.subheader("🔍 Search Product")
    products = view_products()
    product_ids = [p["id"] for p in products]

    if product_ids:
        search_id = st.selectbox("Select Product ID to Search", [""] + product_ids)

        if search_id != "":
            product = fetch_product_by_id(search_id)
            if product:
                df = pd.DataFrame([product])
                df = df.rename(columns={"id": "Product ID", "name": "Product Name", "price": "Price", "stock": "Stock"})
                st.dataframe(df, use_container_width=True)

                # Sell form
                with st.form("sell_form", clear_on_submit=True):
                    sale_password = st.text_input("Enter Sale Password", type="password")
                    qty = st.number_input("Quantity to Sell", min_value=1, step=1)
                    submitted = st.form_submit_button("Sell Product")

                    if submitted:
                        if sale_password == SALE_PASSWORD:
                            success = reduce_stock(search_id, qty)
                            if success:
                                st.success(f"✅ Sold {qty} units of '{product['name']}'. Stock updated!")
                                updated_product = fetch_product_by_id(search_id)
                                updated_df = pd.DataFrame([updated_product])
                                updated_df = updated_df.rename(columns={"id": "Product ID", "name": "Product Name", "price": "Price", "stock": "Stock"})
                                st.dataframe(updated_df, use_container_width=True)
                            else:
                                st.error("❌ Not enough stock available!")
                        else:
                            st.error("❌ Invalid Sale Password!")
    else:
        st.info("No products available to search.")


if __name__ == "__main__":
    main()
