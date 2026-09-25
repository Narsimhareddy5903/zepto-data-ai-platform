import os
import requests
import chromadb
from sentence_transformers import SentenceTransformer


# 1. Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# 2. Connect to persistent ChromaDB
db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
client = chromadb.PersistentClient(path=db_path)

collection = client.get_collection(name="zepto_support")


# 3. Customer question
question = "What should I do if my order arrives damaged?"


# 4. Convert question into an embedding
query_embedding = model.encode(question).tolist()


# 5. Retrieve relevant documents
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)


# 6. Combine retrieved documents into context
context_parts = []

for document in results["documents"][0]:
    context_parts.append(document)

context = "\n\n".join(context_parts)


# 7. Create a grounded prompt for Llama 3
prompt = f"""
You are a helpful Zepto customer support assistant.

Answer the customer's question using ONLY the information provided
in the context below.

If the answer is not available in the context, say:
"I don't have enough information to answer that."

Do not invent policies, prices, or information.

Context:
{context}

Customer question:
{question}

Answer:
"""


# 8. Send prompt to local Ollama
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3:latest",
        "prompt": prompt,
        "stream": False
    }
)


# 9. Check for errors
response.raise_for_status()


# 10. Get Llama's answer
answer = response.json()["response"]


# 11. Display result
print("\nCustomer Question:")
print(question)

print("\nRetrieved Context:")
print(context)

print("\nAssistant Answer:")
print(answer)

print("\nSources:")

for source in results["ids"][0]:
    print("-", source)