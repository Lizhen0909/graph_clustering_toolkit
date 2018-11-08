import gct.alg
from gct.alg import cggc_clustering, clustering, dct_clustering, igraph_clustering, \
    mcl_clustering, networkit_clustering, OSLOM_clustering, powergraph_clustering, \
    PyCABeM_clustering, scan_clustering, sklearn_clustering, snap_clustering, \
    unsorted_clustering

from gct.alg.function import *
from gct.alg.function import __ALG_LIST__

def list_algorithms():
    return __ALG_LIST__


def run_alg(runname, data, algname, **algparams):
    if algname not in __ALG_LIST__:
        raise Exception ("algorithm {} not found. Available algorithms:\n" + str(list_algorithms()))
    fun = getattr(gct.alg, algname)
    return fun(name=runname, graph=data, **algparams)

from gct.alg.clustering import load_result as load_clustering_result, has_result as has_clustering_result

