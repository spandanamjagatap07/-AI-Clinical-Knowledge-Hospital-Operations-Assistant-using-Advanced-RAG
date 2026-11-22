
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# 1. Departments
class Department(Base):
    __tablename__ = "departments"

    department_id = Column(String, primary_key=True)
    department_name = Column(String)


# 2. Patients
class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String, primary_key=True)
    patient_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    blood_group = Column(String)
    city = Column(String)


# 3. Doctors
class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(String, primary_key=True)
    doctor_name = Column(String)
    department_id = Column(
        String, ForeignKey("departments.department_id")
    )
    specialization = Column(String)


# 4. Nurses
class Nurse(Base):
    __tablename__ = "nurses"

    nurse_id = Column(String, primary_key=True)
    nurse_name = Column(String)
    department_id = Column(
        String, ForeignKey("departments.department_id")
    )
    shift = Column(String)


# 5. Appointments
class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    doctor_id = Column(String, ForeignKey("doctors.doctor_id"))
    appointment_date = Column(String)
    status = Column(String)


# 6. Admissions
class Admission(Base):
    __tablename__ = "admissions"

    admission_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    department_id = Column(
        String, ForeignKey("departments.department_id")
    )
    admission_date = Column(String)
    admission_type = Column(String)


# 7. Discharges
class Discharge(Base):
    __tablename__ = "discharges"

    discharge_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    discharge_date = Column(String)
    discharge_status = Column(String)
    checklist_status = Column(String)


# 8. Lab Results
class LabResult(Base):
    __tablename__ = "lab_results"

    lab_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    test_name = Column(String)
    result_status = Column(String)
    test_date = Column(String)


# 9. Pharmacy Inventory
class PharmacyInventory(Base):
    __tablename__ = "pharmacy_inventory"

    item_id = Column(String, primary_key=True)
    item_name = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    reorder_level = Column(Integer)


# 10. Prescriptions
class Prescription(Base):
    __tablename__ = "prescriptions"

    prescription_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    doctor_id = Column(String, ForeignKey("doctors.doctor_id"))
    item_id = Column(
        String, ForeignKey("pharmacy_inventory.item_id")
    )
    status = Column(String)


# 11. Billing
class Billing(Base):
    __tablename__ = "billing"

    bill_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    amount = Column(Float)
    payment_status = Column(String)
    bill_date = Column(String)


# 12. Insurance
class Insurance(Base):
    __tablename__ = "insurance"

    insurance_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    provider = Column(String)
    policy_status = Column(String)


# 13. Bed Management
class BedManagement(Base):
    __tablename__ = "bed_management"

    bed_id = Column(String, primary_key=True)
    department_id = Column(
        String, ForeignKey("departments.department_id")
    )
    bed_type = Column(String)
    status = Column(String)


# 14. OT Schedule
class OTSchedule(Base):
    __tablename__ = "ot_schedule"

    ot_id = Column(String, primary_key=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    doctor_id = Column(String, ForeignKey("doctors.doctor_id"))
    procedure_category = Column(String)
    schedule_date = Column(String)
    status = Column(String)


# 15. Incident Reports
class IncidentReport(Base):
    __tablename__ = "incident_reports"

    incident_id = Column(String, primary_key=True)
    department_id = Column(
        String, ForeignKey("departments.department_id")
    )
    incident_type = Column(String)
    severity = Column(String)
    incident_date = Column(String)
    status = Column(String)

# 16. Users for Authentication
from sqlalchemy import Boolean, DateTime
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="nurse")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())