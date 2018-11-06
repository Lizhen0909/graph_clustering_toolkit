from .dataset import local_exists as local_graph_exists, load_local as load_local_graph, \
    list_local as list_local_graph, remove_local as remove_local_graph, list_all_clustering as list_all_clustering_results, \
    list_clustering as list_clustering_result
    
from .random_dataset import generate_LFR as generate_random_graph_LFR, generate_Erdos_Renyi as generate_random_graph_Erdos_Renyi   


def generate_undirected_unweighted_random_graph_LFR(name, N, k=None, maxk=None, mut=None, beta=None, t1=None, t2=None, minc=None, \
                maxc=None, on=None, om=None, C=None, seed=None, overide=False):
    params = locals()
    params['muw'] = 0
    params['a'] = 0
    params['weighted'] = False
    return generate_random_graph_LFR(**params)


def generate_directed_unweighted_random_graph_LFR(name, N, k=None, maxk=None, mut=None, beta=None, t1=None, t2=None, minc=None, \
                maxc=None, on=None, om=None, C=None, seed=None, overide=False):
    params = locals()
    params['muw'] = 0
    params['a'] = 1
    params['weighted'] = False
    return generate_random_graph_LFR(**params)


def generate_undirected_weighted_random_graph_LFR(name, N, k=None, maxk=None, mut=None, muw=None, beta=None, t1=None, t2=None, \
                minc=None, maxc=None, on=None, om=None, C=None, seed=None, overide=False):
    params = locals()
    params['a'] = 0
    params['weighted'] = True 
    return generate_random_graph_LFR(**params)


def generate_directed_weighted_random_graph_LFR(name, N, k=None, maxk=None, mut=None, muw=None, beta=None, t1=None, t2=None, \
                minc=None, maxc=None, on=None, om=None, C=None, seed=None, overide=False):
    params = locals()
    params['a'] = 1
    params['weighted'] = True 
    return generate_random_graph_LFR(**params)
