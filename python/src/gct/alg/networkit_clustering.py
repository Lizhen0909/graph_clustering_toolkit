'''
Created on Oct 27, 2018

@author: lizhen
'''
from gct.dataset import convert
import igraph    
from gct.alg.clustering import Clustering, save_result
from gct import utils
import networkit


class LPDegreeOrdered(Clustering):
    '''
    A wrapper of *LPDegreeOrdered* algorithm from NetworKit. 
    Label propagation-based community detection algorithm which processes nodes in increasing order of node degree.
    
    Arguments
    --------------------
    None

    Reference 
    ------------------------
    TBD
    '''
    def __init__(self):
        name = "networkit-LPDegreeOrdered"
        super(LPDegreeOrdered, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"networkit", "name": 'LPDegreeOrdered' }
    
    def run(self, data):
        if False and (data.is_directed())  :
            raise Exception("only undirected is supported")
        g = convert.to_networkit(data)
        timecost, ret = utils.timeit(lambda: networkit.community.detectCommunities(g, algo=networkit.community.LPDegreeOrdered(g)))
        clusters = {}
        for c in ret.getSubsetIds():
            clusters[c] = list(ret.getMembers(c))
            
        self.logger.info("Made %d clusters in %f seconds." % (len(clusters), timecost))
        
        result = {}
        result['timecost'] = timecost
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 

 
class CutClustering(Clustering):
    '''
    A wrapper of *CutClustering* algorithm from NetworKit. 
    
    Arguments
    --------------------
    None

    Reference
    ------------------------
    Tarjan, Robert E.; Tsioutsiouliklis, Kostas. Graph Clustering and Minimum Cut Trees. Internet Mathematics 1 (2003), no. 4, 385–408.
    '''
    def __init__(self):
        name = "networkit-CutClustering"
        super(CutClustering, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"networkit", "name": 'CutClustering' }
    
    def run(self, data, alpha=0.1):
        if False and (data.is_directed())  :
            raise Exception("only undirected is supported")
        
        params = {'alpha':alpha}
        g = convert.to_networkit(data)
        fun = lambda: networkit.community.detectCommunities(g, algo=networkit.community.CutClustering(g, alpha=alpha))
        timecost, ret = utils.timeit(fun)
        clusters = {}
        for c in ret.getSubsetIds():
            clusters[c] = list(ret.getMembers(c))
            
        self.logger.info("Made %d clusters in %f seconds." % (len(clusters), timecost))
        
        result = {}
        result['params'] = params         
        result['timecost'] = timecost
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 


class PLP(Clustering):
    '''
    A wrapper of *PLP (Parallel Label Propagation)* algorithm from NetworKit. 
    Parallel label propagation for community detection: Moderate solution quality, very short time to solution.

    As described in Ovelgoenne et al: An Ensemble Learning Strategy for Graph Clustering Raghavan et al. proposed 
    a label propagation algorithm for graph clustering. This algorithm initializes every vertex of a graph with a 
    unique label. Then, in iterative sweeps over the set of vertices the vertex labels are updated. A vertex gets 
    the label that the maximum number of its neighbors have. The procedure is stopped when every vertex has the 
    label that at least half of its neighbors have.
    
    Arguments
    --------------------
    None

    Reference
    ------------------------
    TBD
    '''
    def __init__(self):
        name = "networkit-PLP"
        super(PLP, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"networkit", "name": 'PLP' }
    
    def run(self, data, updateThreshold=None, maxIterations=None):
        if False and (data.is_directed())  :
            raise Exception("only undirected is supported")
        
        params = {"updateThreshold": updateThreshold, 'maxIterations':maxIterations }
        params = {k:v for k, v in params.items() if v is not None }
        g = convert.to_networkit(data)
        fun = lambda: networkit.community.detectCommunities(g, algo=networkit.community.PLP(g, **params))
        timecost, ret = utils.timeit(fun)
        clusters = {}
        for c in ret.getSubsetIds():
            clusters[c] = list(ret.getMembers(c))
            
        self.logger.info("Made %d clusters in %f seconds." % (len(clusters), timecost))
        
        result = {}
        result['params'] = params 
        result['timecost'] = timecost
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 


class PLM(Clustering):
    '''
    A wrapper of *PLM (Parallel Louvain Method)* algorithm from NetworKit. 
    Parallel Louvain Method - the Louvain method, optionally extended to a full multi-level algorithm with refinement

    Arguments
    --------------------
    refine (bool, optional) – Add a second move phase to refine the communities.
    gamma (double) – Multi-resolution modularity parameter: 1.0 -> standard modularity 0.0 -> one community 2m -> singleton communities
    par (string) – parallelization strategy
    maxIter (count) – maximum number of iterations for move phase
    turbo (bool, optional) – faster but uses O(n) additional memory per thread
    recurse (bool, optional) – use recursive coarsening, see http://journals.aps.org/pre/abstract/10.1103/PhysRevE.89.049902 for some explanations (default: true)

    Reference
    ------------------------
    TBD
    '''
    def __init__(self):
        name = "networkit-PLM"
        super(PLM, self).__init__(name) 
    
    def get_meta(self):
        return {'lib':"networkit", "name": 'PLM' }
    
    def run(self, data, refine=False, gamma=1.0, par="balanced", maxIter=32, turbo=True, recurse=True):
        if False and (data.is_directed())  :
            raise Exception("only undirected is supported")
        
        params = locals();del params['data'];del params['self']
        
        g = convert.to_networkit(data)
        fun = lambda: networkit.community.detectCommunities(g, algo=networkit.community.PLM(g, **params))
        timecost, ret = utils.timeit(fun)
        clusters = {}
        for c in ret.getSubsetIds():
            clusters[c] = list(ret.getMembers(c))
            
        self.logger.info("Made %d clusters in %f seconds." % (len(clusters), timecost))
        
        result = {}
        result['params'] = params 
        result['timecost'] = timecost
        result['algname'] = self.name
        result['dataname'] = data.name
        result['meta'] = self.get_meta()
        result['clusters'] = clusters 

        save_result(result)
        self.result = result 
        return self 
