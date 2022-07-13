usr guide
+++++++++++++++++++++++++++++++++++++

step1:prepare database
-------------------

metaphlan ::

    #http://cmprod1.cibio.unitn.it/biobakery3/metaphlan_databases/
    mkdir -p reference/metaphlan
    cd reference/metaphlan
    wget http://cmprod1.cibio.unitn.it/biobakery3/metaphlan_databases/mpa_v31_CHOCOPhlAn_201901.tar
    tar xvf mpa_v31_CHOCOPhlAn_201901.tar
    bunzip2 mpa_v31_CHOCOPhlAn_201901.fna.bz2
    bowtie2-build mpa_v31_CHOCOPhlAn_201901.fna
    wget http://cmprod1.cibio.unitn.it/biobakery3/metaphlan_databases/mpa_v31_CHOCOPhlAn_201901_marker_info.txt.bz2
    bunzip2 mpa_v31_CHOCOPhlAn_201901_marker_info.txt.bz2

CARD   ::

    #https://github.com/arpcard/rgi#load-card-reference-data
    mkdir -p reference/CARD
    cd reference/metaphlan
    wget https://card.mcmaster.ca/latest/data
    tar -xvf data card.json
    rgi load --card_json card.json --local
    rgi card_annotation -i card.json
    rgi load -i card.json --card_annotation card_database_v3.0.1.fasta --local
    wget -O wildcard_data.tar.bz2 https://card.mcmaster.ca/latest/variants
    mkdir -p wildcard
    tar -xjf wildcard_data.tar.bz2 -C wildcard
    gunzip wildcard/*.gz
    rgi wildcard_annotation -i wildcard --card_json card.json -v version_number
    rgi load --wildcard_annotation wildcard_database_v3.0.2.fasta --wildcard_index /path/to/wildcard/index-for-model-sequences.txt --card_annotation card_database_v3.0.1.fasta --local

kraken2 ::

    mkdir -p reference/kraken2
    cd reference/kraken2
    wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20220607.tar.gz

phinx ::

    https://www.ncbi.nlm.nih.gov/nuccore/NC_001422
    mkdir -p reference/phix_index
    cd reference/phix_index
    bowtie-build NC_001422.fasta

adapter ::

    mkdir -p adpater/
    ./
    ├── NexteraPE-PE.fa
    ├── TruSeq2-PE.fa
    ├── TruSeq2-SE.fa
    ├── TruSeq3-PE-2.fa
    ├── TruSeq3-PE.fa
    └── TruSeq3-SE.fa
    Download files from Trimmomatic(http://www.usadellab.org/cms/index.php?page=trimmomatic)

step2:software
----------------------------
docker pull fanyucai1/mngs:latest



step3:script
-----------------------------

QC_fastp.py
=========================
::

    remove adaptors
    quality filtering of reads
    removal of low-quality reads(q < 20)
    removal of short reads ( < 36 bp)
    deduplication for FASTQ data

    usage: Quality control [-h] -p1 PE1 -p2 PE2 -o OUTDIR -p PREFIX -a ADPATER

    optional arguments:
      -h, --help            show this help message and exit
      -p1 PE1, --pe1 PE1    5' reads
      -p2 PE2, --pe2 PE2    3' reads
      -o OUTDIR, --outdir OUTDIR
                            output directory
      -p PREFIX, --prefix PREFIX
                            prefix of output
      -a ADPATER, --adpater ADPATER
                            adapter fasta file
filter_host.py
=========================
::

    usage: Filter human host and phix sequence. [-h] -p1 PE1 -p2 PE2 -i INDEX -o OUTDIR -p PREFIX

    optional arguments:
      -h, --help            show this help message and exit
      -p1 PE1, --pe1 PE1    5' reads
      -p2 PE2, --pe2 PE2    3' reads
      -i INDEX, --index INDEX
                            directory contains bowtie2 index
      -o OUTDIR, --outdir OUTDIR
                            output directory
      -p PREFIX, --prefix PREFIX
                            prefix of output

downsize.py
=========================
::

    usage: Use seqtk downsizing the samples. [-h] -p1 PE1 -p2 PE2 -o OUTDIR [-n NUMBER] -p PREFIX

    optional arguments:
      -h, --help            show this help message and exit
      -p1 PE1, --pe1 PE1    5' reads
      -p2 PE2, --pe2 PE2    3' reads
      -o OUTDIR, --outdir OUTDIR
                            output directory
      -n NUMBER, --number NUMBER
                            the number sequence you want
      -p PREFIX, --prefix PREFIX
                            prefix of output


metaphlan.py
=========================
::

    usage: MetaPhlAn2 uses a database of clade-specific marker genes to classify. [-h] -p1 PE1 -p2 PE2 -i INDEX -o OUTDIR -p PREFIX

    optional arguments:
      -h, --help            show this help message and exit
      -p1 PE1, --pe1 PE1    5' reads
      -p2 PE2, --pe2 PE2    3' reads
      -i INDEX, --index INDEX
                            directory contains metaphlan index
      -o OUTDIR, --outdir OUTDIR
                            output directory
      -p PREFIX, --prefix PREFIX
                            prefix of output

kraken2.py
=========================
::

    usage: Classified out option on the miniKraken database, [-h] -p1 PE1 -p2 PE2 -i INDEX -o OUTDIR -p PREFIX

    optional arguments:
      -h, --help            show this help message and exit
      -p1 PE1, --pe1 PE1    5' reads
      -p2 PE2, --pe2 PE2    3' reads
      -i INDEX, --index INDEX
                            directory contains kraken2 index
      -o OUTDIR, --outdir OUTDIR
                            output directory
      -p PREFIX, --prefix PREFIX
                            prefix of output

metaspades.py
=========================
::

    usage: assemble genome using metaSPAdes. [-h] -p1 PE1 -p2 PE2 -o OUTDIR -p PREFIX

    optional arguments:
      -h, --help            show this help message and exit
      -p1 PE1, --pe1 PE1    5' reads
      -p2 PE2, --pe2 PE2    3' reads
      -o OUTDIR, --outdir OUTDIR
                            output directory
      -p PREFIX, --prefix PREFIX
                            prefix of output

CARD.py
=========================
::

    usage:
    Identify resistance genes.
     [-h] -p1 PE1 -p2 PE2 -o OUTDIR -r REFERENCE -p PREFIX

    optional arguments:
      -h, --help            show this help message and exit
      -p1 PE1, --pe1 PE1    5 reads
      -p2 PE2, --pe2 PE2    3 reads
      -o OUTDIR, --outdir OUTDIR
                            output directory
      -r REFERENCE, --reference REFERENCE
                            path database of ResFinder
      -p PREFIX, --prefix PREFIX
                            prefix of output

