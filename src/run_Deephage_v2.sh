#!/usr/bin/env bash

if [ $# == 0 ];then
    echo -e "Usage: $0 <list> <resultDir> <outputfile>
       list: two coloumn sampleID  fnapath (tab sep)
       Ps: for single run: optput  willbe in deephage dir:sampleID.deephage.csv
           deephage_single inputseq sampleID 
       Example:(test_dir)
       sh ../src/run_Deephage.sh ./example.txt ./RepliPhage/deephage deephage_opt.tsv ../resources ""
       "
    exit 0

fi


## because the program must be execult in the script dir. so just copy it to current dir
function cpdeePhage(){
    local wd=${1:-"."}
    local wdpath=`realpath $wd`
    local resources_dir=$2
    if [ ! -e "$wdpath/DeePhage" ];then
        echo "copy deephage script to $wdpath"
        cp -r $resources_dir $wdpath
        echo 'done'
    else
        echo "DeePhage source code exist in $wdpath"
    fi
}


## input is list with two coloumn sampleID \t fapath
function deephage_single(){
    local inputseq=$1
    local sampleID=${2:-'test'}
    opt="$sampleID.deephage.csv"

    cd ./DeePhage
    ./DeePhage $inputseq $opt 
    cd ..
}

######################
### program  #########
######################

input_seq_list=$1
workdir=$2
summary=$3
db=${4}
otherpara=${5:-""}


## activate conda
echo "RUN DeePhage"
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
source $conda_home/etc/profile.d/conda.sh
conda activate RP_deephage

script_realpath=`realpath $0`
script_dir=`dirname $script_realpath`
source $script_dir/../env/RP_Deephage.source.sh


## prepare environment
## enter wkdir and copy Deephage
currentdir=`pwd`
indexfullpath=`realpath $input_seq_list`

mkdir -p $workdir
 
deephage_source_dir=$db
cpdeePhage $workdir $deephage_source_dir

cd $workdir


## example for batch
# input file is two column file. sampleID \t filepath
summaryopt=$summary
echo -e "sampleID,contig,length,score,lifestyle" >$summaryopt

merged_seq="merged.input.all.fasta"
merged_seq_realpath=`realpath $merged_seq`
if [ -e $merged_seq_realpath ];then
    rm -rf $merged_seq_realpath
fi

while IFS=$'\t' read -ra line;do
    echo "process $line"
    sampleID=${line[0]}
    filePath=`echo ${line[1]}|sed 's/\n$//g'`
    echo $filePath
     
    less $filePath |sed "s/>/>$sampleID|/g" >> $merged_seq_realpath 
done < $indexfullpath

cd ./DeePhage
./DeePhage $merged_seq_realpath ./deephage_prediction.csv
cd ..

grep_opt=`grep \" ./DeePhage/deephage_prediction.csv`
if [ -n "$grep_opt" ];then
    echo "result contain comma, try to solve"
    tail -n +2 ./DeePhage/deephage_prediction.csv|sed 's/^\"//g'|sed 's/|/,\"/1' >> $summaryopt
else
    tail -n +2 ./DeePhage/deephage_prediction.csv|sed 's/^\"//g'|sed 's/|/,/1' >> $summaryopt
fi

conda deactivate 
cd $currentdir

