
# Lab 5: Scalable Analysis Workflow
# Four-stage workflow using Snakemake

rule all:
    input:
        "results/summary_report.txt"


# Stage 1: Clean messy sample data
rule clean_samples:
    input:
        data="data/raw/messy_samples.csv",
        script="scripts/clean_samples.py"
    output:
        "data/processed/cleaned_samples.csv"
    shell:
        """
        python {input.script} \
          --input {input.data} \
          --output {output}
        """


# Stage 2: Query the patient database
rule build_features:
    input:
        db="data/raw/cohort.db",
        script="scripts/build_feature_table.py"
    output:
        "data/processed/feature_table.tsv"
    shell:
        """
        python {input.script}
        """


# Stage 3: Combine the two processed tables
rule combine_tables:
    input:
        samples="data/processed/cleaned_samples.csv",
        features="data/processed/feature_table.tsv",
        script="scripts/merge_tables.py"
    output:
        "data/processed/combined_analysis.csv"
    shell:
        """
        python {input.script} \
          --samples {input.samples} \
          --features {input.features} \
          --output {output}
        """


# Stage 4: Generate the summary report
rule generate_report:
    input:
        table="data/processed/combined_analysis.csv",
        script="scripts/generate_report.py"
    output:
        "results/summary_report.txt"
    shell:
        """
        python {input.script} \
          --input {input.table} \
          --output {output}
        """

