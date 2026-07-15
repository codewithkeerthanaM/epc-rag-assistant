import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "evaluation" / "clean_chunks.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "evaluation" / "top_chunks.json"

# EPC keywords
EPC_KEYWORDS = {
    "shall", "must", "contractor", "engineer",
    "inspection", "installation", "instrument",
    "cable", "pipeline", "commissioning",
    "safety", "procurement", "construction",
    "welding", "testing", "calibration",
    "equipment", "material", "maintenance",
    "permit", "responsibility"
}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} clean chunks.")

ranked_chunks = []

for chunk in chunks:

    text = chunk["text"]
    score = 0

    # -----------------
    # Length Score
    # -----------------
    if 500 <= len(text) <= 1500:
        score += 3
    elif len(text) >= 300:
        score += 1

    # -----------------
    # Sentence Score
    # -----------------
    sentence_count = len(re.findall(r"[.!?]", text))

    if sentence_count >= 5:
        score += 2

    # -----------------
    # EPC Keyword Score
    # -----------------
    lower = text.lower()

    keyword_hits = sum(
        1 for word in EPC_KEYWORDS
        if word in lower
    )

    score += keyword_hits

    # -----------------
    # Action Words
    # -----------------
    for word in ["shall", "must", "required", "ensure"]:
        if word in lower:
            score += 1

    # -----------------
    # Numeric Penalty
    # -----------------
    words = text.split()

    numeric = sum(
        1
        for w in words
        if w.replace(".", "").isdigit()
    )

    if len(words) > 0:
        ratio = numeric / len(words)

        if ratio > 0.20:
            score -= 3

    # -----------------
    # Save Score
    # -----------------
    chunk["quality_score"] = score
    ranked_chunks.append(chunk)

# Highest score first
ranked_chunks.sort(
    key=lambda x: x["quality_score"],
    reverse=True
)

# Keep top 1000
top_chunks = ranked_chunks[:1000]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(top_chunks, f, indent=4, ensure_ascii=False)

print(f"\nTop chunks saved: {len(top_chunks)}")
print(f"Output: {OUTPUT_FILE}")

print("\nTop 10 Scores")

for chunk in top_chunks[:10]:
    print(
        chunk["quality_score"],
        "|",
        chunk["category"],
        "|",
        chunk["source_file"]
    )