#!/usr/bin/env bash

input_seq_list=$1
workdir=$2
summary=$3
db=${4:-""}
otherpara=${5:-""}

echo "RUN replidec"
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
#source $conda_home/etc/profile.d/conda.sh
. $conda_home/etc/profile.d/conda.sh

conda activate RP_replidec 
# Because new version of Replidec were remove -D parameter, here change it.
#echo "Replidec -i $input_seq_list -p multiSeqAsOne -w $workdir -s $summary -D $db $otherpara"
#Replidec -i $input_seq_list -p multiSeqAsOne -w $workdir -s $summary -D $db $otherpara

echo "Replidec -i $input_seq_list -p genome_table -w $workdir -n $summary $otherpara"
Replidec -i $input_seq_list -p genome_table -w $workdir -n $summary $otherpara
conda deactivate
