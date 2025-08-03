import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("Products.csv")

# Set page config for better mobile display
st.set_page_config(page_title="Price Checker", layout="centered")

# App title
st.markdown("<h2 style='text-align: center;'>📦 Product Price Checker</h2>", unsafe_allow_html=True)
st.markdown("---")

# Input section
st.markdown("### 🔍 Enter Product ID to Check Price:")

product_id = st.text_input("Product ID", key="product_id")

# Button
if st.button("Check Price"):
    if product_id.strip() == "":
        st.warning("Please enter a Product ID.")
    else:
        try:
            product_id_int = int(product_id)
            result = df[df['Product ID'] == product_id_int]
            if not result.empty:
                name = result.iloc[0]['Product Name']
                price = result.iloc[0]['Price']
                st.success(f"✅ Product: **{name}**\n💰 Price: ₹{price}")
            else:
                st.error("❌ Product ID not found.")
        except ValueError:
            st.error("❌ Please enter a valid numeric Product ID.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
