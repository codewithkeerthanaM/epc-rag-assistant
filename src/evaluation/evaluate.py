from pathlib import Path
import json

from src.reasoning.rag_engine import answer_question

TEST_SET = Path("data/evaluation/epc_test_set.json")
OUTPUT = Path("data/evaluation/evaluation_results.json")


def main():

    with open(TEST_SET, "r", encoding="utf-8") as f:
        test_set = json.load(f)

    test_set = test_set[:5]

    print(f"Loaded {len(test_set)} questions.\n")

    results = []

    for i, sample in enumerate(test_set, start=1):

        print(f"[{i}/{len(test_set)}] {sample['question']}")

        import time

        start = time.time()

        result = answer_question(sample["question"])

        elapsed = time.time() - start

        print(f"Completed in {elapsed:.2f} seconds")

        results.append({
            "id": sample["id"],
            "category": sample["category"],
            "question": sample["question"],
            "expected_answer": sample["expected_answer"],
            "generated_answer": result["answer"],
            "retrieved_context": result["context"],
            "sources": result["sources"],
            "retrieval_score": result["retrieval_score"]
        })

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("\nEvaluation Finished!")
    print(f"Saved to {OUTPUT}")


if __name__ == "__main__":
    main()