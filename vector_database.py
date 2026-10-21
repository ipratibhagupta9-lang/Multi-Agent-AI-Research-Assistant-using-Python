import pandas as pd
import numpy as np
import faiss
import chromadb
from sentence_transformers import SentenceTransformer

# Load cleaned dataset
df = pd.read_csv("clean_papers.csv")

print("Dataset Loaded Successfully!")
print(df.head())

# Load embedding model
print("\nLoading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(df["Abstract"].tolist())

print("Embeddings Shape:", embeddings.shape)

# ---------------- FAISS ----------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index, "faiss_index.bin")

print("FAISS Index Saved Successfully!")

# ---------------- ChromaDB ----------------

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection("research_papers")

for i, row in df.iterrows():
    collection.add(
        ids=[str(i)],
        documents=[row["Abstract"]],
        metadatas=[{
            "title": row["Title"],
            "year": int(row["Year"])
        }]
    )

print("ChromaDB Created Successfully!")
