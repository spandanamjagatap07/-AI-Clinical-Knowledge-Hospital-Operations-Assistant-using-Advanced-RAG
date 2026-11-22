
import shutil

from document_loader import load_directory
from text_chunking import split_documents
from vector_store import create_vector_store

DOCUMENTS_PATH = "data/documents"
VECTOR_DB_PATH = "chroma_db"


def main():
    print("Loading documents...")

    documents = load_directory(DOCUMENTS_PATH)

    print("Loaded documents:", len(documents))

    print("Creating chunks...")

    chunks = split_documents(documents)

    print("Total chunks:", len(chunks))

    # Remove the old database before rebuilding it
    shutil.rmtree(VECTOR_DB_PATH, ignore_errors=True)

    print("Creating updated vector database...")

    create_vector_store(chunks)

    print("Metadata-enabled ingestion completed!")


if __name__ == "__main__":
    main()
