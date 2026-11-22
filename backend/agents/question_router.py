
# Agentic RAG - Question Router

REPORT_KEYWORDS = [
    "generate report",
    "create report",
    "prepare report",
    "write report",
    "create a checklist",
    "prepare checklist",
    "generate checklist"
]

CLINICAL_KEYWORDS = [
    "procedure",
    "guideline",
    "policy",
    "sop",
    "protocol",
    "manual",
    "clinical pathway",
    "workflow"
]

SQL_KEYWORDS = [
    "how many",
    "count",
    "statistics",
    "by department",
    "appointments",
    "patients",
    "admissions",
    "discharges",
    "lab results",
    "pharmacy inventory",
    "stock",
    "restock",
    "billing",
    "insurance",
    "bed",
    "ot schedule",
    "doctors",
    "nurses",
    "incidents by severity"
]


def route_question(question):
    q = question.lower().strip()

    # 1. Detect report or checklist generation requests
    report_actions = [
        "generate",
        "create",
        "prepare",
        "write",
        "make"
    ]

    report_types = [
        "report",
        "checklist"
    ]

    if (
        any(action in q for action in report_actions)
        and any(report_type in q for report_type in report_types)
    ):
        return "report_generator"

    # 2. Detect clinical knowledge questions
    clinical_keywords = [
        "procedure",
        "guideline",
        "policy",
        "sop",
        "protocol",
        "manual",
        "clinical pathway",
        "workflow"
    ]

    if any(keyword in q for keyword in clinical_keywords):
        return "clinical_rag"

    # 3. Detect SQL analytics questions
    sql_keywords = [
        "how many",
        "count",
        "statistics",
        "by department",
        "appointments",
        "patients",
        "admissions",
        "discharges",
        "lab results",
        "pharmacy inventory",
        "stock",
        "restock",
        "billing",
        "insurance",
        "bed",
        "ot schedule",
        "doctors",
        "nurses",
        "incidents by severity"
    ]

    if any(keyword in q for keyword in sql_keywords):
        return "sql_analytics"

    # 4. Default route
    return "clinical_rag"



if __name__ == "__main__":

    test_questions = [
        "What is the hospital incident reporting procedure?",
        "How many patients are registered?",
        "Show appointments by department",
        "Generate an incident report",
        "What is the infection control policy?",
        "Which pharmacy items need restocking?",
        "Show incidents by severity",
        "Explain the nursing protocol"
    ]

    print("\n========== AGENTIC RAG QUESTION ROUTER ==========\n")

    for question in test_questions:
        selected_route = route_question(question)

        print("Question:", question)
        print("Selected Route:", selected_route)
        print("----------------------------------------")

    print("\n========== ROUTING TEST COMPLETED ==========")
