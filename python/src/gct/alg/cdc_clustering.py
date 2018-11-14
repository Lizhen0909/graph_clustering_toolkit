'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os
import numpy as np
import pandas as pd  
import multiprocessing
import numbers
import glob
import collections
from gct.exception import UnsupportedException

prefix = 'cdc'


class CliquePercolation(Clustering):
    '''
    The sequential clique percolation algorithm is method for detecting clique percolation communities. 
    It is an alternative to CFinder: instead of finding maximal cliques in a graph and producing communities 
    of all the possible clique sizes, the SCP algorithm finds all the cliques of single size and produces 
    the community structure for all the possible thresholds. 
    The SCP algorithm should work well even for large sparse networks, 
    but might have trouble for dense networks and cliques of large size.
    
    *Arguments*
        Usage: ./k_clique [inputfile] [options]
        
        Options:
        
            -k=[clique size] : The size of the clique.
            
            -v : Verbose mode.
    
    *Reference*             
        Kumpula, Jussi M., et al. "Sequential algorithm for fast clique percolation." Physical Review E 78.2 (2008): 026109.
    '''

    def __init__(self, name="CliquePercolation"):
        
        super(CliquePercolation, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'CliquePercolation' }

    def run(self, data, k=None, verbose=False, seed=None):
        if (data.is_directed() or data.is_edge_mirrored):
            raise UnsupportedException("only undirected and unmirrored graph is supported for " + self.get_meta()['name'])
        
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
            cmd.append("-o=output")

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
    
    *Arguments*
        ./cis -i network -o output -dl delimiter -s seed file -l lambda value

    *Reference* 
        Kelley, Stephen. The existence and discovery of overlapping communities in large-scale networks.  Diss. Rensselaer Polytechnic Institute, 2009.
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
    
    *Arguments*
        Sinopsi: ./2009-eagle nThreads src <dir|undir> [dest]

    *Reference* 
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
        
    *Arguments*
        java -cp CM.jar clique_modularity.CM <networkFile> -m <method> -c <nComm>
        where method is BK or KJ

    *Reference* 
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
            cmd = "{} -cp {} clique_modularity.CM {} -m {} -c {}".format(
                utils.get_java_command(), config.get_cdc_prog('conga-1.0-SNAPSHOT.jar', data.is_directed),
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
        
    *Arguments*
        Usage: java conga.CONGA <file> [-e] [-g f] [-n nC] [-s] [-cd t] [-f v] [-r]
                             [-mem] [-m c] [-mo c] [-vad c] [-ov c]
                             [-dia c] [-h h] [-GN] [-peacock s] [-w eW]
        Options:
          -n   Find clustering containing nC clusters. Default: 0.
          -s   Silent operation: don't display steps in algorithm.
          -r   Recompute clusters even if clustering file exists.
          -h   Use region with horizon h. Default: unlimited.
          -w   Include edge weights in computations. A positive number or 'min', 'mean','max'.  Default: unweighted. 

    *Reference* 
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
            cmd = ["{} -cp {} conga.CONGA {}".format(
                utils.get_java_command(), 
                config.get_cdc_prog('conga-1.0-SNAPSHOT.jar', data.is_directed),
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
        
    *Arguments*
        ./calcJaccards input.pairs output.jaccs
        
        ./clusterJaccards network.pairs network.jaccs network.clusters network.cluster_stats threshold

    *Reference* 
        Yong-Yeol Ahn, James P. Bagrow, and Sune Lehmann, Link communities reveal multiscale complexity in networks, Nature 466, 761 (2010)
    '''

    def __init__(self, name="LinkCommunities"):
        
        super(LinkCommunities, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'LinkCommunities' }

    def run(self, data, threshold=[0.01], seed=None):
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
                                                
                with open (os.path.join(tmp_dir, outputfile), "r") as output:
                    lines = [u.strip() for u in output.readlines()]
                this_clusters = {}
                for i, line in enumerate(lines):
                    if line:
                        this_clusters[i] = list(set([int(u) for u in line.replace(",", " ").split(" ")]))
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
        
    *Arguments*
    
        Usage: java -jar TopGC.jar -i inputGraph [-p mostProm] [-max maxClusterSize] [-min minClusterSize] [-lambda overlapThreshold] [-l wordLength] [-m m] [-w numWords] [-trials trials]
        
        Options:
    
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

    *Reference* 
        Macropol, Kathy, and Ambuj Singh. "Scalable discovery of best clusters on large graphs." Proceedings of the VLDB Endowment 3.1-2 (2010): 693-702.
    '''

    def __init__(self, name="TopGC"):
        
        super(TopGC, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'TopGC' }

    def run(self, data, seed=None, **kwargs):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = dict(kwargs)
        params = {u:v for u, v in params.items() if v is not None}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_topgc):
            data.to_topgc_fromat()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_topgc, tmp_dir, "edges.topgc")
            
            cmd = ["{} -cp {} {}".format(
                utils.get_java_command(), config.get_cdc_prog('topgc-1.0-SNAPSHOT.jar', data.is_directed),
                                                     "TopGC")]
            cmd.append("-i {}".format("edges.topgc"))
            if data.is_directed(): cmd.append("-d")
            for u, v in params.items():
                cmd.append("-{} {}".format(u, v))
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))

            if 1:            
                outputfile = "edges.topgc.clusters_directed" if data.is_directed() else "edges.topgc.clusters"
                                                
                with open (os.path.join(tmp_dir, outputfile), "r") as output:
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
    Greedy Clique Expansion Community Finder
    Community finder. Requires edge list of nodes. Processes graph in undirected, unweighted form. 
    Edgelist must be two values separated with non digit character.
        
    *Arguments*
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

    *Reference* 
        Lee, Conrad, et al. "Detecting highly overlapping community structure by greedy clique expansion." arXiv preprint arXiv:1002.1827 (2010).    
    '''

    def __init__(self, name="GCE"):
        
        super(GCE, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'GCE' }

    def run(self, data, minimumCliqueSizeK=4, overlapToDiscardEta=0.6, fitnessExponentAlpha=1.0, CCHthresholdPhi=0.75, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        params = dict(locals());del params['self'];del params['data'];del params['seed']
        params = {u:v for u, v in params.items() if v is not None}
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
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))

            if 1:            
                outputfile = "cluster.output"
                                                
                with open (os.path.join(tmp_dir, outputfile), "r") as output:
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


class MOSES(Clustering):
    '''
     Model-based Overlapping Seed Expansion
        
    *Arguments*
    
   
    *Reference* 
    
    Aaron McDaid, Neil Hurley. Detecting highly overlapping communities with Model-based Overlapping Seed Expansion. ASONAM 2010    
    '''

    def __init__(self, name="MOSES"):
        
        super(MOSES, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'MOSES' }

    def run(self, data, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        if seed is None:
            seed = np.random.randint(999999)
        params = {'seed':seed}
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            
            cmd = ["{}".format(config.get_cdc_prog('2011-moses', data.is_directed))]
            cmd.append('edges.txt')
            cmd.append('cluster.output')
            if seed: cmd.append('--seed {}'.format(seed))
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))

            if 1:            
                outputfile = "cluster.output"
                                                
                with open (os.path.join(tmp_dir, outputfile), "r") as output:
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


class ParCPM(Clustering):
    '''
     Model-based Overlapping Seed Expansion
        
    *Arguments*
        ===================    ===========================================================================
         -P <num_threads>      Specifies the number of parallel threads to be executed.
                               Default value is 8.
         -W <exp>              Set the sliding window buffer size to 2**<exp> Bytes.
                               Default value is 30 for a sliding window buffer size of 2**30 B = 1 GB.
         -p                    Specifies to use the proof-of-concept method COSpoc rather than COS.
                               With this option, parameter -W is ignored.
        ===================    ===========================================================================              
    *Reference* 
        Gregori, Enrico, Luciano Lenzini, and Simone Mainardi. 
        "Parallel k-clique community detection on large-scale networks." 
        IEEE Transactions on Parallel and Distributed Systems 24.8 (2013): 1651-1660.
        
    '''

    def __init__(self, name="ParCPM"):
        
        super(ParCPM, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'ParCPM' }

    def run(self, data, n_thread=None, W=30, poc=False, seed=None):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        if seed  is not None: self.logger.info("seed ignored")
        n_thread = utils.get_num_thread(n_thread)
        params = {'n_thread':n_thread, 'W':W, 'poc':poc }
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            
            cmd = ["{}".format(config.get_cdc_prog('max-clique', data.is_directed))]
            cmd.append('edges.txt')
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            self.logger.info("Take {} seconds for step 1".format(timecost))
            
            cmd = ["{}".format(config.get_cdc_prog('2012-ParCPM', data.is_directed))]
            cmd.append('-P {}'.format(n_thread))
            if W: cmd.append('-W {}'.format(W))
            if poc: cmd.append("-p")
            cmd.append('edges.txt.mcliques')
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            nodemap = pd.read_csv(os.path.join(tmp_dir, "edges.txt.map"), header=None, sep=" ")
            nodemap.set_index(1)
            nodemap = nodemap.loc[:, 0].to_dict()
            outputfiles = glob.glob(os.path.join(tmp_dir, "*_communities.txt"))
            for outputfile in outputfiles:
                if outputfile.endswith('k_num_communities.txt'): continue 
                k = int(outputfile.split('/')[-1].split('_')[0])
                                          
                this_cluster = collections.defaultdict(set)
                with open (os.path.join(tmp_dir, outputfile), "r") as output:
                    lines = [u.strip() for u in output.readlines()]
                for i, line in enumerate(lines):
                    if line:
                        a, b = line.split(':')
                        a = int(a)
                        for u in b.split(" "):
                            this_cluster[a].add(nodemap[int(u)])
                            
                this_cluster = {u:list(v) for u, v in this_cluster.items()}
                self.logger.info("Made %d clusters with k=%d" % (len(this_cluster), k))
                
                clusters[k] = this_cluster
            
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
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


class DEMON(Clustering):
    '''
     DEMON
        
    *Arguments*
        epsilon  the tolerance required in order to merge communities
        
        min_community_size: min_community_size
    
    *Reference* 
        Michele Coscia, Giulio Rossetti, Fosca Giannotti, Dino Pedreschi:
        DEMON: a local-first discovery method for overlapping communities.
        KDD 2012:615-623
    '''

    def __init__(self, name="DEMON"):
        super(DEMON, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'DEMON' }

    def run(self, data, epsilon=0.25, min_community_size=3, seed=None):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        if seed  is not None: self.logger.info("seed ignored")
        params = {'epsilon':epsilon, 'min_community_size':min_community_size }
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            
            cmd = ["python {}".format(config.get_cdc_prog('Demon.py', data.is_directed))]
            cmd.append('edges.txt')
            cmd.append('w' if data.is_weighted() else 'uw')
            cmd.append('d' if data.is_directed() else 'ud')
            cmd.append(str(epsilon))
            cmd.append(str(min_community_size))
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            outputfile = "communities.txt"
                                            
            with open (os.path.join(tmp_dir, outputfile), "r") as output:
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


class HDEMON(Clustering):
    '''
     Hierarchical Demon
        
    *Arguments*
        epsilon  the tolerance required in order to merge communities
        
        min_community_size: min_community_size
    
    *Reference* 
        M. Coscia, G. Rossetti, F. Giannotti, D. Pedreschi:
        Uncovering Hierarchical and Overlapping Communities with a Local-First Approach, TKDD 2015
    '''

    def __init__(self, name="HDEMON"):
        super(HDEMON, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'HDEMON' }

    def run(self, data, epsilon=0.25, min_community_size=5, seed=None):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        if seed  is not None: self.logger.info("seed ignored")
        params = {'epsilon':epsilon, 'min_community_size':min_community_size }
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            
            cmd = ["python {}".format(config.get_cdc_prog('HDemon.py', data.is_directed))]
            cmd.append('edges.txt')
            cmd.append('w' if data.is_weighted() else 'uw')
            cmd.append('d' if data.is_directed() else 'ud')
            cmd.append(str(epsilon))
            cmd.append(str(min_community_size))
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            outputfiles = glob.glob(os.path.join(tmp_dir, "communities-*"))
            for outputfile in outputfiles:
                k = int(outputfile.split('/')[-1].split('-')[-1])
                                          
                this_cluster = collections.defaultdict(set)
                with open (os.path.join(tmp_dir, outputfile), "r") as output:
                    lines = [u.strip() for u in output.readlines()]
                for i, line in enumerate(lines):
                    if line:
                        for u in line.split(" "):
                            this_cluster[i].add(int(u))
                            
                this_cluster = {u:list(v) for u, v in this_cluster.items()}
                self.logger.info("Made %d clusters with k=%d" % (len(this_cluster), k))
                
                clusters[k] = this_cluster
            
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
        result = {}
        result['multilevel'] = True         
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 


class FastCpm(Clustering):
    '''
     Find maximal cliques, via the Bron Kerbosch algorithm, http://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm. Then perform k-clique percolation on these cliques, for a given value of k.
        
    *Arguments*
        k:  k for k-clique
    
    *Reference* 
        Reid, Fergal, Aaron McDaid, and Neil Hurley. 
        "Percolation computation in complex networks." 
        Proceedings of the 2012 international conference on advances in social networks analysis and mining (asonam 2012). 
        IEEE Computer Society, 2012.
    '''

    def __init__(self, name="FastCpm"):
        super(FastCpm, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'FastCpm' }

    def run(self, data, k=4, seed=None):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        if seed  is not None: self.logger.info("seed ignored")
        params = {'k':k}
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            
            cmd = ["{}".format(config.get_cdc_prog('2012-fast-cpm', data.is_directed))]
            cmd.append('edges.txt')
            cmd.append(str(k))
            cmd.append(str('output.cluster'))
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            outputfile = "output.cluster"
                                            
            with open (os.path.join(tmp_dir, outputfile), "r") as output:
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


class _MSCDBase(Clustering):
    '''
     Fast Multi-Scale Community Detection Tools
        
    *Arguments*
        mscd -g graph -c cext -a alg params [-d] [-w] [-p expar] [-v level] [-h]
        -a: community detection algorithms followed by scale parameter values (e.g.[1,2], [1:1:10])
        -p: optional extra parameters for the given algorithm
        -v: verbose level (default=0, max=2)
        
    *Reference* 
        Le Martelot, Erwan, and Chris Hankin. 
        "Fast multi-scale detection of relevant communities in large-scale networks." 
        The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD", prog=""):
        assert prog in {'AFG', 'HSLSW', 'LFK', 'LFK2', 'RB', 'RN', 'SO', 'SOM'}
        self.prog = prog
        super(_MSCDBase, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'MSCD-' + self.prog }

    def run(self, data, scale_param="[1.0,2]", extra_param=None, verbose=0, seed=None):
        
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        if seed  is not None: self.logger.info("seed ignored")
        params = {'a': self.prog, 'p': extra_param, 'v':verbose, 'scale':scale_param}
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "graph.edges")
            
            cmd = ["{}".format(config.get_cdc_prog('2013-mscd', data.is_directed))]
            cmd.append("-g {}".format("graph.edges"))
            if data.is_directed(): cmd.append("-d")
            if extra_param: cmd.append("-p {}".format(extra_param))
            cmd.append("-w")
            if verbose: cmd.append("-v {}".format(verbose))
            cmd.append("-a {} {}".format(self.prog, scale_param))
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            outputfiles = glob.glob(os.path.join(tmp_dir, "graph_*.coms"))
            for outputfile in outputfiles:
                k = float(outputfile.split('/')[-1].split('_')[-1].split('.')[0])
                                          
                this_cluster = collections.defaultdict(set)
                with open (os.path.join(tmp_dir, outputfile), "r") as output:
                    lines = [u.strip() for u in output.readlines()]
                for i, line in enumerate(lines):
                    if line:
                        for u in line.split(" "):
                            this_cluster[i].add(int(u))
                            
                this_cluster = {u:list(v) for u, v in this_cluster.items()}
                self.logger.info("Made %d clusters with k=%d" % (len(this_cluster), k))
                
                clusters[k] = this_cluster
            
        self.logger.info("Made %d clusters in %f seconds" % (len(clusters), timecost))
        
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


class MSCD_RB(_MSCDBase):
    '''
     (Reichardt and Bornholdt’s) Fast Multi-Scale Community Detection Tools
        
    *Arguments*
        scale_param: scale parameter values (e.g.[1,2], [1:1:10])
        
        extra_param: optional extra parameters for the given algorithm
        
        verbose: verbose level (default=0, max=2)
    
    *Reference* 
        Reichardt, Jörg, and Stefan Bornholdt. "Statistical mechanics of community detection." Physical Review E 74.1 (2006): 016110.
        
        Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD_RB"):
        super(MSCD_RB, self).__init__(name, prog="RB") 

    
class MSCD_HSLSW(_MSCDBase):
    '''
     (Huang et al.’s) Fast Multi-Scale Community Detection Tools
        
    *Arguments*
        scale_param: scale parameter values (e.g.[1,2], [1:1:10])
        
        extra_param: optional extra parameters for the given algorithm
        
        verbose: verbose level (default=0, max=2)

        The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:
          1. Merging threshold beyond which communities are merged. Value must be in [0,1]. (default 0.5)
          
    *Reference* 
        Huang, Jianbin, et al. "Towards online multiresolution community detection in large-scale networks." PloS one 6.8 (2011): e23829.
    
        Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD_HSLSW"):
        super(MSCD_HSLSW, self).__init__(name, prog="HSLSW") 


class MSCD_LFK(_MSCDBase):
    '''
     (Lancichinetti et al.’s) Fast Multi-Scale Community Detection Tools
        
    *Arguments*
        scale_param: scale parameter values (e.g.[1,2], [1:1:10])
        
        extra_param: optional extra parameters for the given algorithm
        
        verbose: verbose level (default=0, max=2)
        
        The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:
          1. Merging threshold beyond which communities are merged. Value must be in [0,1]. (default 0.5)
          2. When growing a community, maximum number of neighbours from the sorted list of candidate nodes that can fail to join before the failures makes the growth stop. (default: infinite / value 0)
          3. When growing a community, maximum number of iterations through all nodes during which nodes can be removed. (default: infinite / value 0)
          
          Ex: To merge communities with 30% of overlapping nodes
          
              mscd -g network.edges -w -c coms -p 0.3 -a LFK [1:-0.01:0]

    *Reference* 
        Lancichinetti, Andrea, Santo Fortunato, and János Kertész. "Detecting the overlapping and hierarchical community structure in complex networks." New Journal of Physics 11.3 (2009): 033015.
    
        Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD_LFK"):
        super(MSCD_LFK, self).__init__(name, prog="LFK") 


class MSCD_LFK2(_MSCDBase):
    '''
     ( Lancichinetti et al.’s multi-threaded ) Fast Multi-Scale Community Detection Tools
        
    *Arguments*
    
        scale_param: scale parameter values (e.g.[1,2], [1:1:10])
        extra_param: optional extra parameters for the given algorithm
        verbose: verbose level (default=0, max=2)
        
        The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:

          1. Merging threshold beyond which communities are merged. Value must be in [0,1]. (default 0.5)
          2. Maximum number of additional threads the program can use (default: number of cores available / value 0)
          3. Maximum number of seeds to start growing communities. (default: infinite / value 0)
          4. Recursive level of seed neighbours not to use as seeds must be 0, 1 or 2. (default 1) (i.e. with 1, all the neighbours of a seed cannot be added as a seed)
          
    *Reference* 
        Lancichinetti, Andrea, Santo Fortunato, and János Kertész. "Detecting the overlapping and hierarchical community structure in complex networks." New Journal of Physics 11.3 (2009): 033015.
        
        Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD_LFK2"):
        super(MSCD_LFK2, self).__init__(name, prog="LFK2") 


class MSCD_AFG(_MSCDBase):
    '''
     (Arenas et al.’s) Fast Multi-Scale Community Detection Tools
        
    *Arguments*
        scale_param: scale parameter values (e.g.[1,2], [1:1:10])
        
        extra_param: optional extra parameters for the given algorithm
        
        verbose: verbose level (default=0, max=2)
    
    *Reference* 
        Arenas, Alex, Alberto Fernandez, and Sergio Gomez. "Analysis of the structure of complex networks at different resolution levels." New Journal of Physics 10.5 (2008): 053039.
        
        Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD_AFG"):
        super(MSCD_AFG, self).__init__(name, prog="AFG") 
        

class MSCD_RN(_MSCDBase):
    '''
     (Ronhovde and Nussinov’s) Fast Multi-Scale Community Detection Tools
        
    *Arguments*
        scale_param: scale parameter values (e.g.[1,2], [1:1:10])
        
        extra_param: optional extra parameters for the given algorithm
        
        verbose: verbose level (default=0, max=2)
    
    *Reference* 
        Ronhovde, Peter, and Zohar Nussinov. "Local resolution-limit-free Potts model for community detection." Physical Review E 81.4 (2010): 046114.
        
        Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD_RN"):
        super(MSCD_RN, self).__init__(name, prog="RN")         

        
class MSCD_SO(_MSCDBase):
    '''
      stability optimisation (Fast Multi-Scale Community Detection Tools)
        
    *Arguments*
        scale_param: scale parameter values (e.g.[1,2], [1:1:10])
        
        extra_param: optional extra parameters for the given algorithm
        
        verbose: verbose level (default=0, max=2)
        
        The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:

          1. edge threshold (for walks of length>1 computed edges below this value are discarded) (default: 0)
          2. memory saving mode (for walks of length>1 the number of networks kept in memory) (default: 0, i.e. off)
          
          Ex: mscd -g network.edges -w -c coms -p 0.01,1 -a SO [0:0.1:5]
          
    *Reference* 
        Le Martelot, Erwan, and Chris Hankin. "Multi-scale community detection using stability optimisation within greedy algorithms." arXiv preprint arXiv:1201.3307 (2012).
        
        Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD_SO"):
        super(MSCD_SO, self).__init__(name, prog="SO")         

                
class MSCD_SOM(_MSCDBase):
    '''
      tability optimisation using matrices  (Fast Multi-Scale Community Detection Tools)
        
    *Arguments*
        scale_param: scale parameter values (e.g.[1,2], [1:1:10])
        
        extra_param: optional extra parameters for the given algorithm
        
        verbose: verbose level (default=0, max=2)
        
        The optional extra parameters must be given in order as a list with ',' between values and no space. The parameters are:

          1. memory saving mode (for walks of length>1 the number of networks kept in memory) (default: 0, i.e. off)

          Ex: mscd -g network.edges -w -c coms -p 1 -a SOM [0:0.1:5]
    
    *Reference* 
        Le Martelot, Erwan, and Chris Hankin. "Multi-scale community detection using stability optimisation within greedy algorithms." arXiv preprint arXiv:1201.3307 (2012).
        
        Le Martelot, Erwan, and Chris Hankin.  "Fast multi-scale detection of relevant communities in large-scale networks." The Computer Journal 56.9 (2013): 1136-1150.
    '''

    def __init__(self, name="MSCD_SOM"):
        super(MSCD_SOM, self).__init__(name, prog="SOM")    
        
        
class SVINET(Clustering):
    '''
     SVINET implements sampling based algorithms that derive from stochastic variational inference under the (assortative) mixed-membership stochastic blockmodel.
        
    *Arguments*
    
        SVINET: fast stochastic variational inference of undirected networks
        
        svinet [OPTIONS]
            ===============         ===========================================================================
            -file <name>            input tab-separated file with a list of undirected links
            -n <N>                  number of nodes in network
            -k <K>                  number of communities
            -batch                  run batch variational inference
            -stratified             use stratified sampling, use with rpair or rnode options
            -rnode                  inference using random node sampling
            -rpair                  inference using random pair sampling
            -link-sampling          inference using link sampling 
            -infset                 inference using informative set sampling
            -rfreq                  set the frequency at which  (convergence is estimated;  statistics, e.g., heldout likelihood are computed)
            -max-iterations         maximum number of iterations (use with -no-stop to avoid stopping in an earlier iteration)
            -no-stop                disable stopping criteria
            -seed                   set GSL random generator seed
            ===============         ===========================================================================
    
    *Reference* 
        Prem K. Gopalan, David M. Blei. Efficient discovery of overlapping communities in massive networks. To appear in the Proceedings of the National Academy of Sciences, 2013
    '''

    def __init__(self, name="SVINET"):
        super(SVINET, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'SVINET' }

    def run(self, data, num_cluster=None, inference="link-sampling", stratified=False, rfreq=None, max_iterations=None, no_stop=False, seed=None):
        assert inference in ['link-sampling', 'batch', 'rnode', 'rpair', 'infset']
        if stratified: assert inference in ['rnode', 'rpair']
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        if seed is None:
            seed = np.random.randint(999999)
        params = {'num_cluster':num_cluster, 'seed':seed, 'stratified':stratified, "rfreq":rfreq, "max_iterations":max_iterations, 'no_stop':no_stop, 'inference':inference}
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        clusters = {}
        n_node = data.num_node

        def estimate_num_cluster():
            with utils.TempDir() as tmp_dir:
                utils.link_file(data.file_edges, tmp_dir, "edges.txt")
                cmd = ["{}".format(config.get_cdc_prog('2013-svinet', data.is_directed))]
                cmd.append('-file {}'.format('edges.txt'))
                cmd.append('-n {}'.format(n_node))
                cmd.append('-k {}'.format(n_node))
                if max_iterations: cmd.append('-max-iterations {}'.format(max_iterations))
                if data.is_weighted(): cmd.append('-weighted')
                cmd.append('-findk')
                cmd .append('&& (cat n*findk/communities_size.txt | wc -l  > num_cluster.txt) ')
                cmd = " ".join(cmd)
                with open(os.path.join(tmp_dir, "tmpcmd"), 'wt') as f:
                    f.write(cmd + "\n")
                    
                self.logger.info("Running " + cmd)
                
                timecost, status = utils.timeit(lambda: utils.shell_run_and_wait("bash -x tmpcmd", tmp_dir))
                if status != 0: 
                    raise Exception("Run command with error status code {}".format(status))
                with open(os.path.join(tmp_dir, "num_cluster.txt")) as f:
                    n = int(f.readlines()[0].strip())
                self.logger.info("Find k=%d  in %f seconds" % (n, timecost))
                return n

        if num_cluster is None or num_cluster < 1:
                num_cluster = estimate_num_cluster()
                    
        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = ["{}".format(config.get_cdc_prog('2013-svinet', data.is_directed))]
            cmd.append('-file {}'.format('edges.txt'))
            cmd.append('-n {}'.format(n_node))
            cmd.append('-k {}'.format(num_cluster))
            if data.is_weighted(): cmd.append('-weighted')
            cmd.append('-' + inference)
            if stratified: cmd.append('-stratified')
            if rfreq: cmd.append('-rfreq {}'.format(rfreq))
            if max_iterations: cmd.append('-max-iterations {}'.format(max_iterations))
            if no_stop: cmd.append('-no-stop')
            if seed:  cmd.append('-seed {}'.format(seed))
            cmd = " ".join(cmd)
                
            self.logger.info("Running " + cmd)
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            outputfile = glob.glob(os.path.join(tmp_dir, 'n{}-k{}-*-seed{}-*'.format(n_node, num_cluster, seed), 'communities.txt'))[0]
            self.logger.info("read output form " + outputfile)
            with open (os.path.join(tmp_dir, outputfile), "r") as output:
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

