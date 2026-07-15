import json
import random
from pathlib import Path
import ollama

# ==========================================================
# CONFIGURATION
# ==========================================================

MODEL = "llama3.1:8b"
QUESTIONS_PER_CATEGORY = 10

# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "evaluation" / "clean_chunks.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "evaluation" / "epc_test_set.json"

# ==========================================================
# LOAD DATA
# ==========================================================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"\nLoaded {len(chunks)} clean chunks")

# ==========================================================
# GROUP CHUNKS
# ==========================================================

categories = {}

for chunk in chunks:
    categories.setdefault(chunk["category"], []).append(chunk)

print("\nCategories:")

for category, items in categories.items():
    print(f"{category:<20} {len(items)}")

# ==========================================================
# GENERATE DATASET
# ==========================================================

dataset = []
question_id = 1

for category, chunk_list in categories.items():

    print(f"\n========== {category.upper()} ==========")

    sample_count = min(QUESTIONS_PER_CATEGORY, len(chunk_list))

    selected_chunks = random.sample(chunk_list, sample_count)

    generated = 0

    for chunk in selected_chunks:

        prompt = f"""
You are an EPC domain expert.

Read the EPC document below.

Generate ONLY ONE question.

Rules:

- The question MUST be answerable ONLY using this document.
- Do NOT answer the question.
- Do NOT explain anything.
- Return ONLY the question.
- Do NOT use markdown.
- Do NOT use bullet points.

DOCUMENT:

{chunk["text"]}
"""

        try:

            response = ollama.chat(
                model=MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            question = response["message"]["content"].strip()

            # Clean response
            question = (
                question.replace("```", "")
                        .replace("json", "")
                        .replace('"', "")
                        .strip()
            )

            # Build concise expected answer
            text = chunk["text"].replace("\n", " ")

            sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 40]

            if len(sentences) >= 3:
                expected_answer = ". ".join(sentences[:3]) + "."
            elif len(sentences) > 0:
                expected_answer = ". ".join(sentences) + "."
            else:
                expected_answer = text[:300]

            evaluation_item = {

                "id": question_id,

                "category": category,

                "question": question,

                "expected_answer": expected_answer,

                "difficulty": "Medium",

                "question_type": "Definition",

                "source_file": chunk["source_file"],

                "chunk_id": chunk["chunk_id"],

                "context": chunk["text"]

            }

            dataset.append(evaluation_item)

            generated += 1

            print(f"✓ {generated}/{sample_count}")

            question_id += 1

        except Exception as e:

            print(f"❌ Failed: {e}")

# ==========================================================
# SAVE
# ==========================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=4, ensure_ascii=False)

print("\n=========================================")
print("Evaluation Dataset Generated Successfully")
print("=========================================")

print(f"Total Questions : {len(dataset)}")
print(f"Saved To        : {OUTPUT_FILE}")