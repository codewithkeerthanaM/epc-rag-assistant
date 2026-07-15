import json

from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings


# =====================================================
# Local Ollama LLM
# =====================================================

ollama_llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)

ragas_llm = LangchainLLMWrapper(ollama_llm)


# =====================================================
# Local Embedding Model
# =====================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

ragas_embeddings = LangchainEmbeddingsWrapper(
    embedding_model
)


# =====================================================
# Load Evaluation Results
# =====================================================

with open(
    "data/evaluation/evaluation_results.json",
    "r",
    encoding="utf-8",
) as f:
    results = json.load(f)


dataset = Dataset.from_dict(
    {
        "question": [
            x["question"]
            for x in results
        ],

        "answer": [
            x["generated_answer"]
            for x in results
        ],

        "contexts": [
            [x["retrieved_context"]]
            for x in results
        ],

        "ground_truth": [
            x["expected_answer"]
            for x in results
        ],
    }
)


print("\nRunning RAGAS Evaluation...\n")


scores = evaluate(
    dataset=dataset,
    llm=ragas_llm,
    embeddings=ragas_embeddings,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
)


df = scores.to_pandas()

print("\nEvaluation Results\n")
print(df)


df.to_csv(
    "data/evaluation/ragas_report.csv",
    index=False,
)

print("\n====================================")
print("Evaluation Complete!")
print("Saved:")
print("data/evaluation/ragas_report.csv")
print("====================================")