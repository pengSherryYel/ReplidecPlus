# coding: utf-8
import pandas as pd
from collections import Counter 
import sys

inputf = sys.argv[1]

## load weights for each software
load_weights=pd.read_csv("weights.allsft.list",index_col=0)

## load pre results 
ldf = pd.read_csv(inputf)
#ldf = pd.read_csv("/Users/pengxue/notneed4icolud/PROJECT/lifestyle_v2/v6/v6_testD3/IBD.merged.RepliPhage.summary.txt")

common=[]
for row in ldf.index:
    t = {"Temperate":0,
         "Virulent": 0,
         "Chronic": 0}
    countert = Counter()
    for col in ["deephage_final","phabox_final","bacphlip_label","replidec_final"]:
        lifestyle = ldf.loc[row,col]
        if lifestyle == "Temperate" or lifestyle == "Virulent":
            #print(load_weights.query('software==@col'))
            weight=load_weights.query('software==@col')[lifestyle].values[0]
            t[lifestyle] += weight
            
        elif lifestyle == "Chronic":
            t[lifestyle] += 1
            
        countert[lifestyle] += 1
    #print(t)
    label=""
    if t["Chronic"] > 0:
        label = 'Chronic'
    else:
        if t["Temperate"] == t["Virulent"]:
            #print("same")
            label = "Undecide"
        elif t["Temperate"] > t["Virulent"]:
            label = 'Temperate'
        elif t["Temperate"] < t["Virulent"]:
            label = 'Virulent'
    common.append(label)
    #print(t)
    #print(countert)
    #print(label)
ldf["final_replication_cycle"] = common
ldf.to_csv(inputf)
