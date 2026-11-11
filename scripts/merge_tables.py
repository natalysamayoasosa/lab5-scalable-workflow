
import argparse
from pathlib import Path
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--samples", required=True)
parser.add_argument("--features", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

# Read the two processed tables
samples = pd.read_csv(args.samples)
features = pd.read_csv(args.features, sep="\t")

# Identify where each record came from
samples["source"] = "messy_samples"
features["source"] = "cohort_database"

# Use one identifier column without implying a patient match
samples = samples.rename(columns={"sample_id": "record_id"})
features = features.rename(columns={"patient_id": "record_id"})

# Avoid exporting names or birth dates into the combined table
samples = samples.drop(columns=["patient_name", "dob"], errors="ignore")

# Combine records while retaining source-specific columns
combined = pd.concat([samples, features], ignore_index=True)

# Save
Path(args.output).parent.mkdir(parents=True, exist_ok=True)
combined.to_csv(args.output, index=False)

print(f"Sample records: {len(samples)}")
print(f"Database records: {len(features)}")
print(f"Combined records: {len(combined)}")
print(f"Saved to: {args.output}")

