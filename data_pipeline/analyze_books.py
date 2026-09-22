import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned CSV
df = pd.read_csv("data_pipeline/books.csv")

print("Dataset Shape:",df.shape)

print("Columns:",df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nPrice Statistics:")
print(df["price"].describe())

print("\nRating distribution:")
print(df["rating"].value_counts().sort_index())

print("\nCategory distribution:")
print(df["category"].value_counts())

print("\nRows with invalid category:")
print(df[df["category"] == "Add a comment"])

print("\nAverage price by category:")
print(df.groupby("category")["price"].mean().sort_values(ascending=False))

print("\nAverage rating by category:")
print(df.groupby("category")["rating"].mean().sort_values(ascending=False))

# Category distribution chart
category_counts = df["category"].value_counts()

plt.figure(figsize=(12, 6))
category_counts.plot(kind="bar")

plt.title("Number of Books by Category")
plt.xlabel("Category")
plt.ylabel("Number of Books")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.show()