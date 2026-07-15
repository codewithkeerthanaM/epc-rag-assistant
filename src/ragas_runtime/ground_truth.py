import json
from pathlib import Path

TEST_SET = Path("data/evaluation/epc_test_set.json")


def get_ground_truth(question: str):

    if not TEST_SET.exists():
        return None

    with open(TEST_SET, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    for sample in dataset:

        if sample["question"].strip().lower() == question.strip().lower():

            return sample["expected_answer"]

    return None