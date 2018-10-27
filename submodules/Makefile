# sudo apt-get install google-perftools libboost-all-dev libbz2-dev libxml2-dev libjemalloc-dev libcurl-dev openssl libcurl4-openssl-dev libssl-dev libtbb-dev



all: OSLOM2 OSLOM  SCAN LFR STREAM cggc dct mcl webgraph

clean: 
	cd OSLOM2 && make clean
	cd OSLOM && make clean


OSLOM2:
	cd OSLOM2 && make

OSLOM:
	cd OSLOM && make

LFR:
	cd LFR-Benchmark_UndirWeightOvp && if [ ! -f lfrbench_udwov ]; then  make; fi

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

dct:
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


webgraph:
	if [ ! -d webgraph-3.6.1 ]; then rm -fr webgraph-3.6.1.tar.gz && wget http://webgraph.di.unimi.it/webgraph-3.6.1-bin.tar.gz && tar xf webgraph-3.6.1-bin.tar.gz; fi

	if [ ! -f webgraph-3.6.1/sux4j-4.2.0.jar ]; then cd webgraph-3.6.1 &&  wget http://webgraph.di.unimi.it/webgraph-deps.tar.gz && tar xf webgraph-deps.tar.gz; fi



