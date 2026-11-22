
from pathlib import Path
from uuid import uuid4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma

from backend.rag.document_loader import load_directory
from backend.rag.vector_store import create_embedding_model


BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"

CHILD_DB_PATH = BASE_DIR / "chroma_parent_child"


def create_parent_child_chunks(
    documents,
    parent_size=1000,
    child_size=300
):
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=parent_size,
        chunk_overlap=100
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=child_size,
        chunk_overlap=50
    )

    parent_documents = []
    child_documents = []

    for document in documents:

        parents = parent_splitter.split_documents([document])

        for parent in parents:

            parent_id = str(uuid4())

            parent.metadata["parent_id"] = parent_id

            parent_documents.append(parent)

            children = child_splitter.split_documents([parent])

            for child in children:

                child.metadata["parent_id"] = parent_id
                child.metadata["child_id"] = str(uuid4())

                child_documents.append(child)

    return parent_documents, child_documents


def search_parent_child(question, top_k=3):

    documents = load_directory(DOCUMENTS_DIR)

    parents, children = create_parent_child_chunks(documents)

    embedding_model = create_embedding_model()

    child_vector_store = Chroma.from_documents(
        documents=children,
        embedding=embedding_model,
        collection_name="hospital_child_chunks",
        persist_directory=str(CHILD_DB_PATH)
    )

    child_results = child_vector_store.similarity_search(
        question,
        k=top_k
    )

    parent_lookup = {
        parent.metadata["parent_id"]: parent
        for parent in parents
    }

    retrieved_parents = []
    seen_parent_ids = set()

    for child in child_results:

        parent_id = child.metadata.get("parent_id")

        if (
            parent_id in parent_lookup
            and parent_id not in seen_parent_ids
        ):
            retrieved_parents.append(parent_lookup[parent_id])
            seen_parent_ids.add(parent_id)

    return child_results, retrieved_parents


if __name__ == "__main__":

    question = "What is the hospital incident reporting procedure?"

    child_results, parent_results = search_parent_child(question)

    print("\n========== PARENT-CHILD RETRIEVAL ==========")

    print("\nQuestion:", question)

    print("\nMatching child chunks:", len(child_results))

    for index, child in enumerate(child_results, start=1):
        print(f"\nChild Result {index}:")
        print(child.page_content[:300])

    print("\nRetrieved parent chunks:", len(parent_results))

    for index, parent in enumerate(parent_results, start=1):
        print(f"\nParent Result {index}:")
        print("Source:", parent.metadata.get("source"))
        print(parent.page_content[:500])

    print("\n========== PARENT-CHILD RETRIEVAL COMPLETED ==========")
