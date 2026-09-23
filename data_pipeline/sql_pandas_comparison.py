import sqlite3
import pandas as pd

DB_PATH = "data_pipeline/books.db"

conn = sqlite3.connect(DB_PATH)

# --------------------------------------------------
# 1. Read SQL query results using pd.read_sql()
# --------------------------------------------------

query_rating = """
SELECT title, price_gbp, rating
FROM books
WHERE rating >= 4
ORDER BY rating DESC, price_gbp DESC;
"""

query_join = """
SELECT
    b.title,
    b.price_gbp,
    b.rating,
    c.category_name
FROM books AS b
JOIN categories AS c
    ON b.category_id = c.category_id
ORDER BY b.price_gbp DESC
LIMIT 10;
"""

rating_df = pd.read_sql(query_rating, conn)
sql_join_df = pd.read_sql(query_join, conn)

print("=" * 70)
print("SQL QUERY RESULT 1 - Books with Rating >= 4")
print("=" * 70)
print(rating_df.to_string(index=False))

print("\n" + "=" * 70)
print("SQL JOIN RESULT")
print("=" * 70)
print(sql_join_df.to_string(index=False))


# --------------------------------------------------
# 2. Load database tables into pandas
# --------------------------------------------------

books_df = pd.read_sql(
    """
    SELECT book_id, title, price_gbp, rating, category_id
    FROM books;
    """,
    conn
)

categories_df = pd.read_sql(
    """
    SELECT category_id, category_name
    FROM categories;
    """,
    conn
)


# --------------------------------------------------
# 3. Reproduce the SQL JOIN using pd.merge()
# --------------------------------------------------

pandas_join_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

pandas_join_df = pandas_join_df[
    ["title", "price_gbp", "rating", "category_name"]
]

pandas_join_df = (
    pandas_join_df
    .sort_values("price_gbp", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

sql_compare_df = sql_join_df.reset_index(drop=True)


# --------------------------------------------------
# 4. Compare SQL JOIN and pandas merge
# --------------------------------------------------

print("\n" + "=" * 70)
print("PANDAS pd.merge() RESULT")
print("=" * 70)
print(pandas_join_df.to_string(index=False))

print("\n" + "=" * 70)
print("SQL JOIN vs pandas.merge()")
print("=" * 70)

print("SQL JOIN rows:", len(sql_compare_df))
print("pandas.merge() rows:", len(pandas_join_df))

print(
    "JOIN outputs equivalent:",
    sql_compare_df.equals(pandas_join_df)
)

conn.close()