#!/usr/bin/env python3

from subprocess import Popen
import argparse
import sys
import os
import re
from threading import Thread
from collections import defaultdict
import pandas as pd
from time import sleep

script_dir = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("%s/bin"%(script_dir))
from merged_all import parse_result
from get_final_label import final_lable 

 
wkdir = str(os.getcwd())

################
## default #####
################

anno = argparse.ArgumentParser(description="Replication cycle prediction for phage. current support: replidec, bacphlip, deephage, phabox. Usage: python ReplidecPlus.py -i input.txt -r -p -b -d")
anno.add_argument('--version', action='version', version='ReplidecPlus v1.1')

##require
anno.add_argument('-i', type=str, required=True, help='input file, two cloumn. sample\tseqence_path. tab sepearte.')

##optional
anno.add_argument('-o', type=str, default="./ReplidecPlus",
                  help="path to deposit output folder and temporary files, will create if doesn't exist [default= working directory]")
anno.add_argument('-t', type=int, default='3',
                  help='thread number used in each software')

##repliedc
anno.add_argument('-r', '--replidec',action='store_true',dest="replidec",default=False, help="run replidec")
anno.add_argument('-rd', '--replidec_db',type=str, dest="replidec_db",choices=["all","prokaryote"],
                  default='prokaryote', help="define replidec database")
anno.add_argument('-rp', '--replidec_parameter',type=str, dest="replidec_para",
                  default='-c 1e-5 -m 1e-5 -b 1e-6', help="define replidec parameter")
anno.add_argument('-rf', '--replidecF',action='store_true',dest="replidecF",default=False, help="force rerun replidec")

##Deephage
anno.add_argument('-d', '--deephage',action='store_true',dest="deephage",default=False, help="run deephage")
anno.add_argument('-df', '--deephageF',action='store_true',dest="deephageF",default=False, help="force rerun deephage")

##BACPHLIP
anno.add_argument('-b', '--bacphlip',action='store_true',dest="bacphlip",default=False, help="run bacphlip")
anno.add_argument('-bf', '--bacphlipF',action='store_true',dest="bacphlipF",default=False, help="force rerun bacphlipF")

##PhaBOX_PhaTYP
anno.add_argument('-p', '--phabox',action='store_true',dest="phabox",default=False, help="run phaTYP from PhaBOX")
anno.add_argument('-pp', '--phabox_parameter',type=str, dest="phabox_para",
                  default='--task phatyp --threads 8 --len 3000', help="define phabox parameter")
anno.add_argument('-pf', '--phaboxF',action='store_true',dest="phaboxF",default=False, help="force rerun phaTYP")

##PHACTS
anno.add_argument('-c', '--phacts',action='store_true',dest="phacts",default=False, help="run phacts")
anno.add_argument('-cf', '--phactsF',action='store_true',dest="phactsF",default=False, help="force rerun phacts")
# #


args = anno.parse_args()
thread=args.t
input_list=args.i
outputD = args.o
print("Results will be store at %s"%outputD)

## perpare the dir
if not os.path.exists(str(outputD)):
    Popen('mkdir -p ' + str(outputD) + ' 2>/dev/null', shell=True)


###############
### set script
###############
## check script file and related file
##replidec
replidec_src=os.path.join(script_dir,"src/run_Replidec.sh")

##deephage
deephage_src=os.path.join(script_dir,"src/run_Deephage_v2.sh")
#deephage_src=os.path.join(script_dir,"src/run_Deephage.sh")
deephage_source_code=os.path.join(script_dir,"resources/DeePhage")

##bacphlip
bacphlip_src=os.path.join(script_dir,"src/run_bacphlip.sh")

##phagebox
##v2 is merged seq then predict, ori file is to predict each of them; and suit for phabox v2
phabox_src=os.path.join(script_dir,"src/run_phabox_v2.sh")
phabox_source_code=os.path.join(script_dir,"resources/PhaBOX/phabox_db_v2")

##phacts
phacts_src=os.path.join(script_dir,"src/run_phacts.sh")


##########################
#### Function ############
##########################
def create_dir(dir_path):
    if not os.path.exists(str(dir_path)):
        print("mkdir %s"%dir_path)
        obj=Popen('mkdir -p ' + str(dir_path) + ' 2>/dev/null', shell=True)
        obj.wait()

def oneStepRun(inputfile, prefix, wd, db, outD, src, otherPara="", force=False):
    print("###### %s begin ######"%prefix)
    print("%s force:"%prefix,force)

     
    create_dir(wd)
    ##### replidec ########
    if prefix == "replidec":
        outPath = "%s/%s.%s.opt.tsv" % (wd,prefix, db)
        
        if not os.path.exists(outPath) or force:
            replidec_cmd="sh {src} {inputf} {wd} {summary} {db} '{para}' 2>&1 >{wd}/RP_replidec.log".format(
                    src=src, inputf=inputfile, wd=wd, summary="%s.%s.opt.tsv"%(prefix,db),
                    db=db, para=otherPara)
            print(replidec_cmd)
            obj=Popen(replidec_cmd, shell=True)
            obj.wait()
        else:
            print("Skip %s the running part, cause output file found!"%prefix)
    
    ##### deephage ########
    elif prefix == "deephage":
        outPath = "%s/%s.opt.tsv" % (wd,prefix) 

        if not os.path.exists(outPath) or force:
            deephage_cmd="sh {src} {inputf} {wd} {summary} {db} '{para}' 2>&1 >{wd}/RP_deephage.log".format(
                    src=src, inputf=inputfile, wd=wd, summary="%s.opt.tsv"%(prefix),
                    db=db, para=otherPara)
            print(deephage_cmd)
            obj=Popen(deephage_cmd, shell=True)
            obj.wait()
        else:
            print("Skip %s the running part, cause output file found!"%prefix)

    ##### bacphlip ########
    elif prefix == "bacphlip":
        outPath = "%s/bacphlip_report.txt" % (wd)

        if not os.path.exists(outPath) or force:
            bacphlip_cmd="sh {src} {inputf} {wd} {summary} {db} '{para}' 2>&1 >{wd}/RP_bacphlip.log".format(
                    src=src, inputf=inputfile, wd=wd, summary="%s.opt.tsv"%(prefix),
                    db=db, para=otherPara)
            print(bacphlip_cmd)
            obj=Popen(bacphlip_cmd, shell=True)
            obj.wait()
        else:
            print("Skip %s the running part, cause output file found!"%prefix)

    ##### phabox ########
    elif prefix == "phabox":
        outPath = "%s/%s.opt.tsv" % (wd,prefix)

        if not os.path.exists(outPath) or force:
            phabox_cmd="sh {src} {inputf} {wd} {summary} {db} '{para}' 2>&1 >{wd}/RP_phabox.log".format(
                    src=src, inputf=inputfile, wd=wd, summary="%s.opt.tsv"%(prefix),
                    db=db, para=otherPara)
            print(phabox_cmd)
            obj=Popen(phabox_cmd, shell=True)
            obj.wait()
        else:
            print("Skip %s the running part, cause output file found!"%prefix)

    ##### phacts ########
    if prefix == "phacts":
        outPath = "%s/%s.opt.tsv" % (wd,prefix)

        if not os.path.exists(outPath) or force:
            phacts_cmd="sh {src} {inputf} {wd} {summary} {db} '{para}' 2>&1 >{wd}/RP_phacts.log".format(
                    src=src, inputf=inputfile, wd=wd, summary="%s.opt.tsv"%(prefix),
                    db=db, para=otherPara)
            print(phacts_cmd)
            obj=Popen(phacts_cmd, shell=True)
            obj.wait()
        else:
            print("Skip %s the running part, cause output file found!"%prefix)

    #elif prefix == "phmmer":
    #    hmm_outPath = "%s/%s.phmmer.tblout" % (wd, prefix)
    #    dbseq = db
    #    if not os.path.exists(hmm_outPath) or force:
    #        hmm_outPath = runPhmmer(inputfile, prefix, wd, dbseq, otherPara="-T 40 --cpu 1")
    #    else:
    #        print("Skip %s the running part, cause output file found!"%prefix)
    #    annoD = load_hmmsearch_opt(hmm_outPath, creteria=1e-5, reverse=True)
    outD[prefix] = os.path.realpath(outPath)
    print("###### %s end ######\n"%prefix)

def split_dict_for_pandas(indict):
    outd = defaultdict(dict)
    for db,annos in indict.items():
        for query, values in annos.items():
            for accession,name in values.items():
                #print(db,query,name)

                des = "%s_des"%db
                acc = "%s_acc"%db
                outd[des][query]= name
                outd[acc][query]= accession
    return outd

###########################
#### main Programe ########
###########################

outD = {}
###########################  Run Replidec  #########################
if args.replidec:
    replidecOptD=os.path.join(outputD,"replidec")
    argsL = [input_list, "replidec", replidecOptD, args.replidec_db, outD]
    kwargsD = {"otherPara":"%s -t %s"%(args.replidec_para,thread),
                "force":args.replidecF,
                'src':replidec_src}
    
    replidect = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
    replidect.start()

############################  Run DeePhage  ##########################
if args.deephage:
    sleep(0.5)
    deephageOptD=os.path.join(outputD,"deephage")
    argsL = [input_list, "deephage", deephageOptD, deephage_source_code, outD]
    kwargsD = {"otherPara":"",
                "force":args.deephageF,
                "src":deephage_src}

    deephaget = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
    deephaget.start()

############################  Run BACPHLIP ##########################
if args.bacphlip:
    sleep(1)
    bacphlipOptD=os.path.join(outputD,"bacphlip")
    argsL = [input_list, "bacphlip", bacphlipOptD, "", outD]
    kwargsD = {"otherPara":"",
                "force":args.bacphlipF,
                "src":bacphlip_src}

    bacphlipt = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
    bacphlipt.start()

############################  Run PhaBOX  ##########################
if args.phabox:
    sleep(1.5)
    phaboxOptD=os.path.join(outputD,"phabox")
    argsL = [input_list, "phabox", phaboxOptD, phabox_source_code, outD]
    kwargsD = {"otherPara":"%s --threads %s"%(args.phabox_para,thread),
                "force":args.phaboxF,
                "src":phabox_src}

    phaboxt = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
    phaboxt.start()

############################  Run PHACTS  ##########################
#if args.phacts:
#    sleep(2)
#    phactsOptD=os.path.join(outputD,"phacts")
#    argsL = [input_list, "phacts", phactsOptD, "", outD]
#    kwargsD = {"otherPara":"",
#                "force":args.phactsF,
#                "src":phacts_src}
#
#    phactst = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
#    phactst.start()

###########################  Run/Parse PHROG hmmsearih ##########################
#if args.phrog:
#    phrogOptD=os.path.join(outputD,"phrog")
#    argsL = [input_faa, "phrog", phrogOptD, phrog_db, outD]
#    kwargsD = {"otherPara":"-T 40 --cpu %s"%(thread),
#                "creteria":args.rc,
#                "force":args.rf,
#                "program":"hmmsearch"}
#    phrogt = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
#    phrogt.start()
#
############################
##### fetch result #########
############################
if args.replidec:
    replidect.join()

if args.deephage:
    deephaget.join()

if args.bacphlip:
    bacphlipt.join()

if args.phabox:
    phaboxt.join()

#if args.phacts:
#    phactst.join()

#if args.pdb:
#    pdbt.join()
#
#print(outD)

###############
## merge 
###############
sleep(2)
print("Merge all the output, please wait.")
output_summary=os.path.join(outputD,"ReplidecPlus.summary.detail.txt")
parse_result(input_list,outD,output_summary)

## generate the final
final_summary=os.path.join(outputD,"ReplidecPlus.summary.final.txt")
final_lable(output_summary,final_summary)

