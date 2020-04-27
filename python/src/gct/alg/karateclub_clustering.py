'''
Created on Apr 27, 2020
include a few algorithms mentioned at https://karateclub.readthedocs.io
@author: Bo Chen
'''
from gct.alg.clustering import ClusteringAlg, save_result
from gct import utils, config
import os
import json
import glob

import karateclub
 

def run_EdMot(data, kwargs):
    graph = data.to_graph_networkx()
    model = karateclub.EdMot(**kwargs)
    model.fit(graph)
    cluster_membership = model.get_memberships()
    return cluster_membership


def run_SCD(data, kwargs):
    graph = data.to_graph_networkx()
    model = karateclub.SCD(**kwargs)
    model.fit(graph)
    cluster_membership = model.get_memberships()
    return cluster_membership


def run_EgoNetSplitter(data, kwargs):
    graph = data.to_graph_networkx()
    model = karateclub.EgoNetSplitter(**kwargs)
    model.fit(graph)
    cluster_membership = model.get_memberships()
    return cluster_membership


def run_DANMF(data, kwargs):
    graph = data.to_graph_networkx()
    model = karateclub.DANMF(**kwargs)
    model.fit(graph)
    cluster_membership = model.get_memberships()
    return cluster_membership


def run_NNSED(data, kwargs):
    graph = data.to_graph_networkx()
    model = karateclub.NNSED(**kwargs)
    model.fit(graph)
    cluster_membership = model.get_memberships()
    return cluster_membership


def run_MNMF(data, kwargs):
    graph = data.to_graph_networkx()
    model = karateclub.MNMF(**kwargs)
    model.fit(graph)
    cluster_membership = model.get_memberships()
    return cluster_membership


def run_BigClam(data, kwargs):
    graph = data.to_graph_networkx()
    model = karateclub.BigClam(**kwargs)
    model.fit(graph)
    cluster_membership = model.get_memberships()
    return cluster_membership


def run_SymmNMF(data, kwargs):
    graph = data.to_graph_networkx()
    model = karateclub.SymmNMF(**kwargs)
    model.fit(graph)
    cluster_membership = model.get_memberships()
    return cluster_membership


prefix = 'karateclub'


class SymmNMF(ClusteringAlg):
    '''
    An implementation of “Symm-NMF” from the SDM‘12 paper “Symmetric Nonnegative Matrix Factorization for Graph Clustering”. The procedure decomposed the second power od the normalized adjacency matrix with an ADMM based non-negative matrix factorization based technique. This results in a node embedding and each node is associated with an embedding factor in the created latent space.

    Parameters:    
        dimensions (int) – Number of dimensions. Default is 32.
        iterations (int) – Number of power iterations. Default is 200.
        rho (float) – ADMM tuning parameter. Default is 100.0.

    '''

    def __init__(self, name="SymmNMF"):
        
        super(SymmNMF, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"karateclub", "name": 'SymmNMF' }

    def run(self, data, dimensions=32, iterations=200, rho=100.0, seed=None):
        
        if seed is not None:self.logger.info("seed ignored")

        params = {}
        params['dimensions'] = dimensions
        params['iterations'] = iterations
        params['rho'] = rho
        
        timecost, result = utils.timeit(lambda: run_SymmNMF(data, params))
        clusters = {}
        for k, vv in result.items():
            if isinstance(vv, list):
                for v in vv:
                    v = int(v)
                    if v not in clusters:
                        clusters[v] = []
                    clusters[v].append(k)
            else:
                v = vv
                v = int(v)
                if v not in clusters:
                    clusters[v] = []
                clusters[v].append(k)

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

    
class BigClam(ClusteringAlg):
    '''
    
    An implementation of “BigClam” from the WSDM ‘13 paper “Overlapping Community Detection at Scale: A Non-negative Matrix Factorization Approach”. 
    The procedure uses gradient ascent to create an embedding which is used for deciding the node-cluster affiliations.

    Parameters:    
        dimensions (int) – Number of embedding dimensions. Default 8.
        iterations (int) – Number of training iterations. Default 50.
        learning_rate (float) – Gradient ascent learning rate. Default is 0.005.
    
    '''

    def __init__(self, name="BigClam"):
        
        super(BigClam, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"karateclub", "name": 'BigClam' }

    def run(self, data, dimensions=8, iterations=50, learning_rate=0.005, seed=None):
        
        if seed is not None:self.logger.info("seed ignored")

        params = {}
        params['dimensions'] = dimensions
        params['iterations'] = iterations
        params['learning_rate'] = learning_rate
        
        timecost, result = utils.timeit(lambda: run_BigClam(data, params))
        clusters = {}
        for k, vv in result.items():
            if isinstance(vv, list):
                for v in vv:
                    v = int(v)
                    if v not in clusters:
                        clusters[v] = []
                    clusters[v].append(k)
            else:
                v = vv
                v = int(v)
                if v not in clusters:
                    clusters[v] = []
                clusters[v].append(k)

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
    

class NNSED(ClusteringAlg):
    '''
    An implementation of “NNSED” from the CIKM ‘17 paper “A Non-negative Symmetric Encoder-Decoder Approach for Community Detection”. The procedure uses non-negative matrix factorization in order to learn an unnormalized cluster membership distribution over nodes. The method can be used in an overlapping and non-overlapping way.
    
    Parameters:    
        layers (int) – Embedding layer size. Default is 32.
        iterations (int) – Number of training epochs. Default 10.
        seed (int) – Random seed for weight initializations. Default 42.
    
    '''

    def __init__(self, name="NNSED"):
        
        super(NNSED, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"karateclub", "name": 'NNSED' }

    def run(self, data, dimensions=32, iterations=10, seed=42):

        params = {}
        params['dimensions'] = dimensions
        params['iterations'] = iterations
        params['seed'] = seed
        
        timecost, result = utils.timeit(lambda: run_NNSED(data, params))
        clusters = {}
        for k, vv in result.items():
            if isinstance(vv, list):
                for v in vv:
                    if v not in clusters:
                        clusters[v] = []
                    clusters[v].append(k)
            else:
                v = vv
                if v not in clusters:
                    clusters[v] = []
                clusters[v].append(k)

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


class DANMF(ClusteringAlg):
    '''
    An implementation of “DANMF” from the CIKM ‘18 paper “Deep Autoencoder-like Nonnegative Matrix Factorization for Community Detection”. The procedure uses telescopic non-negative matrix factorization in order to learn a cluster membership distribution over nodes. The method can be used in an overlapping and non-overlapping way.
    
    Parameters:    
        layers (list) – Autoencoder layer sizes in a list of integers. Default [32, 8].
        pre_iterations (int) – Number of pre-training epochs. Default 100.
        iterations (int) – Number of training epochs. Default 100.
        seed (int) – Random seed for weight initializations. Default 42.
        lamb (float) – Regularization parameter. Default 0.01.
    '''

    def __init__(self, name="DANMF"):
        
        super(DANMF, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"karateclub", "name": 'DANMF' }

    def run(self, data, layers=[32, 8], pre_iterations=100, iterations=100, seed=42, lamb=0.01):

        params = {}
        params['layers'] = layers
        params['pre_iterations'] = pre_iterations
        params['iterations'] = iterations
        params['seed'] = seed
        params['lamb'] = lamb
        
        timecost, result = utils.timeit(lambda: run_DANMF(data, params))
        clusters = {}
        for k, vv in result.items():
            if isinstance(vv, list):
                for v in vv:
                    if v not in clusters:
                        clusters[v] = []
                    clusters[v].append(k)
            else:
                v = vv
                if v not in clusters:
                    clusters[v] = []
                clusters[v].append(k)

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
    

class EgoNetSplitter(ClusteringAlg):
    '''
    An implementation of “Ego-Splitting” from the KDD ‘17 paper “Ego-Splitting Framework: from Non-Overlapping to Overlapping Clusters”. The tool first creates the ego-nets of nodes. A persona-graph is created which is clustered by the Louvain method. The resulting overlapping cluster memberships are stored as a dictionary.
    
    Parameters:    
        resolution (float) – Resolution parameter of Python Louvain. Default 1.0.
    '''

    def __init__(self, name="EgoNetSplitter"):
        
        super(EgoNetSplitter, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"karateclub", "name": 'EgoNetSplitter' }

    def run(self, data, resolution=1.0, seed=None):
        
        if seed is not None:self.logger.info("seed ignored")
        
        params = {}
        params['resolution'] = resolution
        
        timecost, result = utils.timeit(lambda: run_EgoNetSplitter(data, params))
        clusters = {}
        for k, vv in result.items():
            for v in vv:
                if v not in clusters:
                    clusters[v] = []
                clusters[v].append(k)

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


class SCD(ClusteringAlg):
    '''
    An implementation of “SCD” from the WWW ‘14 paper “High Quality, Scalable and Parallel Community Detection for Large Real Graphs”. The procedure greedily optimizes the approximate weighted community clustering metric. First, clusters are built around highly clustered nodes. Second, we refine the initial partition by using the approximate WCC. These refinements happen for the whole vertex set.
    
    Parameters:    
        iterations (int) – Refinemeent iterations. Default is 25.
        eps (float) – Epsilon score for zero division correction. Default is 10**-6.
    '''

    def __init__(self, name="SCD"):
        
        super(SCD, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"karateclub", "name": 'SCD' }

    def run(self, data, iterations=25, eps=1e-06, seed=None):
        
        if seed is not None:self.logger.info("seed ignored")
        
        params = {}
        params['iterations'] = iterations
        params['eps'] = eps
        
        timecost, result = utils.timeit(lambda: run_SCD(data, params))
                
        clusters = {}
        for k, v in result.items():
            if v not in clusters:
                clusters[v] = []
            clusters[v].append(k)

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

    
class EdMot(ClusteringAlg):
    '''
    An implementation of “Edge Motif Clustering” from the KDD ‘19 paper “EdMot: An Edge Enhancement Approach for Motif-aware Community Detection”. The tool first creates the graph of higher order motifs. This graph is clustered by the Louvain method. The resulting cluster memberships are stored as a dictionary.
    
    Parameters:    
        component_count (int) – Number of extracted motif hypergraph components. Default is 2.
        cutoff (int) – Motif edge cut-off value. Default is 50.
    
    '''

    def __init__(self, name="EdMot"):
        
        super(EdMot, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"karateclub", "name": 'EdMot' }

    def run(self, data, component_count=2, cutoff=50, seed=None):
        
        if seed is not None:self.logger.info("seed ignored")
        
        params = {}
        params['component_count'] = component_count
        params['cutoff'] = cutoff
        
        timecost, result = utils.timeit(lambda: run_EdMot(data, params))
                
        clusters = {}
        for k, v in result.items():
            if v not in clusters:
                clusters[v] = []
            clusters[v].append(k)

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
    
