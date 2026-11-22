
import re

from backend.rag.vector_store import load_vector_store
from backend.agents.clinical_answer_generator import generate_clinical_answer


# Expected content for each test question
evaluation_dataset = [
    {
        "question": "What does the nursing protocol say about nursing procedures?",
        "expected_source": "nursing_protocol.txt",
        "expected_steps": [
            "verify the patient's authorized hospital record",
            "record observations",
            "document relevant handover information",
            "escalate missing or inconsistent records",
            "follow the hospital's approved clinical protocols"
        ]
    },
    {
        "question": "What is the emergency response procedure?",
        "expected_source": "emergency_response.txt",
        "expected_steps": [
            "register the emergency event",
            "notify the designated response team",
            "record event timestamps",
            "maintain communication records",
            "document event closure",
            "complete the required incident report"
        ]
    },
    {
        "question": "What do the pharmacy guidelines say?",
        "expected_source": "pharmacy_guidelines.txt",
        "expected_steps": [
            "record incoming inventory",
            "update available stock",
            "monitor expiry information",
            "identify items below reorder levels",
            "record dispensing transactions",
            "escalate inventory discrepancies"
        ]
    },
    {
        "question": "What procedures are described in the laboratory manual?",
        "expected_source": "laboratory_manual.txt",
        "expected_steps": [
            "register the laboratory request",
            "verify sample identification",
            "record sample receipt",
            "track processing status",
            "record result verification",
            "escalate delayed or rejected samples"
        ]
    }
]


def normalize_text(text):
    """
    Normalize text before comparing expected steps.
    Handles curly apostrophes, punctuation and extra spaces.
    """
    text = text.lower()

    text = text.replace("’", "'")
    text = text.replace("‘", "'")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def evaluate_answer(response, expected_steps, expected_source):

    # Separate answer and source sections
    parts = response.split("SOURCE DOCUMENTS", 1)

    answer_text = normalize_text(parts[0])

    source_text = parts[1] if len(parts) > 1 else ""

    # Check expected procedure steps
    covered_steps = [
        step for step in expected_steps
        if normalize_text(step) in answer_text
    ]

    # Debug expected-step matching
    print("\n--- STEP MATCHING DEBUG ---")

    for step in expected_steps:
        normalized_step = normalize_text(step)

        print(
            f"{'MATCH' if normalized_step in answer_text else 'MISSING'}: "
            f"{step}"
        )

    step_coverage = len(covered_steps) / len(expected_steps)

    # Extract source filenames
    cited_sources = re.findall(
        r"Source:\s*(.+)",
        source_text
    )

    cited_sources = [
        source.strip() for source in cited_sources
    ]

    # Calculate citation precision
    relevant_citations = [
        source for source in cited_sources
        if source == expected_source
    ]

    citation_precision = (
        len(relevant_citations) / len(cited_sources)
        if cited_sources else 0
    )

    # Calculate citation recall
    citation_recall = (
        1.0 if expected_source in cited_sources else 0.0
    )

    return {
        "total_steps": len(expected_steps),
        "covered_steps": len(covered_steps),
        "step_coverage": step_coverage,
        "cited_sources": cited_sources,
        "citation_precision": citation_precision,
        "citation_recall": citation_recall
    }


def evaluate_answer(response, expected_steps, expected_source):

    # Separate answer and source sections
    parts = response.split("SOURCE DOCUMENTS", 1)

    answer_text = normalize_text(parts[0])

    source_text = parts[1] if len(parts) > 1 else ""

    # Check expected procedure steps
    covered_steps = [
        step for step in expected_steps
        if normalize_text(step) in answer_text
    ]

    step_coverage = len(covered_steps) / len(expected_steps)

    # Extract source filenames
    cited_sources = re.findall(
        r"Source:\s*(.+)",
        source_text
    )

    cited_sources = [
        source.strip() for source in cited_sources
    ]

    # Calculate citation precision
    relevant_citations = [
        source for source in cited_sources
        if source == expected_source
    ]

    citation_precision = (
        len(relevant_citations) / len(cited_sources)
        if cited_sources else 0
    )

    # Calculate citation recall
    citation_recall = (
        1.0 if expected_source in cited_sources else 0.0
    )

    return {
        "total_steps": len(expected_steps),
        "covered_steps": len(covered_steps),
        "step_coverage": step_coverage,
        "cited_sources": cited_sources,
        "citation_precision": citation_precision,
        "citation_recall": citation_recall
    }





if __name__ == "__main__":

    vector_store = load_vector_store()

    all_results = []

    print("\n========== MULTI-QUESTION ANSWER EVALUATION ==========")

    for index, test in enumerate(evaluation_dataset, start=1):

        question = test["question"]

        print("\n" + "=" * 65)
        print(f"TEST {index}: {question}")
        print("=" * 65)

        # Retrieve relevant documents
        documents = vector_store.similarity_search(
            question,
            k=5
        )

        # Generate answer using Groq
        response = generate_clinical_answer(
            question,
            documents
        )

        print("\n========== GENERATED ANSWER ==========")
        print(response)

        # Evaluate answer
        metrics = evaluate_answer(
            response,
            test["expected_steps"],
            test["expected_source"]
        )

        all_results.append(metrics)

        print("\n========== TEST METRICS ==========")

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

        print(
            f"Covered Steps: "
            f"{metrics['covered_steps']}/"
            f"{metrics['total_steps']}"
        )

        print("Cited Sources:", metrics["cited_sources"])

    # Calculate averages
    total_tests = len(all_results)

    average_coverage = sum(
        item["step_coverage"] for item in all_results
    ) / total_tests

    average_precision = sum(
        item["citation_precision"] for item in all_results
    ) / total_tests

    average_recall = sum(
        item["citation_recall"] for item in all_results
    ) / total_tests

    print("\n" + "=" * 65)
    print("========== FINAL EVALUATION SUMMARY ==========")

    print(f"Total Questions Tested: {total_tests}")

    print(f"Average Step Coverage: {average_coverage:.2%}")

    print(f"Average Citation Precision: {average_precision:.2%}")

    print(f"Average Citation Recall: {average_recall:.2%}")

    print("\n========== EVALUATION COMPLETED ==========")
