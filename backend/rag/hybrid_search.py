
from pathlib import Path
import re

from rank_bm25 import BM25Okapi
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# ChromaDB configuration
CHROMA_PATH = BASE_DIR / "chroma_db"
COLLECTION_NAME = "hospital_knowledge"

# Use the SAME embedding model used during ingestion
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def tokenize(text):
    """
    Convert text into lowercase keyword tokens.
    """
    return re.findall(r"\b\w+\b", text.lower())


def get_vector_store():
    """
    Connect to the existing ChromaDB collection.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )

    return vector_store


def hybrid_search(query, k=5, vector_k=10, bm25_k=10):
    """
    Perform hybrid retrieval using:
    1. Vector similarity search
    2. BM25 keyword search
    3. Reciprocal Rank Fusion (RRF)
    """

    vector_store = get_vector_store()

    # --------------------------------
    # STEP 1: Retrieve all indexed chunks
    # --------------------------------

    stored_data = vector_store.get(
        include=["documents", "metadatas"]
    )

    documents = stored_data["documents"]
    metadatas = stored_data["metadatas"]

    if not documents:
        return []

    # --------------------------------
    # STEP 2: BM25 keyword search
    # --------------------------------

    tokenized_corpus = [
        tokenize(document)
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    query_tokens = tokenize(query)

    bm25_scores = bm25.get_scores(query_tokens)

    bm25_ranking = sorted(
        range(len(bm25_scores)),
        key=lambda i: bm25_scores[i],
        reverse=True
    )[:bm25_k]

    # --------------------------------
    # STEP 3: Vector similarity search
    # --------------------------------

    vector_results = vector_store.similarity_search(
        query,
        k=vector_k
    )

    # --------------------------------
    # STEP 4: Combine results using RRF
    # --------------------------------

    combined_scores = {}
    document_data = {}

    def get_key(content, metadata):
        return (
            content,
            str(metadata.get("source", ""))
        )

    # Add BM25 rankings
    for rank, index in enumerate(bm25_ranking, start=1):

        content = documents[index]
        metadata = metadatas[index] or {}

        key = get_key(content, metadata)

        combined_scores[key] = (
            combined_scores.get(key, 0)
            + 1 / (60 + rank)
        )

        document_data[key] = {
            "content": content,
            "metadata": metadata
        }

    # Add vector rankings
    for rank, document in enumerate(vector_results, start=1):

        content = document.page_content
        metadata = document.metadata or {}

        key = get_key(content, metadata)

        combined_scores[key] = (
            combined_scores.get(key, 0)
            + 1 / (60 + rank)
        )

        document_data[key] = {
            "content": content,
            "metadata": metadata
        }

    # --------------------------------
    # STEP 5: Sort combined results
    # --------------------------------

    ranked_results = sorted(
        combined_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    final_results = []

    for key, score in ranked_results[:k]:

        result = document_data[key].copy()
        result["hybrid_score"] = round(score, 5)

        final_results.append(result)

    return final_results


# --------------------------------
# TEST HYBRID SEARCH
# --------------------------------

if __name__ == "__main__":

    question = (
        "What is the hospital incident reporting procedure?"
    )

    print("\n========== HYBRID SEARCH ==========")

    print("\nQuestion:", question)

    results = hybrid_search(question)

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")

        print(
            "Source:",
            result["metadata"].get("source", "Unknown")
        )

        print(
            "Hybrid Score:",
            result["hybrid_score"]
        )

        print(
            "Content:",
            result["content"][:500]
        )

    print("\n========== SEARCH COMPLETED ==========")
