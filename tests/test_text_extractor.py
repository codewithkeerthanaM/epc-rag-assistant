from pathlib import Path

from src.ingestion.pdf_parser.text_extractor import extract_text


pdf_path = Path("data/temp/EPC-contract-23.pdf")

text = extract_text(pdf_path)

print("=" * 60)
print("TEXT EXTRACTION")
print("=" * 60)

print(text[:1500])

print()

print("Total Characters :", len(text))