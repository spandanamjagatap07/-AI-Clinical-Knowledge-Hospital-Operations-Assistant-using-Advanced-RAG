
from sqlalchemy import text
from db_connection import engine


def run_query(title, query):
    print(f"\n========== {title} ==========")

    with engine.connect() as connection:
        result = connection.execute(text(query))

        for row in result:
            print(row)


# Query 1: Display all hospital departments
run_query(
    "HOSPITAL DEPARTMENTS",
    """
    SELECT * FROM departments
    """
)

# Query 2: Display the total number of patients
run_query(
    "TOTAL PATIENTS",
    """
    SELECT COUNT(*) AS total_patients
    FROM patients
    """
)

# Query 3: Display appointment counts by status
run_query(
    "APPOINTMENTS BY STATUS",
    """
    SELECT status, COUNT(*) AS total_appointments
    FROM appointments
    GROUP BY status
    """
)

# Query 4: Display available pharmacy inventory
run_query(
    "PHARMACY INVENTORY",
    """
    SELECT item_name, quantity, reorder_level
    FROM pharmacy_inventory
    ORDER BY quantity ASC
    LIMIT 10
    """
)

# Query 5: Display incident reports by severity
run_query(
    "INCIDENT REPORTS BY SEVERITY",
    """
    SELECT severity, COUNT(*) AS total_incidents
    FROM incident_reports
    GROUP BY severity
    """
)


# Query 6: Find pharmacy items below reorder level
run_query(
    "PHARMACY ITEMS BELOW REORDER LEVEL",
    """
    SELECT item_id, item_name, quantity, reorder_level
    FROM pharmacy_inventory
    WHERE quantity < reorder_level
    ORDER BY quantity ASC
    """
)
