
import argparse
import re
from pathlib import Path
import pandas as pd

# Allow Snakemake to specify input and output files
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

df = pd.read_csv(args.input, dtype=str)

# Standardize sample IDs: s-0003 -> S0003
def clean_sample_id(value):
    if pd.isna(value):
        return None
    match = re.fullmatch(r"S[\s-]*(\d+)", value.strip(), re.I)
    return f"S{int(match.group(1)):04d}" if match else None

df["sample_id"] = df["sample_id"].apply(clean_sample_id)

# Standardize sex
df["sex"] = df["sex"].str.strip().str.upper()
df["sex"] = df["sex"].replace({
    "FEMALE": "F",
    "MALE": "M"
})

# Standardize enrollment sites
df["enrollment_site"] = (
    df["enrollment_site"]
    .str.upper()
    .str.replace(r"\s+", "", regex=True)
)

# Standardize glucose values and units
df["glucose_value"] = pd.to_numeric(
    df["glucose_value"], errors="coerce"
)
df["glucose_unit"] = (
    df["glucose_unit"].str.strip().str.lower()
)

# Parse dates into a consistent format
from datetime import datetime

def clean_date(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    # Handle two-digit years, e.g. 11.24.53
    if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{2}", value):
        month, day, year = map(int, value.split("."))
        year += 1900 if year >= 30 else 2000
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            return None

    date = pd.to_datetime(value, errors="coerce")

    if pd.isna(date):
        return None

    if date.date() > datetime.now().date():
        return None

    return date.strftime("%Y-%m-%d")

df["dob"] = df["dob"].apply(clean_date)

# Save the cleaned table
Path(args.output).parent.mkdir(parents=True, exist_ok=True)
df.to_csv(args.output, index=False)

print(f"Cleaned {len(df)} rows.")
print(f"Saved cleaned table to {args.output}")

