#!/project/genomics/xuePeng/software/python3.9.5/bin/python3.9
import os
import time
import csv
from pathlib import Path
import sys

#fasta_path=sys.argv[1]
inseq_list=sys.argv[1]
#tokens=['nwt3zR9SwDOOfw5eeChbK5jZx3vdUl']
tokens=[
'3vyJFrOEvYD74AeIFn98qIwfuxf0yP',
#'nwt3zR9SwDOOfw5eeChbK5jZx3vdUl',
#'Md2nZaSjPm2ap2hUP6ZHCNGJihdq3S',
#'4ghWnwDNzxT2lb142SlJK83YuyVNEr',
#'MIpSPrBaUiX5Ccd08nhWwcbjXqgZPt',
#'koqGTapXXIywL2XCFqmprzrF23MwNB',
#'a5XCrN5VayHzXYvEVxheO35hSikNWF'
]
csv_file = "%s_phageai_report.csv"%inseq_list

from phageai.lifecycle.classifier import LifeCycleClassifier

#load data
inputD={}
with open(inseq_list) as f:
    for line in f:
        sampleid, path=line.strip("\n").split("\t")
        inputD[sampleid] = path

if tokens:
    token = tokens.pop()
    lcc = LifeCycleClassifier(access_token=token)

# Be aware that directory have to includes *.fasta files only
#phage_dir_path = Path(fasta_path)
#phage_directory = os.listdir(phage_dir_path)

prediction_results = {}

for sampleid, path in inputD.items():
    print(sampleid, path)
    try:
        print("Use token:%s"%token)
        prediction_results[sampleid] = lcc.predict(fasta_path=os.path.realpath(path))
    except Exception as e:
        print(tokens)
        if tokens:
            print("change token")
            token = tokens.pop()
            #lcc = LifeCycleClassifier(access_token=token)
            #prediction_results[sampleid] = lcc.predict(fasta_path=os.path.realpath(path))
        else:
            #print(f'[PhageAI] Phage {sampleid} raised an exception "{e}"')
            print('[PhageAI] Phage %s raised an exception %s'%(sampleid,e))
    finally:
        print(sampleid, prediction_results.get(sampleid))

#print(prediction_results)
# Python dict with prediction results
#for fasta, phageai in prediction_results.items():
#    print(fasta, phageai)

# Prepare CSV report as a final result
csv_columns = [
'fasta_name', 'predicted_lifecycle', 'prediction_accuracy',
'gc', 'sequence_length','hash'
]

# CSV file name
#csv_file = "phageai_report.csv"

with open(csv_file, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()

    for fasta_name, phage_data in zip(prediction_results.keys(), prediction_results.values()):
        phage_data["fasta_name"] = fasta_name
        writer.writerow(phage_data)
