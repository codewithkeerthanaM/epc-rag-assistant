from pathlib import Path
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter

PROCESSED_DIR = Path("data/processed")
CHUNKS_DIR = Path("data/chunks")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

# --------------------------------------------------
# Save chunks
# --------------------------------------------------

def save_chunks(chunks, category, filename):

    output_dir = CHUNKS_DIR / category

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for idx, chunk in enumerate(chunks):

        chunk_data = {
            "chunk_id": idx,
            "source_file": f"{filename}.txt",
            "category": category,
            "text": chunk,
        }

        output_file = (
            output_dir /
            f"{filename}_chunk_{idx}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                chunk_data,
                f,
                indent=2,
                ensure_ascii=False,
            )

    return len(chunks)


# --------------------------------------------------
# Process ONE uploaded text file
# --------------------------------------------------

def process_single_text(txt_file: Path):

    category = txt_file.parent.name

    print(f"\nChunking {txt_file.name}")

    text = txt_file.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    chunks = splitter.split_text(text)

    total = save_chunks(
        chunks,
        category,
        txt_file.stem,
    )

    print(f"Created {total} chunks")

    return total


# --------------------------------------------------
# Process Category
# --------------------------------------------------

def process_category(category):

    category_path = PROCESSED_DIR / category

    output_dir = CHUNKS_DIR / category

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    txt_files = list(category_path.glob("*.txt"))

    print(f"\nProcessing {category}")

    print(f"Found {len(txt_files)} text files")

    for txt_file in txt_files:

        try:

            process_single_text(txt_file)

        except Exception as e:

            print(
                f"Error processing "
                f"{txt_file.name}: {e}"
            )


# --------------------------------------------------
# Full Dataset Processing
# --------------------------------------------------

def process_all_texts():

    categories = [

        "engineering",

        "procurement",

        "construction",

        "project_management",

        "safety",

    ]

    for category in categories:

        process_category(category)


def main():

    process_all_texts()


if __name__ == "__main__":

    main()