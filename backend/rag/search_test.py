
from vector_store import load_vector_store


def search_hospital_documents(question):

    vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(
        question,
        k=3
    )

    print("\nQUESTION:", question)
    print("\n========== SEARCH RESULTS ==========")

    for index, (document, score) in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("Source:", document.metadata.get("source"))
        print("Content:", document.page_content)
        print("Distance:", score)


if __name__ == "__main__":

    question = input("Ask a hospital-related question: ")

    search_hospital_documents(question)
