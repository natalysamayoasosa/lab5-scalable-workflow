
import argparse
from pathlib import Path
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

# Read the combined analysis table
df = pd.read_csv(args.input)

# Separate datasets by source
samples = df[df["source"] == "messy_samples"].copy()
patients = df[df["source"] == "cohort_database"].copy()

# Calculate descriptive statistics

# Use only measurements explicitly labeled mg/dL.
# Flag mmol/L records because their recorded magnitudes
# suggest possible unit-label errors.

glucose_values = pd.to_numeric(
    samples["glucose_value"], errors="coerce"
)

glucose_units = samples["glucose_unit"].str.strip().str.lower()

sample_glucose = glucose_values.where(glucose_units == "mg/dl")

questionable_units = (glucose_units == "mmol/l").sum()


glucose_units = samples["glucose_unit"].str.strip().str.lower()

# 1 mmol/L glucose ≈ 18.0182 mg/dL
sample_glucose.loc[glucose_units == "mmol/l"] *= 18.0182

# Exclude measurements with missing or unrecognized units
valid_units = glucose_units.isin(["mg/dl", "mmol/l"])
sample_glucose = sample_glucose.where(valid_units)

patient_age = pd.to_numeric(
    patients["age_at_diagnosis"], errors="coerce"
)

report = [
    "LAB 5: SCALABLE ANALYSIS WORKFLOW",
    "=================================",
    "",
    "1. DATASET OVERVIEW",
    f"Total records: {len(df)}",
    f"Cleaned sample records: {len(samples)}",
    f"Database patient records: {len(patients)}",
    "",
    "2. CLEANED SAMPLE SUMMARY",
    f"Average glucose (mg/dL): {sample_glucose.mean():.2f}",  
    f"Records flagged for unit review (mmol/L): {questionable_units}",
    f"Missing glucose values: {glucose_values.isna().sum()}",
    f"Glucose values included in average: {sample_glucose.notna().sum()}",
    f"Glucose values excluded due to unit uncertainty: {((glucose_units == 'mmol/l') & glucose_values.notna()).sum()}",
    "",
    "3. DATABASE PATIENT SUMMARY",
    f"Average age at diagnosis: {patient_age.mean():.2f}",
    f"Missing ages: {patient_age.isna().sum()}",
    "",
    "4. DATA INTEGRATION NOTE",
    "The two datasets have different identifier systems.",
    "Records were concatenated with a source column.",
    "No patient-level matches were assumed.",
    "Glucose averages include only records labeled mg/dL.",
    "Records labeled mmol/L were excluded pending unit verification."
]

# Write the report
Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text("\n".join(report) + "\n")

print(f"Report saved to: {args.output}")

