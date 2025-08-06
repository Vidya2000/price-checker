import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("ProductDatabase").sheet1  # use your actual sheet name

# Get data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# UI
st.title("📦 Product Price Checker")

product_id = st.text_input("**Enter Product ID:**")

if product_id:
    result = df[df['Product ID'].str.lower() == product_id.lower()]
    if not result.empty:
        row = result.iloc[0]
        st.markdown(f"**✅ Product:** {row['Product Name']}")
        st.markdown(f"**💰 Price:** ₹{row['Price']}")
    else:
        st.error("Product not found.")

# Admin section
st.markdown("---")
st.markdown("### 🔐 Admin: Add New Product")
with st.form("admin_form"):
    new_id = st.text_input("New Product ID")
    new_name = st.text_input("Product Name")
    new_price = st.number_input("Price", min_value=1)
    submitted = st.form_submit_button("Add Product")

    if submitted and new_id and new_name:
        sheet.append_row([new_id, new_name, new_price])
        st.success("Product added successfully!")
