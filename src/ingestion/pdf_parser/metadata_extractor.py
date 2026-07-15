from pathlib import Path
import json
import fitz  # PyMuPDF


# --------------------------------------------------
# Output Directory
# --------------------------------------------------

METADATA_OUTPUT_DIR = Path("data/extracted/metadata")
METADATA_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Extract PDF Metadata
# --------------------------------------------------

def extract_metadata(pdf_path: Path):

    document = fitz.open(pdf_path)

    pdf_metadata = document.metadata

    metadata = {

        "file_name": pdf_path.name,

        "file_path": str(pdf_path),

        "page_count": document.page_count,

        "is_encrypted": document.is_encrypted,

        "title": pdf_metadata.get("title"),

        "author": pdf_metadata.get("author"),

        "subject": pdf_metadata.get("subject"),

        "keywords": pdf_metadata.get("keywords"),

        "creator": pdf_metadata.get("creator"),

        "producer": pdf_metadata.get("producer"),

        "creation_date": pdf_metadata.get("creationDate"),

        "modification_date": pdf_metadata.get("modDate")

    }

    document.close()

    output_file = (
        METADATA_OUTPUT_DIR /
        f"{pdf_path.stem}_metadata.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )

    return metadata