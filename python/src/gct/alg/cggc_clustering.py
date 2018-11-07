'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os

prefix = 'cgcc'

class CGGC(Clustering):
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
    
    def __init__(self, name="CGGC"):
        
        super(CGGC, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"CGCC", "name": 'CGCC' }
    
    def run(self, data, startk=None, finalk=None, runs=None, ensemblesize=None, algorithm=None, seed=None):
        if False and (data.is_directed() or data.is_weighted()):
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
        result['runname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
    
