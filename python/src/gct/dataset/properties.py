'''
Created on Oct 31, 2018

@author:  Lizhen Shi
'''

import numpy as np
import pandas as pd   
from gct.alg.clustering import Result
import sys


class GraphProperties(object):

    def __init__(self, data):
        if data.is_directed() or data.is_weighted():
            print ("Warning! Graph will be taken as undirected and unweighted.")
        self.data = data 

    def set_if_not_exists(self, name, fun):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            print ("call fun for " + name)
            value = fun()
            setattr(self, name, value)
            return value 
        
    @property    
    def directed(self):
        return self.data.directed
    
    @property
    def edges(self):
        return self.set_if_not_exists("_edges", lambda: self.data.get_edges())
    
    @property
    def weighted(self):
        return self.data.weighted    
    
    @property 
    def num_edges(self):
        return self.edges.shape[0]
    
    @property 
    def num_vectices(self):
        return self.set_if_not_exists("_num_vetices", lambda: len(set(np.unique(self.edges[['src', 'dest']].values))))

    @property
    def density1(self):
        m, n = self.num_edges, self.num_vectices
        assert n > 1
        return float(m) / n
        
    @property
    def density(self):
        m, n = self.num_edges, self.num_vectices
        assert n > 1
        return float(m) * 2 / n / (n - 1)
    
    @property
    def degrees(self):

        def f():
            arr = self.edges[['src', 'dest']].values.ravel() 
            unique, counts = np.unique(arr, return_counts=True)
            return dict(zip(unique, counts))

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)


class GraphClustersProperties(object):

    def __init__(self, data, clusterobj):
        if data.is_directed() or data.is_weighted():
            print ("Warning! Graph will be taken as undirected and unweighted.")
        if isinstance(clusterobj, Result):
            self.clusters = clusterobj.clusters(as_dataframe=True)
        elif isinstance(clusterobj, pd.DataFrame):
            self.clusters = clusterobj
        else:
            raise Exception("Unsupported " + str(type(clusterobj)))
        self.data = data 

    def set_if_not_exists(self, name, fun):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            print ("call fun for " + name)
            value = fun()
            setattr(self, name, value)
            return value 
    
    @property
    def edges(self):
        prop_name = "_" + sys._getframe().f_code.co_name 
        return self.set_if_not_exists(prop_name, lambda: self.data.get_edges())
    
    @property 
    def num_edges(self):
        return self.edges.shape[0]
    
    @property 
    def num_vectices(self):
        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, lambda: len(set(np.unique(self.edges[['src', 'dest']].values))))

    @property 
    def num_clusters(self):
        return len(self.cluser_indexes)
    
    @property 
    def cluser_indexes(self):
        # prop_name = "_" + sys._getframe().f_code.co_name        
        # return self.set_if_not_exists(prop_name, lambda: list(sorted((set(np.unique(self.clusters['cluster'].values))))))
        return self.cluser_sizes.keys()    
    
    @property 
    def cluser_sizes(self):
        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, lambda: self.clusters[['node', 'cluster']].groupby('cluster')['node'].count().to_dict())

    @property
    def cluser_edge_sizes(self):

        def f():
            df = self.edges[['src', 'dest']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df['is_intra'] = (df['src_c'] == df['dest_c']).astype(np.float)

            a = df[['src_c', 'is_intra']].groupby('src_c')['is_intra'].sum().to_dict()
            return a 
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        
    
    @property
    def intra_cluster_densities(self):

        def f():
            r = {}
            d = self.cluser_edge_sizes
            for cluster, n_node in self.cluser_sizes.items():
                n_edge = d[cluster]
                a = float(n_edge) * 2 / n_node / (n_node - 1) if n_node > 1 else 0.0
                r[cluster] = a
            return r 

        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        
    
    @property
    def intra_cluster_density(self):
        return np.mean(list(self.intra_cluster_densities.values()))    
    
    @property
    def inter_cluster_density(self):
        n_intra_edges = np.sum(list(self.cluser_edge_sizes.values()))
        n_edge = self.num_edges
        n = self.num_vectices
        d = n * (n - 1) - np.sum([u * (u - 1) for u in self.cluser_sizes.values()])
        return float(n_edge - n_intra_edges) * 2 / d
    
