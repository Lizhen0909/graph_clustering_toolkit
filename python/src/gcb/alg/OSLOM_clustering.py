'''
Created on Oct 27, 2018

@author: lizhen
'''
from gcb.alg.clustering import Clustering, save_result
from gcb import utils, config
import subprocess
import os
import glob
import multiprocessing
import numpy as np 
from random import random


class Infomap(Clustering):

    def __init__(self, name="oslom_infomap"):
        super(Infomap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"OSLOM", "name": 'infomap' }
    
    def run(self, data, seed=None):
        if seed is None:
            seed = np.random.randint(999999)
        params = {'seed':seed}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_pajek):
            data.to_pajek()
        
        with utils.TempDir() as tmp_dir:
            pajek = os.path.join(tmp_dir, 'pajek.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_pajek, pajek)
            cmd = "{} {} {} {}".format(config.get_OSLOM_prog('infomap', data.is_directed()), seed, pajek, 1)            
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = glob.glob(tmp_dir + "/pajek.tree")[0]
            import pandas as pd 
            output = pd.read_csv(outputfile, sep=" ", skiprows=1, header=None)
            output['cluster'] = output.loc[:, 0].map(lambda u: int(u.split(':')[0]))
            output['node'] = output.loc[:, 2].astype(np.int)
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
    

class Infohiermap(Clustering):

    def __init__(self, name="oslom_infohiermap"):
        super(Infohiermap, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"OSLOM", "name": 'Infohiermap' }
    
    def run(self, data, seed=None):
        if seed is None:
            seed = np.random.randint(999999)
        params = {'seed':seed}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_pajek):
            data.to_pajek()
        
        with utils.TempDir() as tmp_dir:
            pajek = os.path.join(tmp_dir, 'pajek.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_pajek, pajek)
            cmd = "{} {} {} {}".format(config.get_OSLOM_prog('Infohiermap', data.is_directed()), seed, pajek, 1)            
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = glob.glob(tmp_dir + "/pajek.tree")[0]
            import pandas as pd 
            output = pd.read_csv(outputfile, sep=" ", skiprows=1, header=None)
            output['cluster'] = output.loc[:, 0].map(lambda u: int(u.split(':')[0]))
            output['node'] = output.loc[:, 2].astype(np.int)
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
    
    
class lpm(Clustering):

    def __init__(self, name="oslom_lpm"):
        super(lpm, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"OSLOM", "name": 'lpm' }
    
    def run(self, data, seed=None):
        if seed is None:
            seed = np.random.randint(999999)
        params = {'seed':seed}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            pajek = os.path.join(tmp_dir, 'edges.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_edges, pajek)
            cmd = "{} -f {} -r {} -seed {}".format(config.get_OSLOM_prog('lpm', data.is_directed()), pajek, 1, seed)            
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = pajek + 'part'
            with open(outputfile) as f:
                lines = [u.strip() for u in f]
            lines = [[int(v) for v in u.split("\t")] for u in lines]
            
        clusters = dict(enumerate (lines))
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
    

class louvain_method(Clustering):

    def __init__(self, name="oslom_louvain_method"):
        super(louvain_method, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"OSLOM", "name": 'louvain_method' }
    
    def run(self, data, seed=None):
        if seed is None:
            seed = np.random.randint(999999)
        params = {'seed':seed}
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            pajek = os.path.join(tmp_dir, 'edges.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_edges, pajek)
            cmd = "{} -f {} -r {} -seed {}".format(config.get_OSLOM_prog('louvain_method', data.is_directed()), pajek, 1, seed)            
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = os.path.join(tmp_dir, 'tp')
            with open(outputfile) as f:
                lines = [u.strip() for u in f]
            lines = [[int(v) for v in u.split("\t")] for u in lines]
            
        clusters = dict(enumerate (lines))
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


class modopt(Clustering):

    def __init__(self, name="oslom_modopt"):
        super(modopt, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"OSLOM", "name": 'modopt' }
    
    def run(self, data, seed=None, lamb=1, trials=5, temp_step=0.999, initial_temp=1e-6):
        params = locals()
        del params['data'];del params['self']
        if seed is None:
            seed = np.random.randint(999999)
        params ['seed'] = seed 
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            tmp_dir = "/tmp/abc"
            pajek = os.path.join(tmp_dir, 'edges.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_edges, pajek)
            cmd = "{} {} {} {} {} {} {}".format(config.get_OSLOM_prog('modopt', data.is_directed()),
                                                pajek,
                                                seed,
                                                lamb,
                                                trials,
                                                temp_step,
                                                initial_temp
                                                )            
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = pajek + "part"
            with open(outputfile) as f:
                lines = [u.strip() for u in f]
            lines = [[int(v) for v in u.split("\t")] for u in lines]
            
        clusters = dict(enumerate (lines))
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
