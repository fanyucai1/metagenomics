
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

human_phinx_index(host index) ::

    mkdir -p reference/human_phinx_index/
    # download phinx from NCBI
    https://www.ncbi.nlm.nih.gov/nuccore/NC_001422
    # download human genome sequence from gencode
    wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_41/GRCh38.p13.genome.fa.gz
    cd reference/human_phinx_index/
    cat GRCh38.p13.genome.fa.gz NC_001422.fasta >host.fasta
    bowtie2-build host.fasta host.fasta

adapter ::

    mkdir -p reference/adpater/
    ./
    ├── NexteraPE-PE.fa
    ├── TruSeq2-PE.fa
    ├── TruSeq2-SE.fa
    ├── TruSeq3-PE-2.fa
    ├── TruSeq3-PE.fa
    └── TruSeq3-SE.fa
    Download files from Trimmomatic(http://www.usadellab.org/cms/index.php?page=trimmomatic)

ResFinder ::

    mkdir reference/ResFinder
    cd reference/ResFinder
    git clone https://git@bitbucket.org/genomicepidemiology/resfinder_db.git
    python3 INSTALL.py

diamond ::

    wget https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz
    wget https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/swissprot.gz
    diamond makedb --in swissprot -d swissprot
    diamond makedb --in nr -d nr