# sudo apt-get install google-perftools libbz2-dev libxml2-dev libjemalloc-dev openssl libcurl4-openssl-dev libssl-dev libtbb-dev libarmadillo-dev libgsl-dev
#sudo apt-get install git maven openjdk-8-jdk libboost-program-options-dev 
# conda create --name python3 python=3.6 pandas seaborn scikit-learn cython matplotlib networkx python-igraph tabulate fastparquet python-snappy dask pyamg
# python3 -m pip install --user --upgrade pip==9.0.3
# http://snap.stanford.edu/snappy/release/beta/snap-5.0.9-64-3.0-centos6.5-x64-py3.6.tar.gz
##install graph-tool
  #107  apt-get install libexpat1-dev
  #110  apt-get install libboost-python-dev

#install https://github.com/sparsehash/sparsehash/archive/sparsehash-2.0.3.tar.gz
# conda install -c pkgw/label/superseded gtk3




all: oslom2 oslom  SCAN LFR STREAM cggc dct mcl relaxmap powergraph genconvnmi ovpnmi xmeasures hirecs GANXiS lso-cluster CDC webgraph graphtool

clean: 
	cd OSLOM2 && make clean
	cd OSLOM && make clean


oslom2:
	cd OSLOM2 && make

oslom:
	cd OSLOM && make

relaxmap:
	cd RelaxMap && make

LFR:
	cd LFR-Benchmark_UndirWeightOvp && if [ ! -f lfrbench_udwov ]; then  make; fi

powergraph: PowerGraph/label_propagation PowerGraph/GossipMap
PowerGraph/label_propagation: powergraph_build
	cp PowerGraph/release/apps/label_propagation/label_propagation PowerGraph/
PowerGraph/GossipMap: powergraph_build
	cp PowerGraph/release/apps/GossipMap/GossipMap PowerGraph/
powergraph_build: 
	if [ ! -d PowerGraph/release ]; then  cd PowerGraph && ./configure  --no_jvm; fi 
	if [ ! -f PowerGraph/release/apps/label_propagation/label_propagation ]; then  cd PowerGraph/release/apps/label_propagation && make; fi 
	if [ ! -f PowerGraph/release/apps/GossipMap/GossipMap ]; then  cd PowerGraph/release/apps/GossipMap && make; fi


LIGRA:
	cd ligra && \
	make -C apps   && \
	make -C apps/bucketing  && \
	make -C apps/eccentricity  && \
	make -C apps/localAlg  && \
	make -C utils 


SCAN: ppSCAN/pSCANParallel ppSCAN/scanpp ppSCAN/pscan ppSCAN/anyscan

ppSCAN/pSCANParallel:
	cd ppSCAN/ppSCAN-release 	&& \
	mkdir -p build  && \
	cd build  && \
	cmake ..    && \
	make	 
	cp ppSCAN/ppSCAN-release/build/pSCANParallel* ppSCAN/
	cp ppSCAN/ppSCAN-release/build/converter/converter ppSCAN/  
 
ppSCAN/scanpp:
	cp  ppSCAN/SCANVariants/scan_plus2/scanpp ppSCAN/ &&  chmod u+x ppSCAN/scanpp

ppSCAN/anyscan:
	cp  ppSCAN/SCANVariants/anySCAN/anyscan ppSCAN/ &&  chmod u+x ppSCAN/anyscan

ppSCAN/pscan:
	cd  ppSCAN/SCANVariants/pSCAN-statistics/ && mkdir -p .obj && \
	make
	cp ppSCAN/SCANVariants/pSCAN-statistics/pscan ppSCAN/


STREAM: graph-streaming/streamcom

graph-streaming/streamcom:
	cd graph-streaming/cpp && \
	sed -i.bak  's/std::time/time/g' source/streamcom/main.cpp && \
	mkdir -p build && cd build && cmake .. && make 
	
	cp graph-streaming/cpp/build/streamcom graph-streaming/


cggc: CGGC/rgmc

CGGC/rgmc:
	cd CGGC && \
	make release && cp bin/Release/rgmc .

dct: distributed_clustering_thrill/seq_louvain 

distributed_clustering_thrill/seq_louvain: distributed_clustering_thrill/BUILD_DONE
	cd distributed_clustering_thrill && find build -executable -type f  -exec cp {} . \;

distributed_clustering_thrill/BUILD_DONE:
	if [ ! -f distributed_clustering_thrill/BUILD_DONE ] ; then \
		cd distributed_clustering_thrill && \
		git submodule update --init --recursive && \
		mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make && touch ../BUILD_DONE; \
	fi

mcl:	
	if [ ! -d mcl-14-137 ]; then rm -fr mcl-14-137.tar.gz && wget https://micans.org/mcl/src/mcl-14-137.tar.gz && tar xf mcl-14-137.tar.gz; fi
	if [ ! -f mcl-14-137/BUILD_DONE ] ; then \
		cd mcl-14-137 && ./configure --prefix=$(shell pwd)/local &&  make install && touch BUILD_DONE; \
	fi



webgraph: net.gct.webgraph/webgraph.jar
net.gct.webgraph/webgraph.jar:
	cd net.gct.webgraph && mvn package &&  cp target/net.gct.webgraph*-jar-with-dependencies.jar webgraph.jar



genconvnmi_bk:
	if [ ! -f GenConvNMI/gecmi ]; then \
	   cd GenConvNMI && wget https://github.com/eXascaleInfolab/GenConvNMI/releases/download/v2.53-AccuracyConvergence/gecmi && chmod u+x gecmi; \
	fi

genconvnmi: GenConvNMI/gecmi
GenConvNMI/gecmi:
	cd GenConvNMI && make release && cp bin/Release/gecmi . \


ovpnmi:
	if [ ! -f OvpNMI/onmi ]; then \
	   cd OvpNMI && make && cp bin/Release/onmi . ; \
	fi

xmeasures: xmeasures/xmeasures
xmeasures/xmeasures:
	cd xmeasures && make release && cp bin/Release/xmeasures . ; \

hirecs: hirecs/hirecs hirecs/libhirecs.so hirecs/pajek_hig.py
hirecs/pajek_hig.py:
	cd hirecs && cp pytools/pajek_hig.py .
hirecs/hirecs:
	cd hirecs && cp client/bin/Release/hirecs . && chmod u+x hirecs
hirecs/libhirecs.so:
	cd hirecs && cp bin/Release/libhirecs.so .

GANXiS: GANXiS/LabelRank GANXiS/GANXiSw.jar
GANXiS/LabelRank:
	cd GANXiS/GANXiS-S_v1.0 && g++ *.cpp -o LabelRank && cp LabelRank ..
GANXiS/GANXiSw.jar:
	cd GANXiS/GANXiS_v3.0.2  &&  cp *.jar ..

lso-cluster: graph-cluster/lso-cluster
graph-cluster/lso-cluster:
	cd graph-cluster && make lso-cluster

CDC: 
	cd CommunityDetectionCodes && make

graphtool:
	if [ ! -d graph-tool-2.27  ]; then \
	   wget https://downloads.skewed.de/graph-tool/graph-tool-2.27.tar.bz2 && tar xf graph-tool-2.27.tar.bz2;\
	fi; \
	cd graph-tool-2.27 && CPPFLAGS=-I$(CONDA_PREFIX)/include ./configure --prefix $(pwd)/../local  && make && make install
