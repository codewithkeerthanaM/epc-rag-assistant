"""
evaluator.py

Main Live Evaluation Pipeline.

This module combines:

1. Confidence
2. Evidence

without modifying the existing RAG pipeline.
"""

from src.live_evaluation.confidence import compute_confidence
from src.live_evaluation.evidence import build_evidence


def evaluate_response(
    retrieval_score,
    sources,
    retrieved_context,
):

    confidence = compute_confidence(
        retrieval_score
    )

    evidence = build_evidence(
        sources,
        retrieved_context,
    )

    return {

        "confidence": confidence,

        "evidence": evidence,

        "overall_status": (
            "Reliable"
            if confidence["confidence"] == "High"
            else "Moderately Reliable"
            if confidence["confidence"] == "Medium"
            else "Needs Verification"
        ),

    }