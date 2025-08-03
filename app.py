import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("Products.csv")

# Set page config
st.set_page_config(page_title="Price Checker", layout="centered")

# Title
st.markdown("<h2 style='text-align: center;'>📦 Product Price Checker</h2>", unsafe_allow_html=True)
st.markdown("---")

# Product ID dropdown
product_ids = df['Product ID'].tolist()
selected_id = st.selectbox("Select Product ID", options=product_ids)

# Fetch product info
result = df[df['Product ID'] == selected_id]
if not result.empty:
    name = result.iloc[0]['Product Name']
    price = result.iloc[0]['Price']
    st.success(f"✅ Product: **{name}**\n💰 Price: ₹{price}")
else:
    st.error("❌ Product not found.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
