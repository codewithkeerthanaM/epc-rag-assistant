from pathlib import Path
import fitz  # PyMuPDF


# --------------------------------------------------
# Output Directory
# --------------------------------------------------

PAGE_OUTPUT_DIR = Path("data/extracted/pages")
PAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Render PDF Pages
# --------------------------------------------------

def render_pages(pdf_path: Path, dpi: int = 300):
    """
    Render every page of a PDF into a high-quality PNG image.

    Parameters
    ----------
    pdf_path : Path
        Path to the PDF.

    dpi : int
        Rendering DPI (default = 300)

    Returns
    -------
    list
        Metadata of rendered pages.
    """

    rendered_pages = []

    try:

        document = fitz.open(pdf_path)

        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)

        for page_number in range(len(document)):

            page = document.load_page(page_number)

            pix = page.get_pixmap(
                matrix=matrix,
                alpha=False
            )

            image_name = (
                f"{pdf_path.stem}"
                f"_page_{page_number + 1}.png"
            )

            image_path = PAGE_OUTPUT_DIR / image_name

            pix.save(image_path)

            rendered_pages.append(
                {
                    "page": page_number + 1,
                    "image_name": image_name,
                    "image_path": str(image_path),
                    "dpi": dpi
                }
            )

        document.close()

    except Exception as e:

        print(f"[Page Renderer Error] {e}")

    return rendered_pages