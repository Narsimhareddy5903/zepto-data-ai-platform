import sqlite3
import pandas as pd

DB_PATH = "data_pipeline/books.db"
OUTPUT_PATH = "data_pipeline/sql_query_results.txt"

conn = sqlite3.connect(DB_PATH)

queries = {
    "Query 1 - SELECT and WHERE": """
        SELECT title, price_gbp, rating
        FROM books
        WHERE rating >= 4;
    """,

    "Query 2 - ORDER BY and LIMIT": """
        SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 5;
    """,

    "Query 3 - DISTINCT categories": """
        SELECT DISTINCT category_name
        FROM categories
        ORDER BY category_name;
    """,

    "Query 4 - BETWEEN": """
        SELECT title, price_gbp, rating
        FROM books
        WHERE price_gbp BETWEEN 20 AND 40
        ORDER BY price_gbp;
    """,

    "Query 5 - JOIN": """
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
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as file:

    for name, query in queries.items():

        result = pd.read_sql(query, conn)

        separator = "=" * 70

        # Print to terminal
        print("\n" + separator)
        print(name)
        print(separator)
        print("SQL:")
        print(query.strip())
        print("\nOutput:")
        print(result.to_string(index=False))

        # Save to evidence file
        file.write("\n" + separator + "\n")
        file.write(name + "\n")
        file.write(separator + "\n")
        file.write("SQL:\n")
        file.write(query.strip() + "\n")
        file.write("\nOutput:\n")
        file.write(result.to_string(index=False))
        file.write("\n\n")

conn.close()

print("\nSQL query strings and outputs saved to:")
print(OUTPUT_PATH)