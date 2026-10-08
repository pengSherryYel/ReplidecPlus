#!/usr/bin/env python
# coding: utf-8

import bacphlip
import os
import sys
import pandas as pd
from Bio import Seq,SeqIO
import shutil

def calculate(seqfile):
    return sum(1 for _ in SeqIO.parse(seqfile, "fasta"))

def mkdirs(dirname):
    '''
    makedirs
    '''
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

def bacphlip_predict_multi(seqfile,optdir,force_overwrite=True, local_hmmsearch="/home/viro/xue.peng/.linuxbrew/bin/hmmsearch"):
    os.makedirs(optdir)

    path,target_file = os.path.split(seqfile)
    new_target_file_link = os.path.join(optdir,target_file)
    if not os.path.exists(new_target_file_link):
        os.symlink(seqfile,new_target_file_link)

    outputSuffix = ["6frame","bacphlip","hmmsearch","hmmsearch.tsv"]
    outputFile = "%s.%s"%(new_target_file_link,outputSuffix[1])
    if not os.path.exists(new_target_file_link):
        os.symlink(os.path.abspath(seqfile), new_target_file_link)

    outputFile = f"{new_target_file_link}.bacphlip"

    # Run Bacphlip pipeline
    print("Calculating sequence count...")
    genome_number = calculate(seqfile)
    print(f"Total contigs found: {genome_number}")

    if genome_number > 1:
        bacphlip.run_pipeline_multi(new_target_file_link, force_overwrite=force_overwrite,
                                    local_hmmsearch=local_hmmsearch)
    else:
        bacphlip.run_pipeline(new_target_file_link, force_overwrite=force_overwrite, local_hmmsearch=local_hmmsearch)

    if not os.path.exists(outputFile):
        raise FileNotFoundError(f"Expected Bacphlip output not found at: {outputFile}")

    # Parse and report prediction for every contig/sequence
    df = pd.read_csv(outputFile, header=0, sep="\t")

    summary_file = os.path.join(optdir, "bacphlip_summary.tsv")
    results = []

    print("\n--- Predictions ---")
    print("Contig_ID\tPrediction\tVirulent|Temperate")

    for _, row in df.iterrows():
        contig_id = str(row.iloc[0])
        virulent = float(row["Virulent"])
        temperate = float(row["Temperate"])

        lstype = "Virulent" if virulent > temperate else "Temperate"
        score_str = f"{virulent:.4f}|{temperate:.4f}"

        print(f"{contig_id}\t{lstype}\t{score_str}")
        results.append({
            "Contig_ID": contig_id,
            "Prediction": lstype,
            "Virulent_Score": virulent,
            "Temperate_Score": temperate
        })

    # Save summary table
    summary_df = pd.DataFrame(results)
    summary_df.to_csv(summary_file, sep="\t", index=False)
    print(f"\nSummary table saved to: {summary_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <multi_fasta_file> <output_dir>")
        sys.exit(1)

    inputfasta = sys.argv[1]
    optdir = sys.argv[2]
    hmmer_path=shutil.which("hmmsearch")
    bacphlip_predict_multi(
        input_fasta,
        optdir,
        force_overwrite=True,
        local_hmmsearch=hmmer_path
    )

