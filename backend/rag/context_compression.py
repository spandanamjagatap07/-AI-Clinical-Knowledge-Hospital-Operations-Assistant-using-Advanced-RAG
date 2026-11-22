
from backend.rag.reranking import reranker, search_with_reranking


def compress_documents(question, documents, max_lines=12):
    """
    Keep the lines most relevant to the question.
    Uses the same CrossEncoder model as the reranking step.
    """

    if not documents:
        return []

    candidates = []

    # Break each retrieved document into individual non-empty lines.
    for doc_index, document in enumerate(documents):
        lines = [
            line.strip()
            for line in document["content"].splitlines()
            if line.strip()
        ]

        for line_index, line in enumerate(lines):
            candidates.append({
                "doc_index": doc_index,
                "line_index": line_index,
                "line": line
            })

    if not candidates:
        return []

    # Score each line against the original question.
    pairs = [
        (question, candidate["line"])
        for candidate in candidates
    ]

    scores = reranker.predict(pairs)

    for candidate, score in zip(candidates, scores):
        candidate["score"] = float(score)

    # Select the most relevant lines.
    selected = sorted(
        candidates,
        key=lambda item: item["score"],
        reverse=True
    )[:max_lines]

    # Group selected lines by their original document.
    compressed_documents = []

    for doc_index, document in enumerate(documents):
        selected_lines = [
            item for item in selected
            if item["doc_index"] == doc_index
        ]

        # Restore the original order of the selected lines.
        selected_lines.sort(key=lambda item: item["line_index"])

        if not selected_lines:
            continue

        compressed_document = document.copy()
        compressed_document["content"] = "\n".join(
            item["line"] for item in selected_lines
        )

        compressed_documents.append(compressed_document)

    return compressed_documents


def search_with_compression(question, top_k=5, max_lines=12):
    # First retrieve and rerank documents.
    documents = search_with_reranking(
        question,
        top_k=top_k
    )

    # Then compress their content.
    compressed_documents = compress_documents(
        question,
        documents,
        max_lines=max_lines
    )

    return compressed_documents


if __name__ == "__main__":
    question = "What is the hospital incident reporting procedure?"

    print("\n========== COMPRESSED SEARCH RESULTS ==========\n")

    results = search_with_compression(
        question,
        top_k=5,
        max_lines=12
    )

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Source:", result["metadata"].get("source", "Unknown"))
        print("Compressed Content:")
        print(result["content"])
        print("-" * 50)

    print("\n========== CONTEXT COMPRESSION COMPLETED ==========")
