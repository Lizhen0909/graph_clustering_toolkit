from gcb import utils, config
import pandas as pd
import numpy as np  
import json 
from . import dataset 
import snap 
import os
 
    
class RandomDataset(dataset.Dataset):        

    def __init__(self, name, description="",
                 with_ground_truth=False, directed=False, weighted=False,
                 params=None):
        super(RandomDataset, self).__init__(name, description)
        assert params is not None 
        self.params = params 
        self.with_ground_truth = with_ground_truth
        self.directed = directed
        self.weighted = weighted
        
        meta_file = config.get_data_file_path(self.name, 'meta.info')
        if not utils.file_exists(meta_file):
            json.dump(self.get_meta(), open(meta_file, 'wt')) 

    def get_meta(self):
        d = dataset.Dataset.get_meta(self)
        d['params'] = self.params 
        return d             
    
    def has_ground_truth(self):
        return self.with_ground_truth
    
    def is_directed(self):
        return self.directed
    
    def is_weighted(self):
        return self.weighted
    
    def generate(self):
        params = self.params
        if params['name'] == 'Erdos-Renyi':
            gtype = snap.PNGraph if params['directed'] else snap.PUNGraph
            g = snap.GenRndGnm(gtype , params['n_node'], params['n_edge'])
            lst = [] 
            for EI in g.Edges():
                lst.append([EI.GetSrcNId(), EI.GetDstNId()])
            self.edges = pd.DataFrame(lst, columns=['src', 'dest'])
        elif params['name'] == 'LFR':
            with utils.TempDir() as tmpdir:
                program = config.LFR_PROG
                cmd = program + " " + " ".join([ "-" + str(u[0]) + " " + str(u[1]) for u in params.items() if u[1] is not None])
                self.logger.info("Runing " + cmd)
                self.logger.info("working dir: " + tmpdir)
                utils.shell_run_and_wait(cmd, working_dir=tmpdir)

                edgefile = "LFR.nsa" if self.is_directed() else "LFR.nse"
                edgefile = os.path.join(tmpdir, edgefile)
                if self.is_weighted():
                    edges = pd.read_csv(edgefile, sep='\t', header=None, skiprows=1, dtype={2:np.float})
                    edges.columns = ['src', 'dest', 'weight']                    
                else:
                    edges = pd.read_csv(edgefile, sep='\t', header=None, skiprows=1, usecols=[0, 1])
                    edges.columns = ['src', 'dest']
                
                gtfile = "LFR.nmc"
                gtfile = os.path.join(tmpdir, gtfile)
                gt = pd.read_csv(gtfile, sep='\t', header=None)
                gt.columns = ['node', 'cluster']
                self.edges, self.ground_truth = self.make_offset_0(edges, gt)   
                self.load()             
        else :
            raise Exception("unknown " + params['name'])
    
    def make_offset_0(self, edges, gt):
        min_node = edges[['src', 'dest']].min().min()
        if min_node != 0:
            self.logger.info("min node is {}. will make it 0".format(min_node))
            edges['src'] = edges['src'] - min_node
            edges['dest'] = edges['dest'] - min_node
            if gt is not None:
                gt['node'] = gt['node'] - min_node 
            return edges, gt
        else:
            return edges, gt

    def get_edges(self):
        fname = self.parq_edges
        if utils.file_exists(fname):
            return self.edges_from_parq()
        else:
            if not  hasattr(self, 'edges'):
                self.generate()
            edges = self.edges
            
            self.logger.info("Loaded {} edges".format(len(edges)))
            self.logger.info("The graph have {} nodes".format(len(set(edges.values.ravel()))))
            self.logger.info("\n" + str(edges.head()))
            return edges 
                         
    # return
    def get_ground_truth(self):
        if self.has_ground_truth():
            fname = self.parq_ground_truth
            if utils.file_exists(fname):
                return self.ground_from_parq()
            else:
                if not  hasattr(self, 'ground_truth'):
                    self.generate()
                ground_truth = self.ground_truth
            
                n_node = len(set(ground_truth['node']))
                n_cluster = len(set(ground_truth['cluster']))
                self.logger.info("Loaded {} nodes that have ground truth".format(n_node))  
                self.logger.info("The graph have  {} clusters".format(n_cluster))
                self.logger.info("Mean cluster size: {}".format(float(ground_truth.shape[0]) / n_cluster))
                self.logger.info("Mean #membership: {}".format(ground_truth.groupby('node').count().mean()[0]))
                self.logger.info("\n" + str(ground_truth.head()))
                return ground_truth
                        
        else:
            raise Exception("graph has no ground truth")
        

def generate_Erdos_Renyi(name, n_node, n_edge, directed=False):
    params = {"name":"Erdos-Renyi", 'n_node':n_node, "n_edge":n_edge, "directed": directed}
    return RandomDataset(name, description="Erdos_Renyi random graph", with_ground_truth=False,
                          weighted=False, directed=directed, params=params)

'''
./benchmark [FLAG] [P]

To set the parameters, type:
-N        [number of nodes]
-k        [average degree]
-maxk        [maximum degree]
-mut        [mixing parameter for the topology]
-muw        [mixing parameter for the weights]
-beta        [exponent for the weight distribution]
-t1        [minus exponent for the degree sequence]
-t2        [minus exponent for the community size distribution]
-minc        [minimum for the community sizes]
-maxc        [maximum for the community sizes]
-on        [number of overlapping nodes]
-om        [number of memberships of the overlapping nodes]
-C        [Average clustering coefficient]
-cnl        [output communities as strings of nodes (input format for NMI evaluation)]
-name        [base name for the output files]. It is used for the network, communities and statistics; files extensions are added automatically:
    .nsa  - network, represented by space/tab separated arcs
    .nse  - network, represented by space/tab separated edges
    {.cnl, .nmc}  - communities, represented by nodes lists '.cnl' if '-cnl' is used, otherwise as a nodes membership in communities '.nmc')
    .nst  - network statistics
-seed        [file name of the random seed, default: seed.txt]
-a        [{0, 1} yield directed network (1 - arcs) rather than undirected (0 - edges), default: 0 - edges]
'''

    
def generate_LFR(name, N, k=None, maxk=None, mut=None, muw=None, beta=None, t1=None, t2=None, minc=None, maxc=None,
                 on=None, om=None, C=None, a=0, weighted=False):
    params = locals()
    params['a'] = int(a)
    params['name'] = 'LFR'
    del params['weighted']
    
    return RandomDataset(name, description="LFR random graph", with_ground_truth=True ,
                          weighted=weighted, directed=(a > 0), params=params)    
 
