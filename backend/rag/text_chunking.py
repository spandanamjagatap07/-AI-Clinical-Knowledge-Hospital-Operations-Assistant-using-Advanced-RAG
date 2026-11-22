
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.rag.document_loader import load_directory


BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


def split_documents(
    documents,
    chunk_size=500,
    chunk_overlap=100
):
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("Chunk overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("Chunk overlap must be smaller than chunk size.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":

    documents = load_directory(DOCUMENTS_DIR)

    chunks = split_documents(
        documents,
        chunk_size=500,
        chunk_overlap=100
    )

    print("\n========== CONFIGURABLE CHUNKING TEST ==========")

    print("Original document units:", len(documents))
    print("Generated chunks:", len(chunks))
    print("Chunk size:", 500)
    print("Chunk overlap:", 100)

    if chunks:
        print("\nFirst chunk content:")
        print(chunks[0].page_content[:500])

        print("\nFirst chunk metadata:")
        print(chunks[0].metadata)

    print("\n========== CHUNKING COMPLETED ==========")
