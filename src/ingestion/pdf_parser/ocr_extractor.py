from pathlib import Path
import json

import pytesseract
from PIL import Image


# --------------------------------------------------
# Configure Tesseract
# --------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# --------------------------------------------------
# Directories
# --------------------------------------------------

PAGE_DIR = Path("data/extracted/pages")

OCR_OUTPUT_DIR = Path("data/extracted/ocr")

OCR_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# --------------------------------------------------
# OCR One Image
# --------------------------------------------------


def extract_page(image_path: Path):

    image = Image.open(image_path)

    data = pytesseract.image_to_data(
        image,
        output_type=pytesseract.Output.DICT,
        lang="eng"
    )

    words = []

    full_text = []

    total = len(data["text"])

    for i in range(total):

        text = data["text"][i].strip()

        if text == "":
            continue

        confidence = float(data["conf"][i])

        word = {

            "text": text,

            "confidence": confidence,

            "left": data["left"][i],

            "top": data["top"][i],

            "width": data["width"][i],

            "height": data["height"][i]

        }

        words.append(word)

        full_text.append(text)

    return {

        "text": " ".join(full_text),

        "words": words

    }


# --------------------------------------------------
# OCR All Pages
# --------------------------------------------------


def run_ocr():

    results = []

    pages = sorted(
    PAGE_DIR.glob("*.png"),
    key=lambda p: int(p.stem.split("_page_")[-1])
)

    for page in pages:

        print(f"OCR -> {page.name}")

        result = extract_page(page)

        output = {

            "page": page.stem,

            "image": page.name,

            "text": result["text"],

            "word_count": len(result["words"]),

            "words": result["words"]

        }

        json_file = OCR_OUTPUT_DIR / f"{page.stem}.json"

        with open(

            json_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                output,

                f,

                indent=4,

                ensure_ascii=False

            )

        results.append(output)

    return results