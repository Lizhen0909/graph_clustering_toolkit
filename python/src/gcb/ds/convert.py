'''
Created on Oct 26, 2018

@author: lizhen
'''
from gcb import utils
from gcb.ds.dataset import DefaultDataset
import pandas as pd 


# turn a dataset into a networkx graph
def to_networkx(data):
    import networkx as nx 
    fname = data.file_edges 
    if not utils.file_exists(fname):
        data.to_edgelist()
        
    container = nx.DiGraph() if data.is_directed() else nx.Graph()
    if data.is_weighted():
        return nx.read_weighted_edgelist(fname, create_using=container, nodetype=int)
    else:
        return nx.read_edgelist(fname, create_using=container, nodetype=int)


# turn  a networkx graph into a dataset 
def from_networkx(name, graph, weighted=False, data='weight', default=1):
    directed = graph.is_directed()
    lst = []
    if weighted:
        for e in graph.edges(data=data, default=default):
            lst.append(e)
    else:
        for e in graph.edges():
            lst.append(e)
    
    return DefaultDataset(name, edges=lst, weighted=weighted, directed=directed)


# turn a dataset into a igraph graph
def to_igraph(data):
    import igraph 
    edges = data.get_edges()
    
    g = igraph.Graph(edges=edges[['src', 'dest']].values.tolist(), directed=data.is_directed()) 
    if data.is_weighted():
        g.es["weight"] = edges['weight'].values 

    return g


# turn  a networkx graph into a dataset 
def from_igraph(name, graph, data='weight'):
    directed = graph.is_directed()
    weighted = graph.is_weighted()
    
    lst = []
    for e in graph.es:
        lst.append(e.tuple)
    df = pd.DataFrame(lst, columns=['src', 'dest'])
    if weighted:
        w = graph.es[data]
        df['weight'] = w 
    
    return DefaultDataset(name, edges=df, weighted=weighted, directed=directed)
