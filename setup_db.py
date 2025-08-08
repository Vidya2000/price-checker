import sqlite3

# Connect (creates the DB file if it doesn't exist)
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        price INTEGER
    )
''')

conn.commit()
conn.close()

print("Database initialized!")
