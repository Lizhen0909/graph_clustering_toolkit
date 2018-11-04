'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os

prefix='mcl'

class MCL(Clustering):
    '''
    A wrapper of *MCL (Markov Cluster Algorithm)* from `https://micans.org/mcl/`
    
    Arguments
    --------------------
    Since there are a lot options for mcl. refer to https://micans.org/mcl/ for all of them.
    However only specify algrithm options, don't specify file/folder/format related option.
    ------------------------
    Stijn van Dongen, Graph Clustering by Flow Simulation. PhD thesis, University of Utrecht, May 2000
    '''
    def __init__(self, name="mcl"):
        
        super(MCL, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"mcl", "name": 'mcl' }

    def run(self, data, **kwargs):
        if (data.is_directed()):
            raise Exception("only undirected is supported")
        
        params = dict(kwargs)
        params['abc'] = '' 
        params['o'] = 'output'
        params = {u:v for u, v in params.items() if v is not None }
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        cmd = "{} {} {}".format(config.MCL_PROG, data.file_edges,
            " ".join(['{}{} {}'.format('-' if len(u) == 1 else '--', u, v).strip() for u, v in params.items()]))
        self.logger.info("Running " + cmd)

        with utils.TempDir() as tmp_dir:
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        from collections import defaultdict
        clusters = defaultdict(list)
        for c, line in enumerate(lines):
            if line.startswith('#'):continue
            for n in line.split("\t"): 
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
    
