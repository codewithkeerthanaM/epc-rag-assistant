from pathlib import Path
import shutil

# --------------------------------------------------
# Temporary Upload Directory
# --------------------------------------------------

TEMP_UPLOAD_DIR = Path("data/temp")

TEMP_UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Save Uploaded PDF
# --------------------------------------------------

def save_uploaded_pdf(file):

    """
    Saves the uploaded PDF temporarily.

    Returns:
        Path to saved PDF
    """

    destination = TEMP_UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    return destination


# --------------------------------------------------
# Delete Temporary PDF
# --------------------------------------------------

def delete_uploaded_pdf(pdf_path: Path):

    if pdf_path.exists():

        pdf_path.unlink()


# --------------------------------------------------
# Clear Temp Folder
# --------------------------------------------------

def clear_temp_folder():

    for file in TEMP_UPLOAD_DIR.glob("*"):

        try:

            file.unlink()

        except Exception:

            pass