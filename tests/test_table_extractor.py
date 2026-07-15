from pathlib import Path

from src.ingestion.pdf_parser.table_extractor import extract_tables


pdf_path = Path(
    "data/temp/EPC-contract-23.pdf"
)

tables = extract_tables(pdf_path)

print("=" * 60)
print("TABLE EXTRACTION SUMMARY")
print("=" * 60)

print(f"Tables Found : {len(tables)}")

print()

for table in tables:

    print(table)