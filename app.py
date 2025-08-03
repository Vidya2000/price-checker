import streamlit as st
import pandas as pd

# Load the CSV
df = pd.read_csv("products.csv")

st.title("🛒 Price Checker App")

product_name = st.selectbox("Select a product", df["Product Name"])

if product_name:
    product_info = df[df["Product Name"] == product_name].iloc[0]
    st.write(f"**Product ID**: {product_info['Product ID']}")
    st.write(f"**Price**: ₹{product_info['Price']}")
