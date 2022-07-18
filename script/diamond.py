import os
import sys
import subprocess
import argparse

docker_name="mngs:latest"
parser=argparse.ArgumentParser("Use Diamond mapping the database to classify.")
parser.add_argument("-p1","--pe1",help="5 reads",required=True)
parser.add_argument("-p2","--pe2",help="3 reads",required=True)
parser.add_argument("-o","--outdir",help="output directory",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-r","--reference",help="reference index",required=True)
args=parser.parse_args()

##step1:prepare input
args.pe1=os.path.abspath(args.pe1)
args.pe2 = os.path.abspath(args.pe2)
in_dir=os.path.dirname(args.pe1)
if in_dir!=os.path.dirname(args.pe2):
    print("read1 and reads2 must be in the same directory.")
    exit()
a=args.pe1.split("/")[-1]
b=args.pe2.split("/")[-1]
args.outdir=os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
    subprocess.check_call('mkdir -p %s'%(args.outdir),shell=True)
reference_dir=os.path.abspath(args.reference)

#step2:use fastp merge pe1 and pe2
cmd="docker run -v %s:/raw_data/ -v %s:/outdir/ %s "%(in_dir,args.outdir,docker_name)
cmd+="sh -c \"fastp -i /raw_data/%s -I /raw_data/%s -m /outdir/%s.merger.fastq\""%(a,b,args.prefix)
subprocess.check_call(cmd,shell=True)

#step3:diamond mapping to FDA-ARGOS(https://www.ncbi.nlm.nih.gov/bioproject/231221)
# contains Protein Sequences 5210460
# 2022/07/14

cmd="docker run -v %s:/outdir/ -v %s:/reference/ %s "%(args.outdir,reference_dir,docker_name)
cmd+="diamond -q /outdir/%s.merger.fastq --threads 24 --db /reference/ --out --outfmt"
subprocess.check_call(cmd,shell=True)