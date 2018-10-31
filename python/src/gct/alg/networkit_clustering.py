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
