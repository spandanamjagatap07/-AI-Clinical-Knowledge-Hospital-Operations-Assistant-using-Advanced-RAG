
from sqlalchemy import text
from backend.database.db_connection import engine

TABLES = [
    "departments",
    "patients",
    "doctors",
    "nurses",
    "appointments",
    "admissions",
    "discharges",
    "lab_results",
    "pharmacy_inventory",
    "prescriptions",
    "billing",
    "insurance",
    "bed_management",
    "ot_schedule",
    "incident_reports",
]

print("\n========== DATABASE VERIFICATION ==========")

total_records = 0

with engine.connect() as connection:
    for table in TABLES:
        count = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar()

        total_records += count

        print(f"{table}: {count} records")

print("\nTotal records in database:", total_records)
print("========== VERIFICATION COMPLETED ==========")
