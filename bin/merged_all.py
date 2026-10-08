# coding: utf-8
# %load merged_all.py
# %load merged_all.py
import os
import pandas as pd
import numpy as np
from collections import defaultdict, Counter



## merge all the output
def parse_result(input_fasta, resultD, output_file):
    contig_names = []
    with open(input_fasta, "r") as f:
        for line in f:
            if line.startswith(">"):
                contig_id = line.strip()[1:].split()[0]
                contig_names.append(contig_id)


    inputDf = pd.DataFrame({'sample_name': contig_names})

    print("## Number of input genomes:",len(inputDf))

    for software,infile in resultD.items():

        clen=0
        with open(infile,"r") as f:
            c=f.readlines()
            clen = len(c)
        
        print("%s:%s\t%s\n"%(software,clen-1,infile))

        if infile and clen > 2:
            if software == "replidec":
                header=['sample_name','pfam_label','bc_label', 'final_label','match_gene_number']
                new_header=['sample_name','replidec_pfam','replidec_bc', 'replidec_final','replidec_match_gene_number']
                d = pd.read_csv(infile,header=0,sep="\t")
                replidecDf = d.loc[:,header]
                replidecDf.columns =new_header
                inputDf = inputDf.merge(replidecDf, on="sample_name", how="left")
                 
            elif software == "deephage":
                d = pd.read_csv(infile,header=0,sep=",",quotechar = '"')
                #print(d)
                # resultD = {}
                deephage_counts = {}
                for i in d.index:
                    sampleid = d.loc[i,"sampleID"]
                    
                    if sampleid not in deephage_counts:
                        deephage_counts[sampleid] = [0,0,0]
                        
                    lifestyle = d.loc[i,"lifestyle"]
                    if lifestyle == "temperate":
                        deephage_counts[sampleid][0]+=1
                    elif lifestyle == "virulent":
                        deephage_counts[sampleid][1]+=1
                    else:
                        deephage_counts[sampleid][2]+=1
                
                t=[]
                for sid,resultL in deephage_counts.items():
                    deephage_final = "Virulent"
                    if resultL[0] > resultL[1]:
                        deephage_final = "Temperate"
                    elif resultL[0] == resultL[1]:
                        deephage_final = "Undecide"
                    deephage_stat = "|".join([str(i) for i in resultL])
                    t.append([sid, deephage_stat ,deephage_final])
                deephageDf = pd.DataFrame(t,columns=['sample_name',"deephage_T|V|O","deephage_final"]) 
                inputDf = inputDf.merge(deephageDf, on="sample_name", how="left")
                #print(deephageDf)
                
            elif software == "bacphlip":
                #print(infile)
                bacphlipDf = pd.read_csv(infile,header=0,sep="\t").loc[:,["sampleID", "bacphlip_result"]]
                print (bacphlipDf)
                bacphlipDf.columns=['sample_name','bacphlip_label']
                inputDf = inputDf.merge(bacphlipDf, on="sample_name", how="left")
                
            elif software == "phabox":
                d = pd.read_csv(infile,header=0,sep="\t")
                # resultD = {}
                phabox_counts = {}
                for i in d.index:
                    sampleid = d.loc[i,"Accession"]
                    if sampleid not in phabox_counts:
                        phabox_counts[sampleid] = [0,0,0]

                    lifestyle = d.loc[i,"TYPE"]
                    if lifestyle == "temperate":
                        phabox_counts[sampleid][0]+=1
                    elif lifestyle == "virulent":
                        phabox_counts[sampleid][1]+=1
                    else:
                        phabox_counts[sampleid][2]+=1

                t=[]
                for sid,resultL in phabox_counts.items():
                    phabox_final = "Virulent"
                    if resultL[0] > resultL[1]:
                        phabox_final = "Temperate"
                    elif resultL[0] == resultL[1]:
                        phabox_final = "Undecide"
                    phabox_stat = "|".join([str(i) for i in resultL])
                    t.append([sid, phabox_stat ,phabox_final])
                phaboxDf = pd.DataFrame(t,columns=['sample_name',"phabox_T|V|O","phabox_final"])
                inputDf = inputDf.merge(phaboxDf, on="sample_name", how="left")

        elif clen < 2:
            print("WARNING: %s not complete. please rerun!!" %software)
    
    print(inputDf)
    
    ## merged all
    print("!! SUMMARY RESULT: store at %s"%output_file)
    inputDf.to_csv(output_file, sep=",", index=False)
    
if __name__ == "__main__":
    outD = {
        'replidec': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/replidec/replidec.prokaryote.opt.tsv',
        'deephage': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/deephage/deephage.opt.tsv',
        'bacphlip': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/bacphlip/bacphlip_final_output.tsv',
        'phabox': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/phabox/phatyp_prediction/phatyp_prediction.tsv',
        'phacts': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/phacts/phacts.opt.tsv'}

    parse_result("example.txt",outD,"merged_all.tsv")
