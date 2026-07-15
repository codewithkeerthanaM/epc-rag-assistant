from pathlib import Path

from src.chat.temp_document_processor import process_uploaded_pdf
from src.retrieval.temp_retriever import temporary_retriever

pdf = Path("data/temp/EPC-contract-23.pdf")

print("Building Temporary Index...")

process_uploaded_pdf(pdf)

print("\nSearching...\n")

results = temporary_retriever.search(
    "What is Performance Guarantee?",
    top_k=3
)

print("=" * 60)

for i, chunk in enumerate(results, 1):

    print(f"\nResult {i}")

    print("-" * 40)

    print(chunk["text"][:800])