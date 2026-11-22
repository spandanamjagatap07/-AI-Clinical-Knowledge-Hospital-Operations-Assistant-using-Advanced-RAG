
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_DB_PATH = PROJECT_ROOT / "chroma_db"


def create_embedding_model():
    """
    Load a local Sentence Transformers embedding model.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    return embedding_model


def create_vector_store(chunks):
    """
    Convert chunks into embeddings and save them in ChromaDB.
    """

    if not chunks:
        raise ValueError("No chunks available for indexing.")

    embedding_model = create_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name="hospital_knowledge",
        persist_directory=str(VECTOR_DB_PATH)
    )

    print("\n========== VECTOR DATABASE ==========")
    print("Vector database created successfully!")
    print("Stored chunks:", vector_store._collection.count())
    print("Database location:", VECTOR_DB_PATH)

    return vector_store


def load_vector_store():
    """
    Load an existing ChromaDB collection.
    """

    embedding_model = create_embedding_model()

    vector_store = Chroma(
        collection_name="hospital_knowledge",
        embedding_function=embedding_model,
        persist_directory=str(VECTOR_DB_PATH)
    )

    return vector_store
