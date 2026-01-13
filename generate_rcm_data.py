"""
RCM Process Mining - Synthetic Data Generator

Generates 1M+ patient journeys through healthcare revenue cycle management process.
Creates a Delta table with realistic RCM activity sequences.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from databricks.sdk import WorkspaceClient
import numpy as np
from pyspark.sql import DataFrame

# RCM Process Steps - 50+ activities across the complete lifecycle
RCM_ACTIVITIES = {
    # INTAKE PHASE (5 steps)
    "intake": [
        ("NEW_PATIENT_REGISTRATION", "New Patient Registration", "Registration", 15, 0),
        ("DEMOGRAPHIC_COLLECTION", "Demographic Collection", "Registration", 10, 0),
        ("INSURANCE_INFO_CAPTURE", "Insurance Info Capture", "Registration", 12, 0),
        ("EMERGENCY_CONTACT_SETUP", "Emergency Contact Setup", "Registration", 5, 0),
        ("CONSENT_FORMS_SIGNING", "Consent Forms Signing", "Registration", 8, 0),
    ],
    # PRE-SERVICE PHASE (8 steps)
    "pre_service": [
        ("APPOINTMENT_SCHEDULING", "Appointment Scheduling", "Scheduling", 10, 0),
        ("INSURANCE_VERIFICATION", "Insurance Verification", "Verification", 20, 0),
        ("ELIGIBILITY_CHECK", "Eligibility Check", "Verification", 15, 0),
        ("PRIOR_AUTHORIZATION_REQUEST", "Prior Authorization Request", "Authorization", 60, 0),
        ("PRIOR_AUTHORIZATION_APPROVAL", "Prior Authorization Approval", "Authorization", 30, 0),
        ("BENEFIT_INVESTIGATION", "Benefit Investigation", "Verification", 25, 0),
        ("PATIENT_FINANCIAL_COUNSELING", "Patient Financial Counseling", "Financial", 30, 0),
        ("APPOINTMENT_REMINDER", "Appointment Reminder", "Scheduling", 2, 0),
    ],
    # SERVICE PHASE (12 steps)
    "service": [
        ("PATIENT_CHECK_IN", "Patient Check-In", "Front Desk", 8, 0),
        ("COPAY_COLLECTION", "Copay Collection", "Financial", 5, 25),
        ("INSURANCE_CARD_SCAN", "Insurance Card Scan", "Front Desk", 3, 0),
        ("CLINICAL_ENCOUNTER_START", "Clinical Encounter Start", "Clinical", 5, 0),
        ("VITAL_SIGNS_COLLECTION", "Vital Signs Collection", "Nursing", 10, 0),
        ("PHYSICIAN_EXAMINATION", "Physician Examination", "Clinical", 30, 0),
        ("DIAGNOSTIC_TEST_ORDER", "Diagnostic Test Order", "Clinical", 5, 0),
        ("LAB_TEST_EXECUTION", "Lab Test Execution", "Laboratory", 45, 150),
        ("IMAGING_PROCEDURE", "Imaging Procedure", "Radiology", 60, 500),
        ("TREATMENT_ADMINISTRATION", "Treatment Administration", "Clinical", 90, 300),
        ("CLINICAL_DOCUMENTATION", "Clinical Documentation", "Clinical", 20, 0),
        ("PATIENT_DISCHARGE", "Patient Discharge", "Clinical", 15, 0),
    ],
    # CODING & BILLING PHASE (10 steps)
    "coding_billing": [
        ("CHARGE_CAPTURE", "Charge Capture", "Billing", 10, 0),
        ("MEDICAL_CODING_CPT", "Medical Coding - CPT", "Coding", 30, 0),
        ("MEDICAL_CODING_ICD", "Medical Coding - ICD", "Coding", 25, 0),
        ("CODING_REVIEW", "Coding Review", "Coding", 15, 0),
        ("CHARGE_ENTRY", "Charge Entry", "Billing", 10, 0),
        ("CLAIM_SCRUBBING", "Claim Scrubbing", "Billing", 5, 0),
        ("CLAIM_VALIDATION", "Claim Validation", "Billing", 8, 0),
        ("CLAIM_SUBMISSION", "Claim Submission", "Billing", 5, 0),
        ("CLAIM_ACKNOWLEDGMENT", "Claim Acknowledgment", "Billing", 1440, 0),  # 1 day
        ("CLEARINGHOUSE_PROCESSING", "Clearinghouse Processing", "Billing", 2880, 0),  # 2 days
    ],
    # AR MANAGEMENT PHASE (10 steps)
    "ar_management": [
        ("CLAIM_ADJUDICATION", "Claim Adjudication", "AR", 4320, 0),  # 3 days
        ("PAYMENT_POSTING_INSURANCE", "Payment Posting - Insurance", "AR", 15, 0),
        ("DENIAL_IDENTIFICATION", "Denial Identification", "AR", 10, 0),
        ("DENIAL_ANALYSIS", "Denial Analysis", "AR", 30, 0),
        ("APPEAL_PREPARATION", "Appeal Preparation", "AR", 120, 0),
        ("APPEAL_SUBMISSION", "Appeal Submission", "AR", 10, 0),
        ("APPEAL_REVIEW", "Appeal Review", "AR", 7200, 0),  # 5 days
        ("UNDERPAYMENT_ANALYSIS", "Underpayment Analysis", "AR", 45, 0),
        ("SECONDARY_CLAIM_SUBMISSION", "Secondary Claim Submission", "AR", 20, 0),
        ("AR_FOLLOW_UP", "AR Follow-Up", "AR", 30, 0),
    ],
    # PAYMENT PHASE (7 steps)
    "payment": [
        ("PATIENT_STATEMENT_GENERATION", "Patient Statement Generation", "Billing", 5, 0),
        ("PATIENT_STATEMENT_MAILING", "Patient Statement Mailing", "Billing", 4320, 0),  # 3 days
        ("PATIENT_PAYMENT_RECEIVED", "Patient Payment Received", "Financial", 1, 0),
        ("PAYMENT_POSTING_PATIENT", "Payment Posting - Patient", "Financial", 10, 0),
        ("PAYMENT_PLAN_SETUP", "Payment Plan Setup", "Financial", 20, 0),
        ("COLLECTIONS_REFERRAL", "Collections Referral", "Collections", 15, 0),
        ("ACCOUNT_CLOSURE", "Account Closure", "Billing", 10, 0),
    ],
}

# Journey outcome types with probabilities
JOURNEY_OUTCOMES = [
    ("SUCCESS_FULL_PAYMENT", 0.65),  # Happy path
    ("SUCCESS_PARTIAL_PAYMENT", 0.15),
    ("DENIAL_RESOLVED", 0.10),
    ("DENIAL_UNRESOLVED", 0.05),
    ("COLLECTIONS", 0.03),
    ("WRITE_OFF", 0.02),
]

# Insurance types with different behaviors
INSURANCE_TYPES = [
    ("COMMERCIAL", 0.45),
    ("MEDICARE", 0.25),
    ("MEDICAID", 0.20),
    ("SELF_PAY", 0.10),
]


class RCMJourneyGenerator:
    """Generates realistic RCM patient journeys with variations."""

    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        self.activity_lookup = self._build_activity_lookup()

    def _build_activity_lookup(self) -> List[Tuple[str, str, str, int, float]]:
        """Flatten all activities into a single lookup list."""
        activities = []
        for phase_activities in RCM_ACTIVITIES.values():
            activities.extend(phase_activities)
        return activities

    def _select_insurance_type(self) -> str:
        """Select insurance type based on probability distribution."""
        return random.choices(
            [ins[0] for ins in INSURANCE_TYPES],
            weights=[ins[1] for ins in INSURANCE_TYPES],
        )[0]

    def _select_journey_outcome(self) -> str:
        """Select journey outcome based on probability distribution."""
        return random.choices(
            [out[0] for out in JOURNEY_OUTCOMES],
            weights=[out[1] for out in JOURNEY_OUTCOMES],
        )[0]

    def _add_time_variance(self, base_minutes: int, variance: float = 0.3) -> int:
        """Add realistic time variance to activity duration."""
        min_time = int(base_minutes * (1 - variance))
        max_time = int(base_minutes * (1 + variance))
        return random.randint(max(1, min_time), max_time)

    def _should_skip_activity(self, activity_code: str, insurance_type: str) -> bool:
        """Determine if an activity should be skipped based on context."""
        # Self-pay patients skip some insurance steps
        if insurance_type == "SELF_PAY":
            if activity_code in [
                "INSURANCE_VERIFICATION",
                "ELIGIBILITY_CHECK",
                "PRIOR_AUTHORIZATION_REQUEST",
                "PRIOR_AUTHORIZATION_APPROVAL",
                "BENEFIT_INVESTIGATION",
            ]:
                return random.random() < 0.8  # 80% chance to skip

        # Some patients don't need imaging or complex procedures
        if activity_code in ["IMAGING_PROCEDURE", "TREATMENT_ADMINISTRATION"]:
            return random.random() < 0.4  # 40% skip rate

        # Not all claims need appeals
        if activity_code in [
            "DENIAL_ANALYSIS",
            "APPEAL_PREPARATION",
            "APPEAL_SUBMISSION",
            "APPEAL_REVIEW",
        ]:
            return random.random() < 0.85  # Only 15% need appeals

        return False

    def generate_journey(
        self, entity_id: str, patient_id: int, start_date: datetime
    ) -> List[Dict]:
        """Generate a single patient journey through RCM process."""
        events = []
        current_time = start_date
        activity_order = 0

        # Journey context
        insurance_type = self._select_insurance_type()
        outcome = self._select_journey_outcome()
        doctor_id = random.randint(1, 500)
        hospital_id = random.randint(1, 50)
        insurance_id = random.randint(1, 200) if insurance_type != "SELF_PAY" else 0

        # Determine which phases to include based on outcome
        include_denial_path = outcome in ["DENIAL_RESOLVED", "DENIAL_UNRESOLVED"]
        include_collections = outcome in ["COLLECTIONS", "WRITE_OFF"]
        include_payment_plan = outcome == "SUCCESS_PARTIAL_PAYMENT"

        # INTAKE PHASE - always required
        for activity_code, activity, department, base_duration, cost in RCM_ACTIVITIES[
            "intake"
        ]:
            duration = self._add_time_variance(base_duration)
            events.append(
                {
                    "entity_id": entity_id,
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "hospital_id": hospital_id,
                    "insurance_id": insurance_id,
                    "activity_id": activity_order,
                    "activity": activity,
                    "activity_code": activity_code,
                    "timestamp": current_time,
                    "activity_order": activity_order,
                    "duration_minutes": duration,
                    "cost_dollars": float(cost),
                    "outcome": "SUCCESS",
                    "department": department,
                }
            )
            current_time += timedelta(minutes=duration)
            activity_order += 1

        # PRE-SERVICE PHASE
        for activity_code, activity, department, base_duration, cost in RCM_ACTIVITIES[
            "pre_service"
        ]:
            if self._should_skip_activity(activity_code, insurance_type):
                continue

            duration = self._add_time_variance(base_duration)
            activity_outcome = "SUCCESS"

            # Prior auth can fail
            if activity_code == "PRIOR_AUTHORIZATION_APPROVAL" and random.random() < 0.1:
                activity_outcome = "DENIED"

            events.append(
                {
                    "entity_id": entity_id,
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "hospital_id": hospital_id,
                    "insurance_id": insurance_id,
                    "activity_id": activity_order,
                    "activity": activity,
                    "activity_code": activity_code,
                    "timestamp": current_time,
                    "activity_order": activity_order,
                    "duration_minutes": duration,
                    "cost_dollars": float(cost),
                    "outcome": activity_outcome,
                    "department": department,
                }
            )
            current_time += timedelta(minutes=duration)
            activity_order += 1

        # SERVICE PHASE - always required
        for activity_code, activity, department, base_duration, cost in RCM_ACTIVITIES[
            "service"
        ]:
            if self._should_skip_activity(activity_code, insurance_type):
                continue

            duration = self._add_time_variance(base_duration)
            activity_cost = cost * random.uniform(0.8, 1.2) if cost > 0 else 0.0

            events.append(
                {
                    "entity_id": entity_id,
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "hospital_id": hospital_id,
                    "insurance_id": insurance_id,
                    "activity_id": activity_order,
                    "activity": activity,
                    "activity_code": activity_code,
                    "timestamp": current_time,
                    "activity_order": activity_order,
                    "duration_minutes": duration,
                    "cost_dollars": round(activity_cost, 2),
                    "outcome": "SUCCESS",
                    "department": department,
                }
            )
            current_time += timedelta(minutes=duration)
            activity_order += 1

        # CODING & BILLING PHASE - always required
        for activity_code, activity, department, base_duration, cost in RCM_ACTIVITIES[
            "coding_billing"
        ]:
            duration = self._add_time_variance(base_duration)
            activity_outcome = "SUCCESS"

            # Claim scrubbing can find errors
            if activity_code == "CLAIM_SCRUBBING" and random.random() < 0.15:
                activity_outcome = "ERRORS_FOUND"

            events.append(
                {
                    "entity_id": entity_id,
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "hospital_id": hospital_id,
                    "insurance_id": insurance_id,
                    "activity_id": activity_order,
                    "activity": activity,
                    "activity_code": activity_code,
                    "timestamp": current_time,
                    "activity_order": activity_order,
                    "duration_minutes": duration,
                    "cost_dollars": float(cost),
                    "outcome": activity_outcome,
                    "department": department,
                }
            )
            current_time += timedelta(minutes=duration)
            activity_order += 1

        # AR MANAGEMENT PHASE - conditional based on outcome
        for activity_code, activity, department, base_duration, cost in RCM_ACTIVITIES[
            "ar_management"
        ]:
            # Skip denial/appeal steps if not needed
            if not include_denial_path and activity_code in [
                "DENIAL_IDENTIFICATION",
                "DENIAL_ANALYSIS",
                "APPEAL_PREPARATION",
                "APPEAL_SUBMISSION",
                "APPEAL_REVIEW",
            ]:
                continue

            if self._should_skip_activity(activity_code, insurance_type):
                continue

            duration = self._add_time_variance(base_duration)
            activity_outcome = "SUCCESS"

            # Denials
            if activity_code == "CLAIM_ADJUDICATION":
                if include_denial_path:
                    activity_outcome = "DENIED"
                else:
                    activity_outcome = "APPROVED"

            events.append(
                {
                    "entity_id": entity_id,
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "hospital_id": hospital_id,
                    "insurance_id": insurance_id,
                    "activity_id": activity_order,
                    "activity": activity,
                    "activity_code": activity_code,
                    "timestamp": current_time,
                    "activity_order": activity_order,
                    "duration_minutes": duration,
                    "cost_dollars": float(cost),
                    "outcome": activity_outcome,
                    "department": department,
                }
            )
            current_time += timedelta(minutes=duration)
            activity_order += 1

        # PAYMENT PHASE
        for activity_code, activity, department, base_duration, cost in RCM_ACTIVITIES[
            "payment"
        ]:
            # Collections only for specific outcomes
            if activity_code == "COLLECTIONS_REFERRAL" and not include_collections:
                continue

            # Payment plan only for partial payment
            if activity_code == "PAYMENT_PLAN_SETUP" and not include_payment_plan:
                continue

            duration = self._add_time_variance(base_duration)

            events.append(
                {
                    "entity_id": entity_id,
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "hospital_id": hospital_id,
                    "insurance_id": insurance_id,
                    "activity_id": activity_order,
                    "activity": activity,
                    "activity_code": activity_code,
                    "timestamp": current_time,
                    "activity_order": activity_order,
                    "duration_minutes": duration,
                    "cost_dollars": float(cost),
                    "outcome": outcome,
                    "department": department,
                }
            )
            current_time += timedelta(minutes=duration)
            activity_order += 1

        return events

    def generate_dataset(
        self, num_journeys: int = 1_000_000, batch_size: int = 10_000, 
        catalog: str = None, schema: str = None, table_name: str = None, 
        save_batches: bool = False
    ) -> DataFrame:
        """Generate complete dataset of RCM journeys. If save_batches is True, saves each batch to Delta table."""
        print(f"Generating {num_journeys:,} RCM journeys...")

        start_date = datetime(2023, 1, 1)
        df = None
        full_table_name = None

        if save_batches:
            assert catalog and schema and table_name, "catalog, schema, and table_name must be provided when save_batches=True"
            full_table_name = f"{catalog}.{schema}.{table_name}"
            # Drop table if exists to start fresh
            spark.sql(f"DROP TABLE IF EXISTS {full_table_name}")

        for i in range(0, num_journeys, batch_size):
            end = min(i + batch_size, num_journeys)
            batch_events = []
            for j in range(i, end):
                entity_id = f"JOURNEY_{j:08d}"
                patient_id = random.randint(1, num_journeys // 3)
                journey_start = start_date + timedelta(days=random.randint(0, 730))
                journey_events = self.generate_journey(entity_id, patient_id, journey_start)
                batch_events.extend(journey_events)
            batch_df = spark.createDataFrame(batch_events)
            if save_batches:
                mode = "overwrite" if i == 0 else "append"
                batch_df.write.format("delta").mode(mode).saveAsTable(full_table_name)
            else:
                if df is None:
                    df = batch_df
                else:
                    df = df.unionByName(batch_df)
            print(f"  Generated {end:,} journeys...")

        if save_batches:
            df = spark.table(full_table_name)
            print(f"Generated {df.count():,} total events (saved in Delta table)")
        else:
            print(f"Generated {df.count():,} total events")
            print(f"Generated spark dataframe with total events")
        return df
    
def main():
    """Main execution function."""
    # Configuration
    NUM_JOURNEYS = 250_000
    CATALOG = "rcm_demo"
    SCHEMA = "process_mining"
    TABLE_NAME = "rcm_events"

    # Generate data
    generator = RCMJourneyGenerator(seed=42)
    df = generator.generate_dataset(
    num_journeys=NUM_JOURNEYS,
    catalog=CATALOG,
    schema=SCHEMA,
    table_name=TABLE_NAME,
    save_batches=True
    )


if __name__ == "__main__":
    main()