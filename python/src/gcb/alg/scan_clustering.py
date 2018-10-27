'''
Created on Oct 27, 2018

@author: lizhen
'''
from gcb.alg.clustering import Clustering, save_result
from gcb import utils, config
import subprocess


class Scanpp(Clustering):

    def __init__(self):
        name = "SCAN++"
        super(Scanpp, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"scanpp (no code)", "name": 'scanpp' }
    
    def run(self, data, mu=1, epsilon=0):
        params = {'mu':mu, 'epsilon':epsilon}
        if (data.is_directed() or data.is_weighted()):
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        cmd = "{} -e {} -m {} -r {}".format(config.SCANPP_PROG, epsilon, mu, data.file_edges)
        self.logger.info("Running " + cmd)
        timecost, output = utils.timeit(lambda: subprocess.check_output(cmd.split(" ")))
        if not output.startswith('node'):
            raise Exception("Something wrong with scapp. output:\n" + output)

        output = [u.strip() for u in output.split("\n")][1:]
        output = [u.split("\t") for u in output if u]
        output = [[int(v) for v in u] for u in output]
        
        from collections import defaultdict
        clusters = defaultdict(list)
        for n, c in output:
            clusters[c].append(n)
        
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
    
    def get_result(self):
        if hasattr(self, 'result'):
            return self.result
        else:
            raise Exception("No result found. probably no run has been done")
