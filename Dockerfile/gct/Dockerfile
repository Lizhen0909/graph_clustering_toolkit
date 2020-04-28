# docker build -t lizhen0909/graph_clustering_toolkit .
FROM lizhen0909/gct_base2

RUN mkdir -p /opt/gct/submodules/local/bin  && cd /opt/gct/submodules/local/bin && find ../..   -executable -type f |grep -v ipynb |grep -v Makefile |grep -v CMake |grep -v 'local/' | xargs -L1 -I{} ln -sf {} .

ADD python /usr/bin/
ADD jupyter_notebook /usr/bin/

ENV PATH="/usr/bin:${PATH}:/opt/gct/submodules/local/bin:/opt/conda/bin"
ENV PYTHONPATH="${PYTHONPATH}:/opt/gct/python/src"
ENV GCT_HOME=/opt/gct
ENV DATA_HOME=/data

#ENV TINI_VERSION v0.16.1
#ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
#RUN chmod +x /usr/bin/tini

#ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
