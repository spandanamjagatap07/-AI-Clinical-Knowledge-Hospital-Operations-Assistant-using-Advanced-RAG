
import re

from backend.rag.vector_store import load_vector_store
from backend.agents.clinical_answer_generator import generate_clinical_answer


def evaluate_answer(answer):
    """Evaluate answer coverage and source citation relevance."""

    # Expected incident investigation steps
    expected_steps = {
        "Register incident": ["register the incident"],
        "Assign investigation owner": ["assign an investigation owner"],
        "Collect records": ["collect relevant records"],
        "Document findings": ["document findings"],
        "Assign corrective actions": ["assign corrective actions"],
        "Track completion": ["track completion"],
        "Final review and closure": [
            "final review and closure",
            "final review",
            "record final review"
        ]
    }

    answer_lower = answer.lower()

    # Calculate step coverage
    covered_steps = []

    for step, phrases in expected_steps.items():

        if any(phrase in answer_lower for phrase in phrases):
            covered_steps.append(step)

    coverage = len(covered_steps) / len(expected_steps)

    # Extract cited source documents
    source_section = answer.split("SOURCE DOCUMENTS")

    cited_sources = []

    if len(source_section) > 1:
        cited_sources = re.findall(
            r"Source:\s*(.+)",
            source_section[1]
        )

    # Manually identified relevant sources for this question
    relevant_sources = {
        "incident_investigation.txt",
        "quality_audit_report.txt",
        "infection_control.txt"
    }

    relevant_citations = [
        source for source in cited_sources
        if source.strip() in relevant_sources
    ]

    citation_precision = (
        len(relevant_citations) / len(cited_sources)
        if cited_sources else 0
    )

    citation_recall = (
        len(set(relevant_citations)) / len(relevant_sources)
    )

    return {
        "total_expected_steps": len(expected_steps),
        "covered_steps": covered_steps,
        "step_coverage": coverage,
        "total_cited_sources": len(cited_sources),
        "relevant_sources": relevant_citations,
        "citation_precision": citation_precision,
        "citation_recall": citation_recall
    }


if __name__ == "__main__":

    question = "What is the hospital incident reporting procedure?"

    print("\n========== CLINICAL RAG EVALUATION ==========")

    # Retrieve documents
    vector_store = load_vector_store()

    documents = vector_store.similarity_search(
        question,
        k=5
    )

    # Generate answer using Groq
    answer = generate_clinical_answer(
        question,
        documents
    )

    print("\n========== GENERATED ANSWER ==========")
    print(answer)

    # Evaluate generated answer
    metrics = evaluate_answer(answer)

    print("\n========== EVALUATION RESULTS ==========")

    print(
        f"Step Coverage: "
        f"{metrics['step_coverage']:.2%}"
    )

    print(
        f"Citation Precision: "
        f"{metrics['citation_precision']:.2%}"
    )

    print(
        f"Citation Recall: "
        f"{metrics['citation_recall']:.2%}"
    )

    print("\nCovered Steps:")

    for step in metrics["covered_steps"]:
        print("-", step)

    print("\nRelevant Cited Sources:")

    for source in metrics["relevant_sources"]:
        print("-", source)

    print("\n========== EVALUATION COMPLETED ==========")
