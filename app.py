import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("Products.csv")

# Set page config
st.set_page_config(page_title="Price Checker", layout="centered")

# Title
st.markdown("<h2 style='text-align: center;'>📦 Product Price Checker</h2>", unsafe_allow_html=True)
st.markdown("---")

# Create dropdown options: "101 - Notebook", etc.
dropdown_options = [f"{row['Product ID']} - {row['Product Name']}" for _, row in df.iterrows()]

selected_option = st.selectbox("Select Product", options=dropdown_options)

# Extract Product ID from selected dropdown value
product_id = int(selected_option.split(" - ")[0])

# Show result
result = df[df['Product ID'] == product_id]
if not result.empty:
    name = result.iloc[0]['Product Name']
    price = result.iloc[0]['Price']
    st.success(f"✅ Product: **{name}**\n💰 Price: ₹{price}")
else:
    st.error("❌ Product ID not found.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
