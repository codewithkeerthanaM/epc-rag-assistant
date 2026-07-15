from datasets import Dataset


def build_dataset(
    question: str,
    answer: str,
    context,
    ground_truth: str,
):

    if isinstance(context, str):
        context = [context]

    return Dataset.from_dict(
        {
            "question": [
                question
            ],

            "answer": [
                answer
            ],

            "contexts": [
                context
            ],

            "ground_truth": [
                ground_truth
            ],
        }
    )