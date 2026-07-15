from sentence_transformers import CrossEncoder

print("Loading Re-Ranker Model...")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank(query, chunks, top_k=5):

    pairs = [
        (query, chunk["text"])
        for chunk in chunks
    ]

    scores = reranker.predict(pairs)

    ranked_chunks = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        chunk
        for chunk, score in ranked_chunks[:top_k]
    ]