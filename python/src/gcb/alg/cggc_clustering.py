'''
Created on Oct 27, 2018

@author: lizhen
'''
from gcb.ds import convert
import snap    
from gcb.alg.clustering import Clustering, save_result
from gcb import utils, config
import os


class CGGC(Clustering):

    def __init__(self, name="CGGC"):
        
        super(CGGC, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"CGCC", "name": 'CGCC' }
    
    def run(self, data, startk=None, finalk=None, runs=None, ensemblesize=None, algorithm=None, seed=None):
        if (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        
        params = locals()
        del(params['self']);del(params['data'])
        params['inpfmt'] = 'e' 
        params['outfile'] = 'output'
        params['outfmt'] = 'l'
        params = {u:v for u, v in params.items() if v is not None }
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        cmd = "{} {} {}".format(config.CGGC_PROG, " ".join(['--{}={}'.format(u, v) for u, v in params.items()]), data.file_edges)
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
    
