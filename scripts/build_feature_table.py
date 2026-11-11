import sqlite3
from pathlib import Path
import pandas as pd

# Database and output paths
project_dir = Path(__file__).resolve().parent.parent
db_path = project_dir / "data" / "raw" / "cohort.db"
output_path = project_dir / "data" / "processed" / "feature_table.tsv"

conn = sqlite3.connect(db_path)

# Step 1: Get patient information and sample characteristics
# Aggregate samples to one row per patient
patient_query = """
SELECT
    p.patient_id,
    p.sex,
    p.age_at_diagnosis,
    p.stage,
    s.tissue_source_site,
    s.tmb_nonsynonymous
FROM patients AS p
LEFT JOIN samples AS s
    ON p.patient_id = s.patient_id;
"""

patients = pd.read_sql_query(patient_query, conn)

print("Patient rows after joining samples:", len(patients))

# Check that each patient appears once
assert len(patients) == 566
assert patients["patient_id"].is_unique

# Step 2: Get protein-altering mutation counts
mutation_query = """
SELECT
    p.patient_id,
    m.gene_symbol,
    COUNT(m.mutation_id) AS mutation_count
FROM patients AS p
LEFT JOIN samples AS s
    ON p.patient_id = s.patient_id
LEFT JOIN mutations AS m
    ON s.sample_id = m.sample_id
    AND m.gene_symbol IN ('TP53', 'KRAS', 'EGFR', 'STK11', 'KEAP1')
    AND m.variant_classification IS NOT NULL
    AND m.variant_classification != 'Silent'
GROUP BY p.patient_id, m.gene_symbol;
"""

mutations = pd.read_sql_query(mutation_query, conn)
conn.close()

# Remove rows where no mutation matched
mutations = mutations.dropna(subset=["gene_symbol"])

# Step 3: Reshape mutation data into wide format using Python
wide = mutations.pivot(
    index="patient_id",
    columns="gene_symbol",
    values="mutation_count"
)

# Include all five gene columns even if a gene has no mutations
genes = ["TP53", "KRAS", "EGFR", "STK11", "KEAP1"]
wide = wide.reindex(columns=genes, fill_value=0).fillna(0)
wide = wide.astype(int).reset_index()

# Step 4: Combine patient information with mutation counts
feature_table = patients.merge(
    wide,
    on="patient_id",
    how="left",
    validate="one_to_one"
)

# No recorded mutation in a selected gene = 0
feature_table[genes] = feature_table[genes].fillna(0).astype(int)

# Step 5: Validate the final table
print("Final patient rows:", len(feature_table))
print("Unique patients:", feature_table["patient_id"].nunique())

assert len(feature_table) == 566
assert feature_table["patient_id"].is_unique

# Step 6: Save as TSV
feature_table.to_csv(output_path, sep="\t", index=False)

print("\nFeature table saved to:", output_path)
print("\nFirst five rows:")
print(feature_table.head())

print("\nMissing values by column:")
print(feature_table.isna().sum())
