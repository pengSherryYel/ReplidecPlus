#!/usr/bin/env bash

input_seq=$1
workdir=$2
summary=$3
db=${4:-""}
otherpara=${5:-""}

echo "RUN replidec"
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
. $conda_home/etc/profile.d/conda.sh

conda activate RP_replidec
echo "Replidec -i $input_seq -p multi_fasta -w $workdir -n $summary $otherpara"
Replidec -i $input_seq -p multi_fasta -w $workdir -n $summary $otherpara
conda deactivate
