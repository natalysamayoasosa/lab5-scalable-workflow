# AI Usage Documentation — Lab 5

## AI Tools Used

- **Tool:** OpenAI ChatGPT
- **Purpose:** Assistance with Python programming, Snakemake workflow development, debugging, and documentation.

## How AI Was Used

**1. Python Script Development**

ChatGPT helped develop and adapt Python scripts for cleaning sample data, querying a SQLite database, combining analysis tables, and generating a summary report.

The cleaning script incorporated regular expressions and pandas to standardize sample identifiers, dates, enrollment sites, and glucose information.

**2. Snakemake Workflow Development**

ChatGPT assisted with the syntax and structure of the `Snakefile`, including defining rules, declaring inputs and outputs, and establishing dependencies between analysis stages.

**3. Debugging and Troubleshooting**

ChatGPT helped identify and resolve Python syntax errors, incorrect file paths, missing software dependencies, and problems with date formatting.

**4. Reproducibility Testing**

ChatGPT provided guidance for running the workflow from a clean state and demonstrating partial reruns after changes to upstream input files.

**5. Documentation**

ChatGPT assisted in drafting the README, explaining the workflow structure, documenting limitations, and providing reproducibility instructions.

## Changes and Decisions

During development, I reviewed AI-generated suggestions and made adjustments based on actual outputs and error messages.

These included:

- Correcting two-digit birth years that were incorrectly interpreted as future dates.
- Adjusting Python file paths to match the Lab 5 repository structure.
- Excluding glucose measurements with questionable unit labels from summary calculations.
- Using source-labeled concatenation rather than inventing patient matches between datasets with incompatible identifiers.
- Testing and debugging the workflow through repeated terminal executions.

## Verification

The workflow was tested through a successful full Snakemake run and an incremental rerun following an input change.

AI assistance was used throughout development, while the execution, testing, and verification were performed in the local computing environment.
