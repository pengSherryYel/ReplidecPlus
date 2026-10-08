#!/usr/bin/env bash

if [ $# == 0 ];then
    echo -e "Usage: $0 <list> <resultDir> <outputfile>
       list: two coloumn sampleID  fnapath (tab sep)
       Ps: for single run: optput  will be in deephage dir:sampleID.deephage.csv
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

######################
### program  #########
######################

input_seq=$1
workdir=$2
summary=$3
db=${4}
otherpara=${5:-""}


## activate conda
echo "RUN DeePhage"
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
. $conda_home/etc/profile.d/conda.sh
conda activate RP_deephage

script_realpath=`realpath $0`
script_dir=`dirname $script_realpath`
. $script_dir/../env/RP_Deephage.source.sh


## prepare environment
## enter wkdir and copy Deephage
currentdir=`pwd`

mkdir -p $workdir
 
deephage_source_dir=$db
cpdeePhage $workdir $deephage_source_dir

cd $workdir


## example for batch
summaryopt=$summary

cd ./DeePhage
./DeePhage $input_seq ./deephage_prediction.csv
cd ..

grep_opt=`grep \" ./DeePhage/deephage_prediction.csv`
if [ -n "$grep_opt" ];then
    echo "result contain comma, try to solve"
    tail -n +2 ./DeePhage/deephage_prediction.csv|sed 's/^\"//g'|sed 's/|/,\"/1' >> $summaryopt
else
    tail -n +2 ./DeePhage/deephage_prediction.csv|sed 's/^\"//g'|sed 's/|/,/1' >> $summaryopt
fi

HEADER="sampleID,Length,lifestyle_score,lifestyle"
sed -i "1i ${HEADER}" "$summaryopt"

conda deactivate 
cd $currentdir

