from pathlib import Path

from src.ingestion.pdf_parser.metadata_extractor import (
    extract_metadata
)

pdf_path = Path(
    "data/temp/EPC-contract-23.pdf"
)

metadata = extract_metadata(pdf_path)

print("=" * 60)
print("PDF METADATA")
print("=" * 60)

for key, value in metadata.items():
    print(f"{key}: {value}")