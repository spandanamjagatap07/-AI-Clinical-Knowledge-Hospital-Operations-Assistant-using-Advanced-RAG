
from sentence_transformers import CrossEncoder
from backend.rag.hybrid_search import hybrid_search


# Load the reranking model
RERANKING_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(RERANKING_MODEL)


def rerank_documents(question, documents, top_k=5):
    """
    Rerank retrieved documents according to
    their relevance to the user's question.
    """

    if not documents:
        return []

    # Create question-document pairs
    pairs = [
        (question, document["content"])
        for document in documents
    ]

    # Calculate relevance scores
    scores = reranker.predict(pairs)

    # Attach scores to documents
    reranked_documents = []

    for document, score in zip(documents, scores):

        result = document.copy()
        result["rerank_score"] = float(score)

        reranked_documents.append(result)

    # Sort by relevance score
    reranked_documents.sort(
        key=lambda item: item["rerank_score"],
        reverse=True
    )

    return reranked_documents[:top_k]


def search_with_reranking(question, top_k=5):

    # Step 1: Retrieve more documents using hybrid search
    retrieved_documents = hybrid_search(
        question,
        k=10,
        vector_k=10,
        bm25_k=10
    )

    # Step 2: Rerank retrieved documents
    final_documents = rerank_documents(
        question,
        retrieved_documents,
        top_k=top_k
    )

    return final_documents


# Test reranking
if __name__ == "__main__":

    question = (
        "What is the hospital incident reporting procedure?"
    )

    print("\n========== RERANKING TEST ==========")
    print("\nQuestion:", question)

    results = search_with_reranking(question)

    for index, result in enumerate(results, start=1):

        print(f"\nResult {index}")

        print(
            "Source:",
            result["metadata"].get("source", "Unknown")
        )

        print(
            "Rerank Score:",
            round(result["rerank_score"], 4)
        )

        print(
            "Content:",
            result["content"][:500]
        )

    print("\n========== RERANKING COMPLETED ==========")
