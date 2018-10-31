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

            def link_file(path, destname=None):
                if destname is None :
                    destname = path.split("/")[-1]
                destpath = os.path.join(tmp_dir, destname)
                utils.remove_if_file_exit(destpath)
                os.symlink(path, destpath)
                return destpath            

            pajek = link_file(data.file_pajek, 'pajek.txt')
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


class copra(Clustering):

    def __init__(self, name="oslom_copra"):
        super(copra, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"OSLOM", "name": 'copra' }
    
    def run(self, data, v=5, v1=None, v2=None, prop=None, repeat=None, mo=None, nosplit=False, extrasimplify=False, q=False):
        assert (v1 is None and v2 is None) or (v1 is not  None and v2 is not None)
        params = locals();del params['self'];del params['data']
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            pajek = os.path.join(tmp_dir, 'edges.txt')
            utils.remove_if_file_exit(pajek)
            os.symlink(data.file_edges, pajek)
            cmd = "java -cp {} COPRA {} -w -v {}".format(config.get_OSLOM_prog('copra', data.is_directed()), pajek, v)
            if (v1 is not  None and v2 is not None): cmd += "-vs {} {}".format(v1, v2)
            if prop is not None: cmd += ' -prop {}'.format(prop)
            if repeat is not None:cmd += ' -repeat {}'.format(repeat)
            if mo is not None:cmd += ' -mo'
            if nosplit is not None:cmd += ' -nosplit'
            if extrasimplify is not None:cmd += ' -extrasimplify'
            if q is not None:cmd += ' -q'
                        
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfile = os.path.join(tmp_dir, 'clusters-edges.txt')
            with open(outputfile) as f:
                lines = [u.strip() for u in f]
            lines = [[int(v) for v in u.split(" ")] for u in lines]
            
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

'''
***************************************************************************************************************************************************
OPTIONS

  [-r R]:                       sets the number of runs for the first hierarchical level, bigger this value, more accurate the output (of course, it takes more). Default value is 10.

  [-hr R]:                      sets the number of runs  for higher hierarchical levels. Default value is 50 (the method should be faster since the aggregated network is usually much smaller).

  [-seed m]:                    sets m equal to the seed for the random number generator. (instead of reading from time_seed.dat)

  [-hint filename]:             takes a partition from filename. The file is expected to have the nodes belonging to the same cluster on the same line.

  [-load filename]:             takes modules from a tp file you already got in a previous run.

  [-t T]:                       sets the threshold equal to T, default value is 0.1

  [-singlet]:                    finds singletons. If you use this flag, the program generally finds a number of nodes which are not assigned to any module.
                                the program will assign each node with at least one not homeless neighbor. This only applies to the lowest hierarchical level.

  [-cp P]:                      sets a kind of resolution parameter equal to P. This parameter is used to decide if it is better to take some modules or their union.
                                Default value is 0.5. Bigger value leads to bigger clusters. P must be in the interval (0, 1).

  [-fast]:                      is equivalent to "-r 1 -hr 1" (the fastest possible execution).

  [-infomap runs]:              calls infomap and uses its output as a starting point. runs is the number of times you want to call infomap.

  [-copra runs]:                same as above using copra.

  [-louvain runs]:              same as above using louvain method.


Please look at ReadMe.pdf for a more detailed explanation.



***************************************************************************************************************************************************
'''


class OSLOM(Clustering):

    def __init__(self, name="oslom_oslom"):
        super(OSLOM, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"OSLOM", "name": 'oslom' }
    
    def run(self, data, seed=None, r=10, hr=50, t=0.1, cp=0.5, fast=False, singlet=False, infomap=False, copra=False , louvain=False, runs=1):
        params = locals()
        del params['data'];del params['self']
        if seed is None:
            seed = np.random.randint(999999)
        params ['seed'] = seed 
        if (data.is_directed() or data.is_weighted()) and False:
            raise Exception("only undirected and unweighted graph is supported")
        if int(infomap) + int(copra) + int(louvain) > 1:
            raise Exception ("only of infomap, corpra, louvain can be true")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()
        
        with utils.TempDir() as tmp_dir:
            # tmp_dir = "/tmp/abc"
            def link_file(path, destname=None):
                if destname is None :
                    destname = path.split("/")[-1]
                destpath = os.path.join(tmp_dir, destname)
                utils.remove_if_file_exit(destpath)
                os.symlink(path, destpath)
                return destpath

            pajek = link_file(data.file_edges)
            if copra:
                _ = link_file(config.get_OSLOM_prog('copra', data.is_directed()))
            if infomap:
                _ = link_file(config.get_OSLOM_prog('infomap_script', True))
                _ = link_file(config.get_OSLOM_prog('infomap', True))
                _ = link_file(config.get_OSLOM_prog('infomap_script', False))
                _ = link_file(config.get_OSLOM_prog('infomap', False))
            if louvain:            
                _ = link_file(config.get_OSLOM_prog('louvain_script', data.is_directed()))
                _ = link_file(config.get_OSLOM_prog('convert', data.is_directed()))
                _ = link_file(config.get_OSLOM_prog('community', data.is_directed()))
                _ = link_file(config.get_OSLOM_prog('hierarchy', data.is_directed()))
            
            cmd = "{} -f {} -{} -r {} -hr {} -seed {} -t {} -cp {}".format(config.get_OSLOM_prog('oslom', data.is_directed()),
                                                pajek,
                                                'w' if data.is_weighted() else 'uw',
                                                r,
                                                hr,
                                                seed,
                                                t,
                                                cp
                                                ) 
            if fast: cmd += " -fast"  
            if singlet: cmd += " -singlet"
            if infomap: cmd += " -infomap {}".format(runs)         
            if copra: cmd += " -copra {}".format(runs)
            if louvain: cmd += " -louvain {}".format(runs)
            
            self.logger.info("Running " + cmd) 
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0:
                raise Exception("Run command with error status code {}".format(status))
    
            outputfiles = glob.glob(os.path.join(tmp_dir, "edges.txt_oslo_files", "tp*"))
            clusters = {}
            for tp in outputfiles:
                fname = tp.split("/")[-1]
                if fname == 'tp':
                    level = 0 
                else:
                    level = int(fname[2:])
                with open(tp) as f:
                    lines = [u.strip() for u in f if not u.startswith('#')]
                    lines = [[int(v) for v in u.split(" ")] for u in lines]
                    clusters[level] = dict(enumerate (lines))
                    
        self.logger.info("Made %d levels of clusters with #clusters %s in %f seconds" % (len(clusters), str([len(u) for u in clusters.values()]), timecost))
        
        result = {}
        result['multilevel'] = True
        result['num_level'] = len(clusters)
        result['algname'] = self.name
        result['params'] = params
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['timecost'] = timecost
        result['clusters'] = clusters 
        save_result(result)
        self.result = result 
        return self
