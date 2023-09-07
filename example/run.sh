#!/usr/bin/bash
conda activate RP_base
sh ../utility/fasta2list.sh sequences.fasta sequence.list sequence_split 
python ../RepliPhage.py -i sequence.list -o example_repliplus -t 4 -r -b -p -d 

