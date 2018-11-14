'''
Created on Oct 26, 2018

@author: lizhen
'''
from gct import utils
from gct.dataset.dataset import Dataset
import pandas as pd 
import numpy as np 
from scipy.sparse.coo import coo_matrix


def from_edgelist(name, edgelist , groundtruth=None, directed=False , description="", overide=True):
    """
    create a graph from edge list.
    
    :param name:         identifier of the dataset
    :param edgelist:     a 2d list (list of list) or a 2d numpy ndaray in [[src node, target node, weight],...] format.
                         Or a dataframe that has columns of "src","dest","weight". 
                         Weight is optional, if missing it is an unweighted graph.
    :param groundtruth:  None or a 2d list (list of list) or a 2d numpy ndaray in [[node, cluster],...] format.
                         Or a dataframe that has columns of "node","cluster". 
    
    :param directed:     this is a directed graph
    :param description:    discription
    :param overide:        When true and the named dataset already exists, it will be deleted
    
    :rtype: :py:class:`gct.Dataset` 
    
    """
    assert len(edgelist) > 0, "Error, empty edgelist"
    if isinstance(edgelist, pd.DataFrame):
        firstrow = edgelist.iloc[0]
    else:
        firstrow = edgelist[0]
    if len(firstrow) == 2:
        weighted = False 
    elif len(firstrow) == 3:
        weighted = True 
    else:
        raise Exception("Format not right")
    
    return Dataset(name=name, edgesObj=edgelist, groundtruthObj=groundtruth, weighted=weighted, directed=directed, description=description, overide=overide)

    
# turn a dataset into a networkx graph
def to_networkx(data):
    """
    convert the dataset to a networkx graph.
    
    :param data: :py:class:`gct.Dataset`
    :rtype: networkx graph
    """
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
    '''
    create a datast from networkx graph
    
    :param name:         identifier of the dataset
    :param graph:        a networkx graph 
    :param weight:       is it a weighted graph?
    
    :param data:         the name of the edge data which is taken as weights.
    :param default:        default weight if networkx edge data is missing.
    :param description:    discription
    :param overide:        When true and the named dataset already exists, it will be deleted
    
    :rtype: :py:class:`gct.Dataset`
    '''    
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
    """
    convert the dataset to a igraph graph.
    
    :param data: :py:class:`gct.Dataset`
    :rtype: igraph graph
    
    """    
    import igraph 
    edges = data.get_edges()
    g = igraph.Graph(edges=edges[['src', 'dest']].values.tolist(), directed=data.is_directed()) 
    if data.is_weighted():
        g.es["weight"] = edges['weight'].values 

    return g


# turn  a networkx graph into a dataset 
def from_igraph(name, graph, data='weight', description="", overide=True):
    '''
    create a datast from iGraph graph
    
    :param name:         identifier of the dataset
    :param graph:        a igraph graph 
    :param data:         the name of the edge data which is taken as weights. Ignore for unweighted graph.
    :param description:    discription
    :param overide:        When true and the named dataset already exists, it will be deleted
    
    :rtype: :py:class:`gct.Dataset`
    '''    
        
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
    """
    convert the dataset to a SNAP graph.
    
    :param data: :py:class:`gct.Dataset`
    :rtype: SNAP graph
    """    
    import snap
    if 1 and utils.file_exists(data.file_snap):
        FIn = snap.TFIn(data.file_snap)
        if data.is_directed():
            graph = snap.TNGraph.Load(FIn)
        else: 
            graph = snap.TUNGraph.Load(FIn)
        return graph 

    if False and data.is_weighted():
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
    '''
    create a datast from a SNAP graph
    
    :param name:         identifier of the dataset
    :param graph:        a SNAP graph 
    :param description:    discription
    :param overide:        When true and the named dataset already exists, it will be deleted
    
    :rtype: :py:class:`gct.Dataset`
    '''        
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
    """
    convert the dataset to a networkit graph.
    
    :param data: :py:class:`gct.Dataset`
    :rtype: networkit graph
    """    
    import networkit
    fname = data.file_edges 
    if not utils.file_exists(fname):
        data.to_edgelist()
    return networkit.readGraph(fname, fileformat=networkit.Format.EdgeListSpaceZero, directed=data.is_directed())


def to_coo_adjacency_matrix(data, simalarity=False, distance_fun=None):
    '''
    convert the dataset to a sparse coo adjacency matrix.
    
    :param data: :py:class:`gct.Dataset`
    :rtype: scipy coo_matrix
    '''
     
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


def as_undirected(data, newname, description="", overide=False):
    edges = data.get_edges()
    if data.has_ground_truth():
        gt = data.get_ground_truth()
    else:
        gt = None 
    
    return Dataset(name=newname, description=description, groundtruthObj=gt, edgesObj=edges, directed=False,
                    weighted=data.is_weighted(), overide=overide)

    
def as_unweight(data, newname, description="", overide=False):
    edges = data.get_edges()[['src', 'dest']]
    if data.has_ground_truth():
        gt = data.get_ground_truth()
    else:
        gt = None 
    
    return Dataset(name=newname, description=description, groundtruthObj=gt, edgesObj=edges, directed=data.is_directed(),
                    weighted=False, overide=overide)


def as_unweight_undirected(data, newname, description="", overide=False):
    edges = data.get_edges()[['src', 'dest']]
    if data.has_ground_truth():
        gt = data.get_ground_truth()
    else:
        gt = None 
    
    return Dataset(name=newname, description=description, groundtruthObj=gt, edgesObj=edges, directed=False,
                    weighted=False, overide=overide)


def as_mirror_edges(data, newname, description="", overide=False):
    edges1 = data.get_edges()
    edges2 = edges1.copy()
    edges2['src'] = edges1['dest']
    edges2['dest'] = edges1['src']
    edges = pd.concat([edges1, edges2], axis=0)
    if data.has_ground_truth():
        gt = data.get_ground_truth()
    else:
        gt = None 
    
    return Dataset(name=newname, description=description, groundtruthObj=gt, edgesObj=edges, directed=data.is_directed(),
                    weighted=data.is_weighted(), is_edge_mirrored=True, overide=overide)
