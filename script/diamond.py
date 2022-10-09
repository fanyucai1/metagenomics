import os
import subprocess
import argparse

docker_diamond="mngs:latest"
docker_megan="megan6:latest"

parser=argparse.ArgumentParser("Use Diamond mapping the database to classify.")
parser.add_argument("-p1","--pe1",help="5 reads",required=True)
parser.add_argument("-p2","--pe2",help="3 reads",required=True)
parser.add_argument("-o","--outdir",help="output directory",required=True)
parser.add_argument("-p","--prefix",help="prefix of output",required=True)
parser.add_argument("-d","--diamond",help="diamond database file **.dmnd",required=True)
parser.add_argument("-m","--mapping_file",help= "megan6 mapping file.",required=True)
args=parser.parse_args()

##step1:prepare input
args.pe1=os.path.abspath(args.pe1)
args.pe2 = os.path.abspath(args.pe2)
args.diamond=os.path.abspath(args.diamond)
args.mapping_file=os.path.abspath(args.mapping_file)
args.outdir=os.path.abspath(args.outdir)
if not os.path.exists(args.outdir):
    subprocess.check_call('mkdir -p %s'%(args.outdir),shell=True)

#step2:use fastp merge pe1 and pe2
if args.pe1.endswith(".gz") and args.pe2.endswith(".gz"):
    subprocess.check_call("zcat %s %s >%s/%s.merge.fastq" % (args.pe1, args.pe2, args.outdir, args.prefix), shell=True)
else:
    subprocess.check_call("cat %s %s >%s/%s.merge.fastq"%(args.pe1,args.pe2,args.outdir,args.prefix),shell=True)

#step3:diamond mapping to database
cmd="docker run -v %s:/outdir/ -v %s:/reference/ %s "%(args.outdir,os.path.dirname(args.diamond),docker_diamond)
cmd+="diamond blastx -q /outdir/%s.merge.fastq --threads 24 --evalue 0.00001 --max-target-seqs 1 " \
     "--db /reference/%s " \
     "--out /outdir/%s.daa --outfmt 100"%(args.prefix,args.diamond.split("/")[-1].split(".dmnd")[0],args.prefix)
print(cmd)
subprocess.check_call(cmd,shell=True)
subprocess.check_call("rm -rf >%s/%s.merge.fastq"%(args.outdir,args.prefix),shell=True)

#step4:parse diamond output (daa file) to txt
cmd="docker run -v %s:/outdir/ -v %s:/reference/ %s "%(args.outdir,os.path.dirname(args.mapping_file),docker_megan)
cmd+="/opt/conda/bin/blast2lca -i /outdir/%s.daa -f DAA -m BlastX -mdb /reference/%s --output /outdir/%s.details.txt" \
     %(args.prefix,args.mapping_file.split("/")[-1],args.prefix)
print(cmd)
subprocess.check_call(cmd,shell=True)


