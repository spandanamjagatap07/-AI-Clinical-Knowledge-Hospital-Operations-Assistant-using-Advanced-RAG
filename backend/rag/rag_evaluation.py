
from backend.rag.vector_store import load_vector_store


# Evaluation questions and expected relevant documents.
# These are manually labelled examples for our synthetic dataset.

EVALUATION_DATA = [
    {
        "question": "What is the hospital incident reporting procedure?",
        "relevant_sources": [
            "incident_investigation.txt",
            "infection_control.txt",
            "quality_audit_report.txt"
        ]
    },
    {
        "question": "What is the nursing documentation procedure?",
        "relevant_sources": [
            "nursing_protocol.txt",
            "patient_care_policy.txt"
        ]
    },
    {
        "question": "What are the hospital emergency response steps?",
        "relevant_sources": [
            "emergency_response.txt"
        ]
    },
    {
        "question": "What are the pharmacy inventory guidelines?",
        "relevant_sources": [
            "pharmacy_guidelines.txt"
        ]
    },
    {
        "question": "What is the laboratory testing procedure?",
        "relevant_sources": [
            "laboratory_manual.txt"
        ]
    }
]


def precision_at_k(retrieved_sources, relevant_sources, k=5):

    retrieved = retrieved_sources[:k]

    if not retrieved:
        return 0.0

    relevant_count = sum(
        1 for source in retrieved
        if source in relevant_sources
    )

    return relevant_count / len(retrieved)


def recall_at_k(retrieved_sources, relevant_sources, k=5):

    if not relevant_sources:
        return 0.0

    retrieved = retrieved_sources[:k]

    relevant_count = sum(
        1 for source in retrieved
        if source in relevant_sources
    )

    return relevant_count / len(relevant_sources)


def reciprocal_rank(retrieved_sources, relevant_sources):

    for rank, source in enumerate(retrieved_sources, start=1):

        if source in relevant_sources:
            return 1 / rank

    return 0.0


def evaluate_rag(k=5):

    vector_store = load_vector_store()

    total_precision = 0
    total_recall = 0
    total_mrr = 0

    print("\n========== RAG EVALUATION ==========")

    for index, item in enumerate(EVALUATION_DATA, start=1):

        question = item["question"]
        relevant_sources = item["relevant_sources"]

        results = vector_store.similarity_search(
            question,
            k=k
        )

        retrieved_sources = [
            result.metadata.get("source", "")
            for result in results
        ]

        precision = precision_at_k(
            retrieved_sources,
            relevant_sources,
            k
        )

        recall = recall_at_k(
            retrieved_sources,
            relevant_sources,
            k
        )

        mrr = reciprocal_rank(
            retrieved_sources,
            relevant_sources
        )

        total_precision += precision
        total_recall += recall
        total_mrr += mrr

        print(f"\nQuestion {index}: {question}")

        print("Retrieved documents:", retrieved_sources)
        print("Relevant documents:", relevant_sources)

        print(f"Precision@{k}: {precision:.4f}")
        print(f"Recall@{k}: {recall:.4f}")
        print(f"MRR: {mrr:.4f}")

    total_questions = len(EVALUATION_DATA)

    print("\n========== FINAL EVALUATION ==========")

    print(
        f"Average Precision@{k}: "
        f"{total_precision / total_questions:.4f}"
    )

    print(
        f"Average Recall@{k}: "
        f"{total_recall / total_questions:.4f}"
    )

    print(
        f"Mean Reciprocal Rank: "
        f"{total_mrr / total_questions:.4f}"
    )

    print("\n========== EVALUATION COMPLETED ==========")


if __name__ == "__main__":
    evaluate_rag(k=5)
