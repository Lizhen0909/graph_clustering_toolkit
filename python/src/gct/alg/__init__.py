import gct.alg

__ALG_LIST__ = []


def pycabem_GANXiSw(name, graph, **kwargs):
    '''
    None
    '''
    obj = gct.alg.PyCABeM_clustering.GANXiSw(name)
    return obj.run(graph, **kwargs)


def pycabem_HiReCS(name, graph, **kwargs):
    '''
    None
    '''
    obj = gct.alg.PyCABeM_clustering.HiReCS(name)
    return obj.run(graph, **kwargs)


def pycabem_LabelRank(name, graph, **kwargs):
    '''
    None
    '''
    obj = gct.alg.PyCABeM_clustering.LabelRank(name)
    return obj.run(graph, **kwargs)


__ALG_LIST__ += ['GANXiSw', 'HiReCS', 'LabelRank']


def list_algorithms():
    return __ALG_LIST__


def run_alg(runname, algname, params):
    if algname not in __ALG_LIST__:
        raise Exception ("algorithm {} not found. Available algorithms:\n" + str(list_algorithms()))
    fun = getattr(gct.alg, algname)
    return fun(runname, **params)
