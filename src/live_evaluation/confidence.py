"""
confidence.py

Computes confidence using the retrieval score.

This module does NOT modify the RAG pipeline.
It only interprets the retrieval score.
"""


def compute_confidence(retrieval_score: float):

    if retrieval_score is None:
        return {
            "confidence": "Unknown",
            "confidence_score": 0,
            "retrieval_quality": "Unavailable",
            "reason": "No retrieval score was available."
        }

    percentage = round(retrieval_score * 100)

    if retrieval_score >= 0.85:
        return {
            "confidence": "High",
            "confidence_score": percentage,
            "retrieval_quality": "Excellent",
            "reason": "The retrieved documents are highly relevant to the question."
        }

    elif retrieval_score >= 0.70:
        return {
            "confidence": "Medium",
            "confidence_score": percentage,
            "retrieval_quality": "Good",
            "reason": "Most retrieved documents appear relevant."
        }

    elif retrieval_score >= 0.50:
        return {
            "confidence": "Low",
            "confidence_score": percentage,
            "retrieval_quality": "Fair",
            "reason": "Retrieved information is only partially relevant."
        }

    else:
        return {
            "confidence": "Very Low",
            "confidence_score": percentage,
            "retrieval_quality": "Poor",
            "reason": "The retrieved documents may not sufficiently support the answer."
        }