#!/usr/bin/env bash

input_seq=$1
workdir=$2
summary=$3
db=$4
otherpara=${5:-"--task phatyp --threads 8 --len 3000"}

echo "RUN PhaBox"
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
. $conda_home/etc/profile.d/conda.sh

## prepare env
conda activate RP_phabox
currentdir=`pwd`
mkdir -p $workdir


phabox2 --contigs $input_seq $otherpara --outpth $workdir --dbdir $db

pred_file="$workdir/final_prediction/phatyp_prediction.tsv"
if [ -n "$pred_file" ] && [ -s "$pred_file" ]; then
    echo "Processing predictions from $pred_file"
    tail -n +2 "$pred_file" | sed 's/|/,/1' | sed 's/\t/,/g' >> "$summary"
else
    echo "Warning: No PhaBox prediction file found at $workdir. Summary file created empty." >&2
fi

cp $workdir/final_prediction/phatyp_prediction.tsv $workdir/phabox.opt.tsv

conda deactivate

