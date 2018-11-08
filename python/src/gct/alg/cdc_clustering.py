'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.alg.clustering import Clustering, save_result
from gct import utils, config
import os
import subprocess
import multiprocessing

prefix = 'cdc'


class CliquePercolation(Clustering):
    '''
    The sequential clique percolation algorithm is method for detecting clique percolation communities. 
    It is an alternative to CFinder: instead of finding maximal cliques in a graph and producing communities 
    of all the possible clique sizes, the SCP algorithm finds all the cliques of single size and produces 
    the community structure for all the possible thresholds. 
    The SCP algorithm should work well even for large sparse networks, 
    but might have trouble for dense networks and cliques of large size.
    
    Arguments
    --------------------
    Usage: ./k_clique [inputfile] [options]
    Options:
            -k=[clique size] : The size of the clique.
            -v : Verbose mode.
            
    ------------------------
    Kumpula, Jussi M., et al. "Sequential algorithm for fast clique percolation." Physical Review E 78.2 (2008): 026109.
    '''

    def __init__(self, name="CliquePercolation"):
        
        super(CliquePercolation, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'CliquePercolation' }

    def run(self, data, k=None, verbose=False, seed=None):
        if (data.is_directed()):
            raise Exception("only undirected is supported")
        
        params = {'k':k}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()

        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = [config.get_cdc_prog('k_clique', data.is_directed)]
            cmd.append("edges.txt")
            if verbose: cmd.append('-v')
            if k is not None: cmd.append("-k={}".format(k))
            if data.is_weighted(): cmd.append("-w")
            if k is not None: cmd.append("-o=output")

            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        clusters = {}
        for i, line in enumerate(lines):
            if line:
                clusters[i] = [int(u) for u in line.split(" ")]
        
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

class Connected_Iterative_Scan(Clustering):
    '''
    Connected Iterative Scan Connected Iterative Scan is also known at times as Locally Optimal Sets.
    
    Arguments
    --------------------
    ./cis -i network -o output -dl delimiter -s seed file -l lambda value

    ------------------------
    Kelley, Stephen. The existence and discovery of overlapping communities in large-scale networks. 
    Diss. Rensselaer Polytechnic Institute, 2009.
    '''

    def __init__(self, name="Connected_Iterative_Scan"):
        
        super(Connected_Iterative_Scan, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'Connected_Iterative_Scan' }

    def run(self, data, l=None, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        params = {'l':l}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()

        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = [config.get_cdc_prog('2009-cis', data.is_directed)]
            cmd.append("-i edges.txt -o output")
            if l is not None: cmd.append("-l {}".format(l))

            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        clusters = {}
        for i, line in enumerate(lines):
            if line:
                clusters[i] = [int(u) for u in line.split("|")]
        
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
    
    
class EAGLE(Clustering):
    '''
    EAGLE (agglomerativE hierarchicAl clusterinG based on maximaL cliquE)
    
    Arguments
    --------------------
    Sinopsi: ./2009-eagle nThreads src <dir|undir> [dest]

    ------------------------
    Shen, Huawei, et al. "Detect overlapping and hierarchical community structure in networks." 
    Physica A: Statistical Mechanics and its Applications 388.8 (2009): 1706-1712.
    '''

    def __init__(self, name="EAGLE"):
        
        super(EAGLE, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"cdc", "name": 'EAGLE' }

    def run(self, data, nThread=None, seed=None):
        if False and (data.is_directed()):
            raise Exception("only undirected is supported")
        
        if nThread is None or nThread<1:
            nThread= max(1,multiprocessing.cpu_count()-1)
        params = {'nThread':nThread}
        if seed  is not None: self.logger.info("seed ignored")
        
        if not utils.file_exists(data.file_edges):
            data.to_edgelist()

        with utils.TempDir() as tmp_dir:
            utils.link_file(data.file_edges, tmp_dir, "edges.txt")
            cmd = [config.get_cdc_prog('2009-eagle', data.is_directed)]
            cmd.append(str(nThread))
            cmd.append("edges.txt")
            cmd.append("dir" if data.is_directed() else "undir")
            cmd.append("output")
            cmd = " ".join(cmd)
            self.logger.info("Running " + cmd)
            
            timecost, status = utils.timeit(lambda: utils.shell_run_and_wait(cmd, tmp_dir))
            if status != 0: 
                raise Exception("Run command with error status code {}".format(status))
            
            with open (os.path.join(tmp_dir, "output"), "r") as output:
                lines = [u.strip() for u in output.readlines()]

        clusters = {}
        n_cluster=int(lines[0])
        for i, line in enumerate(lines[1:]):
            if line:
                clusters[i] = [int(u) for u in line.split(" ")[1:]]
        assert(len(clusters)==n_cluster)
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
    
    
