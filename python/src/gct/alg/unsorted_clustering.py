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
        result['algname'] = self.name
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
        result['algname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
