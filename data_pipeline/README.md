# Module 1 — Data Pipeline

This module builds a complete data pipeline for books from **Books to Scrape**.

The pipeline covers:

1. Web scraping using Requests and BeautifulSoup
2. Data cleaning and type conversion
3. GBP to INR price conversion
4. SQLite database creation
5. SQL analysis queries
6. Pandas SQL-to-DataFrame analysis
7. SQL JOIN vs `pandas.merge()` comparison

## Project Files

```text
data_pipeline/
├── scrape_books.py
├── analyze_books.py
├── books.csv
├── database_pipeline.py
├── books.db
├── sql_queries.py
├── sql_query_results.txt
├── sql_pandas_comparison.py
└── README.md
```

## Requirements

Python 3.x with the following packages:

```bash
pip install requests beautifulsoup4 pandas
```

## Step 1 — Scrape Books

Run:

```bash
python data_pipeline/scrape_books.py
```

The scraper uses:

* `requests` to download web pages
* `BeautifulSoup` to parse HTML
* pagination across the first 3 pages
* 20 books per page

The resulting dataset contains **60 books**.

Raw fields collected include:

* title
* price
* availability
* rating
* category

## Step 2 — Analyze and Validate Data

Run:

```bash
python data_pipeline/analyze_books.py
```

The analysis checks:

* dataset shape
* column names
* data types
* missing values
* duplicate rows
* price statistics
* rating distribution
* category-level summaries

Current dataset:

* Rows: 60
* Columns: 5
* Missing values: 0
* Duplicate rows: 0

## Step 3 — Build SQLite Database

Run:

```bash
python data_pipeline/database_pipeline.py
```

The script reads `books.csv` and performs the required cleaning.

### Cleaning Decisions

#### Price

The scraped price is converted to a numeric GBP value and stored as:

```text
price_gbp
```

#### Rating

The text star rating is converted to an integer from 1 to 5.

Example:

```text
One → 1
Two → 2
Three → 3
Four → 4
Five → 5
```

#### Stock Status

The availability text is converted into a Boolean-style field:

```text
in_stock
```

SQLite stores this Boolean value as `0` or `1`.

#### GBP to INR Conversion

A fixed conversion rate is used as required:

```text
1 GBP = 105.50 INR
```

The INR price is calculated as:

```text
price_inr = price_gbp × 105.50
```

No currency API is used.

## SQLite Database

The database is:

```text
books.db
```

It contains two application tables:

### `categories`

| Column        | Type    | Description          |
| ------------- | ------- | -------------------- |
| category_id   | INTEGER | Primary key          |
| category_name | TEXT    | Unique category name |

### `books`

| Column      | Type    | Description            |
| ----------- | ------- | ---------------------- |
| book_id     | INTEGER | Primary key            |
| title       | TEXT    | Book title             |
| price_gbp   | REAL    | Price in GBP           |
| price_inr   | REAL    | Converted price in INR |
| rating      | INTEGER | Rating from 1 to 5     |
| in_stock    | INTEGER | Stock flag             |
| category_id | INTEGER | Foreign key            |

The relationship is:

```text
categories
    │
    │ category_id
    ▼
books
```

The `books.category_id` column references `categories.category_id`.

The database pipeline recreates the database when rerun, preventing duplicate inserts.

## Step 4 — Run SQL Queries

Run:

```bash
python data_pipeline/sql_queries.py
```

Five SQL queries are included.

### Query 1 — SELECT and WHERE

Find books with a rating of at least 4.

### Query 2 — ORDER BY and LIMIT

Find the five most expensive books.

### Query 3 — DISTINCT

List unique book categories.

### Query 4 — BETWEEN

Find books with prices between £20 and £40.

### Query 5 — JOIN

Join the `books` and `categories` tables to display book details together with category names.

The SQL query strings and their outputs are saved in:

```text
sql_query_results.txt
```

## Step 5 — SQL and Pandas Comparison

Run:

```bash
python data_pipeline/sql_pandas_comparison.py
```

This script demonstrates two important pandas/SQL operations.

### `pd.read_sql()`

SQL query results are loaded directly into pandas DataFrames using:

```python
pd.read_sql()
```

### `pd.merge()`

The database JOIN is reproduced using:

```python
pd.merge()
```

The SQL JOIN and pandas merge produce the same 10-row result.

The script verifies this programmatically:

```text
JOIN outputs equivalent: True
```

This demonstrates the relationship between SQL JOIN operations and pandas DataFrame merging.

## Reproducibility

From the project root, run the scripts in this order:

```bash
python data_pipeline/scrape_books.py
python data_pipeline/analyze_books.py
python data_pipeline/database_pipeline.py
python data_pipeline/sql_queries.py
python data_pipeline/sql_pandas_comparison.py
```

The database can be recreated from the scraped CSV using `database_pipeline.py`.

## Module 1 Result

The completed pipeline produces:

* 60 scraped books
* 24 categories
* cleaned numeric ratings
* cleaned GBP prices
* Boolean-style stock status
* INR prices using the fixed rate of 105.50
* normalized SQLite database
* primary key / foreign key relationship
* five SQL analysis queries
* saved SQL query evidence
* `pd.read_sql()` examples
* SQL JOIN reproduced using `pandas.merge()`
* verified equivalent SQL and pandas JOIN results
