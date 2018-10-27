'''
Created on Oct 26, 2018

@author: lizhen
'''
from gcb import utils
from gcb.ds.dataset import DefaultDataset
import pandas as pd 


def from_nodelist(name, edgelist , directed=False , description=""):
    assert len(edgelist) > 0, "Error, empty edgelist"
    if len(edgelist[0]) == 2:
        weighted = False 
    elif len(edgelist[0]) == 3:
        weighted = True 
    else:
        raise Exception("Format not right")
    
    return DefaultDataset(name=name, edges=edgelist, weighted=weighted, directed=directed, description=description)

    
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
def from_networkx(name, graph, weighted=False, data='weight', default=1, description=""):
    directed = graph.is_directed()
    lst = []
    if weighted:
        for e in graph.edges(data=data, default=default):
            lst.append(e)
    else:
        for e in graph.edges():
            lst.append(e)
    
    return DefaultDataset(name, edges=lst, weighted=weighted, directed=directed, description=description)


# turn a dataset into a igraph graph
def to_igraph(data):
    import igraph 
    edges = data.get_edges()
    
    g = igraph.Graph(edges=edges[['src', 'dest']].values.tolist(), directed=data.is_directed()) 
    if data.is_weighted():
        g.es["weight"] = edges['weight'].values 

    return g


# turn  a networkx graph into a dataset 
def from_igraph(name, graph, data='weight', description=""):
    directed = graph.is_directed()
    weighted = graph.is_weighted()
    
    lst = []
    for e in graph.es:
        lst.append(e.tuple)
    df = pd.DataFrame(lst, columns=['src', 'dest'])
    if weighted:
        w = graph.es[data]
        df['weight'] = w 
    
    return DefaultDataset(name, edges=df, weighted=weighted, directed=directed, description=description)


# turn a dataset into a snap graph
def to_snap(data):
    import snap
    if 1 and utils.file_exists(data.file_snap):
        FIn = snap.TFIn(data.file_snap)
        if data.is_directed():
            graph= snap.TNGraph.Load(FIn)
        else: 
            graph = snap.TUNGraph.Load(FIn)
        return graph 

    if data.is_weighted():
        raise Exception("weighted graph is not supported well on snap")
    fname = data.file_edges 
    if not utils.file_exists(fname):
        data.to_edgelist()

    if data.is_directed():
        return snap.LoadEdgeList(snap.PNGraph, fname, 0, 1)
    else:
        return snap.LoadEdgeList(snap.PUNGraph, fname, 0, 1)

    
# turn  a snap graph into a dataset 
def from_snap(name, graph, description=""):
    import snap 
    if isinstance(graph, snap.PUNGraph):
        directed = False 
    elif isinstance(graph, snap.PNGraph):
        directed = True 
    else:
        raise Exception("Unkown graph type: " + str(type(graph)))
    
    lst = []
    for EI in graph.Edges():
        lst.append([EI.GetSrcNId(), EI.GetDstNId()])

    df = pd.DataFrame(lst, columns=['src', 'dest'])
    
    return DefaultDataset(name, edges=df, weighted=False, directed=directed, description=description)    

