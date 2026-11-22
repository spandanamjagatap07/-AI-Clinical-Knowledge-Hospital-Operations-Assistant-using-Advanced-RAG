
def expand_query(question: str) -> list[str]:
    """
    Generate alternative search queries using simple
    rule-based expansion.
    """

    expansions = {
        "incident": [
            "hospital incident reporting procedure",
            "incident investigation workflow",
            "incident documentation and corrective actions"
        ],
        "appointment": [
            "patient appointment scheduling",
            "appointment booking and management",
            "doctor appointment records"
        ],
        "lab": [
            "laboratory test results",
            "pending laboratory reports",
            "lab report processing workflow"
        ],
        "pharmacy": [
            "pharmacy inventory management",
            "medicine stock availability",
            "prescription and medication records"
        ],
        "discharge": [
            "patient discharge procedure",
            "discharge documentation",
            "patient discharge checklist"
        ]
    }

    queries = [question]
    question_lower = question.lower()

    for keyword, alternatives in expansions.items():
        if keyword in question_lower:
            queries.extend(alternatives)

    # Remove duplicate queries while preserving order
    return list(dict.fromkeys(queries))


if __name__ == "__main__":
    question = "What is the hospital incident reporting procedure?"

    expanded = expand_query(question)

    print("\nOriginal question:")
    print(question)

    print("\nExpanded search queries:")
    for query in expanded:
        print("-", query)
