#!/usr/bin/bash
# make sure you have phacts in your python. pip install phacts. 
# website: https://pypi.org/project/phacts/

#source /home/viro/xue.peng/software_home/PHACTS/phacts/bin/activate
#export PATH=/home/viro/xue.peng/software_home/fasta-35.4.5/bin:$PATH

## faa as input
echo "please pay attention the input file is a [faa] file. if not can ues prodigal to predict"


if [ $# == 0 ];then
    echo -e "Usage: $0 <input>
       input:sampleID,faaPath(tab)
       phacts.py *faa"
fi

# example for single
# phacts.py example/test.faa
#phacts.py $1


# example for batch
# input file is two column file. sampleID \t filepath
opt="$1.phacts.opt"
echo -e "sampleID\tlifestyle\tscore\tsd" >$opt
while IFS=$'\t' read -ra line;do
    echo "process $line"
    sampleID=${line[0]}
    filePath=`echo ${line[1]}|sed 's/\n$//g'`
    #echo $filePath
    ## reassign the variable. pay attention
    read label score sd <<< `phacts.py $filePath|tail -n 1`
    echo -e "$sampleID\t$label\t$score\t$sd" >> $opt
done < $1

