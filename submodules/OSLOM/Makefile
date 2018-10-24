

Main_folder=Sources


source_folder=${Main_folder}/OSLOM_files
visual_folder=${Main_folder}/Cvis_sources_1_5_netcom

targets=oslom_undir oslom_dir \
	cvis_undir cvis_dir \
	infomap_dir_script infomap_dir \
	infomap_undir_script infomap_undir \
	infohiermap_undir infohiermap_undir_script \
	infohiermap_dir infohiermap_dir_script \
	pr_consensus \
	modopt

all: $(targets)

clean:
	rm -fr $(targets)
	find . -name \*.o -exec rm {} \;

oslom_undir:
	echo "Compiling OSLOM undirected (oslom_undir) ..."
	echo "g++ -o oslom_undir ${source_folder}/main_undirected.cpp -O3 -Wall"
	g++ -o oslom_undir ${source_folder}/main_undirected.cpp -O3 -Wall


oslom_dir:
	echo ""
	echo "Compiling OSLOM directed (oslom_dir) ..."
	echo "g++ -o oslom_dir ${source_folder}/main_directed.cpp -O3 -Wall"
	g++ -o oslom_dir ${source_folder}/main_directed.cpp -O3 -Wall

cvis_undir:
	echo ""
	echo "Compiling cvis_undir"
	echo "g++ -o cvis_undir ${visual_folder}/main_undir.cpp -O3 -Wall"
	g++ -o cvis_undir ${visual_folder}/main_undir.cpp -O3 -Wall

cvis_dir:
	echo ""
	echo "Compiling cvis_dir"
	echo "g++ -o cvis_dir ${visual_folder}/main_dir.cpp -O3 -Wall"
	g++ -o cvis_dir ${visual_folder}/main_dir.cpp -O3 -Wall


infomap_undir: infomap_undir_script
infomap_undir_script:
	echo ""
	echo "Compiling infomap_undirected ..."
	cd ${Main_folder}/infomap_undir/ && \
	make clean && \
	make && \
	g++ -o infomap_scr infomap_scr.cpp -O3

	mv ${Main_folder}/infomap_undir/infomap infomap_undir
	mv ${Main_folder}/infomap_undir/infomap_scr infomap_undir_script
	mv infomap_undir .
	mv infomap_undir_script .

infomap_dir: infomap_dir_script
infomap_dir_script:
	echo ""
	echo "Compiling infomap_directed ..."
	cd ${Main_folder}/infomap_dir/ &&\
	make clean &&\
	make &&\
	g++ -o infomap_scr infomap_scr.cpp -O3

	mv ${Main_folder}/infomap_dir/infomap infomap_dir
	mv ${Main_folder}/infomap_dir/infomap_scr infomap_dir_script

infohiermap_undir: infohiermap_undir_script
infohiermap_undir_script:
	echo ""
	echo "Compiling hier infomap_undirected ..."
	cd ${Main_folder}/infohiermap_undir/ &&\
	make clean &&\
	make &&\
	g++ -o infomap_scr infomap_scr.cpp -O3  

	mv ${Main_folder}/infohiermap_undir/infohiermap infohiermap_undir
	mv ${Main_folder}/infohiermap_undir/infomap_scr infohiermap_undir_script

infohiermap_dir: infohiermap_dir_script
infohiermap_dir_script:
	echo ""
	echo "Compiling hier infomap_directed ..."
	cd ${Main_folder}/infohiermap_dir/ &&\
	make clean &&\
	make &&\
	g++ -o infomap_scr infomap_scr.cpp -O3

	mv ${Main_folder}/infohiermap_dir/infomap infohiermap_dir
	mv ${Main_folder}/infohiermap_dir/infomap_scr infohiermap_dir_script


louvain_method:
	echo ""
	echo "Compiling louvain  method ..."
	cd ${Main_folder}/sig_louvain/ &&\
	g++ main_undirected.cpp -Wall -O3 -o a.out

	mv ${Main_folder}/sig_louvain/a.out louvain_method

lpm:
	echo ""
	echo "Compiling LPM"
	cd Sources/reka_et_al/ &&\
	g++ -o lpm main_undirected.cpp -O3

	mv Sources/reka_et_al/lpm .


pr_consensus:
	echo "compiling consensus program"
	g++ -o pr_consensus Sources/consensus_matrix/consensus_pr/from_partitions_to_network.cpp -O3

modopt:
	echo "compiling modularity optimization (simulated annealing)"
	g++ Sources/modopt/main.cpp -O3 -o modopt



