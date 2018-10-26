'''
Created on Oct 26, 2018

@author: lizhen
'''
from gcb import utils
from gcb.ds.dataset import DefaultDataset


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
