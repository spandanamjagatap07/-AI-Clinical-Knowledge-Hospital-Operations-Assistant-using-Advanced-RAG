
from sqlalchemy import text
from backend.database.db_connection import engine


def execute_query(query, params=None):
    """
    Execute a SQL query and return the results.
    """

    with engine.connect() as connection:
        result = connection.execute(
            text(query),
            params or {}
        )

        rows = result.fetchall()

        return [dict(row._mapping) for row in rows]


if __name__ == "__main__":

    query = """
        SELECT patient_id, patient_name, age, city
        FROM patients
        LIMIT 5
    """

    results = execute_query(query)

    print("\n========== SQL SERVICE TEST ==========")

    for patient in results:
        print(patient)

    print("\nTotal records retrieved:", len(results))
