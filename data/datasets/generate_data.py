
import csv
import random
from pathlib import Path
from datetime import date, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

BASE_DIR = Path(__file__).resolve().parent
BASE_DIR.mkdir(parents=True, exist_ok=True)

def random_date(days_back=180):
    return (date.today() - timedelta(
        days=random.randint(0, days_back)
    )).isoformat()

def save_csv(filename, rows):
    if not rows:
        return

    filepath = BASE_DIR / filename

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created: {filepath.name} ({len(rows)} rows)")


# 1. DEPARTMENTS
departments = [
    {"department_id": f"DEP{i:03}", "department_name": name}
    for i, name in enumerate([
        "Cardiology", "Neurology", "Emergency",
        "ICU", "Pediatrics", "Radiology",
        "Laboratory", "General Medicine"
    ], start=1)
]

# 2. DOCTORS
doctors = [
    {
        "doctor_id": f"DOC{i:03}",
        "doctor_name": fake.name(),
        "department_id": random.choice(departments)["department_id"],
        "specialization": random.choice([
            "Cardiology", "Neurology", "General Medicine",
            "Pediatrics", "Emergency Medicine"
        ])
    }
    for i in range(1, 16)
]

# 3. NURSES
nurses = [
    {
        "nurse_id": f"NUR{i:03}",
        "nurse_name": fake.name(),
        "department_id": random.choice(departments)["department_id"],
        "shift": random.choice(["Morning", "Evening", "Night"])
    }
    for i in range(1, 21)
]

# 4. PATIENT MASTER
patients = [
    {
        "patient_id": f"PAT{i:04}",
        "patient_name": fake.name(),
        "age": random.randint(1, 90),
        "gender": random.choice(["Male", "Female", "Other"]),
        "blood_group": random.choice([
            "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"
        ]),
        "city": fake.city()
    }
    for i in range(1, 101)
]

patient_ids = [p["patient_id"] for p in patients]
doctor_ids = [d["doctor_id"] for d in doctors]
department_ids = [d["department_id"] for d in departments]

# 5. APPOINTMENTS
appointments = [
    {
        "appointment_id": f"APT{i:04}",
        "patient_id": random.choice(patient_ids),
        "doctor_id": random.choice(doctor_ids),
        "appointment_date": random_date(30),
        "status": random.choice([
            "Scheduled", "Completed", "Cancelled", "Pending"
        ])
    }
    for i in range(1, 121)
]

# 6. ADMISSIONS
admissions = [
    {
        "admission_id": f"ADM{i:04}",
        "patient_id": random.choice(patient_ids),
        "department_id": random.choice(department_ids),
        "admission_date": random_date(120),
        "admission_type": random.choice([
            "Emergency", "Planned", "Referral"
        ])
    }
    for i in range(1, 61)
]

# 7. DISCHARGES
discharges = [
    {
        "discharge_id": f"DIS{i:04}",
        "patient_id": random.choice(patient_ids),
        "discharge_date": random_date(90),
        "discharge_status": random.choice([
            "Completed", "Pending Review"
        ]),
        "checklist_status": random.choice([
            "Complete", "Incomplete"
        ])
    }
    for i in range(1, 36)
]

# 8. LABORATORY RESULTS
lab_results = [
    {
        "lab_id": f"LAB{i:04}",
        "patient_id": random.choice(patient_ids),
        "test_name": random.choice([
            "CBC", "Lipid Profile", "Blood Glucose",
            "Liver Function Test", "Kidney Function Test"
        ]),
        "result_status": random.choice([
            "Pending", "Completed", "Under Review"
        ]),
        "test_date": random_date(30)
    }
    for i in range(1, 101)
]

# 9. PHARMACY INVENTORY
pharmacy = [
    {
        "item_id": f"MED{i:04}",
        "item_name": f"Sample Medical Item {i}",
        "category": random.choice([
            "Tablet", "Syrup", "Injection", "Medical Supply"
        ]),
        "quantity": random.randint(0, 500),
        "reorder_level": 50
    }
    for i in range(1, 41)
]

# 10. PRESCRIPTIONS
prescriptions = [
    {
        "prescription_id": f"PRE{i:04}",
        "patient_id": random.choice(patient_ids),
        "doctor_id": random.choice(doctor_ids),
        "item_id": random.choice(pharmacy)["item_id"],
        "status": random.choice([
            "Issued", "Pending", "Dispensed"
        ])
    }
    for i in range(1, 81)
]

# 11. BILLING
billing = [
    {
        "bill_id": f"BIL{i:04}",
        "patient_id": random.choice(patient_ids),
        "amount": round(random.uniform(500, 50000), 2),
        "payment_status": random.choice([
            "Paid", "Pending", "Partially Paid"
        ]),
        "bill_date": random_date(90)
    }
    for i in range(1, 101)
]

# 12. INSURANCE
insurance = [
    {
        "insurance_id": f"INS{i:04}",
        "patient_id": random.choice(patient_ids),
        "provider": random.choice([
            "Sample Health Cover A",
            "Sample Health Cover B",
            "Sample Health Cover C"
        ]),
        "policy_status": random.choice([
            "Active", "Expired", "Under Review"
        ])
    }
    for i in range(1, 101)
]

# 13. BED MANAGEMENT
beds = [
    {
        "bed_id": f"BED{i:03}",
        "department_id": random.choice(department_ids),
        "bed_type": random.choice(["General", "ICU", "Private"]),
        "status": random.choice([
            "Available", "Occupied", "Maintenance"
        ])
    }
    for i in range(1, 51)
]

# 14. OPERATION THEATRE SCHEDULE
ot_schedule = [
    {
        "ot_id": f"OT{i:03}",
        "patient_id": random.choice(patient_ids),
        "doctor_id": random.choice(doctor_ids),
        "procedure_category": random.choice([
            "Cardiac", "Orthopedic", "General Surgery"
        ]),
        "schedule_date": random_date(30),
        "status": random.choice([
            "Scheduled", "Completed", "Postponed"
        ])
    }
    for i in range(1, 31)
]

# 15. INCIDENT REPORTS
incidents = [
    {
        "incident_id": f"INC{i:04}",
        "department_id": random.choice(department_ids),
        "incident_type": random.choice([
            "Equipment Issue", "Documentation Issue",
            "Patient Safety Review", "Infection Control Review"
        ]),
        "severity": random.choice(["Low", "Medium", "High"]),
        "incident_date": random_date(180),
        "status": random.choice([
            "Open", "Under Investigation", "Closed"
        ])
    }
    for i in range(1, 26)
]

# SAVE ALL STRUCTURED DATASETS
datasets = {
    "departments.csv": departments,
    "doctors.csv": doctors,
    "nurses.csv": nurses,
    "patients.csv": patients,
    "appointments.csv": appointments,
    "admissions.csv": admissions,
    "discharges.csv": discharges,
    "lab_results.csv": lab_results,
    "pharmacy_inventory.csv": pharmacy,
    "prescriptions.csv": prescriptions,
    "billing.csv": billing,
    "insurance.csv": insurance,
    "bed_management.csv": beds,
    "ot_schedule.csv": ot_schedule,
    "incident_reports.csv": incidents
}

for filename, rows in datasets.items():
    save_csv(filename, rows)

print("\nAll 15 synthetic hospital datasets created!")
