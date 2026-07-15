from pathlib import Path
from pypdf import PdfReader

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


# --------------------------------------------------
# Extract text from one PDF
# --------------------------------------------------

def extract_text_from_pdf(pdf_path: Path) -> str:

    text = ""

    try:

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:

        print(f"Error reading {pdf_path}: {e}")

    return text


# --------------------------------------------------
# Save extracted text
# --------------------------------------------------

def save_text(
    text: str,
    category: str,
    filename: str,
):

    output_dir = PROCESSED_DIR / category

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = output_dir / f"{filename}.txt"

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(text)

    return output_file


# --------------------------------------------------
# Process ONE uploaded PDF
# --------------------------------------------------

def process_single_pdf(pdf_path: Path):

    category = pdf_path.parent.name

    print(f"\nProcessing uploaded PDF:")
    print(pdf_path.name)

    text = extract_text_from_pdf(pdf_path)

    output_file = save_text(
        text,
        category,
        pdf_path.stem,
    )

    print(f"Saved: {output_file.name}")

    return output_file


# --------------------------------------------------
# Process one category
# --------------------------------------------------

def process_category(category_path):

    category_name = category_path.name

    output_dir = PROCESSED_DIR / category_name

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    pdf_files = list(
        category_path.rglob("*.pdf")
    )

    print(f"\nProcessing {category_name}")

    print(f"Found {len(pdf_files)} PDFs")

    for pdf_file in pdf_files:

        process_single_pdf(pdf_file)


# --------------------------------------------------
# Full Dataset Processing
# --------------------------------------------------

def process_all_pdfs():

    categories = [

        "engineering",

        "procurement",

        "construction",

        "project_management",

        "safety",

    ]

    for category in categories:

        category_path = RAW_DATA_DIR / category

        if category_path.exists():

            process_category(category_path)


def main():

    process_all_pdfs()


if __name__ == "__main__":

    main()