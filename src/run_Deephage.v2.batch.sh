#!/usr/bin/bash

if [ $# == 0 ];then
    echo -e "Usage: $0 <list> <resultDir>
       list: two coloumn sampleID  fnapath (tab sep)
       Ps: for single run: optput  willbe in deephage dir:sampleID.deephage.csv
           deephage_single inputseq sampleID "
    exit 0

fi


## because the program must be execult in the script dir. so just copy it to current dir
function cpdeePhage(){
    local wd=${1:-"."}
    local wdpath=`realpath $wd`
    mkdir -p $wdpath
    if [ ! -e "$wdpath/DeePhage" ];then
        echo "copy deephage script to $wdpath"
        cp -r /home/viro/xue.peng/software_home/DeePhage $wdpath
        echo 'done'
    fi
}


## input is list with two coloumn sampleID \t fapath
function deephage_single(){
    inputseq=$1
    local sampleID=${2:-'test'}
    opt="$sampleID.deephage.csv"

    cd ./DeePhage
    $deephage $inputseq $opt 
    cd ..

    ########## not uesful #################
    #contig=`tail -n 1 $opt|awk -vFPAT='([^,]*)|("[^"]+")' -vOFS=, '{print $1}'|sed 's/\"//g'`
    #length=`tail -n 1 $opt|awk -vFPAT='([^,]*)|("[^"]+")' -vOFS=, '{print $2}'`
    #score=`tail -n 1 $opt|awk -vFPAT='([^,]*)|("[^"]+")' -vOFS=, '{print $3}'`
    #label=`tail -n 1 $opt|awk -vFPAT='([^,]*)|("[^"]+")' -vOFS=, '{print $4}'`
    #echo -e "$sampleID\t$length\t$score\t$label\t$contig" &&\
    #rm -rf $opt &&\
    ####################################
    
}


## prepare environment
. /home/viro/xue.peng/software_home/DeePhage/SourceMe.sh
cpdeePhage $2

## enter wkdir
currentdir=`pwd`
indexfullpath=`realpath $1`
cd $2
deephage="./DeePhage"

## example for single
#sh run_Deephage.sh /project/genomics/xuePeng/workPlace/2021/lifestyle_predict_my/data/phageai/sample1/NC_013693.fasta NC_013693
#deephage_single $1 $2


## example for batch
# input file is two column file. sampleID \t filepath
summaryopt="$1.DeePhage.opt"
echo -e "sampleID,contig,length,score,lifestyle" >$summaryopt

while IFS=$'\t' read -ra line;do
    echo "process $line"
    sampleID=${line[0]}
    filePath=`echo ${line[1]}|sed 's/\n$//g'`
    #echo $filePath

    ## reassign the variable. pay attention
    deephage_single $filePath $sampleID &&\
    tail -n +2 ./DeePhage/$opt|sed "s/^/$sampleID,/" >> $summaryopt
done < $indexfullpath

conda deactivate
cd $currentdir

