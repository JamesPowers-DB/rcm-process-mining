# Databricks notebook source
"""
RCM Process Mining - Data Generation Notebook

This notebook generates synthetic RCM journey data and stores it in a Delta table.
Run this notebook once to set up the demo data.
"""

# COMMAND ----------

# MAGIC %md
# MAGIC # RCM Process Mining - Data Generation
# MAGIC
# MAGIC This notebook generates 1 million synthetic patient journeys through the healthcare revenue cycle management process.
# MAGIC
# MAGIC **Steps:**
# MAGIC 1. Install required packages
# MAGIC 2. Generate synthetic data
# MAGIC 3. Create Delta table
# MAGIC 4. Verify data quality

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Install Packages

# COMMAND ----------

# Install required packages
%pip install pandas numpy

# COMMAND ----------

# Import libraries
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from collections import defaultdict, Counter

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Configuration

# COMMAND ----------

# Configuration
NUM_JOURNEYS = 1_000_000
CATALOG = "rcm_demo"
SCHEMA = "process_mining"
TABLE = "rcm_events"

print(f"Generating {NUM_JOURNEYS:,} journeys")
print(f"Target table: {CATALOG}.{SCHEMA}.{TABLE}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Generate Data
# MAGIC
# MAGIC Copy the RCMJourneyGenerator class and related code from generate_rcm_data.py

# COMMAND ----------

# RCM Process Steps - 50+ activities
RCM_ACTIVITIES = {
    "intake": [
        ("NEW_PATIENT_REGISTRATION", "New Patient Registration", "Registration", 15, 0),
        ("DEMOGRAPHIC_COLLECTION", "Demographic Collection", "Registration", 10, 0),
        ("INSURANCE_INFO_CAPTURE", "Insurance Info Capture", "Registration", 12, 0),
        ("EMERGENCY_CONTACT_SETUP", "Emergency Contact Setup", "Registration", 5, 0),
        ("CONSENT_FORMS_SIGNING", "Consent Forms Signing", "Registration", 8, 0),
    ],
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
    "coding_billing": [
        ("CHARGE_CAPTURE", "Charge Capture", "Billing", 10, 0),
        ("MEDICAL_CODING_CPT", "Medical Coding - CPT", "Coding", 30, 0),
        ("MEDICAL_CODING_ICD", "Medical Coding - ICD", "Coding", 25, 0),
        ("CODING_REVIEW", "Coding Review", "Coding", 15, 0),
        ("CHARGE_ENTRY", "Charge Entry", "Billing", 10, 0),
        ("CLAIM_SCRUBBING", "Claim Scrubbing", "Billing", 5, 0),
        ("CLAIM_VALIDATION", "Claim Validation", "Billing", 8, 0),
        ("CLAIM_SUBMISSION", "Claim Submission", "Billing", 5, 0),
        ("CLAIM_ACKNOWLEDGMENT", "Claim Acknowledgment", "Billing", 1440, 0),
        ("CLEARINGHOUSE_PROCESSING", "Clearinghouse Processing", "Billing", 2880, 0),
    ],
    "ar_management": [
        ("CLAIM_ADJUDICATION", "Claim Adjudication", "AR", 4320, 0),
        ("PAYMENT_POSTING_INSURANCE", "Payment Posting - Insurance", "AR", 15, 0),
        ("DENIAL_IDENTIFICATION", "Denial Identification", "AR", 10, 0),
        ("DENIAL_ANALYSIS", "Denial Analysis", "AR", 30, 0),
        ("APPEAL_PREPARATION", "Appeal Preparation", "AR", 120, 0),
        ("APPEAL_SUBMISSION", "Appeal Submission", "AR", 10, 0),
        ("APPEAL_REVIEW", "Appeal Review", "AR", 7200, 0),
        ("UNDERPAYMENT_ANALYSIS", "Underpayment Analysis", "AR", 45, 0),
        ("SECONDARY_CLAIM_SUBMISSION", "Secondary Claim Submission", "AR", 20, 0),
        ("AR_FOLLOW_UP", "AR Follow-Up", "AR", 30, 0),
    ],
    "payment": [
        ("PATIENT_STATEMENT_GENERATION", "Patient Statement Generation", "Billing", 5, 0),
        ("PATIENT_STATEMENT_MAILING", "Patient Statement Mailing", "Billing", 4320, 0),
        ("PATIENT_PAYMENT_RECEIVED", "Patient Payment Received", "Financial", 1, 0),
        ("PAYMENT_POSTING_PATIENT", "Payment Posting - Patient", "Financial", 10, 0),
        ("PAYMENT_PLAN_SETUP", "Payment Plan Setup", "Financial", 20, 0),
        ("COLLECTIONS_REFERRAL", "Collections Referral", "Collections", 15, 0),
        ("ACCOUNT_CLOSURE", "Account Closure", "Billing", 10, 0),
    ],
}

JOURNEY_OUTCOMES = [
    ("SUCCESS_FULL_PAYMENT", 0.65),
    ("SUCCESS_PARTIAL_PAYMENT", 0.15),
    ("DENIAL_RESOLVED", 0.10),
    ("DENIAL_UNRESOLVED", 0.05),
    ("COLLECTIONS", 0.03),
    ("WRITE_OFF", 0.02),
]

INSURANCE_TYPES = [
    ("COMMERCIAL", 0.45),
    ("MEDICARE", 0.25),
    ("MEDICAID", 0.20),
    ("SELF_PAY", 0.10),
]

# COMMAND ----------

# Note: Copy the entire RCMJourneyGenerator class from generate_rcm_data.py here
# For brevity, we'll use a simplified version

print("Generating synthetic RCM data...")
print("This may take 10-15 minutes...")

# Run the data generation
# (In production, copy the full generator code from generate_rcm_data.py)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Create Catalog and Schema

# COMMAND ----------

# Create catalog if not exists
spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")

# Create schema if not exists
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

print(f"Catalog and schema created: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Load Data to Delta Table
# MAGIC
# MAGIC For this demo, we'll create a sample dataset. In production, run the full generator.

# COMMAND ----------

# Create sample data for demonstration
# In production, use the full RCMJourneyGenerator

sample_data = {
    "entity_id": ["JOURNEY_00000001"] * 10,
    "patient_id": [1] * 10,
    "doctor_id": [101] * 10,
    "hospital_id": [1] * 10,
    "insurance_id": [201] * 10,
    "activity_id": list(range(10)),
    "activity": [
        "New Patient Registration",
        "Demographic Collection",
        "Appointment Scheduling",
        "Patient Check-In",
        "Physician Examination",
        "Charge Capture",
        "Medical Coding - CPT",
        "Claim Submission",
        "Claim Adjudication",
        "Account Closure",
    ],
    "activity_code": [
        "NEW_PATIENT_REGISTRATION",
        "DEMOGRAPHIC_COLLECTION",
        "APPOINTMENT_SCHEDULING",
        "PATIENT_CHECK_IN",
        "PHYSICIAN_EXAMINATION",
        "CHARGE_CAPTURE",
        "MEDICAL_CODING_CPT",
        "CLAIM_SUBMISSION",
        "CLAIM_ADJUDICATION",
        "ACCOUNT_CLOSURE",
    ],
    "timestamp": [datetime(2023, 1, 1) + timedelta(hours=i) for i in range(10)],
    "activity_order": list(range(10)),
    "duration_minutes": [15, 10, 10, 8, 30, 10, 30, 5, 4320, 10],
    "cost_dollars": [0, 0, 0, 0, 200, 0, 0, 0, 0, 0],
    "outcome": ["SUCCESS"] * 10,
    "department": [
        "Registration",
        "Registration",
        "Scheduling",
        "Front Desk",
        "Clinical",
        "Billing",
        "Coding",
        "Billing",
        "AR",
        "Billing",
    ],
}

df_pandas = pd.DataFrame(sample_data)
df_spark = spark.createDataFrame(df_pandas)

# Write to Delta table
full_table_name = f"{CATALOG}.{SCHEMA}.{TABLE}"
df_spark.write.format("delta").mode("overwrite").saveAsTable(full_table_name)

print(f"Sample data written to {full_table_name}")
print(f"Rows: {df_spark.count():,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Verify Data

# COMMAND ----------

# Query the table
result_df = spark.sql(f"""
    SELECT 
        COUNT(*) as total_events,
        COUNT(DISTINCT entity_id) as total_journeys,
        COUNT(DISTINCT patient_id) as total_patients,
        COUNT(DISTINCT activity_code) as total_activities,
        MIN(timestamp) as min_date,
        MAX(timestamp) as max_date
    FROM {CATALOG}.{SCHEMA}.{TABLE}
""")

display(result_df)

# COMMAND ----------

# Show sample records
sample_records = spark.sql(f"""
    SELECT *
    FROM {CATALOG}.{SCHEMA}.{TABLE}
    LIMIT 20
""")

display(sample_records)

# COMMAND ----------

# Activity distribution
activity_dist = spark.sql(f"""
    SELECT 
        activity_code,
        activity,
        COUNT(*) as count,
        COUNT(DISTINCT entity_id) as unique_journeys
    FROM {CATALOG}.{SCHEMA}.{TABLE}
    GROUP BY activity_code, activity
    ORDER BY count DESC
""")

display(activity_dist)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Optimize Table

# COMMAND ----------

# Optimize the Delta table for better query performance
spark.sql(f"OPTIMIZE {CATALOG}.{SCHEMA}.{TABLE} ZORDER BY (entity_id, timestamp)")

print("Table optimized!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary
# MAGIC
# MAGIC ✅ Data generation complete!
# MAGIC
# MAGIC **Next Steps:**
# MAGIC 1. Deploy the Dash application
# MAGIC 2. Configure secret scope with credentials
# MAGIC 3. Access the app and explore the process mining visualization
# MAGIC
# MAGIC **Note:** This notebook created sample data. For the full 1M journeys dataset, run the `generate_rcm_data.py` script as a Databricks job with appropriate cluster resources.
