import json
import re
from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "vector_store" / "chunk_store.json"

OUTPUT_FILE = PROJECT_ROOT / "data" / "evaluation" / "clean_chunks.json"

# ==========================================================
# Load Chunk Store
# ==========================================================

print("=" * 60)
print("Loading chunk_store.json...")
print("=" * 60)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Total Chunks : {len(chunks)}")

# ==========================================================
# Helper Functions
# ==========================================================

BAD_KEYWORDS = {
    "table of contents",
    "contents",
    "annexure",
    "list of figures",
    "list of tables",
    "index"
}


def is_good_chunk(text: str) -> bool:
    """
    Returns True if the chunk is useful for evaluation.
    """

    text = text.strip()

    if len(text) < 400:
        return False

    lower = text.lower()

    # Skip common noisy pages
    for word in BAD_KEYWORDS:
        if word in lower:
            return False

    # Too many numbers
    words = text.split()

    numeric = 0

    for w in words:

        w = w.replace(".", "")
        w = w.replace(",", "")

        if w.isdigit():
            numeric += 1

    if len(words) > 0:

        if numeric / len(words) > 0.25:
            return False

    # Too few sentences
    sentence_count = len(re.findall(r"[.!?]", text))

    if sentence_count < 4:
        return False

    return True


# ==========================================================
# Filter Chunks
# ==========================================================

clean_chunks = []

for chunk in chunks:

    if is_good_chunk(chunk["text"]):

        clean_chunks.append(chunk)

print(f"Clean Chunks : {len(clean_chunks)}")

# ==========================================================
# Save
# ==========================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(clean_chunks, f, indent=4, ensure_ascii=False)

print()
print("=" * 60)
print("clean_chunks.json created successfully!")
print(f"Saved to:\n{OUTPUT_FILE}")
print("=" * 60)