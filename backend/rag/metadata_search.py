
from vector_store import load_vector_store


def search_by_department(question, department):
    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        question,
        k=5,
        filter={"department": department}
    )

    for index, doc in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Source:", doc.metadata.get("source"))
        print("Department:", doc.metadata.get("department"))
        print("Content:", doc.page_content)


if __name__ == "__main__":
    question = "What is the incident investigation procedure?"

    search_by_department(question, "Quality")
