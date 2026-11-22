
def process_followup_question(question, history):
    """
    Convert common follow-up questions into standalone questions
    using previous conversation messages.
    """

    q = question.lower().strip()

    # Find the previous user question
    previous_question = ""

    for message in reversed(history):
        if message["role"] == "user" and message["content"] != question:
            previous_question = message["content"].lower()
            break

    # Rule 1: Follow-up about appointments
    if "what about appointments" in q or "and appointments" in q:
        return "Show appointment statistics"

    # Rule 2: Ask which department has the most appointments
    if "which department has the most" in q:
        if "appointment" in previous_question:
            return "Which department has the most appointments?"

    # Rule 3: Follow-up about patients
    if "what about patients" in q or "and patients" in q:
        return "How many patients are registered?"

    # Rule 4: Follow-up about incidents
    if "what about incidents" in q or "and incidents" in q:
        return "Show incidents by severity"

    # Rule 5: Follow-up about pharmacy
    if "what about pharmacy" in q or "and pharmacy" in q:
        return "Which pharmacy items need restocking?"

    # Rule 6: Repeat the previous question
    if q in ["show those again", "repeat that", "show it again"]:
        if previous_question:
            return previous_question

    # If no follow-up rule matches, keep the original question
    return question


if __name__ == "__main__":

    # Simulated previous conversation
    history = [
        {
            "role": "user",
            "content": "How many patients are registered?"
        },
        {
            "role": "assistant",
            "content": "There are 100 registered patients."
        },
        {
            "role": "user",
            "content": "Show appointments by department"
        },
        {
            "role": "assistant",
            "content": "Appointment statistics by department."
        }
    ]

    test_questions = [
        "What about appointments?",
        "Which department has the most?",
        "What about patients?",
        "What about incidents?",
        "What about pharmacy?",
        "Show those again"
    ]

    print("\n========== FOLLOW-UP QUESTION TEST ==========")

    for question in test_questions:

        rewritten = process_followup_question(
            question,
            history
        )

        print("\nOriginal Question:", question)
        print("Processed Question:", rewritten)

    print("\n========== FOLLOW-UP TEST COMPLETED ==========")
