
from pathlib import Path
import pandas as pd

from pypdf import PdfReader
from docx import Document as DocxDocument
from langchain_core.documents import Document


def load_txt(file_path):
    file_path = Path(file_path)

    content = file_path.read_text(encoding="utf-8")

    metadata = {
        "source": file_path.name,
        "file_type": file_path.suffix.lstrip(".")
    }

    # Extract metadata from document headers
    for line in content.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)

            key = key.strip().lower()
            value = value.strip()

            if key in ["department", "document_type", "version"]:
                metadata[key] = value

    return [
        Document(
            page_content=content,
            metadata=metadata
        )
    ]

def load_pdf(file_path):
    """Load a PDF file page by page."""

    reader = PdfReader(str(file_path))
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": Path(file_path).name,
                        "file_type": "pdf",
                        "page_number": page_number
                    }
                )
            )

    return documents


def load_docx(file_path):
    """Load paragraphs and tables from a Word document."""

    doc = DocxDocument(str(file_path))

    content = []

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            content.append(paragraph.text)

    for table in doc.tables:
        for row in table.rows:
            row_text = " | ".join(
                cell.text.strip() for cell in row.cells
            )
            if row_text.strip():
                content.append(row_text)

    text = "\n".join(content)

    return [
        Document(
            page_content=text,
            metadata={
                "source": Path(file_path).name,
                "file_type": "docx"
            }
        )
    ] if text.strip() else []


def load_csv(file_path):
    """Load a CSV file row by row."""

    dataframe = pd.read_csv(file_path).fillna("")

    documents = []

    for index, row in dataframe.iterrows():

        row_text = "\n".join(
            f"{column}: {value}"
            for column, value in row.items()
        )

        documents.append(
            Document(
                page_content=row_text,
                metadata={
                    "source": Path(file_path).name,
                    "file_type": "csv",
                    "row_number": int(index) + 1
                }
            )
        )

    return documents


def load_excel(file_path):
    """Load every Excel sheet row by row."""

    excel_file = pd.ExcelFile(file_path)
    documents = []

    for sheet_name in excel_file.sheet_names:

        dataframe = pd.read_excel(
            excel_file,
            sheet_name=sheet_name
        ).fillna("")

        for index, row in dataframe.iterrows():

            row_text = "\n".join(
                f"{column}: {value}"
                for column, value in row.items()
            )

            documents.append(
                Document(
                    page_content=row_text,
                    metadata={
                        "source": Path(file_path).name,
                        "file_type": "xlsx",
                        "sheet_name": str(sheet_name),
                        "row_number": int(index) + 1
                    }
                )
            )

    return documents


def load_document(file_path):
    """Automatically identify and load supported files."""

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    loaders = {
        ".txt": load_txt,
        ".pdf": load_pdf,
        ".docx": load_docx,
        ".csv": load_csv,
        ".xlsx": load_excel,
        ".xlsm": load_excel
    }

    if extension not in loaders:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    return loaders[extension](file_path)


def load_directory(directory_path):
    """Load all supported files from a directory."""

    directory_path = Path(directory_path)

    all_documents = []

    supported_extensions = {
        ".txt", ".pdf", ".docx",
        ".csv", ".xlsx", ".xlsm"
    }

    for file_path in directory_path.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        try:
            documents = load_document(file_path)
            all_documents.extend(documents)

            print(
                f"Loaded {file_path.name}: "
                f"{len(documents)} document units"
            )

        except Exception as error:
            print(
                f"Error loading {file_path.name}: {error}"
            )

    return all_documents
