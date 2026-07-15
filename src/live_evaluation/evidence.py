"""
evidence.py

Builds an evidence summary from the retrieved
sources and retrieved context.

This module does NOT modify the RAG pipeline.
"""


def build_evidence(
    sources,
    retrieved_context,
):

    if not sources:
        sources = []

    if isinstance(retrieved_context, list):

        retrieved_chunks = len(retrieved_context)

        preview = [
            chunk[:200] + "..."
            if len(chunk) > 200
            else chunk
            for chunk in retrieved_context[:3]
        ]

    else:

        retrieved_chunks = 1 if retrieved_context else 0

        preview = [
            retrieved_context[:200] + "..."
            if retrieved_context and len(retrieved_context) > 200
            else retrieved_context
        ] if retrieved_context else []

    return {

        "source_count": len(sources),

        "sources": sources,

        "retrieved_chunks": retrieved_chunks,

        "context_preview": preview,

        "evidence_strength": (
            "Strong"
            if len(sources) >= 3
            else "Moderate"
            if len(sources) == 2
            else "Weak"
        ),

    }