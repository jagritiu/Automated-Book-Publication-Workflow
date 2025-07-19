import json
import chromadb
from chromadb import PersistentClient

client = PersistentClient(path="version_storage")


# Create or get collection
collection = client.get_or_create_collection(name="chapter_versions")

# Load AI-written version
with open("rewritten_output/output_ai_written.json", "r", encoding="utf-8") as f:
    ai_data = json.load(f)
    ai_text = ai_data.get("chapter", "")

# Load Human-reviewed version
with open("human_reviewed/human_approved_output.json", "r", encoding="utf-8") as f:
    human_data = json.load(f)
    human_text = human_data.get("chapter", "")

# Add both versions to ChromaDB
collection.add(
    documents=[ai_text, human_text],
    metadatas=[{"version": "AI-written"}, {"version": "Human-approved"}],
    ids=["chapter_v1", "chapter_v2"]
)

print("✅ Chapter versions stored in ChromaDB!")

# Optional: Perform a semantic search
query = input("🔍 Enter a search query (e.g. 'describe main character'): ")
results = collection.query(query_texts=[query], n_results=2)

print("\n🔎 Search Results:")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"- Version: {meta['version']}\nText Snippet: {doc[:200]}...\n")
