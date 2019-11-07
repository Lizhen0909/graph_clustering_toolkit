# docker build -t lizhen0909/gct_base2
FROM lizhen0909/gct_base

RUN cd /opt && git clone https://LizhenShi@bitbucket.org/LizhenShi/graph_clustering_toolkit.git && cd /opt && ln -s graph_clustering_toolkit gct && cd gct && git submodule update --init --recursive && find . -type d -name .git -exec rm {} \; && cd  submodules && make && ls -d */*/ |grep -v local | xargs -L1 rm -fr 

