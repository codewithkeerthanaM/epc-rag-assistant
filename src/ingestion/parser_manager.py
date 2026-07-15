from pathlib import Path
import json

from src.ingestion.pdf_parser.text_extractor import extract_text
from src.ingestion.pdf_parser.image_extractor import extract_images
from src.ingestion.pdf_parser.page_renderer import render_pages
from src.ingestion.pdf_parser.ocr_extractor import run_ocr
from src.ingestion.pdf_parser.table_extractor import extract_tables
from src.ingestion.pdf_parser.metadata_extractor import extract_metadata


# --------------------------------------------------
# Output Directory
# --------------------------------------------------

OUTPUT_DIR = Path("data/extracted/final")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Parse One PDF
# --------------------------------------------------

def parse_pdf(pdf_path: Path):

    print("=" * 70)
    print("Starting Multimodal Parsing")
    print("=" * 70)

    # -------------------------
    # Metadata
    # -------------------------

    print("\n[1/6] Extracting Metadata...")

    metadata = extract_metadata(pdf_path)

    # -------------------------
    # Text
    # -------------------------

    print("\n[2/6] Extracting Text...")

    text = extract_text(pdf_path)

    # -------------------------
    # Images
    # -------------------------

    print("\n[3/6] Extracting Images...")

    images = extract_images(pdf_path)

    # -------------------------
    # Render Pages
    # -------------------------

    print("\n[4/6] Rendering Pages...")

    pages = render_pages(pdf_path)

    # -------------------------
    # OCR
    # -------------------------

    print("\n[5/6] Running OCR...")

    ocr = run_ocr()

    # -------------------------
    # Tables
    # -------------------------

    print("\n[6/6] Extracting Tables...")

    tables = extract_tables(pdf_path)

    final_document = {

        "metadata": metadata,

        "text": text,

        "images": images,

        "rendered_pages": pages,

        "ocr": ocr,

        "tables": tables

    }

    output_file = (

        OUTPUT_DIR /

        f"{pdf_path.stem}.json"

    )

    with open(

        output_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            final_document,

            f,

            indent=4,

            ensure_ascii=False

        )

    print()

    print("=" * 70)

    print("Parsing Completed Successfully")

    print(output_file)

    print("=" * 70)

    return final_document