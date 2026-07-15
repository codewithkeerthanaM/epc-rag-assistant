from pathlib import Path
import json
import pdfplumber
import pandas as pd


# --------------------------------------------------
# Output Directories
# --------------------------------------------------

TABLE_JSON_DIR = Path("data/extracted/tables/json")
TABLE_CSV_DIR = Path("data/extracted/tables/csv")

TABLE_JSON_DIR.mkdir(parents=True, exist_ok=True)
TABLE_CSV_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Extract Tables
# --------------------------------------------------

def extract_tables(pdf_path: Path):

    extracted_tables = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            print(f"Checking Page {page_number}")

            tables = page.extract_tables()

            if not tables:
                continue

            for table_number, table in enumerate(tables, start=1):

                # Remove empty rows
                clean_table = []

                for row in table:

                    if row is None:
                        continue

                    row = [
                        "" if cell is None else str(cell).strip()
                        for cell in row
                    ]

                    if any(cell != "" for cell in row):
                        clean_table.append(row)

                if not clean_table:
                 continue

                # Ignore tiny false-positive tables
                if len(clean_table) < 2:
                 continue

                if len(clean_table[0]) < 2:
                 continue

                dataframe = pd.DataFrame(clean_table)

                json_name = (
                    f"{pdf_path.stem}"
                    f"_page_{page_number}"
                    f"_table_{table_number}.json"
                )

                csv_name = (
                    f"{pdf_path.stem}"
                    f"_page_{page_number}"
                    f"_table_{table_number}.csv"
                )

                json_path = TABLE_JSON_DIR / json_name
                csv_path = TABLE_CSV_DIR / csv_name

                # Save JSON
                with open(
                    json_path,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        clean_table,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )

                # Save CSV
                dataframe.to_csv(
                    csv_path,
                    index=False,
                    header=False
                )

                extracted_tables.append(

                    {

                        "page": page_number,

                        "table_number": table_number,

                        "rows": len(clean_table),

                        "columns": len(clean_table[0]),

                        "json_path": str(json_path),

                        "csv_path": str(csv_path)

                    }

                )

    return extracted_tables