import gct.alg
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
    obj = gct.alg.OSLOM_clustering.Infohiermap(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.OSLOM_clustering.Infomap(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.OSLOM_clustering.OSLOM(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.OSLOM_clustering.copra(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.OSLOM_clustering.louvain_method(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.OSLOM_clustering.lpm(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.OSLOM_clustering.modopt(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.PyCABeM_clustering.GANXiSw(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.PyCABeM_clustering.HiReCS(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.PyCABeM_clustering.LabelRank(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.cggc_clustering.CGGC(name)
    return obj.run(graph, **kwargs)


def dct_dct(name, graph, **kwargs):
    '''

    A wrapper of *dct (Distributed Graph Clustering using Thrill)* algorithm collected from `https://github.com/kit-algo/distributed_clustering_thrill`
    
    Arguments
    --------------------
    progname : str
        name of dct program. Be one of [dlslm, dlslm_map_eq, dlslm_no_contraction, dlslm_with_seq]

    Reference 
    ------------------------
    Hamann, Michael, et al. "Distributed Graph Clustering Using Modularity and Map Equation." 
    European Conference on Parallel Processing. Springer, Cham, 2018.
    
    '''
    obj = gct.alg.dct_clustering.dct(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.dct_clustering.infomap(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.dct_clustering.seq_louvain(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_edge_betweenness(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_fastgreedy(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_infomap(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_label_propagation(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_leading_eigenvector(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_multilevel(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_optimal_modularity(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_spinglass(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.igraph_clustering.community_walktrap(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.mcl_clustering.MCL(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.networkit_clustering.CutClustering(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.networkit_clustering.LPDegreeOrdered(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.networkit_clustering.PLM(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.networkit_clustering.PLP(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.powergraph_clustering.GossipMap(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.powergraph_clustering.RelaxMap(name)
    return obj.run(graph, **kwargs)


def alg_label_propagation(name, graph, **kwargs):
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
    obj = gct.alg.powergraph_clustering.label_propagation(name)
    return obj.run(graph, **kwargs)


def scan_AnyScan(name, graph, **kwargs):
    '''

    A wrapper of *anyscan* algorithm  

    Arguments
    --------------------
    Usage: ./anyscan [switches] -i filename -m minpts -e epsilon -o output -t threads
            -c algorithm: algorithm used 
            -i filename     : file containing input data to be clustered
            -g gname        : file containing ground truth 
            -m minpts       : input parameter of DBSCAN, min points to form a cluster, e.g. 2
            -e epsilon      : input parameter of DBSCAN, radius or threshold on neighbourhoods retrieved, e.g. 0.8
            -o output       : clustering results, format, (each line, point id, clusterid)
            -a alpha    : block size alpha 
            -b beta     : block size beta 
            -t threads      : number of threads to be employed

    
    Reference
    ------------------------
    Mai S T, Dieu M S, Assent I, et al. Scalable and Interactive Graph Clustering Algorithm on Multicore CPUs[C]//Data Engineering (ICDE), 2017 IEEE 33rd International Conference on. IEEE, 2017: 349-360
    
    '''
    obj = gct.alg.scan_clustering.AnyScan(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.scan_clustering.Scanpp(name)
    return obj.run(graph, **kwargs)


def scan_pScan(name, graph, **kwargs):
    '''

    A wrapper of *pScan, ppScan, ppScanSSE* algorithm  

    Arguments
    --------------------
    prog:         one of pScan, ppScan, ppScanSSE
    epsilon:     similarity-threshold 
    mu:         density-threshold
    
    Reference
    ------------------------
    Chang L, Li W, Qin L, et al. $\mathsf {pSCAN} $: Fast and Exact Structural Graph Clustering[J]. IEEE Transactions on Knowledge and Data Engineering, 2017, 29(2): 387-401.
    Yulin Che, Shixuan Sun, Qiong Luo. 2018. Parallelizing Pruning-based Graph Structural Clustering. In ICPP 2018: 47th International Conference on Parallel Processing, August 13–16, 2018, Eugene, OR, USA. ACM, New York, NY, USA    
    
    '''
    obj = gct.alg.scan_clustering.pScan(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.snap_clustering.Clauset_Newman_Moore(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.snap_clustering.Girvan_Newman(name)
    return obj.run(graph, **kwargs)


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
    obj = gct.alg.streaming_clustering.streamcom(name)
    return obj.run(graph, **kwargs)


__ALG_LIST__ += ['oslom_Infohiermap', 'oslom_Infomap', 'oslom_OSLOM', 'oslom_copra', 'oslom_louvain_method', 'oslom_lpm', 'oslom_modopt', 'pycabem_GANXiSw', 'pycabem_HiReCS', 'pycabem_LabelRank', 'cgcc_CGGC', 'dct_dct', 'dct_infomap', 'dct_seq_louvain', 'igraph_community_edge_betweenness', 'igraph_community_fastgreedy', 'igraph_community_infomap', 'igraph_community_label_propagation', 'igraph_community_leading_eigenvector', 'igraph_community_multilevel', 'igraph_community_optimal_modularity', 'igraph_community_spinglass', 'igraph_community_walktrap', 'mcl_MCL', 'networkit_CutClustering', 'networkit_LPDegreeOrdered', 'networkit_PLM', 'networkit_PLP', 'alg_GossipMap', 'alg_RelaxMap', 'alg_label_propagation', 'scan_AnyScan', 'scan_Scanpp', 'scan_pScan', 'snap_Clauset_Newman_Moore', 'snap_Girvan_Newman', 'alg_streamcom']

#### end generated algorithm methods

def list_algorithms():
    return __ALG_LIST__


def run_alg(runname, algname, params):
    if algname not in __ALG_LIST__:
        raise Exception ("algorithm {} not found. Available algorithms:\n" + str(list_algorithms()))
    fun = getattr(gct.alg, algname)
    return fun(runname, **params)
