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

################
## default #####

script_dir = str(os.path.dirname(os.path.abspath(__file__)))
wkdir = str(os.getcwd())

anno = argparse.ArgumentParser(description="Replication cycle prediction for phage. current support: replidec, phact, bacphlip, phageAI, deephage. Usage: python RepliPhage.py -i test.faa -r -p -b -a -d")
anno.add_argument('--version', action='version', version='RepliPhage v1.1')

##require
anno.add_argument('-i', type=str, required=True, help='input file, two cloumn. sample\tseqence_path. tab sepearte.')

##optional
anno.add_argument('-o', type=str, default="./RepliPhage",
                  help="path to deposit output folder and temporary files, will create if doesn't exist [default= working directory]")
anno.add_argument('-t', type=int, default='3',
                  help='thread number used in each software')
#anno.add_argument('-virome', action='store_true',
#                  help='use this setting if dataset is known to be comprised mainly of viruses. More sensitive to viruses, less sensitive to false identifications [default=off]')
#anno.add_argument('-no_plot', action='store_true',
#                  help='suppress the generation of summary plots [default=off]')

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

#anno.add_argument('-v', '--vog',action='store_true',dest="vog",default=False, help="run vog")
#anno.add_argument('-vc', '--vogC',type=float, default="1e-5", dest="vc", help="vogdb creteria. discard the not meet this creteria")
#anno.add_argument('-vf', '--vogF',action='store_true',dest="vf",default=False, help="force rerun vog")
#
#anno.add_argument('-p', '--pfam',action='store_true',dest="pfam",default=False, help="run pfam")
#anno.add_argument('-pc', '--pfamC',type=float, default="1e-5", dest="pc", help="pfam creteria. discard the not meet this creteria")
#anno.add_argument('-pf', '--pfamF',action='store_true',dest="pf",default=False, help="force rerun pfam")
#
#anno.add_argument('-r', '--phrog',action='store_true',dest="phrog",default=False, help="run phrog")
#anno.add_argument('-rc', '--phrogC',type=float, default="1e-5", dest="rc", help="phrog creteria. discard the not meet this creteria")
#anno.add_argument('-rf', '--phrogF',action='store_true',dest="rf",default=False, help="force rerun phrog")
#
#anno.add_argument('-u', '--uniprot',action='store_true',dest="uniprot",default=False, help="run uniprot(default swiss-prot)")
#anno.add_argument('-ud', '--uniprotDB',choices=['sprot', 'trembl', 'all'],default="sprot", help="run uniprot using sprot(swiss-prot); trembl  or all (sprot+trembl)")
#anno.add_argument('-uc', '--uniprotC',type=float, default="1e-5", dest="uc", help="uniprot creteria. discard the not meet this creteria")
#anno.add_argument('-uf', '--uniprotF',action='store_true',dest="uf",default=False, help="force rerun uniprot")
#
#anno.add_argument('-b', '--pdb',action='store_true',dest="pdb",default=False, help="run pdb")
#anno.add_argument('-bc', '--pdbC',type=float, default="1e-5", dest="bc", help="pdb creteria. discard the not meet this creteria")
#anno.add_argument('-bf', '--pdbF',action='store_true',dest="bf",default=False, help="force rerun pdb")

#anno.add_argument('-l',type=str, nargs=1, default='1000',
#                  help='length in basepairs to limit input sequences [default=1000, can increase but not decrease]')
#anno.add_argument('-m', type=str, nargs=1, default=str(vibrant_path) + '/files/',
#                  help='path to original "files" directory that contains .tsv and model files (if moved from default location)')


args = anno.parse_args()
thread=args.t
input_list=args.i
outputD = args.o
print("Results will be store at %s"%outputD)

## perpare the dir
if not os.path.exists(str(outputD)):
    Popen('mkdir -P ' + str(outputD) + ' 2>/dev/null', shell=True)

## check script file and related file
replidec_src=os.path.join(script_dir,"src/run_Replidec.sh")

deephage_src=os.path.join(script_dir,"src/run_Deephage.sh")
deephage_source_code=os.path.join(script_dir,"resoruces/Deephage")

#pfam_db=os.path.join(databases,"Pfam-A.hmm")
#vog_db=os.path.join(databases,"VOGDB_phage.HMM")
#phrog_db=os.path.join(databases,"all_phrogs.hmm")
#phrog_db_anno=os.path.join(databases,"phrog_annot.tsv")
#
#if args.uniprotDB == "sprot":
#    uniprot_db=os.path.join(databases,"uniprot_sprot.fasta")
#elif args.uniprotDB == "trembl":
#    uniprot_db=os.path.join(databases,"uniprot_trembl.fasta")
#elif args.uniprotDB == "all":
#    uniprot_db=os.path.join(databases,"uniprot_trembl_sprot.merge.fasta")
#else:
#    print("Wrong parameter")
#
#pdb_db=os.path.join(databases,"pdb_seqres.txt")
#pdb_db_anno=os.path.join(databases,"pdb_seqres.header.anno.txt")
#
#
#def checkdb(db_file):
#    if not os.path.exists(db_file):
#        print("check %s! this file is not exist!"%db_file)
#        exit()
#    else:
#        logging.info("using db_file: %s"%db_file)
#
#checkdb(kegg_db)
#checkdb(pfam_db)
#checkdb(vog_db)
#checkdb(phrog_db)
#checkdb(pdb_db)





##########################
#### Function ############
##########################


def oneStepRun(inputfile, prefix, wd, db, outD, src, otherPara="", force=False):
    print("###### %s begin ######"%prefix)
    print("###### %s force:"%prefix,force)

    if prefix == "replidec":
        outPath = "%s/%s.%s.opt.tsv" % (wd,prefix, db)

        if not os.path.exists(outPath) or force:
            replidec_cmd="sh {src} {inputf} {wd} {summary} {db} '{para}' 2>&1 >replidec.log".format(
                    src=src, inputf=inputfile, wd=wd, summary="%s.%s.opt.tsv"%(prefix,db),
                    db=db, para=otherPara)
            print(replidec_cmd)
            obj=Popen(replidec_cmd, shell=True)
            obj.wait()
        else:
            print("###### Skip %s the running part, cause output file found!"%prefix)
    
    elif prefix == "deephage":
        outPath = "%s/%s.opt.tsv" % (wd,prefix) 

        if not os.path.exists(outPath) or force:
            deephage_cmd="sh {src} {inputf} {wd} {summary} {db} '{para}' 2>&1 >deephage.log".format(
                    src=src, inputf=inputfile, wd=wd, summary="%s.opt.tsv"%(prefix),
                    db=db, para=otherPara)
            print(deephage_cmd)
            obj=Popen(deephage_cmd, shell=True)
            obj.wait()
        else:
            print("###### Skip %s the running part, cause output file found!"%prefix)


    #elif prefix == "phmmer":
    #    hmm_outPath = "%s/%s.phmmer.tblout" % (wd, prefix)
    #    dbseq = db
    #    if not os.path.exists(hmm_outPath) or force:
    #        hmm_outPath = runPhmmer(inputfile, prefix, wd, dbseq, otherPara="-T 40 --cpu 1")
    #    else:
    #        print("Skip %s the running part, cause output file found!"%prefix)
    #    annoD = load_hmmsearch_opt(hmm_outPath, creteria=1e-5, reverse=True)
    outD[prefix] = os.path.realpath(outPath)
    print("###### %s end ######"%prefix)

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
    #runHmmsearch(input_faa, "kegg", keggOptD, kegg_db, otherPara="-T 40 --cpu %s"%(thread))

############################  Run DeePhage  ##########################
if args.deephage:
    sleep(1)
    deephageOptD=os.path.join(outputD,"deephage")
    argsL = [input_list, "deephage", deephageOptD, deephage_source_code, outD]
    kwargsD = {"otherPara":"",
                "force":args.deephageF,
                "src":deephage_src}

    deephaget = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
    deephaget.start()
    #runHmmsearch(input_faa, "vog", vogOptD, vog_db, otherPara="-T 40 --cpu %s"%(thread))


############################  Run/Parse pfam hmmsearch ##########################
#if args.pfam:
#    pfamOptD=os.path.join(outputD,"pfam")
#    argsL = [input_faa, "pfam", pfamOptD, pfam_db, outD]
#    kwargsD = {"otherPara":"-T 40 --cpu %s"%(thread),
#                "creteria":args.pc,
#                "force":args.pf,
#                "program":"hmmsearch"}
#
#    pfamt = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
#    pfamt.start()
#    #runHmmsearch(input_faa, "pfam", pfamOptD, pfam_db, otherPara="-T 40 --cpu %s"%(thread))
#
############################  Run/Parse PHROG hmmsearch ##########################
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
############################  Run/Parse Uniprot(Swiss-prot) phmmer ##########################
#if args.uniprot:
#    uniprotOptD=os.path.join(outputD,"uniprot")
#    argsL = [input_faa, "uniprot", uniprotOptD, uniprot_db, outD]
#    kwargsD = {"otherPara":"-T 40 --cpu %s"%(thread),
#                "creteria":args.uc,
#                "force":args.uf,
#                "program":"phmmer"}
#    uniprott = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
#    uniprott.start()
#
############################  Run/Parse Uniprot(Swiss-prot) phmmer ##########################
#if args.pdb:
#    pdbOptD=os.path.join(outputD,"pdb")
#    argsL = [input_faa, "pdb", pdbOptD, pdb_db, outD]
#    kwargsD = {"otherPara":"-T 40 --cpu %s"%(thread),
#               "creteria":args.bc,
#               "force":args.bf,
#               "program":"phmmer"}
#    pdbt = Thread(target=oneStepRun,args=argsL, kwargs=kwargsD)
#    pdbt.start()
#
############################
##### fetch result #########
############################
if args.replidec:
    replidect.join()

if args.deephage:
    deephaget.join()
#
#if args.pfam:
#    pfamt.join()
#
#if args.phrog:
#    phrogt.join()
#
#if args.uniprot:
#    uniprott.join()
#
#if args.pdb:
#    pdbt.join()
#
print(outD)

#summaryFile = os.path.join(outputD,"Vanno_summary.tsv")
#fmt_outD = split_dict_for_pandas(outD)
#res_df = pd.DataFrame.from_dict(fmt_outD)
#res_df = res_df.fillna("NA")
#print(res_df)
#
### add phrog annotation
#if args.phrog:
#    phrog_db_anno_df = pd.read_csv(phrog_db_anno,sep="\t",names=["phrog_ori","color","phrog_annot","phrog_category"])
#    phrog_db_anno_df["phrogID"] = ["phrog_%s"%i for i in phrog_db_anno_df.phrog_ori]
#    phrog_db_anno_df_sub = phrog_db_anno_df.loc[:,["phrog_annot","phrog_category","phrogID"]]
#    res_df = res_df.reset_index().merge(phrog_db_anno_df_sub,left_on="phrog_des",right_on="phrogID",how="left")
#
### add pdb annotation
#if args.pdb:
#    pdb_db_anno_df = pd.read_csv(pdb_db_anno,sep="\t",names=["pdb_id","pdb_annot"])
#    res_df = res_df.merge(pdb_db_anno_df,left_on="pdb_des",right_on="pdb_id",how="left")
#
### select coloumn to save
#res_df.to_csv(summaryFile,index=True,sep="\t")
#

