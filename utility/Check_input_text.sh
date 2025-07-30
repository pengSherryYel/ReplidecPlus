#!/usr/bin/bash

## This file help you check if your input text format

input_text=$1

echo "Check 1: Separator "
awk -F '\t' '{if (NF!=2) {print "Row",NR,"is WRONG, Check the Separator, ONLY TAB ALLOWED!!"}}' $input_text
echo "-----------------------"


echo "Check 2: Unnecessary Characters"

res=`less $input_text|cut -f 1|rev|cut -d " " -f 2-|rev|sed -n /[[:space:]]/p`

if [ -n "$res" ];
then
echo "\nPlease changes spaces within contig name OR next to the contig name (Left side or Right side)"
less $input_text|cut -f 1|rev|cut -d " " -f 2-|rev|sed -n /[[:space:]]/p
fi


res=`less $input_text|cut -f 1|rev|cut -d " " -f 2-|rev|sed -n /,/p`
if [ -n "$res" ];
then
echo "\nPlease changes comma in these contig name"
less $input_text|cut -f 1|rev|cut -d " " -f 2-|rev|sed -n /,/p
fi
echo "-----------------------"


echo "DONE!"
