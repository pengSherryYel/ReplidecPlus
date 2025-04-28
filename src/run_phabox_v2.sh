#!/usr/bin/env bash

input_seq_list=$1
workdir=$2
summary=$3
db=$4
otherpara=${5:-"--threads 8 --len 3000"}

echo "RUN PhaBox"
conda_path=`which conda`
conda_tmp=`dirname $conda_path`
conda_home=`dirname $conda_tmp`
#source $conda_home/etc/profile.d/conda.sh
. $conda_home/etc/profile.d/conda.sh


function cpphabox(){
    local wd=${1:-"."}
    local wdpath=`realpath $wd`
    local resources_dir=$2
    if [ ! -e "$wdpath/PhaBOX" ];then
        echo "copy PhaBOX script to $wdpath"
        cp -r $resources_dir $wdpath
        echo 'done'
    else
        echo "PhaBox source code exist in $wdpath"
    fi
}

## prepare env
conda activate RP_phabox

currentdir=`pwd`
indexfullpath=`realpath $input_seq_list`

mkdir -p $workdir
 
phabox_source_dir=$db
cpphabox $workdir $phabox_source_dir

cd $workdir


## example for batch
# input file is two column file. sampleID \t filepath
summaryopt=$summary
echo -e "SampleID,Accession,Length,Pred,Score" >$summaryopt

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

cd ./PhaBOX
python PhaTYP_single.py --contigs $merged_seq_realpath $otherpara --rootpth ./merged --out merge --midfolder merge --dbdir database/ --parampth parameters/
cd ..
tail -n +2 ./PhaBOX/merged/merge/phatyp_prediction.csv|sed 's/|/,/1' >> $summaryopt

conda deactivate 
cd $currentdir

