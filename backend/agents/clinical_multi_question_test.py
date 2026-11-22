
from backend.agents.agent_executor import execute_agent


test_questions = [
    "What does the nursing protocol say about nursing procedures?",
    "What is the emergency response procedure?",
    "What do the pharmacy guidelines say?",
    "What procedures are described in the laboratory manual?"
]


if __name__ == "__main__":

    print("\n========== MULTI-QUESTION CLINICAL RAG TEST ==========")

    for index, question in enumerate(test_questions, start=1):

        print("\n" + "=" * 70)
        print(f"TEST QUESTION {index}")
        print("=" * 70)

        print(f"\nQUESTION: {question}")

        result = execute_agent(question)

        print("\n========== GENERATED RESPONSE ==========")
        print(result)

    print("\n========== ALL CLINICAL TESTS COMPLETED ==========")
