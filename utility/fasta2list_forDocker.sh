#!/usr/bin/env bash

inputfna=$1
outputlist=$2
split_dir=${3:-"."} 

inputfna_real=`realpath $inputfna`
outputlist_real=`realpath $outputlist`

if [ -e $split_dir ];then rm -r $split_dir && mkdir $split_dir; else mkdir $split_dir;fi

cd $split_dir
less $inputfna_real |sed 's/|/__/g' > changed_name.fna
awk -F " " '/^>/ {close(F); ID=$1; gsub("^>", "", ID); F=ID".fasta"} {print >> F}' changed_name.fna && rm -rf changed_name.fna 

## fit the path to docker mount environment
split_dir_nopartents=`echo $split_dir|sed 's/^.\///g'`
ls *.fasta|awk -F '/' -v sd="$split_dir_nopartents" '{printf "%s\t/data/%s/%s\n",$NF ,sd ,$0}'|sed 's/.fasta//1' > $outputlist_real

cd ..

## fit the path to docker mount environment
head $outputlist_real
