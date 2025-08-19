# import_products.py
import sqlite3
import csv

# Connect to database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Open your CSV file
with open("Products.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            cursor.execute("""
                INSERT INTO products (id, name, price, stock)
                VALUES (?, ?, ?, ?)
            """, (
                row["id"],
                row["name"],
                row["price"],
                row["stock"]
            ))
        except Exception as e:
            print("Failed to insert row:", row, "| Error:", e)

# Commit and close
conn.commit()
conn.close()

print("Products imported successfully!")
