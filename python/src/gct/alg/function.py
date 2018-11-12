import gct.alg
from gct.exception import UnsupportedException
import sys
__ALG_LIST__=[]

#### begin generated algorithm methods
def oslom_Infohiermap(name, graph, **kwargs):
    '''

    A wrapper of *Hierarchical Infomap* collected from `OSLOM <http://www.oslom.org/index.html>`
    
    Arguments
    --------------------
    seed : int
        random seed

    Reference 
    ------------------------
    Martin Rosvall and Carl T. Bergstrom Multilevel compression of random walks on
    networks reveals hierarchical organization in large integrated systems. PLoS ONE 6(4):
    e18209 (2011).     
    
    '''
    try:
        obj = gct.alg.OSLOM_clustering.Infohiermap(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def oslom_Infomap(name, graph, **kwargs):
    '''

    A wrapper of *infomap* collected from `OSLOM <http://www.oslom.org/index.html>`
    
    Arguments
    --------------------
    seed : int
        random seed

    Reference 
    ------------------------ 
    Rosvall, M. and Bergstrom, C. T. Maps of random
    walks on complex networks reveal community structure. Proc. Natl. Acad. Sci.
    USA 105, 11181123 (2008).
    
    '''
    try:
        obj = gct.alg.OSLOM_clustering.Infomap(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def oslom_OSLOM(name, graph, **kwargs):
    '''

    A wrapper of *OSLOM (Order Statistics Local Optimization Method)* collected from `OSLOM <http://www.oslom.org/index.html>`
    
    Arguments
    --------------------
    OPTIONS
    
      [-r R]:                       sets the number of runs for the first hierarchical level, bigger this value, more accurate the output (of course, it takes more). Default value is 10.
    
      [-hr R]:                      sets the number of runs  for higher hierarchical levels. Default value is 50 (the method should be faster since the aggregated network is usually much smaller).
    
      [-seed m]:                    sets m equal to the seed for the random number generator. (instead of reading from time_seed.dat)
    
      [-hint filename]:             takes a partition from filename. The file is expected to have the nodes belonging to the same cluster on the same line.
    
      [-load filename]:             takes modules from a tp file you already got in a previous run.
    
      [-t T]:                       sets the threshold equal to T, default value is 0.1
    
      [-singlet]:                    finds singletons. If you use this flag, the program generally finds a number of nodes which are not assigned to any module.
                                    the program will assign each node with at least one not homeless neighbor. This only applies to the lowest hierarchical level.
    
      [-cp P]:                      sets a kind of resolution parameter equal to P. This parameter is used to decide if it is better to take some modules or their union.
                                    Default value is 0.5. Bigger value leads to bigger clusters. P must be in the interval (0, 1).
    
      [-fast]:                      is equivalent to "-r 1 -hr 1" (the fastest possible execution).
    
      [-infomap runs]:              calls infomap and uses its output as a starting point. runs is the number of times you want to call infomap.
    
      [-copra runs]:                same as above using copra.
    
      [-louvain runs]:              same as above using louvain method.


    Reference 
    ------------------------
    A. Lancichinetti, F. Radicchi, J.J. Ramasco and S. Fortunato Finding statistically sig-
    nificant communities in networks PloS One 6, e18961 (2011)
    
    '''
    try:
        obj = gct.alg.OSLOM_clustering.OSLOM(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def oslom_copra(name, graph, **kwargs):
    '''

    A wrapper of *COPRA (Community Overlap PRopagation Algorithm)* collected from `OSLOM <http://www.oslom.org/index.html>`
    
    Arguments
    --------------------
    Usage: java COPRA <file> <options>
    Options:
      -bi            <file> is a bipartite network. "-w" not allowed.
      -w             <file> is a weighted unipartite network. "-bi" not allowed.
      -v <v>         <v> is maximum number of communities/vertex. Default: 1.
      -vs <v1> <v2>  Repeats for -v <v> for all <v> between <v1>-<v2>.
      -prop <p>      <p> is maximum number of propagations. Default: no limit.
      -repeat <r>    Repeats <r> times, for each <v>, and computes average.
      -mo            Compute the overlap modularity of each solution.
      -nosplit       Don't split discontiguous communities.
      -extrasimplify Simplify communities again after splitting.
      -q             Don't show information when starting program.


    Reference 
    ------------------------
    Lancichinetti, Andrea, Santo Fortunato, and János Kertész. 
    "Detecting the overlapping and hierarchical community structure in complex networks." 
    New Journal of Physics 11.3 (2009): 033015.  
    
    '''
    try:
        obj = gct.alg.OSLOM_clustering.copra(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def oslom_louvain_method(name, graph, **kwargs):
    '''

    A wrapper of *Louvain* algorithm collected from `OSLOM <http://www.oslom.org/index.html>`
    
    Arguments
    --------------------
    seed : int
        random seed

    Reference 
    ------------------------
    V.D. Blondel, J.-L. Guillaume, R. Lambiotte and E. Lefebvre Fast unfolding of com-
    munity hierarchies in large networks. J. Stat. Mech. 2008 (10): P10008  
    
    '''
    try:
        obj = gct.alg.OSLOM_clustering.louvain_method(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def oslom_lpm(name, graph, **kwargs):
    '''

    A wrapper of *Label Propagation Method* collected from `OSLOM <http://www.oslom.org/index.html>`
    
    Arguments
    --------------------
    seed : int
        random seed

    Reference 
    ------------------------
    Raghavan, U. N., Albert, R. and Kumara, S. Near linear time algorithm to detect
    community structures in large-scale networks. Phys. Rev. E 76, 036106 (2007).    
    
    '''
    try:
        obj = gct.alg.OSLOM_clustering.lpm(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def oslom_modopt(name, graph, **kwargs):
    '''

    A wrapper of *Modularity Optimization (Simulated Annealing)* collected from `OSLOM <http://www.oslom.org/index.html>`
    
    Arguments
    --------------------
    ./modopt [netfile] [random_seed] [lambda] [trials] [temp_step] [initial_temp]
    default random_seed = 1
    default lambda= 1
    default trials= 5
    default temp_step= 0.999
    default initial_temp= 1e-6

    Reference 
    ------------------------
    Sales-Pardo, M., Guimer, R., Moreira, A. A. and Amaral, L. A. N Extracting the
    hierarchical organization of complex systems. Proc. Natl. Acad. Sci. USA 104, 1522415229
    (2007).
    
    '''
    try:
        obj = gct.alg.OSLOM_clustering.modopt(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def pycabem_GANXiSw(name, graph, **kwargs):
    '''

    
    A wrapper of *GANXiSw* algorithm from https://sites.google.com/site/communitydetectionslpa/. 

    Arguments
    --------------------
    GANXiSw 3.0.2(used to be SLPAw) is for weighted (directed) networks, version=3.0.2
    Usage: java -jar GANXiSw.jar -i networkfile
    Options:
      -i input network file
      -d output director (default: output)
      -L set to 1 to use only the largest connected component
      -t maximum iteration (default: 100)
      -run number of repetitions
      -r a specific threshold in [0,0.5]
      -ov set to 0 to perform disjoint detection
      -W treat the input as a weighted network, set 0 to ignore the weights(default 1)
      -Sym set to 1 to make the edges symmetric/bi-directional (default 0)
      -seed user specified seed for random generator
      -help to display usage info
     -----------------------------Advanced Parameters---------------------------------
      -v weighted version in {1,2,3}, default=3
      -Oov set to 1 to output overlapping file, default=0
      -Onc set to 1 to output <nodeID communityID> format, 2 to output <communityID nodeID> format
      -minC min community size threshold, default=2
      -maxC max community size threshold
      -ev embedded SLPAw's weighted version in {1,2,3}, default=1
      -loopfactor determine the num of loops for depomposing each large com, default=1.0
      -Ohis1 set to 1 to output histgram Level1
      -Ohis2 set to 1 to output histgram Level2
    
      -OMem1 set to 1 to output each node's memory content at Level 1
      -EC evolution cutoff, a real value > 1.0 
    NOTE: 1. more parameters refer to Readme.pdf
          2. parameters are *CASE-SENSITIVE*, e.g., -Onc is not -onc
          
    
    Reference
    ------------------------
    J. Xie, B. K. Szymanski and X. Liu, "SLPA: Uncovering Overlapping Communities in Social Networks via A Speaker-listener Interaction Dynamic Process"
    
    
    '''
    try:
        obj = gct.alg.PyCABeM_clustering.GANXiSw(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def pycabem_HiReCS(name, graph, **kwargs):
    '''

    A wrapper of *hirecs* algorithm from http://www.lumais.com/hirecs. 

    Arguments
    --------------------
    Usage: ./hirecs [-o{t,c,j}] [-f] [-r] [-m<float>] <adjacency_matrix.hig>
      -o  - output data format. Default: t
        t  - text like representation for logs
        c  - CSV like representation for parcing
        j  - JSON represenation
        je  - extended JSON represenation (j + unwrap root clusters to nodes)
        jd  - detaile JSON represenation (je + show inter-cluster links)
      -c  - clean links, skip links validation
      -f  - fast quazy-mutual clustering (faster). Default: strictly-mutual (better)
      -r  - rand reorder (shuffle) nodes and links on nodes construction
      -m<float>  - modularity profit margin for early exit, float E [-1, 1]. Default: -0.999, but on practice >~= 0
        -1  - skip stderr tracing after each iteration. Recommended: 1E-6 or 0
        
    Reference
    ------------------------
    Cannot find any publication. Please refer to http://www.lumais.com/hirecs
    
    
    '''
    try:
        obj = gct.alg.PyCABeM_clustering.HiReCS(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def pycabem_LabelRank(name, graph, **kwargs):
    '''

    A wrapper of *LabelRank* algorithm from https://sites.google.com/site/communitydetectionslpa/. 

    Arguments
    --------------------
    > LabelRank netName cutoff_r inflation_in NBDisimilarity_q
    
    Reference
    ------------------------
    J. Xie, B. K. Szymanski, "LabelRank: A Stabilized Label Propagation Algorithm for Community Detection in Networks", IEEE NSW, West point, NY, 2013
    
    
    '''
    try:
        obj = gct.alg.PyCABeM_clustering.LabelRank(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_CONGA(name, graph, **kwargs):
    '''

    Cluster-Overlap Newman Girvan Algorithm
        
    Arguments
    --------------------
    Usage: java conga.CONGA <file> [-e] [-g f] [-n nC] [-s] [-cd t] [-f v] [-r]
                             [-mem] [-m c] [-mo c] [-vad c] [-ov c]
                             [-dia c] [-h h] [-GN] [-peacock s] [-w eW]
    Options:
      -n   Find clustering containing nC clusters. Default: 0.
      -s   Silent operation: don't display steps in algorithm.
      -r   Recompute clusters even if clustering file exists.
      -h   Use region with horizon h. Default: unlimited.
      -w   Include edge weights in computations. A positive number or 'min', 'mean','max'.  Default: unweighted. 

    Reference 
    ------------------------
    Gregory, Steve. "An algorithm to find overlapping community structure in networks." European Conference on Principles of Data Mining and Knowledge Discovery. Springer, Berlin, Heidelberg, 2007.    
    Gregory, Steve. "A fast algorithm to find overlapping communities in networks." Joint European Conference on Machine Learning and Knowledge Discovery in Databases. Springer, Berlin, Heidelberg, 2008.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.CONGA(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_CliquePercolation(name, graph, **kwargs):
    '''

    The sequential clique percolation algorithm is method for detecting clique percolation communities. 
    It is an alternative to CFinder: instead of finding maximal cliques in a graph and producing communities 
    of all the possible clique sizes, the SCP algorithm finds all the cliques of single size and produces 
    the community structure for all the possible thresholds. 
    The SCP algorithm should work well even for large sparse networks, 
    but might have trouble for dense networks and cliques of large size.
    
    Arguments
    --------------------
    Usage: ./k_clique [inputfile] [options]
    Options:
            -k=[clique size] : The size of the clique.
            -v : Verbose mode.
    
    Reference             
    ------------------------
    Kumpula, Jussi M., et al. "Sequential algorithm for fast clique percolation." Physical Review E 78.2 (2008): 026109.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.CliquePercolation(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_Connected_Iterative_Scan(name, graph, **kwargs):
    '''

    Connected Iterative Scan Connected Iterative Scan is also known at times as Locally Optimal Sets.
    
    Arguments
    --------------------
    ./cis -i network -o output -dl delimiter -s seed file -l lambda value

    Reference 
    ------------------------
    Kelley, Stephen. The existence and discovery of overlapping communities in large-scale networks. 
    Diss. Rensselaer Polytechnic Institute, 2009.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.Connected_Iterative_Scan(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_DEMON(name, graph, **kwargs):
    '''

     DEMON
        
    Arguments
    --------------------
    epsilon  the tolerance required in order to merge communities
    min_community_size: min_community_size
    
    Reference 
    ------------------------
    Michele Coscia, Giulio Rossetti, Fosca Giannotti, Dino Pedreschi:
    DEMON: a local-first discovery method for overlapping communities.
    KDD 2012:615-623
    
    '''
    try:
        obj = gct.alg.cdc_clustering.DEMON(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_EAGLE(name, graph, **kwargs):
    '''

    EAGLE (agglomerativE hierarchicAl clusterinG based on maximaL cliquE)
    
    Arguments
    --------------------
    Sinopsi: ./2009-eagle nThreads src <dir|undir> [dest]

    Reference 
    ------------------------
    Shen, Huawei, et al. "Detect overlapping and hierarchical community structure in networks." 
    Physica A: Statistical Mechanics and its Applications 388.8 (2009): 1706-1712.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.EAGLE(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_FastCpm(name, graph, **kwargs):
    '''

     Find maximal cliques, via the Bron Kerbosch algorithm, http://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm. Then perform k-clique percolation on these cliques, for a given value of k.
        
    Arguments
    --------------------
    k:  k for k-clique
    
    Reference 
    ------------------------
    Reid, Fergal, Aaron McDaid, and Neil Hurley. 
    "Percolation computation in complex networks." 
    Proceedings of the 2012 international conference on advances in social networks analysis and mining (asonam 2012). 
    IEEE Computer Society, 2012.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.FastCpm(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_GCE(name, graph, **kwargs):
    '''

     Greedy Clique Expansion
        
    Arguments
    --------------------
    Greedy Clique Expansion Community Finder
    Community finder. Requires edge list of nodes. Processes graph in undirected, unweighted form. 
    Edgelist must be two values separated with non digit character.
    
    Use with either full (if specify all 5) or default (specify just graph file) parameters:
    Full parameters are:
    The name of the file to load
    The minimum size of cliques to use as seeds. Recommend 4 as default, unless particularly small communities are required (in which case use 3).
    The minimum value for one seed to overlap with another seed before it is considered sufficiently overlapping to be discarded (eta). 1 is complete overlap. However smaller values may be used to prune seeds more aggressively. A value of 0.6 is recommended.
    The alpha value to use in the fitness function greedily expanding the seeds. 1.0 is recommended default. Values between .8 and 1.5 may be useful. As the density of edges increases, alpha may need to be increased to stop communities expanding to engulf the whole graph. If this occurs, a warning message advising that a higher value of alpha be used, will be printed.
    The proportion of nodes (phi) within a core clique that must have already been covered by other cliques, for the clique to be 'sufficiently covered' in the Clique Coveage Heuristic
    
    Usage: ./2011-gce graphfilename minimumCliqueSizeK overlapToDiscardEta fitnessExponentAlpha CCHthresholdPhi
    
    Usage (with defaults): ./2011-gce graphfilename
    This will run with the default values of: minimumCliqueSizeK 4, overlapToDiscardEta 0.6, fitnessExponentAlpha 1.0, CCHthresholdPhi .75

    Reference 
    ------------------------
    Lee, Conrad, et al. "Detecting highly overlapping community structure by greedy clique expansion." arXiv preprint arXiv:1002.1827 (2010).    
    
    '''
    try:
        obj = gct.alg.cdc_clustering.GCE(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_HDEMON(name, graph, **kwargs):
    '''

     Hierarchical Demon
        
    Arguments
    --------------------
    epsilon  the tolerance required in order to merge communities
    min_community_size: min_community_size
    
    Reference 
    ------------------------
    M. Coscia, G. Rossetti, F. Giannotti, D. Pedreschi:
    Uncovering Hierarchical and Overlapping Communities with a Local-First Approach, TKDD 2015
    
    '''
    try:
        obj = gct.alg.cdc_clustering.HDEMON(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_LinkCommunities(name, graph, **kwargs):
    '''

    Link communities algorithm
        
    Arguments
    --------------------
    ./calcJaccards input.pairs output.jaccs
    ./clusterJaccards network.pairs network.jaccs network.clusters network.cluster_stats threshold

    Reference 
    ------------------------
    Yong-Yeol Ahn, James P. Bagrow, and Sune Lehmann, Link communities reveal multiscale complexity in networks, Nature 466, 761 (2010)
    
    '''
    try:
        obj = gct.alg.cdc_clustering.LinkCommunities(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MOSES(name, graph, **kwargs):
    '''

     Model-based Overlapping Seed Expansion
        
    Arguments
    --------------------
   
    Reference 
    ------------------------
    Aaron McDaid, Neil Hurley. Detecting highly overlapping communities with Model-based Overlapping Seed Expansion. ASONAM 2010    
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MOSES(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MSCD_AFG(name, graph, **kwargs):
    '''

     (Arenas et al.’s) Fast Multi-Scale Community Detection Tools
        
    Arguments
    --------------------
    scale_param: scale parameter values (e.g.[1,2], [1:1:10])
    extra_param: optional extra parameters for the given algorithm
    verbose: verbose level (default=0, max=2)
    
    Reference 
    ------------------------
    Arenas, Alex, Alberto Fernandez, and Sergio Gomez. "Analysis of the structure of complex networks at different resolution levels." New Journal of Physics 10.5 (2008): 053039.
    Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MSCD_AFG(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MSCD_HSLSW(name, graph, **kwargs):
    '''

     (Huang et al.’s) Fast Multi-Scale Community Detection Tools
        
    Arguments
    --------------------
    scale_param: scale parameter values (e.g.[1,2], [1:1:10])
    extra_param: optional extra parameters for the given algorithm
    verbose: verbose level (default=0, max=2)

    The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:
    - for HSLSW:
      1. Merging threshold beyond which communities are merged. Value must be in [0,1]. (default 0.5)
      
    Reference 
    ------------------------
    Huang, Jianbin, et al. "Towards online multiresolution community detection in large-scale networks." PloS one 6.8 (2011): e23829.
    Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MSCD_HSLSW(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MSCD_LFK(name, graph, **kwargs):
    '''

     (Lancichinetti et al.’s) Fast Multi-Scale Community Detection Tools
        
    Arguments
    --------------------
    scale_param: scale parameter values (e.g.[1,2], [1:1:10])
    extra_param: optional extra parameters for the given algorithm
    verbose: verbose level (default=0, max=2)
    
    The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:
    - for LFK:
      1. Merging threshold beyond which communities are merged. Value must be in [0,1]. (default 0.5)
      2. When growing a community, maximum number of neighbours from the sorted list of candidate nodes that can fail to join before the failures makes the growth stop. (default: infinite / value 0)
      3. When growing a community, maximum number of iterations through all nodes during which nodes can be removed. (default: infinite / value 0)
      Ex: To merge communities with 30% of overlapping nodes
          mscd -g network.edges -w -c coms -p 0.3 -a LFK [1:-0.01:0]

    Reference 
    ------------------------
    Lancichinetti, Andrea, Santo Fortunato, and János Kertész. "Detecting the overlapping and hierarchical community structure in complex networks." New Journal of Physics 11.3 (2009): 033015.
    Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MSCD_LFK(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MSCD_LFK2(name, graph, **kwargs):
    '''

     ( Lancichinetti et al.’s multi-threaded ) Fast Multi-Scale Community Detection Tools
        
    Arguments
    --------------------
    scale_param: scale parameter values (e.g.[1,2], [1:1:10])
    extra_param: optional extra parameters for the given algorithm
    verbose: verbose level (default=0, max=2)
    
    The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:
    - for LFK2:
      1. Merging threshold beyond which communities are merged. Value must be in [0,1]. (default 0.5)
      2. Maximum number of additional threads the program can use (default: number of cores available / value 0)
      3. Maximum number of seeds to start growing communities. (default: infinite / value 0)
      4. Recursive level of seed neighbours not to use as seeds must be 0, 1 or 2. (default 1) (i.e. with 1, all the neighbours of a seed cannot be added as a seed)
      
    Reference 
    ------------------------
    Lancichinetti, Andrea, Santo Fortunato, and János Kertész. "Detecting the overlapping and hierarchical community structure in complex networks." New Journal of Physics 11.3 (2009): 033015.
    Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MSCD_LFK2(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MSCD_RB(name, graph, **kwargs):
    '''

     (Reichardt and Bornholdt’s) Fast Multi-Scale Community Detection Tools
        
    Arguments
    --------------------
    scale_param: scale parameter values (e.g.[1,2], [1:1:10])
    extra_param: optional extra parameters for the given algorithm
    verbose: verbose level (default=0, max=2)
    
    Reference 
    ------------------------
    Reichardt, Jörg, and Stefan Bornholdt. "Statistical mechanics of community detection." Physical Review E 74.1 (2006): 016110.
    Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MSCD_RB(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MSCD_RN(name, graph, **kwargs):
    '''

     (Ronhovde and Nussinov’s) Fast Multi-Scale Community Detection Tools
        
    Arguments
    --------------------
    scale_param: scale parameter values (e.g.[1,2], [1:1:10])
    extra_param: optional extra parameters for the given algorithm
    verbose: verbose level (default=0, max=2)
    
    Reference 
    ------------------------
    Ronhovde, Peter, and Zohar Nussinov. "Local resolution-limit-free Potts model for community detection." Physical Review E 81.4 (2010): 046114.
    Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MSCD_RN(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MSCD_SO(name, graph, **kwargs):
    '''

      stability optimisation (Fast Multi-Scale Community Detection Tools)
        
    Arguments
    --------------------
    scale_param: scale parameter values (e.g.[1,2], [1:1:10])
    extra_param: optional extra parameters for the given algorithm
    verbose: verbose level (default=0, max=2)
    
    The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:
    - for SO:
      1. edge threshold (for walks of length>1 computed edges below this value are discarded) (default: 0)
      2. memory saving mode (for walks of length>1 the number of networks kept in memory) (default: 0, i.e. off)
        Ex: mscd -g network.edges -w -c coms -p 0.01,1 -a SO [0:0.1:5]
      
    Reference 
    ------------------------
    Le Martelot, Erwan, and Chris Hankin. "Multi-scale community detection using stability optimisation within greedy algorithms." arXiv preprint arXiv:1201.3307 (2012).
    Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MSCD_SO(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_MSCD_SOM(name, graph, **kwargs):
    '''

      tability optimisation using matrices  (Fast Multi-Scale Community Detection Tools)
        
    Arguments
    --------------------
    scale_param: scale parameter values (e.g.[1,2], [1:1:10])
    extra_param: optional extra parameters for the given algorithm
    verbose: verbose level (default=0, max=2)
    
    The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:
    - for SOM:
      1. memory saving mode (for walks of length>1 the number of networks kept in memory) (default: 0, i.e. off)
        Ex: mscd -g network.edges -w -c coms -p 1 -a SOM [0:0.1:5]
    
    Reference 
    ------------------------
    Le Martelot, Erwan, and Chris Hankin. "Multi-scale community detection using stability optimisation within greedy algorithms." arXiv preprint arXiv:1201.3307 (2012).
    Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.MSCD_SOM(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_ParCPM(name, graph, **kwargs):
    '''

     Model-based Overlapping Seed Expansion
        
    Arguments
    --------------------
     -P <num_threads>  Specifies the number of parallel threads to be executed.
                       Default value is 8.
     -W <exp>          Set the sliding window buffer size to 2**<exp> Bytes.
                       Default value is 30 for a sliding window buffer size of 2**30 B = 1 GB.
     -p                Specifies to use the proof-of-concept method COSpoc rather than COS.
                       With this option, parameter -W is ignored.
                      
    Reference 
    ------------------------
    Gregori, Enrico, Luciano Lenzini, and Simone Mainardi. 
    "Parallel k-clique community detection on large-scale networks." 
    IEEE Transactions on Parallel and Distributed Systems 24.8 (2013): 1651-1660.
        
    
    '''
    try:
        obj = gct.alg.cdc_clustering.ParCPM(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_SVINET(name, graph, **kwargs):
    '''

     SVINET implements sampling based algorithms that derive from stochastic variational inference under the (assortative) mixed-membership stochastic blockmodel.
        
    Arguments
    --------------------
    SVINET: fast stochastic variational inference of undirected networks
    svinet [OPTIONS]
            -file <name>    input tab-separated file with a list of undirected links
            -n <N>          number of nodes in network
            -k <K>          number of communities
            -batch          run batch variational inference
            -stratified     use stratified sampling
             * use with rpair or rnode options
            -rnode          inference using random node sampling
            -rpair          inference using random pair sampling
            -link-sampling  inference using link sampling 
            -infset         inference using informative set sampling
            -rfreq          set the frequency at which
             * convergence is estimated
             * statistics, e.g., heldout likelihood are computed
            -max-iterations         maximum number of iterations (use with -no-stop to avoid stopping in an earlier iteration)
            -no-stop                disable stopping criteria
            -seed           set GSL random generator seed
    
    Reference 
    ------------------------
    Prem K. Gopalan, David M. Blei. Efficient discovery of overlapping communities in massive networks. To appear in the Proceedings of the National Academy of Sciences, 2013
    
    '''
    try:
        obj = gct.alg.cdc_clustering.SVINET(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_TopGC(name, graph, **kwargs):
    '''

     Top Graph Clusters (TopGC)
        
    Arguments
    --------------------
    Usage: java -jar TopGC.jar -i inputGraph [-p mostProm] [-max maxClusterSize] [-min minClusterSize] [-lambda overlapThreshold] [-l wordLength] [-m m] [-w numWords] [-trials trials]
    
    Options:
    -----

    -max    maxClusterSize
            The maximum size allowed for a cluster.
            Default is 20.

    -min    minClusterSize
            The minimum size allowed for a cluster.
            Default is 5.

    -p    mostProm
            The pruning parameter. Limits the number of nodes to
            consider for final clustering. Lower values will
            achieve greater pruning, as well as limit memory
            usage of the program. Ranges from 1 to graph size.
            Default is 0.3*(# of nodes in graph) or
            50,000 (whichever is smaller).

    -lambda    overlapThreshold
            The maximum overlap allowed between the nodes of
            two clusters. Calculated as the ratio of the
            size of their intersection and the smallest cluster
            size. A double value ranging from 0 to 1.
            Default is 0.2.

    -l    wordLength
            Length of node signature. Experimentally, higher 
            values tend to achieve greater precision, though 
            lower recall.

    -m    m
            Number of minhash values to obtain per node.

    -w    w
            Number of signatures to create per node.
            Higher values may be necessary in graphs with loose
            clusters.

    -trials    trials
            The number of neighborhood instances to create
            per node. Used only in weighted graphs.    

    Reference 
    ------------------------
    Macropol, Kathy, and Ambuj Singh. "Scalable discovery of best clusters on large graphs." Proceedings of the VLDB Endowment 3.1-2 (2010): 693-702.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.TopGC(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cdc_clique_modularity(name, graph, **kwargs):
    '''

    Detecting Communities in Networks by Merging Cliques
        
    Arguments
    --------------------
    java -cp CM.jar clique_modularity.CM <networkFile> -m <method> -c <nComm>
    where method is BK or KJ

    Reference 
    ------------------------
    Yan, Bowen, and Steve Gregory. "Detecting communities in networks by merging cliques." Intelligent Computing and Intelligent Systems, 2009. ICIS 2009. IEEE International Conference on. Vol. 1. IEEE, 2009.
    
    '''
    try:
        obj = gct.alg.cdc_clustering.clique_modularity(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def cgcc_CGGC(name, graph, **kwargs):
    '''

    A wrapper of *CGGC* (Core Groups Graph ensemble Clustering) method* from `https://github.com/eXascaleInfolab/CGGC`
    Performs clustering of the unweighed undirected network (graph) using RG, CGGC_RG or CGGCi_RG algorithms.
        
    Arguments
    --------------------


    Supported Arguments:
      -h [ --help ]                   Display this message
      -i [ --inpfmt ] arg (=)        input network format (inferred from the file
                                      extension if not specified explicitly):
                                      e - nse format: header in comments + each
                                      line specifies a single edge: <sid> <did>,
                                      a - nse format: header in comments + each
                                      line specifies a single arc: <sid> <did>,
                                      m - Metis format of the unweighted network,
                                      p - Pajek format of the undirected unweighted
                                      network
      -s [ --startk ] arg (=2)        sample size of RG
      -f [ --finalk ] arg (=2000)     sample size for final RG step
      -r [ --runs ] arg (=1)          number of runs from which to pick the best
                                      result
      -e [ --ensemblesize ] arg (=-1) size of ensemble for ensemble algorithms (-1
                                      = ln(#vertices))
      -a [ --algorithm ] arg (=3)     algorithm: 1: RG, 2: CGGC_RG, 3: CGGCi_RG
      -o [ --outfmt ] arg (=l)        output clusters format:
                                      l - cnl format: header in comments + each
                                      line corresponds to the cluster and contains
                                      ids of the member vertices,
                                      c - each line corresponds to the cluster and
                                      contains ids of the member vertices,
                                      v - each line corresponds to the vertex and
                                      contains id of the owner cluster
      -f [ --outfile ] arg            file to store the detected communities
      -d [ --seed ] arg               seed value to initialize random number
                                      generator


    Reference 
    ------------------------
    Ovelgönne, Michael, and Andreas Geyer-Schulz. 
    "An ensemble learning strategy for graph clustering." 
    Graph Partitioning and Graph Clustering 588 (2012): 187.
    
    '''
    try:
        obj = gct.alg.cggc_clustering.CGGC(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def dct_dlplm(name, graph, **kwargs):
    '''

    A wrapper of *dlplm (Distributed Graph Clustering using Thrill)* algorithm collected from `https://github.com/kit-algo/distributed_clustering_thrill`
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Hamann, Michael, et al. "Distributed Graph Clustering Using Modularity and Map Equation." 
    European Conference on Parallel Processing. Springer, Cham, 2018.
    
    '''
    try:
        obj = gct.alg.dct_clustering.dlplm(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def dct_dlslm(name, graph, **kwargs):
    '''

    A wrapper of *dlslm (Distributed Graph Clustering using Thrill)* algorithm collected from `https://github.com/kit-algo/distributed_clustering_thrill`
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Hamann, Michael, et al. "Distributed Graph Clustering Using Modularity and Map Equation." 
    European Conference on Parallel Processing. Springer, Cham, 2018.
    
    '''
    try:
        obj = gct.alg.dct_clustering.dlslm(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def dct_dlslm_map_eq(name, graph, **kwargs):
    '''

    A wrapper of *dlslm_map_eq (Distributed Graph Clustering using Thrill)* algorithm collected from `https://github.com/kit-algo/distributed_clustering_thrill`
    
    Arguments
    --------------------
    None
    
    Reference 
    ------------------------
    Hamann, Michael, et al. "Distributed Graph Clustering Using Modularity and Map Equation." 
    European Conference on Parallel Processing. Springer, Cham, 2018.
    
    '''
    try:
        obj = gct.alg.dct_clustering.dlslm_map_eq(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def dct_dlslm_no_contraction(name, graph, **kwargs):
    '''

    A wrapper of *dlslm_no_contraction (Distributed Graph Clustering using Thrill)* algorithm collected from `https://github.com/kit-algo/distributed_clustering_thrill`
    
    Arguments
    --------------------
    None 
    
    Reference 
    ------------------------
    Hamann, Michael, et al. "Distributed Graph Clustering Using Modularity and Map Equation." 
    European Conference on Parallel Processing. Springer, Cham, 2018.
    
    '''
    try:
        obj = gct.alg.dct_clustering.dlslm_no_contraction(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def dct_dlslm_with_seq(name, graph, **kwargs):
    '''

    A wrapper of *dlslm_with_seq (Distributed Graph Clustering using Thrill)* algorithm collected from `https://github.com/kit-algo/distributed_clustering_thrill`
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Hamann, Michael, et al. "Distributed Graph Clustering Using Modularity and Map Equation." 
    European Conference on Parallel Processing. Springer, Cham, 2018.
    
    '''
    try:
        obj = gct.alg.dct_clustering.dlslm_with_seq(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def dct_infomap(name, graph, **kwargs):
    '''

    A wrapper of *infomap* algorithm collected from `https://github.com/kit-algo/distributed_clustering_thrill`
    
    Arguments
    --------------------
    seed : int
        random seed

    Reference 
    ------------------------
    Rosvall, M., Axelsson, D., Bergstrom, C.T.: The map equation. The European
    Physical Journal Special Topics 178(1), 13–23 (2009)
    
    '''
    try:
        obj = gct.alg.dct_clustering.infomap(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def dct_seq_louvain(name, graph, **kwargs):
    '''

    A wrapper of *Louvain* algorithm collected from `https://github.com/kit-algo/distributed_clustering_thrill`
    
    Arguments
    --------------------
    seed : int
        random seed

    Reference 
    ------------------------
    Blondel, V., Guillaume, J.L., Lambiotte, R., Lefebvre, E.: Fast unfolding of communities
    in large networks. Journal of Statistical Mechanics: Theory and Experiment
    2008(10) (2008)
    
    '''
    try:
        obj = gct.alg.dct_clustering.seq_louvain(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_edge_betweenness(name, graph, **kwargs):
    '''

    A wrapper of *community_edge_betweenness* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
     M Girvan and MEJ Newman: Community structure in social and biological networks, Proc. Nat. Acad. Sci. USA 99, 7821-7826 (2002)
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_edge_betweenness(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_fastgreedy(name, graph, **kwargs):
    '''

    A wrapper of *community_fastgreedy* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    A Clauset, MEJ Newman and C Moore: Finding community structure in very large networks. Phys Rev E 70, 066111 (2004).
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_fastgreedy(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_infomap(name, graph, **kwargs):
    '''

    A wrapper of *community_infomap* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    M. Rosvall and C. T. Bergstrom: Maps of information flow reveal community structure in complex networks, PNAS 105, 1118 (2008). http://dx.doi.org/10.1073/pnas.0706851105, http://arxiv.org/abs/0707.0609.
    M. Rosvall, D. Axelsson, and C. T. Bergstrom: The map equation, Eur. Phys. J. Special Topics 178, 13 (2009). http://dx.doi.org/10.1140/epjst/e2010-01179-1, http://arxiv.org/abs/0906.1405.
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_infomap(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_label_propagation(name, graph, **kwargs):
    '''

    A wrapper of *community_label_propagation* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Raghavan, U.N. and Albert, R. and Kumara, S. Near linear time algorithm to detect community structures in large-scale networks. Phys Rev E 76:036106, 2007. http://arxiv.org/abs/0709.2938.
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_label_propagation(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_leading_eigenvector(name, graph, **kwargs):
    '''

    A wrapper of *community_leading_eigenvector* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    MEJ Newman: Finding community structure in networks using the eigenvectors of matrices, arXiv:physics/0605087
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_leading_eigenvector(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_multilevel(name, graph, **kwargs):
    '''

    A wrapper of *community_multilevel* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    VD Blondel, J-L Guillaume, R Lambiotte and E Lefebvre: Fast unfolding of community hierarchies in large networks, J Stat Mech P10008 (2008), http://arxiv.org/abs/0803.0476
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_multilevel(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_optimal_modularity(name, graph, **kwargs):
    '''

    A wrapper of *community_optimal_modularity* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    TBD
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_optimal_modularity(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_spinglass(name, graph, **kwargs):
    '''

    A wrapper of *community_spinglass* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Reichardt J and Bornholdt S: Statistical mechanics of community detection. Phys Rev E 74:016110 (2006). http://arxiv.org/abs/cond-mat/0603718.
    Traag VA and Bruggeman J: Community detection in networks with positive and negative links. Phys Rev E 80:036115 (2009). http://arxiv.org/abs/0811.2329.
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_spinglass(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def igraph_community_walktrap(name, graph, **kwargs):
    '''

    A wrapper of *community_walktrap* algorithm from iGraph
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    Pascal Pons, Matthieu Latapy: Computing communities in large networks using random walks, http://arxiv.org/abs/physics/0512106
    
    '''
    try:
        obj = gct.alg.igraph_clustering.community_walktrap(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def mcl_MCL(name, graph, **kwargs):
    '''

    A wrapper of *MCL (Markov Cluster Algorithm)* from `https://micans.org/mcl/`
    
    Arguments
    --------------------
    Since there are a lot options for mcl. refer to https://micans.org/mcl/ for all of them.
    However only specify algrithm options, don't specify file/folder/format related option.
    ------------------------
    Stijn van Dongen, Graph Clustering by Flow Simulation. PhD thesis, University of Utrecht, May 2000
    
    '''
    try:
        obj = gct.alg.mcl_clustering.MCL(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def networkit_CutClustering(name, graph, **kwargs):
    '''

    A wrapper of *CutClustering* algorithm from NetworKit. 
    
    Arguments
    --------------------
    None

    Reference
    ------------------------
    Tarjan, Robert E.; Tsioutsiouliklis, Kostas. Graph Clustering and Minimum Cut Trees. Internet Mathematics 1 (2003), no. 4, 385–408.
    
    '''
    try:
        obj = gct.alg.networkit_clustering.CutClustering(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def networkit_LPDegreeOrdered(name, graph, **kwargs):
    '''

    A wrapper of *LPDegreeOrdered* algorithm from NetworKit. 
    Label propagation-based community detection algorithm which processes nodes in increasing order of node degree.
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    TBD
    
    '''
    try:
        obj = gct.alg.networkit_clustering.LPDegreeOrdered(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def networkit_PLM(name, graph, **kwargs):
    '''

    A wrapper of *PLM (Parallel Louvain Method)* algorithm from NetworKit. 
    Parallel Louvain Method - the Louvain method, optionally extended to a full multi-level algorithm with refinement

    Arguments
    --------------------
    refine (bool, optional) – Add a second move phase to refine the communities.
    gamma (double) – Multi-resolution modularity parameter: 1.0 -> standard modularity 0.0 -> one community 2m -> singleton communities
    par (string) – parallelization strategy
    maxIter (count) – maximum number of iterations for move phase
    turbo (bool, optional) – faster but uses O(n) additional memory per thread
    recurse (bool, optional) – use recursive coarsening, see http://journals.aps.org/pre/abstract/10.1103/PhysRevE.89.049902 for some explanations (default: true)

    Reference
    ------------------------
    TBD
    
    '''
    try:
        obj = gct.alg.networkit_clustering.PLM(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def networkit_PLP(name, graph, **kwargs):
    '''

    A wrapper of *PLP (Parallel Label Propagation)* algorithm from NetworKit. 
    Parallel label propagation for community detection: Moderate solution quality, very short time to solution.

    As described in Ovelgoenne et al: An Ensemble Learning Strategy for Graph Clustering Raghavan et al. proposed 
    a label propagation algorithm for graph clustering. This algorithm initializes every vertex of a graph with a 
    unique label. Then, in iterative sweeps over the set of vertices the vertex labels are updated. A vertex gets 
    the label that the maximum number of its neighbors have. The procedure is stopped when every vertex has the 
    label that at least half of its neighbors have.
    
    Arguments
    --------------------
    None

    Reference
    ------------------------
    TBD
    
    '''
    try:
        obj = gct.alg.networkit_clustering.PLP(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def alg_GossipMap(name, graph, **kwargs):
    '''

    A wrapper of *GossipMap* algorithm from https://github.com/uwescience/GossipMap. 

    Arguments
    --------------------
    GossipMap Algorithm.:
      --help                              Print this help message.
      --graph arg                         The graph file. Required.
      --format arg (=snap)                The graph file format.
      --thresh arg (=0.001)               The threshold for convergence condition.
      --tol arg (=1.0000000000000001e-15) The threshold for pagerank (ergodic 
                                          state) convergence condition.
      --maxiter arg (=10)                 The maximum of the iteration for finding 
                                          community.
      --maxspiter arg (=3)                The maximum of the iteration of sp-graph 
                                          for finding community.
      --trials arg (=1)                   The number of trials for finding 
                                          community repeatedly.
      --interval arg (=3)                 The time interval for checking whether 
                                          the received message is valid or not.
      --mode arg (=1)                     The running mode of finding community: 1 
                                          - coreOnce, 2 - coreRepeat.
      --outmode arg (=2)                  The running outerloop mode of finding 
                                          community: 1 - outerOnce, 2 - 
                                          outerRepeat.
      --prefix arg                        If set, this app will save the community 
                                          detection result.
      --ncpus arg (=6)                    Number of cpus to use per machine. 
                                          Defaults to (#cores - 2)
      --scheduler arg                     Supported schedulers are: fifo, sweep, 
                                          priority, queued_fifo. Too see options 
                                          for each scheduler, run the program with 
                                          the option ---schedhelp=[scheduler_name]
      --engine_opts arg                   string of engine options i.e., 
                                          "timeout=100"
      --graph_opts arg                    String of graph options i.e., 
                                          "ingress=random"
      --scheduler_opts arg                String of scheduler options i.e., 
                                          "strict=true"
      --engine_help arg                   Display help for engine options.
      --graph_help arg                    Display help for the distributed graph.
      --scheduler_help arg                Display help for schedulers.

    Reference
    ------------------------
    Bae, Seung-Hee, and Bill Howe. "GossipMap: A distributed community detection algorithm for billion-edge directed graphs." High Performance Computing, Networking, Storage and Analysis, 2015 SC-International Conference for. IEEE, 2015.
    
    '''
    try:
        obj = gct.alg.powergraph_clustering.GossipMap(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def alg_RelaxMap(name, graph, **kwargs):
    '''

    A wrapper of *RelaxMap* algorithm from https://github.com/uwescience/RelaxMap. 

    Arguments
    --------------------
    args[0]: seed - random seed value for generating random sequential order of vertices for each iteration.
    args[1]: network data - the input graph data.
           RelaxMap supports 1) pajek format (.net) and 2) edge list format (.txt).
    args[2]: # thread - the number of threads
    args[3]: # attempts - the number of attempts.
           (this is not applied yet, so it only return with 1 attempt.)
    args[4]: threshold - the stop condition threshold (recommended 1e-3 or 1e-4)
    args[5]: vThresh - the threshold value for each vertex movement (recommended 0.0) 
    args[6]: maxIter - the number of maximum iteration for each super-step.
    args[7]: outDir - the directory where the output files will be located.
    args[8]: prior/normal flag - apply the prioritized search for efficient runs (prior) or not (normal).
    
    Reference
    ------------------------
    Seung-Hee Bae, Daniel Halperin, Jevin West, Martin Rosvall, and Bill Howe, 
    "Scalable Flow-Based Community Detection for Large-Scale Network Analysis,"
    In Proceedings of IEEE 13th International Conference on Data Mining Workshop (ICDMW), 2013
    
    '''
    try:
        obj = gct.alg.powergraph_clustering.RelaxMap(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def alg_pg_label_propagation(name, graph, **kwargs):
    '''

    A wrapper of *LPA* algorithm from PowerGraph. 

    Arguments
    --------------------
    Label Propagation algorithm.:
      --help                         Print this help message.
      --graph arg                    The graph file. Required 
      --execution arg (=synchronous) Execution type (synchronous or asynchronous)
      --saveprefix arg               If set, will save the resultant pagerank to a 
                                     sequence of files with prefix saveprefix
      --ncpus arg (=6)               Number of cpus to use per machine. Defaults to
                                     (#cores - 2)
      --scheduler arg                Supported schedulers are: fifo, sweep, 
                                     priority, queued_fifo. Too see options for 
                                     each scheduler, run the program with the 
                                     option ---schedhelp=[scheduler_name]
      --engine_opts arg              string of engine options i.e., "timeout=100"
      --graph_opts arg               String of graph options i.e., "ingress=random"
      --scheduler_opts arg           String of scheduler options i.e., 
                                     "strict=true"
      --engine_help arg              Display help for engine options.
      --graph_help arg               Display help for the distributed graph.
      --scheduler_help arg           Display help for schedulers.

    Reference
    ------------------------
    Gonzalez, Joseph E., et al. "Powergraph: distributed graph-parallel computation on natural graphs." OSDI. Vol. 12. No. 1. 2012.
    
    '''
    try:
        obj = gct.alg.powergraph_clustering.pg_label_propagation(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_AnyScan_Scan(name, graph, **kwargs):
    '''

    A wrapper of *scan@anyscan* algorithm  

    Arguments
    --------------------
    Usage: ./anyscan [switches] -i filename -m minpts -e epsilon -o output -t threads
            -m minpts       : input parameter of DBSCAN, min points to form a cluster, e.g. 2
            -e epsilon      : input parameter of DBSCAN, radius or threshold on neighbourhoods retrieved, e.g. 0.8
            -a alpha    : block size alpha 
            -b beta     : block size beta 
            -t threads      : number of threads to be employed
    
    Reference
    ------------------------
    Mai S T, Dieu M S, Assent I, et al. Scalable and Interactive Graph Clustering Algorithm on Multicore CPUs[C]//Data Engineering (ICDE), 2017 IEEE 33rd International Conference on. IEEE, 2017: 349-360
    
    '''
    try:
        obj = gct.alg.scan_clustering.AnyScan_Scan(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_AnyScan_ScanIdealPar(name, graph, **kwargs):
    '''

    A wrapper of *scanIdealParl@anyscan* algorithm  

    Arguments
    --------------------
    Usage: ./anyscan [switches] -i filename -m minpts -e epsilon -o output -t threads
            -m minpts       : input parameter of DBSCAN, min points to form a cluster, e.g. 2
            -e epsilon      : input parameter of DBSCAN, radius or threshold on neighbourhoods retrieved, e.g. 0.8
            -a alpha    : block size alpha 
            -b beta     : block size beta 
            -t threads      : number of threads to be employed
    
    Reference
    ------------------------
    Mai S T, Dieu M S, Assent I, et al. Scalable and Interactive Graph Clustering Algorithm on Multicore CPUs[C]//Data Engineering (ICDE), 2017 IEEE 33rd International Conference on. IEEE, 2017: 349-360
    
    '''
    try:
        obj = gct.alg.scan_clustering.AnyScan_ScanIdealPar(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_AnyScan_anyScan(name, graph, **kwargs):
    '''

    A wrapper of *anyscan* algorithm  

    Arguments
    --------------------
    Usage: ./anyscan [switches] -i filename -m minpts -e epsilon -o output -t threads
            -m minpts       : input parameter of DBSCAN, min points to form a cluster, e.g. 2
            -e epsilon      : input parameter of DBSCAN, radius or threshold on neighbourhoods retrieved, e.g. 0.8
            -a alpha    : block size alpha 
            -b beta     : block size beta 
            -t threads      : number of threads to be employed
    
    Reference
    ------------------------
    Mai S T, Dieu M S, Assent I, et al. Scalable and Interactive Graph Clustering Algorithm on Multicore CPUs[C]//Data Engineering (ICDE), 2017 IEEE 33rd International Conference on. IEEE, 2017: 349-360
    
    '''
    try:
        obj = gct.alg.scan_clustering.AnyScan_anyScan(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_AnyScan_anyScanParl(name, graph, **kwargs):
    '''

    A wrapper of *anyscan parallel* algorithm  

    Arguments
    --------------------
    Usage: ./anyscan [switches] -i filename -m minpts -e epsilon -o output -t threads
            -m minpts       : input parameter of DBSCAN, min points to form a cluster, e.g. 2
            -e epsilon      : input parameter of DBSCAN, radius or threshold on neighbourhoods retrieved, e.g. 0.8
            -a alpha    : block size alpha 
            -b beta     : block size beta 
            -t threads      : number of threads to be employed
    
    Reference
    ------------------------
    Mai S T, Dieu M S, Assent I, et al. Scalable and Interactive Graph Clustering Algorithm on Multicore CPUs[C]//Data Engineering (ICDE), 2017 IEEE 33rd International Conference on. IEEE, 2017: 349-360
    
    '''
    try:
        obj = gct.alg.scan_clustering.AnyScan_anyScanParl(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_AnyScan_pScan(name, graph, **kwargs):
    '''

    A wrapper of *pScan@anyscan* algorithm  

    Arguments
    --------------------
    Usage: ./anyscan [switches] -i filename -m minpts -e epsilon -o output -t threads
            -m minpts       : input parameter of DBSCAN, min points to form a cluster, e.g. 2
            -e epsilon      : input parameter of DBSCAN, radius or threshold on neighbourhoods retrieved, e.g. 0.8
            -a alpha    : block size alpha 
            -b beta     : block size beta 
            -t threads      : number of threads to be employed
    
    Reference
    ------------------------
    Mai S T, Dieu M S, Assent I, et al. Scalable and Interactive Graph Clustering Algorithm on Multicore CPUs[C]//Data Engineering (ICDE), 2017 IEEE 33rd International Conference on. IEEE, 2017: 349-360
    
    '''
    try:
        obj = gct.alg.scan_clustering.AnyScan_pScan(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_Scanpp(name, graph, **kwargs):
    '''

    A wrapper of *scan++* algorithm  

    Arguments
    --------------------
    option    arguments (Default)    description
    -e    Real number between 0 and 1 (Default: 0)    Set the epsilon parameter for the clustering.
    -m    Natural number (Default: 1)    Set the mu parameter for the clustering.
    -v    No arguments are required.    Display statistics of the clustering.
    -r    No arguments are required.    Display the clustering results.
    
    Reference
    ------------------------
    Shiokawa H, Fujiwara Y, Onizuka M. SCAN++: efficient algorithm for finding clusters, hubs and outliers on large-scale graphs[J]. Proceedings of the VLDB Endowment, 2015, 8(11): 1178-1189.
    
    '''
    try:
        obj = gct.alg.scan_clustering.Scanpp(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_pScan(name, graph, **kwargs):
    '''

    A wrapper of *pScan* algorithm  

    Arguments
    --------------------
    epsilon:     similarity-threshold 
    mu:         density-threshold
    
    Reference
    ------------------------
    Chang L, Li W, Qin L, et al. $\mathsf {pSCAN} $: Fast and Exact Structural Graph Clustering[J]. IEEE Transactions on Knowledge and Data Engineering, 2017, 29(2): 387-401.
    Yulin Che, Shixuan Sun, Qiong Luo. 2018. Parallelizing Pruning-based Graph Structural Clustering. In ICPP 2018: 47th International Conference on Parallel Processing, August 13–16, 2018, Eugene, OR, USA. ACM, New York, NY, USA    
    
    '''
    try:
        obj = gct.alg.scan_clustering.pScan(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_ppScan(name, graph, **kwargs):
    '''

    A wrapper of *ppScan* algorithm  

    Arguments
    --------------------
    epsilon:     similarity-threshold 
    mu:         density-threshold
    
    Reference
    ------------------------
    Chang L, Li W, Qin L, et al. $\mathsf {pSCAN} $: Fast and Exact Structural Graph Clustering[J]. IEEE Transactions on Knowledge and Data Engineering, 2017, 29(2): 387-401.
    Yulin Che, Shixuan Sun, Qiong Luo. 2018. Parallelizing Pruning-based Graph Structural Clustering. In ICPP 2018: 47th International Conference on Parallel Processing, August 13–16, 2018, Eugene, OR, USA. ACM, New York, NY, USA    
    
    '''
    try:
        obj = gct.alg.scan_clustering.ppScan(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def scan_ppScanSSE(name, graph, **kwargs):
    '''

    A wrapper of *ppScanSSE* algorithm  

    Arguments
    --------------------
    epsilon:     similarity-threshold 
    mu:         density-threshold
    
    Reference
    ------------------------
    Chang L, Li W, Qin L, et al. $\mathsf {pSCAN} $: Fast and Exact Structural Graph Clustering[J]. IEEE Transactions on Knowledge and Data Engineering, 2017, 29(2): 387-401.
    Yulin Che, Shixuan Sun, Qiong Luo. 2018. Parallelizing Pruning-based Graph Structural Clustering. In ICPP 2018: 47th International Conference on Parallel Processing, August 13–16, 2018, Eugene, OR, USA. ACM, New York, NY, USA    
    
    '''
    try:
        obj = gct.alg.scan_clustering.ppScanSSE(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def sklearn_AffinityPropagation(name, graph, **kwargs):
    '''

    A wrapper of *AffinityPropagation* algorithm from http://scikit-learn.org. 

    Parameters
    ----------
    damping : float, optional, default: 0.5
        Damping factor (between 0.5 and 1) is the extent to
        which the current value is maintained relative to
        incoming values (weighted 1 - damping). This in order
        to avoid numerical oscillations when updating these
        values (messages).
    max_iter : int, optional, default: 200
        Maximum number of iterations.
    convergence_iter : int, optional, default: 15
        Number of iterations with no change in the number
        of estimated clusters that stops the convergence.
    verbose : boolean, optional, default: False
        Whether to be verbose.
        
    Reference
    ------------------------
    Brendan J. Frey and Delbert Dueck, “Clustering by Passing Messages Between Data Points”, Science Feb. 2007
    
    
    '''
    try:
        obj = gct.alg.sklearn_clustering.AffinityPropagation(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def sklearn_DBSCAN(name, graph, **kwargs):
    '''

    A wrapper of *DBSCAN* algorithm from http://scikit-learn.org. 

   Parameters
    ----------
    eps : float, optional
        The maximum distance between two samples for them to be considered
        as in the same neighborhood.
    min_samples : int, optional
        The number of samples (or total weight) in a neighborhood for a point
        to be considered as a core point. This includes the point itself.
    algorithm : {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional
        The algorithm to be used by the NearestNeighbors module
        to compute pointwise distances and find nearest neighbors.
        See NearestNeighbors module documentation for details.
    leaf_size : int, optional (default = 30)
        Leaf size passed to BallTree or cKDTree. This can affect the speed
        of the construction and query, as well as the memory required
        to store the tree. The optimal value depends
        on the nature of the problem.
    p : float, optional
        The power of the Minkowski metric to be used to calculate distance
        between points.
    n_jobs : int or None, optional (default=None)
        The number of parallel jobs to run.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.
    Reference
    ------------------------
    Ester, M., H. P. Kriegel, J. Sander, and X. Xu, “A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise”. In: Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining, Portland, OR, AAAI Press, pp. 226-231. 1996    
    
    '''
    try:
        obj = gct.alg.sklearn_clustering.DBSCAN(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def sklearn_SpectralClustering(name, graph, **kwargs):
    '''

    A wrapper of *SpectralClustering* algorithm from http://scikit-learn.org. 

    Parameters
    -----------
    eigen_solver : {None, 'arpack', 'lobpcg', or 'amg'}
        The eigenvalue decomposition strategy to use. AMG requires pyamg
        to be installed. It can be faster on very large, sparse problems,
        but may also lead to instabilities
    random_state : int, RandomState instance or None (default)
        A pseudo random number generator used for the initialization of the
        lobpcg eigen vectors decomposition when eigen_solver == 'amg' and by
        the K-Means initialization. Use an int to make the randomness
        deterministic.
        See :term:`Glossary <random_state>`.
    n_init : int, optional, default: 10
        Number of time the k-means algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of inertia.
    gamma : float, default=1.0
        Kernel coefficient for rbf, poly, sigmoid, laplacian and chi2 kernels.
        Ignored for ``affinity='nearest_neighbors'``.
    n_neighbors : integer
        Number of neighbors to use when constructing the affinity matrix using
        the nearest neighbors method. Ignored for ``affinity='rbf'``.
    eigen_tol : float, optional, default: 0.0
        Stopping criterion for eigendecomposition of the Laplacian matrix
        when using arpack eigen_solver.
    assign_labels : {'kmeans', 'discretize'}, default: 'kmeans'
        The strategy to use to assign labels in the embedding
        space. There are two ways to assign labels after the laplacian
        embedding. k-means can be applied and is a popular choice. But it can
        also be sensitive to initialization. Discretization is another approach
        which is less sensitive to random initialization.
    degree : float, default=3
        Degree of the polynomial kernel. Ignored by other kernels.
    coef0 : float, default=1
        Zero coefficient for polynomial and sigmoid kernels.
        Ignored by other kernels.
    kernel_params : dictionary of string to any, optional
        Parameters (keyword arguments) and values for kernel passed as
        callable object. Ignored by other kernels.
    n_jobs : int or None, optional (default=None)
        The number of parallel jobs to run.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.
        
    Reference
    ------------------------
    Normalized cuts and image segmentation, 2000 Jianbo Shi, Jitendra Malik http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.160.2324
    A Tutorial on Spectral Clustering, 2007 Ulrike von Luxburg http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.165.9323
    Multiclass spectral clustering, 2003 Stella X. Yu, Jianbo Shi http://www1.icsi.berkeley.edu/~stellayu/publication/doc/2003kwayICCV.pdf
    
    '''
    try:
        obj = gct.alg.sklearn_clustering.SpectralClustering(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def snap_Clauset_Newman_Moore(name, graph, **kwargs):
    '''

    A wrapper of *CommunityCNM* algorithm from SNAP 

    Arguments
    --------------------
    None 
    
    Reference
    ------------------------
    Clauset, Aaron, Mark EJ Newman, and Cristopher Moore. "Finding community structure in very large networks." Physical review E 70.6 (2004): 066111.
    
    '''
    try:
        obj = gct.alg.snap_clustering.Clauset_Newman_Moore(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def snap_Girvan_Newman(name, graph, **kwargs):
    '''

    A wrapper of *CommunityGirvanNewman* algorithm from SNAP 

    Arguments
    --------------------
    None 
    
    Reference
    ------------------------
    Girvan, Michelle, and Mark EJ Newman. "Community structure in social and biological networks." Proceedings of the national academy of sciences 99.12 (2002): 7821-7826.
    
    '''
    try:
        obj = gct.alg.snap_clustering.Girvan_Newman(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def alg_Paris(name, graph, **kwargs):
    '''

    A wrapper of *paris* algorithm from https://github.com/tbonald/paris 

    Arguments
    --------------------
    None
            
    Reference
    ------------------------
    Bonald, Thomas, et al. "Hierarchical Graph Clustering using Node Pair Sampling." arXiv preprint arXiv:1806.01664 (2018).
    
    '''
    try:
        obj = gct.alg.unsorted_clustering.Paris(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def alg_lso_cluster(name, graph, **kwargs):
    '''

    A wrapper of *lso-cluster* algorithm from https://github.com/twanvl/graph-cluster 
    
    Please specify long-format options. Don't specify output.

    Arguments
    --------------------
    Optional parameters regarding the clustering:
    
    'eval', clustering Evaluate the objective function on clustering, do not optimize.
    
    'init', clustering Use the given clustering as initial value for the optimization. Default: each node is initially in a separate cluster, i.e. clustering=1:length(A).
    
    Optional parameters regarding the objective:
    
    'loss', loss Use the given loss/objective function. The loss is given a string name. See below for a list of supported loss functions. Default: loss = 'modularity'
    
    'total_volume', m Replace the total volume (sum of edges) by m. Many objectives use the total volume for normalization, and changing it will change the scale at which clusters are found. Usually increasing the total volume will result in larger clusters. Default: m = sum(sum(A))
    
    'extra_loss', alpha Add a term to the loss function that penalizes the volume of clusters, with weight alpha.
    
    'num_clusters', n Force the solution to have the given number of clusters. The algorithm uses a binary search to alter the objective until it finds a solution with the given number of clusters. The alteration is the same as the one used by extra_loss.
    
    'min_num_cluster', n Force the solution to have at least the given number of clusters.
    
    'max_num_cluster', n Force the solution to have at most the given number of clusters.
    
    'max_cluster_size', n Allow clusters to have at most n nodes.
    
    Optional parameters about internal algorithm details, you only need these if you know what you are doing:
    
    'seed', random_seed Use a given random seed. By default a fixed seed is used, so repeated runs with the same input give the same output.
    
    'num_repeats', n Repeat the search n times from scratch with different random seeds and return the best result. Default: 1
    
    'num_partitions', n Number of times to try and break apart the clusters and re-cluster them Default: 0
    
    'optimize_exhaustive', bool Use an exhaustive search instead of local search. This is of course very slow. Can be combined with max_num_cluster. Default: false.
    
    'optimize_higher_level', bool Use a hierarchical optimizer, where small clusters are considered as nodes of a higher level graph. Default: true.
    
    'always_consider_empty', bool Always consider the move of a node into a new singleton cluster. Default: true.
    
    'num_loss_tweaks', n Maximum number of iterations in the binary search to force the specified number of clusters. Default: 32
    
    'check_invariants', bool Check invariants of the algorithm (for debugging). Default: false.
    
    'trace_file', filename Write a trace of the steps performed by the optimization algorithm to a file in JSON format.
    
    'verbose', level Level of debug output. Levels go up to 7 and are increasingly chatty. Default: level = 0, i.e. no output.

    Some of the supported loss functions are:
                
    'modularity', loss = -sum_c (w_c/m - v_c^2/m^2) This is the negation of the usual definition
    
    'infomap': The infomap objective by [3].
    
    'ncut': Normalized cut, loss = sum_c (v_c - w_c) / n_c
    
    'rcut': Ratio cut, loss = sum_c (v_c - w_c) / v_c
    
    {'pmod',p}: Modularity with a different power, loss = -sum_c (w_c/m - (v_c/m)^p / (p-1))
    
    {'mom',m}: Monotonic variant of modularity, loss = -sum_c (w_c/(m + 2v_c) - (v_c/(m + 2v_c))^2)
    
    'w-log-v', loss = sum_c (w_c/m * log(v_c) )

    num loss = |C|: Minimize the number of clusters, this leads to finding the connected components.
            
    Reference
    ------------------------
    Graph clustering: does the optimization procedure matter more than the objective function?; Twan van Laarhoven and Elena Marchiori; Physical Review E 87, 012812 (2013)
    
    '''
    try:
        obj = gct.alg.unsorted_clustering.lso_cluster(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


def alg_streamcom(name, graph, **kwargs):
    '''

    A wrapper of *streamcom* algorithm from https://github.com/ahollocou/graph-streaming 

    Arguments
    --------------------
    Usage: streamcom <flags>
    Availaible flags:
            -f [graph file name] : Specifies the graph file.
            --skip [number of lines] : Specifies the number of lines to skip in the graph file.
            -o [output file name] : Specifies the output file for communities.
            --vmax-start [maximum volume range start] : Specifies the maximum volume for the aggregation phase, beginning of the range.
            --vmax-end [maximum volume range end] : Specifies the maximum volume for the aggregation phase, end of the range.
            -c [condition] : Specifies the aggregation condition for the aggregation phase: 0 is AND and 1 is OR.
            --seed [random seed]: Specifies the random seed if the edges need to be shuffle.
            --niter [number of iteration]: Specifies the number of iteration of the algorithm.
            
    Reference
    ------------------------
    Hollocou, Alexandre, et al. "A Streaming Algorithm for Graph Clustering." arXiv preprint arXiv:1712.04337 (2017)
    
    '''
    try:
        obj = gct.alg.unsorted_clustering.streamcom(name)
        return obj.run(graph, **kwargs)
    except UnsupportedException as err:
        print("Error: " + str(err), file=sys.stderr)
        return None


__ALG_LIST__ += ['oslom_Infohiermap', 'oslom_Infomap', 'oslom_OSLOM', 'oslom_copra', 'oslom_louvain_method', 'oslom_lpm', 'oslom_modopt', 'pycabem_GANXiSw', 'pycabem_HiReCS', 'pycabem_LabelRank', 'cdc_CONGA', 'cdc_CliquePercolation', 'cdc_Connected_Iterative_Scan', 'cdc_DEMON', 'cdc_EAGLE', 'cdc_FastCpm', 'cdc_GCE', 'cdc_HDEMON', 'cdc_LinkCommunities', 'cdc_MOSES', 'cdc_MSCD_AFG', 'cdc_MSCD_HSLSW', 'cdc_MSCD_LFK', 'cdc_MSCD_LFK2', 'cdc_MSCD_RB', 'cdc_MSCD_RN', 'cdc_MSCD_SO', 'cdc_MSCD_SOM', 'cdc_ParCPM', 'cdc_SVINET', 'cdc_TopGC', 'cdc_clique_modularity', 'cgcc_CGGC', 'dct_dlplm', 'dct_dlslm', 'dct_dlslm_map_eq', 'dct_dlslm_no_contraction', 'dct_dlslm_with_seq', 'dct_infomap', 'dct_seq_louvain', 'igraph_community_edge_betweenness', 'igraph_community_fastgreedy', 'igraph_community_infomap', 'igraph_community_label_propagation', 'igraph_community_leading_eigenvector', 'igraph_community_multilevel', 'igraph_community_optimal_modularity', 'igraph_community_spinglass', 'igraph_community_walktrap', 'mcl_MCL', 'networkit_CutClustering', 'networkit_LPDegreeOrdered', 'networkit_PLM', 'networkit_PLP', 'alg_GossipMap', 'alg_RelaxMap', 'alg_pg_label_propagation', 'scan_AnyScan_Scan', 'scan_AnyScan_ScanIdealPar', 'scan_AnyScan_anyScan', 'scan_AnyScan_anyScanParl', 'scan_AnyScan_pScan', 'scan_Scanpp', 'scan_pScan', 'scan_ppScan', 'scan_ppScanSSE', 'sklearn_AffinityPropagation', 'sklearn_DBSCAN', 'sklearn_SpectralClustering', 'snap_Clauset_Newman_Moore', 'snap_Girvan_Newman', 'alg_Paris', 'alg_lso_cluster', 'alg_streamcom']