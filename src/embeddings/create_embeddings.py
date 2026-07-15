from pathlib import Path
import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

CHUNKS_DIR = Path("data/chunks")
VECTOR_STORE_DIR = Path("data/vector_store")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)

all_texts = []
all_metadata = []

categories = [
    "engineering",
    "procurement",
    "construction",
    "project_management",
    "safety"
]

for category in categories:

    category_dir = CHUNKS_DIR / category

    json_files = list(category_dir.glob("*.json"))

    print(f"\nProcessing {category}")
    print(f"Found {len(json_files)} chunks")

    for file in json_files:

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            text = data.get("text", "").strip()

            if len(text) == 0:
                continue

            all_texts.append(text)

            all_metadata.append({
                "category": data["category"],
                "source_file": data["source_file"],
                "chunk_id": data["chunk_id"]
            })

        except Exception as e:
            print(f"Error reading {file}: {e}")

print(f"\nTotal chunks loaded: {len(all_texts)}")

print("\nGenerating embeddings...")

embeddings = model.encode(
    all_texts,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True
)

dimension = embeddings.shape[1]

print(f"\nEmbedding Dimension: {dimension}")

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    str(VECTOR_STORE_DIR / "faiss_index.bin")
)

np.save(
    VECTOR_STORE_DIR / "embeddings.npy",
    embeddings
)

with open(
    VECTOR_STORE_DIR / "metadata.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        all_metadata,
        f,
        indent=2,
        ensure_ascii=False
    )

print("\nVector Database Created Successfully!")
print(f"Indexed Chunks: {len(all_texts)}")