import streamlit as st
import pandas as pd

# Load the product data
df = pd.read_csv("Products.csv")

# Convert Product ID column to string (just in case)
df['Product ID'] = df['Product ID'].astype(str)

# Page settings
st.set_page_config(page_title="Price Checker", layout="centered")

# Title
st.markdown("<h2 style='text-align: center;'>🔍 Product Price Checker</h2>", unsafe_allow_html=True)
st.markdown("---")

# Text input for Product ID
product_id = st.text_input("Enter Product ID (e.g., b101, cb103, ...)", "").strip()

# Lookup
if product_id:
    result = df[df['Product ID'].str.lower() == product_id.lower()]
    if not result.empty:
        name = result.iloc[0]['Product Name']
        price = result.iloc[0]['Price']
        st.success(f"✅ Product: **{name}**\n💰 Price: ₹{price}")
    else:
        st.warning("⚠️ Product ID not found. Please check and try again.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
