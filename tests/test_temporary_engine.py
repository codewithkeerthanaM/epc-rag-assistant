from pathlib import Path

from src.chat.temp_document_processor import process_uploaded_pdf
from src.chat.temporary_engine import answer_question


pdf = Path("data/temp/EPC-contract-23.pdf")

print("Building Temporary Index...")

process_uploaded_pdf(pdf)

print("\n")

question = input("Ask Question: ")

result = answer_question(question)

print("\n")

print("=" * 80)

print(result["answer"])

print("\nSources:")

for s in result["sources"]:

    print("-", s)