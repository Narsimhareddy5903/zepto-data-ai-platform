import os
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Load the same embedding model used during ingestion
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Connect to our persistent ChromaDB
db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
client = chromadb.PersistentClient(path=db_path)

# 3. Get the existing collection
collection = client.get_collection(name="zepto_support")

# 4. Ask a customer question
question = "How much is the delivery fee for an order below INR 149?"

# 5. Convert the question into an embedding
query_embedding = model.encode(question).tolist()

# 6. Search ChromaDB for the top 3 relevant chunks
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

# 7. Display the results
print("\nCustomer Question:")
print(question)

print("\nTop 3 Relevant Documents:")

for i in range(3):
    print(f"\n--- Result {i + 1} ---")
    print(results["documents"][0][i])
    print("Source:", results["ids"][0][i])