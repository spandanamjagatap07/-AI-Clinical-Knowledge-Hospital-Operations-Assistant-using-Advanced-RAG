
from pathlib import Path

DOC_DIR = Path(__file__).resolve().parent / "documents"
DOC_DIR.mkdir(parents=True, exist_ok=True)

documents = {
    "clinical_guidelines.txt": """
TITLE: Clinical Practice Guidelines
DEPARTMENT: General Medicine
DOCUMENT_TYPE: Guideline
VERSION: 1.0

PURPOSE:
This is a synthetic demonstration document for the hospital AI project.

SCOPE:
Clinical practice guidelines must be approved by the hospital's
authorized clinical governance committee before use.

WORKFLOW:
1. Staff identify the applicable approved guideline.
2. Staff verify its version and effective date.
3. Staff consult the responsible clinical team.
4. Any uncertainty is escalated through the approved clinical process.

IMPORTANT:
This sample does not contain clinical treatment instructions.
""",

    "hospital_sop.txt": """
TITLE: Hospital Standard Operating Procedure
DEPARTMENT: Administration
DOCUMENT_TYPE: SOP
VERSION: 1.0

PURPOSE:
Define a consistent process for hospital administrative operations.

WORKFLOW:
1. Receive the relevant request.
2. Verify the request details.
3. Route the request to the responsible department.
4. Record the action taken.
5. Escalate unresolved requests to the department supervisor.

DOCUMENTATION:
All actions must be recorded in the approved hospital system.
""",

    "nursing_protocol.txt": """
TITLE: Nursing Documentation Protocol
DEPARTMENT: Nursing
DOCUMENT_TYPE: Protocol
VERSION: 1.0

PURPOSE:
Describe administrative documentation responsibilities for nursing staff.

WORKFLOW:
1. Verify the patient's authorized hospital record.
2. Record observations in the approved system.
3. Document relevant handover information.
4. Escalate missing or inconsistent records.
5. Follow the hospital's approved clinical protocols.

NOTE:
This is a synthetic training document, not clinical guidance.
""",

    "laboratory_manual.txt": """
TITLE: Laboratory Operations Manual
DEPARTMENT: Laboratory
DOCUMENT_TYPE: Manual
VERSION: 1.0

PURPOSE:
Describe the laboratory's administrative workflow.

WORKFLOW:
1. Register the laboratory request.
2. Verify sample identification according to approved policy.
3. Record sample receipt.
4. Track processing status.
5. Record result verification and release status.
6. Escalate delayed or rejected samples.

RECORDS:
Maintain an auditable laboratory activity record.
""",

    "radiology_procedures.txt": """
TITLE: Radiology Operations Procedure
DEPARTMENT: Radiology
DOCUMENT_TYPE: Procedure
VERSION: 1.0

WORKFLOW:
1. Receive an imaging request.
2. Verify the request and appointment details.
3. Coordinate the imaging schedule.
4. Record procedure completion.
5. Track report verification and availability.
6. Escalate scheduling or equipment issues.
""",

    "pharmacy_guidelines.txt": """
TITLE: Pharmacy Inventory Management Guideline
DEPARTMENT: Pharmacy
DOCUMENT_TYPE: Guideline
VERSION: 1.0

WORKFLOW:
1. Record incoming inventory.
2. Update available stock.
3. Monitor expiry information.
4. Identify items below reorder levels.
5. Record dispensing transactions.
6. Escalate inventory discrepancies.

NOTE:
No medication dosage or prescribing advice is provided.
""",

    "infection_control.txt": """
TITLE: Infection Control Reporting Manual
DEPARTMENT: Infection Control
DOCUMENT_TYPE: Manual
VERSION: 1.0

PURPOSE:
Define the administrative reporting and review workflow.

WORKFLOW:
1. Register an infection-control incident.
2. Notify the responsible infection-control team.
3. Record investigation status.
4. Document corrective actions.
5. Track closure and review dates.

Clinical prevention and treatment instructions must come
from approved hospital policies.
""",

    "emergency_response.txt": """
TITLE: Emergency Response Administrative Protocol
DEPARTMENT: Emergency
DOCUMENT_TYPE: Protocol
VERSION: 1.0

WORKFLOW:
1. Register the emergency event.
2. Notify the designated response team.
3. Record event timestamps.
4. Maintain communication records.
5. Document event closure.
6. Complete the required incident report.

For actual emergencies, follow approved emergency procedures.
""",

    "patient_care_policy.txt": """
TITLE: Patient Care Documentation Policy
DEPARTMENT: Patient Care
DOCUMENT_TYPE: Policy
VERSION: 1.0

POLICY:
Patient care documentation must be accurate, timely and traceable.

REQUIREMENTS:
1. Use authorized patient records.
2. Record relevant activities.
3. Maintain confidentiality.
4. Correct documentation errors using approved procedures.
5. Escalate discrepancies to the responsible team.
""",

    "accreditation_documents.txt": """
TITLE: Hospital Accreditation Documentation
DEPARTMENT: Quality
DOCUMENT_TYPE: Accreditation
VERSION: 1.0

PURPOSE:
Maintain evidence required for hospital quality reviews.

REQUIREMENTS:
1. Maintain current approved policies.
2. Record staff training evidence.
3. Maintain audit documentation.
4. Track corrective action plans.
5. Record review and approval dates.
""",

    "medical_equipment_manual.txt": """
TITLE: Medical Equipment Administration Manual
DEPARTMENT: Biomedical Engineering
DOCUMENT_TYPE: Manual
VERSION: 1.0

WORKFLOW:
1. Register medical equipment.
2. Record equipment identification.
3. Track maintenance schedules.
4. Document service requests.
5. Record equipment downtime.
6. Escalate safety and maintenance issues.
""",

    "quality_audit_report.txt": """
TITLE: Synthetic Hospital Quality Audit Report
DEPARTMENT: Quality
DOCUMENT_TYPE: Audit Report
VERSION: 1.0

AUDIT AREAS:
1. Documentation completeness.
2. Policy version management.
3. Staff training records.
4. Incident reporting.
5. Corrective action tracking.

FINDINGS:
This sample report is intended for testing document
retrieval and summarization.

RECOMMENDATION:
Record audit findings and assign corrective actions
to the responsible department.
""",

    "incident_investigation.txt": """
TITLE: Incident Investigation Procedure
DEPARTMENT: Quality
DOCUMENT_TYPE: Investigation Report
VERSION: 1.0

WORKFLOW:
1. Register the incident.
2. Assign an investigation owner.
3. Collect relevant records.
4. Document findings.
5. Assign corrective actions.
6. Track completion.
7. Record final review and closure.
""",

    "clinical_pathways.txt": """
TITLE: Clinical Pathway Governance Document
DEPARTMENT: Clinical Governance
DOCUMENT_TYPE: Clinical Pathway
VERSION: 1.0

PURPOSE:
Describe the governance process for clinical pathways.

WORKFLOW:
1. Identify the pathway and its intended scope.
2. Obtain review from the responsible specialists.
3. Obtain required clinical governance approval.
4. Publish the approved version.
5. Review and update according to hospital policy.

IMPORTANT:
This is a synthetic governance example, not a
patient-specific clinical pathway.
"""
}

for filename, content in documents.items():
    filepath = DOC_DIR / filename
    filepath.write_text(content.strip(), encoding="utf-8")
    print("Created:", filename)

print("\nAll 14 synthetic hospital documents created!")
