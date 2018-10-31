'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import glob
import numpy as np 


class seq_louvain(Clustering):

    def __init__(self, name="dct-seq_louvain"):
        super(seq_louvain, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"dct", "name": 'seq_louvain' }
    
    def run(self, data, seed=None):
        self.logger.warning("dct::seq_louvain assumes node starts with zero and is continuous")
        if seed is None:
            seed = np.random.randint(999999)
        params = {'seed':seed}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()()
        
        with utils.TempDir() as tmp_dir:
            pajek = utils.link_file(data.file_edges, dest_dir=tmp_dir, destname='edges.txt')
            cmd = "{} -f -s {} -o output {}".format(config.get_dct_prog('seq_louvain'), seed, pajek)            
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = tmp_dir + "/output"
            import pandas as pd 
            output = pd.read_csv(outputfile, sep=" ", header=None)
            output.columns = ['cluster']
            output['node'] = range(len(output))
        clusters = output[['cluster', 'node']]
        clusters = clusters.groupby('cluster').apply(lambda u: list(u['node'])).to_dict()
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

    
class infomap(Clustering):

    def __init__(self, name="dct-infomap"):
        super(infomap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"dct", "name": 'infomap' }
    
    def run(self, data, seed=None):
        self.logger.warning("dct::seq_louvain assumes node starts with zero and is continuous")
        if seed is None:
            seed = np.random.randint(999999)
        params = {'seed':seed}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()()
        
        with utils.TempDir() as tmp_dir:
            pajek = utils.link_file(data.file_edges, dest_dir=tmp_dir, destname='edges.txt')
            cmd = "{} -f -s {} -o output {}".format(config.get_dct_prog('infomap', data.is_directed()), seed, pajek)            
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = tmp_dir + "/output"
            import pandas as pd 
            output = pd.read_csv(outputfile, sep=" ", header=None)
            output.columns = ['cluster']
            output['node'] = range(len(output))
        clusters = output[['cluster', 'node']]
        clusters = clusters.groupby('cluster').apply(lambda u: list(u['node'])).to_dict()
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


class dct(Clustering):

    def __init__(self, name=None, progname='dlplm'):
        if name is None: name = "dct-" + progname
        super(dct, self).__init__(name) 
        self.progname = progname
    
    def get_meta(self):
        return {'lib':"dct", "name": self.progname }
    
    def run(self, data, seed=None):
        self.logger.warning("dct assumes node starts with zero and is continuous")
        if seed is None:
            seed = np.random.randint(999999)
        params = {'seed':seed, 'prog':self.progname}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()()
        
        with utils.TempDir() as tmp_dir:
            #tmp_dir = "/tmp/abc"
            pajek = utils.link_file(data.file_edges, dest_dir=tmp_dir, destname='edges.txt')
            cmd = "{} {}".format(config.get_dct_prog(self.progname, data.is_directed()), pajek)            
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir, env={'SEED':str(seed)}))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfiles = glob.glob(tmp_dir + "/output*.cluster")
            import pandas as pd 
            df_from_each_file = (pd.read_csv(f, sep=" ", header=None) for f in outputfiles)
            output = pd.concat(df_from_each_file, ignore_index=True)
            output.columns = ['node', 'cluster']
        clusters = output[['cluster', 'node']]
        clusters = clusters.groupby('cluster').apply(lambda u: list(u['node'])).to_dict()
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
