import streamlit as st
import pandas as pd

# Load the CSV
df = pd.read_csv("Products.csv")

st.title("🛍️ Price Checker")

# Show dropdown with Product ID
selected_id = st.selectbox("Select Product ID", df['Product ID'].unique())

# Get product details for selected ID
product = df[df['Product ID'] == selected_id].iloc[0]

# Show details
st.subheader("Product Details")
st.write(f"**Product Name:** {product['Product Name']}")
st.write(f"**Price:** ₹{product['Price']}")
