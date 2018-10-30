'''
Created on Oct 27, 2018

@author: lizhen
'''
from gcb.alg.clustering import Clustering, save_result
from gcb import utils, config
import os
import glob

class label_propagation(Clustering):

    def __init__(self, name="powergraph_label_propagation"):
        super(label_propagation, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"powergraph", "name": 'label_propagation' }
    
    def run(self, data, execution='async', ncpus=None, scheduler=None, engine_opts=None, graph_opts=None, scheduler_opts=None):
        params = locals();del params['self'];del params['data']
        params = {u:v for u, v in params.items() if v is not None}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            pajek = os.path.join(tmp_dir, 'edges.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_edges, pajek)
            args = " ".join (["--{} {}".format(u, v) for u, v in params.items()])
            cmd = "{} --graph {} --saveprefix=output.cluster {}".format(config.get_powergraph_prog('label_propagation', data.is_directed()), pajek, args)
                        
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
        
            outputfiles = glob.glob(tmp_dir + "/output.cluster.*")
            import pandas as pd 
            df_from_each_file = (pd.read_csv(f, sep="\t", header=None) for f in outputfiles)
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


class GossipMap(Clustering):

    def __init__(self, name="powergraph_GossipMap"):
        super(GossipMap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"powergraph", "name": 'GossipMap' }
    
    def run(self, data, thresh=None, tol=None, maxiter=None, maxspiter=None, trials=None, interval=None, outmode=None, ncpus=None, scheduler=None, engine_opts=None, graph_opts=None, scheduler_opts=None):
        params = locals();del params['self'];del params['data']
        params = {u:v for u, v in params.items() if v is not None}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            tmp_dir = '/tmp/abc'
            pajek = os.path.join(tmp_dir, 'edges.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_edges, pajek)
            args = " ".join (["--{} {}".format(u, v) for u, v in params.items()])
            cmd = "{} --graph {} --prefix output.cluster {}".format(config.get_powergraph_prog('GossipMap', data.is_directed()), pajek, args).strip()
                        
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
        
            outputfiles = glob.glob(tmp_dir + "/output.cluster.*")
            import pandas as pd 
            df_from_each_file = (pd.read_csv(f, sep="\t", header=None) for f in outputfiles)
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
