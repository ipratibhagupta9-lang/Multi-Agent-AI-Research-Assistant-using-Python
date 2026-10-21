import chromadb
from sentence_transformers import SentenceTransformer

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

# Open Collection
collection = client.get_collection("research_papers")

# Load Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_papers(query):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    papers = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):

        paper = {
            "title": metadatas[i]["title"],
            "year": metadatas[i]["year"],
            "abstract": documents[i],
            "score": round(1 - distances[i], 3)
        }

        papers.append(paper)

    return papers
