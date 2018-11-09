'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os
import subprocess
import multiprocessing
import numbers

prefix = 'cdc'


class CliquePercolation(Clustering):
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

    def __init__(self, name="CliquePercolation"):
        
        super(CliquePercolation, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'CliquePercolation' }

    def run(self, data, k=None, verbose=False, seed=None):
        if (data.is_directed()):
            raise Exception("only undirected is supported")
        
        params = {'k':k}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()

        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = [config.get_cdc_prog('k_clique', data.is_directed)]
            cmd.append("edges.txt")
            if verbose: cmd.append('-v')
            if k is not None: cmd.append("-k={}".format(k))
            if data.is_weighted(): cmd.append("-w")
            if k is not None: cmd.append("-o=output")

            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        clusters = {}
        for i, line in enumerate(lines):
            if line:
                clusters[i] = [int(u) for u in line.split(" ")]
        
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 


class Connected_Iterative_Scan(Clustering):
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

    def __init__(self, name="Connected_Iterative_Scan"):
        
        super(Connected_Iterative_Scan, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'Connected_Iterative_Scan' }

    def run(self, data, l=None, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        params = {'l':l}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()

        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = [config.get_cdc_prog('2009-cis', data.is_directed)]
            cmd.append("-i edges.txt -o output")
            if l is not None: cmd.append("-l {}".format(l))

            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        clusters = {}
        for i, line in enumerate(lines):
            if line:
                clusters[i] = [int(u) for u in line.split("|")]
        
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
    
class EAGLE(Clustering):
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

    def __init__(self, name="EAGLE"):
        
        super(EAGLE, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'EAGLE' }

    def run(self, data, nThread=None, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        if nThread is None or nThread < 1:
            nThread = max(1, multiprocessing.cpu_count() - 1)
        params = {'nThread':nThread}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()

        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = [config.get_cdc_prog('2009-eagle', data.is_directed)]
            cmd.append(str(nThread))
            cmd.append("edges.txt")
            cmd.append("dir" if data.is_directed() else "undir")
            cmd.append("output")
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        clusters = {}
        n_cluster = int(lines[0])
        for i, line in enumerate(lines[1:]):
            if line:
                clusters[i] = [int(u) for u in line.split(" ")[1:]]
        assert(len(clusters) == n_cluster)
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 


class clique_modularity(Clustering):
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

    def __init__(self, name="clique_modularity"):
        
        super(clique_modularity, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'clique_modularity' }

    def run(self, data, method="BK", nComm=10, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        assert method in {"BK" , "KJ"}

        params = {'method':method, "nComm":nComm}
        
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()

        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = "java -cp {} clique_modularity.CM {} -m {} -c {}".format(config.get_cdc_prog('conga-1.0-SNAPSHOT.jar', data.is_directed),
                                                     "edges.txt",
                                                     'clique_modularity.algorithm.BK.BK' if method == "BK" else 'clique_modularity.algorithm.KJ.KJ',
                                                     nComm)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "ClustersOutput.txt"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        clusters = {}
        for i, line in enumerate(lines):
            if line:
                clusters[i] = [int(u) for u in line.split(" ")]
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
        
    
class CONGA(Clustering):
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

    def __init__(self, name="CONGA"):
        
        super(CONGA, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'CONGA' }

    def run(self, data, silent=True, recompute=False, horizon=None, nComm=[5], weight="mean", seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        if isinstance(nComm, int): nComm = [nComm]
        params = {'silent':silent, "recompute":recompute, 'horizon':horizon, "nComm":nComm, "weight":weight}
        
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = ["java -cp {} conga.CONGA {}".format(config.get_cdc_prog('conga-1.0-SNAPSHOT.jar', data.is_directed),
                                                     "edges.txt")]
            cmd.append("-e")
            if silent: cmd.append('-s')
            if recompute: cmd.append('-r')
            if horizon is not None: cmd.append("-h {}".format(horizon))
            if data.is_weighted(): 
                if weight:
                    cmd.append("-w {}".format(weight))
                else:
                    self.logger.info("weights are ignored")
            cmd = " ".join(cmd) 
            step0cmd = cmd
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            self.logger.info("Finish first step in %f seconds" % (timecost))
            
            for n in sorted(nComm)[::-1]:
                cmd = [step0cmd]
                cmd.append("-n {}".format(n))
                cmd = " ".join(cmd) 
                self.logger.info("Running " + cmd)
                
                timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
                if status != 0: 
                    raise Exception("Run command with error status code {}".format(status))
                                                
                with open (os.path.join(tmp_dir, "clusters-edges.txt"), "r") as output:
                    lines = [u.strip() for u in output.readlines()]
                this_clusters = {}
                for i, line in enumerate(lines):
                    if line:
                        this_clusters[i] = [int(u) for u in line.split(" ")]
                self.logger.info("Made %d clusters in %f seconds" % (len(this_clusters), timecost))
                                    
                clusters[n] = this_clusters
        
        result = {}
        result['multiclusters'] = True        
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 

    
class LinkCommunities(Clustering):
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

    def __init__(self, name="LinkCommunities"):
        
        super(LinkCommunities, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'LinkCommunities' }

    def run(self, data, threshold=[5], seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        if isinstance(threshold, numbers.Number): threshold = [float(threshold)]
        params = {'threshold':threshold}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_unweighted_edges):
            data.to_unweighted_fromat()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_unweighted_edges, tmp_dir, "edges.pairs")
            cmd = "{} {} {}".format(config.get_cdc_prog('calcJaccards', data.is_directed),
                                                     "edges.pairs", "edges.jaccs")
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            self.logger.info("Finish first step in %f seconds" % (timecost))
            
            for t  in sorted(threshold)[::-1]:
                outputfile = "edges.clusters." + str(t)
                cmd = "{} {} {} {} {} {}".format(config.get_cdc_prog('clusterJaccards', data.is_directed),
                                                     "edges.pairs", "edges.jaccs", outputfile, "edges.mc_nc." + str(t), t)
                
                self.logger.info("Running " + cmd)
                
                timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
                if status != 0: 
                    raise Exception("Run command with error status code {}".format(status))
                                                
                with open (os.path.join(tmp_dir,outputfile), "r") as output:
                    lines = [u.strip() for u in output.readlines()]
                this_clusters = {}
                for i, line in enumerate(lines):
                    if line:
                        this_clusters[i] = list(set([int(u) for u in line.replace(","," ").split(" ")]))
                self.logger.info("Made %d clusters in %f seconds" % (len(this_clusters), timecost))
                                    
                clusters[t] = this_clusters
        
        result = {}
        result['multiclusters'] = True        
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    

class TopGC(Clustering):
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

    def __init__(self, name="TopGC"):
        
        super(TopGC, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'TopGC' }

    def run(self, data,  seed=None, **kwargs):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params=dict(kwargs)
        params={u:v for u,v in params.items() if v is not None}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_topgc):
            data.to_topgc_fromat()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_topgc, tmp_dir, "edges.topgc")
            
            cmd = ["java -cp {} {}".format(config.get_cdc_prog('topgc-1.0-SNAPSHOT.jar', data.is_directed),
                                                     "TopGC")]
            cmd.append("-i {}".format("edges.topgc"))
            if data.is_directed(): cmd.append("-d")
            for u, v in params.items():
                cmd.append("-{} {}".format(u,v))
            cmd=" ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))

            if 1:            
                outputfile = "edges.topgc.clusters_directed" if data.is_directed() else "edges.topgc.clusters"
                                                
                with open (os.path.join(tmp_dir,outputfile), "r") as output:
                    lines = [u.strip() for u in output.readlines()]
                for i, line in enumerate(lines):
                    if line:
                        clusters[i] = list(set([int(u) for u in line.split("\t")]))
                self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
                                    
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
    
class GCE(Clustering):
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

    def __init__(self, name="GCE"):
        
        super(GCE, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'GCE' }

    def run(self, data, minimumCliqueSizeK=4, overlapToDiscardEta=0.6, fitnessExponentAlpha=1.0, CCHthresholdPhi=0.75, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params=dict(locals());del params['self'];del params['data'];del params['seed']
        params={u:v for u,v in params.items() if v is not None}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            
            cmd = ["{}".format(config.get_cdc_prog('2011-gce', data.is_directed))]
            cmd.append('edges.txt')
            cmd.append(str(minimumCliqueSizeK))
            cmd.append(str(overlapToDiscardEta))
            cmd.append(str(fitnessExponentAlpha))
            cmd.append(str(CCHthresholdPhi))
            cmd=" ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))

            if 1:            
                outputfile = "cluster.output"
                                                
                with open (os.path.join(tmp_dir,outputfile), "r") as output:
                    lines = [u.strip() for u in output.readlines()]
                for i, line in enumerate(lines):
                    if line:
                        clusters[i] = list(set([int(u) for u in line.split(" ")]))
                self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
                                    
        
        result = {}
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
   