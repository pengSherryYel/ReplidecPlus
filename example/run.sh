#!/usr/bin/bash
. /dss/dsshome1/09/ge85hit2/miniconda3/etc/profile.d/conda.sh
conda activate RP_base
sh ../utility/fasta2list.sh sequences.fasta sequence.list sequence_split 
#sh ReplidecPlus/utility/fasta2list.sh GPD.split.fabv fabv.index fabv_split
python ../RepliPhage.py -i sequence.list -o example_repliplus -t 4 -r -b -p -d 

