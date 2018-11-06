'''
Created on Oct 26, 2018

@author: lizhen
'''
from gct import utils
from gct.dataset.dataset import Dataset
import pandas as pd 
import numpy as np 
from scipy.sparse.coo import coo_matrix


def from_edgelist(name, edgelist , directed=False , description="", overide=True):
    assert len(edgelist) > 0, "Error, empty edgelist"
    if len(edgelist[0]) == 2:
        weighted = False 
    elif len(edgelist[0]) == 3:
        weighted = True 
    else:
        raise Exception("Format not right")
    
    return Dataset(name=name, edgesObj=edgelist, weighted=weighted, directed=directed, description=description, overide=overide)

    
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
def from_networkx(name, graph, weighted=False, data='weight', default=1, description="", overide=True):
    directed = graph.is_directed()
    lst = []
    if weighted:
        for e in graph.edges(data=data, default=default):
            lst.append(e)
    else:
        for e in graph.edges():
            lst.append(e)
    
    return Dataset(name, edgesObj=lst, weighted=weighted, directed=directed, description=description, overide=overide)


# turn a dataset into a igraph graph
def to_igraph(data):
    import igraph 
    edges = data.get_edges()
    
    g = igraph.Graph(edges=edges[['src', 'dest']].values.tolist(), directed=data.is_directed()) 
    if data.is_weighted():
        g.es["weight"] = edges['weight'].values 

    return g


# turn  a networkx graph into a dataset 
def from_igraph(name, graph, data='weight', description="", overide=True):
    directed = graph.is_directed()
    weighted = graph.is_weighted()
    
    lst = []
    for e in graph.es:
        lst.append(e.tuple)
    df = pd.DataFrame(lst, columns=['src', 'dest'])
    if weighted:
        w = graph.es[data]
        df['weight'] = w 
    
    return Dataset(name, edgesObj=df, weighted=weighted, directed=directed, description=description, overide=overide)


# turn a dataset into a snap graph
def to_snap(data):
    import snap
    if 1 and utils.file_exists(data.file_snap):
        FIn = snap.TFIn(data.file_snap)
        if data.is_directed():
            graph = snap.TNGraph.Load(FIn)
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
def from_snap(name, graph, description="", overide=False):
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
    
    return Dataset(name, edgesObj=df, weighted=False, directed=directed, description=description, overide=overide)    


# turn a dataset into a networkit graph
def to_networkit(data):
    import networkit
    fname = data.file_edges 
    if not utils.file_exists(fname):
        data.to_edgelist()
    return networkit.readGraph(fname, fileformat=networkit.Format.EdgeListSpaceZero, directed=data.is_directed())


def to_coo_adjacency_matrix(data, simalarity=False, distance_fun=None):
    edges = data.get_edges()
    rows = edges['src'].values
    cols = edges['dest'].values
    n = int(max(np.max(rows), np.max(cols))) + 1
    if data.is_weighted():
        weight = edges['weight'].values
    else:
        weight = np.ones_like(rows)
    if not simalarity:  # distance
        if distance_fun is None or distance_fun == 'minus':
            weight = -weight
        elif distance_fun == 'exp_minus':
            weight = np.exp(-weight)
        else:
            raise ValueError("unknown " + distance_fun)
    if data.is_directed():
        return coo_matrix((weight, (rows, cols)), shape=[n, n])
    else:
        newX = np.concatenate([weight, weight])
        newrows = np.concatenate([rows, cols])
        newcols = np.concatenate([cols, rows])
        return coo_matrix((newX, (newrows, newcols)), shape=[n, n])


def as_undirected(data, newname, description=""):
    edges = data.get_edges()
    if data.has_ground_truth():
        gt = data.get_ground_truth()
    else:
        gt = None 
    
    return Dataset(name=newname, description=description, groundtruthObj=gt, edgesObj=edges, directed=False,
                    weighted=data.is_weighted(), overide=False)

    
def as_unweight(data, newname, description=""):
    edges = data.get_edges()[['src', 'dest']]
    if data.has_ground_truth():
        gt = data.get_ground_truth()
    else:
        gt = None 
    
    return Dataset(name=newname, description=description, groundtruthObj=gt, edgesObj=edges, directed=data.is_directed(),
                    weighted=False, overide=False)


def as_unweight_undirected(data, newname, description=""):
    edges = data.get_edges()[['src', 'dest']]
    if data.has_ground_truth():
        gt = data.get_ground_truth()
    else:
        gt = None 
    
    return Dataset(name=newname, description=description, groundtruthObj=gt, edgesObj=edges, directed=False,
                    weighted=False, overide=False)
