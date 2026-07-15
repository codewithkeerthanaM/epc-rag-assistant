from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.ingestion.parser_manager import parse_pdf
from src.retrieval.temp_retriever import temporary_retriever


# --------------------------------------------------
# Same Chunk Settings as Permanent RAG
# --------------------------------------------------

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


# --------------------------------------------------
# Build Temporary Document Index
# --------------------------------------------------

def process_uploaded_pdf(pdf_path):
    """
    Processes an uploaded PDF for temporary chat.

    Flow:
        PDF
            ↓
        Multimodal Parser
            ↓
        Merge Text + OCR
            ↓
        Split into Chunks
            ↓
        Build Temporary FAISS
    """

    print("\nProcessing temporary PDF...")

    # ---------------------------------------------
    # Parse uploaded PDF
    # ---------------------------------------------

    parsed_document = parse_pdf(pdf_path)

    # ---------------------------------------------
    # Get extracted PDF text
    # ---------------------------------------------

    combined_text = parsed_document["text"]

    # ---------------------------------------------
    # Append OCR text (for scanned pages/images)
    # ---------------------------------------------

    for page in parsed_document["ocr"]:

        page_text = page.get("text", "").strip()

        if page_text:

            combined_text += "\n\n" + page_text

    if not combined_text.strip():

        raise Exception("No text could be extracted from the PDF.")

    # ---------------------------------------------
    # Split into chunks
    # ---------------------------------------------

    text_chunks = splitter.split_text(combined_text)

    chunks = []

    for idx, chunk in enumerate(text_chunks):

        chunks.append(
            {
                "chunk_id": idx,
                "source_file": pdf_path.name,
                "category": "temporary",
                "parser": "multimodal",
                "text": chunk,
            }
        )

    # ---------------------------------------------
    # Build Temporary FAISS
    # ---------------------------------------------

    temporary_retriever.build_index(chunks)

    print(
        f"Temporary document indexed successfully "
        f"({len(chunks)} chunks)"
    )

    return {
        "success": True,
        "filename": pdf_path.name,
        "chunks": len(chunks),
    }