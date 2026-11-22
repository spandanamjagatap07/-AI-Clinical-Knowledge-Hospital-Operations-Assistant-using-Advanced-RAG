
from backend.database.sql_service import execute_query


def get_total_patients():
    query = """
        SELECT COUNT(*) AS total_patients
        FROM patients
    """
    return execute_query(query)


def get_appointment_summary():
    query = """
        SELECT status, COUNT(*) AS total
        FROM appointments
        GROUP BY status
    """
    return execute_query(query)


def get_low_stock_items():
    query = """
        SELECT item_id, item_name, quantity, reorder_level
        FROM pharmacy_inventory
        WHERE quantity < reorder_level
        ORDER BY quantity ASC
    """
    return execute_query(query)


def get_incident_summary():
    query = """
        SELECT severity, COUNT(*) AS total
        FROM incident_reports
        GROUP BY severity
    """
    return execute_query(query)


def get_department_summary():
    query = """
        SELECT d.department_name, COUNT(a.appointment_id) AS total_appointments
        FROM departments d
        LEFT JOIN appointments a
        ON d.department_id = (
            SELECT department_id
            FROM doctors
            WHERE doctor_id = a.doctor_id
        )
        GROUP BY d.department_name
    """
    return execute_query(query)


def get_admission_summary():
    query = """
        SELECT admission_type, COUNT(*) AS total
        FROM admissions
        GROUP BY admission_type
    """
    return execute_query(query)


def get_department_with_most_appointments():

    query = """
        SELECT
            d.department_name,
            COUNT(a.appointment_id) AS total_appointments
        FROM departments d
        LEFT JOIN doctors doc
            ON d.department_id = doc.department_id
        LEFT JOIN appointments a
            ON doc.doctor_id = a.doctor_id
        GROUP BY d.department_id, d.department_name
        ORDER BY total_appointments DESC
        LIMIT 1
    """

    return execute_query(query)



def handle_sql_question(question):

    question = question.lower()

    # 1. Department with the highest appointments
    if "most" in question and "department" in question:
        return get_department_with_most_appointments()

    # 2. Department-wise appointment summary
    elif "department" in question:
        return get_department_summary()

    # 3. Patient count
    elif "patient" in question:
        return get_total_patients()

    # 4. Appointment statistics
    elif "appointment" in question:
        return get_appointment_summary()

    # 5. Pharmacy stock and restocking
    elif (
        "stock" in question
        or "restock" in question
        or "inventory" in question
    ):
        return get_low_stock_items()

    # 6. Incident statistics
    elif "incident" in question:
        return get_incident_summary()

    # 7. Admission statistics
    elif "admission" in question:
        return get_admission_summary()

    # 8. Unsupported question
    else:
        return {
            "message": "Sorry, I cannot handle this SQL question yet."
        }



if __name__ == "__main__":

    print("\n========== SQL ANALYTICS TEST ==========")

    print("\nTotal Patients:")
    print(get_total_patients())

    print("\nAppointment Summary:")
    print(get_appointment_summary())

    print("\nLow Stock Items:")
    print(get_low_stock_items())

    print("\nIncident Summary:")
    print(get_incident_summary())

    print("\nDepartment Appointment Summary:")
    print(get_department_summary())

    print("\nAdmission Summary:")
    print(get_admission_summary())