from pathlib import Path

from src.ingestion.pdf_parser.page_renderer import render_pages

pdf_path = Path("data/temp/EPC-contract-23.pdf")

pages = render_pages(pdf_path)

print("=" * 60)
print("PAGE RENDERING RESULT")
print("=" * 60)

for page in pages:
    print(page)

print(f"\nTotal Pages Rendered: {len(pages)}")