from pathlib import Path
import fitz  # PyMuPDF

# --------------------------------------------------
# Output Directory
# --------------------------------------------------

IMAGE_OUTPUT_DIR = Path("data/extracted/images")
IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Extract Embedded Images
# --------------------------------------------------

def extract_images(pdf_path: Path):
    """
    Extract all embedded images from a PDF.

    Parameters
    ----------
    pdf_path : Path

    Returns
    -------
    list
        List of extracted image metadata.
    """

    extracted_images = []

    try:

        document = fitz.open(pdf_path)

        for page_number in range(len(document)):

            page = document.load_page(page_number)

            image_list = page.get_images(full=True)

            if not image_list:
                continue

            for image_index, image in enumerate(image_list, start=1):

                xref = image[0]

                base_image = document.extract_image(xref)

                image_bytes = base_image["image"]

                image_ext = base_image["ext"]

                image_name = (
                    f"{pdf_path.stem}"
                    f"_page_{page_number + 1}"
                    f"_img_{image_index}.{image_ext}"
                )

                image_path = IMAGE_OUTPUT_DIR / image_name

                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                extracted_images.append(
                    {
                        "page": page_number + 1,
                        "image_number": image_index,
                        "image_name": image_name,
                        "image_path": str(image_path),
                        "extension": image_ext,
                    }
                )

        document.close()

    except Exception as e:

        print(f"[Image Extractor Error] {e}")

    return extracted_images