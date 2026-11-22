
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from backend.rag.document_loader import load_directory
from backend.rag.text_chunking import split_documents


BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


EMBEDDING_MODELS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2"
]


def compare_embedding_models(question):

    print("\n========== EMBEDDING MODEL COMPARISON ==========")

    # Load hospital documents
    documents = load_directory(DOCUMENTS_DIR)

    print("\nTotal documents loaded:", len(documents))

    # Split documents into chunks
    chunks = split_documents(
        documents,
        chunk_size=500,
        chunk_overlap=100
    )

    print("Total chunks generated:", len(chunks))

    # Test each embedding model separately
    for index, model_name in enumerate(EMBEDDING_MODELS, start=1):

        print("\n" + "=" * 55)
        print(f"MODEL {index}: {model_name}")
        print("=" * 55)

        embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )

        # Create a temporary in-memory Chroma collection
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            collection_name=f"embedding_test_{index}"
        )

        # Retrieve the top 5 documents
        results = vector_store.similarity_search(
            question,
            k=5
        )

        for result_number, result in enumerate(results, start=1):

            print(f"\nResult {result_number}")
            print("Source:", result.metadata.get("source"))
            print("Content:")
            print(result.page_content[:300])

    print("\n========== EMBEDDING COMPARISON COMPLETED ==========")


if __name__ == "__main__":

    question = "What is the hospital incident reporting procedure?"

    print("Test Question:", question)

    compare_embedding_models(question)
