'''
Created on Oct 31, 2018

@author:  Lizhen Shi
'''

import numpy as np
import pandas as pd   
from gct.alg.clustering import Result
import sys
from gct.dataset import convert
from gct.dataset.dataset import Clustering
from gct import utils, config
import os


class GraphMetrics(object):
    '''
    metrics for a graph. e.g. density, diameter etc.
    
    The class is here just for convenience. It is not powerful and efficient.    
    One may analyze the graph use other graph libraries (e.g. SNAP, igraph, networkit, etc) using converting functions.
    '''

    def __init__(self, data):
        '''
        :param data: a :class:`gct.Dataset` object 
        '''
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
        '''
        Return True if the graph is directed
        '''
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
        '''
        Return True if the graph is weighted
        '''

        return self.data.weighted    
    
    @property 
    def num_edges(self):
        '''
        Return number of edges
        '''
        
        return self.edges.shape[0]
    
    @property 
    def num_vertices(self):
        '''
        Return number of vertices (nodes)
        '''
        return self.set_if_not_exists("_num_vetices", lambda: len(set(np.unique(self.edges[['src', 'dest']].values))))

    @property
    def density1(self):
        '''
        Return density of :math:`\\frac{|E|}{|V|}`
               
        '''
        
        m, n = self.num_edges, self.num_vertices
        assert n > 1
        return float(m) / n
        
    @property
    def density(self):
        '''
        Return density of :math:`\\frac{|E|}{|all\ possible\ edges|}`.
        '''
        
        m, n = self.num_edges, self.num_vertices
        assert n > 1
        return float(m) * 2 / n / (n - 1)
    
    @property
    def degrees(self):
        '''
        return weighted node degrees
        '''
        return self.weighted_degrees()
    
    @property
    def unweighted_degrees(self):
        '''
        return unweighted node degrees (e.g. number of out edges)
        '''

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


class SNAPGraphMetrics(object):
    '''
    metrics for a graph using SNAP
    '''

    def __init__(self, data):
        '''
        :param data: a :class:`gct.Dataset` object 
        '''
        if data.is_directed() or data.is_weighted():
            print ("Warning! Graph will be taken as undirected.")
        self.graph = data.to_graph_snap() 
        import snap 
        self.snap = snap 

    @property
    def degree_histogram(self):
        '''
        return list[(degree,num_node)]
        '''

        def f():
            snap = self.snap 
            DegToCntV = snap.TFltPr64V()
            snap.GetDegCnt(self.graph, DegToCntV)
            ret = []
            for item in DegToCntV:
                ret.append((item.GetVal1(), item.GetVal2()))
            return ret 
    
        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)

    @property
    def degree_in_histogram(self):
        '''
        return list[(degree,num_node)] of in degree
        '''

        def f():
            snap = self.snap 
            DegToCntV = snap.TFltPr64V()
            snap.GetInDegCnt(self.graph, DegToCntV)
            ret = []
            for item in DegToCntV:
                ret.append((item.GetVal1(), item.GetVal2()))
            return ret 
    
        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)
    
    @property
    def degree_out_histogram(self):
        '''
        return list[(degree,num_node)] of out degree
        '''

        def f():
            snap = self.snap 
            DegToCntV = snap.TFltPr64V()
            snap.GetOutDegCnt(self.graph, DegToCntV)
            ret = []
            for item in DegToCntV:
                ret.append((item.GetVal1(), item.GetVal2()))
            return ret 
    
        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)
    
    @property
    def nodes(self):

        def f():
            return [u.GetId() for u in self.graph.Nodes()]

        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)            

    @property
    def num_nodes(self):
        return self.graph.GetNodes()

    @property
    def num_edges(self):
        return self.graph.GetEdges()
    
    @property
    def node_degrees(self):
        '''
        return list[(node,degree)] 
        '''

        def f():
            snap = self.snap 
            nodes = self.nodes 
            V = snap.TInt64V()
            snap.GetDegSeqV(self.graph, V)
            ret = []
            for i in range(0, V.Len()):
                ret.append((nodes[i], V[i]))
            return ret 
    
        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)            
    
    @property
    def num_self_edges(self):
        '''
        return number of self edges 
        '''

        def f():
            snap = self.snap
            return snap.CntSelfEdges(self.graph) 
    
        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)            

    @property
    def scc_distribution(self):
        '''
        return list[(scc_size, count)] for strongly connected components
        '''

        def f():
            snap = self.snap
            ret = []
            ComponentDist = snap.TIntPr64V()
            snap.GetSccSzCnt(self.graph, ComponentDist)
            for comp in ComponentDist:
                ret.append((comp.GetVal1(), comp.GetVal2()))
            return ret  
    
        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)            
    
    @property
    def wcc_distribution(self):
        '''
        return list[(cc_size, count)] for weakly connected components
        '''

        def f():
            snap = self.snap
            ret = []
            ComponentDist = snap.TIntPr64V()
            snap.GetWccSzCnt(self.graph, ComponentDist)
            for comp in ComponentDist:
                ret.append((comp.GetVal1(), comp.GetVal2()))
            return ret  
    
        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)            
    
    @property
    def edge_bridges(self):
        '''
        return list[edge] where edge is a bridge.
        
        An edge is a bridge if, when removed, increases the number of connected components.
        '''

        def f():
            snap = self.snap
            ret = []
            EdgeV = snap.TIntPr64V()
            snap.GetEdgeBridges(self.graph, EdgeV)
            for edge in EdgeV:
                ret.append((edge.GetVal1(), edge.GetVal2()))
            return ret 

        prop_name = "_" + sys._getframe().f_code.co_name        
        return utils.set_if_not_exists(self, prop_name, f)            

    def effect_diameter(self, n_node=100 , isDir=False):
        '''
        Returns the (approximation of the) Effective Diameter (90-th percentile of the distribution of shortest path lengths) of a graph
        
        :param n_node: number of nodes to sample
        :param isDir: consider direct or not
         
        '''
        snap = self.snap
        n_node = min(self.num_nodes, n_node)
        diam = snap.GetBfsEffDiam(self.graph, n_node, isDir)
        return diam             

    def diameter(self, n_node=100 , isDir=False):
        '''
        Computes the diameter, or ‘longest shortest path’, of a Graph
        
         This diameter is approximate, as it is calculated with an n_node number of random starting nodes.
         
        :param n_node: number of nodes to sample
        :param isDir: consider direct or not
         
        '''

        snap = self.snap
        n_node = min(self.num_nodes, n_node)
        diam = snap.GetBfsFullDiam(self.graph, n_node, isDir)
        return diam
    
    def sample_shortest_path(self, n_node=100 , isDir=False):
        '''
        sample diameter, e.g. ‘shortest path’, of a Graph
        
        :param n_node: number of nodes to sample
        :param isDir: consider direct or not
         
        '''

        snap = self.snap
        n_node = min(self.num_nodes, n_node)
        nodes = self.nodes
        src = np.random.choice(nodes, n_node, replace=False)
        dest = np.random.choice(nodes, n_node, replace=False)
        ret = []
        for i in range(n_node):
            Length = snap.GetShortPath(self.graph, int(src[i]), int(dest[i]))
            ret.append(Length)
        return ret
    
    def sample_degree_centrality(self, n_node=100):
        '''
         Degree centrality of a node is defined as its degree/(N-1), where N is the number of nodes in the network.
        
        :param n_node: number of nodes to sample
        
        '''
        snap = self.snap
        n_node = min(self.num_nodes, n_node)
        nodes = self.nodes
        src = np.random.choice(nodes, n_node, replace=False)
        ret = []
        for i in range(n_node):
            DegCentr = snap.GetDegreeCentr(self.graph, int(src[i]))
            ret.append(DegCentr)
        return ret

    def sample_betweenness_centrality(self, quality=1, isDir=False):
        '''
         Computes (approximate) Node and Edge Betweenness Centrality based on a sample
        
        :param quality: Quality of the approximation. 1.0 gives exact betweenness values.

        :param isDir: consider direct or not
        
        '''
        snap = self.snap
        Nodes = snap.TIntFlt64H()
        Edges = snap.TIntPrFlt64H()
        snap.GetBetweennessCentr(self.graph, Nodes, Edges, float(quality), isDir)
        node_btwn = []
        edge_btwn = []
        for node in Nodes:
            node_btwn.append(Nodes[node])
        for edge in Edges:
            edge_btwn.append(Edges[edge])
        return (node_btwn, edge_btwn)

    def sample_nodes(self, n_node):
        nodes = self.nodes
        return np.random.choice(nodes, min(len(nodes), n_node), replace=False)
        
    def sample_closeness_centrality(self, n_node=100, normalized=True, isDir=False):
        '''
        Returns closeness centrality sample in Graph. Closeness centrality is equal to 1/farness centrality.
        
        :param n_node: number of nodes to sample
        :param normalized: Output should be normalized (True) or not (False).
        :param isDir: consider direct or not
        
        '''
        snap = self.snap
        ret = [] 
        for node in self.sample_nodes(n_node):
            CloseCentr = snap.GetClosenessCentr(self.graph, int(node), normalized, isDir)
            ret.append(CloseCentr)
            
        return ret 
    
    def sample_farness_centrality(self, n_node=100, normalized=True, isDir=False):
        '''
        Returns farness centrality sample in Graph. Farness centrality of a node is the average shortest path length to all other nodes that reside in the same connected component as the given node.

        :param n_node: number of nodes to sample
        :param normalized: Output should be normalized (True) or not (False).
        :param isDir: consider direct or not
        
        '''
        snap = self.snap
        ret = [] 
        for node in self.sample_nodes(n_node):
            CloseCentr = snap.GetFarnessCentr(self.graph, int(node), normalized, isDir)
            ret.append(CloseCentr)
            
        return ret     

    def page_rank_score(self, C=0.85, Eps=1e-4, MaxIter=100):
        '''
        Computes the PageRank score of every node in Graph

        :param C: Damping factor.
        :param Eps: Convergence difference.
        :param MaxIter: Maximum number of iterations.
        
        '''
        snap = self.snap
        
        ret = []
        PRankH = snap.TIntFlt64H()
        snap.GetPageRank(self.graph, PRankH, C, Eps, MaxIter)
        for item in PRankH:
            ret.append((item, PRankH[item]))
             
        return ret     

    def  hubs_and_authorities_score(self , MaxIter=20):
        '''
        Computes the Hubs and Authorities score of every node in Graph

        return tuple of hubs score and authorrities score
        :param MaxIter: Maximum number of iterations.
        
        '''
        snap = self.snap
        
        ret1 = []
        ret2 = []
        NIdHubH = snap.TIntFlt64H()
        NIdAuthH = snap.TIntFlt64H()        
        snap.GetHits(self.graph, NIdHubH, NIdAuthH, MaxIter)
        for item in NIdHubH:
            ret1.append((item, NIdHubH[item]))
        for item in NIdAuthH:
            ret2.append((item, NIdAuthH[item]))
            
        return ret1, ret2   
    
    def  sample_node_eccentricity (self , n_node=100, normalized=True, isDir=False):
        '''
        Returns node eccentricity, the largest shortest-path distance from the node to any other node in the Graph.

        return tuple of hubs score and authorrities score
        :param MaxIter: Maximum number of iterations.
        
        '''
        snap = self.snap
        
        nodes = self.sample_nodes(n_node)
        ret = []
        for node in nodes :
            ret.append(snap.GetNodeEcc(self.graph , int(node), isDir))
        return ret 

    def  eigenvector_centrality(self, Eps=1e-4, MaxIter=100):
        '''
        Computes eigenvector centrality of all nodes in Graph. 
        Eigenvector Centrality of a node N is defined recursively as the average of centrality values of N’s neighbors in the network.
        
        :param Eps: Convergence difference.
        :param MaxIter: Maximum number of iterations.
        
        '''
        snap = self.snap
        
        ret = []
        
        NIdEigenH = snap.TIntFlt64H()
        snap.GetEigenVectorCentr(self.graph, NIdEigenH, Eps, MaxIter)
        for item in NIdEigenH:
            ret.append((item, NIdEigenH[item]))
                    
        return ret  
    
    def  average_clustering_coefficient(self, sample_node=False):
        '''
        Computes the average clustering coefficient as defined in Watts and Strogatz, Collective dynamics of ‘small-world’ networks

        :param sample_node:  compute clustering coefficient only for a random sample of SampleNodes nodes. Useful for approximate but quick computations.
        '''
        snap = self.snap
        GraphClustCoeff = snap.GetClustCf (self.graph, -1 if not sample_node else 1)
        return  GraphClustCoeff

    def  distribution_clustering_coefficient(self, sample_node=False):
        '''
        Computes the distribution of clustering coefficient as defined in Watts and Strogatz, Collective dynamics of ‘small-world’ networks

        :param sample_node:  compute clustering coefficient only for a random sample of SampleNodes nodes. Useful for approximate but quick computations.
        '''
        snap = self.snap
        
        CfVec = snap.TFltPr64V()
        Cf = snap.GetClustCf(self.graph, CfVec, -1 if not sample_node else 1)
        ret = []
        for pair in CfVec:
            ret.append((pair.GetVal1(), pair.GetVal2()))
                    
        return Cf, ret 
    
    def k_core(self, K):
        '''
        Returns the K-core of the graph Graph. If the core of order K does not exist, the function returns an empty graph.
        '''
        KCore = self.snap.GetKCore(self.graph, K)
        return KCore 
        
