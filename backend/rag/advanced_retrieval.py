
from query_expansion import expand_query
from vector_store import load_vector_store


def multi_query_search(question: str, k: int = 3):
    """
    Search ChromaDB using the original question
    and its expanded queries.
    """

    vector_store = load_vector_store()

    expanded_queries = expand_query(question)

    all_results = []
    seen_content = set()

    print("\n========== EXPANDED QUERIES ==========")

    for query in expanded_queries:
        print(f"\nSearching: {query}")

        results = vector_store.similarity_search_with_score(
            query,
            k=k
        )

        for document, distance in results:
            content_key = document.page_content.strip()

            # Avoid showing duplicate chunks
            if content_key not in seen_content:
                seen_content.add(content_key)

                all_results.append({
                    "document": document,
                    "distance": distance,
                    "query": query
                })

    # Sort results by distance (lower is generally better)
    all_results.sort(key=lambda item: item["distance"])

    return all_results


if __name__ == "__main__":

    question = input("\nEnter your hospital question: ")

    results = multi_query_search(question, k=3)

    print("\n========== MULTI-QUERY SEARCH RESULTS ==========")

    for index, result in enumerate(results, start=1):

        document = result["document"]

        print(f"\nResult {index}")
        print("Source:", document.metadata.get("source"))
        print("Matched query:", result["query"])
        print("Distance:", result["distance"])
        print("Content:")
        print(document.page_content)
