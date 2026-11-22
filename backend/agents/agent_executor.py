
from backend.agents.question_router import route_question
from backend.rag.vector_store import load_vector_store
from backend.rag.sql_analytics import handle_sql_question
from backend.agents.report_generator import generate_incident_report
from backend.rag.conversation_memory import ConversationMemory
from backend.agents.followup_handler import process_followup_question
from backend.agents.clinical_answer_generator import generate_clinical_answer


# Create conversation memory for this running session
memory = ConversationMemory(max_messages=10)


def run_clinical_rag(question):
    """Retrieve documents and generate a structured answer."""

    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        question,
        k=5
    )

    if not results:
        return "No relevant clinical documents found."

    # Generate a structured answer using retrieved documents
    response = generate_clinical_answer(
        question,
        results
    )

    return response


def run_sql_analytics(question):
    """Execute SQL analytics."""

    return handle_sql_question(question)


def run_report_generator(question):
    """Generate a report."""

    q = question.lower()

    if "incident" in q:
        return generate_incident_report()

    return "Currently, only incident summary reports are supported."


def execute_agent(question):
    """Process follow-up, route the question and save conversation."""

    processed_question = process_followup_question(
        question,
        memory.get_history()
    )

    print("\nOriginal Question:", question)
    print("Processed Question:", processed_question)

    memory.add_message("user", question)

    print("\n========== CONVERSATION CONTEXT ==========")
    print(memory.get_context())

    selected_route = route_question(processed_question)

    print(f"\nSelected Route: {selected_route}")

    if selected_route == "clinical_rag":
        result = run_clinical_rag(processed_question)

    elif selected_route == "sql_analytics":
        result = run_sql_analytics(processed_question)

    elif selected_route == "report_generator":
        result = run_report_generator(processed_question)

    else:
        result = "Unable to process the question."

    memory.add_message("assistant", str(result))

    return result


if __name__ == "__main__":

    test_questions = [
        "What is the hospital incident reporting procedure?"
    ]

    for question in test_questions:

        print("\n" + "=" * 60)
        print("QUESTION:", question)
        print("=" * 60)

        result = execute_agent(question)

        print("\nRESPONSE:")
        print(result)

    print("\n========== FINAL CONVERSATION HISTORY ==========")

    for message in memory.get_history():
        print(f"{message['role'].capitalize()}: {message['content'][:200]}")

    print("\nTotal messages:", len(memory.get_history()))
