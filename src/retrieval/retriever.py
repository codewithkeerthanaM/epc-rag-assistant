from pathlib import Path
import json
import faiss

from sentence_transformers import SentenceTransformer


VECTOR_STORE_DIR = Path("data/vector_store")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading model...")
model = SentenceTransformer(MODEL_NAME)

print("Loading FAISS index...")
index = faiss.read_index(
    str(VECTOR_STORE_DIR / "faiss_index.bin")
)

with open(
    VECTOR_STORE_DIR / "metadata.json",
    "r",
    encoding="utf-8"
) as f:
    metadata = json.load(f)


query = input("\nEnter EPC Query: ")

query_embedding = model.encode(
    [query],
    convert_to_numpy=True
)

k = 5

distances, indices = index.search(
    query_embedding,
    k
)

print("\nTop Results\n")

for rank, idx in enumerate(indices[0], start=1):

    result = metadata[idx]

    print(f"\nResult {rank}")
    print(f"Category    : {result['category']}")
    print(f"Source File : {result['source_file']}")
    print(f"Chunk ID    : {result['chunk_id']}")