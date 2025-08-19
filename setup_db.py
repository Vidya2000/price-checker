import sqlite3

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Drop old table if exists
cursor.execute("DROP TABLE IF EXISTS products")

# Create new table with stock column
cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Database initialized!")

