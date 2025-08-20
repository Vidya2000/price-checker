import streamlit as st
import pandas as pd

# Load product data
products = pd.read_csv("Products.csv")

# App title
st.title("🛍️ Price Checker")

# Bold input label
st.markdown("**Enter Product ID:**")
product_id = st.text_input("", help="Example: b101, cb103, 101")

# Convert both input and CSV IDs to lowercase for case-insensitive matching
product = products[products["Product ID"].astype(str).str.lower() == product_id.lower()]

if product_id:
    if not product.empty:
        product = product.iloc[0]
        st.markdown(f"""
        ✅ **Product:** **{product['Product Name']}**  
        💰 **Price:** **₹{product['Price']}**
        """)
    else:
        st.error("❌ Product ID not found. Please try again.")
