from pathlib import Path
import json

CHUNKS_DIR = Path("data/chunks")
VECTOR_STORE_DIR = Path("data/vector_store")

chunk_store = []

categories = [
    "engineering",
    "procurement",
    "construction",
    "project_management",
    "safety"
]

for category in categories:

    category_dir = CHUNKS_DIR / category

    json_files = sorted(
        category_dir.glob("*.json")
    )

    for file in json_files:

        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            chunk_store.append({
                "category": data["category"],
                "source_file": data["source_file"],
                "chunk_id": data["chunk_id"],
                "text": data["text"]
            })

        except Exception as e:

            print(
                f"Error reading {file}: {e}"
            )

with open(
    VECTOR_STORE_DIR / "chunk_store.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunk_store,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    f"Saved {len(chunk_store)} chunks"
)