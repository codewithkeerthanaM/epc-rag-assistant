from pathlib import Path
import pdfplumber


# --------------------------------------------------
# Extract Text From PDF
# --------------------------------------------------

def extract_text(pdf_path: Path):
    """
    Extract all readable text from a PDF.

    Parameters
    ----------
    pdf_path : Path
        Path to the PDF file.

    Returns
    -------
    str
        Complete extracted text.
    """

    extracted_text = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            page_text = page.extract_text()

            if page_text:

                extracted_text.append(page_text)

    return "\n\n".join(extracted_text)