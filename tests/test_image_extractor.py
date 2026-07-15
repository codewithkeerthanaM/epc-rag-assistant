from pathlib import Path

from src.ingestion.pdf_parser.image_extractor import extract_images

pdf_path = Path("data/temp/EPC-contract-23.pdf")

images = extract_images(pdf_path)

print("=" * 60)
print("IMAGE EXTRACTION RESULT")
print("=" * 60)

if not images:
    print("No embedded images found.")

else:
    for image in images:
        print(image)

print(f"\nTotal Images: {len(images)}")