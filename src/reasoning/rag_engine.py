from pathlib import Path
import json
import faiss
import ollama

from sentence_transformers import SentenceTransformer
from src.retrieval.reranker import rerank

VECTOR_STORE_DIR = Path("data/vector_store")

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")
embedding_model = SentenceTransformer(MODEL_NAME)

print("Loading FAISS index...")
index = faiss.read_index(
    str(VECTOR_STORE_DIR / "faiss_index.bin")
)

with open(
    VECTOR_STORE_DIR / "chunk_store.json",
    "r",
    encoding="utf-8"
) as f:
    chunk_store = json.load(f)


# Conversation Memory
conversation_history = []


def answer_question(query):
    global conversation_history

    # ----------------------------
    # History-aware retrieval
    # ----------------------------

    retrieval_query = query

    if len(conversation_history) > 0:
        last_question = conversation_history[-1]["user"]
        retrieval_query = f"{last_question} {query}"

    # Generate query embedding
    query_embedding = embedding_model.encode(
        [retrieval_query],
        convert_to_numpy=True
    )

    # Retrieve Top-20 chunks
    k = 20

    distances, indices = index.search(
        query_embedding,
        k
    )

    retrieval_score = sum(distances[0][:5]) / 5

    retrieved_chunks = []

    for idx in indices[0]:
        retrieved_chunks.append(chunk_store[idx])

    # Re-rank
    reranked_chunks = rerank(
        query,
        retrieved_chunks,
        top_k=5
    )

    # ----------------------------
    # Build Context
    # ----------------------------

    context = []
    sources = []

    for chunk in reranked_chunks:

        sources.append(
            f"{chunk['source_file']} (Chunk {chunk['chunk_id']})"
        )

        context.append(
            f"""Category: {chunk['category']}
Source: {chunk['source_file']}

{chunk['text']}"""
        )

    # ----------------------------
    # Conversation History
    # ----------------------------

    history_text = ""

    for item in conversation_history:
        history_text += f"""
User: {item['user']}
Assistant: {item['assistant']}
"""

    # ----------------------------
    # Prompt
    # ----------------------------

    prompt = f"""
You are a Senior EPC (Engineering, Procurement, Construction) domain expert.

Your expertise includes:

- Engineering
- Procurement
- Construction
- Project Management
- Industrial Safety

Rules:

1. Answer ONLY using the provided context.
2. Never invent facts.
3. If the information is unavailable, respond:
   Information not found in EPC knowledge base.
4. Use conversation history when relevant.
5. Provide:
   - Explanation
   - Key Points
   - Risks / Implications
6. Keep answers professional.

Conversation History:
{history_text}

Context:
{chr(10).join(context)}

Question:
{query}

Answer:
"""

    # ----------------------------
    # LLM Response
    # ----------------------------

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    # ----------------------------
    # Update Memory
    # ----------------------------

    conversation_history.append(
        {
            "user": query,
            "assistant": answer
        }
    )

    if len(conversation_history) > 3:
        conversation_history.pop(0)

    # ----------------------------
    # Return
    # ----------------------------

    return {
        "answer": answer,
        "sources": sorted(set(sources)),
        "retrieval_score": float(retrieval_score),
        "context": context
    }


def main():

    print("\nEPC RAG Assistant Ready!")
    print("Type 'exit' to quit.\n")

    while True:

        query = input("Ask EPC Question: ")

        if query.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        result = answer_question(query)

        print(
            f"\nRetrieval Score: "
            f"{result['retrieval_score']:.4f}"
        )

        print("\nGenerating Answer...\n")

        print(result["answer"])

        print("\nSources Used:")

        for source in result["sources"]:
            print(f"- {source}")

        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()