import streamlit as st
import sqlite3
import pandas as pd
import io
import re

DB_PATH = "products.db"

# ---------------------- DB Helpers ----------------------
def get_conn():
    # check_same_thread=False helps with Streamlit's reruns
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

def fetch_all_df():
    conn = get_conn()
    df = pd.read_sql_query("SELECT id, name, price, stock FROM products ORDER BY id;", conn)
    conn.close()
    return df

def upsert_products(df):
    """Insert or update rows by id (UPSERT)."""
    conn = get_conn()
    c = conn.cursor()
    # INSERT OR REPLACE keeps primary key identity but replaces the row
    c.executemany(
        "INSERT OR REPLACE INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
        list(df[["id", "name", "price", "stock"]].itertuples(index=False, name=None))
    )
    conn.commit()
    conn.close()

def replace_all_products(df):
    """Clear table then bulk insert."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM products;")
    conn.commit()
    conn.close()
    upsert_products(df)

# ---------------------- CSV Validation/Cleaning ----------------------
REQUIRED = {"id", "name", "price", "stock"}

def normalize_header(col: str) -> str:
    """
    Make headers case/space/underscore-insensitive,
    and map common variants to required names.
    """
    base = re.sub(r"[\s_]+", "", col.strip().lower())
    mapping = {
        "id": "id",
        "productid": "id",
        "product_id": "id",
        "productid#": "id",

        "name": "name",
        "productname": "name",

        "price": "price",
        "mrp": "price",
        "sellingprice": "price",

        "stock": "stock",
        "qty": "stock",
        "quantity": "stock",
        "available": "stock",
    }
    return mapping.get(base, col)  # default to original if unknown

def clean_and_validate_csv(df_raw: pd.DataFrame):
    # 1) Normalize headers
    df = df_raw.copy()
    df.columns = [normalize_header(c) for c in df.columns]

    # 2) Ensure required columns exist
    missing = REQUIRED - set(df.columns.str.lower())
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")

    # 3) Keep only required in correct order
    df = df[[ "id", "name", "price", "stock" ]]

    # 4) Trim whitespace in text fields
    df["id"]   = df["id"].astype(str).str.strip()
    df["name"] = df["name"].astype(str).str.strip()

    # 5) Clean numbers (remove commas, currency symbols) then convert
    def to_number(series, is_int=False):
        s = series.astype(str)
        # remove commas, currency symbols and words like INR/₹/rs
        s = (s.str.replace(",", "", regex=False)
               .str.replace("₹", "", regex=False)
               .str.replace("INR", "", case=False, regex=True)
               .str.replace("Rs.", "", case=False, regex=True)
               .str.replace("Rs", "", case=False, regex=True)
            )
        out = pd.to_numeric(s, errors="coerce")
        if is_int:
            out = out.fillna(0).astype(int)
        return out

    df["price"] = to_number(df["price"], is_int=False)
    df["stock"] = to_number(df["stock"], is_int=True)

    # 6) Drop duplicates by id (keep last occurrence)
    df = df.drop_duplicates(subset=["id"], keep="last")

    # 7) Validate rows
    invalid = pd.DataFrame()
    invalid_mask = (
        (df["id"] == "") |
        (df["name"] == "") |
        (df["price"].isna()) |
        (df["price"] < 0) |
        (df["stock"].isna()) |
        (df["stock"] < 0)
    )
    if invalid_mask.any():
        invalid = df[invalid_mask].copy()

    # keep only valid rows to import
    valid_df = df[~invalid_mask].copy()

    return valid_df, invalid

# ---------------------- Streamlit UI ----------------------
def main():
    st.title("🛒 Product Inventory (CSV Bulk Import + SQLite)")

    init_db()

    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Go to",
            ["📥 Bulk Import", "📦 View Products", "⬇️ Download Template / Export"]
        )

    if page == "📥 Bulk Import":
        st.subheader("Bulk Import from CSV")

        st.markdown(
            """
            **CSV requirements**
            - Required columns (any order, case-insensitive; aliases allowed):  
              **id, name, price, stock**  
            - Allowed examples:  
              `Product ID, Product Name, Price, Stock` or `id,name,price,qty`  
            - Prices like `60,000.0000` or `₹1200` are cleaned automatically.  
            """
        )

        uploaded = st.file_uploader("Upload CSV", type=["csv"])
        mode = st.radio("Import mode", ["Append / Update (upsert)", "Replace all data"])

        if uploaded is not None:
            try:
                raw = pd.read_csv(uploaded)
            except Exception as e:
                st.error(f"Could not read CSV: {e}")
                return

            st.caption("Preview of uploaded file")
            st.dataframe(raw.head(20), use_container_width=True)

            # Validate & clean
            try:
                valid_df, invalid_df = clean_and_validate_csv(raw)
            except ValueError as ve:
                st.error(str(ve))
                return
            except Exception as e:
                st.error(f"Validation error: {e}")
                return

            # Show summary
            st.markdown("### Validation Summary")
            st.write(f"Total rows in file: **{len(raw)}**")
            st.write(f"Valid rows to import: **{len(valid_df)}**")

            if len(invalid_df) > 0:
                with st.expander(f"⚠️ {len(invalid_df)} invalid row(s) — click to view"):
                    st.dataframe(invalid_df, use_container_width=True)
                st.info("Fix invalid rows in your CSV and upload again, or proceed to import only valid rows.")

            # Import button
            if st.button("✅ Import to Database"):
                try:
                    if len(valid_df) == 0:
                        st.warning("No valid rows to import.")
                    else:
                        if mode == "Replace all data":
                            replace_all_products(valid_df)
                        else:
                            upsert_products(valid_df)
                        st.success(f"Imported {len(valid_df)} row(s) successfully.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Import failed: {e}")

    elif page == "📦 View Products":
        st.subheader("Products in Database")
        df = fetch_all_df()
        if df.empty:
            st.info("Database is empty.")
        else:
            # Pretty display with formatted price
            df_show = df.copy()
            df_show["price"] = df_show["price"].map(lambda x: f"₹{x:,.2f}")
            st.dataframe(df_show.rename(columns={
                "id": "Product ID",
                "name": "Product Name",
                "price": "Price",
                "stock": "Stock"
            }), use_container_width=True)

    elif page == "⬇️ Download Template / Export":
        st.subheader("Templates & Exports")

        # Blank template
        template = pd.DataFrame({
            "id": ["B101", "CB103"],
            "name": ["Pen", "Notebook"],
            "price": [10.0, 50.0],
            "stock": [100, 40]
        })
        buf_template = io.StringIO()
        template.to_csv(buf_template, index=False)
        st.download_button(
            "⬇️ Download CSV Template",
            buf_template.getvalue(),
            file_name="products_template.csv",
            mime="text/csv"
        )

        # Export current DB
        df = fetch_all_df()
        if df.empty:
            st.info("No data to export.")
        else:
            buf_export = io.StringIO()
            df.to_csv(buf_export, index=False)
            st.download_button(
                "⬇️ Export Current Database to CSV",
                buf_export.getvalue(),
                file_name="products_export.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
