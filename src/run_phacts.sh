#!/usr/bin/bash
# make sure you have phacts in your python. pip install phacts. 
# website: https://pypi.org/project/phacts/

input_seq_list=$1
workdir=${2:-"./phacts"}
summary=${3:-"phacts_opt.tsv"}
db=${4:-""}
otherpara=${5:-""}

echo "RUN phacts"
echo "please pay attention the input file is a [faa] file. if not can ues prodigal to predict"

if [ $# == 0 ];then
    echo -e "Usage: $0 <input>
       input:sampleID,faaPath(tab)
       phacts.py *faa"
fi

## load conda
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
source $conda_home/etc/profile.d/conda.sh
conda activate RP_phacts
if [ ! -e $workdir ];then mkdir $workdir; fi

## prepare faa list
# example for single
# phacts.py example/test.faa
#phacts.py $1


# example for batch
# input file is two column file. sampleID \t filepath
#opt="$1.phacts.opt"
opt="$workdir/$summary"
echo -e "sampleID\tlifestyle\tscore\tsd" >$opt
while IFS=$'\t' read -ra line;do
    echo "process $line"
    sampleID=${line[0]}
    filePath=`echo ${line[1]}|sed 's/\n$//g'`
    #echo $filePath

    ## predict the faa
    prodigal_dir="$workdir/prodigal"
    if [ ! -e $prodigal_dir ];then mkdir $prodigal_dir; fi
    faa="$prodigal_dir/$sampleID.faa"
    ffn="$prodigal_dir/$sampleID.ffn"
    gff="$prodigal_dir/$sampleID.gff"
    prodigal -a $faa -d $ffn -f gff -o $gff -g 11 -p meta -i $filePath
    
    ## predict phacts
    ## reassign the variable. pay attention
    echo "RUNNING PHACTS: $sampleID"
    read label score sd <<< `phacts.py $faa|tail -n 1`
    echo -e "$sampleID\t$label\t$score\t$sd" >> $opt

done < $input_seq_list

