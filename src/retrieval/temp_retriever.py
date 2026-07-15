from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class TemporaryRetriever:
    """
    Temporary Retriever

    Used ONLY for uploaded PDFs.

    Completely independent from the
    permanent EPC Knowledge Base.
    """

    def __init__(self):

        print("Loading Temporary Embedding Model...")

        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.index = None
        self.chunks = []

    # -------------------------------------------------
    # Build Temporary Index
    # -------------------------------------------------

    def build_index(self, chunks):

        """
        chunks = [
            {
                "text": "...",
                "source_file": "...",
                "chunk_id": ...
            }
        ]
        """

        self.chunks = chunks

        if len(chunks) == 0:

            self.index = None
            return

        texts = []

        for chunk in chunks:
            texts.append(chunk["text"])

        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True
        )

        embeddings = embeddings.astype(np.float32)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        print(
            f"Temporary FAISS built with "
            f"{len(chunks)} chunks."
        )

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    def search(
        self,
        query,
        top_k=5
    ):

        if self.index is None:
            return []

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True
        ).astype(np.float32)

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            results.append(self.chunks[idx])

        return results

    # -------------------------------------------------
    # Clear Temporary Index
    # -------------------------------------------------

    def clear(self):

        self.index = None

        self.chunks = []

        print("Temporary retriever cleared.")

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def has_document(self):

        return (
            self.index is not None
            and len(self.chunks) > 0
        )


temporary_retriever = TemporaryRetriever()