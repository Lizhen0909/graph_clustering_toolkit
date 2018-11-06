'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os
import glob
from gct.dataset import convert

prefix = 'alg'


class streamcom(Clustering):
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

    def __init__(self, name="streamcom"):
        
        super(streamcom, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"streamcom", "name": 'streamcom' }
    
    def run(self, data, vmax_start=None, vmax_end=None, c=None, niter=None, seed=None):
        if False and (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        params = locals()
        del(params['self']);del(params['data'])
        params['f'] = data.file_edges
        params['o'] = 'output'
        params = {u.replace("_", "-"):v for u, v in params.items() if v is not None }
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        cmd = "{} {} {}".format(config.STREAMCOM_PROG,
            " ".join(['{}{} {}'.format('-' if len(u) == 1 else '--', u, v) for u, v in params.items()]), data.file_edges)
        self.logger.info("Running " + cmd)

        with utils.TempDir() as tmp_dir:
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            output = glob.glob(os.path.join(tmp_dir, "output*"))[0]
            with open (os.path.join(tmp_dir, output), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        from collections import defaultdict
        clusters = defaultdict(list)
        for c, line in enumerate(lines):
            if line.startswith('#'):continue
            for n in line.split(" "): 
                clusters[c].append(int(n))
        
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

    
class Paris(Clustering):
    '''
    A wrapper of *paris* algorithm from https://github.com/tbonald/paris 

    Arguments
    --------------------
    None
            
    Reference
    ------------------------
    Bonald, Thomas, et al. "Hierarchical Graph Clustering using Node Pair Sampling." arXiv preprint arXiv:1806.01664 (2018).
    '''    

    def __init__(self, name="pairs"):
        
        super(Paris, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"paris", "name": 'paris' }
    
    def run(self, data, vmax_start=None, vmax_end=None, c=None, niter=None, seed=None):
        if False and (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        
        def fun():        
            paris = utils.try_import("paris", config.MODULE_PARIS_PATH)
            G = convert.to_networkx(data)
            D = paris.paris(G, copy_graph=False)
            uu = utils.try_import("utils", config.MODULE_PARIS_PATH)
            best = uu.best_clustering(D)
            return  best

        timecost, res = utils.timeit(fun)
        
        params = {}
        
        clusters = dict(enumerate(res))
        
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


class lso_cluster(Clustering):
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

    def __init__(self, name="lso_cluster"):
        
        super(lso_cluster, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"lso_cluster", "name": 'lso_cluster' }
    
    def run(self, data, **kwargs):
        if False and (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        params = dict(kwargs)
        params = {u:v for u, v in params.items() if v is not None }
        
        if "loss" not in params: params['loss'] = 'modularity'
        argparams = dict(params)
        if argparams['loss'] in ['pmod', 'mom']: 
            if argparams['loss'] not in argparams:
                raise Exception("You have to specify pmod=<val> or mom=<val> for the loss function")
            loss_args = "--loss {{{},{}}}".format(argparams['loss'], argparams[argparams['loss']])
            del argparams[argparams['loss']];del argparams['loss']
             
        else:
            loss_args = "--loss {}".format(argparams["loss"])
            del argparams['loss']

        if not utils.file_exists(data.file_edges):
            data.to_edgelist()()
        
        with utils.TempDir() as tmp_dir:
            pajek = utils.link_file(data.file_edges, dest_dir=tmp_dir, destname='edges.txt')
            cmdargs = ["--{} {}".format(u, v) for u, v in argparams.items()]
            cmdargs.append(loss_args)
            cmdargs.append("-o lsooutput")
            cmdargs = " ".join(cmdargs)
            cmd = "{} {} {}".format(config.LSO_CLUSTER_PROG, pajek, cmdargs)
            with open(os.path.join(tmp_dir, "tmpcmd"), 'wt') as f: f.write(cmd)
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait("bash -x ./tmpcmd", tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfiles = tmp_dir + "/lsooutput"
            import pandas as pd 
            
            output = pd.read_csv(outputfiles, sep="\t", header=None)
            output.columns = ['node', 'cluster']
        clusters = output
        clusters = clusters.groupby('cluster').apply(lambda u: list(u['node'])).to_dict()
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

