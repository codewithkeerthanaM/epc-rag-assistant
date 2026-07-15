from pathlib import Path

from src.ingestion.parser_manager import parse_pdf


pdf_path = Path(
    "data/temp/EPC-contract-23.pdf"
)

result = parse_pdf(pdf_path)

print()

print("=" * 60)

print("SUMMARY")

print("=" * 60)

print()

print("Pages :", result["metadata"]["page_count"])

print("Images :", len(result["images"]))

print("Tables :", len(result["tables"]))

print("OCR Pages :", len(result["ocr"]))

print("Text Length :", len(result["text"]))