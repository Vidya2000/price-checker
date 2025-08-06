import streamlit as st
import pandas as pd
import os

# CSV file
DATA_FILE = "Products.csv"

# Load existing data or create a new DataFrame
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Product ID", "Product Name", "Price"])

st.title("🔐 Login")

# Select role
role = st.selectbox("Select role", ["Viewer", "Admin"])
st.markdown("---")

# Viewer: Check product price
if role == "Viewer":
    st.header("🔍 Price Checker")
    product_id = st.text_input("**Enter Product ID**")
    
    if product_id:
        result = df[df['Product ID'].astype(str).str.lower() == product_id.lower()]
        if not result.empty:
            st.markdown(f"**Product**: {result.iloc[0]['Product Name']}")
            st.markdown(f"**Price**: ₹{result.iloc[0]['Price']}")
        else:
            st.error("Product not found.")

# Admin: Add product
elif role == "Admin":
    st.header("🛠 Admin Panel - Add Product")

    with st.form("add_product_form"):
        prod_id = st.text_input("Product ID")
        prod_name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0)

        submitted = st.form_submit_button("Add Product")
        if submitted:
            new_row = {
                "Product ID": prod_id,
                "Product Name": prod_name,
                "Price": price
            }
            df = df.append(new_row, ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Product added successfully!")
