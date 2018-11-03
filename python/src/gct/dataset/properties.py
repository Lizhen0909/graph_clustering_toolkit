'''
Created on Oct 31, 2018

@author:  Lizhen Shi
'''

import numpy as np
import pandas as pd   
from gct.alg.clustering import Result
import sys
from gct.dataset import convert
from gct.dataset.dataset import Cluster


class GraphProperties(object):

    def __init__(self, data):
        if data.is_directed() or data.is_weighted():
            print ("Warning! Graph will be taken as undirected.")
        self.data = data 

    def set_if_not_exists(self, name, fun):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            # print ("call fun for " + name)
            value = fun()
            setattr(self, name, value)
            return value 
        
    @property    
    def directed(self):
        return self.data.directed
    
    @property
    def edges(self):

        def f():
            df = self.data.get_edges()
            if not self.data.is_weighted():
                df['weight'] = float(1)
            return df 

        return self.set_if_not_exists("_edges", f)
    
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
        return self.weighted_degrees()
    
    @property
    def unweighted_degrees(self):

        def f():
            arr = self.edges[['src', 'dest']].values.ravel() 
            unique, counts = np.unique(arr, return_counts=True)
            return dict(zip(unique, counts))

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)

    @property
    def weighted_degrees(self):

        def f():
            df1 = self.edges[['src', 'weight']]
            df2 = self.edges[['dest', 'weight']]
            df2.columns = df1.columns
            df = pd.concat([df1, df2])
            return df.groupby('src')['weight'].sum().to_dict()

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)


class GraphClustersProperties(object):

    def __init__(self, data, clusterobj):
        if data.is_directed() or data.is_weighted():
            print ("Warning! Graph will be taken as undirected and unweighted.")
        if isinstance(clusterobj, Cluster):
            self.clusterobj = clusterobj
        elif isinstance(clusterobj, Result):
            self.clusterobj = Cluster(clusterobj.clusters(as_dataframe=True))
        elif isinstance(clusterobj, pd.DataFrame) or isinstance(clusterobj, list) \
            or isinstance(clusterobj, np.ndarray) or isinstance(clusterobj, str) or isinstance(clusterobj, dict):
            self.clusterobj = Cluster(clusterobj)
        else:
            raise Exception("Unsupported " + str(type(clusterobj)))
        self.data = data 
        self.clusters = self.clusterobj.value()

    def set_if_not_exists(self, name, fun):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            # print ("call fun for " + name)
            value = fun()
            setattr(self, name, value)
            return value 
    
    @property
    def edges(self):

        def f():
            df = self.data.get_edges()
            if not self.data.is_weighted():
                df['weight'] = float(1)
            return df         

        prop_name = "_" + sys._getframe().f_code.co_name 
        return self.set_if_not_exists(prop_name, f)
    
    @property 
    def num_edges(self):
        return self.edges.shape[0]
    
    @property 
    def num_vectices(self):
        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, lambda: len(set(np.unique(self.edges[['src', 'dest']].values))))

    '''
    degree for each node
    '''    

    @property
    def node_degrees(self):
        return self.unweighted_degrees

    '''
    sum weight for each node
    '''

    @property
    def node_weights(self):
        return self.weighted_degrees

    @property
    def sum_weight(self):
        return np.sum(list(self.node_weights.values()))
        
    @property
    def unweighted_degrees(self):

        def f():
            arr = self.edges[['src', 'dest']].values.ravel() 
            unique, counts = np.unique(arr, return_counts=True)
            return dict(zip(unique, counts))

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)

    @property
    def weighted_degrees(self):

        def f():
            df1 = self.edges[['src', 'weight']]
            df2 = self.edges[['dest', 'weight']]
            df2.columns = df1.columns
            df = pd.concat([df1, df2])
            return df.groupby('src')['weight'].sum().to_dict()

        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, f)

    @property 
    def num_clusters(self):
        return len(self.cluster_indexes)
    
    @property 
    def cluster_indexes(self):
        return self.cluster_sizes.keys()    
    
    @property 
    def cluster_sizes(self):
        prop_name = "_" + sys._getframe().f_code.co_name        
        return self.set_if_not_exists(prop_name, lambda: self.clusters[['node', 'cluster']].groupby('cluster')['node'].count().to_dict())
    
    @property 
    def cluster_sum_intra_weights(self):

        def f():
            df = self.edges[['src', 'dest', 'weight']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df = df [(df['src_c'] == df['dest_c'])]

            a = df[['src_c', 'weight']].groupby('src_c')['weight'].sum() * 2
            return a.to_dict()
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        

    @property 
    def cluster_sum_weighted_degrees(self):

        def f():
            df = self.clusters[['node', 'cluster']]
            d = self.weighted_degrees
            df['wd'] = df['node'].map(d)
            return df.groupby("cluster")['wd'].sum().to_dict()
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        
        
    @property
    def cluster_edge_sizes(self):

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
    def cluster_out_sum_weights(self):

        def f():
            df = self.edges[['src', 'dest', 'weight']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df = df[(df['src_c'] != df['dest_c'])]
            
            a = df.groupby('src_c')[['weight']].sum().reset_index()
            b = df.groupby('dest_c')[['weight']].sum().reset_index() 
            b.columns = a.columns
            a = pd.concat([a, b]).groupby('src_c').sum()
            return a['weight'].to_dict()
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)
        
    @property
    def cluster_expansions(self):
        if self.data.is_weighted():
            raise Exception("only support unweighted graph")

        def f():
            ow = self.cluster_out_sum_weights
            cs = self.cluster_sizes
            return {u:v / cs[u] for u, v in ow.items()}
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)        

    @property
    def cluster_cut_ratios(self):
        d = self.cluster_sizes
        n = self.num_vectices
        return {u:v / float(n - d[u]) for u, v in self.cluster_expansions.items()}
    
    @property
    def intra_cluster_densities(self):
        if self.data.is_weighted():
            raise Exception("only support unweighted graph")
        return self.unweighted_intra_cluster_densities
    
    @property
    def unweighted_intra_cluster_densities(self):

        def f():
            r = {}
            d = self.cluster_edge_sizes
            for cluster, n_node in self.cluster_sizes.items():
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
        if self.data.is_weighted():
            raise Exception("only support unweighted graph")        
        return self.inter_unweighted_cluster_density
    
    @property
    def inter_unweighted_cluster_density(self):
        n_intra_edges = np.sum(list(self.cluster_edge_sizes.values()))
        n_edge = self.num_edges
        n = self.num_vectices
        d = n * (n - 1) - np.sum([u * (u - 1) for u in self.cluster_sizes.values()])
        return float(n_edge - n_intra_edges) * 2 / d

    @property
    def relative_cluster_densities(self):

        def f():
            df = self.edges[['src', 'dest', 'weight']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df['is_intra'] = (df['src_c'] == df['dest_c'])
            df['is_inter'] = (df['src_c'] != df['dest_c'])

            a = df[df['is_intra']].groupby('src_c')['weight'].sum()
            b = df[df['is_inter']].groupby('src_c')['weight'].sum()
            c = df[df['is_inter']].groupby('dest_c')['weight'].sum()

            newdf = pd.concat([a, b, c], axis=1).fillna(0)
            newdf.columns = ['intra', 'inter1', 'inter2']
            newdf['density'] = newdf['intra'] / (newdf['inter1'] + newdf['inter2'] + newdf['intra'])
            
            return newdf['density'].to_dict()
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)       

    @property
    def snap_modularities(self):
        import snap

        def f():
            G = convert.to_snap(self.data)
            m = self.num_edges
            ret = {}
            for k, v in self.clusters.groupby('cluster')['node'].apply(lambda u: list(u)).to_dict().items():
                Nodes = snap.TIntV()
                for nodeId in v:
                    Nodes.Add(nodeId)
                    print (nodeId, m)
                mod = snap.GetModularity(G, Nodes, 1024)
                ret[k] = mod 
            return ret 

        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)       

    @property
    def modularity(self):
        return self.modularity2

    @property
    def modularity2(self):  # another formula

        def f():
            c = self.sum_weight
            d = 1.0 / (c * c)
            a = np.sum(list(self.cluster_sum_intra_weights.values())) / c
            b = np.sum([u * u * d for u in self.cluster_sum_weighted_degrees.values()])
            return a - b
            
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)
           
    @property
    def conductance(self):  # another formula

        def f():
            a = self.cluster_out_sum_weights
            d = self.cluster_sum_intra_weights
            return {u:v / (v + d[u]) for u, v in a.items() }
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)       
        
    @property
    def normalized_cut(self):  # another formula

        def f():
            m = self.sum_weight
            a = self.cluster_out_sum_weights
            d = self.cluster_sum_intra_weights
            return {u:v / (v + d[u]) + v / (v + m - d[u]) for u, v in a.items() }
                
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f)       
    
    @property
    def cluster_max_out_degree_fraction(self):
        return self.cluster_out_degree_fraction[0]

    @property
    def cluster_avg_out_degree_fraction(self):
        return self.cluster_out_degree_fraction[1]

    @property
    def cluster_flake_out_degree_fraction(self):
        return self.cluster_out_degree_fraction[2]    
        
    @property
    def cluster_out_degree_fraction(self):

        def f1():
            df = self.edges[['src', 'dest', 'weight']]
            df2 = self.edges[['dest', 'src', 'weight']]
            df2.columns = df.columns 
            df = pd.concat([df, df2]);del df2 
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df1 = df[(df['src_c'] != df['dest_c'])].drop(['dest_c', 'dest'], axis=1)
            df1 = df1.groupby(['src_c', 'src'])["weight"].sum().reset_index()
            df1.columns = ['cluster', 'node', 'inter_weight']
            df2 = df[(df['src_c'] == df['dest_c'])].drop(['dest_c', 'dest'], axis=1)
            df2 = df.groupby(['src_c', 'src'])["weight"].sum().reset_index()
            df2.columns = ['cluster', 'node', 'intra_weight']
            df = pd.merge(df1, df2, on=['cluster', 'node'], how='outer')
            return df

        def f2():
            df = f1()
            df['odf'] = df['inter_weight'] / (df['inter_weight'] + df['intra_weight'])
            df['flake'] = (df['inter_weight'] > df['intra_weight']).astype(np.float)
            max_odf = df.groupby('cluster')['odf'].max().to_dict()
            avg_odf = df.groupby('cluster')['odf'].mean().to_dict()
            flake_odf = df.groupby('cluster')[['flake']].sum()
            d = self.cluster_sizes
            flake_odf['cluster_size'] = flake_odf.index.map(d)
            flake_odf = (flake_odf['flake'] / flake_odf['cluster_size']).to_dict()
            return max_odf, avg_odf, flake_odf

        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f2)
        
    @property
    def separability(self):
        a = self.cluster_out_sum_weights
        b = self.cluster_sum_intra_weights
        return {u:b[u] / float(v) for u, v in a.items() }
        
    @property
    def cluster_clustering_coefficient(self):

        def f1(edges):
            import igraph 
            g = igraph.Graph(edges=edges[['src', 'dest']].values.tolist(), directed=False) 
            return g.transitivity_undirected()

        def f2():
            df = self.edges[['src', 'dest']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df = df[(df['src_c'] == df['dest_c'])]
            
            ret = {}
            for i in self.cluster_indexes:
                edges = df[df['src_c'] == i]
                ret[i] = f1(edges)
            return ret 
        
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f2)

    @property
    def cluster_local_clustering_coefficient(self):

        def f1(edges):
            import igraph 
            g = igraph.Graph(edges=edges[['src', 'dest']].values.tolist(), directed=False) 
            return g.transitivity_local_undirected()

        def f2():
            df = self.edges[['src', 'dest']]
            c_df = self.clusters[['node', 'cluster']].set_index('node')['cluster'].to_dict()
            df['src_c'] = df['src'].map(c_df) 
            df['dest_c'] = df['dest'].map(c_df)
            df = df[(df['src_c'] == df['dest_c'])]
            
            ret = {}
            for i in self.cluster_indexes:
                edges = df[df['src_c'] == i]
                print (edges.shape) 
                ret[i] = f1(edges)
            return ret 
        
        prop_name = "_" + sys._getframe().f_code.co_name
        
        return self.set_if_not_exists(prop_name, f2)
    
