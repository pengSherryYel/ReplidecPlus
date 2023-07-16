# coding: utf-8
# %load merged_all.py
# %load merged_all.py
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

## merge all the output
def parse_result(input_list, resultD, output_file):
    inputDf = pd.read_csv(input_list,names=['sample_name','file'],sep="\t").loc[:,["sample_name"]]
    #print(inputDf )
   
    softwares=['replidec', 'deephage', 'bacphlip', 'phabox', 'phacts']
    for software,infile in resultD.items():
        print(software,infile)
        if infile:
            if software == "replidec":
                header=['sample_name','pfam_label','bc_label', 'final_label','match_gene_number']
                new_header=['sample_name','replidec_pfam','replidec_bc', 'replidec_final','replidec_match_gene_number']
                d = pd.read_csv(infile,header=0,sep="\t")
                replidecDf = d.loc[:,header]
                replidecDf.columns =new_header
                #print(replidecDf)
                inputDf = inputDf.merge(replidecDf, on="sample_name", how="left")
                 
            elif software == "deephage":
                d = pd.read_csv(infile,header=0,sep=",")
                resultD = {}
                for i in d.index:
                    sampleid = d.loc[i,"sampleID"]
                    if sampleid not in resultD:
                        resultD[sampleid] = [0,0,0]
                        
                    lifestyle = d.loc[i,"lifestyle"]
                    if lifestyle == "temperate":
                        resultD[sampleid][0]+=1
                    elif lifestyle == "virulent":
                        resultD[sampleid][1]+=1
                    else:
                        resultD[sampleid][2]+=1
                
                t=[]
                for sid,resultL in resultD.items():
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
                bacphlipDf = pd.read_csv(infile,header=0,sep="\t").loc[:,["sampleID", "bacphlip_ressult"]]
                bacphlipDf.columns=['sample_name','bacphlip_label']
                inputDf = inputDf.merge(bacphlipDf, on="sample_name", how="left")
                
            elif software == "phabox":
                d = pd.read_csv(infile,header=0,sep=",")
                resultD = {}
                for i in d.index:
                    sampleid = d.loc[i,"SampleID"]
                    if sampleid not in resultD:
                        resultD[sampleid] = [0,0,0]

                    lifestyle = d.loc[i,"Pred"]
                    if lifestyle == "temperate":
                        resultD[sampleid][0]+=1
                    elif lifestyle == "virulent":
                        resultD[sampleid][1]+=1
                    else:
                        resultD[sampleid][2]+=1

                t=[]
                for sid,resultL in resultD.items():
                    phabox_final = "Virulent"
                    if resultL[0] > resultL[1]:
                        phabox_final = "Temperate"
                    elif resultL[0] == resultL[1]:
                        phabox_final = "Undecide"
                    phabox_stat = "|".join([str(i) for i in resultL])
                    t.append([sid, phabox_stat ,phabox_final])
                phaboxDf = pd.DataFrame(t,columns=['sample_name',"phabox_T|V|O","phabox_final"])
                inputDf = inputDf.merge(phaboxDf, on="sample_name", how="left")
             
            elif software == "phacts":
                d = pd.read_csv(infile,header=0,sep="\t")
                phactsDf = d.loc[:,["sampleID", "lifestyle"]]
                phactsDf.columns=['sample_name','phacts_label']
                inputDf = inputDf.merge(phactsDf, on="sample_name", how="left")
                
    print(inputDf)
    ## merged all
    inputDf.to_csv(output_file, sep=",", index=False)
    
if __name__ == "__main__":
    outD={'replidec': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/replidec/replidec.prokaryote.opt.tsv','deephage': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/deephage/deephage.opt.tsv','bacphlip': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/bacphlip/bacphlip_report.txt','phabox': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/phabox/phabox.opt.tsv','phacts': '/dss/dsshome1/09/ge85hit2/repliphage_code/RepliPhage/test/RepliPhage/phacts/phacts.opt.tsv'}
    parse_result("example.txt",outD,"merged_all.tsv")    
