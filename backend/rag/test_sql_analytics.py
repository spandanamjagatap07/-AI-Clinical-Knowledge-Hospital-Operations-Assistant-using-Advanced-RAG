
from backend.rag.sql_analytics import handle_sql_question


questions = [
    "How many patients are registered?",
    "Show appointment statistics",
    "Which pharmacy items need restocking?",
    "Show incidents by severity",
    "Show appointments by department",
    "Show admission statistics"
]

for question in questions:

    print("\n================================")
    print("QUESTION:", question)

    result = handle_sql_question(question)

    print("ANSWER:", result)
