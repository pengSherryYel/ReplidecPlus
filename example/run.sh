#!/usr/bin/bash

##Example for conda
cd example
conda activate RP_base
sh ../utility/fasta2list.sh sequences.fasta sequence.list sequence_split 
python ../ReplidecPlus.py -i sequence.list -o example_repliplus -t 4 -r -b -p -d 



## Example for docker
cd ReplidecPlus 
docker run --rm --platform linux/amd64 -v `pwd`:/data pengsherry/replidec_plus:v2.1 conda run -n RP_base sh /data/utility/fasta2list.sh /data/example/sequences.fasta /data/example/sequence.list /data/example/sequence_split

docker run --rm --platform linux/amd64 -v `pwd`:/data pengsherry/replidec_plus:v2.1 conda run -n RP_base python ReplidecPlus/ReplidecPlus.py -i /data/example/sequence.list -o /data/example/repliplus_v2.1 -t 2 -r -rf -p -pf -d -df -b -bf
