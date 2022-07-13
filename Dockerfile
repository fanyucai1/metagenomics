FROM fanyucai1/biobase:latest
COPY *.gz /software/
COPY *.zip /software/
COPY *bz2 /software/
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
COPY diamond_0.8.36 /bin/
COPY prodigal_v2.6.3 /bin/
COPY jellyfish_v2.2.10 /bin/
RUN sh /software/run.sh
COPY Python-3.10.5.tgz /software/python3
RUN cd /software/python3 && tar xvf Python-3.10.5.tgz && cd Python-3.10.5 && ./configure --prefix=/software/python3/Python-v3.10.5 --with-openssl=/usr/local/openssl && make -j20 && make install
RUN /software/python3/Python-v3.7.0/bin/python3.7 -m pip install --upgrade pip
RUN /software/python3/Python-v3.7.0/bin/pip3 install numpy==1.21.0 metaphlan
COPY rgi-5.2.1.tar /software/
RUN cd /software/ && tar xvf rgi-5.2.1.tar && cd rgi-5.2.1 && /software/python3/Python-v3.7.0/bin/python3 setup.py install
RUN /software/python3/Python-v3.7.0/bin/pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple cgelib pandas tabulate