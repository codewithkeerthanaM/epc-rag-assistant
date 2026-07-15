from src.ingestion.pdf_parser.ocr_extractor import run_ocr

results = run_ocr()

print("=" * 60)
print("OCR SUMMARY")
print("=" * 60)

print(f"Pages Processed : {len(results)}")

print()

print("First Page OCR Preview:\n")

print(results[0]["text"][:1000])

print()

print("Words Found :", results[0]["word_count"])