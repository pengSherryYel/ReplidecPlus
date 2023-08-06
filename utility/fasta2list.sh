#!/usr/bin/env bash

inputfna=$1
outputlist=$2
split_dir=$3

inputfna_real=`realpath $inputfna`
outputlist_real=`realpath $outputlist`

if [ -e $split_dir ];then rm -r $split_dir && mkdir $split_dir; else mkdir $split_dir;fi

cd $split_dir
less $inputfna_real |sed 's/|/__/g' > changed_name.fna
awk -F " " '/^>/ {close(F); ID=$1; gsub("^>", "", ID); F=ID".fasta"} {print >> F}' changed_name.fna && rm -rf changed_name.fna 
realpath *.fasta|awk -F '/' '{printf "%s\t%s\n",$NF ,$0}'|sed 's/.fasta//1' > $outputlist_real
cd ..

head $outputlist_real
