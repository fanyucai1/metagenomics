import os
import re
import subprocess
import sys
import argparse

docker_name="mngs:latest"
parser=argparse.ArgumentParser("")
parser.add_argument("-m","--metaphlan",required=True,help="metaphlan output")
parser.add_argument("-o","--outdir",default=os.getcwd(),help="output directory")
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
args=parser.parse_args()

args.outdir=os.path.abspath(args.outdir)
args.metaphlan=os.path.abspath(args.metaphlan)
if not os.path.exists(args.outdir):
    subprocess.check_call("mkdir -p %s"%(args.outdir),shell=True)

infile=open(args.metaphlan,"r")
outfile=open("%s/%s.metaphaln2krona.txt","w")
for line in infile:
    line=line.strip()
    if line.startswith("#clade_name"):

infile.close()
outfile.close()
cmd="docker run -v %s:/raw_data/ -v %s:/outdir/ %s "%(os.path.dirname(args.metaphlan),args.outdir,docker_name)
