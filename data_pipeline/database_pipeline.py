import pandas as pd
import sqlite3

# Fixed conversion rate required by the capstone
GBP_TO_INR = 105.50

# Load scraped data
df = pd.read_csv("data_pipeline/books.csv")

# Rename price column to the required name
df = df.rename(columns={"price": "price_gbp"})

# Convert availability text to boolean
df["in_stock"] = df["availability"].str.contains(
    "In stock",
    case=False,
    na=False
)

# Convert GBP to INR using the required fixed rate
df["price_inr"] = df["price_gbp"] * GBP_TO_INR

# Keep only the columns needed for the database
df = df[
    [
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category"
    ]
]

# Display the cleaned data
print("Cleaned Data:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nShape:")
print(df.shape)

print("\nPrice Conversion Check:")
print(df[["price_gbp", "price_inr"]].head())

# SQLite database
db_path = "data_pipeline/books.db"

# Start with a fresh database each time the pipeline runs
import os

if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON")

# Create categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
""")

# Create books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL NOT NULL,
    price_inr REAL NOT NULL,
    rating INTEGER NOT NULL,
    in_stock INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
""")

conn.commit()

print("\nDatabase and tables created successfully.")

conn.close()

# Reconnect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON")

# Insert unique categories
categories = df["category"].dropna().unique()

for category in categories:
    cursor.execute(
        """
        INSERT OR IGNORE INTO categories (category_name)
        VALUES (?)
        """,
        (category,)
    )

# Insert books
for _, row in df.iterrows():

    # Get category_id
    cursor.execute(
        """
        SELECT category_id
        FROM categories
        WHERE category_name = ?
        """,
        (row["category"],)
    )

    category_id = cursor.fetchone()[0]

    # Insert book
    cursor.execute(
        """
        INSERT INTO books (
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            int(row["in_stock"]),
            category_id
        )
    )

conn.commit()

# Check number of records
cursor.execute("SELECT COUNT(*) FROM categories")
category_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM books")
book_count = cursor.fetchone()[0]

print("\nDatabase Insert Complete")
print("Categories:", category_count)
print("Books:", book_count)

conn.close()