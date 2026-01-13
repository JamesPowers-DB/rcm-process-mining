"""
Activity Glossary

Comprehensive definitions of all RCM process activities.
"""

ACTIVITY_GLOSSARY = {
    "intake": [
        {
            "code": "NEW_PATIENT_REGISTRATION",
            "name": "New Patient Registration",
            "description": "Initial registration of a new patient into the healthcare system. Captures basic identifying information and creates the patient record in the system.",
            "department": "Registration",
            "typical_duration": "10-20 minutes",
        },
        {
            "code": "DEMOGRAPHIC_COLLECTION",
            "name": "Demographic Collection",
            "description": "Collection of detailed demographic information including address, contact information, emergency contacts, preferred language, and other relevant patient details.",
            "department": "Registration",
            "typical_duration": "8-12 minutes",
        },
        {
            "code": "INSURANCE_INFO_CAPTURE",
            "name": "Insurance Information Capture",
            "description": "Recording of patient insurance details including primary and secondary insurance, policy numbers, group numbers, and subscriber information.",
            "department": "Registration",
            "typical_duration": "10-15 minutes",
        },
        {
            "code": "EMERGENCY_CONTACT_SETUP",
            "name": "Emergency Contact Setup",
            "description": "Documentation of emergency contact persons, their relationship to the patient, and multiple contact methods.",
            "department": "Registration",
            "typical_duration": "3-7 minutes",
        },
        {
            "code": "CONSENT_FORMS_SIGNING",
            "name": "Consent Forms Signing",
            "description": "Patient review and signature of required consent forms including HIPAA authorization, treatment consent, and financial responsibility agreements.",
            "department": "Registration",
            "typical_duration": "5-10 minutes",
        },
    ],
    "pre_service": [
        {
            "code": "APPOINTMENT_SCHEDULING",
            "name": "Appointment Scheduling",
            "description": "Scheduling of patient appointments based on provider availability, patient preference, and clinical urgency. Includes coordination with multiple departments if needed.",
            "department": "Scheduling",
            "typical_duration": "8-12 minutes",
        },
        {
            "code": "INSURANCE_VERIFICATION",
            "name": "Insurance Verification",
            "description": "Verification of active insurance coverage, policy status, and benefits with the insurance carrier. Confirms patient eligibility for services.",
            "department": "Verification",
            "typical_duration": "15-25 minutes",
        },
        {
            "code": "ELIGIBILITY_CHECK",
            "name": "Eligibility Check",
            "description": "Real-time electronic check of patient eligibility for specific procedures or services under their insurance plan.",
            "department": "Verification",
            "typical_duration": "10-20 minutes",
        },
        {
            "code": "PRIOR_AUTHORIZATION_REQUEST",
            "name": "Prior Authorization Request",
            "description": "Submission of prior authorization request to insurance carrier for procedures or services that require pre-approval. Includes clinical documentation and medical necessity justification.",
            "department": "Authorization",
            "typical_duration": "45-90 minutes",
        },
        {
            "code": "PRIOR_AUTHORIZATION_APPROVAL",
            "name": "Prior Authorization Approval",
            "description": "Receipt and documentation of prior authorization approval from insurance carrier. Includes authorization number and approved service details.",
            "department": "Authorization",
            "typical_duration": "20-40 minutes",
        },
        {
            "code": "BENEFIT_INVESTIGATION",
            "name": "Benefit Investigation",
            "description": "Detailed investigation of patient benefits including deductibles, co-insurance, out-of-pocket maximums, and coverage limitations for planned services.",
            "department": "Verification",
            "typical_duration": "20-30 minutes",
        },
        {
            "code": "PATIENT_FINANCIAL_COUNSELING",
            "name": "Patient Financial Counseling",
            "description": "Discussion with patient about expected costs, patient responsibility, payment options, and financial assistance programs. Helps patients understand their financial obligations.",
            "department": "Financial",
            "typical_duration": "25-35 minutes",
        },
        {
            "code": "APPOINTMENT_REMINDER",
            "name": "Appointment Reminder",
            "description": "Automated or manual reminder sent to patient about upcoming appointment via phone, text, or email. Includes preparation instructions if needed.",
            "department": "Scheduling",
            "typical_duration": "1-3 minutes",
        },
    ],
    "service": [
        {
            "code": "PATIENT_CHECK_IN",
            "name": "Patient Check-In",
            "description": "Patient arrival confirmation and check-in process. Verification of demographic and insurance information, collection of updated forms.",
            "department": "Front Desk",
            "typical_duration": "5-10 minutes",
        },
        {
            "code": "COPAY_COLLECTION",
            "name": "Copay Collection",
            "description": "Collection of patient copayment at time of service. Includes payment processing and receipt generation.",
            "department": "Financial",
            "typical_duration": "3-7 minutes",
        },
        {
            "code": "INSURANCE_CARD_SCAN",
            "name": "Insurance Card Scan",
            "description": "Scanning and digital capture of patient insurance cards (front and back) for documentation and verification purposes.",
            "department": "Front Desk",
            "typical_duration": "2-4 minutes",
        },
        {
            "code": "CLINICAL_ENCOUNTER_START",
            "name": "Clinical Encounter Start",
            "description": "Initiation of clinical encounter in the electronic health record. Patient moved to exam room and encounter opened.",
            "department": "Clinical",
            "typical_duration": "3-7 minutes",
        },
        {
            "code": "VITAL_SIGNS_COLLECTION",
            "name": "Vital Signs Collection",
            "description": "Collection and documentation of patient vital signs including blood pressure, temperature, pulse, respiratory rate, and oxygen saturation.",
            "department": "Nursing",
            "typical_duration": "8-12 minutes",
        },
        {
            "code": "PHYSICIAN_EXAMINATION",
            "name": "Physician Examination",
            "description": "Comprehensive physician examination of patient including history taking, physical examination, assessment, and treatment planning.",
            "department": "Clinical",
            "typical_duration": "20-40 minutes",
        },
        {
            "code": "DIAGNOSTIC_TEST_ORDER",
            "name": "Diagnostic Test Order",
            "description": "Physician ordering of diagnostic tests such as lab work, imaging, or other diagnostic procedures. Includes electronic order entry and documentation.",
            "department": "Clinical",
            "typical_duration": "3-7 minutes",
        },
        {
            "code": "LAB_TEST_EXECUTION",
            "name": "Lab Test Execution",
            "description": "Performance of ordered laboratory tests including specimen collection, processing, analysis, and result documentation.",
            "department": "Laboratory",
            "typical_duration": "30-60 minutes",
        },
        {
            "code": "IMAGING_PROCEDURE",
            "name": "Imaging Procedure",
            "description": "Performance of diagnostic imaging procedures such as X-ray, CT, MRI, or ultrasound. Includes patient preparation, image acquisition, and preliminary review.",
            "department": "Radiology",
            "typical_duration": "45-90 minutes",
        },
        {
            "code": "TREATMENT_ADMINISTRATION",
            "name": "Treatment Administration",
            "description": "Administration of prescribed treatments including medications, infusions, injections, or therapeutic procedures.",
            "department": "Clinical",
            "typical_duration": "60-120 minutes",
        },
        {
            "code": "CLINICAL_DOCUMENTATION",
            "name": "Clinical Documentation",
            "description": "Comprehensive documentation of clinical encounter including history, examination findings, assessment, plan, and orders in the electronic health record.",
            "department": "Clinical",
            "typical_duration": "15-25 minutes",
        },
        {
            "code": "PATIENT_DISCHARGE",
            "name": "Patient Discharge",
            "description": "Patient discharge process including discharge instructions, prescription provision, follow-up appointment scheduling, and discharge documentation.",
            "department": "Clinical",
            "typical_duration": "10-20 minutes",
        },
    ],
    "coding_billing": [
        {
            "code": "CHARGE_CAPTURE",
            "name": "Charge Capture",
            "description": "Identification and capture of all billable services, procedures, and supplies provided during the patient encounter.",
            "department": "Billing",
            "typical_duration": "8-12 minutes",
        },
        {
            "code": "MEDICAL_CODING_CPT",
            "name": "Medical Coding - CPT",
            "description": "Assignment of Current Procedural Terminology (CPT) codes to procedures and services performed. Requires review of clinical documentation.",
            "department": "Coding",
            "typical_duration": "20-40 minutes",
        },
        {
            "code": "MEDICAL_CODING_ICD",
            "name": "Medical Coding - ICD",
            "description": "Assignment of International Classification of Diseases (ICD) diagnosis codes based on clinical documentation. Ensures proper code specificity and sequencing.",
            "department": "Coding",
            "typical_duration": "20-35 minutes",
        },
        {
            "code": "CODING_REVIEW",
            "name": "Coding Review",
            "description": "Quality review of assigned codes for accuracy, completeness, and compliance with coding guidelines. May include queries to providers for clarification.",
            "department": "Coding",
            "typical_duration": "12-18 minutes",
        },
        {
            "code": "CHARGE_ENTRY",
            "name": "Charge Entry",
            "description": "Entry of charges into the billing system including codes, units, modifiers, and associated charges. Links charges to the appropriate encounter.",
            "department": "Billing",
            "typical_duration": "8-12 minutes",
        },
        {
            "code": "CLAIM_SCRUBBING",
            "name": "Claim Scrubbing",
            "description": "Automated and manual review of claims for errors, missing information, or potential rejections before submission. Identifies and corrects issues.",
            "department": "Billing",
            "typical_duration": "3-7 minutes",
        },
        {
            "code": "CLAIM_VALIDATION",
            "name": "Claim Validation",
            "description": "Final validation of claim completeness and accuracy including verification of patient demographics, insurance information, and coding.",
            "department": "Billing",
            "typical_duration": "5-10 minutes",
        },
        {
            "code": "CLAIM_SUBMISSION",
            "name": "Claim Submission",
            "description": "Electronic submission of claims to insurance carriers or clearinghouses. Includes generation of submission files and transmission.",
            "department": "Billing",
            "typical_duration": "3-7 minutes",
        },
        {
            "code": "CLAIM_ACKNOWLEDGMENT",
            "name": "Claim Acknowledgment",
            "description": "Receipt and processing of claim acknowledgment from clearinghouse or payer confirming claim receipt. Typically received within 24 hours.",
            "department": "Billing",
            "typical_duration": "1 day",
        },
        {
            "code": "CLEARINGHOUSE_PROCESSING",
            "name": "Clearinghouse Processing",
            "description": "Processing of claim by clearinghouse including additional validation and routing to appropriate insurance carrier.",
            "department": "Billing",
            "typical_duration": "1-3 days",
        },
    ],
    "ar_management": [
        {
            "code": "CLAIM_ADJUDICATION",
            "name": "Claim Adjudication",
            "description": "Insurance carrier review and processing of claim to determine payment amount. Includes verification of coverage, benefits, and medical necessity.",
            "department": "AR",
            "typical_duration": "2-5 days",
        },
        {
            "code": "PAYMENT_POSTING_INSURANCE",
            "name": "Payment Posting - Insurance",
            "description": "Posting of insurance payments and adjustments to patient accounts. Includes reconciliation of payment with explanation of benefits (EOB).",
            "department": "AR",
            "typical_duration": "10-20 minutes",
        },
        {
            "code": "DENIAL_IDENTIFICATION",
            "name": "Denial Identification",
            "description": "Identification and categorization of claim denials. Includes review of denial reasons and determination of appeal potential.",
            "department": "AR",
            "typical_duration": "8-12 minutes",
        },
        {
            "code": "DENIAL_ANALYSIS",
            "name": "Denial Analysis",
            "description": "Detailed analysis of denial reason, review of supporting documentation, and determination of appropriate corrective action or appeal strategy.",
            "department": "AR",
            "typical_duration": "25-35 minutes",
        },
        {
            "code": "APPEAL_PREPARATION",
            "name": "Appeal Preparation",
            "description": "Preparation of appeal documentation including clinical records, medical necessity justification, and appeal letter. May require provider input.",
            "department": "AR",
            "typical_duration": "90-150 minutes",
        },
        {
            "code": "APPEAL_SUBMISSION",
            "name": "Appeal Submission",
            "description": "Submission of appeal to insurance carrier with all supporting documentation. Includes tracking of submission and follow-up timeline.",
            "department": "AR",
            "typical_duration": "8-12 minutes",
        },
        {
            "code": "APPEAL_REVIEW",
            "name": "Appeal Review",
            "description": "Insurance carrier review of appeal submission. Typically takes 30-60 days depending on carrier and appeal level.",
            "department": "AR",
            "typical_duration": "30-60 days",
        },
        {
            "code": "UNDERPAYMENT_ANALYSIS",
            "name": "Underpayment Analysis",
            "description": "Analysis of insurance payments to identify underpayments or incorrect contractual adjustments. Includes contract verification.",
            "department": "AR",
            "typical_duration": "35-50 minutes",
        },
        {
            "code": "SECONDARY_CLAIM_SUBMISSION",
            "name": "Secondary Claim Submission",
            "description": "Submission of claim to secondary insurance after primary insurance payment. Includes coordination of benefits information.",
            "department": "AR",
            "typical_duration": "15-25 minutes",
        },
        {
            "code": "AR_FOLLOW_UP",
            "name": "AR Follow-Up",
            "description": "Follow-up on outstanding claims with insurance carriers. Includes status inquiries, missing information requests, and payment tracking.",
            "department": "AR",
            "typical_duration": "25-35 minutes",
        },
    ],
    "payment": [
        {
            "code": "PATIENT_STATEMENT_GENERATION",
            "name": "Patient Statement Generation",
            "description": "Generation of patient billing statements showing charges, insurance payments, adjustments, and patient balance due.",
            "department": "Billing",
            "typical_duration": "3-7 minutes",
        },
        {
            "code": "PATIENT_STATEMENT_MAILING",
            "name": "Patient Statement Mailing",
            "description": "Printing and mailing of patient statements. Includes processing time and mail delivery time.",
            "department": "Billing",
            "typical_duration": "3-5 days",
        },
        {
            "code": "PATIENT_PAYMENT_RECEIVED",
            "name": "Patient Payment Received",
            "description": "Receipt of patient payment via mail, online portal, phone, or in-person. Includes payment processing and documentation.",
            "department": "Financial",
            "typical_duration": "1-2 minutes",
        },
        {
            "code": "PAYMENT_POSTING_PATIENT",
            "name": "Payment Posting - Patient",
            "description": "Posting of patient payments to accounts. Includes allocation of payments to appropriate charges and balance reconciliation.",
            "department": "Financial",
            "typical_duration": "8-12 minutes",
        },
        {
            "code": "PAYMENT_PLAN_SETUP",
            "name": "Payment Plan Setup",
            "description": "Establishment of payment plan for patients unable to pay balance in full. Includes financial assessment and agreement documentation.",
            "department": "Financial",
            "typical_duration": "15-25 minutes",
        },
        {
            "code": "COLLECTIONS_REFERRAL",
            "name": "Collections Referral",
            "description": "Referral of delinquent accounts to collections agency after exhausting internal collection efforts. Includes account documentation and transfer.",
            "department": "Collections",
            "typical_duration": "12-18 minutes",
        },
        {
            "code": "ACCOUNT_CLOSURE",
            "name": "Account Closure",
            "description": "Final closure of patient account after full payment or write-off. Includes final reconciliation and documentation.",
            "department": "Billing",
            "typical_duration": "8-12 minutes",
        },
    ],
}


def get_activity_by_code(activity_code: str) -> dict:
    """
    Get activity details by activity code.

    Args:
        activity_code: Activity code to lookup

    Returns:
        Dictionary with activity details or None if not found
    """
    for phase, activities in ACTIVITY_GLOSSARY.items():
        for activity in activities:
            if activity["code"] == activity_code:
                return {**activity, "phase": phase}
    return None


def get_all_activities() -> list:
    """
    Get all activities as a flat list.

    Returns:
        List of all activity dictionaries
    """
    all_activities = []
    for phase, activities in ACTIVITY_GLOSSARY.items():
        for activity in activities:
            all_activities.append({**activity, "phase": phase})
    return all_activities


def get_activities_by_phase(phase: str) -> list:
    """
    Get all activities for a specific phase.

    Args:
        phase: Phase name (intake, pre_service, service, coding_billing, ar_management, payment)

    Returns:
        List of activity dictionaries for the phase
    """
    return ACTIVITY_GLOSSARY.get(phase, [])
