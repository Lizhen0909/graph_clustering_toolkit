# docker build -t lizhen0909/gct_base .
FROM ubuntu:16.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \ 
    apt-get install -y software-properties-common vim build-essential google-perftools libbz2-dev libxml2-dev libjemalloc-dev openssl \
	libcurl4-openssl-dev libssl-dev libtbb-dev libarmadillo-dev libgsl-dev git maven openjdk-8-jdk libboost-program-options-dev \
	bzip2 ca-certificates curl wget zip unzip \
	libboost-python-dev libboost-context-dev libboost-coroutine-dev libboost-iostreams-dev libboost-graph-dev libboost-regex-dev libboost-thread-dev \
	libexpat1-dev libcairomm-1.0-dev \
	libgmp-dev libcgal-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#install cmake
RUN mkdir -p /tmp/cmake_build && cd /tmp/cmake_build && wget https://cmake.org/files/v3.12/cmake-3.12.4.tar.gz && tar xf cmake*.tar.gz && cd cmake* && ./bootstrap && make && make install && rm -fr /tmp/cmake_build

# install sparsehash for graph_tool
RUN  cd /tmp/ && mkdir -p tmpsparsehash && cd tmpsparsehash && wget https://github.com/sparsehash/sparsehash/archive/sparsehash-2.0.3.tar.gz && tar xf sparse*.tar.gz && cd sparsehash*2.0.3 && bash ./configure && make install && rm -fr /tmp/tmpsparsehash

#install conda 
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda install nb_conda && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc 

# env python3.6
RUN  /opt/conda/bin/conda create  -c conda-forge --name python3 python=3.7 ipykernel pandas seaborn scikit-learn cython matplotlib networkx \
	python-igraph tabulate fastparquet python-snappy dask pyamg pycairo gobject-introspection pygobject gtk3 networkit graph-tool && \
    /opt/conda/bin/conda clean -tipsy && \
    echo "conda activate python3" >> ~/.bashrc && \
    echo "alias l='ls -alrt'" >> ~/.bashrc      && \
    echo "alias h='history'" >> ~/.bashrc      && \
    echo "set -o vi" >> ~/.bashrc

#install snap and karateclub
RUN . /etc/profile.d/conda.sh && conda activate python3 && mkdir -p /tmp/snap_build && cd /tmp/snap_build && wget http://snap.stanford.edu/snappy/release/beta/snap-5.0.9-64-3.0-centos6.5-x64-py3.6.tar.gz && tar xf snap*.tar.gz && cd snap* && python setup.py install && rm -fr /tmp/snap_build && cd ~ &&  \
    python -m pip install --upgrade pip==9.0.3 && pip install karateclub


#COPY  a.tar.gz /opt/
#RUN cd /opt && tar xf a.tar.gz && mv graph* gct && ls -alrt gct && cd gct && git submodule update --init --recursive && find . -type d -name .git -exec rm {} \; && cd  submodules && make && ls -d */*/ |grep -v local | xargs -L1 rm -fr 


#ENV TINI_VERSION v0.16.1
#ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
#RUN chmod +x /usr/bin/tini

#ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
