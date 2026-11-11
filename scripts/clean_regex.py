import re
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "data" / "raw" / "messy_sequences.fasta"
output_file = BASE_DIR / "data" / "processed" / "regex_cleaned_sequences.csv"
def read_fasta(file_path):
    records = []
    header = None
    sequence_parts = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith(">"):
                if header is not None:
                    records.append({
                        "header": header,
                        "sequence": "".join(sequence_parts)
                    })

                header = line[1:]
                sequence_parts = []

            else:
                sequence_parts.append(line)

        if header is not None:
            records.append({
                "header": header,
                "sequence": "".join(sequence_parts)
            })

    return records
def parse_header(header):
    # Sample ID
    sample_match = re.search(r"(sample|seq)[_\-\s]?0*(\d+)", header, re.IGNORECASE)

    if sample_match:
        sample_id = f"sample_{int(sample_match.group(2)):03d}"
    else:
        sample_id = "NA"

    # Organism
    if re.search(r"Homo[_\s]?sapiens|H\.sapiens|Hsapiens", header, re.IGNORECASE):
        organism = "Homo sapiens"
    else:
        organism = "NA"

    # Gene
    gene_match = re.search(r"\b(BRCA1|TP53|EGFR)\b", header, re.IGNORECASE)

    if gene_match:
        gene = gene_match.group(1).upper()
    else:
        gene = "NA"

    # Reported length
    length_match = re.search(
        r"(?:len(?:gth)?\s*[=:]?\s*|;\s*)(\d+)(?:\s*bp)?",
        header,
        re.IGNORECASE
    )

    if length_match:
        reported_length = int(length_match.group(1))
    else:
        reported_length = "NA"

    return {
        "sample_id": sample_id,
        "organism": organism,
        "gene": gene,
        "reported_length": reported_length
    }
records = read_fasta(input_file)

cleaned_records = []

for record in records:
    parsed = parse_header(record["header"])
    parsed["actual_sequence_length"] = len(record["sequence"])
    parsed["sequence"] = record["sequence"]

    cleaned_records.append(parsed)

fieldnames = [
    "sample_id",
    "organism",
    "gene",
    "reported_length",
    "actual_sequence_length",
    "sequence"
]

with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cleaned_records)

print(f"Cleaned {len(cleaned_records)} FASTA records.")
print(f"Output written to: {output_file}")
