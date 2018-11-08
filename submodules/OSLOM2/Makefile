


#version 2.4, September 28, 2011

Main_folder=Sources_2_5



source_folder=$(Main_folder)/OSLOM_files
visual_folder=$(Main_folder)/visualSources

targets=oslom_undir oslom_dir \
	pajek_write_undir pajek_write_dir \
	infomap_dir_script infomap_dir \
	infomap_undir_script infomap_undir \
	louvain_script 	community convert hierarchy

all: $(targets)

clean:
	rm -fr $(targets)
	find . -name \*.o -exec rm {} \;

oslom_undir:
	echo "Compiling OSLOM undirected (oslom_undir) ..."
	echo "g++ -o oslom_undir $(source_folder)/main_undirected.cpp -O3 -Wall"
	g++ -o oslom_undir $(source_folder)/main_undirected.cpp -O3 -Wall

oslom_dir:
	echo ""
	echo "Compiling OSLOM directed (oslom_dir) ..."
	echo "g++ -o oslom_dir $(source_folder)/main_directed.cpp -O3 -Wall"
	g++ -o oslom_dir $(source_folder)/main_directed.cpp -O3 -Wall


pajek_write_undir:
	echo ""
	echo "Compiling program to write pajek format (pajek_write_undir) ..."
	echo "g++ -o pajek_write_undir $(visual_folder)/main_pajek.cpp -O3"
	g++ -o pajek_write_undir $(visual_folder)/main_pajek.cpp -O3


pajek_write_dir:
	echo ""
	echo "Compiling program to write pajek format (pajek_write_dir) ..."
	echo "g++ -o pajek_write_dir $(visual_folder)/main_pajek_directed.cpp -O3"
	g++ -o pajek_write_dir $(visual_folder)/main_pajek_directed.cpp -O3



infomap_undir_script: infomap_undir 
infomap_undir:
	echo ""
	echo "Compiling infomap_undirected ..."
	cd $(Main_folder)/infomap_undir/ && make clean && make
	cd $(Main_folder)/infomap_undir/ && g++ -o infomap_scr infomap_scr.cpp -O3
	mv $(Main_folder)/infomap_undir/infomap infomap_undir
	mv $(Main_folder)/infomap_undir/infomap_scr infomap_undir_script


infomap_dir_script: infomap_dir
infomap_dir:
	echo ""
	echo "Compiling infomap_directed ..."
	cd $(Main_folder)/infomap_dir/ 
	cd $(Main_folder)/infomap_dir/ && make clean && make
	cd $(Main_folder)/infomap_dir/ && g++ -o infomap_scr infomap_scr.cpp -O3
	mv $(Main_folder)/infomap_dir/infomap infomap_dir
	mv $(Main_folder)/infomap_dir/infomap_scr infomap_dir_script


MAKE_LOUVAIN: community convert hierarchy louvain_script

community: louvain_script
	cp $(Main_folder)/louvain/community .

convert: louvain_script
	cp $(Main_folder)/louvain/convert .

hierarchy: louvain_script
	cp $(Main_folder)/louvain/hierarchy .

louvain_script: 

	echo ""
	echo "Compiling louvain  method ..."
	cd $(Main_folder)/louvain/ && \
	g++ script_to_compile.cpp  && \
	./a.out  
	cd $(Main_folder)/louvain/ && \
	g++ -o louvain_script order.cpp -O3 
	cp $(Main_folder)/louvain/louvain_script .


