
# Lab 5: Scalable Analysis Workflow

## Overview

This project implements a reproducible data analysis workflow using Snakemake. It integrates data-cleaning techniques from Lab 3 with SQL-based feature extraction from Lab 4.

The workflow demonstrates how individual Python scripts can be organized into a Directed Acyclic Graph (DAG), allowing automated execution and selective rerunning of dependent steps.

## Workflow Stages

1. **Clean Samples:** Standardize sample identifiers, dates, sex, enrollment sites, and glucose units from `messy_samples.csv`.
2. **Build Patient Features:** Query `cohort.db` using SQL to generate a patient-level feature table.
3. **Combine Tables:** Combine both processed datasets into a source-labeled analysis table.
4. **Generate Report:** Produce descriptive statistics and a summary of data-quality limitations.

## Project Structure

```text
lab5-scalable-workflow/
├── Snakefile
├── README.md
├── AI_USAGE.md
├── environment.yml
├── .gitignore
├── scripts/
│   ├── clean_samples.py
│   ├── clean_regex.py
│   ├── build_feature_table.py
│   ├── merge_tables.py
│   └── generate_report.py
├── data/
│   ├── raw/
│   └── processed/
│       ├── cleaned_samples.csv
│       ├── feature_table.tsv
│       └── combined_analysis.csv
├── results/
│   └── summary_report.txt
└── evidence/
    ├── full_run.txt
    ├── partial_rerun.txt
    └── input_change_rerun.txt
```

## Requirements

- Python 3.11
- Snakemake 9.24.0
- pandas
- Conda or Miniforge

## Installation

Create the environment:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate lab5-workflow
```

## Input Data

The workflow requires:

- `data/raw/messy_samples.csv` — messy sample data from the course repository.
- `data/raw/cohort.db` — SQLite patient database used in Lab 4.

The input files must be present before running the workflow.

## Running the Full Workflow

From the repository root:

```bash
snakemake --cores 1 -p
```

To perform a clean run, first delete the generated outputs:

```bash
rm -f data/processed/cleaned_samples.csv \
      data/processed/feature_table.tsv \
      data/processed/combined_analysis.csv \
      results/summary_report.txt
```

Then execute the workflow:

```bash
snakemake --cores 1 -p
```

Snakemake automatically runs all four analysis stages in dependency order.

Evidence from a successful full run is saved in `evidence/full_run.txt`.

## Demonstrating a Partial Rerun

An upstream input change can be tested by modifying a value in `data/raw/messy_samples.csv`, then executing:

```bash
snakemake --cores 1 -p
```

Only the affected downstream rules should execute:

- `clean_samples`
- `combine_tables`
- `generate_report`

The `build_features` rule should be skipped because the database input remains unchanged.

Evidence is provided in `evidence/input_change_rerun.txt`.

A forced rerun of the cleaning stage can also be demonstrated using:

```bash
snakemake --cores 1 -p --forcerun clean_samples
```

## Results

The workflow produced:

- 60 cleaned sample records
- 566 unique database patient records
- 626 records in the combined analysis table
- A text summary report

The mean glucose value among measurements explicitly labeled mg/dL was approximately 152.48 mg/dL.

Measurements labeled mmol/L were excluded from the glucose average because their recorded magnitudes suggested possible unit-label inconsistencies.

## Data Integration Limitations

The Lab 3 and Lab 4 datasets use different identifier systems and do not have an established patient-level relationship.

Therefore, the datasets were concatenated with a `source` column rather than joined using fabricated patient matches.

The resulting combined table preserves data provenance but should not be interpreted as a matched patient-level dataset.

## Reproducibility

Snakemake tracks declared file dependencies and automatically reruns affected stages when inputs or scripts change.

A full run and an input-change partial rerun were successfully demonstrated.

## AI Assistance

Generative AI was used to assist with Snakemake syntax, Python script adaptation, debugging, documentation, and workflow testing.

See`AI_USAGE.md` for additional details.
