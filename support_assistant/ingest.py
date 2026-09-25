import os
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Create a persistent ChromaDB client
db_path = os.path.join(os.path.dirname(__file__), "chroma_db")
client = chromadb.PersistentClient(path=db_path)

# 3. Create or get the collection
collection = client.get_or_create_collection(name="zepto_support")

# 4. Location of our documents
docs_folder = os.path.join(os.path.dirname(__file__), "docs")

documents = []
ids = []
metadatas = []

# 5. Read all TXT files
for filename in sorted(os.listdir(docs_folder)):
    if filename.endswith(".txt"):
        file_path = os.path.join(docs_folder, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        # 6. Split the document into paragraphs
        chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]

        # 7. Store each paragraph as a separate chunk
        for index, chunk in enumerate(chunks):
            documents.append(chunk)
            ids.append(f"{filename}_chunk_{index + 1}")
            metadatas.append({
                "source": filename,
                "chunk": index + 1
            })

# 8. Create embeddings for all chunks
embeddings = model.encode(documents).tolist()

# 9. Store chunks and embeddings in ChromaDB
collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print(f"Documents processed: 8")
print(f"Chunks created: {len(documents)}")
print(f"Chunks stored in ChromaDB: {collection.count()}")