#!/project/genomics/xuePeng/software/python3.9.5/bin/python3.9
# coding: utf-8

import bacphlip
import os
import sys
import pandas as pd
from Bio import Seq,SeqIO
import shutil

def calculate(seqfile):
    n = 0
    for seq in SeqIO.parse(seqfile,"fasta"):
        n+=1
    return n

def mkdirs(dirname):
    '''
    makedirs
    '''
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def bacphlip_predict(seqfile,optdir,force_overwrite=True, local_hmmsearch="/home/viro/xue.peng/.linuxbrew/bin/hmmsearch"):
    if not os.path.exists(optdir):
        os.makedirs(optdir)

    path,target_file = os.path.split(seqfile)
    new_target_file_link = os.path.join(optdir,target_file)
    if not os.path.exists(new_target_file_link):
        os.symlink(seqfile,new_target_file_link)

    outputSuffix = ["6frame","bacphlip","hmmsearch","hmmsearch.tsv"]
    outputFile = "%s.%s"%(new_target_file_link,outputSuffix[1])
    if not os.path.exists(outputFile):
        print("calculate genome number")
        genome_number = calculate(seqfile)
        print("genome_number: %s"%genome_number)
        if genome_number > 1:
            bacphlip.run_pipeline_multi(new_target_file_link,force_overwrite, local_hmmsearch)
        else:
            bacphlip.run_pipeline(new_target_file_link,force_overwrite, local_hmmsearch)


    d = pd.read_csv(outputFile,header = 0,sep = "\t")
    lstype = "Temperate"
    possibility = "%s|%s"%(d.Virulent[0],d.Temperate[0])
    if d.Virulent[0] > d.Temperate[0]:
        lstype = "Virulent"
    print(target_file,possibility,lstype)
    #os.remove(new_target_file_link)
    return [target_file,possibility,lstype]


def batch_bacphlip_predict(seqfileList,optdir,force_overwrite=True, local_hmmsearch="/home/viro/xue.peng/.linuxbrew/bin/hmmsearch"):
    mkdirs(optdir)
    opt = open("%s.bacphlip_report.txt"%optdir,"w")
    opt.flush()
    opt.write("sampleID\tbacphlip_ressult\tVirulent|Temperate_score\tfilePath\n")
    n=0
    with open(seqfileList) as f:
        for line in f:
            n+=1
            sample, line = line.strip("\n").split('\t')
            line = os.path.realpath(line)
            path,target_file = os.path.split(line)
            target_file,possibility,lstype = [target_file,"NA|NA","NA"]
            try:
                target_file,possibility,lstype = bacphlip_predict(line,optdir,force_overwrite, local_hmmsearch)
            except Exception as e:
                print("warning: %s is not work: %s"%(line,e))
            opt.write("\t".join([sample,lstype,possibility,line])+"\n")

            if n == 50:
                opt.flush()
                n = 0
    opt.close()

if __name__ == "__main__":
    inputlist = sys.argv[1]
    #input is file contain two coloumn sample\tpath
    optdir = sys.argv[2]
    hmmer_path=shutil.which("hmmsearch")
    batch_bacphlip_predict(inputlist,optdir, force_overwrite=True,
    local_hmmsearch=hmmer_path)
#infile = "/home/viro/xue,.peng/workplace_2021/lifestyle_predict_my/test/lifestyle_phageai/test/RF_V__s_Aalivirus_A__NC_023985.1.fasta"
#possibility,lstype = bacphlip_predict(infile,"/home/viro/xue.peng/workplace_2021/lifestyle_predict_my/test/")
#print(possibility,lstype)
