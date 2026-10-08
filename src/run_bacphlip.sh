#!/usr/bin/env bash
input_seq=$1
workdir=$2
summary=${3:-""}
db=${4:-""}
otherpara=${5:-""}

echo "RUN BACPHLIP"
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
. $conda_home/etc/profile.d/conda.sh

current_path=`realpath $0`
parent_dir=`dirname $current_path`
conda activate RP_bacphlip
cp $input_seq $workdir/"tmp_input.fna"
bacphlip -i $workdir/"tmp_input.fna" --multi_fasta
rm $workdir/"tmp_input.fna"

# Bacphlip results modification
awk 'BEGIN { FS="\t"; OFS="\t"; print "sampleID", "bacphlip_result" }
     NR > 1 {
         if ($2 > $3) {
             print $1, "Virulent"
         } else {
             print $1, "Temperate"
         }
     }' $workdir/"tmp_input.fna.bacphlip" > $workdir/"bacphlip_final_output.tsv"

conda deactivate

