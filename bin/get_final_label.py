# coding: utf-8
import pandas as pd
from collections import Counter 
import sys
import os

# inputf = sys.argv[1]
# outputf = sys.argv[2]

def final_lable(inputf,outputf):

    ## load weights for each software
    script_dir = str(os.path.dirname(os.path.abspath(__file__)))
    load_weights=pd.read_csv("%s/weights.allsft.list"%script_dir, index_col=0)
    
    ## load pre results 
    ldf = pd.read_csv(inputf)
    
    common=[]
    weightL=[]
    for row in ldf.index:
        t = {"Temperate":0,
             "Virulent": 0,
             "Chronic": 0}
        countert = Counter()
        for col in ["deephage_final","phabox_final","bacphlip_label","replidec_final"]:
            if col in ldf.columns:
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
        weightL.append("%s|%s"%(t["Temperate"],t["Virulent"]))
        #print(t)
        #print(countert)
        #print(label)
    ldf["final_replication_cycle"] = common
    ldf["weight_T|V"] = weightL
    ldf.loc[:,["sample_name","final_replication_cycle","weight_T|V"]].to_csv(outputf)
    print("!! SUMMARY FINAL RESULT: store at %s"%outputf)


if __name__=="__main__":
    final_lable("/Users/pengxue/notneed4icolud/PROJECT/lifestyle_v2/v6/v6_testD3/IBD.merged.RepliPhage.summary.txt","summary.txt")
