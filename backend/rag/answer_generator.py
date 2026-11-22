
def generate_clinical_answer(question, documents):
    """
    Format retrieved clinical documents into a structured,
    evidence-based response with source references.

    This is an extractive formatter, not an LLM-generated answer.
    """

    if not documents:
        return "No relevant information was found in the hospital documents."

    response = []

    response.append("=" * 60)
    response.append("CLINICAL KNOWLEDGE RESPONSE")
    response.append("=" * 60)

    response.append(f"\nQUESTION: {question}")

    response.append("\nRELEVANT INFORMATION")
    response.append("-" * 60)

    sources = []
    seen_content = set()

    for index, document in enumerate(documents, start=1):

        content = document.page_content.strip()
        metadata = document.metadata or {}

        # Avoid displaying identical content more than once.
        if content in seen_content:
            continue

        seen_content.add(content)

        source = metadata.get("source", "Unknown document")
        department = metadata.get("department", "Not specified")
        document_type = metadata.get("document_type", "Not specified")
        version = metadata.get("version", "Not specified")
        page = metadata.get("page")

        response.append(f"\nEvidence {len(sources) + 1}:")
        response.append(content)

        response.append(f"\nSource: {source}")
        response.append(f"Department: {department}")
        response.append(f"Document Type: {document_type}")
        response.append(f"Version: {version}")

        if page is not None:
            response.append(f"Page: {page}")

        sources.append(source)

    response.append("\n" + "=" * 60)
    response.append("SOURCE DOCUMENTS")
    response.append("=" * 60)

    for index, source in enumerate(dict.fromkeys(sources), start=1):
        response.append(f"[{index}] {source}")

    response.append("\nNote: This response presents retrieved document evidence.")
    response.append("It does not replace approved clinical guidance.")

    return "\n".join(response)


if __name__ == "__main__":

    from backend.rag.vector_store import load_vector_store

    question = "What is the hospital incident reporting procedure?"

    vector_store = load_vector_store()

    retrieved_documents = vector_store.similarity_search(
        question,
        k=5
    )

    answer = generate_clinical_answer(
        question,
        retrieved_documents
    )

    print(answer)
