import os
import subprocess
import argparse

docker_name="mngs:latest"
parser=argparse.ArgumentParser("Quality control")
parser.add_argument("-p1","--pe1",help="5' reads",required=True)
parser.add_argument("-p2","--pe2",help="3' reads",required=True)
parser.add_argument("-o","--outdir",help="output directory",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-a","--adpater",help="adapter fasta file",required=True)
args=parser.parse_args()

############prepare input##########################
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
args.adapter=os.path.abspath(args.adpater)
adapter_filename=args.adapter.split("/")[-1]
adapter_dir=os.path.dirname(args.adapter)
######################################
cmd="docker run -v %s:/raw_data/ -v %s:/reference/ -v %s:/outdir/ %s "%(in_dir,adapter_dir,args.outdir,docker_name)

#     remove adaptors
#     quality filtering of reads
#     removal of low-quality reads(q < 20)
#     removal of short reads ( < 36 bp)
#     deduplication for FASTQ data
cmd+="/software/fastp -i /raw_data/%s -I /raw_data/%s -o /outdir/%s.qc.R1.fq.gz" \
     " -O /outdir/%s.qc.R2.fq.gz --dedup --thread 16 --low_complexity_filter" \
     " --adapter_fasta /reference/%s --length_required 36 " \
     "--html /outdir/%s.qc.html" %(a,b,args.prefix,args.prefix,adapter_filename,args.prefix)

print(cmd)
subprocess.check_call(cmd,shell=True)