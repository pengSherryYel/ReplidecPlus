#!/usr/bin/env bash
input_seq_list=$1
workdir=$2
summary=${3:-""}
db=${4:-""}
otherpara=${5:-""}

echo "RUN BACPHLIP"
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
source $conda_home/etc/profile.d/conda.sh

current_path=`realpath $0`
parent_dir=`dirname $current_path`
conda activate RP_bacphlip
echo "$parent_dir/run_bacphlip.py $input_seq_list $workdir"
$parent_dir/run_bacphlip.py $input_seq_list $workdir
conda deactivate

