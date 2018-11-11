# docker build -t ubuntu1604py36
FROM ubuntu:16.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \ 
    apt-get install -y software-properties-common vim build-essential google-perftools libbz2-dev libxml2-dev libjemalloc-dev openssl libcurl4-openssl-dev libssl-dev libtbb-dev libarmadillo-dev libgsl-dev git maven openjdk-8-jdk libboost-program-options-dev bzip2 ca-certificates curl wget zip unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#install cmake
RUN mkdir -p /tmp/cmake_build && cd /tmp/cmake_build && wget https://cmake.org/files/v3.12/cmake-3.12.4.tar.gz && tar xf cmake*.tar.gz && cd cmake* && ./bootstrap && make && make install && rm -fr /tmp/cmake_build

#install conda 
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda install nb_conda && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN  /opt/conda/bin/conda create  -c conda-forge --name python3 python=3.6 ipykernel pandas seaborn scikit-learn cython matplotlib networkx python-igraph tabulate fastparquet python-snappy dask pyamg && \
    /opt/conda/bin/conda clean -tipsy

RUN . /etc/profile.d/conda.sh && conda activate python3 && mkdir -p /tmp/snap_build && cd /tmp/snap_build && wget http://snap.stanford.edu/snappy/release/beta/snap-5.0.9-64-3.0-centos6.5-x64-py3.6.tar.gz && tar xf snap*.tar.gz && cd snap* && python setup.py install && rm -fr /tmp/snap_build && \
    python -m pip install --upgrade pip==9.0.3 && pip install networkit

#RUN apt-get install zip unzip
COPY  a.tar.gz /opt/
RUN cd /opt && tar xf a.tar.gz && mv graph* gct && ls -alrt gct && cd gct && git submodule update --init --recursive && find . -type d -name .git -exec rm {} \; && cd  submodules && make && ls -d */*/ |grep -v local | xargs -L1 rm -fr 


ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
