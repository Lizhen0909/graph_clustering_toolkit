'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import ClusteringAlg, save_result
from gct import utils, config
import os

prefix='mcl'

class MCL(ClusteringAlg):
    '''
    A wrapper of *MCL (Markov Cluster Algorithm)* from https://micans.org/mcl/
    
    Arguments
        Since there are a lot options for mcl. refer to https://micans.org/mcl/man/mcl.html for all of them.
        However only specify algrithm options, don't specify file/folder/format related option.
    
    Reference
        Stijn van Dongen, Graph Clustering by Flow Simulation. PhD thesis, University of Utrecht, May 2000
    '''
    def __init__(self, name="mcl"):
        
        super(MCL, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"mcl", "name": 'mcl' }

    def run(self, data, **kwargs):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        params = dict(kwargs)
        if "seed" in params:
            if params['seed'] is not None:
                self.logger.info("seed ignored")
            del params['seed']
            
        #params['abc'] = '' 
        params['o'] = 'output'
        params = {u:v for u, v in params.items() if v is not None }
        
        if not utils.file_exists(data.file_mcl_mci):
            data.to_mcl_mci()
            if not utils.file_exists(data.file_mcl_mci):
                raise Exception("failed to crate mcl mci format file")
        

        with utils.TempDir() as tmp_dir:
            cmd1 = "{} {} {}".format(config.MCL_PROG, data.file_mcl_mci,
                " ".join(['{}{} {}'.format('-' if len(u) == 1 else '--', u, v).strip() for u, v in params.items()]))
            cmd2 = "{} -imx {} -o cluster.output".format(config.MCLDUMP_PROG, 'output')
            cmdfile = os.path.join(tmp_dir,"tmpcmd.sh")
            with open(cmdfile,'wt') as f :
                f.write(cmd1+"\n")            
                f.write(cmd2+"\n")
            self.logger.info("Running " + cmd1)
            self.logger.info("Running " + cmd2)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait("bash "+cmdfile, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "cluster.output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        from collections import defaultdict
        clusters = defaultdict(list)
        for line in lines:
            cluster,node=line.split("\t")[:2]
            clusters[int(cluster)].append(int(node))
        
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
    
