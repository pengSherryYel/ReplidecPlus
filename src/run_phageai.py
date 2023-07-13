#!/project/genomics/xuePeng/software/python3.9.5/bin/python3.9
import os
import csv
from pathlib import Path
import sys

fasta_path=sys.argv[1]

from phageai.lifecycle.classifier import LifeCycleClassifier

lcc = LifeCycleClassifier(access_token='nwt3zR9SwDOOfw5eeChbK5jZx3vdUl')

# Be aware that directory have to includes *.fasta files only
phage_dir_path = Path(fasta_path)
phage_directory = os.listdir(phage_dir_path)

prediction_results = {}

for single_fasta_file in phage_directory:
    try:
        prediction_results[single_fasta_file] = lcc.predict(fasta_path=os.path.join(phage_dir_path,single_fasta_file))
    except Exception as e:
        print(f'[PhageAI] Phage {single_fasta_file} raised an exception "{e}"')

# Python dict with prediction results
for fasta, phageai in prediction_results.items():
    print(fasta, phageai)

# Prepare CSV report as a final result
csv_columns = [
    'fasta_name', 'predicted_lifecycle', 'prediction_accuracy',
    'gc', 'sequence_length','hash'
]

# CSV file name
csv_file = "phageai_report.csv"

with open(csv_file, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()

    for fasta_name, phage_data in zip(prediction_results.keys(), prediction_results.values()):
        phage_data["fasta_name"] = fasta_name
        writer.writerow(phage_data)
