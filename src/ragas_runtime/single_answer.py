import pandas as pd

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

from src.ragas_runtime.dataset_builder import build_dataset
from src.ragas_runtime.ground_truth import get_ground_truth


# ======================================================
# Local Ollama LLM
# ======================================================

ollama_llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)

ragas_llm = LangchainLLMWrapper(
    ollama_llm
)

# ======================================================
# Embedding Model
# ======================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

ragas_embeddings = LangchainEmbeddingsWrapper(
    embedding_model
)


# ======================================================
# Convert NaN -> None
# ======================================================

def clean_metric(value):

    if pd.isna(value):
        return None

    return float(value)


# ======================================================
# Evaluate One Answer
# ======================================================

def evaluate_single_answer(
    question: str,
    answer: str,
    context,
):

    ground_truth = get_ground_truth(question)

    if ground_truth is None:

        return {
            "success": False,
            "message": "Ground truth not found for this question.",
        }

    dataset = build_dataset(

        question=question,

        answer=answer,

        context=context,

        ground_truth=ground_truth,

    )

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

    row = df.iloc[0].to_dict()

    return {

        "success": True,

        "ground_truth": ground_truth,

        "metrics": {

            "faithfulness":
                clean_metric(
                    row.get("faithfulness")
                ),

            "answer_relevancy":
                clean_metric(
                    row.get("answer_relevancy")
                ),

            "context_precision":
                clean_metric(
                    row.get("context_precision")
                ),

            "context_recall":
                clean_metric(
                    row.get("context_recall")
                ),

        }

    }