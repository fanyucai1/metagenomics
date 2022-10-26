FROM fanyucai1/biobase:latest
COPY *.gz /software/
COPY *.zip /software/
COPY *bz2 /software/
COPY *.tar /software/
COPY *.tgz /software/
RUN cd /software/ && tar xzvf MEGAHIT-1.2.9-Linux-x86_64-static.tar.gz
RUN mkdir -p /script/ && mkdir -p /raw_data/ && mkdir -p /reference/ && mkdir -p /outdir/
RUN cd /software/ && tar xjvf bwa-0.7.17.tar.bz2 && cd bwa-0.7.17 && make && ln -s /software/bwa-0.7.17/bwa /usr/bin/bwa
RUN cd /software/ && tar xjvf samtools-1.15.1.tar.bz2 && cd samtools-1.15.1 && ./configure && make && make install
RUN cd /software/ && tar xzvf prinseq-lite-0.20.4.tar.gz
RUN cd /software/ && tar xzvf kraken2-2.1.2.tar.gz && cd kraken2-2.1.2/ && sh install_kraken2.sh /software/kraken2-2.1.2/
RUN cd /software/ && unzip bowtie2-2.4.5-linux-x86_64.zip
RUN cd /software/ && unzip seqtk-master.zip && cd seqtk-master && make
RUN cd /software/ && unzip Trimmomatic-0.39.zip
RUN cd /software/ && tar xzvf SPAdes-3.15.4-Linux.tar.gz
RUN cd /software/ && tar xzvf ncbi-blast-2.9.0+-x64-linux.tar.gz
RUN cd /software/ && tar xzvf bedtools-2.27.1.tar.gz && cd bedtools2 && make
RUN cd /software/ && tar xzvf kma-1.3.4.tar.gz && cd genomicepidemiology-kma-34dd939c90cd/ && make
COPY oligoarrayaux-3.8-1.x86_64.rpm /software/
RUN cd /software/ && rpm -ivh oligoarrayaux-3.8-1.x86_64.rpm
RUN cd /software/ && tar xzvf cmake-3.24.0-rc3-linux-x86_64.tar.gz
RUN cd /software && tar xzvf bamtools-2.5.1.tar.gz  && cd bamtools-2.5.1 && mkdir build
RUN cd /software/bamtools-2.5.1/build && /software/cmake-3.24.0-rc3-linux-x86_64/bin/cmake ../ && make install
COPY fastp /software/
COPY freebayes-1.3.6-linux-amd64-static /software/
COPY run.sh /software/
COPY diamond /bin/
COPY prodigal_v2.6.3 /bin/
COPY jellyfish_v2.2.10 /bin/
RUN sh /software/run.sh
RUN cd /software/ && tar xvf Python-3.10.5.tgz && cd Python-3.10.5 && ./configure --prefix=/software/python3/Python-v3.10.5 --with-openssl=/usr/local/openssl && make -j20 && make install
RUN yum install -y git
RUN /software/python3/Python-v3.7.0/bin/python3 -m pip install --upgrade pip
COPY rgi-6.0.0-requirements.txt /software/
RUN cd /software/ && /software/python3/Python-v3.7.0/bin/pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r rgi-6.0.0-requirements.txt
RUN cd /software/ && tar xvf rgi-6.0.0.tar && cd rgi-6.0.0 && /software/python3/Python-v3.7.0/bin/python3 setup.py install
RUN /software/python3/Python-v3.10.5/bin/python3.10 -m pip install --upgrade pip
RUN /software/python3/Python-v3.10.5/bin/pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple wheel tabulate biopython cgecore gitpython python-dateutil
RUN /software/python3/Python-v3.10.5/bin/pip3 install MetaPhlAn==4.0.2
RUN cd /software/ && git clone https://git@bitbucket.org/genomicepidemiology/resfinder.git
RUN cp /software/genomicepidemiology-kma-34dd939c90cd/kma /bin/
RUN cd /software/ && tar xvf KronaTools-2.8.1.tar && cd KronaTools-2.8.1 && perl install.pl
RUN cd /software/ && tar xzvf KrakenTools.v1.2.tar.gz
RUN cd /software/ && rm -rf *tar.gz *rpm *tar *bz2 *zip *gz run.sh /software/Python-3.10.5.tgz /software/Python-3.10.5 /software/python3/Python-3.7.0
