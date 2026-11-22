
from backend.database.sql_service import execute_query


def generate_incident_report():

    # Get total incident count
    total_result = execute_query("""
        SELECT COUNT(*) AS total_incidents
        FROM incident_reports
    """)

    total_incidents = total_result[0]["total_incidents"]

    # Get incident counts by severity
    severity_summary = execute_query("""
        SELECT severity, COUNT(*) AS incident_count
        FROM incident_reports
        GROUP BY severity
        ORDER BY severity
    """)

    # Get incident details with department names
    incident_details = execute_query("""
        SELECT
            ir.incident_id,
            d.department_name,
            ir.incident_type,
            ir.severity,
            ir.incident_date,
            ir.status
        FROM incident_reports ir
        LEFT JOIN departments d
            ON ir.department_id = d.department_id
        ORDER BY ir.incident_date DESC
    """)

    # Build the report
    report = []

    report.append("=" * 55)
    report.append("HOSPITAL INCIDENT SUMMARY REPORT")
    report.append("=" * 55)

    report.append(f"\nTotal Incidents: {total_incidents}")

    report.append("\nINCIDENTS BY SEVERITY")
    report.append("-" * 35)

    for item in severity_summary:
        report.append(
            f"{item['severity']}: {item['incident_count']}"
        )

    report.append("\nINCIDENT DETAILS")
    report.append("-" * 55)

    for incident in incident_details:
        report.append(
            f"\nIncident ID: {incident['incident_id']}"
            f"\nDepartment: {incident['department_name']}"
            f"\nType: {incident['incident_type']}"
            f"\nSeverity: {incident['severity']}"
            f"\nDate: {incident['incident_date']}"
            f"\nStatus: {incident['status']}"
        )

    report.append("\n" + "=" * 55)
    report.append("END OF REPORT")
    report.append("=" * 55)

    return "\n".join(report)


if __name__ == "__main__":

    result = generate_incident_report()

    print(result)
